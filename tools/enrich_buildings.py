"""Build buildings.csv from building_seed.csv."""

import csv
import datetime
import time

from geocode_address import geocode_address
from city_config import load_city
from walk_route import walk_route

CITY = load_city()
OFFICE = (CITY["office"]["lat"], CITY["office"]["lon"])
WALK_METERS_PER_MINUTE = CITY.get("walk_meters_per_minute", 80)


def enrich_buildings(seed_path, facts_path, table_path):
    """Add coordinates and walking distance to every seeded building.

    Args:
        seed_path: Path to data/building_seed.csv.
        facts_path: Path to data/building_facts.csv.
        table_path: Path to data/buildings.csv, whose header sets the columns.
    """
    with open(table_path, newline="") as handle:
        columns = next(csv.reader(handle))
    with open(seed_path, newline="") as handle:
        seeds = list(csv.DictReader(handle))
    with open(facts_path, newline="") as handle:
        facts = {row["id"]: row for row in csv.DictReader(handle)}
    today = datetime.date.today().isoformat()
    rows = []
    for seed in seeds:
        row = {column: seed.get(column, "") for column in columns}
        row["as_of"] = today
        row.update({k: v for k, v in facts.get(seed["id"], {}).items() if v})
        if seed["status"] == "exclude":
            rows.append(row)
            continue
        row["walk_verified"] = "false"
        point = None
        if seed["lat"]:
            point = float(seed["lat"]), float(seed["lon"])
        else:
            point = geocode_address(seed["address"])
            time.sleep(1.1)
        if point:
            row["lat"], row["lon"] = point
            distance = walk_route(point, OFFICE)
            row["walk_m"] = round(distance)
            row["walk_min"] = round(distance / WALK_METERS_PER_MINUTE, 1)
            row["walk_method"] = "osrm-foot"
            time.sleep(0.4)
        else:
            print("no coordinates:", seed["id"])
        rows.append(row)
    with open(table_path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    enrich_buildings(
        "data/building_seed.csv", "data/building_facts.csv", "data/buildings.csv"
    )
