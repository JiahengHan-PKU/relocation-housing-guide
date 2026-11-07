---
name: housing-platform-access
description: Read rental platforms and listing sites safely and politely for housing research. Use before fetching Apartments.com, Zillow, Yelp, Google Maps, condo databases or broker sites, when a site returns 403, 429 or a human check, or when a page reads as empty.
---

# Platform access

## Limits

Do not spoof identity, use stealth tooling, or solve CAPTCHAs. Stop at a human check and skip that site. On 403, 429 or an error page, stop and wait. Check each site's terms if the result will be published.

Allowed routes: official APIs with the user's key, pages the user saves, search results, and reading in the user's own browser at a low rate.

## Pace

- Wait 4 to 8 seconds between pages.
- Keep browser batches to about three pages, because a long batch can time out and keep running.
- A collector must raise on 429, never record it as "page not found". Silent 429s once produced false empty records that blocked later runs, because collectors skip saved files.
- After a rate limit, delete any empty records the run wrote, wait, and retry slowly.

## Finding pages

- A site's own search box misses pages. Before calling a page missing, run a web search limited to that domain. This found four building pages reported as not found.
- Try the building's aliases and old names.
- Check the address on every page you accept.
- Separate three outcomes: no page found, page exists with no data, and could not check.

## Reading pages

- Scope reads to the section you need, such as the amenities block, and exclude "nearby" content. Otherwise you collect another building's data.
- Short platform items need an exact-match table. Regex rules written for sentences miss them or misfire.
- JavaScript-rendered pages read as navigation only through plain fetching. Open them in a browser, or look for embedded JSON such as `__NEXT_DATA__`.
- Return small results. Browser tool output truncates near 1,000 characters, so filter and read in chunks.
- Results containing URLs with query strings may be blocked by the browser tool. Return only the fields you need.
- Verify parsers against a screenshot on at least one page.

## Calibrate

Compare a new parser with a known value before trusting it. Count unique IDs, not string matches: a raw count of 3D tours was inflated by duplicates, and unique IDs matched the known value.
