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
    PYTHONPATH=tools python3 tools/fetch_walk_network.py
    PYTHONPATH=tools python3 tools/route_pois.py

`fetch_walk_network.py` downloads every walkable way (streets, sidewalks, footpaths, steps, crossings) inside `pois_bbox` with one Overpass request. `route_pois.py` then routes from each building to the places within 2 km (bus stops within 400 m) on that network locally, in seconds, with no routing service to rate-limit you. Rerun both after `fetch_pois.py` or after moving a building, because the page and `build_nearby.py` match places by their index in `data/pois.json`. Without them, walking times fall back to straight-line distance × 1.25 and show as ≈.

The walk to the office can come from Google Maps instead of OSRM: put `data/google_walk.csv` (building_id, walk_min, walk_mi, source_url, as_of, note) next to the other tables and `export_data.py` uses it, linking each value to its Google Maps route. Look these up by hand or in your own browser. Do not scrape Google Maps.

Collectors skip buildings already saved, so delete a building's file to read it again.
