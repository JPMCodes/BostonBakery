#!/usr/bin/env python3
"""Build the Miami page: the Miami plan's model as a page whose assumptions can be moved.

Usage:
    python3 tools/build_miami.py                    # checks the model, then writes db/miami.html
    python3 tools/build_miami.py --body-only PATH   # also writes the page body only,
                                                    # for publishing as a claude.ai artifact
    python3 tools/build_miami.py --check            # checks the model only

db/miami.html opens in any browser with no server. It carries the Miami formats, sites, prices
and costs from db/proforma.yaml and the menu database, and recomputes the pro forma in the page
with tools/miami_model.js, a port of tools/proforma.py's arithmetic. Every build runs that port
against the Python model (needs Node.js; skipped with a warning without it). The page's layout
is tools/miami_page.html. Rerun after tools/costing.py whenever the data changes.
"""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import proforma  # noqa: E402
from costing import DB, ROOT, Book, DBError  # noqa: E402

TOOLS = Path(__file__).resolve().parent
OUT = DB / "miami.html"
MODEL_JS = TOOLS / "miami_model.js"
PAGE_HTML = TOOLS / "miami_page.html"
MARKET = "miami"
GROWTH = "_growth"          # suffix of the format a growth_case makes
MANAGER_HIRE = 70000        # the plan's "pay a manager and step back" salary

# How the page names each channel and reads its lever back in the channel's own units.
CHANNEL_UI = {
    "window": {"short": "Walk-up window", "unit": "orders", "per": "window day", "days": "window days"},
    "drops": {"short": "Saturday pickup", "unit": "orders", "per": "Saturday", "days": "Saturdays"},
    "markets": {"short": "Farmers markets", "unit": "sales", "per": "stall-day", "days": "stall-days"},
    "orders": {"short": "Office and gift orders", "unit": "orders_week", "per": "week", "days": "working days",
               "days_week": {"roll_popup": 3, "roll_kitchen": 4}},
    "fundraisers": {"short": "Fundraisers", "unit": "events", "per": "event", "days": "events"},
    "apps": {"short": "Delivery apps", "unit": "orders", "per": "window day", "days": "window days"},
    "grocers": {"short": "Grocers' shelves", "unit": "sales", "per": "delivery day", "days": "delivery days"},
}
# Channel colors are assigned to the channel, not to its place in a chart (see the page's :root).
CHANNEL_ORDER = ["window", "drops", "markets", "orders", "fundraisers", "apps", "grocers"]

STAGES = [
    {"id": "popup", "n": 1, "format": "roll_popup", "kicker": "Stage 1", "name": "Pop-up",
     "blurb": "Market stalls, Saturday pickup, office orders and fundraisers, baked in a rented shared kitchen.",
     "tag": "The test"},
    {"id": "kitchen", "n": 2, "format": "roll_kitchen", "kicker": "Stage 2", "name": "Roll kitchen",
     "blurb": "A small production kitchen with a walk-up window and no seats, selling five ways.",
     "tag": "The business"},
    {"id": "filled", "n": 3, "format": "roll_kitchen" + GROWTH, "kicker": "Stage 3", "name": "The kitchen, filled",
     "blurb": "The same kitchen and lease with a second market team, more office orders and grocers' shelves.",
     "tag": "A target, not an estimate"},
]

