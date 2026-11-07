---
name: housing-rents-costs
description: Collect apartment rents and estimate the true monthly cost, including fees, utilities, concessions and move-in charges. Use when gathering prices, checking whether a rent looks wrong, adding a platform, or computing all-in cost or net effective rent.
---

# Rents and costs

## Choose sources per city

Before collecting, find out how this city's rentals work: who lists condos, whether an MLS mirror is public, and what fees are customary. Start from `docs/CITY_NOTES.md`, then verify. Set `source_rank` in `config/city.json`.

Useful source types, in order: the official leasing site, a platform's page for that property, a manager's listing, a local site showing owner listings, a broker site that mirrors the MLS with list dates. Building pages on broker sites can be the best source for owner-leased condos, because they show unit, price, size and list date in one table.

## One primary source per unit type

Do not mix sources into one median. For each unit type use the source with the most rows, break ties by `source_rank`, and show the others as a cross-check. A guide once showed $3,300 for a tower whose real rents were near $4,700, because one owner listing filled a gap. A user caught it.

## Rules

- Count asking rents for leases of 12 months or longer, seen within 60 days.
- Drop sublets, short stays, duplicates and deposits scraped as rents. Values under about $1,000 in an expensive market are usually deposits.
- Separate "from" prices (`floorplan_from`) from real units (`unit`). The page labels them differently.
- Drop listings that contradict building facts, such as a 36th-floor unit in a 14-story building.
- Reject stale listings instead of using them to fill a gap. Check that the page is still live.
- Exclude furnished units from headline figures unless fewer than three others remain, then say so.
- Show a low-sample label when n is below 3.

## All-in cost

Include required fees, amenity fee, trash, pest, water and sewer, electricity, internet, renters insurance, tax and one-time charges. Use actual values when published, and sourced estimates otherwise, labeled as estimates. Show parking, and keep it out of totals unless the person drives. Check whether residential rent is taxed locally, because this changes by state and lease length.

Sourced inputs live in `data/cost_assumptions.csv`. `tools/estimate_all_in.py` does the calculation.

## Concessions

Store offers in `data/raw/concessions.csv` with a status: `stated`, `select`, `conflict` or `expired`. Net rent = median × (lease − months free) / lease. Keep offers out of base rent and all-in totals, because they often cover select homes and may end before the move-in date. In concession-heavy markets, show both figures side by side.

## Income rules

Compare against the building's stated minimum where one exists. Otherwise show a common multiple, labeled as a rule of thumb.
