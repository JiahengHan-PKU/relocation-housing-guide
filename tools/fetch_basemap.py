"""Download the raw OpenStreetMap layers used to draw the basemap."""

import json
import urllib.parse
import urllib.request

from city_config import load_city

MAP = load_city()["basemap"]
BBOX = ",".join(map(str, MAP["detail_bbox"]))
WIDE = ",".join(map(str, MAP["wide_bbox"]))
QUERY = f"""[out:json][timeout:180];
(way["highway"~"^(motorway|trunk|primary|secondary|tertiary|residential|unclassified|living_street|pedestrian)$"]({BBOX});
 way["highway"~"^(motorway|trunk|primary|secondary|tertiary)$"]({WIDE});
 way["natural"="coastline"]({WIDE});
 way["natural"="water"]({WIDE}); relation["natural"="water"]({WIDE});
 way["waterway"="riverbank"]({WIDE});
 way["leisure"="park"]({WIDE}); relation["leisure"="park"]({WIDE});
 way["building"]({BBOX});
 way["railway"~"monorail|subway|light_rail"]({WIDE}););
out geom;"""


def fetch_basemap(out_path):
    """Save street, coastline, water, park, building and rail geometry.

    Args:
        out_path: JSON file for the raw Overpass response.
    """
    request = urllib.request.Request(
        "https://overpass-api.de/api/interpreter",
        data=urllib.parse.urlencode({"data": QUERY}).encode(),
        headers={"User-Agent": "housing-map/1.0"})
    with urllib.request.urlopen(request, timeout=180) as response:
        json.dump(json.load(response), open(out_path, "w"))


if __name__ == "__main__":
    fetch_basemap("data/basemap_raw.json")
