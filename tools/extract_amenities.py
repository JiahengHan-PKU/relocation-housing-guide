"""Map collected amenity text onto one shared amenity list."""

import csv
import glob
import json
import os
import re

from city_config import load_city

RULES = {
    "pool": r"\b(swimming|lap|heated|resort|rooftop|infinity|plunge|social|outdoor|indoor) pools?\b|\bpools?\b(?! (table|deck|side|bar))",
    "rooftop": r"roof ?top|roof terrace|sky ?deck|sky ?lounge|sky terrace",
    "gym": r"fitness|\bgym\b|gymnasium|work ?out",
    "spa": r"\bspa\b|sauna|steam room|hammam|massage|treatment room",
    "concierge": r"concierge|door ?man|front desk|lobby attendant",
    "security": r"24.{0,8}(hour|hr).{0,20}security|security.{0,20}24|on.?site security|security (guard|staff|desk)",
    "valet": r"\bvalet\b(?! trash)",
    "garage": r"garage|covered parking|assigned parking|parking (space|structure|deck)",
    "ev": r"\bev\b.{0,12}charg|electric (car|vehicle).{0,20}charg|charging station|car charg",
    "laundry": r"(in.?unit|in.?residence|in.?home|each).{0,24}(washer|laundry)|washer.{0,6}(and|&|/).{0,6}dryer",
    "pets": r"pet.?friendly|pets? (are )?(welcome|allowed)|pet spa|pet wash|dog (park|run|wash)|bark park",
    "dog": r"dog (park|run|wash|walk)|pet (park|spa|wash)|bark park",
    "work": r"co.?working|business (cent|lounge)|conference room|meeting room|work ?space|work.?from.?home",
    "theater": r"theat(er|re)|cinema|screening room|media room|movie",
    "lounge": r"club ?room|club ?house|resident(s)? lounge|social room|sky lounge|party room|owners.? lounge",
    "games": r"game room|billiard|bowling|arcade|ping.?pong|simulator|poker|foosball",
    "sports": r"tennis|basketball|racquet ?ball|squash|pickle ?ball|volleyball",
    "bbq": r"\bbbq\b|barbe?cue|\bgrills?\b|grilling|summer kitchen|outdoor kitchen",
    "kids": r"kids?\b|children|playground|play ?room|teen",
    "marina": r"marina|boat slip|boat dock|private dock",
    "waterfront": r"water ?front|bay ?front|river ?front|river ?walk|baywalk",
    "retail": r"on.?site (restaurant|retail|cafe|market)|ground.?floor (retail|restaurant)|poolside (cafe|bar)|\bcaf[eé]\b",
    "bike": r"bike (storage|room|rack|share)|bicycle",
    "package": r"package (locker|room|concierge|service)|parcel|luxer",
    "storage": r"storage (unit|room|locker|space)s?|private storage",
}
SKIP = re.compile(r"steps (from|to|away)|minutes? (from|to|away)|\bnear(by)?\b|close to|walking distance|"
                  r"blocks? (from|away)|short (walk|drive)|surrounded by|\bno (pool|pets?|valet|gym)\b|not (allowed|available|permitted)|"
                  r"pool table|cookie|privacy|\bmap\b|copyright|schedule a tour|gallery|should be confirmed|pet playground|"
                  r"Residences .*Residences", re.I)


def relevant_lines(page):
    """Return the lines of a page that describe the building itself."""
    lines = [line.strip() for line in page["text"].splitlines() if line.strip()]
    if "miamicondosolution" in page["url"]:
        end = next((i for i, line in enumerate(lines) if line == "FOR SALE"), len(lines))
        start = next((i for i, line in enumerate(lines) if line.startswith("Price range")), 0)
        lines = lines[start:end]
    parts = [part.strip() for line in lines for part in re.split(r"(?<=[.;•])\s+|\s+[•·|]\s+", line)]
    return [part for part in parts if 14 <= len(part) <= 260 and not SKIP.search(part)]


