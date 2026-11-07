(() => {
"use strict";
const D = window.DATA, B = D.buildings, REV = D.reviews || {};
const byId = Object.fromEntries(B.map(b => [b.id, b]));

/* ---------- language ---------- */
const T = {
  en: { title: "Housing Guide", subtitle: "data as of ", map: "Map", list: "List",
    colorBy: "Color by 1B rent", median: "median", lowest: "lowest", search: "Search buildings",
    legendPrice: "1B base rent", noPrice: "no 1B listing", office: "Office", shapeTitle: "How you rent",
    chA: "Official site", chB: "Leasing office", chC: "Owners & agents",
    chAlong: "Lease from the building's own website", chBlong: "One official leasing office, listed on platforms", chClong: "Individual owners lease units, usually through an agent",
    rental: "Rental tower", condo: "Condo", hotel_condo: "Hotel condo", mixed: "Mixed use",
    walk: "walk", min: "min", year: "Built", floors: "Floors", units: "Units", developer: "Developer",
    rent: "Rent by unit type", type: "Type", low: "Low", mid: "Median", high: "High", n: "n", allin: "All-in / mo",
    ratings: "Ratings", reviews: "reviews", open: "Open building page", site: "Official site",
    studio: "Studio", "1b": "1 bed", "1b_den": "1 bed + den", "2b": "2 bed", "3b_plus": "3+ bed",
    name: "Building", score: "Score", rating: "Rating", size: "1B size", ppsf: "$/sqft", age: "Building age",
    google: "Google", apts: "Apts.com", walkHead: "Walk", nbGrocery: "Groceries", nbPharmacy: "Pharmacies", nbTransit: "Transit", nbDining: "Food and coffee", nbOutdoor: "Parks and gyms", nbSafety: "Safety", nbRestaurant: "Restaurant", nbCafe: "Cafe", nbDogPark: "Dog park", nbWithin5: "within a 5-minute walk", nbFiveShort: "5-min walk", nbBus300: "bus stops within 300 m", nbShowAll: "Show all within a 10-minute walk", nbNotFound: "Not in our data for this area", nbNote: "Walking times are estimates: straight-line distance × 1.25 at 80 m a minute. Places come from OpenStreetMap, which may miss some restaurants. Select a place to draw it on the map.", weights: "Score weights", weightsNote: "Each factor becomes a percentile rank from 0 to 1 across all buildings before weighting, so dollars, square feet and rating points are comparable. A missing factor's weight is shared across the others, except that a building with no 1B all-in cost gets no score.", sortBy: "Sort by", sortAsc: "Ascending", sortDesc: "Descending", aptsNone: "Apartments.com: no renter ratings yet", aptsMissing: "Apartments.com: building page not found",  aptsOverall: "Apartments.com overall", aptsOverallNote: "Apartments.com's 5-star score blends renter reviews with the CoStar building rating. It is left out of this guide's score.", goTitle: "See it and rent it", goVirtual: "3D virtual tours", goTour: "Book an in-person tour", goRent: "Rent or apply", goVirtualNone: "No 3D tour found. Ask the leasing office or a listing agent for a video walkthrough.", goTip: "Many leasing offices close on Sundays, so book weekdays and Saturdays first.", goCondoNote: "Units are leased by individual owners. Book through a listing agent.", phoneLabel: "Leasing office", kOfficial: "Official site", kOfficialTour: "Book on the official site", kOfficialApply: "Apply on the official site", kApartments: "Apartments.com", kApartmentsTour: "Request a tour on Apartments.com", k3d: "Apartments.com 3D tours", kVideo: "Official video tour", kCondo: "Owner listings", kCondoSub: "Live owner listings; agents arrange showings", kCbb: "Condo database", kCbbSub: "Listings and floor plans", kZillow: "Zillow", kZillowSub: "Address search", galTitle: "Listing floor plans", galNote: "Original listing images, shown online only. Open one to see it full size.", galAll: "All", galPlans: "plans", filters: "Filters", amenities: "Amenities", amenNote: "From the building's site and listing platforms. A missing amenity may simply be unlisted.", amenNone: "No amenity list found yet.",
    fRent: "1B rent up to", fAllin: "All-in up to", fWalk: "Walk up to", fRating: "Rating at least", fYear: "Built from", fAny: "any", fTypes: "Building type", fAmen: "Must have", fMore: "Also", fHas1b: "Has 1B price", fPlans: "Has floor plans", fOffer: "Has an offer", fReset: "Clear filters", fShow: "buildings match", fPricedOnly: "Price filters hide buildings with no 1B price.", weightsReset: "Reset to default", weightsCustom: "adjusted", safety: "Safety", noData: "No data yet",
    back: "Back to list", backMap: "Back to map", facts: "Building facts", about: "About", architect: "Architect", manager: "Manager",
    channel: "How you rent", address: "Address", costTitle: "Monthly cost, 1 bed", fees: "Mandatory building fees",
    electricity: "Electricity (FPL)", water_sewer: "Water & sewer", internet: "Internet", renters_insurance: "Renters insurance",
    total: "All-in per month", estimate: "estimate", actual: "actual", base: "Base rent (median)", onetime: "One-time charges",
    parking: "Parking (not counted)", rules: "Rental rules", min_lease: "Minimum lease", leases_per_year: "Leases per year",
    approval: "Association approval", approval_time: "Approval time", application_fee: "Application fee", deposit: "Deposit",
    pets: "Pets", income: "Income or credit", short_term: "Short-term rentals", unknown: "Ask the building",
    incomeTitle: "Can I afford it?", incomeLabel: "Annual base",
    rule40: "Max rent at the 40× rule", rule30: "Max all-in at 30% of income", gapOk: "Room to spare", gapBad: "Short by",
    reviewTitle: "What residents say", aiSummary: "AI summary", platform: "Platform", sortedLikes: "Sorted by likes",
    showMore: "Show more", likes: "likes", ownerReply: "owner replied", noReviews: "No reviews collected yet.",
    nearby: "Around the building", supermarket: "Nearest supermarket", publix: "Publix", whole_foods: "Whole Foods",
    trader_joes: "Trader Joe's", pharmacy: "Pharmacy", metromover: "Metromover", metrorail: "Metrorail", brightline: "Brightline",
    bus: "Bus stops within 300 m", restaurants: "Restaurants & cafés within 400 m", park: "Nearest park", gym: "Gym (outside building)",
    none: "none in the area", sources: "Sources", notes: "Research notes", pros: "Pros", cons: "Cons",
    summaryPending: "Review summary in progress.", fromPlans: "floor plan start price", lowN: "few listings", inclFurn: "includes furnished",
    walkTo: "to the office", weightRent: "All-in rent", weightPpsf: "$/sqft", weightSize: "Unit size", weightRating: "Ratings",
    weightWalk: "Walk time", weightAge: "Newer building", weightSafety: "Safety", ofTotal: "of non-rent costs estimated" },
  zh: { title: "租房指南", subtitle: "数据日期 ", map: "地图", list: "列表",
    colorBy: "颜色：1B 租金", median: "中位数", lowest: "最低价", search: "搜索楼盘",
    legendPrice: "1B 基础租金", noPrice: "暂无 1B 挂牌", office: "公司", shapeTitle: "租房方式",
    chA: "官网直租", chB: "官方租赁处", chC: "业主/中介",
    chAlong: "直接在大楼官网申请", chBlong: "由统一的官方租赁办公室出租，在平台挂牌", chClong: "由个人业主出租，通常经中介",
    rental: "整栋出租楼", condo: "Condo 公寓", hotel_condo: "酒店式 Condo", mixed: "混合用途",
    walk: "步行", min: "分钟", year: "建成", floors: "层数", units: "户数", developer: "开发商",
    rent: "各房型租金", type: "房型", low: "最低", mid: "中位", high: "最高", n: "样本", allin: "每月合计",
    ratings: "评分", reviews: "条评论", open: "打开楼盘页", site: "官网",
    studio: "开间", "1b": "一居", "1b_den": "一居+书房", "2b": "两居", "3b_plus": "三居及以上",
    name: "楼盘", score: "综合分", rating: "评分", size: "1B 面积", ppsf: "每平尺", age: "楼龄",
    google: "Google", apts: "Apts.com", walkHead: "步行", nbGrocery: "超市", nbPharmacy: "药店", nbTransit: "交通", nbDining: "餐饮咖啡", nbOutdoor: "公园与健身", nbSafety: "治安", nbRestaurant: "餐厅", nbCafe: "咖啡馆", nbDogPark: "狗公园", nbWithin5: "步行 5 分钟内", nbFiveShort: "步行 5 分钟内", nbBus300: "300 米内公交站", nbShowAll: "显示 10 分钟步行范围内全部", nbNotFound: "本区域数据未收录", nbNote: "步行时间为估算：直线距离 × 1.25，按每分钟 80 米计算。地点来自 OpenStreetMap，餐饮可能不全。点选地点可在地图上画出路线方向。", weights: "评分权重", weightsNote: "每一项都先换算成所有楼中的百分位排名（0 到 1），再按权重相加，所以美元、平方英尺和评分的单位差异不会影响结果。某栋楼缺某一项时，该项权重分摊给其余项；但没有 1B 月总成本的楼不计分。", sortBy: "排序方式", sortAsc: "升序", sortDesc: "降序", aptsNone: "Apartments.com：暂无住户评分", aptsMissing: "Apartments.com：未找到楼栋页",  aptsOverall: "Apartments.com 综合星级", aptsOverallNote: "Apartments.com 的 5 星综合评分，由住户评分和 CoStar 建筑评级混合而成，不计入本指南的综合评分。", goTitle: "看房与租房", goVirtual: "3D 虚拟看房", goTour: "预约线下看房", goRent: "租房与申请", goVirtualNone: "没有找到 3D 看房。可以向租赁办公室或挂牌经纪索要视频。", goTip: "不少租赁办公室周日不开门，建议优先约工作日和周六。", goCondoNote: "这栋楼由业主个人出租，需要通过挂牌经纪预约。", phoneLabel: "租赁办公室", kOfficial: "官方网站", kOfficialTour: "在官网预约", kOfficialApply: "在官网申请", kApartments: "Apartments.com", kApartmentsTour: "在 Apartments.com 预约", k3d: "Apartments.com 3D 看房", kVideo: "官方视频看房", kCondo: "业主挂牌", kCondoSub: "实时业主挂牌，经纪可安排看房", kCbb: "公寓数据库", kCbbSub: "挂牌与户型图", kZillow: "Zillow", kZillowSub: "按地址搜索", galTitle: "挂牌户型图", galNote: "挂牌平台原图，需联网显示。点开可看大图。", galAll: "全部", galPlans: "个户型", filters: "筛选", amenities: "设施", amenNote: "来自楼盘官网和挂牌平台。未列出不代表没有。", amenNone: "暂未找到设施列表。",
    fRent: "1B 租金上限", fAllin: "每月合计上限", fWalk: "步行上限", fRating: "评分不低于", fYear: "建成不早于", fAny: "不限", fTypes: "楼盘类型", fAmen: "必须有", fMore: "其他", fHas1b: "有 1B 价格", fPlans: "有户型图", fOffer: "有当前优惠", fReset: "清除筛选", fShow: "栋符合", fPricedOnly: "价格筛选会隐藏没有 1B 价格的楼。", weightsReset: "恢复默认", weightsCustom: "已调整", safety: "治安", noData: "暂无数据",
    back: "返回列表", backMap: "返回地图", facts: "基本信息", about: "简介", architect: "建筑师", manager: "物业",
    channel: "租房方式", address: "地址", costTitle: "一居每月开销", fees: "大楼强制费用",
    electricity: "电费 (FPL)", water_sewer: "水费和污水费", internet: "网络", renters_insurance: "租客保险",
    total: "每月合计", estimate: "估计值", actual: "实际值", base: "基础租金（中位）", onetime: "一次性费用",
    parking: "停车（不计入）", rules: "租赁规则", min_lease: "最短租期", leases_per_year: "每年可出租次数",
    approval: "协会审批", approval_time: "审批时长", application_fee: "申请费", deposit: "押金",
    pets: "宠物", income: "收入或信用要求", short_term: "短租", unknown: "需向楼方确认",
    incomeTitle: "租得起吗？", incomeLabel: "年 base",
    rule40: "按 40 倍规则可租上限", rule30: "按收入 30% 的每月合计上限", gapOk: "还有余量", gapBad: "差额",
    reviewTitle: "住户怎么说", aiSummary: "AI 总结", platform: "平台", sortedLikes: "按点赞数排序",
    showMore: "显示更多", likes: "赞", ownerReply: "业主已回复", noReviews: "尚未收集到评论。",
    nearby: "周边配套", supermarket: "最近超市", publix: "Publix", whole_foods: "Whole Foods",
    trader_joes: "Trader Joe's", pharmacy: "药店", metromover: "Metromover", metrorail: "Metrorail", brightline: "Brightline",
    bus: "300 米内公交站", restaurants: "400 米内餐厅和咖啡馆", park: "最近公园", gym: "健身房（楼外）",
    none: "区域内没有", sources: "来源", notes: "调研备注", pros: "优点", cons: "缺点",
    summaryPending: "评论总结生成中。", fromPlans: "户型起价", lowN: "样本少", inclFurn: "含带家具",
    walkTo: "到公司", weightRent: "每月合计", weightPpsf: "每平尺价格", weightSize: "面积", weightRating: "评分",
    weightWalk: "步行时间", weightAge: "楼越新越好", weightSafety: "治安", ofTotal: "的非租金开销为估计值" },
};
for (const code of ["en", "zh"]) Object.assign(T[code], ((D.city || {}).strings || {})[code]);
const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
let lang = store.get("lang") || ((navigator.language || "").startsWith("zh") ? "zh" : "en");
const t = k => (T[lang] && T[lang][k]) || T.en[k] || k;
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const money = v => v == null ? "–" : "$" + Math.round(v).toLocaleString("en-US");
const stars = s => { const f = Math.round(s); return "★".repeat(f) + "☆".repeat(5 - f); };
const css = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

/* ---------- metrics and score ---------- */
const PLATFORM_MEAN = {};
(() => { const acc = {}; B.forEach(b => b.ratings.filter(r => r.group === "resident" && r.count).forEach(r => {
  (acc[r.platform] = acc[r.platform] || []).push(r.score); }));
  Object.entries(acc).forEach(([p, v]) => PLATFORM_MEAN[p] = v.reduce((a, c) => a + c, 0) / v.length); })();
function combinedRating(b) {
  const rs = b.ratings.filter(r => r.group === "resident" && r.count > 0);
  if (!rs.length) return null;
  let num = 0, den = 0;
  rs.forEach(r => { const m = 20, c = PLATFORM_MEAN[r.platform] ?? 4; num += r.count * (r.count * r.score + m * c) / (r.count + m); den += r.count; });
  return den ? num / den : null;
}
function metrics(b) {
  const r1 = b.rents["1b"], a1 = b.all_in["1b"];
  return {
    rentMid: r1 ? r1.median : null, rentMin: r1 ? r1.min : null,
    allin: a1 ? a1.total.value : null, size: r1 && r1.sqft ? r1.sqft : null,
    ppsf: r1 && r1.sqft ? r1.median / r1.sqft : null, rating: combinedRating(b),
    walk: b.walk_min, age: b.year_built ? 2027 - b.year_built : null,
    safety: b.safety ? +b.safety.rate_per_1000 : null,
    google: (b.ratings.find(r => r.platform === "Google" && r.group === "resident") || null),
    apts: (b.ratings.find(r => r.platform === "Apartments.com") || b.ratings.find(r => r.group === "overall") || null),
  };
}
const M = Object.fromEntries(B.map(b => [b.id, metrics(b)]));
const WEIGHTS = [ ["allin", "weightRent", 25, -1], ["ppsf", "weightPpsf", 10, -1], ["size", "weightSize", 10, 1],
  ["rating", "weightRating", 15, 1], ["walk", "weightWalk", 15, -1], ["age", "weightAge", 10, -1], ["safety", "weightSafety", 15, -1] ];
const weights = Object.fromEntries(WEIGHTS.map(w => [w[0], w[2]]));
function percentile(key, dir) {
  const vals = B.map(b => M[b.id][key]).filter(v => v != null).sort((a, b) => a - b);
  return v => { if (v == null || vals.length < 2) return null;
    const below = vals.filter(x => x < v).length, equal = vals.filter(x => x === v).length;
    const p = (below + (equal - 1) / 2) / (vals.length - 1); return dir > 0 ? p : 1 - p; };
}
function computeScores() {
  const ranks = Object.fromEntries(WEIGHTS.map(([k, , , d]) => [k, percentile(k, d)]));
  B.forEach(b => { let s = 0, w = 0, used = 0;
    WEIGHTS.forEach(([k]) => { const r = ranks[k](M[b.id][k]); if (r != null && weights[k] > 0) { s += r * weights[k]; w += weights[k]; used++; } });
    const ok = M[b.id].allin != null && M[b.id].walk != null;
    M[b.id].score = ok && w ? 100 * s / w : null; M[b.id].scoreInputs = used; });
}
computeScores();

/* ---------- shared bits ---------- */
const priceSteps = () => [css("--p1"), css("--p2"), css("--p3"), css("--p4"), css("--p5")];
let colorBy = "median";
const priceVals = () => B.map(b => colorBy === "min" ? M[b.id].rentMin : M[b.id].rentMid).filter(v => v != null).sort((a, b) => a - b);
function priceBreaks() { const v = priceVals(); return [0.2, 0.4, 0.6, 0.8].map(q => v[Math.floor(q * (v.length - 1))]); }
function priceColor(b) {
  const v = colorBy === "min" ? M[b.id].rentMin : M[b.id].rentMid; if (v == null) return null;
  const br = priceBreaks(); let i = 0; while (i < br.length && v > br[i]) i++; return priceSteps()[i];
}
function shapeSvg(ch, fill, size = 18) {
  const stroke = css("--surface"), f = fill || "none", sw = fill ? 2 : 2.5, sc = fill ? stroke : css("--nodata");
  const h = size, m = h / 2;
  const body = ch === "A" ? `<circle cx="${m}" cy="${m}" r="${m - 2}"/>`
    : ch === "B" ? `<rect x="2.5" y="2.5" width="${h - 5}" height="${h - 5}" rx="2"/>`
    : `<path d="M${m} 2 L${h - 2} ${h - 3} L2 ${h - 3} Z"/>`;
  return `<svg width="${h}" height="${h}" viewBox="0 0 ${h} ${h}" fill="${f}" stroke="${sc}" stroke-width="${sw}" stroke-linejoin="round">${body}</svg>`;
}
const chName = c => c ? t("ch" + c) : "–";
function splitTags(s) { return (s || "").split(";").map(x => x.trim()).filter(Boolean); }
function autoTags(b) {
  const out = [t(b.building_type) || b.building_type];
  if (b.year_built >= 2015) out.push(lang === "zh" ? `${b.year_built} 年新楼` : `Built ${b.year_built}`);
  if (b.floors >= 50) out.push(lang === "zh" ? `${b.floors} 层高楼` : `${b.floors} floors`);
  if (b.walk_min != null) out.push(`${t("walk")} ${Math.round(b.walk_min)} ${t("min")}`);
  return out;
}
function photoSrc(b) { return (window.PHOTOS || {})[b.id] || null; }

/* ---------- info card ---------- */
const SOURCE_LABELS = {
  "Official site": { en: "official leasing site", zh: "官方租赁网站" },
  "Apartments.com": { en: "Apartments.com, the property's listing", zh: "Apartments.com 楼方挂牌" },
  "RentCafe": { en: "RentCafe, the manager's listing", zh: "RentCafe 物业挂牌" },
  ...((D.city || {}).source_labels || {}),
};
const sourceName = s => (SOURCE_LABELS[s] || {})[lang] || s;
const sourceLine = r => `${sourceName(r.source)} · ${esc(r.observed_on)}`;
function rentSources(b) {
  const zh = lang === "zh";
  const lines = Object.entries(b.rents).map(([u, r]) => {
    const check = (r.cross_check || []).map(c => `${sourceName(c.source)} ${zh ? "中位" : "median"} ${money(c.median)} (${c.n})`).join(zh ? "；" : "; ");
    return `<li><b>${t(u)}</b> ${sourceLine(r)}${check ? `<br><span class="muted">${zh ? "交叉核对：" : "Cross-check: "}${check}</span>` : ""}</li>`;
  }).join("");
  return lines ? `<p class="section-title" style="margin-top:10px">${zh ? "价格来源与日期" : "Price source and date"}</p><ul class="muted" style="margin:0;padding-left:16px;font-size:12px;line-height:1.5">${lines}</ul>` : "";
}
const AMENITIES = [["pool", "Pool", "泳池", "waves"], ["gym", "Fitness center", "健身房", "dumbbell"], ["rooftop", "Rooftop", "屋顶露台", "sunset"], ["spa", "Spa or sauna", "水疗/桑拿", "flower-2"],
  ["concierge", "Concierge", "礼宾", "bell-ring"], ["security", "24-hour security", "24 小时安保", "shield-check"], ["valet", "Valet", "代客泊车", "car"], ["garage", "Garage parking", "车库", "square-parking"],
  ["ev", "EV charging", "充电桩", "plug-zap"], ["laundry", "In-unit laundry", "室内洗衣机", "washing-machine"], ["pets", "Pet friendly", "可养宠物", "paw-print"], ["dog", "Dog park or spa", "狗公园/宠物美容", "dog"],
  ["work", "Coworking", "共享办公", "laptop"], ["theater", "Theater", "影音室", "clapperboard"], ["lounge", "Resident lounge", "住户休息室", "sofa"], ["games", "Game room", "游戏室", "gamepad-2"],
  ["sports", "Sports courts", "球场", "trophy"], ["bbq", "BBQ area", "烧烤区", "flame"], ["kids", "Kids' area", "儿童区", "baby"], ["marina", "Marina", "游艇码头", "anchor"],
  ["waterfront", "Waterfront", "临水", "sailboat"], ["retail", "On-site dining", "楼内餐饮", "store"], ["bike", "Bike storage", "自行车房", "bike"], ["package", "Package room", "包裹间", "package"], ["storage", "Storage", "储物间", "archive"]];
const icon = name => `<svg class="ic" viewBox="0 0 24 24" aria-hidden="true">${(window.ICONS || {})[name] || ""}</svg>`;
const amenLabel = a => lang === "zh" ? a[2] : a[1];
function amenityRow(b) {
  const list = AMENITIES.filter(a => (b.amenities || []).some(x => x.key === a[0]));
  if (!list.length) return "";
  return `<div><p class="section-title">${t("amenities")}</p><div class="amen-row" style="margin-top:6px">${list.slice(0, 8).map(a => `<span title="${esc(amenLabel(a))}">${icon(a[3])}</span>`).join("")}${list.length > 8 ? `<b>+${list.length - 8}</b>` : ""}</div></div>`;
}
function amenityPanel(b) {
  const have = b.amenities || [];
  const list = AMENITIES.map(a => [a, have.find(x => x.key === a[0])]).filter(([, x]) => x);
  const urls = [...new Set(have.map(x => x.url))].slice(0, 3);
  return `<div class="panel"><h3>${t("amenities")}</h3>${list.length ? `<div class="amen-grid">${list.map(([a, x]) => `<div class="amen" title="${esc(x.evidence)}">${icon(a[3])}<span>${esc(amenLabel(a))}</span></div>`).join("")}</div>
    <p class="amen-note">${t("amenNote")} ${urls.map((u, i) => `<a href="${esc(u)}" target="_blank" rel="noopener">${lang === "zh" ? "来源" : "source"}${urls.length > 1 ? " " + (i + 1) : ""}</a>`).join(" · ")}</p>` : `<p class="muted">${t("amenNone")}</p>`}</div>`;
}
function goLink(url, title, sub) {
  return `<a class="go-link" href="${esc(url)}" target="_blank" rel="noopener"><span>${esc(title)}${sub ? `<small>${esc(sub)}</small>` : ""}</span>${icon("external-link")}</a>`;
}
function goPanel(b) {
  const c = b.contacts; if (!c) return "";
  const zh = lang === "zh";
  const virtual = c.virtual.map(x => x.kind === "apartments3d" ? goLink(x.url, t("k3d"), zh ? `${x.count} 个 3D 看房` : `${x.count} 3D tours`)
    : goLink(x.url, /video/i.test(x.url + x.text) ? t("kVideo") : (x.text && x.text.length < 30 ? x.text : t("goVirtual")), t("kOfficial"))).join("");
  const nameOf = (x, mode) => ({ official: [mode === "tour" ? t("kOfficialTour") : t("kOfficialApply"), ""], apartments: [mode === "tour" ? t("kApartmentsTour") : t("kApartments"), ""],
    condo: [t("kCondo"), t("kCondoSub")], cbb: [t("kCbb"), t("kCbbSub")], zillow: [t("kZillow"), t("kZillowSub")] }[x.kind]);
  const list = (rows, mode) => rows.map(x => goLink(x.url, ...nameOf(x, mode))).join("");
  const owner = b.channel_primary === "C";
  return `<div class="panel"><h3>${t("goTitle")}</h3><div class="go-grid">
    <div class="go-card"><h4>${icon("box")}${t("goVirtual")}</h4>${virtual || `<p>${t("goVirtualNone")}</p>`}</div>
    <div class="go-card"><h4>${icon("calendar-check")}${t("goTour")}</h4>${owner ? `<p>${t("goCondoNote")}</p>` : ""}${c.phone ? `<a class="go-link" href="tel:${esc(c.phone.replace(/[^\d+]/g, ""))}"><span>${esc(c.phone)}<small>${t("phoneLabel")}</small></span>${icon("phone")}</a>` : ""}${list(c.tour, "tour")}</div>
    <div class="go-card"><h4>${icon("key-round")}${t("goRent")}</h4>${list(c.rent, "rent")}</div>
  </div><p class="go-tip">${t("goTip")}</p></div>`;
}
const bedKey = s => { const m = /^(\d)/.exec(String(s || "")); return m ? m[1] : "?"; };
function galleryHtml(b) {
  const g = b.gallery; if (!g) return "";
  const zh = lang === "zh", groups = [...new Set(g.plans.map(p => bedKey(p.beds)))].sort();
  const label = k => k === "0" ? (zh ? "开间" : "Studio") : k === "?" ? (zh ? "其他" : "Other") : zh ? `${k} 居` : `${k} bed`;
  const card = p => `<a class="fp-item" data-bed="${bedKey(p.beds)}" href="${esc(p.full)}" target="_blank" rel="noopener"><img loading="lazy" src="${esc(p.thumb)}" alt="${esc(p.model || "")}" onerror="this.style.display='none'">
    <b>${esc(p.model || "–")}</b><span>${esc(p.beds || "")} · ${p.area ? Math.round(p.area).toLocaleString() + " ft²" : "–"}${p.ext ? ` + ${esc(p.ext)}` : ""}${p.floors ? ` · ${zh ? "楼层" : "floors"} ${esc(p.floors)}` : ""}</span></a>`;
  return `<p class="muted" style="margin:0 0 8px;font-size:12px">${t("galNote")} <a href="${esc(g.url)}" target="_blank" rel="noopener">${t("kCbb")}</a> · ${g.plans.length} ${t("galPlans")}</p>
    <div class="fp-tabs">${[["all", t("galAll")], ...groups.map(k => [k, label(k)])].map(([k, l], i) => `<button type="button" class="f-chip" data-galbed="${k}" aria-pressed="${i === (groups.includes("1") ? groups.indexOf("1") + 1 : 0)}">${esc(l)}</button>`).join("")}</div>
    <div class="fp-gal">${g.plans.map(card).join("")}</div>`;
}
function bindGallery() {
  document.querySelectorAll(".fp-tabs").forEach(tabs => {
    const gal = tabs.nextElementSibling, show = k => gal.querySelectorAll(".fp-item").forEach(i => { i.hidden = k !== "all" && i.dataset.bed !== k; });
    tabs.querySelectorAll("button").forEach(btn => btn.onclick = () => { tabs.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === btn)); show(btn.dataset.galbed); });
    const on = tabs.querySelector('[aria-pressed="true"]'); if (on) show(on.dataset.galbed);
  });
}
const aptsNote = b => { const k = { no_ratings: "aptsNone", page_not_found: "aptsMissing" }[b.apartments_status];
  return k && !b.ratings.some(r => r.platform === "Apartments.com") ? `<p class="muted" style="margin:6px 0 0;font-size:12px">${t(k)}</p>` : ""; };
