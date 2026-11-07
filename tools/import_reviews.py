"""Move review files downloaded by Chrome into the project."""

import glob
import json
import os
import re


def import_reviews(download_dir, review_dir, meta_path):
    """Keep the largest download per building and write it as JSON lines.

    Args:
        download_dir: Folder where Chrome saved reviews-<id>*.json files.
        review_dir: Folder for <id>.jsonl review files.
        meta_path: JSON lines file collecting each building's Google rating.

    Returns:
        A dict of building id to the number of reviews imported.
    """
    best = {}
    for path in glob.glob(os.path.join(download_dir, "reviews-*.json")):
        building_id = re.match(r"reviews-(.+?)(?: \(\d+\))?\.json$", os.path.basename(path)).group(1)
        data = json.load(open(path))
        reviews = data["reviews"] if isinstance(data, dict) else data
        if building_id not in best or len(reviews) > len(best[building_id][1]):
            best[building_id] = (data.get("meta") if isinstance(data, dict) else None, reviews, path)
    metas = {}
    if os.path.exists(meta_path):
        metas = {json.loads(line)["id"]: json.loads(line) for line in open(meta_path)}
    for building_id, (meta, reviews, _) in best.items():
        with open(os.path.join(review_dir, f"{building_id}.jsonl"), "w") as handle:
            for review in reviews:
                handle.write(json.dumps(review, ensure_ascii=False) + "\n")
        if meta:
            metas[building_id] = meta
    with open(meta_path, "w") as handle:
        for meta in metas.values():
            handle.write(json.dumps(meta, ensure_ascii=False) + "\n")
    for path in glob.glob(os.path.join(download_dir, "reviews-*.json")):
        os.remove(path)
    return {building_id: len(value[1]) for building_id, value in best.items()}
