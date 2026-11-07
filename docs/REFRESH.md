# Refreshing a guide

Run these from the repository root. Files in `dist/` are generated.

## Rebuild after any change

    tools/build_all.sh

## Update rents and facts

1. Edit `data/raw/<id>.json`, or the hand-read tables in `data/raw/` (`apartments_plans.csv`, `apartments_units.csv`, `broker_units.csv`, `apartments_fees.csv`, `apartments_amenities.csv`, `apartments_overall.csv`).
2. Set `as_of` in `config/city.json`.
3. Rebuild.

`merge_raw` regenerates `building_facts.csv`, `listings.csv`, `costs.csv` and `qa_excluded_listings.csv`, so edit their inputs instead. `sync_facts.py` copies facts into `buildings.csv` without moving coordinates. Run `enrich_buildings.py` only when the seed changes, because it geocodes every building again and shifts coordinates.

## Offers

Offers change often. Re-read them before a trip, and update `data/raw/concessions.csv`.

## Places and basemap

    python3 tools/fetch_basemap.py
    python3 tools/build_basemap.py
    python3 tools/fetch_pois.py

Collectors skip buildings already saved, so delete a building's file to read it again.
