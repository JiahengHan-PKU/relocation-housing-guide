---
name: housing-universe
description: Decide which buildings belong in a housing guide and establish their identity, address, aliases, facts and rental channel. Use when starting a city, adding buildings, or when records from different sources may refer to the same or different buildings.
---

# Building universe

Scope is the union of every building named in the user's materials and found online or in OpenStreetMap. Keep excluded buildings in `data/building_seed.csv` with `status` and a reason, so they are not rediscovered.

## Identity comes first

Most later failures here were identity failures, and they looked like missing data.

- Use one stable slug per building.
- Check the street address against at least two sources before scaling. One wrong street number blocked a building's plans, amenities and rents, because address checks then rejected every correct page.
- Record conflicts when you find them, and fix them at once. A conflict noted but left unfixed caused that failure.
- Record aliases. Platforms use old names, tower names and marketing names, for example a hotel brand that changed, or `Met1` for `Met 1`.
- Corner buildings can have two valid addresses. Allow a named exception, and write down why.
- Match on number and street together. Two different buildings can share a number on different streets, and two can share a name in different neighborhoods.
- When an address disagrees but name, year and height all match, accept the page and record the exception.

## Facts

Source order: county records, official site, developer or architect, then listing sites. Keep the conflict when sources disagree. Listing databases contain errors, such as 14 floors for a 44-story tower, so sanity-check floors and units.

Do not accept a claim that appears only on low-quality sites, even when several repeat it. Copied pages count as one source.

## Rental channel

Apply in order and stop at the first match:

- `A`: the building or manager has a site with live plans or an online application.
- `B`: no such site, but one leasing office lists and signs.
- `C`: individual owners lease, usually through an agent.

Channel drives the rent source, the tour module and the income rules, so settle it early.

## Coordinates and walking time

`tools/enrich_buildings.py` geocodes the seed and routes on the street network. Run it once. It shifts coordinates, so use `tools/sync_facts.py` when only facts change.