# The plan's gates for signing a lease (reports/Miami bakery business plan.md, section 9).
GATES = [
    ["Sales", "$5,000 or more a week for eight straight weeks between March and May",
     "The pop-up's design averages about {popup_week} a week across the year, and the season should beat the average"],
    ["Markets", "$1,500 or more a stall-day in season", "With the crew held, the pop-up's second year leaves nothing at about {market_floor} a stall-day"],
    ["Pre-orders", "25 or more Saturday pickup orders a week by May; 40% of roll sales in boxes, trays and loaves",
     "The best proxy for the window, which can't be measured before a lease"],
    ["Offices and gifts", "12 or more orders a week from 30 or more accounts", "Two-thirds of the kitchen's design of {kitchen_orders} a week"],
    ["Fundraisers", "5 run, averaging 120 units, 3 rebooked", "The kitchen's design is {kitchen_events} a year"],
    ["Summer", "June and July at 55% or more of March and April", "The summer schedule assumes a dip, not a collapse"],
    ["Production", "1.5 hands-on minutes a roll or less over four weeks", "Otherwise budget a third baker: {baker_cost} a year"],
    ["Price", "The single roll sells at {roll_price} without discounts", "5% on prices is worth {price_5} a year"],
    ["List", "2,000 customers; 35% of pre-orders from repeat buyers", "A habit, not a novelty"],
    ["Site", "A former food bay of 800–1,200 sq ft with parking, a window allowed, five years plus an option, no bakery exclusive against you",
     "At Dadeland Plaza's size the kitchen can carry about {rent_ceiling} a sq ft and still pay you {target}"],
]


def with_growth(cfg: dict) -> dict:
    """A copy of the config with a '<format>_growth' format for each format that has a growth_case."""
    cfg = copy.deepcopy(cfg)
    formats = cfg["labor"]["formats"]
    for fid, f in list(formats.items()):
        g = f.get("growth_case")
        if not g:
            continue
        nf = copy.deepcopy(f)
        nf.pop("growth_case")
        for c in nf["channels"]:
            if c["id"] in (g.get("channel_days") or {}):
                c["days_per_year"] = g["channel_days"][c["id"]]
            factor = (g.get("channel_volume") or {}).get(c["id"])
            if factor:
                c["menu"] = {pid: par * factor for pid, par in c["menu"].items()}
            c["note"] = (g.get("channel_notes") or {}).get(c["id"], "")  # the design's notes quote its own volumes
        nf["channels"] += copy.deepcopy(g.get("add_channels") or [])
        for r in nf["roles"]:
            r["hours"] = r["hours"] + (g.get("add_hours") or {}).get(r["role"], 0)
        nf["roles"] += copy.deepcopy(g.get("add_roles") or [])
        nf["fixed_costs_per_year"] = {**(nf.get("fixed_costs_per_year") or {}), **(g.get("fixed_costs_per_year") or {})}
        nf["label"] = g.get("label", nf["label"])
        nf["growth"] = {"of": fid, "index_gain": float(g.get("sales_index_gain", 0)), "note": g.get("note", "")}
        formats[fid + GROWTH] = nf
        cfg["equipment"][fid + GROWTH] = cfg["equipment"][fid]
        cfg["space_program"][fid + GROWTH] = cfg["space_program"][fid]
    return cfg


def hero_inside(book: Book, pid: str, hero: str | None, depth: int = 0) -> float:
    """Units of the hero product inside one unit of `pid` (proforma.hero_units, for one product)."""
    if not hero:
        return 0.0
    if pid == hero:
        return 1.0
    doc = book.products.get(pid)
    if doc is None or depth > 4:
        return 0.0
    return sum(float(line["qty"]) * hero_inside(book, line["item"], hero, depth + 1)
               for line in doc["build"] if line["item"] in book.products)


