#!/usr/bin/env python3
"""Build the Formula Book viewer, a self-contained HTML page, from db/.

Usage:
    python3 tools/build_viewer.py                    # writes db/viewer.html
    python3 tools/build_viewer.py --body-only PATH   # also writes the page body only,
                                                     # for publishing as a claude.ai artifact

db/viewer.html opens in any browser with no server. It reads nothing at run
time: rerun this script (after tools/costing.py) whenever the data changes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from costing import CHANNELS, DB, ROOT, Book, DBError  # noqa: E402

OUT = DB / "viewer.html"
UNIT_LABELS = {"fl_oz": "fl oz", "l": "L"}


def pack_label(size: float, unit: str) -> str:
    return f"{size:g} {UNIT_LABELS.get(unit, unit)}"


def item_name(book: Book, item: str) -> str:
    if item in book.ingredients:
        return book.ingredients[item]["name"]
    return book.formulas[item]["name"]


def per_channel(fn) -> dict:
    return {ch: fn(ch) for ch in CHANNELS}


def build_data(book: Book) -> dict:
    used_in: dict[str, list[str]] = {}
    for doc in list(book.formulas.values()) + list(book.products.values()):
        for line in doc.get("ingredients") or doc.get("build") or []:
            used_in.setdefault(line["item"], [])
            if doc["name"] not in used_in[line["item"]]:
                used_in[line["item"]].append(doc["name"])

    products = []
    for pid, doc in book.products.items():
        parts = per_channel(lambda ch, pid=pid: book.product_cost_parts(pid, ch))
        build = []
        for line in doc["build"]:
            build.append(
                {
                    "name": item_name(book, line["item"]),
                    "kind": "formula" if line["item"] in book.formulas else "ingredient",
                    "qty": line["qty"],
                    "unit": line["unit"],
                    "note": line.get("note", ""),
                    "packaging": book.is_packaging(line["item"]),
                    "cost": per_channel(lambda ch, line=line: book.line_cost(line, ch)),
                }
            )
        products.append(
            {
                "id": pid,
                "name": doc["name"],
                "category": doc.get("category", ""),
                "status": doc["status"],
                "version": str(doc.get("version", "")),
                "approvedOn": str(doc["approved_on"]) if doc.get("approved_on") else None,
                "description": doc.get("description", ""),
                "price": doc["pricing"].get("suggested_retail_usd"),
                "food": {ch: None if p is None else p[0] for ch, p in parts.items()},
                "packagingCost": {ch: None if p is None else p[1] for ch, p in parts.items()},
                "hasPackaging": book.has_packaging(pid),
                "wastePct": doc.get("waste_pct", 0),
                "batchUnits": doc.get("batch_units"),
                "allergens": sorted(book.allergens(pid)),
                "build": build,
                "targets": doc.get("targets") or {},
                "production": doc.get("production") or {},
                "qa": doc.get("qa") or [],
                "validation": doc.get("validation") or {},
                "history": [
                    {**h, "date": str(h.get("date", ""))} for h in doc.get("history") or []
                ],
            }
        )

    formulas = []
    for fid, doc in book.formulas.items():
        dough = doc["kind"] == "dough"
        flour = sum(
            float(line["qty"])
            for line in doc["ingredients"]
            if line["unit"] == "g"
            and line["item"] in book.ingredients
            and book.ingredients[line["item"]]["category"] == "flour"
        )
        lines = []
        for line in doc["ingredients"]:
            bakers = None
            if dough and flour and line["unit"] == "g":
                bakers = round(100 * float(line["qty"]) / flour, 1)
            lines.append(
                {
                    "stage": line.get("stage", ""),
                    "name": item_name(book, line["item"]),
                    "kind": "formula" if line["item"] in book.formulas else "ingredient",
                    "qty": line["qty"],
                    "unit": line["unit"],
                    "note": line.get("note", ""),
                    "bakers": bakers,
                    "cost": per_channel(lambda ch, line=line: book.line_cost(line, ch)),
                }
            )
        yld = doc["yield"]
        batch = per_channel(lambda ch, fid=fid: book.formula_cost(fid, ch))
        formulas.append(
            {
                "id": fid,
                "name": doc["name"],
                "kind": doc["kind"],
                "status": doc["status"],
                "version": str(doc.get("version", "")),
                "yield": {
                    "grams": yld["grams"],
                    "units": yld.get("units"),
                    "description": yld.get("description", ""),
                },
                "inputGrams": sum(book.line_grams(line) or 0 for line in doc["ingredients"]),
                "batch": batch,
                "perKg": {ch: None if c is None else 1000 * c / yld["grams"] for ch, c in batch.items()},
                "perUnit": {
                    ch: None if c is None or not yld.get("units") else c / yld["units"]
                    for ch, c in batch.items()
                },
                "lines": lines,
                "method": doc.get("method") or [],
                "specs": doc.get("specs") or {},
                "notes": doc.get("notes") or [],
                "usedBy": [book.products[p]["name"] if p in book.products else item_name(book, p)
                           for p in doc.get("used_by") or []
                           if p in book.products or p in book.formulas],
                "history": [
                    {**h, "date": str(h.get("date", ""))} for h in doc.get("history") or []
                ],
            }
        )

    ingredients = []
    for iid, ing in book.ingredients.items():
        prices = {}
        for ch in CHANNELS:
            per_g, per_each = book.unit_costs(iid, ch)
            source_id = ing["price_ref"] or iid
            row = book.prices.get((source_id, ch))
            prices[ch] = {
                "perKg": None if per_g is None else per_g * 1000,
                "perEach": per_each,
                "pack": pack_label(row["pack_size"], row["pack_unit"]) if row else None,
                "price": row["price_usd"] if row else None,
                "asOf": row["as_of"] if row else None,
                "source": row["source"] if row else None,
                "priceRef": item_name(book, ing["price_ref"]) if ing["price_ref"] else None,
            }
        ingredients.append(
            {
                "id": iid,
                "name": ing["name"],
                "category": ing["category"],
                "allergens": sorted(ing["allergens"]),
                "spec": ing.get("spec", ""),
                "notes": ing.get("notes", ""),
                "eachG": ing["each_g"],
                "prices": prices,
                "usedIn": used_in.get(iid, []),
            }
        )

    return {
        "asOf": max(row["as_of"] for row in book.prices.values()),
        "channels": CHANNELS,
        "products": products,
        "formulas": formulas,
        "ingredients": ingredients,
    }


PAGE = r"""<title>BostonBakery Formula Book</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500&family=Source+Sans+3:wght@400;600&display=swap">
<style>
/* Layout: sticky header with view tabs and a cost-basis switch; products as cards grouped by
   category; formulas and ingredients as expandable spec sheets. */