function concessionHtml(b) {
  const c = b.concession, zh = lang === "zh";
  if (!c) return "";
  const usable = c.status === "stated" || c.status === "select";
  const status = { stated: zh ? "目前有效，2 月未必延续" : "Current offer; may change by February",
    select: zh ? "仅部分户型，且 2 月未必延续" : "Select homes only; may change by February",
    conflict: zh ? "条件与 2 月入住不符" : "Terms do not fit a February move-in",
    expired: zh ? "2 月入住前已到期" : "Ends before a February move-in" }[c.status];
  const nets = usable ? Object.entries(c.net).map(([u, n]) => `<tr><td>${t(u)}</td><td class="r num">${n.free_months}</td><td class="r num">${money(n.net)}</td></tr>`).join("") : "";
  return `<p class="section-title" style="margin-top:10px">${zh ? "当前优惠" : "Current offer"}</p>
    <p style="margin:0"><b>${esc(zh ? c.offer_zh : c.offer_en)}</b> <span class="chip est">${status}</span></p>
    <p class="muted" style="margin:4px 0 0;font-size:12px">${esc(zh ? c.conditions_zh : c.conditions_en)} · <a href="${esc(c.source_url)}" target="_blank" rel="noopener">${zh ? "来源" : "source"}</a> · ${esc(c.observed_on)}</p>
    ${nets ? `<table class="mini" style="margin-top:6px"><thead><tr><th>${t("type")}</th><th class="r">${zh ? "免租月数" : "Months free"}</th><th class="r">${zh ? "若适用的净有效中位租金" : "Net median if it applies"}</th></tr></thead><tbody>${nets}</tbody></table>
    <p class="muted" style="margin:4px 0 0;font-size:12px">${zh ? "按 12 个月租约折算。基础租金和全包成本未扣除优惠。" : "Based on a 12-month lease. Base rent and all-in cost do not include this offer."}</p>` : ""}`;
}
function cardHtml(b) {
  const m = M[b.id], rs = b.review_summary;
  const tags = rs ? splitTags(rs["tags_" + lang] || rs.tags_en) : autoTags(b);
  const pros = rs ? splitTags(rs["pros_" + lang] || rs.pros_en) : [], cons = rs ? splitTags(rs["cons_" + lang] || rs.cons_en) : [];
  const ph = photoSrc(b);
  const rentRows = Object.entries(b.rents).map(([u, r]) => `<tr><td>${t(u)}</td><td class="r num">${money(r.min)}</td><td class="r num">${money(r.median)}</td><td class="r num">${money(r.max)}</td><td class="r num">${r.n}</td><td class="r num">${b.all_in[u] ? money(b.all_in[u].total.value) : "–"}</td></tr>`).join("");
  const ratings = b.ratings.filter(r => r.count || r.platform === "Google" || r.group === "overall").map(r => `<tr><td>${esc(r.group === "overall" ? t("aptsOverall") : r.platform)}${r.group === "overall" ? ` <span class="chip est" title="${esc(t("aptsOverallNote"))}">${lang === "zh" ? "含建筑评级" : "includes building rating"}</span>` : ""}${r.group === "short_stay" ? ` <span class="chip est">${lang === "zh" ? "短住" : "short stay"}</span>` : ""}</td><td class="r"><span class="stars">${stars(r.score)}</span> <span class="num">${r.score.toFixed(1)}</span></td><td class="r num muted">${r.count ? r.count.toLocaleString() : "–"}</td></tr>`).join("");
  return `<div class="photo">${ph ? `<img src="${ph}" alt="${esc(b.name)}">` : `<div class="nophoto">${lang === "zh" ? "暂无官网照片" : "No official photo"}</div>`}<button class="close" aria-label="Close">×</button></div>
  <div class="body">
    <div><h2>${esc(b.name)}</h2><div class="sub"><span>${esc(b.address)}</span></div></div>
    <div class="chips">${tags.map(x => `<span class="chip">${esc(x)}</span>`).join("")}</div>
    ${pros.length || cons.length ? `${pros.length ? `<div class="chips">${pros.map(x => `<span class="chip pro">＋ ${esc(x)}</span>`).join("")}</div>` : ""}${cons.length ? `<div class="chips">${cons.map(x => `<span class="chip con">− ${esc(x)}</span>`).join("")}</div>` : ""}` : `<div class="muted" style="font-size:12px">${t("summaryPending")}</div>`}
    <div class="facts">
      <div class="fact"><b>${b.walk_min != null ? Math.round(b.walk_min) : "–"}</b><small>${t("min")} ${t("walkTo")}</small></div>
      <div class="fact"><b>${b.year_built ?? "–"}</b><small>${t("year")}</small></div>
      <div class="fact"><b>${b.floors ?? "–"}</b><small>${t("floors")}</small></div>
      <div class="fact"><b>${b.units ?? "–"}</b><small>${t("units")}</small></div>
      <div class="fact"><b>${m.score != null ? Math.round(m.score) : "–"}</b><small>${t("score")} / 100</small></div>
      <div class="fact"><b style="display:flex;align-items:center;gap:6px">${shapeSvg(b.channel_primary, "var(--accent)", 14)}</b><small>${chName(b.channel_primary)}</small></div>
    </div>
    <div class="sub"><span>${t("developer")}: ${esc(b.developer || "–")}</span>${b.official_url ? `<a href="${esc(b.official_url)}" target="_blank" rel="noopener">${t("site")} ↗</a>` : ""}</div>
    ${amenityRow(b)}${rentRows ? `<div><p class="section-title">${t("rent")}</p><table class="mini"><thead><tr><th>${t("type")}</th><th class="r">${t("low")}</th><th class="r">${t("mid")}</th><th class="r">${t("high")}</th><th class="r">${t("n")}</th><th class="r">${t("allin")}</th></tr></thead><tbody>${rentRows}</tbody></table>${rentSources(b)}${concessionHtml(b)}</div>` : ""}
    ${ratings ? `<div><p class="section-title">${t("ratings")}</p><table class="mini"><tbody>${ratings}</tbody></table>${aptsNote(b)}</div>` : ""}
    <a class="btn" href="#b-${b.id}">${t("open")} →</a>
  </div>`;
}
function showCard(el, b, pinned) {
  el.innerHTML = cardHtml(b); el.hidden = false; el.dataset.id = b.id; el.dataset.pinned = pinned ? "1" : "";
  el.querySelector(".close").onclick = () => { el.hidden = true; el.dataset.pinned = ""; document.querySelectorAll("#ledger tr.active").forEach(x => x.classList.remove("active")); };
}
let hideTimer = null;
function hoverCard(el, b) { if (el.dataset.pinned && el.dataset.id !== b.id) return; clearTimeout(hideTimer); showCard(el, b, false); }
function leaveCard(el) { if (el.dataset.pinned) return; hideTimer = setTimeout(() => { if (!el.matches(":hover") && !el.dataset.pinned) el.hidden = true; }, 350); }
const coarse = matchMedia("(hover: none)").matches;