def export_format(book: Book, cfg: dict, fid: str, mkt: dict, products: dict) -> dict:
    """One format's inputs with the market's overrides applied, as tools/miami_model.js reads them."""
    op, lab = cfg["operating"], cfg["labor"]
    f = lab["formats"][fid]
    at_scale = bool(f.get("production_scale"))
    hero = f.get("hero")
    ipo = float(f.get("items_per_order", 2.0))
    local = mkt.get("wages") or {}
    channels = []
    for c in f.get("channels") or []:
        prices = {**(f.get("prices") or {}), **(c.get("prices") or {})}
        lines = []
        for pid, par in c["menu"].items():
            doc = book.products[pid]
            products.setdefault(pid, {
                "name": doc["name"], "cat": doc["category"],
                "cost": book.product_cost(pid, proforma.CHANNEL) or 0,
                "min": book.product_labor(pid, at_scale=at_scale),
                "hero": hero_inside(book, pid, hero),
            })
            lines.append([pid, float(par), float(prices.get(pid, doc["pricing"].get("suggested_retail_usd") or 0)), pid in prices])
        ui = CHANNEL_UI.get(c["id"], {})
        days_week = (ui.get("days_week") or {}).get(fid.removesuffix(GROWTH))
        channels.append({
            "id": c["id"], "name": c["name"], "short": ui.get("short", c["name"]), "unit": ui.get("unit", "sales"),
            "per": ui.get("per", "day"), "days_label": ui.get("days", "days"), "days_week": days_week,
            "days": float(c["days_per_year"]), "scales": bool(c.get("scales_with_site", True)),
            "ipo": float(c.get("items_per_order", ipo)), "pi": float(c.get("price_index", 1.0)),
            "cost_pct": float(c.get("cost_pct_of_sales", 0)), "fee": float(c.get("fee_per_day", 0)),
            "note": c.get("note", ""), "lines": lines,
        })
    channels.sort(key=lambda c: CHANNEL_ORDER.index(c["id"]) if c["id"] in CHANNEL_ORDER else len(CHANNEL_ORDER))
    roles = [{"role": r["role"], "hours": float(r["hours"]), "owner": bool(r.get("owner")),
              "wage": float(local.get(r["role"], r.get("wage", 0))), "note": r.get("note", "")} for r in f["roles"]]
    baker = next((r for r in roles if r["role"] == "Baker"), None)
    growth = f.get("growth") or {}
    base = lab["formats"][growth["of"]] if growth else f
    return {
        "id": fid, "label": f["label"], "hours_text": f.get("hours", ""),
        "fmt_days": float(f["days_per_year"]),
        "days": float(f["days_per_year"]) - float(mkt.get("closed_days_per_year", 0)),
        "design_index": float(f["design_index"]),
        "fixed_share": float(f.get("fixed_share", lab["fixed_share"])),
        "hero_name": book.products[hero]["name"] if hero in book.products else None,
        "burden_pct": float(mkt.get("burden_pct", lab["burden_pct"])),
        "utilities_psf": float(mkt.get("utilities_per_sqft_year", cfg["utilities_per_sqft_year"])),
        "price_index": float(mkt.get("price_index", 1.0)),
        "managed": bool(f.get("manager", True)),
        "manager_salary": float(mkt.get("manager_salary", lab["manager"]["salary"])),
        "owner_pay_target": float(f.get("owner_pay_target", 0)),
        "roles": roles,
        # The plan's stress test: a third baker working the Baker's hours again.
        "extra_baker": {"role": "Baker", "hours": float(next(r["hours"] for r in base["roles"] if r["role"] == "Baker"))} if baker else None,
        "channels": channels,
        "var_costs": {**cfg["variable_costs_pct_of_sales"], **(f.get("variable_costs_pct_of_sales") or {})},
        "fixed_costs": {**cfg["fixed_costs_per_year"], **(f.get("fixed_costs_per_year") or {}), **(mkt.get("fixed_costs_per_year") or {})},
        "st": {**cfg["startup"], **(f.get("startup") or {}), **(mkt.get("startup") or {})},
        "startup_fees": {**(f.get("startup_fees") or {}), **(mkt.get("startup_fees") or {})},
        "equipment": [{"item": e["item"], "cost": float(e["cost"])} for e in cfg["equipment"][fid]],
        "space": [{"zone": z["zone"], "sqft": float(z["sqft"])} for z in cfg["space_program"][fid]],
        "fin": {**cfg["financing"], **(f.get("financing") or {})},
        "index_gain": float(growth.get("index_gain", 0)),
        "growth_of": growth.get("of"),
        "growth_note": growth.get("note", ""),
    }


SITE_NUMBERS = ("sqft", "seats", "rent_psf", "nnn_psf", "escalation_pct", "buildout_psf", "sales_index")
SITE_OPTIONAL = ("soft_costs_pct", "equipment_credit", "purchase_price", "months_to_open")
SITE_TEXT = ("id", "name", "short", "area", "format", "kitchen", "rent_basis", "risks", "source", "space_note",
             "equipment_credit_note")


