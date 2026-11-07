"""Validate redrawn floor plan JSON files."""

import json
import sys


def check_floorplan(path):
    """Check every plan in a building's floor plan file.

    A plan fails when a field is missing, a room (other than a balcony or
    terrace) sits outside the outline, or the interior rooms add up to less
    than 75% or more than 110% of the official square footage.

    Args:
        path: data/floorplans/<building>.json.

    Returns:
        A list of (plan, problem) tuples; empty when everything passes.
    """
    problems = []
    for fp in json.load(open(path)):
        name = fp.get("plan", "?")
        for key in ["building_id", "plan", "unit_type", "beds", "baths", "sqft", "source_image", "width_ft", "depth_ft", "rooms"]:
            if fp.get(key) in (None, "", []):
                problems.append((name, f"missing {key}"))
        inside = [r for r in fp.get("rooms", []) if r["type"] not in ("balcony", "terrace")]
        for r in inside:
            if r["x"] < -0.1 or r["y"] < -0.1 or r["x"] + r["w"] > fp["width_ft"] + 0.3 or r["y"] + r["h"] > fp["depth_ft"] + 0.3:
                problems.append((name, f"room {r['label']} outside outline"))
        area = sum(r["w"] * r["h"] for r in inside)
        if fp.get("sqft") and not 0.75 <= area / fp["sqft"] <= 1.10:
            problems.append((name, f"rooms cover {area:.0f} ft2 vs official {fp['sqft']}"))
    return problems


if __name__ == "__main__":
    result = check_floorplan(sys.argv[1])
    print("OK" if not result else "\n".join(f"{p}: {m}" for p, m in result))
