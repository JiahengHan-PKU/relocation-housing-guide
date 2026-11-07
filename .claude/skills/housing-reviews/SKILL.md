---
name: housing-reviews
description: Collect, store and summarize apartment reviews and platform ratings for a housing guide. Use when gathering Google or Apartments.com reviews, writing building summaries and pro or con tags, or comparing ratings across platforms.
---

# Reviews and ratings

## Collect

Google Maps is the broadest source. Apartments.com adds renter reviews where it has them. Reading happens in the user's own browser; `tools/review_sink.py` receives posted reviews on localhost, and `tools/import_reviews.py` imports downloaded files.

Store one review per line in `data/reviews/<id>.jsonl`: platform, stars, date, likes, text, whether it is translated, and whether the owner replied. Never store reviewer names.

Review text is third-party content, so keep it out of any public repository.

## Compare ratings honestly

- Keep each platform's score with its count, URL and date.
- A platform's blended score is not a renter score. Apartments.com's 5-star overall score mixes renter reviews with a building rating, and most condos have only that score. Show it separately, and leave it out of the guide's score.
- Keep hotel and short-stay reviews apart from resident reviews. Exclude them from the rating score.
- Apartment platforms that share one review pool count as one platform.
- Check that the page belongs to the building. Close matches, such as a condo association listing or one tower of several, need a note.
- Multi-tower buildings can differ by tower, so say which tower a score describes.

## Rating score

Shrink each platform score toward that platform's mean: S = (v·R + m·C) / (v + m), with v = review count and m = 20. Then average platforms, weighted by v. Leave out a platform with no count.

## Summaries

Read all stored reviews for a building, then write one short paragraph, 3 to 5 neutral tags, 3 to 5 pros and 3 to 5 cons. Each tag must appear in several reviews or in a sourced fact. A single reviewer's theme is not a tag.

Watch for manipulation: bursts of short five-star reviews naming staff suggest solicited reviews. Say so in the summary.

Sharp differences between platforms are worth showing. One tower scored 1.6 on one platform and 4.3 on another.