CBB_FIELDS = {
    "pool": ["sport.pool", "general.heatedPool", "general.privatePool"], "gym": ["sport.exerciseRoom"],
    "spa": ["general.spaHotTub", "general.sauna"], "sports": ["sport.tennis", "sport.basketball", "sport.pickleball"],
    "games": ["sport.billiard"], "lounge": ["general.communityRoom", "general.club"], "work": ["general.businessCenter"],
    "bbq": ["general.bbqPicnicArea"], "kids": ["general.childPlayArea"], "marina": ["general.marina", "general.boatDock"],
    "storage": ["general.extraStorage"], "bike": ["sport.bikeStorage"], "valet": ["parking.valet"],
    "garage": ["parking.garage", "parking.covered"], "laundry": ["convenience.washerDryer"], "pets": ["pets.allowedForRent"],
    "waterfront": ["waterfront.bay", "waterfront.river", "waterfront.ocean", "waterfront.intracoastal"],
}


APARTMENTS_ITEMS = {
    "Pool": ["pool"], "Roof Terrace": ["rooftop"], "Fitness Center": ["gym"], "Spa": ["spa"], "Sauna": ["spa"],
    "Concierge": ["concierge"], "Doorman": ["concierge"], "EV Charging": ["ev"], "Washer/Dryer": ["laundry"],
    "Dog Park": ["dog", "pets"], "Pet Play Area": ["pets"], "Business Center": ["work"], "Conference Rooms": ["work"],
    "Media Center/Movie Theatre": ["theater"], "Clubhouse": ["lounge"], "Lounge": ["lounge"], "Study Lounge": ["lounge"],
    "Gameroom": ["games"], "Basketball Court": ["sports"], "Tennis Court": ["sports"], "Grill": ["bbq"],
    "Playground": ["kids"], "Waterfront": ["waterfront"], "On-Site Retail": ["retail"], "Bicycle Storage": ["bike"],
    "Package Service": ["package"], "Storage Space": ["storage"],
}


def apartments_amenities(path):
    """Return {building_id: {amenity: (evidence, url, date)}} from Apartments.com item lists."""
    found = {}
    if not os.path.exists(path):
        return found
    for row in csv.DictReader(open(path)):
        for key in APARTMENTS_ITEMS.get(row["item"], []):
            found.setdefault(row["building_id"], {}).setdefault(
                key, (f"Apartments.com amenity list: {row['item']}", row["source_url"], row["observed_on"]))
    return found


def cbb_amenities(path):
    """Return {amenity: (evidence, url)} from one Condo Black Book record."""
    if not os.path.exists(path):
        return {}
    record = json.load(open(path))
    fields = (record.get("building") or {}).get("amenity") or {}
    found = {}
    for key, names in CBB_FIELDS.items():
        for name in names:
            group, field = name.split(".")
            if (fields.get(group) or {}).get(field) is True:
                found[key] = (f"Condo Black Book field: {field}", record["url"])
                break
    return found


def extract_amenities(text_dir, out_path, observed_on, cbb_dir="data/raw/cbb",
                      apartments_path="data/raw/apartments_amenities.csv"):
    """Write amenities.csv with one evidence line per building and amenity.

    Args:
        text_dir: Folder from collect_amenity_text.py.
        out_path: Destination CSV.
        observed_on: Date the pages were read, YYYY-MM-DD.

    Returns:
        The number of rows written.
    """
    rows = []
    apartments = apartments_amenities(apartments_path)
    for path in sorted(glob.glob(f"{text_dir}/*.json")):
        record = json.load(open(path))
        found = {}
        for page in record["pages"]:
            for line in relevant_lines(page):
                for key, rule in RULES.items():
                    if key not in found and re.search(rule, line, re.I):
                        found[key] = (line[:150], page["url"])
        for key, value in cbb_amenities(f"{cbb_dir}/{record['id']}.json").items():
            found.setdefault(key, value)
        for key, value in apartments.get(record["id"], {}).items():
            found.setdefault(key, value)
        rows += [{"building_id": record["id"], "amenity": key, "evidence": text, "source_url": url,
                  "observed_on": (date or [observed_on])[0]} for key, (text, url, *date) in found.items()]
    with open(out_path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["building_id", "amenity", "evidence", "source_url", "observed_on"])
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    print(extract_amenities("data/raw/amenity_text", "data/amenities.csv", load_city()["as_of"]))