:root {
  --bg: #f2f4f6;
  --surface: #ffffff;
  --surface-2: #e9edf1;
  --ink: #17202a;
  --ink-2: #4f5e6d;
  --rule: #d3dae2;
  --accent: #1c5b76;
  --accent-ink: #ffffff;
  --pastry: #924e1d;
  --sandwich: #a1352a;
  --drink: #477233;
  --ok: #22704a;
  --ok-bg: #dff1e6;
  --warn: #8c5800;
  --warn-bg: #faeed6;
  --cost: #4f5e6d;
  --pack: #9ba8b5;
  --font-display: "Barlow Semi Condensed", "Arial Narrow", "Helvetica Neue", Arial, sans-serif;
  --font-body: "Source Sans 3", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #10161c; --surface: #172029; --surface-2: #1e2933; --ink: #e4e9ee; --ink-2: #9eacb9;
    --rule: #2b3744; --accent: #6cafce; --accent-ink: #0c1820; --pastry: #e29b63;
    --sandwich: #ef7d68; --drink: #9dca83; --ok: #74d39c; --ok-bg: #163324; --warn: #f0b955;
    --warn-bg: #3a2b0f; --cost: #9eacb9; --pack: #5b6a79; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #10161c; --surface: #172029; --surface-2: #1e2933; --ink: #e4e9ee; --ink-2: #9eacb9;
  --rule: #2b3744; --accent: #6cafce; --accent-ink: #0c1820; --pastry: #e29b63;
  --sandwich: #ef7d68; --drink: #9dca83; --ok: #74d39c; --ok-bg: #163324; --warn: #f0b955;
  --warn-bg: #3a2b0f; --cost: #9eacb9; --pack: #5b6a79; color-scheme: dark;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 15px/1.5 var(--font-body); }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--bg); }
.wrap { max-width: 1180px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.num, .money, td.n, th.n { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }
h1, h2, h3 { font-family: var(--font-display); text-wrap: balance; margin: 0; line-height: 1.15; }
a { color: var(--accent); }
button { font: inherit; color: inherit; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

header.top { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--bg); border-bottom: 1px solid var(--rule); }
.top-row { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px 20px; padding-block: 14px 10px; }
.brand { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.eyebrow { font: 600 12px/1 var(--font-display); letter-spacing: .12em; text-transform: uppercase; color: var(--ink-2); }
.brand h1 { font-size: 28px; font-weight: 700; letter-spacing: .01em; }
.controls { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
.search { width: 220px; max-width: 100%; padding: 7px 10px; border: 1px solid var(--rule); border-radius: 6px; background: var(--surface); color: var(--ink); font: inherit; }
.seg { display: inline-flex; border: 1px solid var(--rule); border-radius: 6px; overflow: hidden; background: var(--surface); }
.seg button { border: 0; background: transparent; padding: 6px 12px; cursor: pointer; font-size: 14px; color: var(--ink-2); }
.seg button[aria-pressed="true"] { background: var(--accent); color: var(--accent-ink); }
.seg-label { font-size: 13px; color: var(--ink-2); }
nav.tabs { display: flex; gap: 4px; overflow-x: auto; }
nav.tabs button { border: 0; background: transparent; padding: 8px 12px 10px; cursor: pointer; font: 600 16px/1 var(--font-display); letter-spacing: .02em; color: var(--ink-2); border-bottom: 3px solid transparent; white-space: nowrap; }
nav.tabs button[aria-selected="true"] { color: var(--ink); border-bottom-color: var(--accent); }
nav.tabs .count { font: 500 12px var(--font-mono); color: var(--ink-2); margin-left: 4px; }

main { padding-block: 18px 40px; display: flex; flex-direction: column; gap: 22px; }
.summary { display: flex; flex-wrap: wrap; gap: 8px 18px; align-items: baseline; color: var(--ink-2); font-size: 14px; }
.summary strong { color: var(--ink); font-weight: 600; }
.group { display: flex; flex-direction: column; gap: 12px; }
.group-head { display: flex; align-items: baseline; gap: 10px; border-bottom: 1px solid var(--rule); padding-bottom: 6px; }
.group-head h2 { font-size: 20px; }
.group-head .count { font: 500 13px var(--font-mono); color: var(--ink-2); }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 330px), 1fr)); gap: 14px; align-items: start; }

