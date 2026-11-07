# relocation-housing-guide

A template for building a private, bilingual, single-file apartment guide for a move to any city. Start with `.claude/skills/city-housing-guide/SKILL.md`.

## Conventions

- `data/` is the source of truth and stays out of git. Generated files go in `dist/` and are never hand-edited.
- City-specific values live in `config/city.json`. Do not put a city name in `tools/*.py` or `web/app.js`. Collectors written for one city go in `tools/sources/<city>/`.
- Python tools go in `tools/`, typically one function per file of about 30 lines, with Google-style docstrings.
- All code, comments and data column names are in English. Chinese appears only as page translations.

## Data rules

Every published number has a source and a date. Blank means unknown. Label estimates. Reviewer names are never stored. See `docs/DATA_DICTIONARY.md`.

## Never commit

Reviews, third-party photos, floor plan images, raw platform records, generated pages, or anyone's income, employer or name. `.gitignore` covers `data/` and `dist/`; check before adding a new folder.

## Test

    python tests/smoke_test.py
