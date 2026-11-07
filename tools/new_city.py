"""Create an empty data folder and city config for a new city."""

import json
import os
import shutil
import sys

TABLES = {
    "building_seed.csv": "id,name,aliases,address,neighborhood,found_in,status,exclude_reason,lat,lon",
    "building_facts.csv": "id,official_url,year_built,floors,units,developer,architect,manager,building_type,channel_primary,channels_all,summary_en,summary_zh,photo_file,photo_source_url,photo_credit,photo_license,facts_source_urls,as_of",
    "buildings.csv": "id,name,aliases,address,zip,lat,lon,neighborhood,official_url,year_built,floors,units,developer,architect,manager,building_type,channel_primary,channels_all,walk_m,walk_min,walk_method,walk_verified,summary_en,summary_zh,photo_file,photo_source_url,photo_credit,photo_license,found_in,status,exclude_reason,facts_source_urls,as_of",
    "listings.csv": "listing_id,building_id,unit_type,baths,sqft,rent_usd,price_basis,furnished,lease_months,free_months,monthly_fees_usd,source_name,source_url,observed_on",
    "costs.csv": "building_id,item,amount_usd,frequency,counted,basis,source_url,notes",
    "cost_assumptions.csv": "item,value,unit,applies_when,source_url,observed_on,notes",
    "ratings.csv": "building_id,platform,group,score_raw,scale,score_5,review_count,latest_review_on,url,retrieved_via,observed_on,notes",
    "nearby.csv": "building_id",
    "safety_zip.csv": "zip,area,overall,violent,property,rate_per_1000,percentile,safest_part,victim_odds_range,source_url,observed_on",
    "raw/concessions.csv": "building_id,free_months_1b,free_months_2b,free_months_3b,free_months_studio,status,lease_months,offer_en,offer_zh,conditions_en,conditions_zh,source_url,observed_on",
}
FOLDERS = ["raw/amenity_text", "raw/links", "raw/cbb", "reviews", "review_summaries", "floorplans", "photos"]


def new_city(root):
    """Write empty tables and config/city.json, keeping files that exist.

    Args:
        root: The repository root.

    Returns:
        The list of paths created.
    """
    created = []
    for folder in FOLDERS:
        os.makedirs(f"{root}/data/{folder}", exist_ok=True)
    for name, header in TABLES.items():
        path = f"{root}/data/{name}"
        if not os.path.exists(path):
            open(path, "w").write(header + "\n")
            created.append(path)
    for name, value in [("contacts.json", {}), ("building_zip.json", {}), ("pois.json", []), ("manual_contacts.json", {})]:
        path = f"{root}/data/{name}"
        if not os.path.exists(path):
            json.dump(value, open(path, "w"))
            created.append(path)
    config = f"{root}/config/city.json"
    if not os.path.exists(config):
        shutil.copy(f"{root}/config/city.example.json", config)
        created.append(config)
    return created


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    if not os.path.isfile(f"{target}/config/city.example.json"):
        sys.exit("usage: python tools/new_city.py [repository root]")
    print(len(new_city(target)), "files created")
