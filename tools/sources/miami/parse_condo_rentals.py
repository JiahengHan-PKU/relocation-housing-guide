"""Parse a Miami Condo Solution rental page into listing rows."""

import re

UNIT_TYPES = {"0": "studio", "1": "1b", "2": "2b"}


def parse_condo_rentals(text, building_id, source_url, observed_on):
    """Extract rental units from the visible text of a building's rental page.

    Args:
        text: Visible page text.
        building_id: Foreign key to buildings.id.
        source_url: Page the text came from.
        observed_on: Date seen, YYYY-MM-DD.

    Returns:
        A list of dicts using the listings.csv columns.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    rows = []
    for index, line in enumerate(lines):
        match = re.search(r"Unit #(\S+)$", line)
        if not match:
            continue
        block = lines[index + 1 : index + 14]
        if "BEDROOMS" not in block or "SQ FT" not in block:
            continue
        rent = re.sub(r"\D", "", block[block.index("RENT") + 1])
        beds = block[block.index("BEDROOMS") + 1]
        baths = block[block.index("BATHROOMS") + 1].split("/")[0].strip()
        sqft = re.sub(r"\D", "", block[block.index("SQ FT") + 1])
        rows.append({
            "listing_id": f"{building_id}-{match.group(1)}",
            "building_id": building_id,
            "unit_type": UNIT_TYPES.get(beds, "3b_plus"),
            "baths": baths,
            "sqft": sqft,
            "rent_usd": rent,
            "price_basis": "unit",
            "source_name": "Miami Condo Solution",
            "source_url": source_url,
            "observed_on": observed_on,
        })
    return rows
