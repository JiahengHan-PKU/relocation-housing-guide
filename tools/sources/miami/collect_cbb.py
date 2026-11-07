"""Collect floor plan and amenity data from Condo Black Book building pages."""

import csv
import json
import os
import re
import sys
import time

from playwright.sync_api import sync_playwright

BASE = "https://www.condoblackbook.com"
AREAS = ["brickell", "brickell-key", "downtown-miami", "miami-river"]
OVERRIDES = {"solaris-brickell": ["solaris-at-brickell"], "met-1": ["met1"],
             "latitude-river": ["latitude"], "brickell-east": ["brickell-east"], "501-first": ["501-first"], "icon-brickell": ["icon-brickell-one", "icon-brickell-ii"], "w-residences": ["icon-brickell-iii-w-miami"],
             "rise": ["rise-brickell-city-center"], "reach": ["brickell-city-centre-reach"],
             "mark-on-brickell": ["the-mark"], "jade-brickell": ["jade"], "palace-brickell": ["the-palace-condo"],
             "villa-regina": ["villa-regina-condo"], "four-seasons": ["the-four-seasons-residences"], "epic-miami": ["epic"],
             "axis-brickell": ["axis"], "wind-neo": ["wind-by-neo"], "mybrickell": ["my-brickell"],
             "tequesta-one": ["one-tequesta-point"], "tequesta-two": ["two-tequesta-point"], "tequesta-three": ["three-tequesta-point"],
             "imperial-brickell": ["imperial-at-brickell"], "infinity-brickell": ["infinity-at-brickell"],
             "brickell-key-one": ["brickell-key-i"], "brickell-key-two": ["brickell-key-ii"], "courts-brickell-key": ["courts-condo"],
             "club-brickell-bay": ["the-club-at-brickell-bay", "club-at-brickell-bay"], "the-plaza-brickell": ["plaza-on-brickell-north", "the-plaza-on-brickell", "plaza-on-brickell", "the-plaza-on-brickell-i"],
             "avenue-on-brickell": ["avenue-1060-brickell", "1060-brickell", "1050-brickell", "avenue-on-brickell"], "brickell-on-the-river": ["brickell-on-the-river", "brickell-on-the-river-north", "brickell-on-the-river-south"],
             "nine-mary-brickell": ["nine-at-mary-brickell-village", "nine-at-mary-brickell"], "millecento": ["1100-millecento"],
             "ivy-riverfront": ["the-ivy", "ivy"], "mint-riverfront": ["mint"], "the-bond": ["the-bond", "bond-on-brickell"],
             "sls-brickell": ["dua-miami-(sls-hotel-and-residences)"], "sail-brickell": ["the-sail", "sail-on-brickell"], "vue-brickell": ["the-vue-at-brickell", "vue-at-brickell"]}


SAME_BUILDING = {"501-first": "121 NE 5th St"}  # Corner building; CBB uses the side-street address.


def candidates(row):
    """Return slug guesses for a building, most specific first."""
    name = re.sub(r"[^a-z0-9]+", "-", row["name"].lower()).strip("-")
    short = re.sub(r"(^the-|-brickell$|-at-brickell$|-on-brickell$|-residences$)", "", name)
    return list(dict.fromkeys(OVERRIDES.get(row["id"], []) + [name, row["id"], short, name + "-condo", short + "-condo"]))


class RateLimited(Exception):
    """The site answered 429; stop rather than record a false miss."""


def read_building(page, url):
    """Return the embedded building record for a page, or None."""
    try:
        response = page.goto(url, wait_until="domcontentloaded", timeout=25000)
        if response and response.status == 429:
            raise RateLimited(url)
        if not response or response.status != 200:
            return None
        match = re.search(r"__NEXT_DATA__[^>]*>(.*?)</script>", page.content(), re.S)
        return json.loads(match.group(1))["props"]["pageProps"].get("building") if match else None
    except RateLimited:
        raise
    except Exception:
        return None


def collect_cbb(buildings_path, out_dir):
    """Save <id>.json for each building whose page address matches ours.

    Args:
        buildings_path: Path to data/buildings.csv.
        out_dir: Folder for the per-building output.
    """
    rows = [r for r in csv.DictReader(open(buildings_path)) if r["status"] == "include"]
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        for row in rows:
            path = f"{out_dir}/{row['id']}.json"
            if os.path.exists(path):
                continue
            number = re.match(r"\d+", row["address"]).group(0)
            found = None
            for slug in candidates(row):
                for area in AREAS:
                    url = f"{BASE}/{area}/{slug}"
                    building = read_building(page, url)
                    time.sleep(8)
                    if building and (number in str(building.get("primaryAddress")) or SAME_BUILDING.get(row["id"], "\0") in str(building.get("primaryAddress"))):
                        found = (url, building)
                        break
                    if building:
                        print("address mismatch", row["id"], url, building.get("primaryAddress"), flush=True)
                if found:
                    break
            url, building = found or (None, {})
            json.dump({"id": row["id"], "url": url, "building": building}, open(path, "w"), ensure_ascii=False)
            print(row["id"], url, len(building.get("floorplans") or []), flush=True)
        browser.close()


if __name__ == "__main__":
    collect_cbb(sys.argv[1], sys.argv[2])
