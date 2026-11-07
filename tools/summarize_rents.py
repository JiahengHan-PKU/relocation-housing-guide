"""Compute rent statistics from listings.csv."""

import csv
import statistics
from collections import defaultdict


def summarize_rents(listings_path):
    """Summarize rent by building and unit type.

    Args:
        listings_path: Path to data/listings.csv.

    Returns:
        A dict keyed by (building_id, unit_type) holding min, median, max, n
        and basis. Unfurnished and unknown units are used first; if fewer than
        3 remain, all units are used and "includes_furnished" is True.
    """
    with open(listings_path, newline="") as handle:
        rows = list(csv.DictReader(handle))
    groups = defaultdict(list)
    for row in rows:
        groups[row["building_id"], row["unit_type"]].append(row)
    summary = {}
    for key, group in groups.items():
        chosen = [row for row in group if row["furnished"] != "true"]
        includes_furnished = len(chosen) < 3 and len(chosen) < len(group)
        chosen = group if includes_furnished else chosen
        rents = [float(row["rent_usd"]) for row in chosen]
        summary[key] = {
            "min": min(rents), "median": statistics.median(rents),
            "max": max(rents), "n": len(rents),
            "basis": sorted({row["price_basis"] for row in chosen}),
            "includes_furnished": includes_furnished,
        }
    return summary
