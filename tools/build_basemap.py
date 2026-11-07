"""Turn raw OpenStreetMap layers into a compact basemap for the page."""

import json

from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import linemerge, polygonize, unary_union

from city_config import load_city

MAP = load_city()["basemap"]
SOUTH, WEST, NORTH, EAST = MAP["wide_bbox"]
BBOX = (WEST, SOUTH, EAST, NORTH)
BAY_POINTS = [tuple(p) for p in MAP.get("sea_points", [])]
ROAD_CLASSES = {"motorway": 1, "trunk": 1, "primary": 2, "secondary": 2,
                "tertiary": 3, "residential": 4, "unclassified": 4,
                "living_street": 4, "pedestrian": 5}


def build_basemap(raw_path, out_path):
    """Write land, water, parks, buildings, roads and rail as rounded arrays.

    Land is found by splitting the bounding box along the coastline and
    dropping faces that contain a known sea point from the city config.

    Args:
        raw_path: Overpass JSON saved by fetch_basemap.
        out_path: Compact JSON consumed by the page.
    """
    elements = json.load(open(raw_path))["elements"]
    r = lambda coords: [[round(y, 5), round(x, 5)] for x, y in coords]
    ring = lambda e: [(p["lon"], p["lat"]) for p in e.get("geometry", [])]
    out = {"sea": [], "land": [], "water": [], "park": [], "building": [], "road": [], "rail": []}
    coast = [LineString(ring(e)) for e in elements if e.get("tags", {}).get("natural") == "coastline"]
    frame = box(*BBOX)
    faces = polygonize(unary_union([frame.boundary, linemerge(coast)]))
    for face in faces:
        if not face.within(frame.buffer(1e-6)):
            continue
        layer = "sea" if any(face.contains(Point(p)) for p in BAY_POINTS) else "land"
        out[layer].append(r(face.simplify(0.00003).exterior.coords))
    for e in elements:
        tags = e.get("tags", {})
        if e["type"] == "relation" and (tags.get("natural") == "water" or tags.get("leisure") == "park"):
            outers = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
                      for m in e.get("members", []) if m.get("role") == "outer" and len(m.get("geometry", [])) > 1]
            layer = "water" if tags.get("natural") == "water" else "park"
            for polygon in polygonize(linemerge(outers)):
                clipped = polygon.intersection(frame)
                for part in getattr(clipped, "geoms", [clipped]):
                    if part.geom_type == "Polygon" and not part.is_empty:
                        out[layer].append(r(part.simplify(0.00002).exterior.coords))
    for e in elements:
        tags, pts = e.get("tags", {}), ring(e)
        if e["type"] != "way" or len(pts) < 2:
            continue
        if tags.get("natural") == "water" or tags.get("waterway") == "riverbank":
            out["water"].append(r(Polygon(pts).simplify(0.00002).exterior.coords))
        elif tags.get("leisure") == "park" and len(pts) > 3:
            out["park"].append(r(Polygon(pts).simplify(0.00002).exterior.coords))
        elif "building" in tags and len(pts) > 3:
            polygon = Polygon(pts)
            if polygon.area > 2e-9:
                out["building"].append(r(polygon.simplify(0.000008).exterior.coords))
        elif tags.get("highway") in ROAD_CLASSES:
            out["road"].append([ROAD_CLASSES[tags["highway"]], tags.get("name"),
                                r(LineString(pts).simplify(0.00001).coords)])
        elif tags.get("railway") in ("monorail", "subway", "light_rail"):
            out["rail"].append(["mover" if tags["railway"] == "monorail" else "rail",
                                r(LineString(pts).simplify(0.00001).coords)])
    json.dump(out, open(out_path, "w"), separators=(",", ":"))
    return {key: len(value) for key, value in out.items()}


if __name__ == "__main__":
    print(build_basemap("data/basemap_raw.json", "web/basemap.json"))
