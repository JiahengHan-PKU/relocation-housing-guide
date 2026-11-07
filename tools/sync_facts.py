"""Copy merged facts into buildings.csv without touching coordinates."""

import csv

COLUMNS = ["floors", "units", "developer", "facts_source_urls"]


def sync_facts(facts_path, table_path):
    """Fill buildings.csv fact columns from building_facts.csv.

    enrich_buildings.py geocodes every row and shifts coordinates, so use this
    when only facts changed.

    Args:
        facts_path: Path to data/building_facts.csv.
        table_path: Path to data/buildings.csv, rewritten in place.

    Returns:
        The number of cells changed.
    """
    facts = {row["id"]: row for row in csv.DictReader(open(facts_path))}
    with open(table_path, newline="") as handle:
        reader = csv.DictReader(handle)
        columns, rows = reader.fieldnames, list(reader)
    changed = 0
    for row in rows:
        source = facts.get(row["id"], {})
        for column in COLUMNS:
            if source.get(column) and source[column] != row[column]:
                row[column] = source[column]
                changed += 1
    with open(table_path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    return changed


if __name__ == "__main__":
    print(sync_facts("data/building_facts.csv", "data/buildings.csv"))