/* ---------- map ---------- */
let map, baseLayer, markerLayer;
function drawBasemap() {
  if (baseLayer) baseLayer.remove();
  const BM = window.BASEMAP, R = L.canvas({ padding: 0.5 }), g = L.layerGroup();
  const poly = (arr, color) => arr.forEach(p => L.polygon(p, { renderer: R, stroke: false, fillColor: color, fillOpacity: 1, interactive: false }).addTo(g));
  poly(BM.sea, css("--water")); poly(BM.land, css("--land")); poly(BM.park, css("--park")); poly(BM.water, css("--water")); poly(BM.building, css("--bldg"));
  const widths = { 1: 5, 2: 4, 3: 3, 4: 2, 5: 1.5 };
  BM.road.slice().sort((a, b) => b[0] - a[0]).forEach(([c, , pts]) => L.polyline(pts, { renderer: R, color: c <= 2 ? css("--road-major") : css("--road"), weight: widths[c], interactive: false, lineCap: "round" }).addTo(g));
  BM.rail.forEach(([k, pts]) => L.polyline(pts, { renderer: R, color: k === "mover" ? css("--mover") : css("--rail"), weight: 2, dashArray: k === "mover" ? "4 3" : null, interactive: false }).addTo(g));
  baseLayer = g.addTo(map);
}
const F = { rent: null, allin: null, walk: null, rating: 0, year: null, types: new Set(), amen: new Set(), has1b: false, plans: false, offer: false };
const FILTER_SLIDERS = [["rent", "fRent", 2000, 7000, 100, v => money(v)], ["allin", "fAllin", 2000, 7500, 100, v => money(v)], ["walk", "fWalk", 3, 25, 1, v => `${v} ${lang === "zh" ? "分钟" : "min"}`],
  ["rating", "fRating", 0, 4.5, 0.5, v => v.toFixed(1)], ["year", "fYear", 1985, 2025, 5, v => String(v)]];
