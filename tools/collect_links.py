"""Collect tour, leasing and contact links from official building sites."""

import csv
import json
import os
import re
import sys
import time

from playwright.sync_api import sync_playwright

KEEP = re.compile(r"tour|schedule|appointment|apply|application|availab|floor.?plan|lease|leasing|contact|matterport|realync|sightmap|engrain|tel:|mailto:|3d|virtual", re.I)


def collect_links(buildings_path, out_dir):
    """Save the relevant links and embedded tours of each official site.

    Args:
        buildings_path: Path to data/buildings.csv.
        out_dir: Folder for the per-building output.
    """
    rows = [r for r in csv.DictReader(open(buildings_path)) if r["status"] == "include" and r["official_url"]]
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        for row in rows:
            path = f"{out_dir}/{row['id']}.json"
            if os.path.exists(path):
                continue
            links, frames, status = [], [], 0
            try:
                response = page.goto(row["official_url"], wait_until="domcontentloaded", timeout=30000)
                status = response.status if response else 0
                page.wait_for_timeout(2200)
                pairs = page.eval_on_selector_all("a[href]", "e => e.map(a => [a.href, (a.innerText || a.title || '').trim().slice(0, 50)])")
                links = sorted({(u, t) for u, t in pairs if KEEP.search(u + " " + t)})[:60]
                frames = [f.url for f in page.frames if re.search("matterport|realync|sightmap|engrain|tour", f.url, re.I)][:6]
            except Exception as error:
                print("failed", row["id"], str(error)[:80], flush=True)
            json.dump({"id": row["id"], "url": row["official_url"], "status": status, "links": links, "frames": frames},
                      open(path, "w"), ensure_ascii=False)
            print(row["id"], status, len(links), len(frames), flush=True)
            time.sleep(1)
        browser.close()


if __name__ == "__main__":
    collect_links(sys.argv[1], sys.argv[2])
