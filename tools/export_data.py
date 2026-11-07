"""Collect every table into the single JSON object the page reads."""

import csv
import glob
import json
import os
import statistics

from city_config import load_city
from estimate_all_in import estimate_all_in
from normalize_rules import normalize_rules

UNIT_TYPES = ["studio", "1b", "1b_den", "2b", "3b_plus"]


def read_jsonl(path):
    """Read a JSON-lines file into a dict keyed by `id`, or {} if missing."""
    if not os.path.exists(path):
        return {}
    return {json.loads(line)["id"]: json.loads(line) for line in open(path)}


CITY = load_city()
SOURCE_RANK = CITY.get("source_rank", ["Official site"])


def source_of(row):
    """Return the short source name of a listing row."""
    return row["source_name"].split(" (")[0]


def split_sources(rows):
    """Pick the source with the most rows; break ties by SOURCE_RANK.

    Returns:
        (primary rows, list of rows for each other source).
    """
    groups = {}
    for row in rows:
        groups.setdefault(source_of(row), []).append(row)
    rank = lambda name: SOURCE_RANK.index(name) if name in SOURCE_RANK else len(SOURCE_RANK)
    ordered = sorted(groups, key=lambda name: (-len(groups[name]), rank(name)))
    return groups[ordered[0]], [groups[name] for name in ordered[1:]]


def rent_summary(rows):
    """Return min/median/max, sample size and median size for listing rows."""
    unfurnished = [r for r in rows if r["furnished"] != "true"]
    chosen = unfurnished if len(unfurnished) >= 3 else rows
    rents = sorted(float(r["rent_usd"]) for r in chosen)
    sizes = [float(r["sqft"]) for r in chosen if r["sqft"]]
    return {"min": rents[0], "median": statistics.median(rents), "max": rents[-1],
            "n": len(rents), "sqft": statistics.median(sizes) if sizes else None,
            "basis": sorted({r["price_basis"] for r in chosen}),
            "includes_furnished": chosen is rows and len(unfurnished) < len(rows),
            "sources": sorted({r["source_url"] for r in chosen})[:4],
            "source": source_of(chosen[0]), "observed_on": max(r["observed_on"] for r in chosen)}


def ratings_for(building_id, google, apartments, extra, overall):
    """Merge platform ratings, preferring first-hand reads over relayed ones."""
    out = []
    g = google.get(building_id, {})
    score, count = g.get("r") or g.get("rating"), g.get("c") or g.get("count")
    if score:
        group = "short_stay" if g.get("group") == "short_stay" else "resident"
        out.append({"platform": "Google", "score": float(score),
                    "count": int(str(count or "0").replace(",", "")),
                    "group": group, "via": "direct"})
    if building_id in apartments and apartments[building_id].get("rating"):
        a = apartments[building_id]
        out.append({"platform": "Apartments.com", "score": float(a["rating"]),
                    "count": int(a["count"]), "group": "resident", "via": "direct",
                    "url": a["url"]})
    row = overall.get(building_id)
    if row and row["stars"]:
        out.append({"platform": "Apartments.com overall", "score": float(row["stars"]), "count": 0, "group": "overall",
                    "via": "direct", "url": row["url"], "observed_on": row["observed_on"]})
    seen = {r["platform"] for r in out} | {"Google", "CoStar network"}
    for r in extra.get(building_id, []):
        if r["platform"] not in seen:
            out.append({"platform": r["platform"], "score": float(r["score_5"]),
                        "count": int(r["review_count"] or 0), "group": r["group"],
                        "via": r["retrieved_via"], "url": r["url"], "notes": r["notes"]})
    return out


def gallery_for(path):
    """Return Condo Black Book floor plan rows for one building, smallest first."""
    if not os.path.exists(path):
        return None
    record = json.load(open(path))
    rows = []
    for plan in (record.get("building") or {}).get("floorplans") or []:
        image = ((plan.get("image") or {}).get("data") or {}).get("attributes") or {}
        small = ((image.get("formats") or {}).get("small") or {}).get("url")
        if image.get("url"):
            spans = [f"{f.get('from')}–{f.get('to')}" for f in plan.get("floors") or []]
            rows.append({"model": plan.get("model"), "beds": plan.get("bedBath"), "area": plan.get("area"),
                         "ext": plan.get("exteriorArea"), "floors": ", ".join(spans), "full": image["url"], "thumb": small or image["url"]})
    seen, unique = set(), []
    for row in sorted(rows, key=lambda r: (str(r["beds"]), r["area"] or 0)):
        if row["full"] not in seen:
            seen.add(row["full"])
            unique.append(row)
    return {"url": record["url"], "plans": unique} if unique else None


def concession_for(row, rents):
    """Return a current offer and the net rent per unit type if it still applies.

    Offers stay out of base rent and all-in totals, because most are limited to
    select homes and may end before the move-in date.
    """
    if not row:
        return None
    columns = {"1b": "free_months_1b", "1b_den": "free_months_1b", "2b": "free_months_2b",
               "3b_plus": "free_months_3b", "studio": "free_months_studio"}
    net = {}
    for unit, rent in rents.items():
        free = row[columns[unit]]
        if free and row["lease_months"]:
            lease = float(row["lease_months"])
            net[unit] = {"free_months": float(free), "net": rent["median"] * (lease - float(free)) / lease}
    return {**{k: row[k] for k in ("status", "offer_en", "offer_zh", "conditions_en", "conditions_zh",
                                   "source_url", "observed_on")}, "net": net}