function passes(b) {
  const m = M[b.id];
  if (F.rent != null && (m.rentMid == null || m.rentMid > F.rent)) return false;
  if (F.allin != null && (m.allin == null || m.allin > F.allin)) return false;
  if (F.walk != null && (b.walk_min == null || +b.walk_min > F.walk)) return false;
  if (F.rating && (m.rating == null || m.rating < F.rating)) return false;
  if (F.year != null && (!b.year_built || +b.year_built < F.year)) return false;
  if (F.types.size && !F.types.has(b.building_type)) return false;
  if (F.has1b && m.rentMid == null) return false;
  if (F.plans && !((D.floorplans || {})[b.id] || []).length && !b.gallery) return false;
  if (F.offer && !(b.concession && ["stated", "select"].includes(b.concession.status))) return false;
  return [...F.amen].every(k => (b.amenities || []).some(x => x.key === k));
}
const activeFilters = () => FILTER_SLIDERS.filter(([k]) => k === "rating" ? F.rating > 0 : F[k] != null).length + F.types.size + F.amen.size + [F.has1b, F.plans, F.offer].filter(Boolean).length;
function filtersChanged() {
  const n = activeFilters(), c = document.getElementById("filterCount"), match = B.filter(passes).length;
  c.hidden = !n; c.textContent = n;
  const out = document.getElementById("fMatch"); if (out) out.textContent = `${match} / ${B.length} ${t("fShow")}`;
  if (map) drawMarkers();
  if (!document.getElementById("listView").hidden) drawList();
}
function drawFilters() {
  const panel = document.getElementById("filterPanel");
  document.getElementById("filterLabel").textContent = t("filters");
  document.getElementById("filterIcon").innerHTML = (window.ICONS || {})["sliders-horizontal"] || "";
  const sliderText = (k, fmt) => k === "rating" ? (F.rating ? fmt(F.rating) : t("fAny")) : F[k] == null ? t("fAny") : fmt(F[k]);
  const start = ([k, , lo, hi]) => k === "rating" ? F.rating : k === "year" ? (F.year ?? lo) : (F[k] ?? hi);
  const pct = s => (start(s) - s[2]) / (s[3] - s[2]) * 100;
  const types = ["rental", "condo", "hotel_condo", "mixed"].filter(x => B.some(b => b.building_type === x));
  const toggles = [["has1b", "fHas1b"], ["plans", "fPlans"], ["offer", "fOffer"]];
  const count = k => B.filter(b => (b.amenities || []).some(x => x.key === k)).length;
  panel.innerHTML = `<div class="f-grid">${FILTER_SLIDERS.map(s => `<label class="w-item"><span class="w-head"><span>${t(s[1])}</span><span class="num" id="f-${s[0]}-v">${sliderText(s[0], s[5])}</span></span>
      <input type="range" id="f-${s[0]}" min="${s[2]}" max="${s[3]}" step="${s[4]}" value="${start(s)}" style="--p:${pct(s)}%"></label>`).join("")}</div>
    <div class="f-group"><span>${t("fAmen")}</span><div class="f-chips">${AMENITIES.filter(a => count(a[0])).map(a => `<button type="button" class="f-chip" data-amen="${a[0]}" aria-pressed="${F.amen.has(a[0])}">${icon(a[3])}${esc(amenLabel(a))} <small>${count(a[0])}</small></button>`).join("")}</div></div>
    <div class="f-grid" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))"><div class="f-group"><span>${t("fTypes")}</span><div class="f-chips">${types.map(x => `<button type="button" class="f-chip" data-type="${x}" aria-pressed="${F.types.has(x)}">${esc(t(x))}</button>`).join("")}</div></div>
    <div class="f-group"><span>${t("fMore")}</span><div class="f-chips">${toggles.map(([k, l]) => `<button type="button" class="f-chip" data-flag="${k}" aria-pressed="${F[k]}">${t(l)}</button>`).join("")}</div></div></div>
    <div class="f-foot"><b id="fMatch"></b><button type="button" class="w-reset" id="fReset">${t("fReset")}</button></div>`;
  FILTER_SLIDERS.forEach(s => { const [k, , lo, hi, , fmt] = s, i = document.getElementById("f-" + k); i.oninput = () => { const v = +i.value;
    if (k === "rating") F.rating = v; else if (k === "year") F.year = v === lo ? null : v; else F[k] = v === hi ? null : v;
    i.style.setProperty("--p", (v - lo) / (hi - lo) * 100 + "%"); document.getElementById(`f-${k}-v`).textContent = sliderText(k, fmt); filtersChanged(); }; });
  panel.querySelectorAll(".f-chip").forEach(c => c.onclick = () => { const d = c.dataset, on = c.getAttribute("aria-pressed") !== "true"; c.setAttribute("aria-pressed", on);
    if (d.amen) on ? F.amen.add(d.amen) : F.amen.delete(d.amen); else if (d.type) on ? F.types.add(d.type) : F.types.delete(d.type); else F[d.flag] = on; filtersChanged(); });
  document.getElementById("fReset").onclick = () => { Object.assign(F, { rent: null, allin: null, walk: null, rating: 0, year: null, has1b: false, plans: false, offer: false }); F.types.clear(); F.amen.clear(); drawFilters(); filtersChanged(); };
  filtersChanged();
}
function bindFilters() {
  const toggle = document.getElementById("filterToggle"), panel = document.getElementById("filterPanel");
  toggle.onclick = () => { panel.hidden = !panel.hidden; toggle.setAttribute("aria-expanded", String(!panel.hidden)); };
  drawFilters();
}
function drawMarkers() {
  if (markerLayer) markerLayer.remove();
  markerLayer = L.layerGroup().addTo(map);
  const card = document.getElementById("mapCard");
  B.forEach(b => { if (b.lat == null || !passes(b)) return;
    const pin = L.divIcon({ className: "marker", html: shapeSvg(b.channel_primary, priceColor(b)), iconSize: [18, 18], iconAnchor: [9, 9] });
    const mk = L.marker([b.lat, b.lon], { icon: pin, keyboard: true, title: b.name, riseOnHover: true }).addTo(markerLayer);
    mk.bindTooltip(esc(b.name), { className: "lbl", direction: "right", offset: [10, 0], permanent: false });
    if (!coarse) { mk.on("mouseover", () => hoverCard(card, b)); mk.on("mouseout", () => leaveCard(card)); }
    mk.on("click", () => showCard(card, b, true));
  });
  const office = L.divIcon({ className: "marker", html: `<svg width="26" height="26" viewBox="0 0 26 26"><path d="M13 1.5l3.4 7.2 7.9.9-5.9 5.4 1.7 7.8L13 18.9 5.9 22.8l1.7-7.8L1.7 9.6l7.9-.9z" fill="#d1495b" stroke="#fff" stroke-width="1.5"/></svg>`, iconSize: [26, 26], iconAnchor: [13, 13] });
  L.marker([D.office.lat, D.office.lon], { icon: office, zIndexOffset: 1000, title: D.office.address }).addTo(markerLayer)
    .bindTooltip(`${t("office")} · ${esc(D.office.address)}`, { className: "lbl", direction: "right", offset: [14, 0], permanent: true });
  document.getElementById("mapCard").onmouseleave = () => leaveCard(card);
}
function drawLegend() {
  const br = priceBreaks(), steps = priceSteps();
  document.getElementById("legendSum").textContent = lang === "zh" ? "图例" : "Legend";
  document.getElementById("legend").innerHTML = `<h4 style="margin-top:6px">${t("legendPrice")} · ${t(colorBy === "min" ? "lowest" : "median")}</h4>
    <div class="ramp">${steps.map(c => `<i style="background:${c}"></i>`).join("")}</div>
    <div class="ramp-labels num"><span>≤${money(br[0])}</span><span>${money(br[1])}</span><span>${money(br[2])}</span><span>&gt;${money(br[3])}</span></div>
    <div class="shapes" style="margin-top:6px"><span>${shapeSvg("A", null, 14)} ${t("noPrice")}</span></div>
    <h4 style="margin-top:10px">${t("shapeTitle")}</h4>
    <div class="shapes">${["A", "B", "C"].map(c => `<span title="${esc(t("ch" + c + "long"))}">${shapeSvg(c, css("--p3"), 14)} ${t("ch" + c)}</span>`).join("")}</div>`;
}
function initMap() {
  map = L.map("map", { zoomControl: false, attributionControl: true, minZoom: 12, maxZoom: 18, zoomSnap: 0.5,
    maxBounds: [[25.700, -80.270], [25.840, -80.110]], maxBoundsViscosity: 1 }).setView([25.766, -80.191], 15);
  const fitMin = () => map.setMinZoom(Math.max(12, map.getBoundsZoom(map.options.maxBounds, true)));
  fitMin(); map.on("resize", fitMin);
  map.attributionControl.setPrefix(false).addAttribution("© OpenStreetMap contributors");
  L.control.zoom({ position: "bottomright" }).addTo(map);
  drawBasemap(); drawMarkers(); drawLegend();
}

