# Data Dictionary

`building_seed.csv` is the hand-checked input: identity, address, `found_in`, status and any coordinate override. `tools/enrich_buildings.py` generates `buildings.csv` from it, so correct addresses in the seed.

Three tables feed the page: `buildings.csv` (one row per building), `listings.csv` (one row per price observation) and `ratings.csv` (one row per building and platform). Summary rents and scores are computed by the build, never typed in.

Blank means unknown. Never use 0, "N/A" or an estimate for missing values.

## buildings.csv

| Column | Meaning |
|---|---|
| `id` | Stable lowercase slug, used in `#b-<id>` |
| `name` | Building name in English; the page does not translate names |
| `aliases` | Other names, separated by `;` |
| `address`, `zip` | Street address used for geocoding and display |
| `lat`, `lon` | Building coordinates |
| `neighborhood` | Brickell, Downtown, Edgewater and so on |
| `official_url` | The building's or manager's own site; blank if none |
| `year_built` | Year of first occupancy |
| `floors` | Number of stories, from the best source in the source order below |
| `units` | Residential unit count |
| `developer`, `architect`, `manager` | Blank if not found |
| `building_type` | `rental`, `condo`, `hotel_condo` or `mixed` |
| `channel_primary` | `A`, `B` or `C`, see Rental channel |
| `channels_all` | Every available channel, separated by `;` |
| `walk_m`, `walk_min` | Street-network distance to the office; minutes at 80 m/min |
| `walk_method` | Routing engine or manual method |
| `walk_verified` | `true` only after a Google Maps or on-site check |
| `summary_en`, `summary_zh` | One or two factual sentences |
| `photo_file` | Local image name |
| `photo_source_url` | Page the photo came from; required whenever `photo_file` is set. All photos come from official sites: the building's, its manager's or its developer's own site. Never use listing sites. If no official photo exists, leave the photo blank and report the building |
| `photo_credit`, `photo_license` | Fill in when stated by the source |
| `found_in` | Where the building came from: `materials`, `online`, `osm`, separated by `;` |
| `status` | `include` or `exclude` |
| `exclude_reason` | Required when excluded |
| `facts_source_urls` | Sources for the facts, separated by `;` |
| `as_of` | Date the facts were last checked, YYYY-MM-DD |

Source order for building facts: county records, official site, developer or architect, then listing sites. When sources disagree, use the highest-ranked one and keep the conflict in `facts_source_urls`.

## Rental channel

This describes how a renter signs a lease. Apply the tests in order and stop at the first match.

| Code | Marker | Test |
|---|---|---|
| `A` | Circle | The building or its manager has a site showing live floor plans or an online application |
| `B` | Square | No such site, but a single official leasing office or manager lists on platforms and signs the lease |
| `C` | Triangle | Units are leased by individual owners, usually through an agent |

Mixed buildings use the channel a renter will most likely use and list the others in `channels_all`. Review the `B` count after step 4; merge `B` into `A` if it holds too few buildings to be useful.

## listings.csv

| Column | Meaning |
|---|---|
| `listing_id` | Unique ID |
| `building_id` | Foreign key to `buildings.id` |
| `unit_type` | `studio`, `1b`, `1b_den`, `2b` or `3b_plus` |
| `baths`, `sqft` | Blank if not stated |
| `rent_usd` | Monthly asking base rent |
| `price_basis` | `unit` for a real unit, `floorplan_from` for a "starting at" price |
| `furnished` | `true`, `false` or blank |
| `lease_months` | Lease term the price applies to |
| `free_months` | Concession in months; blank if none is stated |
| `monthly_fees_usd` | Mandatory monthly fees stated by the source |
| `source_name`, `source_url` | Where the price was seen |
| `observed_on` | Date seen, YYYY-MM-DD |

### Rent sources

Use the official site's floor plans for channel `A`. Use Miami Condo Solution's daily long-term rental pages for condos. Sites that refuse automated access are not scraped; they may only be cited from search results, with `retrieved_via` or `source_name` saying so.

`rent_usd` is base rent. On official sites this is the "From" price, and the gap to "Total Rent + Mandatory Fees" goes in `monthly_fees_usd`. A blank `lease_months` on a long-term page counts as a 12-month lease.

### Primary source

Each unit type uses one primary source: the one with the most rows, with ties going to the official site, then Apartments.com, RentCafe and Miami Condo Solution. Other sources are shown as a cross-check and never mixed into the statistics. The page shows the source and date beside every rent. `data/raw/apartments_plans.csv` and `apartments_fees.csv` hold values read from Apartments.com pages.

### Concessions

`data/raw/concessions.csv` holds current offers. `status` is `stated`, `select`, `conflict` or `expired`. Net rent = median × (lease − months free) / lease, and is shown only for `stated` and `select`. Offers never change base rent or all-in totals, because most cover select homes and may end before a February move-in.

### Rent rules

