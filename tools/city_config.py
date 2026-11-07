"""Load the city settings that every tool shares."""

import json
import os


def load_city(path=None):
    """Return the settings in config/city.json.

    Args:
        path: Optional file path. The CITY_CONFIG environment variable, then
            config/city.json under the repository root, are used otherwise.

    Returns:
        A dict with office, basemap, strings and the other city settings.
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = path or os.environ.get("CITY_CONFIG") or os.path.join(root, "config", "city.json")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)