/* ---------- list ---------- */
const OPT = { year: "opt", floors: "opt", size: "opt", ppsf: "opt", apts: "opt", rating: "opt", safety: "opt", rentMid: "opt2", google: "opt3" };
const COLS = [
  ["name", "name", b => b.name, v => null],
  ["walk", "walkHead", b => M[b.id].walk, v => v == null ? "–" : `${Math.round(v)} ${t("min")}`],
  ["year", "year", b => b.year_built, v => v ?? "–"],
  ["floors", "floors", b => b.floors, v => v ?? "–"],
  ["rentMid", "mid", b => M[b.id].rentMid, money],
  ["allin", "allin", b => M[b.id].allin, money],
  ["size", "size", b => M[b.id].size, v => v == null ? "–" : Math.round(v) + " ft²"],
  ["ppsf", "ppsf", b => M[b.id].ppsf, v => v == null ? "–" : "$" + v.toFixed(2)],
  ["google", "google", b => M[b.id].google ? M[b.id].google.score : null, (v, b) => v == null ? "–" : `${v.toFixed(1)} <span class="muted">(${M[b.id].google.count})</span>`],
  ["apts", "apts", b => M[b.id].apts ? M[b.id].apts.score : null, (v, b) => v == null ? "–" : M[b.id].apts.group === "overall" ? `<span title="${esc(t("aptsOverallNote"))}">★${v.toFixed(1)}</span>` : `${v.toFixed(1)} <span class="muted">(${M[b.id].apts.count})</span>`],
  ["rating", "rating", b => M[b.id].rating, v => v == null ? "–" : v.toFixed(2)],
  ["safety", "safety", b => M[b.id].safety, (v, b) => v == null ? "–" : `${esc(b.safety.overall)} <span class="muted">${v.toFixed(1)}</span>`],
  ["score", "score", b => M[b.id].score, v => v == null ? "–" : `${Math.round(v)}<span class="scorebar"><i style="width:${v}%"></i></span>`],
];
let sortKey = "score", sortDir = -1;
const naturalDir = k => ["walk", "rentMid", "allin", "ppsf", "name", "safety"].includes(k) ? 1 : -1;
const sortArrows = k => `<span class="sort-arrows">${[[1, "▲", "sortAsc"], [-1, "▼", "sortDesc"]].map(([d, mark, label]) =>
  `<button type="button" data-k="${k}" data-dir="${d}" aria-label="${esc(t(label))}" title="${esc(t(label))}" class="${k === sortKey && d === sortDir ? "on" : ""}">${mark}</button>`).join("")}</span>`;
function weightsAreDefault() { return WEIGHTS.every(([k, , d]) => weights[k] === d); }
function drawWeights() {
  const el = document.getElementById("weights");
  document.getElementById("weightsSum").textContent = t("weights");
  document.getElementById("weightsState").textContent = weightsAreDefault() ? "" : "· " + t("weightsCustom");
  document.getElementById("weightsReset").textContent = t("weightsReset");
  document.getElementById("weightsNote").textContent = t("weightsNote");
  el.innerHTML = WEIGHTS.map(([k, label]) => `<label class="w-item"><span class="w-head"><span>${t(label)}</span><span class="num" id="w-${k}-v">${weights[k]}</span></span>
    <input type="range" min="0" max="50" step="5" id="w-${k}" value="${weights[k]}" style="--p:${weights[k] * 2}%"></label>`).join("");
  WEIGHTS.forEach(([k]) => { const i = document.getElementById("w-" + k); i.oninput = () => { weights[k] = +i.value; i.style.setProperty("--p", weights[k] * 2 + "%");
    document.getElementById(`w-${k}-v`).textContent = i.value;
    document.getElementById("weightsState").textContent = weightsAreDefault() ? "" : "· " + t("weightsCustom");
    computeScores(); drawList(); }; });
}
function bindWeights() {
  const toggle = document.getElementById("weightsToggle"), panel = document.getElementById("weightsPanel");
  toggle.onclick = () => { panel.hidden = !panel.hidden; toggle.setAttribute("aria-expanded", String(!panel.hidden)); };
  document.getElementById("weightsReset").onclick = () => { WEIGHTS.forEach(([k, , d]) => { weights[k] = d; }); drawWeights(); computeScores(); drawList(); };
}
function drawList() {
  const q = (document.getElementById("q").value || "").toLowerCase();
  const col = COLS.find(c => c[0] === sortKey);
  const rows = B.filter(passes).filter(b => !q || (b.name + " " + b.address + " " + (b.aliases || "")).toLowerCase().includes(q))
    .sort((a, b) => { const va = col[2](a), vb = col[2](b);
      if (va == null && vb == null) return 0; if (va == null) return 1; if (vb == null) return -1;
      return (typeof va === "string" ? va.localeCompare(vb) : va - vb) * sortDir; });
  const tbl = document.getElementById("ledger");
  tbl.innerHTML = `<thead><tr>${COLS.map(([k, label]) => `<th data-k="${k}" class="${OPT[k] || ""}" ${k === sortKey ? `aria-sort="${sortDir > 0 ? "ascending" : "descending"}"` : ""}><span class="th-in">${t(label)}${sortArrows(k)}</span></th>`).join("")}</tr></thead>
  <tbody>${rows.map(b => `<tr data-id="${b.id}" tabindex="0">${COLS.map(([k, , get, fmt], i) => i === 0
      ? `<td><span class="name-cell">${shapeSvg(b.channel_primary, priceColor(b), 14)}<b>${esc(b.name)}</b> <span class="muted">${esc(t(b.building_type))}</span></span></td>`
      : `<td class="num ${OPT[k] || ""}">${fmt(get(b), b)}</td>`).join("")}</tr>`).join("")}</tbody>`;
  tbl.querySelectorAll("th").forEach(th => th.onclick = () => { const k = th.dataset.k;
    if (k === sortKey) sortDir = -sortDir; else { sortKey = k; sortDir = naturalDir(k); } drawList(); });
  tbl.querySelectorAll(".sort-arrows button").forEach(btn => btn.onclick = e => { e.stopPropagation();
    sortKey = btn.dataset.k; sortDir = +btn.dataset.dir; drawList(); });
  const select = document.getElementById("sortSelect"), dirBtn = document.getElementById("sortDir");
  select.innerHTML = COLS.map(([k, label]) => `<option value="${k}">${esc(t(label))}</option>`).join("");
  select.value = sortKey;
  select.onchange = () => { sortKey = select.value; sortDir = naturalDir(sortKey); drawList(); };
  dirBtn.textContent = sortDir > 0 ? `▲ ${t("sortAsc")}` : `▼ ${t("sortDesc")}`;
  dirBtn.onclick = () => { sortDir = -sortDir; drawList(); };
  document.getElementById("sortLabel").textContent = t("sortBy");
  const card = document.getElementById("listCard");
  tbl.querySelectorAll("tbody tr").forEach(tr => { const b = byId[tr.dataset.id];
    tr.classList.toggle("active", !card.hidden && card.dataset.id === b.id);
    tr.onclick = () => { tbl.querySelectorAll("tr.active").forEach(x => x.classList.remove("active")); tr.classList.add("active"); showCard(card, b, true); };
    tr.onkeydown = e => { if (e.key === "Enter") location.hash = "#b-" + b.id; }; });
}

/* ---------- building page ---------- */
const COST_LABELS = { rent: "base", fees: "fees", electricity: "electricity", water_sewer: "water_sewer", internet: "internet", renters_insurance: "renters_insurance" };
function rulesHtml(b) {
  return `<dl class="kv">${Object.keys(T.en).filter(k => ["min_lease", "leases_per_year", "approval", "approval_time", "application_fee", "deposit", "pets", "income", "short_term"].includes(k))
    .map(k => { const r = b.rules[k]; return `<dt>${t(k)}</dt><dd>${r ? esc(typeof r.value === "object" ? JSON.stringify(r.value) : r.value) + (r.source_url ? ` <a href="${esc(r.source_url)}" target="_blank" rel="noopener">↗</a>` : "") : `<span class="muted">${t("unknown")}</span>`}</dd>`; }).join("")}</dl>`;
}
function costHtml(b) {
  const unit = b.all_in["1b"] ? "1b" : Object.keys(b.all_in)[0];
  if (!unit) return `<p class="muted">${t("noData")}</p>`;
  const a = b.all_in[unit];
  const lines = Object.keys(COST_LABELS).filter(k => a[k]).map(k => `<span>${t(COST_LABELS[k])} ${a[k].basis === "estimate" ? `<span class="chip est">${t("estimate")}</span>` : ""}</span><span class="num">${money(a[k].value)}</span>`).join("");
  const monthly = b.costs.filter(c => c.frequency === "monthly" && c.counted === "True" || c.counted === "true").filter(c => c.frequency === "monthly");
  const once = b.costs.filter(c => c.frequency === "once" && c.amount_usd);
  const parking = b.costs.filter(c => /parking|valet/i.test(c.item));
  return `<p class="muted" style="margin:0">${t(unit)} · ${esc(b.rents[unit].n)} ${lang === "zh" ? "条记录" : "records"} · ${sourceLine(b.rents[unit])}</p>
    <div class="formula">${lines}<span class="total">${t("total")}</span><span class="num total">${money(a.total.value)}</span></div>
    <p class="muted" style="margin:0;font-size:12px">${Math.round(100 * a.share_estimated.value)}% ${t("ofTotal")}</p>
    ${monthly.length ? `<p class="section-title">${t("fees")}</p><table class="mini"><tbody>${monthly.map(c => `<tr><td>${esc(c.item.replace(/_/g, " "))}</td><td class="r num">${c.amount_usd ? money(+c.amount_usd) : "–"}</td><td class="muted">${esc(c.notes || "")}</td></tr>`).join("")}</tbody></table>` : ""}
    ${once.length ? `<p class="section-title">${t("onetime")}</p><table class="mini"><tbody>${once.map(c => `<tr><td>${esc(c.item.replace(/_/g, " "))}</td><td class="r num">${money(+c.amount_usd)}</td></tr>`).join("")}</tbody></table>` : ""}
    ${parking.length ? `<p class="section-title">${t("parking")}</p><table class="mini"><tbody>${parking.map(c => `<tr><td>${esc(c.notes || c.item)}</td><td class="r num">${c.amount_usd ? money(+c.amount_usd) : "–"}</td></tr>`).join("")}</tbody></table>` : ""}`;
}
const ANNUAL_BASE = (D.city || {}).annual_base || null;
function incomeHtml(b) {
  const rent = M[b.id].rentMid, allin = M[b.id].allin;
  if (!rent || !ANNUAL_BASE) return "";
  const cap40 = ANNUAL_BASE / 40, cap30 = ANNUAL_BASE * 0.3 / 12, gap = cap30 - (allin || rent);
  return `<div class="income"><b>${t("incomeTitle")}</b><div class="formula"><span>${t("incomeLabel")}</span><span class="num">${money(ANNUAL_BASE)}</span>
    <span>${t("rule40")}</span><span class="num">${money(cap40)}</span>
    <span>${t("rule30")}</span><span class="num">${money(cap30)}</span>
    <span class="total">${gap >= 0 ? t("gapOk") : t("gapBad")}</span><span class="num total" style="color:var(${gap >= 0 ? "--good" : "--bad"})">${gap >= 0 ? "＋" : "−"}${money(Math.abs(gap))}</span></div></div>`;
}
function reviewsHtml(b) {
  const rs = REV[b.id] || [], sum = b.review_summary;
  if (!rs.length) return `<p class="muted">${t("noReviews")}</p>`;
  const dist = [5, 4, 3, 2, 1].map(s => rs.filter(r => r.stars === s).length), mx = Math.max(...dist, 1);
  return `${sum && (sum["summary_" + lang] || sum.summary_en) ? `<div><p class="section-title">${t("aiSummary")}</p><p style="margin:4px 0 0">${esc(sum["summary_" + lang] || sum.summary_en)}</p></div>` : ""}
    <div class="dist" role="img" aria-label="Star distribution">${[5, 4, 3, 2, 1].map((s, i) => `<span class="num">${s}★</span><div class="track" data-tip="${s}★ · ${dist[i]} ${t("reviews")}"><div class="fill" style="width:${100 * dist[i] / mx}%"></div></div><span class="num muted">${dist[i]}</span>`).join("")}</div>
    <p class="muted" style="margin:0;font-size:12px">Google · ${rs.length} ${t("reviews")} · ${t("sortedLikes")}</p>
    <div id="revList"></div><button class="btn ghost" id="revMore">${t("showMore")}</button>`;
}
function bindReviews(b) {
  const rs = (REV[b.id] || []).filter(r => r.text); let shown = 0;
  const list = document.getElementById("revList"), more = document.getElementById("revMore");
  if (!list) return;
  const add = () => { list.insertAdjacentHTML("beforeend", rs.slice(shown, shown + 15).map(r => `<div class="review"><div class="meta"><span class="stars">${stars(r.stars || 0)}</span><span>${esc(r.date_text || "")}</span><span>👍 ${r.likes || 0}</span>${r.owner_reply ? `<span>${t("ownerReply")}</span>` : ""}</div><p>${esc(r.text)}</p></div>`).join(""));
    shown += 15; more.hidden = shown >= rs.length; };
  more.onclick = add; add();
  document.querySelectorAll("[data-tip]").forEach(el => { const tip = document.getElementById("tip");
    el.onmousemove = e => { tip.hidden = false; tip.textContent = el.dataset.tip; tip.style.left = e.clientX + 12 + "px"; tip.style.top = e.clientY + 12 + "px"; };
    el.onmouseleave = () => tip.hidden = true; });
}
/* ---------- neighborhood ---------- */
const NB_RULES = (D.city || {}).nearby || { brands: {}, transit: {} };
const NB_GROUPS = [["grocery", "nbGrocery", "shopping-basket", "#2c9a68"], ["pharmacy", "nbPharmacy", "pill", "#cf4f76"], ["transit", "nbTransit", "train-front", "#4a63c9"],
  ["dining", "nbDining", "utensils", "#d9821c"], ["outdoor", "nbOutdoor", "trees", "#5b8f35"]];
