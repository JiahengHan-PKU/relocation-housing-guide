#!/bin/bash
# Long-running collection; progress goes to logs/amenity_text.log.
cd "$(dirname "$0")/.." || exit 1
.venv/bin/python tools/collect_amenity_text.py data/buildings.csv data/listings.csv data/raw/amenity_text >> logs/amenity_text.log 2>&1
