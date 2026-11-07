"""Download points of interest around the city center from OpenStreetMap."""

import json
import urllib.parse
import urllib.request

from city_config import load_city

QUERY = """[out:json][timeout:90];
(nwr["shop"="supermarket"]({POIS_BBOX});
 nwr["shop"~"convenience|chemist"]({POIS_BBOX});
 nwr["amenity"="pharmacy"]({POIS_BBOX});
 nwr["railway"~"station|halt"]({POIS_BBOX});
 node["highway"="bus_stop"]({POIS_BBOX});
 nwr["amenity"~"restaurant|cafe"]({POIS_BBOX});
 nwr["leisure"~"park|fitness_centre"]({POIS_BBOX}););
out center tags;"""


def fetch_pois(out_path):
    """Save supermarkets, pharmacies, transit, restaurants and parks to JSON.

    Args:
        out_path: File to write; a list of {kind, name, brand, lat, lon}.
    """
    request = urllib.request.Request(
        "https://overpass-api.de/api/interpreter",
        data=urllib.parse.urlencode({"data": QUERY.replace("{POIS_BBOX}", ",".join(map(str, load_city()["pois_bbox"])))}).encode(),
        headers={"User-Agent": "housing-map/1.0"})
    elements = json.load(urllib.request.urlopen(request, timeout=120))["elements"]
    pois = []
    for element in elements:
        tags = element.get("tags", {})
        point = element.get("center") or element
        kind = (tags.get("shop") or tags.get("railway") or tags.get("highway")
                or tags.get("amenity") or tags.get("leisure"))
        pois.append({"kind": kind, "name": tags.get("name"),
                     "brand": tags.get("brand"), "network": tags.get("network"),
                     "mode": tags.get("station") or tags.get("subway") and "subway" or tags.get("monorail") and "monorail",
                     "lat": point.get("lat"), "lon": point.get("lon")})
    json.dump(pois, open(out_path, "w"), indent=0)


if __name__ == "__main__":
    fetch_pois("data/pois.json")
