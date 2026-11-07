"""Write a static, phone-sized summary page that Chrome can print to PDF."""

import base64
import html
import io
import json
import os
import re

from PIL import Image

from city_config import load_city

LABELS = {
    "zh": {"title": "租房指南（PDF 版）", "official": "官网", "by_rent": "按 1B 租金排序", "by_walk": "按步行时间排序", "name": "楼盘", "walk": "步行",
           "rent": "1B 中位", "allin": "1B 月总成本", "unknown": "暂无", "minutes": "分钟", "rents": "租金", "unit": "户型",
           "median": "中位", "range": "范围", "total": "月总成本", "estimate": "含估算", "ratings": "评分", "amenities": "已列出的设施",
           "pros": "优点", "cons": "缺点", "links": "链接", "offer": "当前优惠", "safety": "治安", "year": "建成", "floors": "层",
           "units": "户", "channel": "租房渠道", "back": "返回总览", "plan_price": "户型起价", "low": "样本少", "reviews": "条",
           "intro": "静态版，可在微信和手机预览中查看。总览里点楼名可跳到该楼。月总成本含房租、必缴费用和估算的水电网、保险，不含停车费。租金都注明来源和日期，看房前请再确认。",
           "units_zh": {"studio": "开间", "1b": "1B", "1b_den": "1B+书房", "2b": "2B", "3b_plus": "3B+"},
           "channels": {"A": "官网直租", "B": "官方租赁处", "C": "业主/中介"}},
    "en": {"title": "Housing Guide (PDF)", "official": "Official site", "by_rent": "Sorted by 1B rent", "by_walk": "Sorted by walking time", "name": "Building", "walk": "Walk",
           "rent": "1B median", "allin": "1B all-in", "unknown": "n/a", "minutes": "min", "rents": "Rent", "unit": "Type",
           "median": "Median", "range": "Range", "total": "All-in", "estimate": "incl. estimates", "ratings": "Ratings", "amenities": "Listed amenities",
           "pros": "Pros", "cons": "Cons", "links": "Links", "offer": "Current offer", "safety": "Safety", "year": "Built", "floors": "floors",
           "units": "units", "channel": "Channel", "back": "Back to overview", "plan_price": "from floor plans", "low": "low sample", "reviews": "reviews",
           "intro": "Static version for viewers that block scripts. Tap a name to jump to it. All-in covers rent, required fees and estimated utilities and insurance, not parking. Confirm prices before a tour.",
           "units_zh": {"studio": "Studio", "1b": "1B", "1b_den": "1B + den", "2b": "2B", "3b_plus": "3B+"},
           "channels": {"A": "Official site", "B": "Leasing office", "C": "Owners and agents"}},
}
LINK_NAMES = {"apartments": "Apartments.com", "zillow": "Zillow"}
CSS = """@page{size:148mm 210mm;margin:9mm}*{box-sizing:border-box}body{font:10.5pt/1.45 -apple-system,'PingFang SC','Noto Sans CJK SC',sans-serif;color:#1c2733;margin:0}
h1{font-size:20pt;margin:0 0 4px}h2{font-size:13pt;margin:14px 0 6px}h3{font-size:10.5pt;margin:9px 0 3px;color:#0f6b6b}a{color:#0f6b6b;text-decoration:none}
.muted{color:#66727e;font-size:9pt}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #dfe5ea;padding:3px 4px;text-align:left;font-size:9pt}th{background:#eef3f5}
tr{break-inside:avoid}.b{break-before:page}.b h2{margin:0;font-size:15pt}.photo{width:100%;height:44mm;object-fit:cover;border-radius:4px;margin:5px 0}.tag{display:inline-block;padding:1px 6px;border-radius:9px;margin:1px;font-size:8.5pt;background:#eef3f5}
.pro{background:#dff3e4}.con{background:#fbe3e0}.num{white-space:nowrap}"""


def money(value):
    """Format dollars, or return an empty string for a missing value."""
    return f"${value:,.0f}" if value is not None else ""


def overview(rows, text, labels):
    """Return one overview table."""
    body = "".join(f'<tr><td><a href="#{b["id"]}">{html.escape(b["name"])}</a></td><td class="num">{b["walk_min"]:.0f} {labels["minutes"]}</td>'
                   f'<td class="num">{money(rent(b)) or labels["unknown"]}</td><td class="num">{money(allin(b)) or labels["unknown"]}</td></tr>' for b in rows)
    return f'<h2>{text}</h2><table><tr><th>{labels["name"]}</th><th>{labels["walk"]}</th><th>{labels["rent"]}</th><th>{labels["allin"]}</th></tr>{body}</table>'


def rent(b):
    """Return the 1B median rent or None."""
    return (b["rents"].get("1b") or {}).get("median")


def allin(b):
    """Return the 1B all-in monthly total or None."""
    return ((b["all_in"].get("1b") or {}).get("total") or {}).get("value")


