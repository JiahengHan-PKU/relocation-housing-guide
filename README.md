# Relocation Housing Guide

Build a private apartment guide for a move to any city: every building on a map and in a sortable list, with sourced rents, all-in monthly costs, reviews, amenities, floor plans and tour links. The result is one interactive HTML file in English and Chinese that opens with no server, install or key, plus a phone-sized PDF for WeChat and other apps that block scripts.

The first guide covered 82 buildings in Miami. Its code, process and lessons are here, so the next city takes far less work. Its reviews, photos and raw platform records are not.

## What it builds

- **Map:** marker color shows rent and marker shape shows how you lease, on an embedded OpenStreetMap basemap.
- **List:** sort and filter by rent, all-in cost, walking time, age, ratings, safety, amenities and an adjustable score.
- **Neighborhood explorer:** on each building page, a linked map and list of groceries, pharmacies, transit, food, parks and gyms, with walking rings, category toggles and safety grades.
- **Building pages:** rent by unit type with source and date, a worked all-in cost, concessions, rules, an AI review summary with pros and cons, floor plans, and links for 3D tours, in-person tours and leasing.

## Use it with Claude Code

    git clone https://github.com/JiahengHan-PKU/relocation-housing-guide.git
    cd relocation-housing-guide
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    python tests/smoke_test.py

Then open Claude Code here and say:

> I'm moving to Chicago. Use the city-housing-guide skill to build my guide.

| Skill | Purpose |
|---|---|
| `city-housing-guide` | Intake, the 10-step plan and shared rules |
| `housing-universe` | Scope, building identity and facts |
| `housing-rents-costs` | Rents, all-in costs and concessions |
| `housing-platform-access` | Reading sites politely, and what to do when blocked |
| `housing-reviews` | Reviews, ratings and summaries |
| `housing-page` | Building and testing the page |
| `housing-qa-gaps` | Finding out why data is missing |

## Use it by hand

    python tools/new_city.py .        # Creates data/ and config/city.json
    # Edit config/city.json and data/building_seed.csv, then collect data
    python tools/fetch_basemap.py
    python tools/build_basemap.py
    python tools/fetch_pois.py
    PYTHONPATH=tools python tools/enrich_buildings.py
    tools/build_all.sh                # Writes the page to dist/

## How it works

    data/raw/*  ->  merge_raw  ->  CSV tables  ->  export_data  ->  web/data.json  ->  build_page  ->  dist/*.html

`config/city.json` holds everything specific to a city, including office, map bounds, source order, local brands and transit, and page text. Set `page.annual_base` to show an affordability module, or leave it null to hide it. Keep it null if the page will be shared.

## What a new city needs

The page, data model, cost model and process carry over. Each city needs new work on its listing sources, because they differ by market. `tools/sources/miami/` shows the pattern, `docs/CITY_NOTES.md` has starting notes for New York, Chicago and Austin, and `examples/miami/` shows a finished config and coverage table.

## Verified

- Run through the template, the Miami dataset reproduced the original project's building, review, floor plan and assumption data exactly.
- `tests/smoke_test.py` builds a page for a fictional city from an empty folder and opens it in Chrome.

Not yet tried: a real second city. Expect to adjust the listing collectors and some local rules.

## Data and respect for sources

Collect at a low rate. Do not bypass bot checks or use stealth tooling. Check each site's terms before publishing anything derived from it. `data/` and `dist/` are ignored by git, because they hold third-party reviews, photos and listing data. Do not host a generated page at a public URL if it contains them.

The guide is for personal research and is not financial, legal or housing advice. Confirm prices, fees and rules with the building.

## License

The code and skills are under the [MIT License](LICENSE). Third-party components keep their own licenses; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). The license does not cover data you collect from other sites.
