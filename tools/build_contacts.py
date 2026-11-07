"""Sort official links into virtual tour, in-person tour and leasing lists."""

import csv
import glob
import json
import os
import re
import urllib.parse

from city_config import load_city

VIRTUAL = re.compile(r"virtual|360|3d.?tour|matterport|realync|video.?tour", re.I)
TOUR = re.compile(r"schedule|book.?a.?tour|plan.?visit|appointment|\btour\b", re.I)
APPLY = re.compile(r"apply|onlineleasing|securecafe|lease.?now|availab", re.I)
JUNK = re.compile(r"\.(jpe?g|png|webp|gif|pdf)($|\?)|career|position|resident|portal|activebuilding|maps|facebook|instagram|youtube\.com/@|#gomenu|elementor-action", re.I)


def pick(links, pattern, limit=2):
    """Return up to `limit` distinct links matching a pattern."""
    seen, out = set(), []
    for url, text in links:
        clean = url.split("#")[0].rstrip("/")
        if clean in seen or JUNK.search(url) or not url.startswith("http"):
            continue
        if pattern.search(url + " " + text):
            seen.add(clean)
            out.append({"url": url.rstrip("#"), "text": text})
    return out[:limit]


def build_contacts(data_dir):
    """Write data/contacts.json from the collected links and listing pages.

    Args:
        data_dir: The project's data folder.
    """
    buildings = [r for r in csv.DictReader(open(f"{data_dir}/buildings.csv")) if r["status"] == "include"]
    city = load_city()
    manual_path = f"{data_dir}/manual_contacts.json"
    manual = json.load(open(manual_path)) if os.path.exists(manual_path) else {}
    PHONES, APARTMENT_TOURS = manual.get("phones", {}), manual.get("apartment_tours", {})
    apartments = {}
    if os.path.exists(f"{data_dir}/raw/apartments_plans.csv"):
        for row in csv.DictReader(open(f"{data_dir}/raw/apartments_plans.csv")):
            apartments[row["building_id"]] = row["source_url"]
    if os.path.exists(f"{data_dir}/raw/apartments_com.jsonl"):
        for line in open(f"{data_dir}/raw/apartments_com.jsonl"):
            row = json.loads(line)
            apartments.setdefault(row["id"], row.get("url"))
    if os.path.exists(f"{data_dir}/raw/apartments_overall.csv"):
        for row in csv.DictReader(open(f"{data_dir}/raw/apartments_overall.csv")):
            if row["url"]:
                apartments.setdefault(row["building_id"], row["url"])
    condo = {}
    for row in csv.DictReader(open(f"{data_dir}/listings.csv")):
        if row["source_name"] == city.get("owner_listing_source"):
            condo.setdefault(row["building_id"], row["source_url"])
    result = {}
    for b in buildings:
        id_ = b["id"]
        path = f"{data_dir}/raw/links/{id_}.json"
        record = json.load(open(path)) if os.path.exists(path) else {"links": [], "frames": []}
        links = [tuple(x) for x in record["links"]]
        cbb_path = f"{data_dir}/raw/cbb/{id_}.json"
        cbb = json.load(open(cbb_path)).get("url") if os.path.exists(cbb_path) else None
        phone = PHONES.get(id_) or next((urllib.parse.unquote(u[4:]).strip() for u, _ in links if u.startswith("tel:")), None)
        direct = b["channel_primary"] in ("A", "B")
        virtual = [{"kind": "official", **x} for x in pick(links, VIRTUAL)]
        virtual += [{"kind": "frame", "url": f, "text": ""} for f in record["frames"] if re.search("matterport|realync", f)][:1]
        if APARTMENT_TOURS.get(id_):
            virtual.append({"kind": "apartments3d", "url": apartments[id_] + "#matterport3dSection", "text": "", "count": APARTMENT_TOURS[id_]})
        tour = [{"kind": "official", **x} for x in pick(links, TOUR) if not VIRTUAL.search(x["url"] + " " + x["text"]) or re.search("schedule", x["text"], re.I)]
        if direct and not tour and b["official_url"]:
            tour.append({"kind": "official", "url": b["official_url"], "text": ""})
        if apartments.get(id_):
            tour.append({"kind": "apartments", "url": apartments[id_], "text": ""})
        if condo.get(id_):
            tour.append({"kind": "condo", "url": condo[id_], "text": ""})
        if cbb:
            tour.append({"kind": "cbb", "url": cbb, "text": ""})
        rent = [{"kind": "official", **x} for x in pick(links, APPLY)] if direct else []
        if apartments.get(id_):
            rent.append({"kind": "apartments", "url": apartments[id_], "text": ""})
        if condo.get(id_):
            rent.append({"kind": "condo", "url": condo[id_], "text": ""})
        if cbb:
            rent.append({"kind": "cbb", "url": cbb, "text": ""})
        query = urllib.parse.quote(f"{b['address']} {city['listing_search_suffix']}".replace(" ", "-"))
        rent.append({"kind": "zillow", "url": f"https://www.zillow.com/homes/{query}_rb/", "text": ""})
        result[id_] = {"virtual": virtual, "tour": tour, "rent": rent, "phone": phone}
    json.dump(result, open(f"{data_dir}/contacts.json", "w"), ensure_ascii=False, indent=0)
    return result


if __name__ == "__main__":
    data = build_contacts("data")
    print(len(data), "virtual", sum(bool(v["virtual"]) for v in data.values()), "phone", sum(bool(v["phone"]) for v in data.values()))