def build_data(book: Book) -> tuple[dict, dict]:
    """The page's data, and the config (with growth formats) it came from."""
    cfg = proforma.load()
    errors = proforma.validate(cfg)
    if errors:
        raise DBError("; ".join(errors))
    cfg = with_growth(cfg)
    errors = proforma.validate(cfg)
    if errors:
        raise DBError("growth_case: " + "; ".join(errors))
    mkt = (cfg.get("markets") or {}).get(MARKET) or {}
    sites = [s for s in cfg["sites"] if proforma.market_id(s) == MARKET]
    if not sites:
        raise DBError(f"proforma.yaml has no sites in the '{MARKET}' market")
    op = cfg["operating"]
    products: dict[str, dict] = {}
    stages = [st for st in STAGES if st["format"] in cfg["labor"]["formats"]]
    formats = {}
    for st in stages:
        base = st["format"].removesuffix(GROWTH)
        if not any(s["format"] == base for s in sites):
            raise DBError(f"no Miami site uses the format '{base}'")
        formats[st["format"]] = export_format(book, cfg, st["format"], mkt, products)
    out_sites = []
    for s in sites:
        row = {k: s.get(k, "") for k in SITE_TEXT}
        row.update({k: float(s[k]) for k in SITE_NUMBERS})
        row.update({k: float(s[k]) for k in SITE_OPTIONAL if k in s})
        row["rent_flat"] = float(s.get("rent_flat_per_year", 0))
        row["rent_assumed"] = bool(s.get("rent_assumed", False))
        out_sites.append(row)
    data = {
        "as_of": str(cfg.get("as_of", "")),
        "market": mkt.get("label", MARKET),
        "op": {"ramp": sum(op["ramp_year1_pct"]) / len(op["ramp_year1_pct"]) / 100, "infl": float(op["cost_inflation_pct"]) / 100,
               "growth": float(op["price_growth_pct"]) / 100, "cogs_buffer": float(op["cogs_buffer_pts"])},
        "manager_hire": {"salary": MANAGER_HIRE},
        "scenarios": [{"id": sc["id"], "name": sc["name"], "factor": float(sc["sales_factor"])} for sc in cfg["scenarios"]],
        "products": products,
        "formats": formats,
        "sites": out_sites,
        "stages": [{**st, "sites": [s["id"] for s in sites if s["format"] == st["format"].removesuffix(GROWTH)]} for st in stages],
        "gates": GATES,
    }
    return data, cfg


# -- the port against the Python model ----------------------------------------

LINES = ("cogs", "hourly_labor", "manager", "rent", "nnn", "utilities", "variable_opex", "channel_costs", "fixed_opex")


def py_case(book: Book, cfg: dict, fid: str, site: dict, factor: float = 1.0) -> dict:
    f = cfg["labor"]["formats"][fid]
    gain = float((f.get("growth") or {}).get("index_gain", 0))
    site = dict(site, format=fid, sales_index=float(site["sales_index"]) + gain)
    menu = proforma.format_menu(book, f, float(site["sales_index"]))
    sc = {"id": "x", "sales_factor": factor}
    r = proforma.model(cfg, menu, site, sc)
    r["rent_ceiling_psf"] = proforma.rent_ceiling(cfg, menu, site, sc)
    return r


