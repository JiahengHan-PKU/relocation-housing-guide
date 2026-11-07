"""Merge per-building research files into the shared tables."""

import csv
import glob
import json
import os

from city_config import load_city

FACT_KEYS = ["official_url", "year_built", "floors", "units", "developer",
             "architect", "manager", "building_type", "channel_primary",
             "channels_all", "summary_en", "summary_zh"]
LISTING_TABLES = [("apartments_plans.csv", "Apartments.com", "floorplan_from", "apt"),
                  ("apartments_units.csv", "Apartments.com", "unit", "unit"),
                  ("broker_units.csv", load_city().get("broker_source", "Broker (MLS)"), "unit", "mls")]
COST_COLUMNS = ["building_id", "item", "amount_usd", "frequency", "counted",
                "basis", "source_url", "notes"]


def suspicious(row):
    """Return a reason when a listing's size contradicts its unit type, else ''."""
    sqft = float(row["sqft"]) if row.get("sqft") else None
    rent = float(row["rent_usd"])
    if sqft and row["unit_type"] == "studio" and sqft > 1000:
        return "studio larger than 1,000 sq ft; unit type likely mislabeled"
    if sqft and row["unit_type"] == "studio" and rent / sqft > 10:
        return "studio above $10 per sq ft; likely short-term or furnished"
    if sqft and rent / sqft < 1.8:
        return "below $1.80 per sq ft; size or type likely wrong"
    return ""


def merge_raw(raw_dir, data_dir, condo_path):
    """Write building_facts.csv, listings.csv and costs.csv from raw JSON.

    Args:
        raw_dir: Folder holding one <id>.json per building.
        data_dir: Folder holding the shared CSV tables.
        condo_path: JSON of condo listing rows by building id. They are used
            for every building whose raw file has no official prices.
    """
    condo = json.load(open(condo_path)) if os.path.exists(condo_path) else {}
    raws = [json.load(open(p)) for p in sorted(glob.glob(f"{raw_dir}/*.json"))]
    raws = [raw for raw in raws if isinstance(raw, dict) and "facts" in raw]
    with open(f"{data_dir}/building_facts.csv", newline="") as handle:
        fact_columns = next(csv.reader(handle))
    with open(f"{data_dir}/listings.csv", newline="") as handle:
        listing_columns = next(csv.reader(handle))
    facts, listings, costs = [], [], []
    for raw in raws:
        info, photo = raw["facts"], raw.get("photo") or {}
        row = {key: info.get(key) for key in FACT_KEYS}
        row.update(id=raw["id"], photo_file=photo.get("file"),
                   photo_source_url=photo.get("source_url"),
                   facts_source_urls=";".join(info.get("sources") or []),
                   as_of=load_city()["as_of"])
        facts.append(row)
        for n, item in enumerate(raw.get("listings") or [], 1):
            listings.append({**item, "listing_id": f"{raw['id']}-{n}",
                             "building_id": raw["id"]})
        if not raw.get("listings"):
            listings += condo.pop(raw["id"], [])
        else:
            condo.pop(raw["id"], None)
        costs += [{**item, "building_id": raw["id"]} for item in raw.get("costs") or []]
    for rows in condo.values():
        listings += rows
    for name, source, basis, tag in LISTING_TABLES:
        if os.path.exists(f"{raw_dir}/{name}"):
            for n, row in enumerate(csv.DictReader(open(f"{raw_dir}/{name}")), 1):
                listings.append({**row, "listing_id": f"{row['building_id']}-{tag}{n}",
                                 "price_basis": basis, "source_name": source})
    if os.path.exists(f"{raw_dir}/apartments_fees.csv"):
        costs += list(csv.DictReader(open(f"{raw_dir}/apartments_fees.csv")))
    excluded = [r for r in listings if suspicious(r)]
    listings = [r for r in listings if not suspicious(r)]
    with open(f"{data_dir}/qa_excluded_listings.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=listing_columns + ["reason"], extrasaction="ignore")
        writer.writeheader()
        writer.writerows({**r, "reason": suspicious(r)} for r in excluded)
    for name, columns, rows in [("building_facts", fact_columns, facts),
                                ("listings", listing_columns, listings),
                                ("costs", COST_COLUMNS, costs)]:
        with open(f"{data_dir}/{name}.csv", "w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
