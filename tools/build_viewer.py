#!/usr/bin/env python3
"""Build the Formula Book viewer, a self-contained HTML page, from db/.

Usage:
    python3 tools/build_viewer.py                    # writes db/viewer.html
    python3 tools/build_viewer.py --body-only PATH   # also writes the page body only,
                                                     # for publishing as a claude.ai artifact

db/viewer.html opens in any browser with no server. It reads nothing at run
time: rerun this script (after tools/costing.py) whenever the data changes.
The Pro forma tab comes from db/proforma.yaml through tools/proforma.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import proforma  # noqa: E402
from costing import CHANNELS, DB, ROOT, Book, DBError  # noqa: E402

OUT = DB / "viewer.html"
UNIT_LABELS = {"fl_oz": "fl oz", "l": "L"}


def pack_label(size: float, unit: str) -> str:
    return f"{size:g} {UNIT_LABELS.get(unit, unit)}"


def item_name(book: Book, item: str) -> str:
    if item in book.ingredients:
        return book.ingredients[item]["name"]
    if item in book.products:
        return book.products[item]["name"]
    return book.formulas[item]["name"]


def line_kind(book: Book, item: str) -> str:
    if item in book.formulas:
        return "formula"
    return "product" if item in book.products else "ingredient"


def per_channel(fn) -> dict:
    return {ch: fn(ch) for ch in CHANNELS}


def proforma_data(book: Book) -> dict:
    """The pro forma as tools/proforma.py builds it; keys keep the model's snake_case names."""
    pf = proforma.build(book)
    cfg = pf["config"]
    return {
        "asOf": str(cfg.get("as_of", "")),
        "menus": pf["menus"],
        "operating": cfg["operating"],
        "variable": cfg["variable_costs_pct_of_sales"],
        "fixed": cfg["fixed_costs_per_year"],
        "utilitiesPsf": cfg["utilities_per_sqft_year"],
        "labor": cfg["labor"],
        "crews": pf["crews"],
        "space": cfg["space_program"],
        "equipment": cfg["equipment"],
        "startup": cfg["startup"],
        "financing": cfg["financing"],
        "scenarios": cfg["scenarios"],
        "sites": cfg["sites"],
        "results": pf["results"],
    }


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
                    "kind": line_kind(book, line["item"]),
                    "qty": line["qty"],
                    "unit": line["unit"],
                    "note": line.get("note", ""),
                    "packaging": book.is_packaging(line["item"]),
                    "credit": bool(line.get("credit")),
                    "cost": per_channel(lambda ch, line=line: book.signed_line_cost(line, ch)),
                }
            )
        labor_min = book.product_labor(pid)
        par = float(doc.get("par_daily") or 0)
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
                "laborMin": labor_min,
                "laborCost": book.labor_cost(labor_min),
                "laborNote": (doc.get("labor") or {}).get("note", ""),
                "laborBreakdown": [
                    {"name": name.replace(" (formula)", "").replace(" (product)", ""), "min": m}
                    for name, m in book.labor_breakdown(pid)
                ],
                "parDaily": par,
                "laborHoursDay": labor_min * par / 60,
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
        dough = doc["kind"] in ("dough", "batter")  # show baker's %
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
                    "kind": line_kind(book, line["item"]),
                    "qty": line["qty"],
                    "unit": line["unit"],
                    "note": line.get("note", ""),
                    "bakers": bakers,
                    "cost": per_channel(lambda ch, line=line: book.line_cost(line, ch)),
                }
            )
        yld = doc["yield"]
        batch = per_channel(lambda ch, fid=fid: book.formula_cost(fid, ch))
        lab = doc.get("labor") or {}
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
                "labor": {
                    "batchMin": lab.get("batch_min"),
                    "productionBatches": lab.get("production_batches", 1),
                    "perBatch": book.formula_labor(fid),
                    "note": lab.get("note", ""),
                },
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
        "laborRate": book.labor_rate,
        "products": products,
        "formulas": formulas,
        "ingredients": ingredients,
        "proforma": proforma_data(book),
    }