def reference_cases(book: Book, cfg: dict, data: dict) -> list[dict]:
    """Cases the port must reproduce: each stage, site and scenario, then one case per lever."""
    sites = {s["id"]: s for s in cfg["sites"]}
    cases = []

    def add(label, fid, sid, state, r, breakeven=True):
        cases.append({"label": label, "format": fid, "site": sid, "state": state, "breakeven": breakeven, "want": {
            "years": [{**{k: y[k] for k in LINES}, "sales": y["sales"], "left": y["cash_after_debt"], "hours_day": y["hours_day"]}
                      for y in r["years"]],
            "startup": r["startup"], "breakeven_sales": r["breakeven_sales"], "rent_ceiling_psf": r["rent_ceiling_psf"],
            "orders_daily": r["orders_daily"], "hero_daily": r["hero_units_daily"],
            "startup_lines": r["startup_lines"]}})

    for st in data["stages"]:
        fid = st["format"]
        ids = [c["id"] for c in data["formats"][fid]["channels"]]
        for sid in st["sites"]:
            for sc in data["scenarios"]:
                add(f"{st['id']} at {sid}, {sc['id']}", fid, sid, {"v": {c: sc["factor"] for c in ids}},
                    py_case(book, cfg, fid, sites[sid], sc["factor"]))

    def variant(fid, fn):
        c = copy.deepcopy(cfg)
        fn(c["labor"]["formats"][fid], c)
        return c

    def scale(cid, k):
        def fn(f, _c):
            ch = next(x for x in f["channels"] if x["id"] == cid)
            ch["menu"] = {p: v * k for p, v in ch["menu"].items()}
        return fn

    def drop(cid):
        def fn(f, _c):
            f["channels"] = [x for x in f["channels"] if x["id"] != cid]
        return fn

    def baker(f, _c):
        for r in f["roles"]:
            if r["role"] == "Baker":
                r["hours"] *= 2

    def reprice(k):
        def fn(f, _c):
            f["prices"] = {p: round(v * k, 2) for p, v in f["prices"].items()}
        return fn

    def one_price(pid, price):
        def fn(f, _c):
            f["prices"] = dict(f["prices"], **{pid: price})
        return fn

    def wages(k):
        def fn(f, c):
            for r in f["roles"]:
                if "wage" in r:
                    r["wage"] *= k
            m = c["markets"][MARKET]
            m["wages"] = {role: w * k for role, w in (m.get("wages") or {}).items()}
        return fn

    def food(pts):
        def fn(_f, c):
            c["operating"]["cogs_buffer_pts"] += pts
        return fn

    K, P = "roll_kitchen", "roll_popup"
    hub = next(s for s in data["stages"] if s["format"] == K)["sites"][0]
    pop = next(s for s in data["stages"] if s["format"] == P)["sites"][0]
    held = {"flex": False}
    add("window index 0.5", K, hub, {"index": 0.5}, py_case(book, cfg, K, dict(sites[hub], sales_index=0.5)))
    for label, fid, sid, state, c, s in [
        ("markets at half, crew held", K, hub, {"v": {"markets": 0.5}, **held}, variant(K, scale("markets", 0.5)), sites[hub]),
        ("no apps, crew held", K, hub, {"v": {"apps": 0}, **held}, variant(K, drop("apps")), sites[hub]),
        ("no fundraisers, crew held", K, hub, {"v": {"fundraisers": 0}, **held}, variant(K, drop("fundraisers")), sites[hub]),
        ("a third baker", K, hub, {"baker": True}, variant(K, baker), sites[hub]),
        ("prices up 5%", K, hub, {"price": 1.05}, variant(K, reprice(1.05)), sites[hub]),
        ("prices down 5%", K, hub, {"price": 0.95}, variant(K, reprice(0.95)), sites[hub]),
        ("the roll at $5.75", K, hub, {"prices": {"cinnamon_roll": 5.75}}, variant(K, one_price("cinnamon_roll", 5.75)), sites[hub]),
        ("wages up 10%", K, hub, {"wage": 1.1}, variant(K, wages(1.1)), sites[hub]),
        ("food up 3 points", K, hub, {"food": 3}, variant(K, food(3)), sites[hub]),
        ("rent $75 + $18", K, hub, {"rent": 75, "nnn": 18}, cfg, dict(sites[hub], rent_psf=75, nnn_psf=18)),
        ("pop-up markets at 60%, crew held", P, pop, {"v": {"markets": 0.6}, **held}, variant(P, scale("markets", 0.6)), sites[pop]),
        ("commissary at $4,000 a month", P, pop, {"flat": 48000}, cfg, dict(sites[pop], rent_flat_per_year=48000)),
    ]:
        add(label, fid, sid, state, py_case(book, c, fid, s), breakeven="flex" not in state)
    return cases