const nbColor = id => NB_GROUPS.find(g => g[0] === id)[3];
const nbMinutes = m => Math.max(1, Math.round(m / 80));
const nbDistance = (b, p) => 6371000 * 1.25 * Math.hypot((p.lon - b.lon) * Math.PI / 180 * Math.cos(b.lat * Math.PI / 180), (p.lat - b.lat) * Math.PI / 180);
const nbTransitMatch = (p, rule) => rule.network ? String(p.network).toLowerCase().includes(rule.network)
  : /station|halt/.test(p.kind) && (rule.modes || []).includes(p.mode);
const nbGroupOf = p => p.kind === "supermarket" ? "grocery" : /pharmacy|chemist/.test(p.kind) ? "pharmacy" : /station|halt|bus_stop/.test(p.kind) ? "transit"
  : /restaurant|cafe|coffee/.test(p.kind) ? "dining" : /park|fitness_centre/.test(p.kind) && p.kind !== "water_park" ? "outdoor" : null;
function nbModel(b) {
  const pois = (window.POIS || []).map(p => ({ ...p, m: nbDistance(b, p) })).sort((x, y) => x.m - y.m);
  const label = p => `${p.name || ""} ${p.brand || ""}`.toLowerCase();
  const items = [], used = new Set(), missing = [];
  const add = (p, group, sub, ic) => { if (used.has(p)) return; used.add(p); items.push({ p, group, sub, ic, m: p.m, name: p.name || sub }); };
  const seen = new Set();
  pois.filter(p => p.kind === "supermarket").forEach(p => { const key = (p.brand || p.name || "").toLowerCase(); if (!seen.has(key) && seen.size < 4) { seen.add(key); add(p, "grocery", "", "shopping-basket"); } });
  Object.entries(NB_RULES.brands || {}).forEach(([key, word]) => { const p = pois.find(q => label(q).includes(word));
    if (p) add(p, "grocery", t(key), "shopping-basket"); else missing.push(t(key)); });
  pois.filter(p => /pharmacy|chemist/.test(p.kind)).slice(0, 3).forEach(p => add(p, "pharmacy", "", "pill"));
  Object.entries(NB_RULES.transit || {}).forEach(([key, rule]) => pois.filter(p => nbTransitMatch(p, rule)).slice(0, rule.network ? 1 : 2)
    .forEach(p => add(p, "transit", t(key), rule.network ? "train-front" : /mono|mover/.test(key + p.mode) ? "tram-front" : "train-front")));
  const buses = pois.filter(p => p.kind === "bus_stop"), busNear = buses.filter(p => p.m <= 300).length;
  if (buses[0]) add(buses[0], "transit", `${t("bus")} · ${busNear}`, "bus");
  const eats = pois.filter(p => /restaurant|cafe/.test(p.kind)), inFive = eats.filter(p => p.m <= 400).length;
  const named = pois.filter(p => /restaurant|cafe|coffee/.test(p.kind) && p.name);
  named.slice(0, 6).forEach(p => add(p, "dining", t(p.kind === "restaurant" ? "nbRestaurant" : "nbCafe"), p.kind === "restaurant" ? "utensils" : "coffee"));
  const extra = named.slice(6).filter(p => p.m <= 800);
  pois.filter(p => p.kind === "park" && p.name).slice(0, 2).forEach(p => add(p, "outdoor", t("park"), "trees"));
  pois.filter(p => p.kind === "fitness_centre").slice(0, 2).forEach(p => add(p, "outdoor", t("gym"), "dumbbell"));
  pois.filter(p => p.kind === "dog_park" && p.m <= 800).slice(0, 1).forEach(p => add(p, "outdoor", t("nbDogPark"), "trees"));
  extra.forEach(p => add(p, "dining", t(p.kind === "restaurant" ? "nbRestaurant" : "nbCafe"), p.kind === "restaurant" ? "utensils" : "coffee"));
  items.forEach((x, i) => { x.i = i; x.extra = extra.includes(x.p); });
  const dots = pois.filter(p => !used.has(p) && nbGroupOf(p) && p.m <= (p.kind === "bus_stop" ? 300 : 800));
  return { items, dots, missing, inFive, busNear, extraCount: extra.length };
}
let nbState = null;
function nbRow(x) {
  const pct = Math.min(100, x.m / 16);
  return `<button type="button" class="nb-row${x.extra ? " nb-extra" : ""}" data-i="${x.i}" ${x.extra ? "hidden" : ""}><span class="nb-ic" style="--c:${nbColor(x.group)}">${icon(x.ic)}</span>
    <span class="nb-name"><b>${esc(x.name)}</b>${x.sub && x.sub !== x.name ? `<small>${esc(x.sub)}</small>` : ""}</span>
    <span class="nb-dist"><b class="num">${nbMinutes(x.m)} ${t("min")}</b><small class="num">${Math.round(x.m)} m</small><i class="nb-bar"><i style="width:${pct}%;background:${nbColor(x.group)}"></i></i></span></button>`;
}
function nbTile(ic, color, value, label, sub) {
  return `<div class="nb-tile"><span class="nb-ic" style="--c:${color}">${icon(ic)}</span><div><b>${value}</b><small>${esc(label)}</small>${sub ? `<em>${esc(sub)}</em>` : ""}</div></div>`;
}
function nbSafety(b) {
  const z = b.safety; if (!z) return "";
  const tone = /^A/.test(z.overall) ? "good" : /^[BC]/.test(z.overall) ? "mid" : "low";
  return `<div class="nb-safety"><div class="nb-grade ${tone}"><b>${esc(z.overall)}</b><small>${t("nbSafety")}</small></div>
    <div class="nb-safety-body"><div class="nb-subgrades"><span>${lang === "zh" ? "暴力犯罪" : "Violent crime"} <b>${esc(z.violent)}</b></span><span>${lang === "zh" ? "财产犯罪" : "Property crime"} <b>${esc(z.property)}</b></span></div>
    <div class="nb-meter" role="img" aria-label="${esc(z.percentile)}%"><i style="width:${+z.percentile}%"></i></div><p class="muted">${safetyHtml(b).split("<br>")[1] || ""}</p></div></div>`;
}
function nearbyHtml(b) {
  if (b.lat == null) return `<p class="muted">${t("noData")}</p>`;
  const model = nbState = nbModel(b), first = id => model.items.find(x => x.group === id), grocery = first("grocery");
  const rail = model.items.find(x => x.group === "transit" && x.ic !== "bus") || first("transit");
  const sections = NB_GROUPS.map(([id, label, ic]) => { const rows = model.items.filter(x => x.group === id);
    const none = id === "grocery" && model.missing.length ? `<p class="nb-missing">${t("nbNotFound")}: ${esc(model.missing.join(", "))}</p>` : "";
    const head = id === "dining" ? ` <span class="muted">${t("nbWithin5")} · ${model.inFive}</span>` : id === "transit" ? ` <span class="muted">${t("nbBus300")} · ${model.busNear}</span>` : "";
    const more = id === "dining" && model.extraCount ? `<button type="button" class="nb-more" id="nbMore">${t("nbShowAll")} (${model.extraCount})</button>` : "";
    return `<section class="nb-group" data-group="${id}"><h4><span class="nb-ic small" style="--c:${nbColor(id)}">${icon(ic)}</span>${t(label)}${head}</h4>${rows.length ? rows.map(nbRow).join("") : `<p class="nb-missing">${t("none")}</p>`}${none}${more}</section>`; }).join("");
  return `<div class="nb-tiles">
      ${nbTile("shopping-basket", nbColor("grocery"), grocery ? `${nbMinutes(grocery.m)} ${t("min")}` : "–", t("nbGrocery"), grocery ? grocery.name : "")}
      ${nbTile("train-front", nbColor("transit"), rail ? `${nbMinutes(rail.m)} ${t("min")}` : "–", t("nbTransit"), rail ? rail.name : "")}
      ${nbTile("utensils", nbColor("dining"), model.inFive, t("nbDining"), t("nbFiveShort"))}
      ${nbTile("shield", "#5a6670", b.safety ? esc(b.safety.overall) : "–", t("nbSafety"), b.zip ? `ZIP ${b.zip}` : "")}
    </div>
    <div class="nb-chips">${NB_GROUPS.map(([id, label, ic]) => `<button type="button" class="nb-chip on" data-group="${id}" aria-pressed="true" style="--c:${nbColor(id)}">${icon(ic)}${t(label)}</button>`).join("")}</div>
    <div class="nb-body"><div class="nb-map"><div id="pageMap"></div></div><div class="nb-list" id="nbList">${sections}</div></div>
    ${nbSafety(b)}<p class="muted nb-note">${t("nbNote")}</p>`;
}
function drawNeighborhood(pm, b) {
  const model = nbState, layers = Object.fromEntries(NB_GROUPS.map(([id]) => [id, L.layerGroup().addTo(pm)]));
  [[5, 400], [10, 800]].forEach(([min, walk]) => { const r = walk / 1.25;
    L.circle([b.lat, b.lon], { radius: r, color: css("--accent"), weight: 1.2, dashArray: "4 6", fillColor: css("--accent"), fillOpacity: min === 5 ? .07 : .03, interactive: false }).addTo(pm);
    L.marker([b.lat + r / 111320, b.lon], { interactive: false, keyboard: false, icon: L.divIcon({ className: "nb-ring", html: `<span>${min} ${t("min")}</span>`, iconSize: [60, 18], iconAnchor: [30, 9] }) }).addTo(pm); });
  model.dots.forEach(p => { const id = nbGroupOf(p); L.circleMarker([p.lat, p.lon], { radius: p.kind === "bus_stop" ? 2.5 : 3.5, color: "#fff", weight: 1, fillColor: nbColor(id), fillOpacity: .85 }).bindTooltip(esc(p.name || t("bus"))).addTo(layers[id]); });
  const rows = [...document.querySelectorAll(".nb-row")], pins = model.items.map(x => L.marker([x.p.lat, x.p.lon], { riseOnHover: true,
    icon: L.divIcon({ className: "nb-mk", html: `<span class="nb-pin ${x.group}" style="--c:${nbColor(x.group)}">${icon(x.ic)}</span>`, iconSize: [26, 26], iconAnchor: [13, 13] }) }).bindTooltip(`${esc(x.name)} · ${nbMinutes(x.m)} ${t("min")}`, { direction: "top", offset: [0, -12] }));
  model.items.forEach((x, i) => { if (!x.extra) pins[i].addTo(layers[x.group]); });
  let line = null, pinned = null;
  const mark = (i, pan) => { rows.forEach(r => r.classList.toggle("on", +r.dataset.i === i)); pins.forEach((m, j) => { const el = m.getElement(); if (el) el.classList.toggle("on", j === i); });
    if (line) { line.remove(); line = null; } if (i == null) return;
    const x = model.items[i]; if (!layers[x.group].hasLayer(pins[i])) pins[i].addTo(layers[x.group]);
    pins[i].getElement()?.classList.add("on");
    line = L.polyline([[b.lat, b.lon], [x.p.lat, x.p.lon]], { color: nbColor(x.group), weight: 2.5, dashArray: "6 6", interactive: false }).addTo(pm);
    if (pan && !pm.getBounds().pad(-.1).contains(pins[i].getLatLng())) pm.fitBounds(L.latLngBounds([[b.lat, b.lon], [x.p.lat, x.p.lon]]).pad(.3)); };
  rows.forEach(row => { const i = +row.dataset.i;
    row.onclick = () => { pinned = pinned === i ? null : i; mark(pinned, true); };
    if (!coarse) { row.onmouseenter = () => mark(i, false); row.onmouseleave = () => mark(pinned, false); } });
  pins.forEach((pin, i) => pin.on("click", () => { pinned = i; mark(i, false); const list = document.getElementById("nbList"), row = rows[i];
    if (row && !row.hidden && list.scrollHeight > list.clientHeight) list.scrollTop = row.offsetTop - list.offsetTop - 40; }));
  document.querySelectorAll(".nb-chip").forEach(chip => chip.onclick = () => { const id = chip.dataset.group, on = !chip.classList.contains("on");
    chip.classList.toggle("on", on); chip.setAttribute("aria-pressed", String(on)); on ? layers[id].addTo(pm) : layers[id].remove();
    document.querySelector(`.nb-group[data-group="${id}"]`).hidden = !on; });
  const more = document.getElementById("nbMore");
  if (more) more.onclick = () => { rows.filter(r => r.classList.contains("nb-extra")).forEach(r => { r.hidden = false; }); model.items.forEach((x, i) => { if (x.extra) pins[i].addTo(layers.dining); }); more.remove(); };
  L.marker([b.lat, b.lon], { zIndexOffset: 2000, keyboard: false, icon: L.divIcon({ className: "nb-self", html: `<span>${esc(b.name)}</span>`, iconSize: [0, 0] }) }).addTo(pm);
  pm.fitBounds(L.latLng(b.lat, b.lon).toBounds(1500));
}
function safetyHtml(b) {
  const z = b.safety; if (!z) return `<span class="muted">${t("noData")}</span>`;
  const zh = lang === "zh";
  return `<b>${esc(z.overall)}</b> ${zh ? "总体" : "overall"} · ${zh ? "暴力" : "violent"} ${esc(z.violent)} · ${zh ? "财产" : "property"} ${esc(z.property)}
    <br><span class="muted">${zh ? "邮编" : "ZIP"} ${esc(b.zip)} · ${esc(z.rate_per_1000)} ${zh ? "起/千人/年" : "per 1,000 residents a year"} · ${zh ? "优于全美" : "safer than"} ${esc(z.percentile)}% ${zh ? "的邮编区。" : "of US ZIPs."}
    ${zh ? "区内最安全的一侧：" : "Safest part of the ZIP: "}${esc(zh ? ({east:"东部",west:"西部",north:"北部",south:"南部",northeast:"东北部",northwest:"西北部",southeast:"东南部",southwest:"西南部"}[z.safest_part] || z.safest_part) : z.safest_part)}${zh ? "；按邮编区平均，同区内各街区有差异。" : ". ZIP-level averages; blocks within a ZIP differ."}
    <a href="${esc(z.source_url)}" target="_blank" rel="noopener">CrimeGrade ↗</a></span>`;
}
const ROOM_WORDS = [["Master suite", "主卧"], ["Master Bedroom", "主卧"], ["Master bedroom", "主卧"], ["Master Bath", "主卫"],
  ["Living / Dining Area", "客厅/餐厅"], ["Living / Dining Room", "客厅/餐厅"], ["Dining Room", "餐厅"], ["Entry hall", "玄关"], ["Laundry · utility", "洗衣 · 设备间"], ["Utility", "设备间"], ["Sleeping area", "卧区"], ["Great Room", "大客厅"], ["Great room", "大客厅"], ["Patio / Balcony", "露台/阳台"], ["Primary bedroom", "主卧"], ["Walk-in closet", "步入式衣柜"], ["Living / Dining", "客厅/餐厅"], ["Living / Sleeping", "客厅/卧区"], ["Sleeping / Living", "卧区/客厅"],
  ["Living Room", "客厅"], ["Living", "客厅"], ["Dining", "餐厅"], ["Kitchen", "厨房"], ["Bedroom", "卧室"], ["Bath", "卫生间"],
  ["Powder", "客卫"], ["Balcony", "阳台"], ["Terrace", "露台"], ["Office / Media", "书房/影音"], ["Den closet", "书房储物"], ["Den", "书房"],
  ["Dressing", "衣帽间"], ["Entry / Foyer", "玄关"], ["Entry", "玄关"], ["Foyer", "门厅"], ["Gallery", "走廊"], ["Hall", "过道"],
  ["Laundry", "洗衣"], ["W/D", "洗衣"], ["A/C closet", "空调间"], ["A/C", "空调"], ["Pantry", "储物柜"], ["Storage", "储藏"],
  ["Closet", "储物"], ["Mech", "设备间"], ["Stair", "楼梯"], ["Water heater", "热水器"]];
