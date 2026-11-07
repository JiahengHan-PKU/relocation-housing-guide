"""Inline the app, data, basemap and photos into one HTML file."""

import base64
import glob
import html as html_lib
import io
import json
import os
import re

from PIL import Image

from city_config import load_city


def noscript_table(data):
    """Return a plain table for viewers that do not run JavaScript."""
    rows = []
    for b in sorted(data["buildings"], key=lambda item: item["walk_min"]):
        rent = (b["rents"].get("1b") or {}).get("median")
        price = f"${rent:,.0f}" if rent else "–"
        rows.append(f"<tr><td>{html_lib.escape(b['name'])}</td><td>{b['walk_min']:.0f} min</td><td>{price}</td></tr>")
    return ('<div style="padding:16px;font:15px/1.5 sans-serif;background:#fff;color:#1c2733"><p><b>This viewer blocks scripts, so the map and building pages cannot run. '
            'Open the file in Safari or Chrome, or use the PDF version.</b></p><p><b>当前查看器禁止运行脚本，地图和楼盘页无法显示。请用 Safari 或 Chrome 打开，或查看 PDF 版。</b></p>'
            f'<table style="border-collapse:collapse;width:100%" cellpadding="4"><tr><th align="left">Building</th><th align="left">Walk</th><th align="left">1B median</th></tr>{"".join(rows)}</table></div>')


def build_page(root, out_path):
    """Write a self-contained HTML page that needs no server or files.

    Photos are shrunk to 640 px JPEG and embedded as data URIs.

    Args:
        root: The housing-map folder.
        out_path: Destination HTML file.

    Returns:
        The output size in megabytes.
    """
    read = lambda p: open(os.path.join(root, p), encoding="utf-8").read()
    data = json.loads(read("web/data.json"))
    photos = {}
    for b in data["buildings"]:
        src = os.path.join(root, "data/photos", b["photo_file"] or "")
        if b["photo_file"] and os.path.isfile(src):
            image = Image.open(src).convert("RGB")
            image.thumbnail((640, 640))
            buffer = io.BytesIO()
            image.save(buffer, "JPEG", quality=58)
            photos[b["id"]] = "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode()
    pois = [{key: value for key, value in p.items() if value is not None}
            for p in json.loads(read("data/pois.json")) if p["lat"]]
    icons = {}
    for path in glob.glob(os.path.join(root, "vendor/icons/*.svg")):
        icons[os.path.basename(path)[:-4]] = "".join(re.findall(r"<(?:path|circle|rect|line|polyline|polygon|ellipse)[^>]*/>", open(path).read()))
    html = read("web/app.html").replace("<!--NOSCRIPT-->", noscript_table(data), 1)
    for marker, value in [("/*LEAFLET_CSS*/", read("vendor/leaflet.css")),
                          ("/*LEAFLET_JS*/", read("vendor/leaflet.js")),
                          ("/*DATA_JSON*/", json.dumps(data, ensure_ascii=False, separators=(",", ":"))),
                          ("/*BASEMAP_JSON*/", read("web/basemap.json")),
                          ("/*POIS_JSON*/", json.dumps(pois, separators=(",", ":"))),
                          ("/*PHOTOS_JSON*/", json.dumps(photos)),
                          ("/*ICONS_JSON*/", json.dumps(icons)),
                          ("/*APP_JS*/", read("web/app.js"))]:
        html = html.replace(marker, value.replace("</script", "<\\/script"), 1)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    open(out_path, "w", encoding="utf-8").write(html)
    return round(os.path.getsize(out_path) / 1e6, 2)


if __name__ == "__main__":
    print(build_page(".", load_city().get("output", "dist/housing-guide.html")), "MB")
