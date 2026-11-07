---
name: housing-qa-gaps
description: Audit coverage in a housing guide and find out why data is missing before accepting a gap. Use before sharing a guide, when a building has blank fields, when a rent looks wrong, or when preparing a refresh before a trip.
---

# QA and gaps

## Treat a gap as a question

A blank is often a matching failure. For each gap, find the reason and record it:

| Reason | Action |
|---|---|
| Wrong address or name | Fix identity, then collect again |
| Page exists under another name | Search that domain, add an override |
| Rate limited or parser failed | Retry slowly, and fix the collector |
| Empty record blocks a rerun | Delete it, then rerun |
| The data does not exist today | Record that, and leave it blank |

Only the last row is a real gap. In the first guide, searching by domain and fixing one address added 6 buildings' floor plans and several rents after they had been reported as missing.

## Report

Write `data/QA_REPORT.md` with a coverage table, listings removed and why, outliers kept on purpose, judgment calls and possible scams. Count coverage from the built `web/data.json`, not from memory. State a rule for each exclusion.

Report results exactly. If a statement you made earlier was wrong, say so and correct it, including what you told the user before.

## Checks

- Rent per square foot within a plausible range for the city, and studios not larger than one-bedrooms.
- Primary and cross-check sources roughly agree.
- Prices match a spot check against a live page, especially for the buildings the user knows.
- Amenity evidence lines describe the building, not its neighborhood. "Steps from the marina" is not a marina. Sample them by hand.
- In-unit laundry excludes hookups and shared laundry rooms.
- After a shared tool changes, diff the tables against a backup. Removed rows need an explanation.

## Scams

Flag sites that take applications for a building but are not tied to it. Tell the user not to pay through them.

## Refresh

Rents and offers go stale in weeks. Refresh within about two weeks of a trip, re-read concessions, and update the as-of date in `config/city.json`.