const zhRoom = label => { let out = label; for (const [en, zh] of ROOM_WORDS) out = out.split(en).join(zh); return out.replace(/ (\d)$/, "$1"); };
const ROOM_FILL = { living: "--fp-living", bedroom: "--fp-bed", kitchen: "--fp-wet", bath: "--fp-wet", utility: "--fp-wet", closet: "--fp-closet", den: "--fp-bed", balcony: "--fp-balcony" };
function floorPlanSvg(fp) {
  const S = 12, pad = 22, rs = fp.rooms;
  const minX = Math.min(0, ...rs.map(r => r.x)), minY = Math.min(0, ...rs.map(r => r.y));
  const maxX = Math.max(fp.width_ft, ...rs.map(r => r.x + r.w)), maxY = Math.max(fp.depth_ft, ...rs.map(r => r.y + r.h));
  const W = (maxX - minX) * S + pad * 2, H = (maxY - minY) * S + pad * 2 + 28;
  const X = v => pad + (v - minX) * S, Y = v => pad + (v - minY) * S;
  const fit = (txt, wpx, base) => { const need = txt.length * base * 0.58; return need <= wpx - 4 ? base : need * 0.75 <= wpx - 4 ? base * 0.75 : 0; };
  const rooms = rs.map(r => { const lab = lang === "zh" ? zhRoom(r.label) : r.label, wpx = r.w * S, hpx = r.h * S;
    const fs = lab ? fit(lab, wpx, hpx > 34 && wpx > 60 ? 12 : 10) : 0, showDims = r.dims && fs >= 10 && hpx > 40 && fit(r.dims, wpx, 10) > 0;
    const cx = X(r.x + r.w / 2), cy = Y(r.y + r.h / 2);
    return `<g><title>${esc(lab || "")}${r.dims ? " · " + esc(r.dims) : ""}</title><rect x="${X(r.x)}" y="${Y(r.y)}" width="${wpx}" height="${hpx}" fill="var(${ROOM_FILL[r.type] || "--fp-closet"})" stroke="var(--fp-wall)" stroke-width="${r.type === "balcony" || r.type === "terrace" ? 1 : 1.2}" ${r.type === "balcony" || r.type === "terrace" ? 'stroke-dasharray="4 3"' : ""}/>
      ${fs ? `<text x="${cx}" y="${cy + (showDims ? -4 : fs / 3)}" text-anchor="middle" class="fp-label" font-size="${fs}">${esc(lab)}</text>` : ""}
      ${showDims ? `<text x="${cx}" y="${cy + 11}" text-anchor="middle" class="fp-dim">${esc(r.dims)}</text>` : ""}</g>`; }).join("");
  const outline = `<rect x="${X(0)}" y="${Y(0)}" width="${fp.width_ft * S}" height="${fp.depth_ft * S}" fill="none" stroke="var(--fp-wall)" stroke-width="4"/>`;
  const win = (fp.windows || []).map(([a, b, c, d]) => `<line x1="${X(a)}" y1="${Y(b)}" x2="${X(c)}" y2="${Y(d)}" stroke="var(--fp-glass)" stroke-width="5"/>`).join("");
  const entry = fp.entry ? `<circle cx="${X(fp.entry[0])}" cy="${Y(fp.entry[1])}" r="5" fill="var(--accent)" stroke="var(--surface)" stroke-width="1.5"/>` : "";
  const sbY = H - 14, sb = `<g class="fp-dim"><line x1="${pad}" y1="${sbY}" x2="${pad + 10 * S}" y2="${sbY}" stroke="var(--fp-wall)" stroke-width="2"/><line x1="${pad}" y1="${sbY - 4}" x2="${pad}" y2="${sbY + 4}" stroke="var(--fp-wall)"/><line x1="${pad + 10 * S}" y1="${sbY - 4}" x2="${pad + 10 * S}" y2="${sbY + 4}" stroke="var(--fp-wall)"/><text x="${pad + 10 * S + 6}" y="${sbY + 4}">10 ft · 3 m</text></g>`;
  const compass = fp.orientation_deg == null ? `<text x="${W - pad}" y="${sbY + 18}" text-anchor="end" class="fp-dim">${lang === "zh" ? "朝向未知" : "Orientation unknown"}</text>`
    : `<g transform="translate(${W - pad - 8} ${sbY - 4}) rotate(${fp.orientation_deg})"><path d="M0 -11 L5 6 L0 2 L-5 6 Z" fill="var(--ink)"/><text y="-14" text-anchor="middle" class="fp-dim" font-weight="600">N</text></g>`;
  return `<svg viewBox="0 0 ${W} ${H + 12}" width="100%" style="max-width:${Math.round(W * 1.1)}px" role="img" aria-label="${esc(fp.plan)} floor plan">${rooms}${outline}${win}${entry}${sb}${compass}</svg>`;
}
function floorPlansHtml(b) {
  const fps = (window.DATA.floorplans || {})[b.id] || [];
  if (!fps.length) return galleryHtml(b) || `<p class="muted">${lang === "zh" ? "暂未找到户型图。" : "No floor plans found yet."}</p>`;
  return `<p class="muted" style="margin:0;font-size:12px">${lang === "zh" ? "按官方户型图统一比例重绘；房间位置为近似值，尺寸取自官方标注。蓝线为窗户，圆点为入户门，在电脑上鼠标悬停可看房间名称和尺寸。" : "Redrawn at one common scale from the official plans; room positions are approximate, dimensions come from the official labels. Blue lines are windows; the dot marks the entry; on a computer, hover a room for its name and size."}</p>
    <div class="fp-grid">${fps.map(fp => `<figure class="fp"><figcaption><b>${esc(fp.plan)}</b> · ${t(fp.unit_type)} · ${fp.baths} ${lang === "zh" ? "卫" : "bath"} · <span class="num">${fp.sqft} ft²</span> <a href="${esc(fp.source_image)}" target="_blank" rel="noopener">${lang === "zh" ? "原图" : "original"} ↗</a></figcaption>${floorPlanSvg(fp)}</figure>`).join("")}</div>`;
}
function drawPageMap(b) {
  const pm = L.map("pageMap", { zoomControl: true, attributionControl: true, scrollWheelZoom: false }).setView([b.lat, b.lon], 16);
  pm.attributionControl.setPrefix(false).addAttribution("© OpenStreetMap contributors");
  const BM = window.BASEMAP, R = L.canvas();
  BM.sea.forEach(p => L.polygon(p, { renderer: R, stroke: false, fillColor: css("--water"), fillOpacity: 1 }).addTo(pm));
  BM.land.forEach(p => L.polygon(p, { renderer: R, stroke: false, fillColor: css("--land"), fillOpacity: 1 }).addTo(pm));
  BM.water.forEach(p => L.polygon(p, { renderer: R, stroke: false, fillColor: css("--water"), fillOpacity: 1 }).addTo(pm));
  BM.park.forEach(p => L.polygon(p, { renderer: R, stroke: false, fillColor: css("--park"), fillOpacity: 1 }).addTo(pm));
  BM.building.forEach(p => L.polygon(p, { renderer: R, stroke: false, fillColor: css("--bldg"), fillOpacity: 1 }).addTo(pm));
  BM.road.forEach(([c, , pts]) => L.polyline(pts, { renderer: R, color: c <= 2 ? css("--road-major") : css("--road"), weight: c <= 2 ? 4 : 2 }).addTo(pm));
  BM.rail.forEach(([k, pts]) => L.polyline(pts, { renderer: R, color: k === "mover" ? css("--mover") : css("--rail"), weight: 2 }).addTo(pm));
  L.circleMarker([b.lat, b.lon], { radius: 9, color: "#fff", weight: 2, fillColor: css("--accent"), fillOpacity: 1, pane: "tooltipPane", interactive: false }).addTo(pm);
  L.marker([D.office.lat, D.office.lon], { icon: L.divIcon({ className: "marker", html: `<svg width="22" height="22" viewBox="0 0 26 26"><path d="M13 1.5l3.4 7.2 7.9.9-5.9 5.4 1.7 7.8L13 18.9 5.9 22.8l1.7-7.8L1.7 9.6l7.9-.9z" fill="#d1495b" stroke="#fff" stroke-width="1.5"/></svg>`, iconSize: [22, 22], iconAnchor: [11, 11] }) }).addTo(pm);
  drawNeighborhood(pm, b);
}
function drawPage(id) {
  const b = byId[id], el = document.getElementById("pageView"); if (!b) { location.hash = ""; return; }
  const m = M[b.id], ph = photoSrc(b), rs = b.review_summary;
  const tags = rs ? splitTags(rs["tags_" + lang] || rs.tags_en) : autoTags(b);
  const pros = rs ? splitTags(rs["pros_" + lang] || rs.pros_en) : [], cons = rs ? splitTags(rs["cons_" + lang] || rs.cons_en) : [];
  const rentRows = Object.entries(b.rents).map(([u, r]) => `<tr><td>${t(u)} ${r.n < 3 ? `<span class="chip est">${t("lowN")}</span>` : ""}${r.basis.includes("floorplan_from") ? ` <span class="chip">${t("fromPlans")}</span>` : ""}${r.includes_furnished ? ` <span class="chip">${t("inclFurn")}</span>` : ""}</td><td class="r num">${money(r.min)}</td><td class="r num">${money(r.median)}</td><td class="r num">${money(r.max)}</td><td class="r num">${r.sqft ? Math.round(r.sqft) + " ft²" : "–"}</td><td class="r num">${r.n}</td><td class="r num">${b.all_in[u] ? money(b.all_in[u].total.value) : "–"}</td></tr>`).join("");
  el.innerHTML = `<div class="page-hero">${ph ? `<img src="${ph}" alt="">` : ""}<div class="veil"></div><div class="inner">
      <a class="btn ghost" href="#list" style="color:#fff;border-color:rgba(255,255,255,.6)">← ${t("back")}</a>
      <h2>${esc(b.name)}</h2><div class="chips">${tags.map(x => `<span class="chip">${esc(x)}</span>`).join("")}</div></div></div>
    <div class="page-body">
      ${pros.length || cons.length ? `${pros.length ? `<div class="chips">${pros.map(x => `<span class="chip pro">＋ ${esc(x)}</span>`).join("")}</div>` : ""}${cons.length ? `<div class="chips">${cons.map(x => `<span class="chip con">− ${esc(x)}</span>`).join("")}</div>` : ""}` : ""}
      <div class="facts" style="grid-template-columns:repeat(auto-fit,minmax(130px,1fr))">
        <div class="fact"><b>${m.score != null ? Math.round(m.score) : "–"}</b><small>${t("score")} / 100</small></div>
        <div class="fact"><b>${b.walk_min != null ? Math.round(b.walk_min) + " " + t("min") : "–"}</b><small>${t("walk")} ${t("walkTo")}</small></div>
        <div class="fact"><b>${money(m.rentMid)}</b><small>1B ${t("mid")}</small></div>
        <div class="fact"><b>${money(m.allin)}</b><small>1B ${t("allin")}</small></div>
        <div class="fact"><b>${m.rating != null ? m.rating.toFixed(2) : "–"}</b><small>${t("rating")}</small></div>
        <div class="fact"><b>${b.year_built ?? "–"}</b><small>${t("year")}</small></div>
      </div>
      <div class="grid2">
        <div class="panel"><h3>${t("about")}</h3><p style="margin:0">${esc(b["summary_" + lang] || b.summary_en || "")}</p>
          <dl class="kv"><dt>${t("address")}</dt><dd>${esc(b.address)}</dd><dt>${t("channel")}</dt><dd>${chName(b.channel_primary)} <span class="muted">· ${esc(t("ch" + b.channel_primary + "long"))}</span></dd>
          <dt>${t("floors")} / ${t("units")}</dt><dd class="num">${b.floors ?? "–"} / ${b.units ?? "–"}</dd><dt>${t("developer")}</dt><dd>${esc(b.developer || "–")}</dd>
          <dt>${t("architect")}</dt><dd>${esc(b.architect || "–")}</dd><dt>${t("manager")}</dt><dd>${esc(b.manager || "–")}</dd>
          ${b.official_url ? `<dt>${t("site")}</dt><dd><a href="${esc(b.official_url)}" target="_blank" rel="noopener">${esc(b.official_url.replace(/^https?:\/\//, ""))}</a></dd>` : ""}</dl></div>
        <div class="panel"><h3>${t("costTitle")}</h3>${costHtml(b)}${incomeHtml(b)}</div>
      </div>
      ${goPanel(b)}${amenityPanel(b)}<div class="panel"><h3>${t("rent")}</h3><div style="overflow-x:auto"><table class="mini"><thead><tr><th>${t("type")}</th><th class="r">${t("low")}</th><th class="r">${t("mid")}</th><th class="r">${t("high")}</th><th class="r">ft²</th><th class="r">${t("n")}</th><th class="r">${t("allin")}</th></tr></thead><tbody>${rentRows || `<tr><td colspan="7" class="muted">${t("noData")}</td></tr>`}</tbody></table></div>${rentSources(b)}${concessionHtml(b)}</div>
      <div class="panel nb-panel"><h3>${t("nearby")}</h3>${nearbyHtml(b)}</div>
      <div class="grid2">
        <div class="panel"><h3>${t("rules")}</h3>${rulesHtml(b)}</div>
        <div class="panel"><h3>${t("ratings")}</h3><table class="mini"><tbody>${b.ratings.map(r => `<tr><td>${esc(r.group === "overall" ? t("aptsOverall") : r.platform)}${r.group === "overall" ? ` <span class="chip est" title="${esc(t("aptsOverallNote"))}">${lang === "zh" ? "含建筑评级" : "includes building rating"}</span>` : ""}${r.group === "short_stay" ? ` <span class="chip est">${lang === "zh" ? "短住" : "short stay"}</span>` : ""}</td><td class="r"><span class="stars">${stars(r.score)}</span> <span class="num">${r.score.toFixed(1)}</span></td><td class="r num muted">${r.count}</td><td class="muted">${esc(r.via || "")}</td></tr>`).join("") || `<tr><td class="muted">${t("noData")}</td></tr>`}</tbody></table>${aptsNote(b)}</div>
      </div>
      <div class="panel"><h3>${lang === "zh" ? "户型图" : "Floor plans"}</h3>${floorPlansHtml(b)}</div>
      <div class="panel"><h3>${t("reviewTitle")}</h3>${reviewsHtml(b)}</div>
      ${b.notes || b.conflicts ? `<div class="panel"><h3>${t("notes")}</h3><p class="muted" style="margin:0;overflow-wrap:anywhere">${esc([b.conflicts, b.notes].filter(Boolean).join(" "))}</p></div>` : ""}
      <div class="panel"><h3>${t("sources")}</h3><ul style="margin:0;padding-left:18px;overflow-wrap:anywhere">${(b.facts_source_urls || "").split(";").filter(Boolean).map(u => `<li><a href="${esc(u)}" target="_blank" rel="noopener">${esc(u)}</a></li>`).join("")}</ul></div>
    </div>`;
  bindReviews(b); bindGallery(); if (b.lat != null) drawPageMap(b); window.scrollTo(0, 0);
}

/* ---------- routing and chrome ---------- */
function applyLang() {
  document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
  document.querySelectorAll("[data-i18n]").forEach(el => el.textContent = t(el.dataset.i18n) + (el.dataset.i18n === "subtitle" ? D.generated_on : ""));
  document.querySelectorAll("[data-i18n-ph]").forEach(el => el.placeholder = t(el.dataset.i18nPh));
  document.getElementById("lEn").setAttribute("aria-pressed", lang === "en"); document.getElementById("lZh").setAttribute("aria-pressed", lang === "zh");
  document.title = t("title");
}
function route() {
  const h = location.hash.slice(1), page = h.startsWith("b-") ? h.slice(2) : null, view = page ? "page" : h === "list" ? "list" : "map";
  document.getElementById("mapView").hidden = view !== "map"; document.getElementById("listView").hidden = view !== "list"; document.getElementById("pageView").hidden = view !== "page";
  document.getElementById("vMap").setAttribute("aria-pressed", view === "map"); document.getElementById("vList").setAttribute("aria-pressed", view === "list");
  if (view === "map") { if (!map) initMap(); else setTimeout(() => map.invalidateSize(), 0); }
  drawFilters();
  if (view === "list") { drawWeights(); drawList(); }
  if (view === "page") drawPage(page);
}
function redrawAll() { applyLang(); if (map) { drawMarkers(); drawLegend(); } route(); }
document.getElementById("vMap").onclick = () => location.hash = "";
document.getElementById("vList").onclick = () => location.hash = "list";
document.getElementById("lEn").onclick = () => { lang = "en"; store.set("lang", lang); redrawAll(); };
document.getElementById("lZh").onclick = () => { lang = "zh"; store.set("lang", lang); redrawAll(); };
document.getElementById("colorBy").onchange = e => { colorBy = e.target.value; if (map) { drawMarkers(); drawLegend(); } if (!document.getElementById("listView").hidden) drawList(); };
document.getElementById("q").oninput = () => drawList();
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { if (map) { drawBasemap(); drawMarkers(); drawLegend(); } });
window.addEventListener("hashchange", route);
const bar = document.querySelector(".bar");
const setBar = () => { document.documentElement.style.setProperty("--bar-h", bar.offsetHeight + "px"); if (map) map.invalidateSize(); };
new ResizeObserver(setBar).observe(bar); setBar();
const narrow = matchMedia("(max-width: 720px)").matches;
document.getElementById("legendBox").open = !narrow; bindWeights(); bindFilters();
applyLang(); route();
})();
