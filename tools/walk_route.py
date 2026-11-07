"""Measure the walking route between two points."""

import json
import urllib.request


def walk_route(start, end):
    """Return the street-network walking distance between two points.

    Args:
        start: (lat, lon) of the origin.
        end: (lat, lon) of the destination.

    Returns:
        Distance in meters.
    """
    coordinates = f"{start[1]},{start[0]};{end[1]},{end[0]}"
    url = (
        "https://routing.openstreetmap.de/routed-foot/route/v1/foot/"
        f"{coordinates}?overview=false"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "housing-map/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)["routes"][0]["distance"]