PAGE = r"""<title>BostonBakery Formula Book</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500&family=Source+Sans+3:wght@400;600&display=swap">
<style>
/* Layout: burgundy header band with view tabs and a cost-basis switch over an ivory page;
   products as cards grouped by category; formulas and ingredients as expandable spec sheets.
   Single light theme by request: burgundy and ivory. */
:root {
  --bg: #faf6ee;
  --surface: #fffdf8;
  --surface-2: #f3ecdf;
  --ink: #2b1e1f;
  --ink-2: #6e5d58;
  --rule: #e4d9c8;
  --accent: #7a1f2e;
  --accent-ink: #fffdf8;
  --header-bg: #6b1a28;
  --header-ink: #fbf6ec;
  --header-ink-2: #e8d3cf;
  --header-rule: #8a3443;
  --pastry: #8a4b1f;
  --sandwich: #b0452b;
  --salad: #2c6e73;
  --soup: #7d6400;
  --catering: #5d4a8a;
  --add-on: #4a5a8a;
  --drink: #4e6e3a;
  --ok: #2f6b45;
  --ok-bg: #e2eedd;
  --warn: #8a5a00;
  --warn-bg: #f6e7c6;
  /* Price-split parts, checked with the dataviz palette validator (light surface #fffdf8).
     The pro forma's cost split reuses them (food, labor, rent, EBITDA) plus --opex; the five
     were validated together. */
  --cost: #8c2f3f;
  --pack: #c98500;
  --labor: #2a78d6;
  --margin: #ecd7d9;
  --opex: #1b8a6b;
  --bad: #8c2f3f;
  --bad-bg: #f6e1e3;
  --font-display: "Barlow Semi Condensed", "Arial Narrow", "Helvetica Neue", Arial, sans-serif;
  --font-body: "Source Sans 3", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
  color-scheme: light;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 15px/1.5 var(--font-body); }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--header-bg); }
.wrap { max-width: 1180px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.num, .money, td.n, th.n { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }
h1, h2, h3 { font-family: var(--font-display); text-wrap: balance; margin: 0; line-height: 1.15; }
a { color: var(--accent); }
button { font: inherit; color: inherit; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

header.top { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--header-bg); color: var(--header-ink); border-bottom: 1px solid var(--header-rule); }
header.top :focus-visible { outline-color: var(--header-ink); }
.top-row { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px 20px; padding-block: 14px 10px; }
.brand { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.eyebrow { font: 600 12px/1 var(--font-display); letter-spacing: .12em; text-transform: uppercase; color: var(--header-ink-2); }
.brand h1 { font-size: 28px; font-weight: 700; letter-spacing: .01em; }
.controls { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
.search { width: 220px; max-width: 100%; padding: 7px 10px; border: 1px solid var(--header-rule); border-radius: 6px; background: var(--surface); color: var(--ink); font: inherit; }
.seg { display: inline-flex; border: 1px solid var(--header-ink-2); border-radius: 6px; overflow: hidden; background: transparent; }
.seg button { border: 0; background: transparent; padding: 6px 12px; cursor: pointer; font-size: 14px; color: var(--header-ink); }
.seg button[aria-pressed="true"] { background: var(--header-ink); color: var(--accent); font-weight: 600; }
.seg-label { font-size: 13px; color: var(--header-ink-2); }
nav.tabs { display: flex; gap: 4px; overflow-x: auto; }
nav.tabs button { border: 0; background: transparent; padding: 8px 12px 10px; cursor: pointer; font: 600 16px/1 var(--font-display); letter-spacing: .02em; color: var(--header-ink-2); border-bottom: 3px solid transparent; white-space: nowrap; }
nav.tabs button[aria-selected="true"] { color: var(--header-ink); border-bottom-color: var(--header-ink); }
nav.tabs .count { font: 500 12px var(--font-mono); color: var(--header-ink-2); margin-left: 4px; }

main { padding-block: 18px 40px; display: flex; flex-direction: column; gap: 22px; }
.summary { display: flex; flex-wrap: wrap; gap: 8px 18px; align-items: baseline; color: var(--ink-2); font-size: 14px; }
.summary strong { color: var(--ink); font-weight: 600; }
.group { display: flex; flex-direction: column; gap: 12px; }
.group-head { display: flex; align-items: baseline; gap: 10px; border-bottom: 2px solid var(--accent); padding-bottom: 6px; }
.group-head h2 { font-size: 20px; }
.group-head .count { font: 500 13px var(--font-mono); color: var(--ink-2); }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 330px), 1fr)); gap: 14px; align-items: start; }

.card { background: var(--surface); border: 1px solid var(--rule); border-radius: 8px; padding: 14px 16px; display: flex; flex-direction: column; gap: 10px; min-width: 0; }
.card.open { grid-column: 1 / -1; }
.card-top { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.card-name { font-size: 22px; font-weight: 700; color: var(--accent); }
.card-desc { margin: 0; color: var(--ink-2); font-size: 14px; max-width: 65ch; }
.chip { display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; border-radius: 999px; font-size: 12px; font-weight: 600; letter-spacing: .03em; border: 1px solid var(--rule); color: var(--ink-2); background: var(--surface); text-transform: lowercase; }
.cat-pastry { color: var(--pastry); border-color: currentColor; }
.cat-sandwich { color: var(--sandwich); border-color: currentColor; }
.cat-salad { color: var(--salad); border-color: currentColor; }
.cat-soup { color: var(--soup); border-color: currentColor; }
.cat-add-on { color: var(--add-on); border-color: currentColor; }
.cat-catering { color: var(--catering); border-color: currentColor; }
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

.bar { display: flex; gap: 2px; height: 8px; border-radius: 4px; overflow: hidden; }
.bar span { display: block; height: 100%; }
.bar .s-cost { background: var(--cost); }
.bar .s-pack { background: var(--pack); }
.bar .s-labor { background: var(--labor); }
.bar .s-margin { background: var(--margin); }
.legend { display: flex; flex-wrap: wrap; gap: 4px 14px; font-size: 12px; color: var(--ink-2); }
.legend i { display: inline-block; width: 9px; height: 9px; border-radius: 2px; margin-right: 5px; vertical-align: -1px; }
.legend .k-cost { background: var(--cost); } .legend .k-pack { background: var(--pack); } .legend .k-labor { background: var(--labor); } .legend .k-margin { background: var(--margin); }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 165px), 1fr)); gap: 12px; }
.tile { background: var(--surface); border: 1px solid var(--rule); border-radius: 8px; padding: 12px 14px; display: flex; flex-direction: column; gap: 4px; }
.tile .t-label { font-size: 13px; color: var(--ink-2); }
.tile .t-value { font: 600 26px/1.1 var(--font-body); color: var(--ink); }
.hours { display: flex; align-items: center; gap: 8px; min-width: 150px; }
.hours .hb { height: 12px; background: var(--labor); border-radius: 0 4px 4px 0; flex: none; }
.hours .hv { font: 500 13px var(--font-mono); font-variant-numeric: tabular-nums; color: var(--ink); white-space: nowrap; }
tr.click:focus-visible td { background: var(--surface-2); }
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
.controls[hidden] { display: none; }
.sr-only { position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }
.pf h4 { margin: 0 0 6px; font: 700 13px var(--font-display); letter-spacing: .1em; text-transform: uppercase; color: var(--ink-2); }
.pf p { margin: 0; max-width: 80ch; }
.pf th { white-space: normal; }
.pf td .pill { white-space: nowrap; }
.stack { display: flex; flex-direction: column; gap: 22px; min-width: 0; }
.pf-ctl { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; }
.ctl-label { font: 700 12px var(--font-display); letter-spacing: .1em; text-transform: uppercase; color: var(--ink-2); }
.tile .t-sub { font-size: 12px; color: var(--ink-2); }
.neg { color: var(--bad); }
.pbar { position: relative; padding-block: 3px; margin-bottom: 6px; }
.pbar .bar { height: 12px; }
.pbar .tick { position: absolute; top: 0; bottom: 0; width: 2px; margin-left: -1px; background: var(--ink); }
.bar .s-opex { background: var(--opex); }
.legend .k-opex { background: var(--opex); }
.legend .k-tick { width: 2px; background: var(--ink); }
.pill.ok { background: var(--ok-bg); color: var(--ok); }
.pill.warn { background: var(--warn-bg); color: var(--warn); }
.pill.bad { background: var(--bad-bg); color: var(--bad); }
tr.cur td { background: var(--surface-2); }
tr.cur td:first-child { box-shadow: inset 3px 0 0 var(--accent); }
.zone { display: flex; align-items: center; min-width: 90px; }
.zone span { display: block; height: 8px; background: var(--ink-2); border-radius: 0 3px 3px 0; }
.empty { padding: 24px; text-align: center; color: var(--ink-2); border: 1px dashed var(--rule); border-radius: 8px; }
footer { padding-block: 0 32px; color: var(--ink-2); font-size: 13px; }
@media (max-width: 560px) {
  .pf th, .pf td { padding-inline: 7px; }
  .pf td .pill { white-space: normal; }
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
    { id: "ingredients", label: "Ingredients", count: DATA.ingredients.length },
    { id: "labor", label: "Labor", count: Math.round(DATA.products.reduce((s, p) => s + p.laborHoursDay, 0)) + " h/day" },
    { id: "proforma", label: "Pro forma", count: DATA.proforma.sites.length + (DATA.proforma.sites.length === 1 ? " site" : " sites") }
  ];
  const CATS = [["pastry", "Pastry"], ["sandwich", "Sandwiches"], ["salad", "Salads"], ["soup", "Soups"], ["add-on", "Add-ons"], ["drink", "Drinks"], ["catering", "Pre-order & catering"]];
  const STATUS = { approved: "Approved", pending_test: "Pending test", draft: "Draft", retired: "Retired" };
  const PF = DATA.proforma;
  const state = { view: "products", channel: "distributor_est", query: "", open: new Set(), cat: "all", lcat: "all",
    site: PF.sites[0].id, scen: PF.scenarios.some((s) => s.id === "base") ? "base" : PF.scenarios[0].id };
  try { const saved = localStorage.getItem("fb-channel"); if (saved && CH.includes(saved)) state.channel = saved; } catch (e) {}

  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const money = (v) => v == null ? "n/a" : (v > 0 && v < 0.005 ? "<$0.01" : v < 0 ? "−$" + (-v).toFixed(2) : "$" + v.toFixed(2));
  const mins = (m) => (Math.round(m * 10) / 10).toFixed(1) + " min";
  const unitCost = (p, ch) => p.food[ch] == null ? null : p.food[ch] + (p.hasPackaging ? (p.packagingCost[ch] || 0) : 0);
  const num = (q) => Number(q).toLocaleString("en-US", { maximumFractionDigits: 1 });
  const qty = (q, unit) => unit === "each" ? num(q) + " each" : num(q) + " g";
  const pct = (a, b) => (a == null || !b) ? "n/a" : String(Math.round((100 * a) / b)).replace("-", "−") + "%";
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
    document.querySelector(".controls").hidden = state.view === "proforma";
    const nav = document.getElementById("tabs"), sel = nav.querySelector('[aria-selected="true"]');
    if (sel) {
      const left = sel.offsetLeft - nav.offsetLeft, right = left + sel.offsetWidth;
      if (left < nav.scrollLeft || right > nav.scrollLeft + nav.clientWidth) nav.scrollLeft = Math.max(0, right - nav.clientWidth + 16);
    }
  }

  function costCells(cost) {
    return CH.map((ch) => `<td class="n ${ch === state.channel ? "sel" : "dim"}">${money(cost[ch])}</td>`).join("");
  }
  const costHeads = () => CH.map((ch) => `<th class="n">${chLabel(ch)}</th>`).join("");

  function productCard(p) {
    const ch = state.channel;
    const food = p.food[ch], pack = p.hasPackaging ? p.packagingCost[ch] : 0;
    const total = food == null ? null : food + (pack || 0);
    const labor = p.laborCost;
    const prime = total == null ? null : total + labor;
    const margin = prime == null || p.price == null ? null : p.price - prime;
    const share = (v) => p.price ? Math.max(0, (100 * (v || 0)) / p.price) : 0;
    let left = 100;
    const fw = Math.min(left, share(food)); left -= fw;
    const pw = Math.min(left, share(pack)); left -= pw;
    const lw = Math.min(left, share(labor)); left -= lw;
    const seg = (cls, w) => w > 0 ? `<span class="${cls}" style="width:${w}%"></span>` : "";
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
          <div><dt>Labor</dt><dd>${money(labor)} <span class="muted small">${mins(p.laborMin)}</span></dd></div>
          <div><dt>Prime cost</dt><dd>${pct(prime, p.price)}</dd></div>
          <div><dt>Margin after labor</dt><dd>${money(margin)}</dd></div>
        </dl>
      </div>
      <div class="bar" role="img" aria-label="Of the price: food ${pct(food, p.price)}, packaging ${p.hasPackaging ? pct(pack, p.price) : "none"}, labor ${pct(labor, p.price)}, margin ${pct(margin, p.price)}">${seg("s-cost", fw)}${seg("s-pack", pw)}${seg("s-labor", lw)}${seg("s-margin", left)}</div>
      <div class="legend"><span><i class="k-cost"></i>Food ${pct(food, p.price)}</span><span><i class="k-pack"></i>Packaging ${p.hasPackaging ? pct(pack, p.price) : "none"}</span><span><i class="k-labor"></i>Labor ${pct(labor, p.price)}</span><span><i class="k-margin"></i>Margin ${pct(margin, p.price)}</span></div>
      <div class="chips">${allergens}</div>
      <button type="button" class="toggle" data-toggle="${key}" aria-expanded="${open}">${open ? "Hide build and method" : "Show build and method"}</button>
      ${open ? productDetails(p) : ""}
    </article>`;
  }

  function productDetails(p) {
    const rows = p.build.map((b) => `<tr><td>${esc(b.name)}${b.kind !== "ingredient" ? ` <span class="muted small">(${b.kind})</span>` : ""}${b.credit ? ` <span class="muted small">(replaced)</span>` : ""}${b.note ? `<span class="note">${esc(b.note)}</span>` : ""}</td><td class="n">${qty(b.qty, b.unit)}</td>${costCells(b.cost)}</tr>`).join("");
    const waste = {};
    const foodOnly = {};
    CH.forEach((ch) => {
      foodOnly[ch] = p.build.filter((b) => !b.packaging).reduce((s, b) => s + (b.cost[ch] || 0), 0);
      waste[ch] = foodOnly[ch] * p.wastePct / 100;
    });
    const totals = {}, laborRow = {}, primes = {};
    CH.forEach((ch) => {
      totals[ch] = p.food[ch] == null ? null : p.food[ch] + (p.packagingCost[ch] || 0);
      laborRow[ch] = p.laborCost;
      primes[ch] = totals[ch] == null ? null : totals[ch] + p.laborCost;
    });
    const breakdown = p.laborBreakdown.map((b) => `${b.name === "own steps" ? "Own steps" : b.name}: ${mins(b.min)}`);
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
          <tr><td>Prep labor at $${DATA.laborRate.toFixed(2)}/hr</td><td class="n">${mins(p.laborMin)}</td>${costCells(laborRow)}</tr>
          <tr class="total"><td>Prime cost</td><td></td>${costCells(primes)}</tr>
        </tbody></table></div>
      </div>
      <div class="cols">${prod}${targets}${p.qa.length ? `<div><h4>QA checks</h4>${list(p.qa)}</div>` : ""}
        <div><h4>Prep labor</h4>${p.laborNote ? `<p style="margin:0 0 6px;max-width:75ch">${esc(p.laborNote)}</p>` : ""}${list(breakdown)}<p class="muted small" style="margin:6px 0 0">${num(p.parDaily)} a day at par: ${(Math.round(p.laborHoursDay * 10) / 10).toFixed(1)} hands-on hours. Minutes include the waste allowance.</p></div>
      </div>
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
    let html = `<div class="summary"><span><strong>${counts.approved || 0}</strong> approved</span><span><strong>${counts.pending_test || 0}</strong> pending test</span>${counts.draft ? `<span><strong>${counts.draft}</strong> draft</span>` : ""}<span>Costs at <strong>${chLabel(state.channel).toLowerCase()}</strong> prices, as of ${esc(DATA.asOf)}. All prices are estimates until real quotes replace them.</span></div>`;
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
        <div><dt>Labor per batch</dt><dd>${mins(f.labor.perBatch)}</dd></div>
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
            ${f.labor.batchMin != null ? `<h4 style="margin-top:14px">Prep labor</h4><p style="margin:0">${num(f.labor.batchMin)} hands-on min per production run of ${num(f.labor.productionBatches)} batch${f.labor.productionBatches == 1 ? "" : "es"}; ${mins(f.labor.perBatch)} per batch with sub-recipes.${f.labor.note ? " " + esc(f.labor.note) : ""}</p>` : ""}
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

  function renderLabor() {
    const ch = state.channel;
    const all = DATA.products;
    const sales = all.reduce((s, p) => s + (p.price || 0) * p.parDaily, 0);
    const hours = all.reduce((s, p) => s + p.laborHoursDay, 0);
    const laborUsd = hours * DATA.laborRate;
    const goods = all.reduce((s, p) => s + (unitCost(p, ch) || 0) * p.parDaily, 0);
    const tiles = `<div class="tiles">
      <div class="tile"><span class="t-label">Sales a day at par</span><span class="t-value">$${Math.round(sales).toLocaleString("en-US")}</span></div>
      <div class="tile"><span class="t-label">Hands-on hours a day</span><span class="t-value">${hours.toFixed(1)}</span></div>
      <div class="tile"><span class="t-label">Prep labor, share of sales</span><span class="t-value">${pct(laborUsd, sales)}</span></div>
      <div class="tile"><span class="t-label">Food, packaging and prep labor, share of sales</span><span class="t-value">${pct(goods + laborUsd, sales)}</span></div>
    </div>`;
    const present = CATS.filter(([c]) => all.some((p) => p.category === c));
    const filters = `<div class="filters" role="group" aria-label="Filter by category"><button type="button" data-lcat="all" aria-pressed="${state.lcat === "all"}">All</button>${present.map(([c, label]) => `<button type="button" data-lcat="${esc(c)}" aria-pressed="${state.lcat === c}">${esc(label)}</button>`).join("")}</div>`;
    const items = all.filter((p) => (state.lcat === "all" || p.category === state.lcat) && matches(p.name)).slice().sort((a, b) => b.laborHoursDay - a.laborHoursDay);
    const maxH = Math.max(0.0001, ...items.map((p) => p.laborHoursDay));
    const rows = items.map((p) => {
      const key = "l:" + p.id, open = state.open.has(key);
      const prime = unitCost(p, ch) == null ? null : unitCost(p, ch) + p.laborCost;
      const h = (Math.round(p.laborHoursDay * 10) / 10).toFixed(1);
      const w = Math.max(p.laborHoursDay > 0 ? 2 : 0, Math.round((120 * p.laborHoursDay) / maxH));
      const detail = open ? `<tr class="detail"><td colspan="6"><div class="cols"><div><h4>Where the minutes go</h4>${list(p.laborBreakdown.map((b) => `${b.name === "own steps" ? "Own steps" : b.name}: ${mins(b.min)}`))}${p.laborNote ? `<p class="muted small" style="margin:6px 0 0">${esc(p.laborNote)}</p>` : ""}</div></div></td></tr>` : "";
      return `<tr class="click" data-toggle="${key}" tabindex="0" aria-expanded="${open}"><td>${esc(p.name)}<span class="note">${esc((CATS.find(([c]) => c === p.category) || [0, p.category])[1])}</span></td><td class="n">${num(p.parDaily)}</td><td class="n">${(Math.round(p.laborMin * 10) / 10).toFixed(1)}</td><td class="n hide-sm">${money(p.laborCost)}</td><td class="n hide-sm">${pct(prime, p.price)}</td><td><div class="hours" role="img" aria-label="${esc(p.name)}: ${h} hands-on hours a day"><span class="hb" style="width:${w}px"></span><span class="hv">${h} h</span></div></td></tr>${detail}`;
    }).join("");
    const table = `<div class="tbl-wrap"><table><thead><tr><th>Product</th><th class="n">Par/day</th><th class="n">Min/unit</th><th class="n hide-sm">Labor/unit</th><th class="n hide-sm">Prime cost</th><th>Hands-on hours a day</th></tr></thead><tbody>${rows}</tbody></table></div>`;
    return `<div class="summary"><span>Hands-on prep and bar minutes at <strong>$${DATA.laborRate.toFixed(2)}/hr</strong>, including each sub-recipe's share of its production run. Proofing, baking and brewing time, taking orders and bagging aren't counted. Daily figures use each product's planning par; prime cost uses <strong>${chLabel(ch).toLowerCase()}</strong> prices. Tap a row to see where the minutes go.</span></div>${tiles}${filters}${items.length ? table : `<div class="empty">No products match.</div>`}`;
  }

  // Pro forma: dollars in whole dollars, $K for tables and $M or $K for tiles.
  const dollars = (v) => v == null ? "n/a" : (v < 0 ? "−$" : "$") + Math.round(Math.abs(v)).toLocaleString("en-US");
  const kd = (v) => v == null ? "n/a" : (Math.round(v / 1000) < 0 ? "−$" : "$") + Math.abs(Math.round(v / 1000)).toLocaleString("en-US") + "K";
  const big = (v) => v != null && Math.abs(v) >= 999500 ? (v < 0 ? "−$" : "$") + (Math.abs(v) / 1e6).toFixed(2) + "M" : kd(v);
  const neg = (v) => v != null && Math.round(v) < 0 ? " neg" : "";
  const whole = (v) => v == null ? "n/a" : Math.round(v).toLocaleString("en-US");
  const fmtCfg = (fmt) => PF.labor.formats[fmt];
  const fmtName = (fmt) => fmtCfg(fmt).label.split(":")[0];
  const fmtDays = (fmt) => fmtCfg(fmt).days_per_year || PF.operating.days_per_year;
  const fmtHours = (fmt) => fmtCfg(fmt).hours || PF.operating.hours;
  const fmtManaged = (fmt) => fmtCfg(fmt).manager !== false;
  const FORMATS = Object.keys(PF.labor.formats);
  const PF_LINES = [
    ["cogs", "Food and packaging"],
    ["hourly_labor", "Hourly crew, with payroll taxes"],
    ["manager", "General manager, with payroll taxes"],
    ["rent", "Base rent"],
    ["nnn", "NNN charges"],
    ["utilities", "Utilities"],
    ["variable_opex", "Card fees, repairs, supplies, marketing"],
    ["fixed_opex", "Insurance, software, accounting, other fixed"]
  ];
  const COST_WORDS = { card_processing: "card fees", repairs_maintenance: "repairs", supplies_cleaning: "supplies", delivery_net: "delivery apps, net", miscellaneous: "other",
    software_pos: "point of sale and software", accounting_payroll_legal: "accounting, payroll and legal", licenses_music: "licenses and music", waste_pest: "trash and pest control", linens_uniforms: "linens and uniforms", internet_phone: "internet and phone" };
  const costWord = (k) => COST_WORDS[k] || k.replace(/_/g, " ");
  const tile = (label, value, sub, isNeg) => `<div class="tile"><span class="t-label">${esc(label)}</span><span class="t-value${isNeg ? " neg" : ""}">${value}</span>${sub ? `<span class="t-sub">${sub}</span>` : ""}</div>`;

  // An owner-run shop has to pay its owner as well as its loan.
  function verdict(r) {
    const y2 = r.years[1];
    if (y2.ebitda <= 0) return ["bad", "Loses money"];
    if (y2.cash_after_debt < 0) return ["bad", "Can't carry the loan"];
    if (!r.managed && r.owner_pay_target && y2.cash_after_debt < r.owner_pay_target) return ["warn", "Underpays the owner"];
    if (!r.reserve_covers_year1) return ["warn", "Year 1 needs more cash"];
    return ["ok", "Pays its way"];
  }

  function costBar(y, managed) {
    const parts = [
      ["cost", "Food and packaging", y.cogs],
      ["labor", managed ? "Crew and manager" : "Paid crew", y.hourly_labor + y.manager],
      ["pack", "Rent and NNN", y.rent + y.nnn],
      ["opex", "Utilities and other costs", y.utilities + y.variable_opex + y.fixed_opex]
    ];
    const costs = parts.reduce((s, x) => s + x[2], 0);
    const denom = Math.max(y.sales, costs);
    const w = (v) => (100 * v / denom).toFixed(2);
    const loss = y.ebitda < 0;
    const rest = managed ? "EBITDA" : "Left for loan payments and the owner";
    const segs = parts.map(([k, , v]) => `<span class="s-${k}" style="width:${w(v)}%"></span>`).join("") + (loss ? "" : `<span class="s-margin" style="width:${w(y.ebitda)}%"></span>`);
    const items = parts.map(([k, label, v]) => [k, label, pct(v, y.sales)]).concat([loss ? ["tick", "Sales end at the line: loss", pct(y.ebitda, y.sales)] : ["margin", rest, pct(y.ebitda, y.sales)]]);
    const aria = "Of Year-2 sales: " + items.map(([, l, v]) => `${l.toLowerCase()} ${v}`).join(", ");
    return `<div class="pbar" role="img" aria-label="${esc(aria)}"><div class="bar">${segs}</div>${loss ? `<b class="tick" style="left:${w(y.sales)}%"></b>` : ""}</div>
      <div class="legend">${items.map(([k, l, v]) => `<span><i class="k-${k}"></i>${esc(l)} ${v}</span>`).join("")}</div>`;
  }

  function renderProforma() {
    const op = PF.operating, fin = PF.financing, lab = PF.labor;
    const sc = state.scen, scen = PF.scenarios.find((s) => s.id === sc);
    const site = PF.sites.find((s) => s.id === state.site) || PF.sites[0];
    const r = PF.results[site.id][sc];
    const f = fmtCfg(site.format), menu = PF.menus[site.format], managed = r.managed;
    const ys = r.years, y1 = ys[0], y2 = ys[1], y3 = ys[2];
    const ramp = op.ramp_year1_pct, rampAvg = ramp.reduce((a, b) => a + b, 0) / ramp.length;
    const hero = menu.hero_name ? menu.hero_name.toLowerCase() + "s" : null;

    // Formats: each one's design day and what it needs
    const fmtRows = FORMATS.map((k) => {
      const m = PF.menus[k], c = PF.crews[k], label = fmtCfg(k).label, i = label.indexOf(":");
      const space = PF.space[k].reduce((a, z) => a + z.sqft, 0), equip = PF.equipment[k].reduce((a, e) => a + e.cost, 0);
      return `<tr><td>${esc(fmtName(k))}<span class="note">${esc(i < 0 ? "" : label.slice(i + 1).trim() + ". ")}${fmtManaged(k) ? "Hired manager" : "Owner-run"}; ${esc(fmtHours(k))}</span></td>
        <td class="n">${dollars(m.sales)}</td><td class="n">${whole(m.orders)}</td><td class="n hide-sm">$${m.ticket.toFixed(2)}</td>
        <td class="n hide-sm">${(m.goods_pct + op.cogs_buffer_pts).toFixed(0)}%</td><td class="n hide-sm">${c.hours}</td>
        <td class="n">${space.toLocaleString("en-US")}</td><td class="n hide-sm">${kd(equip)}</td></tr>`;
    }).join("");
    const top = `<div class="summary"><span>Each format has a design day: its products' daily volumes times their prices. A site's sales index scales that day to the site, and the scenario scales it again. Food cost is the menu's at distributor prices plus ${op.cogs_buffer_pts} points. Estimates as of ${esc(PF.asOf)}; no site has been confirmed with a broker.</span></div>
      <section class="group pf"><div class="group-head"><h2>Formats</h2></div>
      <div class="tbl-wrap"><table><thead><tr><th>Format</th><th class="n">Sales on a design day</th><th class="n">Orders</th><th class="n hide-sm">Average order</th><th class="n hide-sm">Food and packaging</th><th class="n hide-sm">Paid crew hours a day</th><th class="n">Space, sq ft</th><th class="n hide-sm">Equipment</th></tr></thead><tbody>${fmtRows}</tbody></table></div>
      <p class="muted small">Order counts divide the items sold by an assumed items per order, so treat them as rough. An owner-run format's costs include no pay for the owner: what's left after loan payments is the owner's pay.</p></section>`;

    // Sites compared, in the chosen scenario
    const scenChips = `<div class="pf-ctl"><span class="ctl-label" id="scen-label">Scenario</span><div class="filters" role="group" aria-labelledby="scen-label">${PF.scenarios.map((s) => `<button type="button" data-scen="${esc(s.id)}" aria-pressed="${s.id === sc}">${esc(s.name)}, ${Math.round(s.sales_factor * 100)}% of base sales</button>`).join("")}</div></div>`;
    const cmpRows = PF.sites.map((s) => {
      const q = PF.results[s.id][sc], q2 = q.years[1], [cls, text] = verdict(q);
      return `<tr class="click${s.id === site.id ? " cur" : ""}" data-site="${esc(s.id)}" tabindex="0"${s.id === site.id ? ` aria-current="true"` : ""}>
        <td>${esc(s.short || s.name)}<span class="note">${esc(fmtName(s.format))}, ${s.sqft.toLocaleString("en-US")} sq ft</span></td>
        <td class="n">${big(q.steady_sales)}</td>
        <td class="n hide-sm">${whole(q.orders_daily)}</td>
        <td class="n hide-sm">$${Number(s.rent_psf).toFixed(0)}${s.rent_assumed ? "*" : ""} / ${q.rent_ceiling_psf == null ? "none" : "$" + q.rent_ceiling_psf.toFixed(0)}</td>
        <td class="n hide-sm">${kd(q.startup)}</td>
        <td class="n hide-sm${neg(q2.ebitda)}">${kd(q2.ebitda)}</td>
        <td class="n${neg(q2.cash_after_debt)}">${kd(q2.cash_after_debt)}${q.managed ? "" : "†"}</td>
        <td class="n hide-sm">${dollars(q.breakeven_daily)}</td>
        <td><span class="pill ${cls}">${text}</span></td></tr>`;
    }).join("");
    const anyOwnerRun = PF.sites.some((s) => !fmtManaged(s.format));
    const compare = `<section class="group pf"><div class="group-head"><h2>Sites compared</h2><span class="count">${esc(scen.name)}</span></div>${scenChips}
      <div class="tbl-wrap"><table><thead><tr><th>Site</th><th class="n">Sales a year</th><th class="n hide-sm">Orders a day</th><th class="n hide-sm">Rent per sq ft / most it can carry</th><th class="n hide-sm">Startup</th><th class="n hide-sm">EBITDA</th><th class="n">Cash after loan</th><th class="n hide-sm">Break-even a day</th><th>Verdict</th></tr></thead><tbody>${cmpRows}</tbody></table></div>
      <p class="muted small">Sales, EBITDA and cash after loan payments are for Year 2, the first full year after the ramp. ${anyOwnerRun ? "† Owner-run: the costs include no pay for the owner, so this figure is the owner's pay. " : ""}"Most it can carry" is the base rent at which Year-2 cash after loan payments falls to zero${anyOwnerRun ? ", or to the owner's target pay in an owner-run shop" : ""}; * marks a rent assumed because none is published. Break-even is the daily sales at which Year-2 cash after loan payments is zero. Tap a site for its detail.</p></section>`;

    // The chosen site
    const siteChips = `<div class="pf-ctl"><span class="ctl-label" id="site-label">Site</span><div class="filters" role="group" aria-labelledby="site-label">${PF.sites.map((s) => `<button type="button" data-site="${esc(s.id)}" aria-pressed="${s.id === site.id}">${esc(s.short || s.name)}</button>`).join("")}</div></div>`;
    const facts = [["Kitchen", site.kitchen], ["Rent", site.rent_basis], ["Risks", site.risks], ["Source", site.source]].filter(([, v]) => v);
    const [vcls, vtext] = verdict(r);
    const payback = r.payback_years ? `payback ${r.payback_years.toFixed(1)} years on Year-3 EBITDA` : "no payback at these sales";
    const tiles = `<div class="tiles">${(managed ? [
      tile("Sales, Year 2", big(y2.sales), `${dollars(y2.daily_sales)} a day, about ${whole(r.orders_daily)} orders; Year 1 ${big(y1.sales)} while it ramps`),
      tile("EBITDA, Year 2", kd(y2.ebitda), `${pct(y2.ebitda, y2.sales)} of sales; Year 3 ${kd(y3.ebitda)}`, y2.ebitda < 0),
      tile("Cash after loan payments, Year 2", kd(y2.cash_after_debt), `after ${kd(r.debt_service)} a year of loan payments`, y2.cash_after_debt < 0),
      tile("If the owner manages, Year 2", kd(y2.owner_earnings), "EBITDA plus the manager's pay, before loan payments", y2.owner_earnings < 0),
      tile("Startup cost", big(r.startup), `${kd(r.equity)} owner equity; ${payback}`),
      tile("Break-even sales a day", dollars(r.breakeven_daily), `about ${whole(r.breakeven_orders_daily)} orders, against ${dollars(r.steady_daily)} projected`, r.breakeven_daily > r.steady_daily)
    ] : [
      tile("Sales, Year 2", big(y2.sales), `${dollars(y2.daily_sales)} a day; Year 1 ${big(y1.sales)} while it ramps`),
      tile("Orders a day", whole(r.orders_daily), `${hero ? `about ${whole(r.hero_units_daily)} ${esc(hero)} a day, counting boxes; ` : ""}average order $${r.ticket.toFixed(2)}`),
      tile("Left for the owner, Year 2", kd(y2.cash_after_debt), `after ${kd(r.debt_service)} of loan payments; the costs include no owner pay`, y2.cash_after_debt < 0),
      tile(`Orders a day to pay the owner ${kd(r.owner_pay_target)}`, whole(r.owner_target_orders_daily), `${dollars(r.owner_target_daily)} a day; break-even is ${whole(r.breakeven_orders_daily)} orders`, r.owner_target_daily > r.steady_daily),
      tile("Startup cost", big(r.startup), `${kd(r.equity)} owner equity, ${kd(r.loan)} loan`),
      tile("EBITDA, Year 2", kd(y2.ebitda), `${pct(y2.ebitda, y2.sales)} of sales, before loan payments and owner pay`, y2.ebitda < 0)
    ]).join("")}</div>`;

    const plRow = (label, key, cls, note) => `<tr${cls ? ` class="${cls}"` : ""}><td>${esc(label)}${note ? `<span class="note">${esc(note)}</span>` : ""}</td>${ys.map((y, i) => `<td class="n${i === 2 ? " hide-sm" : ""}${neg(y[key])}">${kd(y[key])}</td>`).join("")}<td class="n${neg(y2[key])}">${key === "sales" ? "100%" : pct(y2[key], y2.sales)}</td></tr>`;
    const pl = `<div class="tbl-wrap"><table><thead><tr><th>Line</th><th class="n">Year 1</th><th class="n">Year 2</th><th class="n hide-sm">Year 3</th><th class="n">Year 2 share</th></tr></thead><tbody>
      ${plRow("Sales", "sales", "total", `Year 1 ramps from ${ramp[0]}% to ${ramp[ramp.length - 1]}% of steady sales; Year 3 adds ${op.price_growth_pct}% in prices`)}
      ${PF_LINES.filter(([k]) => ys.some((y) => Math.round(y[k]) !== 0)).map(([k, label]) => plRow(label, k)).join("")}
      ${plRow("EBITDA", "ebitda", "total")}
      ${plRow("Loan payments", "debt_service")}
      ${managed ? plRow("Cash after loan payments", "cash_after_debt", "total") : plRow("Left for the owner after loan payments", "cash_after_debt", "total", "The costs above include no pay for the owner")}
      ${managed ? plRow("If the owner manages", "owner_earnings", "", "EBITDA plus the manager's pay, before loan payments") : ""}
      <tr><td>Paid crew hours a day</td>${ys.map((y, i) => `<td class="n${i === 2 ? " hide-sm" : ""}">${y.hours_day.toFixed(0)}</td>`).join("")}<td></td></tr>
    </tbody></table></div>
    <p class="muted small" style="margin-top:6px">Prime cost (food, packaging${managed ? ", crew and manager" : " and paid crew, before any owner pay"}) is ${pct(y2.cogs + y2.hourly_labor + y2.manager, y2.sales)} of Year-2 sales, with ${dollars(r.sales_per_labor_hour_y2)} of sales per paid crew hour. Each extra $100 a day of sales adds about ${dollars(r.per_extra_100_daily)} a year of EBITDA.${!managed && r.owner_target_daily ? ` Paying the owner ${dollars(r.owner_pay_target)} a year takes ${dollars(r.owner_target_daily)} a day, about ${whole(r.owner_target_orders_daily)} orders.` : ""}</p>`;

    const scRows = PF.scenarios.map((s) => {
      const q = PF.results[site.id][s.id], q2 = q.years[1];
      const last = managed ? `<td class="n hide-sm${neg(q2.owner_earnings)}">${kd(q2.owner_earnings)}</td>` : `<td class="n hide-sm">${whole(q.hero_units_daily)}</td>`;
      return `<tr class="click${s.id === sc ? " cur" : ""}" data-scen="${esc(s.id)}" tabindex="0"${s.id === sc ? ` aria-current="true"` : ""}><td>${esc(s.name)}<span class="note">${Math.round(s.sales_factor * 100)}% of base sales</span></td><td class="n">${dollars(q.steady_daily)}</td><td class="n">${whole(q.orders_daily)}</td><td class="n${neg(q2.cash_after_debt)}">${kd(q2.cash_after_debt)}</td>${last}</tr>`;
    }).join("");
    const scenTable = `<div class="tbl-wrap"><table><thead><tr><th>Scenario</th><th class="n">Sales a day</th><th class="n">Orders a day</th><th class="n">${managed ? "Cash after loan" : "Left for the owner"}</th><th class="n hide-sm">${managed ? "If owner manages" : esc(hero ? hero.replace(/^\w/, (ch) => ch.toUpperCase()) + " a day" : "Units a day")}</th></tr></thead><tbody>${scRows}</tbody></table></div><p class="muted small" style="margin-top:6px">Year 2. Tap a scenario to switch the whole tab.</p>`;

    const y1cash = y1.cash_after_debt >= 0
      ? `Year 1 makes ${dollars(y1.cash_after_debt)} after loan payments, so the ${dollars(r.reserve)} working capital reserve stays untouched.`
      : `Year 1 runs ${dollars(-y1.cash_after_debt)} short after loan payments, ${r.reserve_covers_year1 ? "inside" : "more than"} the ${dollars(r.reserve)} working capital reserve${r.reserve_covers_year1 ? "" : ": it needs more equity or a cheaper start"}.`;
    const startup = `<div class="tbl-wrap"><table><thead><tr><th>Item</th><th class="n">Cost</th></tr></thead><tbody>
      ${Object.entries(r.startup_lines).map(([k, v]) => `<tr><td>${esc(k)}${k === "Equipment" && site.equipment_credit ? `<span class="note">Net of a ${dollars(site.equipment_credit)} credit: ${esc(site.equipment_credit_note || "equipment already in place")}</span>` : ""}</td><td class="n">${dollars(v)}</td></tr>`).join("")}
      <tr class="total"><td>Total</td><td class="n">${dollars(r.startup)}</td></tr>
    </tbody></table></div>
    <p class="small" style="margin-top:6px">Financed ${fin.loan_share_pct}% with a ${fin.term_years}-year loan at ${fin.rate_pct}%: ${dollars(r.loan)}, paid at ${dollars(r.debt_service)} a year. Owner equity ${dollars(r.equity)}. ${y1cash}${managed ? "" : " The owner draws nothing in Year 1 on these figures."}</p>`;

    const zones = PF.space[site.format];
    const ztotal = zones.reduce((a, z) => a + z.sqft, 0), zmax = Math.max(...zones.map((z) => z.sqft));
    const spare = site.sqft - ztotal;
    const space = `<div class="tbl-wrap"><table><thead><tr><th>Zone</th><th class="n">Sq ft</th><th class="hide-sm"><span class="sr-only">Size</span></th></tr></thead><tbody>
      ${zones.map((z) => `<tr><td>${esc(z.zone)}</td><td class="n">${z.sqft.toLocaleString("en-US")}</td><td class="hide-sm"><div class="zone" aria-hidden="true"><span style="width:${Math.round((80 * z.sqft) / zmax)}px"></span></div></td></tr>`).join("")}
      <tr class="total"><td>${esc(fmtName(site.format))} program</td><td class="n">${ztotal.toLocaleString("en-US")}</td><td class="hide-sm"></td></tr>
      <tr><td>This site<span class="note">${site.space_note ? esc(site.space_note) : spare >= 0 ? `${spare.toLocaleString("en-US")} sq ft to spare for seats or storage` : `${(-spare).toLocaleString("en-US")} sq ft short: trim seats or storage`}</span></td><td class="n">${site.sqft.toLocaleString("en-US")}</td><td class="hide-sm"></td></tr>
    </tbody></table></div>`;

    const c = PF.crews[site.format];
    const staff = `<div class="tbl-wrap"><table><thead><tr><th>Role</th><th class="n">Hours a day</th><th class="n">Wage</th><th class="hide-sm">Covers</th></tr></thead><tbody>
      ${f.roles.map((x) => `<tr><td>${esc(x.role)}</td><td class="n">${x.hours}</td><td class="n">${x.owner ? "owner" : "$" + Number(x.wage).toFixed(2)}</td><td class="hide-sm small">${esc(x.note || "")}</td></tr>`).join("")}
      <tr class="total"><td>Paid crew</td><td class="n">${c.hours}</td><td class="n">$${c.avg_wage.toFixed(2)}</td><td class="hide-sm small">average wage</td></tr>
    </tbody></table></div>
    <p class="muted small" style="margin-top:6px">Scheduled for ${Math.round(f.design_index * 100)}% of the format's design day, which the menu counts as ${menu.hands_on_hours.toFixed(1)} hands-on prep and bar hours. ${Math.round(lab.fixed_share * 100)}% of the paid hours stay fixed and the rest flex with sales. ${managed ? `Plus a ${esc(lab.manager.title.toLowerCase())} at ${dollars(lab.manager.salary)}.` : `The owner works about ${c.owner_hours} hours a day and isn't paid in the P&L.`} Payroll taxes and workers' comp add ${lab.burden_pct}% to all pay.</p>`;

    const eq = PF.equipment[site.format], eqTotal = eq.reduce((a, e) => a + e.cost, 0);
    const equipment = `<div class="tbl-wrap"><table><thead><tr><th>Item</th><th class="n">Cost</th></tr></thead><tbody>
      ${eq.map((e) => `<tr><td>${esc(e.item)}</td><td class="n">${dollars(e.cost)}</td></tr>`).join("")}
      ${site.equipment_credit ? `<tr><td>Credit: ${esc(site.equipment_credit_note || "equipment already in place")}</td><td class="n neg">${dollars(-site.equipment_credit)}</td></tr>` : ""}
      <tr class="total"><td>Equipment, before contingency</td><td class="n">${dollars(eqTotal - (site.equipment_credit || 0))}</td></tr>
    </tbody></table></div>`;

    const ceiling = r.rent_ceiling_psf == null ? "none" : "$" + r.rent_ceiling_psf.toFixed(0);
    const detail = `<section class="group pf"><div class="group-head"><h2>${esc(site.name)}</h2><span class="count">${esc(scen.name)}</span></div>${siteChips}
      <div class="chips"><span class="pill ${vcls}">${vtext}</span><span class="muted small">${esc(site.area || "")}. ${esc(fmtName(site.format))}, ${site.sqft.toLocaleString("en-US")} sq ft, ${site.seats} seats. Rent $${Number(site.rent_psf).toFixed(2)} a sq ft${site.rent_assumed ? " (assumed; none published)" : ""} plus about $${Number(site.nnn_psf).toFixed(2)} NNN; the most base rent it can carry${managed ? "" : ` and still pay the owner ${kd(r.owner_pay_target)}`} is ${ceiling}. Sales index ${site.sales_index} of the format's design day. About ${site.months_to_open || 0} months from lease to opening.</span></div>
      ${facts.length ? `<dl class="specs small">${facts.map(([k, v]) => `<dt>${k}</dt><dd>${esc(v)}</dd>`).join("")}</dl>` : ""}
      ${tiles}
      <div><h4>Where Year-2 sales go</h4>${costBar(y2, managed)}</div>
      <div><h4>Three years</h4>${pl}</div>
      <div class="cols">
        <div class="stack"><div><h4>Scenarios at this site</h4>${scenTable}</div><div><h4>Space</h4>${space}</div><div><h4>Staffing</h4>${staff}</div></div>
        <div class="stack"><div><h4>Startup cost</h4>${startup}</div><div><h4>Equipment</h4>${equipment}</div></div>
      </div>
    </section>`;

    const varTotal = Object.values(PF.variable).reduce((a, b) => a + b, 0);
    const fixedOf = (k) => Object.values(Object.assign({}, PF.fixed, fmtCfg(k).fixed_costs_per_year || {})).reduce((a, b) => a + b, 0);
    const lower = (k) => fmtName(k).toLowerCase();
    const assumptions = [
      `Open: ${FORMATS.map((k) => `${lower(k)} ${fmtDays(k)} days a year, ${fmtHours(k)}`).join("; ")}.`,
      `Year 1 ramps month by month from ${ramp[0]}% to ${ramp[ramp.length - 1]}% of steady sales, ${Math.round(rampAvg)}% on average. Year 3 adds ${op.price_growth_pct}% in menu prices.`,
      `Wages, NNN charges and fixed costs rise ${op.cost_inflation_pct}% a year; base rent rises at each site's escalation.`,
      `Food and packaging: each menu's cost at distributor prices (${FORMATS.map((k) => `${lower(k)} ${PF.menus[k].goods_pct.toFixed(1)}%`).join(", ")} of sales) plus ${op.cogs_buffer_pts} points for waste beyond the recipes' allowances, comps, staff meals and price drift.`,
      `Crew: scheduled by format, ${Math.round(lab.fixed_share * 100)}% of paid hours fixed and the rest flexing with sales; ${lab.burden_pct}% payroll taxes and workers' comp. ${FORMATS.map((k) => fmtManaged(k) ? `The ${lower(k)} has a ${lab.manager.title.toLowerCase()} at ${dollars(lab.manager.salary)}` : `the ${lower(k)} is owner-run, with no owner pay in its costs and a target of ${dollars(fmtCfg(k).owner_pay_target)}`).join("; ")}.`,
      `Variable costs, ${varTotal.toFixed(1)}% of sales: ${Object.entries(PF.variable).map(([k, v]) => `${costWord(k)} ${v}%`).join(", ")}.`,
      `Fixed costs a year: ${FORMATS.map((k) => `${lower(k)} ${dollars(fixedOf(k))}`).join("; ")}. The bakery-café's lines: ${Object.entries(PF.fixed).map(([k, v]) => `${costWord(k)} ${dollars(v)}`).join(", ")}.`,
      `Utilities: $${PF.utilitiesPsf} a sq ft a year.`,
      `Startup: soft costs ${PF.startup.soft_costs_pct_of_buildout}% of build-out; furniture $${PF.startup.furniture_per_seat} a seat plus ${dollars(PF.startup.furniture_base)}; signage ${dollars(PF.startup.signage)}; ${PF.startup.preopening_payroll_weeks} weeks of pre-opening payroll at 60% of the crew and ${PF.startup.manager_preopening_weeks || 0} weeks of any manager; opening inventory ${dollars(PF.startup.opening_inventory)}; launch marketing ${dollars(PF.startup.launch_marketing)}; a ${PF.startup.deposit_months}-month deposit; rent and NNN from lease signing to opening, with no free rent assumed; ${PF.startup.working_capital_months} months of working capital; ${PF.startup.contingency_pct}% contingency on build-out and equipment. A smaller format uses smaller signage, inventory, marketing and furniture figures.`,
      `Financing: ${fin.loan_share_pct}% from an SBA 7(a)-style loan at ${fin.rate_pct}% over ${fin.term_years} years; the rest is owner equity.`,
      `Not included: income taxes, depreciation, the owner's pay in an owner-run format, and any landlord build-out allowance or free rent, which would lower the startup cost.`,
      `Sources: sites, sizes and rents from the site reports in reports/; wages, payroll burden and format benchmarks from the market research; menu sales, food cost and prep hours from this database. Full report: db/proforma.md.`
    ];
    const notes = `<section class="group pf"><div class="group-head"><h2>Assumptions</h2></div>${list(assumptions)}</section>`;
    return top + compare + detail + notes;
  }

  function render() {
    renderControls();
    const view = document.getElementById("view");
    view.innerHTML = state.view === "formulas" ? renderFormulas() : state.view === "ingredients" ? renderIngredients() : state.view === "labor" ? renderLabor() : state.view === "proforma" ? renderProforma() : renderProducts();
    document.getElementById("foot").innerHTML = `Generated from the <span class="num">db/</span> folder of the BostonBakery repo. Prices as of ${esc(DATA.asOf)}. Rebuild with <span class="num">tools/build_viewer.py</span> after changing the data.`;
  }

  function setView(v) { state.view = VIEWS.some((x) => x.id === v) ? v : "products"; render(); }
  function fromHash() { setView((location.hash || "").replace("#", "")); }

  document.addEventListener("click", (e) => {
    const t = e.target.closest("[data-toggle],[data-view],[data-channel],[data-cat],[data-lcat],[data-site],[data-scen]");
    if (!t) return;
    if (t.dataset.view) { if (location.hash !== "#" + t.dataset.view) location.hash = t.dataset.view; else setView(t.dataset.view); return; }
    if (t.dataset.channel) { state.channel = t.dataset.channel; try { localStorage.setItem("fb-channel", state.channel); } catch (err) {} render(); return; }
    if (t.dataset.cat) { state.cat = t.dataset.cat; render(); return; }
    if (t.dataset.lcat) { state.lcat = t.dataset.lcat; render(); return; }
    if (t.dataset.site || t.dataset.scen) {
      const attr = t.dataset.site ? "data-site" : "data-scen", val = t.dataset.site || t.dataset.scen;
      if (t.dataset.site) state.site = val; else state.scen = val;
      const tag = t.tagName.toLowerCase();
      render();
      const again = document.querySelector(`${tag}[${attr}="${CSS.escape(val)}"]`);
      if (again) again.focus({ preventScroll: true });
      return;
    }
    const key = t.dataset.toggle;
    if (state.open.has(key)) state.open.delete(key); else state.open.add(key);
    render();
    const again = document.querySelector(`[data-toggle="${CSS.escape(key)}"]`);
    if (again) again.focus({ preventScroll: true });
  });
  document.addEventListener("keydown", (e) => {
    const row = e.target.closest && e.target.closest("tr[data-toggle],tr[data-site],tr[data-scen]");
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
    try:
        body = render_body(book)
    except (DBError, KeyError, ValueError) as exc:
        print(f"error: pro forma: {exc}", file=sys.stderr)
        return 1
    OUT.write_text(STANDALONE.format(body=body), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    if args.body_only:
        args.body_only.write_text(body, encoding="utf-8")
        print(f"wrote {args.body_only}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
