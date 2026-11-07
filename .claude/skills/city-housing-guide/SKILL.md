---
name: city-housing-guide
description: Build a private, bilingual, self-contained apartment guide for someone moving to a city, with a map, sortable list and a page per building. Use when the user is relocating and wants to compare buildings, asks to reproduce this guide for a new city (New York, Chicago, Austin and so on), or asks where to start. Coordinates the other housing skills.
---

# City housing guide

The deliverable is one interactive HTML file that opens with no server, install or key, plus a static PDF for chat apps and phone previews. It shows every building on a map and in a sortable list, and each building has its own page with sourced rents, all-in costs, reviews, amenities, floor plans and tour links.

## Start by asking

Ask only what you cannot find out:

1. Which city, and what is the office or daily destination address?
2. When is the move, and when is the tour trip?
3. Which languages does the page need?
4. Who will see the file, and which app will they open it in? Should an income figure appear in it? It stays out by default.
5. Does the person drive, have pets, or need a shared unit?
6. Which existing notes or reports should be read, and how far should they be trusted?

Treat reports from third parties as leads for building names only, and check every fact against primary sources.

## Steps

Present this plan, record it in the project's `CLAUDE.md`, and wait for the user to name a step.

1. Run `python3 tools/new_city.py .`, then fill in `config/city.json`.
2. Define scope with `housing-universe`.
3. Run three contrasting buildings end to end: a new rental, an owner-leased condo and a large tower. Fix the method before scaling.
4. Collect building facts for every building.
5. Collect rents and all costs with `housing-rents-costs`, reading sites as `housing-platform-access` describes.
6. Collect reviews and ratings with `housing-reviews`.
7. Collect amenities, floor plans, and tour and leasing links.
8. Fetch the basemap and places, then build the page with `housing-page`.
9. Audit with `housing-qa-gaps`, and fix the gaps it finds.
10. Test on real devices, then refresh before the trip.

## Rules that apply everywhere

- Every published number has a source and a date. The page shows both beside each rent.
- Blank means unknown. Never use 0, "N/A" or a silent estimate. Label estimates as estimates.
- `data/` is the source of truth. Never hand-edit generated files.
- Back up before overwriting, and check file times when a session resumes, because a resumed session can start from an older state.
- Keep names of reviewers out of the data. Keep income, employer and other personal details out of the file unless the user asks otherwise.
- Do not host the page at a public URL if it embeds third-party photos or reviews.

## Finished means

Every building opens without errors on Safari and Chrome engines at desktop and phone widths, the coverage table is honest, and the user has opened the file on the device their readers will use.
