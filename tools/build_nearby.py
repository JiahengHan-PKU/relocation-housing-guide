"""Write nearby.csv from pois.json and the building table."""

import csv
import json
import os

from nearest_pois import nearest_pois


def build_nearby(table_path, pois_path, out_path, routes_path="data/poi_routes.json"):
    """Summarize nearby places for each included building.

    Args:
        table_path: Path to data/buildings.csv.
        pois_path: Path to data/pois.json from fetch_pois.py.
        out_path: Path to data/nearby.csv.
        routes_path: Optional data/poi_routes.json from route_pois.py, used for
            street-network walking distances when present.

    Returns:
        The number of rows written.
    """
    pois = [dict(p, i=i) for i, p in enumerate(json.load(open(pois_path)))]
    routes = json.load(open(routes_path)) if os.path.exists(routes_path) else {}
    rows = []
    for row in csv.DictReader(open(table_path)):
        if row["status"] == "include" and row["lat"]:
            found = {"building_id": row["id"]}
            for key, value in nearest_pois(float(row["lat"]), float(row["lon"]), pois, routes.get(row["id"])).items():
                if isinstance(value, tuple):
                    found[f"{key}_name"], found[f"{key}_m"] = value
                else:
                    found[key] = value
            rows.append(found)
    with open(out_path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["building_id"])
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    print(build_nearby("data/buildings.csv", "data/pois.json", "data/nearby.csv"))
