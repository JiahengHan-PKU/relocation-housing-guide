"""Look up coordinates for one address."""

import json
import urllib.parse
import urllib.request

from city_config import load_city


def geocode_address(address):
    """Geocode a street address in the configured city with OpenStreetMap Nominatim.

    Args:
        address: Street address without city or state.

    Returns:
        A (lat, lon) tuple, or None if nothing matched.
    """
    query = urllib.parse.quote(f"{address}, {load_city()['geocode_suffix']}")
    url = f"https://nominatim.openstreetmap.org/search?format=json&limit=1&q={query}"
    request = urllib.request.Request(url, headers={"User-Agent": "housing-map/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        results = json.load(response)
    if not results:
        return None
    return float(results[0]["lat"]), float(results[0]["lon"])
