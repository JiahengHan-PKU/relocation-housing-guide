"""Download the walkable street network around the buildings."""

import json
import urllib.request

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
EXCLUDE = "motorway|motorway_link|construction|proposed|raceway|bus_guideway|escape"


def fetch_walk_network(bbox, out_path):
    """Save every way a pedestrian can use inside a bounding box.

    Includes streets, sidewalks, footways, paths, steps, crossings and
    service roads, and leaves out motorways and ways tagged foot=no or
    access=private. One Overpass request.

    Args:
        bbox: "south,west,north,east" in degrees.
        out_path: JSON file for the raw Overpass response (ways with node ids
            and geometry).

    Returns:
        The number of ways saved.
    """
    query = f"""[out:json][timeout:180];
way["highway"]["highway"!~"^({EXCLUDE})$"]["foot"!="no"]["access"!~"^(private|no)$"]({bbox});
out geom;"""
    request = urllib.request.Request(OVERPASS_URL, data=query.encode(), headers={"User-Agent": "housing-map/1.0"})
    with urllib.request.urlopen(request, timeout=240) as response:
        data = json.load(response)
    json.dump(data, open(out_path, "w"))
    return len(data["elements"])


if __name__ == "__main__":
    from city_config import load_city
    print(fetch_walk_network(",".join(map(str, load_city()["pois_bbox"])), "data/walk_network_raw.json"))
