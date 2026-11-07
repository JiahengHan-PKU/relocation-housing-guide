"""Build a page for a fictional city from an empty folder and open it."""

import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICTION = "Fictional test data. These buildings do not exist."
BUILDINGS = [("harbor-one", "Harbor One", 40.001, -75.001, 2018, 30, 300, "rental", "A"),
             ("mill-lofts", "Mill Lofts", 40.004, -75.003, 2004, 12, 120, "condo", "C"),
             ("park-tower", "Park Tower", 39.998, -74.998, 2022, 45, 410, "rental", "B")]


def fill_demo(root):
    """Write the fictional config and tables into a scaffolded folder."""
    city = json.load(open(f"{root}/config/city.example.json"))
    city.update(as_of="2030-01-01", output="dist/demo.html", geocode_suffix="Demo City, ZZ")
    city["office"] = {"lat": 40.0, "lon": -75.0, "address": "1 Demo Plaza"}
    city["page"]["annual_base"] = 120000
    city["page"]["strings"]["en"].update(title="Demo City Guide", subtitle=FICTION + " Data as of ")
    json.dump(city, open(f"{root}/config/city.json", "w"))
    header = open(f"{root}/data/buildings.csv").readline().strip().split(",")
    with open(f"{root}/data/buildings.csv", "a") as table, open(f"{root}/data/listings.csv", "a") as listings:
        for n, (id_, name, lat, lon, year, floors, units, kind, channel) in enumerate(BUILDINGS):
            values = dict(id=id_, name=name, address=f"{n + 1} Demo St", zip="00001", lat=lat, lon=lon, neighborhood="Demo",
                          year_built=year, floors=floors, units=units, building_type=kind, channel_primary=channel,
                          channels_all=channel, walk_m=400 * (n + 1), walk_min=5 * (n + 1), status="include",
                          summary_en=FICTION, summary_zh=FICTION, as_of="2030-01-01")
            table.write(",".join(str(values.get(col, "")) for col in header) + "\n")
            for i, rent in enumerate([2500, 2700, 2900]):
                listings.write(f"{id_}-{i},{id_},1b,1,700,{rent + 300 * n},unit,false,12,,,Official site,https://example.com/{id_},2030-01-01\n")
                json.dump({"id": id_, "pages": []}, open(f"{root}/data/raw/amenity_text/{id_}.json", "w"))
    with open(f"{root}/data/cost_assumptions.csv", "a") as handle:
        for item, value in [("electricity_rate", 0.15), ("electricity_use", 0.9), ("water_sewer", 40), ("internet", 55),
                            ("renters_insurance", 26), ("sales_tax", 0), ("required_fees", 100)]:
            handle.write(f"{item},{value},demo,always,https://example.com,2030-01-01,{FICTION}\n")
    json.dump({key: [] for key in ["sea", "land", "water", "park", "building", "road", "rail"]},
              open(f"{root}/web/basemap.json", "w"))


def smoke_test():
    """Run the pipeline without network and check the page in a browser."""
    with tempfile.TemporaryDirectory() as tmp:
        for name in ["tools", "web", "vendor", "config"]:
            shutil.copytree(f"{ROOT}/{name}", f"{tmp}/{name}", ignore=shutil.ignore_patterns("city.json", "data.json", "basemap.json", "__pycache__"))
        subprocess.run([sys.executable, "tools/new_city.py", "."], cwd=tmp, check=True)
        fill_demo(tmp)
        env = {**os.environ, "PYTHONPATH": "tools"}
        for step in [["tools/extract_amenities.py"], ["tools/build_contacts.py"], ["tools/export_data.py"], ["tools/build_page.py"]]:
            subprocess.run([sys.executable, *step], cwd=tmp, check=True, env=env)
        page = f"{tmp}/dist/demo.html"
        assert os.path.getsize(page) > 100000
        subprocess.run([sys.executable, "tools/build_summary.py"], cwd=tmp, check=True, env=env)
        assert os.path.getsize(f"{tmp}/dist/summary.html") > 1000
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("page built; install playwright to check it in a browser")
            return
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel="chrome", headless=True)
            tab = browser.new_page()
            errors = []
            tab.on("pageerror", lambda error: errors.append(str(error)))
            tab.goto(f"file://{page}")
            tab.wait_for_timeout(800)
            tab.evaluate("location.hash='b-harbor-one'")
            tab.wait_for_timeout(300)
            body = tab.inner_text("body")
            assert not errors, errors
            assert "Harbor One" in body and "$120,000" in body
            summary = browser.new_page()
            summary.goto(f"file://{tmp}/dist/summary.html")
            assert summary.pdf(prefer_css_page_size=True)[:4] == b"%PDF"
            blocked = browser.new_context(java_script_enabled=False).new_page()
            blocked.goto(f"file://{page}")
            assert "blocks scripts" in blocked.inner_text("body")
        print("smoke test passed")


if __name__ == "__main__":
    smoke_test()
