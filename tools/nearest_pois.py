"""Summarize what is near each building."""

import math

from city_config import load_city


def transit_match(poi, rule):
    """Return True when a station matches {modes: [...]} or {network: word}."""
    if "network" in rule:
        return rule["network"] in str(poi["network"]).lower()
    return poi["kind"] in ("station", "halt") and str(poi.get("mode")) in rule["modes"]


def nearest_pois(lat, lon, pois):
    """Find the nearest place of each kind and count nearby restaurants.

    Distances are straight-line meters times 1.25, a typical street-grid
    detour factor, so they approximate walking distance.

    Args:
        lat: Building latitude.
        lon: Building longitude.
        pois: List of {kind, name, brand, network, lat, lon}.

    Returns:
        A dict mapping each category to (name, meters), plus counts. Brands and
        transit lines come from the `nearby` block of the city config.
    """
    city = load_city().get("nearby", {})

    def meters(poi):
        dx = math.radians(poi["lon"] - lon) * math.cos(math.radians(lat))
        dy = math.radians(poi["lat"] - lat)
        return 6371000 * math.hypot(dx, dy) * 1.25

    groups = {"supermarket": lambda p: p["kind"] == "supermarket"}
    for key, word in city.get("brands", {}).items():
        groups[key] = lambda p, word=word: word in f"{p['name']} {p['brand']}".lower()
    groups["pharmacy"] = lambda p: p["kind"] in ("pharmacy", "chemist")
    for key, rule in city.get("transit", {}).items():
        groups[key] = lambda p, rule=rule: transit_match(p, rule)
    groups.update({"bus_stop": lambda p: p["kind"] == "bus_stop",
                   "park": lambda p: p["kind"] == "park" and p["name"],
                   "gym": lambda p: p["kind"] == "fitness_centre"})
    result = {}
    for key, test in groups.items():
        found = [(meters(p), p["name"]) for p in pois if test(p) and p["lat"]]
        result[key] = (min(found)[1], round(min(found)[0])) if found else (None, None)
    result["restaurants_400m"] = sum(
        1 for p in pois if p["kind"] in ("restaurant", "cafe") and p["lat"] and meters(p) <= 400)
    result["bus_stops_300m"] = sum(
        1 for p in pois if p["kind"] == "bus_stop" and p["lat"] and meters(p) <= 300)
    return result