def export_data(data_dir, out_path):
    """Write web/data.json with buildings, reviews and shared assumptions.

    Args:
        data_dir: The project's data folder.
        out_path: Destination JSON file.
    """
    buildings = [r for r in csv.DictReader(open(f"{data_dir}/buildings.csv")) if r["status"] == "include"]
    listings = list(csv.DictReader(open(f"{data_dir}/listings.csv")))
    costs = list(csv.DictReader(open(f"{data_dir}/costs.csv")))
    nearby = {r["building_id"]: r for r in csv.DictReader(open(f"{data_dir}/nearby.csv"))}
    assumptions = {r["item"]: float(r["value"]) for r in csv.DictReader(open(f"{data_dir}/cost_assumptions.csv"))}
    google = read_jsonl(f"{data_dir}/raw/google_maps.jsonl")
    for key, meta in read_jsonl(f"{data_dir}/raw/google_review_meta.jsonl").items():
        google[key] = {**google.get(key, {}), **meta}
    apartments = read_jsonl(f"{data_dir}/raw/apartments_com.jsonl")
    offers = {r["building_id"]: r for r in csv.DictReader(open(f"{data_dir}/raw/concessions.csv"))}
    amenities = {}
    if os.path.exists(f"{data_dir}/amenities.csv"):
        for r in csv.DictReader(open(f"{data_dir}/amenities.csv")):
            amenities.setdefault(r["building_id"], []).append(
                {"key": r["amenity"], "evidence": r["evidence"], "url": r["source_url"]})
    contacts = json.load(open(f"{data_dir}/contacts.json"))
    overall = {}
    if os.path.exists(f"{data_dir}/raw/apartments_overall.csv"):
        overall = {r["building_id"]: r for r in csv.DictReader(open(f"{data_dir}/raw/apartments_overall.csv"))}
    extra = {}
    for r in csv.DictReader(open(f"{data_dir}/ratings.csv")):
        extra.setdefault(r["building_id"], []).append(r)
    summaries = {}
    for path in glob.glob(f"{data_dir}/review_summaries/*.json"):
        s = json.load(open(path))
        summaries[s["building_id"]] = {k: ";".join(v) if isinstance(v, list) else v for k, v in s.items()}
    raws = {os.path.basename(p)[:-5]: json.load(open(p)) for p in glob.glob(f"{data_dir}/raw/*.json")}
    zips = json.load(open(f"{data_dir}/building_zip.json"))
    safety = {r["zip"]: r for r in csv.DictReader(open(f"{data_dir}/safety_zip.csv"))}
    out, reviews = [], {}
    for b in buildings:
        raw = raws.get(b["id"], {})
        own = [r for r in listings if r["building_id"] == b["id"]]
        own_costs = [c for c in costs if c["building_id"] == b["id"]]
        rents, all_in = {}, {}
        for unit in UNIT_TYPES:
            rows = [r for r in own if r["unit_type"] == unit]
            if rows:
                rows, others = split_sources(rows)
                rents[unit] = rent_summary(rows)
                rents[unit]["cross_check"] = [rent_summary(group) for group in others]
                parts = estimate_all_in([float(r["rent_usd"]) for r in rows],
                                        [float(r["sqft"]) for r in rows if r["sqft"]] or [750],
                                        own_costs, assumptions)
                all_in[unit] = {k: {"value": round(v, 2), "basis": basis} for k, (v, basis) in parts.items()}
        review_path = f"{data_dir}/reviews/{b['id']}.jsonl"
        if os.path.exists(review_path):
            rows = [json.loads(line) for line in open(review_path)]
            reviews[b["id"]] = sorted(rows, key=lambda r: -(r.get("likes") or 0))
        summary = summaries.get(b["id"], {})
        out.append({
            **{k: b[k] for k in ["id", "name", "aliases", "address", "neighborhood", "official_url",
                                 "developer", "architect", "manager", "building_type",
                                 "channel_primary", "channels_all", "summary_en", "summary_zh",
                                 "photo_file", "photo_source_url", "facts_source_urls", "as_of"]},
            **{k: (float(b[k]) if b[k] else None) for k in ["lat", "lon", "walk_m", "walk_min", "year_built", "floors", "units"]},
            "rules": normalize_rules(raw.get("rules")),
            "conflicts": (raw.get("facts") or {}).get("conflicts"),
            "notes": raw.get("notes"),
            "rents": rents, "all_in": all_in,
            "costs": [{k: c[k] for k in ["item", "amount_usd", "frequency", "counted", "basis", "source_url", "notes"]} for c in own_costs],
            "ratings": ratings_for(b["id"], google, apartments, extra, overall),
            "concession": concession_for(offers.get(b["id"]), rents),
            "amenities": amenities.get(b["id"], []),
            "contacts": contacts.get(b["id"]),
            "apartments_status": overall.get(b["id"], {}).get("status"),
            "gallery": gallery_for(f"{data_dir}/raw/cbb/{b['id']}.json"),
            "nearby": nearby.get(b["id"], {}),
            "zip": zips.get(b["id"]),
            "safety": safety.get(zips.get(b["id"])),
            "review_summary": {k: summary.get(k) for k in ["summary_en", "summary_zh", "tags_en", "tags_zh",
                                                           "pros_en", "pros_zh", "cons_en", "cons_zh", "reviews_used"]} if summary else None,
        })
    json.dump({"generated_on": CITY["as_of"], "office": CITY["office"], "city": {**CITY.get("page", {}), "nearby": CITY.get("nearby", {})}, "assumptions": assumptions,
               "buildings": out, "reviews": reviews,
               "floorplans": {os.path.basename(p)[:-5]: json.load(open(p)) for p in glob.glob(f"{data_dir}/floorplans/*.json")}},
              open(out_path, "w"), ensure_ascii=False, separators=(",", ":"))
    return len(out), sum(len(v) for v in reviews.values())


if __name__ == "__main__":
    print(export_data("data", "web/data.json"))