.card { background: var(--surface); border: 1px solid var(--rule); border-radius: 8px; padding: 14px 16px; display: flex; flex-direction: column; gap: 10px; min-width: 0; }
.card.open { grid-column: 1 / -1; }
.card-top { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.card-name { font-size: 22px; font-weight: 700; }
.card-desc { margin: 0; color: var(--ink-2); font-size: 14px; max-width: 65ch; }
.chip { display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; border-radius: 999px; font-size: 12px; font-weight: 600; letter-spacing: .03em; border: 1px solid var(--rule); color: var(--ink-2); background: var(--surface); text-transform: lowercase; }
.cat-pastry { color: var(--pastry); border-color: currentColor; }
.cat-sandwich { color: var(--sandwich); border-color: currentColor; }
.cat-drink { color: var(--drink); border-color: currentColor; }
.pill { padding: 2px 8px; border-radius: 4px; font: 600 12px/1.4 var(--font-display); letter-spacing: .06em; text-transform: uppercase; }
.pill.approved { background: var(--ok-bg); color: var(--ok); }
.pill.pending_test, .pill.draft { background: var(--warn-bg); color: var(--warn); }
.pill.retired { background: var(--surface-2); color: var(--ink-2); }
.allergen { text-transform: none; }

.price-row { display: flex; flex-wrap: wrap; gap: 8px 22px; align-items: flex-end; }
.price { font: 500 30px/1 var(--font-mono); font-variant-numeric: tabular-nums; }
.kv { display: flex; flex-wrap: wrap; gap: 4px 18px; margin: 0; }
.kv div { display: flex; flex-direction: column; }
.kv dt { font-size: 12px; color: var(--ink-2); letter-spacing: .03em; }
.kv dd { margin: 0; font: 500 15px var(--font-mono); font-variant-numeric: tabular-nums; }

.bar { display: flex; height: 10px; border-radius: 5px; background: var(--ok-bg); overflow: hidden; }
.bar span { display: block; height: 100%; }
.bar .s-cost { background: var(--cost); }
.bar .s-pack { background: var(--pack); }
.legend { display: flex; flex-wrap: wrap; gap: 4px 14px; font-size: 12px; color: var(--ink-2); }
.legend i { display: inline-block; width: 9px; height: 9px; border-radius: 2px; margin-right: 5px; vertical-align: -1px; }
.legend .k-cost { background: var(--cost); } .legend .k-pack { background: var(--pack); } .legend .k-margin { background: var(--ok-bg); border: 1px solid var(--ok); }
.chips { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.muted { color: var(--ink-2); }
.small { font-size: 13px; }

.toggle { align-self: flex-start; border: 1px solid var(--rule); background: var(--surface-2); border-radius: 6px; padding: 6px 12px; cursor: pointer; font-weight: 600; font-size: 14px; }
.toggle:hover { border-color: var(--accent); }
.details { display: flex; flex-direction: column; gap: 16px; border-top: 1px solid var(--rule); padding-top: 14px; }
.details h4 { margin: 0 0 6px; font: 700 13px var(--font-display); letter-spacing: .1em; text-transform: uppercase; color: var(--ink-2); }
.cols { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap: 16px 24px; }
.cols > * { min-width: 0; }
ol, ul { margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 4px; max-width: 75ch; }
.pending li::marker { color: var(--warn); }
.tested li::marker { color: var(--ok); }
dl.specs { margin: 0; display: grid; grid-template-columns: minmax(120px, max-content) 1fr; gap: 4px 14px; }
dl.specs dt { color: var(--ink-2); }
dl.specs dd { margin: 0; }

.tbl-wrap { overflow-x: auto; border: 1px solid var(--rule); border-radius: 6px; background: var(--surface); }
table { border-collapse: collapse; width: 100%; font-size: 14px; }
th, td { text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--rule); vertical-align: top; }
th { background: var(--surface-2); font: 700 12px var(--font-display); letter-spacing: .08em; text-transform: uppercase; color: var(--ink-2); white-space: nowrap; }
td.n, th.n { text-align: right; white-space: nowrap; }
tr:last-child td { border-bottom: 0; }
tr.total td { font-weight: 600; background: var(--surface-2); }
.sel { font-weight: 600; }
.dim { color: var(--ink-2); }
.note { display: block; font-size: 12px; color: var(--ink-2); }
.stage td { background: var(--bg); font: 700 12px var(--font-display); letter-spacing: .08em; text-transform: uppercase; color: var(--ink-2); }
tr.click { cursor: pointer; }
tr.click:hover td { background: var(--surface-2); }
tr.detail td { background: var(--bg); }

.filters { display: flex; flex-wrap: wrap; gap: 6px; }
.filters button { border: 1px solid var(--rule); background: var(--surface); border-radius: 999px; padding: 4px 10px; cursor: pointer; font-size: 13px; color: var(--ink-2); }
.filters button[aria-pressed="true"] { border-color: var(--accent); color: var(--accent); font-weight: 600; }
@media (max-width: 560px) { .hide-sm { display: none; } }
.empty { padding: 24px; text-align: center; color: var(--ink-2); border: 1px dashed var(--rule); border-radius: 8px; }
footer { padding-block: 0 32px; color: var(--ink-2); font-size: 13px; }
@media (max-width: 560px) {
  .brand h1 { font-size: 24px; }
  .search { width: 100%; }
  .controls { width: 100%; }
  .price { font-size: 26px; }
}
@media (prefers-reduced-motion: no-preference) {
  .toggle, .seg button, nav.tabs button { transition: background-color .15s, color .15s, border-color .15s; }
}
</style>

<header class="top">
  <div class="wrap">
    <div class="top-row">
      <div class="brand">
        <span class="eyebrow">BostonBakery</span>
        <h1>Formula Book</h1>
      </div>
      <div class="controls">
        <input id="search" class="search" type="search" placeholder="Search by name" aria-label="Search by name">
        <span class="seg-label" id="basis-label">Costs at</span>
        <div class="seg" role="group" aria-labelledby="basis-label" id="basis"></div>
      </div>
    </div>
    <nav class="tabs" role="tablist" id="tabs"></nav>
  </div>
</header>

<main class="wrap" id="view" aria-live="polite"></main>
<footer class="wrap" id="foot"></footer>

<script type="application/json" id="book-data">__DATA__</script>
<script>
(function () {
  const DATA = JSON.parse(document.getElementById("book-data").textContent);
  const CH = Object.keys(DATA.channels);
  const VIEWS = [
    { id: "products", label: "Products", count: DATA.products.length },
    { id: "formulas", label: "Formulas", count: DATA.formulas.length },
    { id: "ingredients", label: "Ingredients", count: DATA.ingredients.length }
  ];
  const CATS = [["pastry", "Pastry"], ["sandwich", "Sandwiches"], ["drink", "Drinks"]];
  const STATUS = { approved: "Approved", pending_test: "Pending test", draft: "Draft", retired: "Retired" };
  const state = { view: "products", channel: "distributor_est", query: "", open: new Set(), cat: "all" };
  try { const saved = localStorage.getItem("fb-channel"); if (saved && CH.includes(saved)) state.channel = saved; } catch (e) {}

  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const money = (v) => v == null ? "n/a" : (v > 0 && v < 0.005 ? "<$0.01" : "$" + v.toFixed(2));
  const num = (q) => Number(q).toLocaleString("en-US", { maximumFractionDigits: 1 });
  const qty = (q, unit) => unit === "each" ? num(q) + " each" : num(q) + " g";
  const pct = (a, b) => (a == null || !b) ? "n/a" : Math.round((100 * a) / b) + "%";
  const UNITS = { g: "g", f: "°F", s: "s", usd: "$", pct: "%", days: "days", minutes: "min" };
  const human = (k) => {
    const parts = String(k).split("_");
    const unit = parts.length > 1 && UNITS[parts[parts.length - 1]] ? UNITS[parts.pop()] : null;
    const text = parts.join(" ").replace(/^bakers /, "baker's ").replace(/^\w/, (c) => c.toUpperCase());
    return unit ? `${text} (${unit})` : text;
  };
  const chLabel = (ch) => ch === "distributor_est" ? "Distributor" : "Retail";
  const other = () => CH.find((c) => c !== state.channel);
  const matches = (name) => !state.query || name.toLowerCase().includes(state.query.toLowerCase());
  const pill = (s) => `<span class="pill ${esc(s)}">${esc(STATUS[s] || s)}</span>`;
  const list = (items, cls) => items && items.length ? `<ul class="${cls || ""}">${items.map((i) => `<li>${esc(i)}</li>`).join("")}</ul>` : "";

  function renderControls() {
    document.getElementById("basis").innerHTML = CH.map((ch) =>
      `<button type="button" data-channel="${ch}" aria-pressed="${ch === state.channel}">${chLabel(ch)}</button>`).join("");
    document.getElementById("tabs").innerHTML = VIEWS.map((v) =>
      `<button type="button" role="tab" data-view="${v.id}" aria-selected="${v.id === state.view}">${v.label}<span class="count">${v.count}</span></button>`).join("");
  }

  function costCells(cost) {
    return CH.map((ch) => `<td class="n ${ch === state.channel ? "sel" : "dim"}">${money(cost[ch])}</td>`).join("");
  }
  const costHeads = () => CH.map((ch) => `<th class="n">${chLabel(ch)}</th>`).join("");

  function productCard(p) {
    const ch = state.channel;
    const food = p.food[ch], pack = p.hasPackaging ? p.packagingCost[ch] : 0;
    const total = food == null ? null : food + (pack || 0);
    const margin = total == null || p.price == null ? null : p.price - total;
    const fw = p.price ? Math.min(100, (100 * (food || 0)) / p.price) : 0;
    const pw = p.price ? Math.min(100 - fw, (100 * (pack || 0)) / p.price) : 0;
    const key = "p:" + p.id, open = state.open.has(key);
    const allergens = p.allergens.length ? p.allergens.map((a) => `<span class="chip allergen">${esc(a)}</span>`).join("") : `<span class="muted small">No major allergens</span>`;
    return `<article class="card${open ? " open" : ""}">
      <div class="card-top"><span class="chip cat-${esc(p.category)}">${esc(p.category)}</span>${pill(p.status)}<span class="muted small">v${esc(p.version)}</span></div>
      <h3 class="card-name">${esc(p.name)}</h3>
      ${p.description ? `<p class="card-desc">${esc(p.description)}</p>` : ""}
      <div class="price-row">
        <div class="price" aria-label="Suggested price">${money(p.price)}</div>
        <dl class="kv">
          <div><dt>Unit cost</dt><dd>${money(total)}</dd></div>
          <div><dt>Margin</dt><dd>${money(margin)}</dd></div>
          <div><dt>Cost of price</dt><dd>${pct(total, p.price)}</dd></div>
        </dl>
      </div>
      <div class="bar" role="img" aria-label="Food ${pct(food, p.price)}, packaging ${p.hasPackaging ? pct(pack, p.price) : "not costed"}, margin ${pct(margin, p.price)} of the price"><span class="s-cost" style="width:${fw}%"></span><span class="s-pack" style="width:${pw}%"></span></div>
      <div class="legend"><span><i class="k-cost"></i>Food ${pct(food, p.price)}</span><span><i class="k-pack"></i>Packaging ${p.hasPackaging ? pct(pack, p.price) : "not costed yet"}</span><span><i class="k-margin"></i>Margin ${pct(margin, p.price)}</span></div>
      <div class="chips">${allergens}</div>
      <button type="button" class="toggle" data-toggle="${key}" aria-expanded="${open}">${open ? "Hide build and method" : "Show build and method"}</button>
      ${open ? productDetails(p) : ""}
    </article>`;
  }

  function productDetails(p) {
    const rows = p.build.map((b) => `<tr><td>${esc(b.name)}${b.kind === "formula" ? ` <span class="muted small">(formula)</span>` : ""}${b.note ? `<span class="note">${esc(b.note)}</span>` : ""}</td><td class="n">${qty(b.qty, b.unit)}</td>${costCells(b.cost)}</tr>`).join("");
    const waste = {};
    const foodOnly = {};
    CH.forEach((ch) => {
      foodOnly[ch] = p.build.filter((b) => !b.packaging).reduce((s, b) => s + (b.cost[ch] || 0), 0);
      waste[ch] = foodOnly[ch] * p.wastePct / 100;
    });
    const totals = {};
    CH.forEach((ch) => { totals[ch] = p.food[ch] == null ? null : p.food[ch] + (p.packagingCost[ch] || 0); });
    const prod = Object.entries(p.production || {}).map(([k, v]) => {
      if (Array.isArray(v)) return `<div><h4>${esc(human(k))}</h4>${list(v)}</div>`;
      if (v && typeof v === "object") return `<div><h4>${esc(human(k))}</h4>${list(Object.values(v).flat())}</div>`;
      return `<div><h4>${esc(human(k))}</h4><p style="margin:0;max-width:75ch">${esc(v)}</p></div>`;
    }).join("");
    const targets = Object.keys(p.targets || {}).length ? `<div><h4>Targets</h4><dl class="specs">${Object.entries(p.targets).map(([k, v]) => `<dt>${esc(human(k))}</dt><dd class="num">${esc(v)}</dd>`).join("")}</dl></div>` : "";
    const val = p.validation || {};
    const history = (p.history || []).map((h) => `${h.date} · v${h.version || ""}: ${h.change}`);
    return `<div class="details">
      <div><h4>Build per unit</h4>
        <div class="tbl-wrap"><table><thead><tr><th>Item</th><th class="n">Qty</th>${costHeads()}</tr></thead><tbody>
          ${rows}
          <tr><td>Waste allowance, food only</td><td class="n">${p.wastePct}%</td>${costCells(waste)}</tr>
          <tr class="total"><td>Unit cost</td><td></td>${costCells(totals)}</tr>
        </tbody></table></div>
        ${p.hasPackaging ? "" : `<p class="muted small" style="margin:6px 0 0">Packaging isn't in this build yet; the pricing memo assumes $0.25 an item.</p>`}
      </div>
      <div class="cols">${prod}${targets}${p.qa.length ? `<div><h4>QA checks</h4>${list(p.qa)}</div>` : ""}</div>
      <div class="cols">
        ${val.tested && val.tested.length ? `<div><h4>Tested</h4>${list(val.tested, "tested")}</div>` : ""}
        ${val.pending && val.pending.length ? `<div><h4>Still to test</h4>${list(val.pending, "pending")}</div>` : ""}
        ${history.length ? `<div><h4>History</h4>${list(history)}</div>` : ""}
      </div>
    </div>`;
  }

  function renderProducts() {
    const items = DATA.products.filter((p) => matches(p.name));
    const counts = {};
    DATA.products.forEach((p) => { counts[p.status] = (counts[p.status] || 0) + 1; });
    let html = `<div class="summary"><span><strong>${counts.approved || 0}</strong> approved</span><span><strong>${counts.pending_test || 0}</strong> pending test</span><span>Costs at <strong>${chLabel(state.channel).toLowerCase()}</strong> prices, as of ${esc(DATA.asOf)}. All prices are estimates until real quotes replace them.</span></div>`;
    CATS.forEach(([cat, label]) => {
      const group = items.filter((p) => p.category === cat);
      if (!group.length) return;
      html += `<section class="group"><div class="group-head"><h2>${label}</h2><span class="count">${group.length}</span></div><div class="grid">${group.map(productCard).join("")}</div></section>`;
    });
    return items.length ? html : html + `<div class="empty">No products match “${esc(state.query)}”.</div>`;
  }

  function formulaCard(f) {
    const ch = state.channel, key = "f:" + f.id, open = state.open.has(key);
    const dough = f.lines.some((l) => l.bakers != null);
    let lastStage = null;
    const rows = f.lines.map((l) => {
      let stageRow = "";
      if (l.stage && l.stage !== lastStage) { stageRow = `<tr class="stage"><td colspan="${dough ? 5 : 4}">${esc(l.stage)}</td></tr>`; lastStage = l.stage; }
      return stageRow + `<tr><td>${esc(l.name)}${l.kind === "formula" ? ` <span class="muted small">(formula)</span>` : ""}${l.note ? `<span class="note">${esc(l.note)}</span>` : ""}</td><td class="n">${qty(l.qty, l.unit)}</td>${dough ? `<td class="n">${l.bakers == null ? "" : l.bakers.toFixed(1) + "%"}</td>` : ""}${costCells(l.cost)}</tr>`;
    }).join("");
    const specs = Object.entries(f.specs || {});
    const history = (f.history || []).map((h) => `${h.date}: ${h.change}`);
    return `<article class="card${open ? " open" : ""}">
      <div class="card-top"><span class="chip">${esc(f.kind)}</span>${pill(f.status)}<span class="muted small">v${esc(f.version)}</span></div>
      <h3 class="card-name">${esc(f.name)}</h3>
      <p class="card-desc">Yield ${num(f.yield.grams)} g${f.yield.units ? ` · ${f.yield.units} unit${f.yield.units > 1 ? "s" : ""}` : ""}. ${esc(f.yield.description)}</p>
      <dl class="kv">
        <div><dt>Batch cost</dt><dd>${money(f.batch[ch])}</dd></div>
        <div><dt>Per kg</dt><dd>${money(f.perKg[ch])}</dd></div>
        ${f.yield.units ? `<div><dt>Per unit</dt><dd>${money(f.perUnit[ch])}</dd></div>` : ""}
      </dl>
      ${f.usedBy.length ? `<p class="muted small" style="margin:0">Used in ${esc(f.usedBy.join(", "))}</p>` : ""}
      <button type="button" class="toggle" data-toggle="${key}" aria-expanded="${open}">${open ? "Hide formula" : "Show formula"}</button>
      ${open ? `<div class="details">
        <div><h4>Ingredients</h4><div class="tbl-wrap"><table><thead><tr><th>Item</th><th class="n">Qty</th>${dough ? `<th class="n">Baker's %</th>` : ""}${costHeads()}</tr></thead><tbody>
          ${rows}
          <tr class="total"><td>Batch</td><td class="n">${num(f.inputGrams)} g in</td>${dough ? "<td></td>" : ""}${costCells(f.batch)}</tr>
        </tbody></table></div></div>
        <div class="cols">
          ${f.method.length ? `<div><h4>Method</h4><ol>${f.method.map((m) => `<li>${esc(m)}</li>`).join("")}</ol></div>` : ""}
          <div>
            ${specs.length ? `<h4>Specs</h4><dl class="specs">${specs.map(([k, v]) => `<dt>${esc(human(k))}</dt><dd>${esc(v)}</dd>`).join("")}</dl>` : ""}
            ${f.notes.length ? `<h4 style="margin-top:14px">Notes</h4>${list(f.notes)}` : ""}
            ${history.length ? `<h4 style="margin-top:14px">History</h4>${list(history)}` : ""}
          </div>
        </div>
      </div>` : ""}
    </article>`;
  }

  function renderFormulas() {
    const items = DATA.formulas.filter((f) => matches(f.name));
    const html = `<div class="summary"><span>Sub-recipes the products are built from. Batch costs at <strong>${chLabel(state.channel).toLowerCase()}</strong> prices.</span></div>`;
    return items.length ? html + `<div class="grid">${items.map(formulaCard).join("")}</div>` : html + `<div class="empty">No formulas match “${esc(state.query)}”.</div>`;
  }

  function renderIngredients() {
    const ch = state.channel;
    const cats = ["all", ...Array.from(new Set(DATA.ingredients.map((i) => i.category)))];
    const items = DATA.ingredients.filter((i) => (state.cat === "all" || i.category === state.cat) && (matches(i.name) || matches(i.id)));
    const filters = `<div class="filters" role="group" aria-label="Filter by category">${cats.map((c) => `<button type="button" data-cat="${esc(c)}" aria-pressed="${c === state.cat}">${esc(c)}</button>`).join("")}</div>`;
    const rows = items.map((i) => {
      const pr = i.prices[ch], key = "i:" + i.id, open = state.open.has(key);
      const detail = open ? `<tr class="detail"><td colspan="7"><div class="cols">
          <div><h4>Spec</h4><p style="margin:0">${esc(i.spec) || "—"}</p>${i.notes ? `<p class="muted small" style="margin:6px 0 0">${esc(i.notes)}</p>` : ""}${i.usedIn.length ? `<p class="small" style="margin:6px 0 0">Used in ${esc(i.usedIn.join(", "))}</p>` : ""}</div>
          ${CH.map((c) => { const q = i.prices[c]; return `<div><h4>${chLabel(c)} price</h4>${q.priceRef ? `<p style="margin:0">Costed as one ${esc(q.priceRef)}.</p>` : ""}${q.price != null ? `<p style="margin:0"><span class="num">${money(q.price)}</span> for ${esc(q.pack)}, as of ${esc(q.asOf)}</p><p class="muted small" style="margin:4px 0 0">${esc(q.source)}</p>` : `<p class="muted" style="margin:0">No price yet</p>`}</div>`; }).join("")}
        </div></td></tr>` : "";
      return `<tr class="click" data-toggle="${key}" tabindex="0" aria-expanded="${open}"><td>${esc(i.name)}<span class="note">${esc(i.id)}</span></td><td class="hide-sm">${esc(i.category)}</td><td>${i.allergens.length ? i.allergens.map((a) => `<span class="chip allergen">${esc(a)}</span>`).join(" ") : ""}</td><td class="n">${money(pr.perKg)}</td><td class="n">${pr.perEach != null ? money(pr.perEach) : ""}</td><td class="n">${pr.price != null ? `${money(pr.price)} / ${esc(pr.pack)}` : (pr.priceRef ? "1 " + esc(pr.priceRef).toLowerCase() : "n/a")}</td><td class="n hide-sm">${esc(pr.asOf || "")}</td></tr>${detail}`;
    }).join("");
    const table = `<div class="tbl-wrap"><table><thead><tr><th>Ingredient</th><th class="hide-sm">Category</th><th>Allergens</th><th class="n">Per kg</th><th class="n">Per each</th><th class="n">Pack price</th><th class="n hide-sm">As of</th></tr></thead><tbody>${rows}</tbody></table></div>`;
    return `<div class="summary"><span>Prices at <strong>${chLabel(ch).toLowerCase()}</strong> estimates. Tap a row for the spec and price source.</span></div>${filters}${items.length ? table : `<div class="empty">No ingredients match.</div>`}`;
  }

  function render() {
    renderControls();
    const view = document.getElementById("view");
    view.innerHTML = state.view === "formulas" ? renderFormulas() : state.view === "ingredients" ? renderIngredients() : renderProducts();
    document.getElementById("foot").innerHTML = `Generated from the <span class="num">db/</span> folder of the BostonBakery repo. Prices as of ${esc(DATA.asOf)}. Rebuild with <span class="num">tools/build_viewer.py</span> after changing the data.`;
  }

  function setView(v) { state.view = VIEWS.some((x) => x.id === v) ? v : "products"; render(); }
  function fromHash() { setView((location.hash || "").replace("#", "")); }

  document.addEventListener("click", (e) => {
    const t = e.target.closest("[data-toggle],[data-view],[data-channel],[data-cat]");
    if (!t) return;
    if (t.dataset.view) { if (location.hash !== "#" + t.dataset.view) location.hash = t.dataset.view; else setView(t.dataset.view); return; }
    if (t.dataset.channel) { state.channel = t.dataset.channel; try { localStorage.setItem("fb-channel", state.channel); } catch (err) {} render(); return; }
    if (t.dataset.cat) { state.cat = t.dataset.cat; render(); return; }
    const key = t.dataset.toggle;
    if (state.open.has(key)) state.open.delete(key); else state.open.add(key);
    render();
    const again = document.querySelector(`[data-toggle="${CSS.escape(key)}"]`);
    if (again) again.focus({ preventScroll: true });
  });
  document.addEventListener("keydown", (e) => {
    const row = e.target.closest && e.target.closest("tr[data-toggle]");
    if (row && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); row.click(); }
  });
  document.getElementById("search").addEventListener("input", (e) => { state.query = e.target.value.trim(); render(); });
  window.addEventListener("hashchange", fromHash);
  fromHash();
})();
</script>
"""

STANDALONE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
</head>
<body>
{body}
</body>
</html>
"""


def render_body(book: Book) -> str:
    data = json.dumps(build_data(book), ensure_ascii=False, separators=(",", ":"))
    return PAGE.replace("__DATA__", data.replace("</", "<\\/"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--body-only", type=Path, help="also write the page body to this path")
    args = parser.parse_args()
    try:
        book = Book()
        errors, _ = book.validate()
    except (DBError, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print("fix the errors above (python3 tools/costing.py --check) and rerun", file=sys.stderr)
        return 1
    body = render_body(book)
    OUT.write_text(STANDALONE.format(body=body), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    if args.body_only:
        args.body_only.write_text(body, encoding="utf-8")
        print(f"wrote {args.body_only}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
