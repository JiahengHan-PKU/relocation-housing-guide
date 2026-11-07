"""Save the amenity text of every building's official and condo pages."""

import csv
import json
import os
import re
import sys
import time

from playwright.sync_api import sync_playwright

BASE = "https://www.miamicondosolution.com"
AREAS = ["brickell-avenue", "downtown-miami", "brickell-key"]


def page_text(page, url):
    """Return (status, text, links) for a URL, or (0, '', []) on failure."""
    try:
        response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(1800)
        links = page.eval_on_selector_all("a[href]", "e => e.map(a => a.href)")
        return response.status if response else 0, page.inner_text("body"), links
    except Exception:
        return 0, "", []


def collect_amenity_text(buildings_path, listings_path, out_dir):
    """Write <id>.json with the text of each page that describes amenities.

    Args:
        buildings_path: Path to data/buildings.csv.
        listings_path: Path to data/listings.csv, used to find condo page slugs.
        out_dir: Folder for the per-building output.
    """
    slugs = {}
    for row in csv.DictReader(open(listings_path)):
        match = re.search(r"miamicondosolution\.com/rental/(.+)\.htm", row["source_url"])
        if match:
            slugs.setdefault(row["building_id"], match.group(1))
    buildings = [r for r in csv.DictReader(open(buildings_path)) if r["status"] == "include"]
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        for n, b in enumerate(buildings, 1):
            path = f"{out_dir}/{b['id']}.json"
            if os.path.exists(path):
                continue
            pages = []
            if b["id"] in slugs:
                for area in AREAS:
                    url = f"{BASE}/{area}/{slugs[b['id']]}.htm"
                    status, text, _ = page_text(page, url)
                    time.sleep(1)
                    if status == 200 and re.search("amenit|pool|fitness", text, re.I):
                        pages.append({"url": url, "text": text[:14000]})
                        break
            if b["official_url"]:
                status, text, links = page_text(page, b["official_url"])
                time.sleep(1)
                if status == 200:
                    pages.append({"url": b["official_url"], "text": text[:9000]})
                    found = [u for u in links if re.search("amenit|feature", u, re.I)][:1]
                    for url in found:
                        status, text, _ = page_text(page, url)
                        time.sleep(1)
                        if status == 200:
                            pages.append({"url": url, "text": text[:9000]})
            json.dump({"id": b["id"], "pages": pages}, open(path, "w"), ensure_ascii=False)
            print(n, b["id"], [p["url"][:60] for p in pages], flush=True)
        browser.close()


if __name__ == "__main__":
    collect_amenity_text(sys.argv[1], sys.argv[2], sys.argv[3])
