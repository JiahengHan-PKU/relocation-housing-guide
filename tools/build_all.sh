#!/bin/bash
# Rebuild the page from data/. Run from the repository root.
set -e
export PYTHONPATH=tools
python3 -c "from merge_raw import merge_raw; merge_raw('data/raw', 'data', 'data/raw/condo_rentals.json')"
python3 tools/sync_facts.py
python3 tools/extract_amenities.py
python3 tools/build_contacts.py
python3 tools/build_nearby.py
python3 tools/export_data.py
python3 tools/build_page.py
python3 tools/build_summary.py
python3 tools/render_pdf.py dist/summary.html dist/summary.pdf
rm -f dist/summary.html
