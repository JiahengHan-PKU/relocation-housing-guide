---
name: housing-page
description: Build and test the single-file bilingual map and list page for a housing guide. Use when changing the page, adding filters or modules, setting up a basemap, generating the HTML, or checking how it opens on phones and in chat apps.
---

# Housing page

## Build

`tools/build_all.sh` runs the pipeline. `tools/build_page.py` inlines the app, data, basemap, places, icons and compressed photos into one file. City-specific text belongs in `config/city.json` under `page.strings`, which override the defaults in `web/app.js`. Never put a city name in `web/app.js`.

Basemap: run `tools/fetch_basemap.py`, then `tools/build_basemap.py`. For a coastal city, add `sea_points` that fall in open water, so the coast polygons close correctly. Keep OpenStreetMap attribution.

## Design rules

- Encode price by color and rental channel by shape, so nothing relies on color alone.
- A click opens the building panel in both the map and the list, and a tap opens it on phones. Hover shows only a name label. Hover-opened panels flicker while the mouse moves, and users found that tiresome.
- The building page's back button returns to the view it was opened from: map to map (zoom and position kept), list to list. `route()` records the last map or list view in `returnView`; a page opened from a direct link falls back to the list.
- Sorting means quality, not raw value. ▼ always runs best to worst, and ▲ worst to best, so rent, walking time and crime sort low first under ▼. Mark each column's better end in `LOWER_IS_BETTER`. Show the arrows on every column, keep missing values last in both directions, and give narrow screens a sort bar so hidden columns stay sortable.
- Convert every score input to a percentile rank before weighting, so dollars, square feet and rating points are comparable. Explain this next to the weights. Percentile ranks stretch clustered values, such as ratings, and flatten real gaps, so say so when presenting scores.
- Put source and date beside every rent.
- Filters apply to both map and list. Say "listed", never "not available", when an amenity is absent from a source.
- Provide modules for 3D tours, in-person tours and leasing links, built from verified links.
- Show the neighborhood as a linked map and list: summary tiles, category toggles, 5- and 10-minute walking rings, and rows that highlight their place and draw a line to the building. Say when a chain is not in the data, rather than leaving a gap. Set brands and transit lines in the `nearby` config.
- Keep safety visible in the list as well as on the building page, and say that ZIP-level grades are averages.
- Make score weights adjustable.
- Keep the income figure out unless the user asked for it (`page.annual_base`). When null, the page hides that module.

## Known traps

- Safari broke `<details>` combined with `display:contents`. Use a button and a panel.
- A page rendered entirely by JavaScript is blank where scripts are blocked. WeChat could not open the interactive file, and neither phone preview nor a chat app proves it works. Find out which app readers use before saying the file can simply be sent.
- Always ship the PDF too. `tools/build_summary.py` and `tools/render_pdf.py` write a phone-sized PDF with an overview and one section per building. PDF opens where HTML does not. The HTML also shows a plain table inside `<noscript>`.
- iOS Safari cannot open a local HTML file directly. For a phone test, serve the folder on the local network and stop the server afterward:

      python3 -m http.server 8000 --directory dist

- Remote floor plan images need a network connection. Say so on the page.
- Keep the file under about 10 MB so that chat apps accept it.

## Test

Open every building page on WebKit and Chrome at desktop and phone widths, and fail on script errors or horizontal overflow. Test a second city too: a run on the original city cannot reveal coordinates left in the code, which is how a hardcoded main map once survived. `tests/smoke_test.py` covers the pipeline from an empty folder. After a change to shared tools, rebuild an existing city and compare `web/data.json` with the previous output.

Finally, open the file on a real phone by the route readers will use. A headless test does not prove this.
