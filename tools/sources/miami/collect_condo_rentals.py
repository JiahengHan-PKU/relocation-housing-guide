"""Collect listing rents for many buildings from Miami Condo Solution."""

import json
import re
import sys
import time

from playwright.sync_api import sync_playwright

from parse_condo_rentals import parse_condo_rentals

BASE = "https://www.miamicondosolution.com/rental/{}.htm"
VIEW_ALL = ("https://www.miamicondosolution.com/property-detail.php"
            "?cf=rental&pf={}&t={}&x=0&viewall=1&listViewType=list")


def collect_condo_rentals(slug_path, out_path, observed_on):
    """Render each building's rental page once and store parsed listings.

    Args:
        slug_path: JSON mapping building id to a list of page slugs.
        out_path: JSON file to write, mapping building id to listing rows.
        observed_on: Date seen, YYYY-MM-DD.
    """
    slugs = json.load(open(slug_path))
    result = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        for building_id, names in slugs.items():
            rows = []
            for name in names:
                url = BASE.format(name)
                try:
                    response = page.goto(url, wait_until="domcontentloaded", timeout=40000)
                    page.wait_for_timeout(2500)
                    text = page.inner_text("body")
                    total = re.search(r"(\d+) for rent", text)
                    found = parse_condo_rentals(text, building_id, url, observed_on)
                    if total and int(total.group(1)) > len(found):
                        page.goto(VIEW_ALL.format(name, total.group(1)),
                                  wait_until="domcontentloaded", timeout=40000)
                        page.wait_for_timeout(3000)
                        found = parse_condo_rentals(page.inner_text("body"), building_id, url, observed_on)
                    print(building_id, name, response.status, len(found), flush=True)
                    rows += found
                except Exception as error:
                    print(building_id, name, "ERROR", str(error)[:80], flush=True)
                time.sleep(1)
            result[building_id] = rows
            json.dump(result, open(out_path, "w"), indent=0)
        browser.close()


if __name__ == "__main__":
    collect_condo_rentals(sys.argv[1], sys.argv[2], sys.argv[3])