- Count only asking rents for leases of 12 months or longer, seen within 60 days of the data as-of date. Drop sublets and short-term stays.
- Remove duplicates of one unit across sites. Keep the most official source.
- Headline statistics use unfurnished units and units with unknown furnishing. If fewer than 3 remain, use all units and label the result "includes furnished".
- For each `unit_type`, report min, median, max and `n`. Show a low-sample label when `n` is below 3.
- `1b` excludes `1b_den`, which has its own row.
- Show "from floor plans" when a summary rests on `floorplan_from` prices, because those medians are not unit medians.
- Net effective rent = `rent_usd` × (`lease_months` − `free_months`) / `lease_months`, plus `monthly_fees_usd`. It is shown only when a concession or fee is documented.

## Amenities, tours and galleries

`data/amenities.csv` has one row per building and amenity, with an evidence line and source. It is built by `tools/extract_amenities.py` from official and Miami Condo Solution text in `data/raw/amenity_text/` and Condo Black Book fields in `data/raw/cbb/`. A missing amenity means unlisted, not absent.

`data/contacts.json` is built by `tools/build_contacts.py` from `data/raw/links/`. Zillow links are address searches and are not verified. Condo Black Book records are accepted only when the page address matches.

## ratings.csv

| Column | Meaning |
|---|---|
| `building_id` | Foreign key to `buildings.id` |
| `platform` | Platform name |
| `group` | `resident`, `short_stay` or `context` |
| `score_raw`, `scale` | Score as published and its maximum |
| `score_5` | `score_raw` / `scale` × 5 |
| `review_count` | Number of reviews; blank if not shown |
| `latest_review_on` | Newest review date if visible |
| `url` | The platform's page for the building |
| `retrieved_via` | `direct`, or the third-party site that reported the score |
| `observed_on` | Date seen, YYYY-MM-DD |
| `notes` | Anything that limits comparability |

### Platforms

| Group | Platforms | Use |
|---|---|---|
| `resident` | Google, Yelp, Apartments.com, ApartmentRatings, ForRent, Lucid Rents, VeryApt | Shown and used in the rating score |
| `resident`, to test in the pilot | Niche, Zillow, RentCafe, Apartment List | Added only if they publish building-level ratings |
| `short_stay` | Expedia, Trip.com, Momondo | Shown separately for hotel-style buildings; excluded from the rating score |
| `context` | BBB | Rates companies, not buildings; never in the rating score |

ForRent, Apartment Finder and Apartments.com appear to share one review pool, so they count as one platform named `CoStar network`.

## reviews/<id>.jsonl

One review per line: `platform`, `stars` (1 to 5), `date_text` as shown, `date` (YYYY-MM, approximate when the platform shows relative dates), `likes`, `text`, `translated` (true when only a machine translation was available), `owner_reply` (true or false) and `observed_on`. Reviewer names are never stored.

## review_summaries.csv

| Column | Meaning |
|---|---|
| `building_id` | Foreign key to `buildings.id` |
| `summary_en`, `summary_zh` | AI summary of all stored reviews, one short paragraph |
| `tags_en`, `tags_zh` | Neutral descriptive tags, separated by `;` |
| `pros_en`, `pros_zh` | Pros, shown as green tags, separated by `;` |
| `cons_en`, `cons_zh` | Cons, shown as red tags, separated by `;` |
| `reviews_used` | Number of reviews read for the summary |
| `generated_on` | Date the summary was written |

Every pro and con must appear in several reviews or in a sourced fact. A theme raised by one reviewer is not a tag.

`data/raw/apartments_amenities.csv` holds items read from Apartments.com amenity sections. `tools/extract_amenities.py` maps them through an exact item table and uses them only to fill gaps left by the sources above. `Washer/Dryer Hookup` and `Laundry Facilities` do not count as in-unit laundry.

`data/raw/broker_units.csv` holds rental rows from Bogatov Realty building pages, which mirror the MLS with list dates. Use it only where other sources have no price for that unit type.

`data/raw/apartments_units.csv` holds individual units read from Apartments.com building pages, stored with `price_basis` `unit`. Drop units that contradict building facts, such as a 36th-floor unit in a 14-story building.

`data/raw/apartments_overall.csv` holds the Apartments.com 5-star overall score, which blends renter reviews with the CoStar building rating. It is shown separately and left out of the weighted score. `status` is `stars`, `no_ratings` or `page_not_found`. Accept a page only when the address and street both match, because 1010 Brickell Ave and 1010 SW 2nd Ave share a number. Carbonell is the one recorded exception: Apartments.com gives 681 Brickell Key Dr, but the name, 2005 build year and 39 stories match. `page_not_found` means only single-unit pages turned up.

## Weighted score

Rating for building *i*: each platform score is shrunk toward that platform's mean across all buildings, S = (v·R + m·C) / (v + m), with v = review count and m = 20. Platforms are then averaged, weighted by v. A platform with no review count is shown but left out of this calculation.

Each factor is first converted to a percentile rank from 0 to 1 across all buildings, so units do not affect the result. The default weights are 1B all-in cost 25, rating 15, walking time 15, safety 15, price per square foot 10, unit size 10 and building age 10. Viewers can change them with sliders.

If a building lacks an input, its weight is shared across the remaining inputs. A building with no 1B all-in cost or walking time gets no score. When sorting by a single field, missing values go last in both directions.