CHECK_JS = r"""
const fs = require("fs");
const MiamiModel = require(process.argv[2]);
const D = JSON.parse(fs.readFileSync(process.argv[3], "utf8"));
const cases = JSON.parse(fs.readFileSync(process.argv[4], "utf8"));
const M = MiamiModel(D);
const sites = Object.fromEntries(D.sites.map(s => [s.id, s]));
const bad = [];
const near = (a, b, tol) => (a == null && b == null) || (a != null && b != null && Math.abs(a - b) <= tol);
for (const c of cases) {
  const r = M.run(c.format, sites[c.site], c.state), w = c.want;
  const miss = (what, got, want, tol) => { if (!near(got, want, tol)) bad.push(`${c.label}: ${what} ${got} != ${want}`); };
  w.years.forEach((y, i) => {
    for (const k of Object.keys(y)) miss(`year ${i + 1} ${k}`, r.years[i][k], y[k], k === "hours_day" ? 1e-6 : 0.01);
  });
  miss("startup", r.startup, w.startup, 0.01);
  const lines = Object.fromEntries(r.startup_lines);
  for (const k of Object.keys(w.startup_lines)) miss(`startup line ${k}`, lines[k], w.startup_lines[k], 0.01);
  if (c.breakeven) miss("break-even", r.breakeven_sales, w.breakeven_sales, 0.01);
  miss("rent ceiling", r.rent_ceiling_psf, w.rent_ceiling_psf, 0.001);
  miss("orders a day", r.orders_daily, w.orders_daily, 1e-6);
  miss("hero units a day", r.hero_daily, w.hero_daily, 1e-6);
}
console.log(JSON.stringify({cases: cases.length, bad}));
"""


def check_model(book: Book, cfg: dict, data: dict) -> tuple[bool, str]:
    """Run tools/miami_model.js against tools/proforma.py. Returns (ok, message)."""
    node = shutil.which("node")
    if not node:
        return True, "warning: Node.js not found, so the page's model was not checked against tools/proforma.py"
    cases = reference_cases(book, cfg, data)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "data.json").write_text(json.dumps(data), encoding="utf-8")
        (tmp / "cases.json").write_text(json.dumps(cases), encoding="utf-8")
        (tmp / "check.js").write_text(CHECK_JS, encoding="utf-8")
        run = subprocess.run([node, str(tmp / "check.js"), str(MODEL_JS), str(tmp / "data.json"), str(tmp / "cases.json")],
                             capture_output=True, text=True)
    if run.returncode != 0:
        return False, "error: the model check did not run: " + run.stderr.strip()
    result = json.loads(run.stdout)
    if result["bad"]:
        shown = "\n  ".join(result["bad"][:12])
        more = f"\n  and {len(result['bad']) - 12} more" if len(result["bad"]) > 12 else ""
        return False, f"error: tools/miami_model.js disagrees with tools/proforma.py:\n  {shown}{more}"
    return True, f"model check: {result['cases']} cases match tools/proforma.py"


# -- the page -----------------------------------------------------------------

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


def render_body(data: dict) -> str:
    page = PAGE_HTML.read_text(encoding="utf-8")
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    model = MODEL_JS.read_text(encoding="utf-8").replace("</", "<\\/")
    for mark in ("__DATA__", "__MODEL__"):
        if page.count(mark) != 1:
            raise DBError(f"tools/miami_page.html must contain {mark} exactly once")
    return page.replace("__MODEL__", model).replace("__DATA__", blob)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--body-only", type=Path, help="also write the page body to this path")
    parser.add_argument("--check", action="store_true", help="check the model only; write nothing")
    args = parser.parse_args()
    try:
        book = Book()
        errors, _ = book.validate()
        if errors:
            for error in errors:
                print(f"error: {error}", file=sys.stderr)
            return 1
        data, cfg = build_data(book)
        ok, message = check_model(book, cfg, data)
        print(message, file=sys.stderr if not ok or message.startswith("warning") else sys.stdout)
        if not ok:
            return 1
        if args.check:
            return 0
        body = render_body(data)
    except (DBError, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    OUT.write_text(STANDALONE.format(body=body), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    if args.body_only:
        args.body_only.write_text(body, encoding="utf-8")
        print(f"wrote {args.body_only}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