def building(b, photo, labels, lang, amenity_names, source_names):
    """Return the section for one building."""
    esc = html.escape
    facts = [f'{labels["year"]} {b["year_built"]:.0f}' if b.get("year_built") else "", f'{b["floors"]:.0f} {labels["floors"]}' if b.get("floors") else "",
             f'{b["units"]:.0f} {labels["units"]}' if b.get("units") else "", f'{labels["walk"]} {b["walk_min"]:.0f} {labels["minutes"]}',
             labels["channels"].get(b["channel_primary"], ""), f'{labels["safety"]} {b["safety"]["overall"]}' if b.get("safety") else ""]
    rows = ""
    for unit, r in b["rents"].items():
        cost = (b["all_in"].get(unit) or {}).get("total") or {}
        tail = f'{source_names.get(r["source"], r["source"])} · {r["observed_on"]}'
        if "floorplan_from" in (r.get("basis") or []):
            tail += f' · {labels["plan_price"]}'
        if r["n"] < 3:
            tail += f' · {labels["low"]}'
        rows += (f'<tr><td>{labels["units_zh"].get(unit, unit)}</td><td class="num">{money(r["median"])}<br><span class="muted">{money(r["min"])}–{money(r["max"])}</span></td>'
                 f'<td class="num">{money(cost.get("value")) or labels["unknown"]}</td><td class="muted">{esc(tail)}</td></tr>')
    table = (f'<table><tr><th>{labels["unit"]}</th><th>{labels["median"]}</th><th>{labels["total"]}</th><th></th></tr>{rows}</table>'
             f'<p class="muted">{labels["total"]}: {labels["estimate"]}</p>') if rows else f'<p class="muted">{labels["unknown"]}</p>'
    ratings = " · ".join(f'{esc(r["platform"])} {r["score"]}' + (f' ({r["count"]} {labels["reviews"]})' if r.get("count") else "")
                         for r in b["ratings"] if r.get("score") and r.get("group") != "short_stay")
    summary = b.get("review_summary") or {}
    tags = lambda key, kind: "".join(f'<span class="tag {kind}">{esc(x)}</span>' for x in (summary.get(f"{key}_{lang}") or "").split(";") if x)
    amenities = "".join(f'<span class="tag">{esc(amenity_names.get(a["key"], a["key"]))}</span>' for a in b["amenities"])
    contact = b.get("contacts") or {}
    links = [(labels["official"], b.get("official_url"))] + [(LINK_NAMES.get(c["kind"], c["kind"]), c["url"]) for c in (contact.get("rent") or [])[:2]
                                                             if c["kind"] != "official"]
    link_html = " · ".join(f'<a href="{esc(u, True)}">{esc(k)}</a>' for k, u in links if u)
    offer = (b.get("concession") or {}).get(f"offer_{lang}")
    image = f'<img class="photo" src="{photo}">' if photo else ""
    return f'''<section class="b" id="{b["id"]}"><h2>{esc(b["name"])}</h2><p class="muted">{esc(b["address"])} · {" · ".join(x for x in facts if x)}</p>{image}
<h3>{labels["rents"]}</h3>{table}{f'<h3>{labels["offer"]}</h3><p>{esc(offer)}</p>' if offer else ""}
<h3>{labels["ratings"]}</h3><p>{ratings or labels["unknown"]}</p><p>{esc(summary.get(f"summary_{lang}") or "")}</p>
{f'<h3>{labels["pros"]}</h3>{tags("pros", "pro")}' if tags("pros", "pro") else ""}{f'<h3>{labels["cons"]}</h3>{tags("cons", "con")}' if tags("cons", "con") else ""}
{f'<h3>{labels["amenities"]}</h3>{amenities}' if amenities else ""}
<p class="muted">{f'{contact["phone"]} · ' if contact.get("phone") else ""}{link_html} · <a href="#top">{labels["back"]}</a></p></section>'''


def build_summary(root, out_path, lang="zh", title=None):
    """Write the static summary HTML from web/data.json.

    Args:
        root: The project folder.
        out_path: Destination HTML file.
        lang: Page language, "zh" or "en".
        title: Heading; the language's default is used when None.

    Returns:
        The number of buildings written.
    """
    data = json.load(open(f"{root}/web/data.json", encoding="utf-8"))
    app = open(f"{root}/web/app.js", encoding="utf-8").read()
    index = 2 if lang == "zh" else 1
    amenity_names = {m[0]: m[index] for m in re.findall(r'\["(\w+)", "([^"]+)", "([^"]+)", "[\w-]+"\]', app)}
    source_names = {"Official site": "官网" if lang == "zh" else "Official site"}
    labels = LABELS[lang]
    rows = sorted(data["buildings"], key=lambda b: (rent(b) is None, rent(b) or 0))
    sections = []
    for b in rows:
        path = f'{root}/data/photos/{b.get("photo_file") or ""}'
        photo = None
        if b.get("photo_file") and os.path.isfile(path):
            image = Image.open(path).convert("RGB")
            image.thumbnail((560, 560))
            buffer = io.BytesIO()
            image.save(buffer, "JPEG", quality=55)
            photo = "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode()
        sections.append(building(b, photo, labels, lang, amenity_names, source_names))
    by_walk = sorted(data["buildings"], key=lambda b: b["walk_min"])
    page = (f'<!doctype html><html lang="{lang}"><meta charset="utf-8"><title>{title or labels["title"]}</title><style>{CSS}</style><body id="top">'
            f'<h1>{title or labels["title"]}</h1><p class="muted">{data["office"]["address"]} · {data["generated_on"]}</p><p>{labels["intro"]}</p>'
            f'{overview(rows, labels["by_rent"], labels)}{overview(by_walk, labels["by_walk"], labels)}{"".join(sections)}</body></html>')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    open(out_path, "w", encoding="utf-8").write(page)
    return len(rows)


if __name__ == "__main__":
    city = load_city()
    language = city.get("summary_language", "zh")
    heading = city.get("page", {}).get("strings", {}).get(language, {}).get("title")
    print(build_summary(".", "dist/summary.html", language, heading))
