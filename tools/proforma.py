#!/usr/bin/env python3
"""Build the bakery pro forma: space, startup cost and three years of P&L per site and scenario.

Usage:
    python3 tools/proforma.py           # validate, then write db/proforma.md
    python3 tools/proforma.py --check   # validate only; exit 1 on any error

Reads db/proforma.yaml and, through tools/costing.py, the menu database. Each
format (bakery-café, roll bakery) has a design day built from product volumes:
its sales, its food-and-packaging cost and its hands-on prep hours. Requires PyYAML.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from costing import DB, ROOT, Book, DBError  # noqa: E402

PROFORMA = DB / "proforma.yaml"
REPORT = DB / "proforma.md"
CHANNEL = "distributor_est"  # pro forma food costs assume distributor buying

REQUIRED = ("operating", "variable_costs_pct_of_sales", "fixed_costs_per_year", "utilities_per_sqft_year",
            "labor", "space_program", "equipment", "startup", "financing", "scenarios", "sites")
SITE_FIELDS = ("id", "name", "format", "sqft", "seats", "rent_psf", "nnn_psf", "escalation_pct",
               "buildout_psf", "sales_index")
DEFAULT_MARKET = "boston"  # a site without a `market` uses the file's own inputs, which are Boston's
MARKET_NUMBERS = ("burden_pct", "utilities_per_sqft_year", "price_index", "closed_days_per_year", "manager_salary")


def market_id(site: dict) -> str:
    return site.get("market", DEFAULT_MARKET)


def market(cfg: dict, site: dict) -> dict:
    """The site's market overrides: wages by role, payroll burden, utilities, fixed costs, prices and fees."""
    return (cfg.get("markets") or {}).get(market_id(site)) or {}


def load() -> dict:
    if not PROFORMA.exists():
        raise DBError("db/proforma.yaml is missing")
    return yaml.safe_load(PROFORMA.read_text(encoding="utf-8")) or {}


def is_number(value, minimum: float = 0) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= minimum


def validate(cfg: dict) -> list[str]:
    errors = [f"proforma.yaml: missing '{key}'" for key in REQUIRED if key not in cfg]
    if errors:
        return errors
    formats = cfg["labor"].get("formats") or {}
    for fmt, f in formats.items():
        where = f"proforma.yaml: format {fmt}"
        if fmt not in cfg["equipment"] or fmt not in cfg["space_program"]:
            errors.append(f"{where}: needs equipment and space_program entries")
        paid = [r for r in f.get("roles") or [] if not r.get("owner")]
        if not paid:
            errors.append(f"{where}: needs at least one paid role")
        errors += [f"{where}: role '{r.get('role', '?')}' needs hours and a wage"
                   for r in paid if not is_number(r.get("hours")) or not is_number(r.get("wage"))]
        errors += [f"{where}: menu volume for '{pid}' must be a number of 0 or more"
                   for pid, par in (f.get("menu") or {}).items() if not is_number(par)]
        errors += [f"{where}: price for '{pid}' must be a positive number"
                   for pid, price in (f.get("prices") or {}).items() if not is_number(price, 0.01)]
        for c in f.get("channels") or []:
            cw = f"{where}: channel {c.get('id', '?')}"
            if not c.get("id") or not c.get("name") or not isinstance(c.get("menu"), dict):
                errors.append(f"{cw}: needs an id, a name and a menu")
                continue
            errors += [f"{cw}: {key} must be a number of 0 or more"
                       for key in ("days_per_year", "cost_pct_of_sales", "fee_per_day")
                       if (key == "days_per_year" or key in c) and not is_number(c.get(key))]
            errors += [f"{cw}: menu volume for '{pid}' must be a number of 0 or more"
                       for pid, par in c["menu"].items() if not is_number(par)]
            if "price_index" in c and not is_number(c["price_index"], 0.01):
                errors.append(f"{cw}: price_index must be positive")
        if f.get("channels") and not is_number(f.get("days_per_year"), 1):
            errors.append(f"{where}: a format with channels needs its own days_per_year")
        if "fixed_share" in f and not (is_number(f["fixed_share"]) and f["fixed_share"] <= 1):
            errors.append(f"{where}: fixed_share must be between 0 and 1")
        if not is_number(f.get("items_per_order", 2.0), 0.1):
            errors.append(f"{where}: items_per_order must be a positive number")
    markets = cfg.get("markets") or {}
    for mid, m in markets.items():
        where = f"proforma.yaml: market {mid}"
        errors += [f"{where}: {key} must be a number of 0 or more"
                   for key in MARKET_NUMBERS if key in m and not is_number(m[key])]
        errors += [f"{where}: wage for '{role}' must be a number of 0 or more"
                   for role, w in (m.get("wages") or {}).items() if not is_number(w)]
        errors += [f"{where}: {group} line '{k}' must be a number of 0 or more"
                   for group in ("fixed_costs_per_year", "startup", "startup_fees")
                   for k, v in (m.get(group) or {}).items() if not is_number(v)]
        if "price_index" in m and not is_number(m["price_index"], 1e-9):
            errors.append(f"{where}: price_index must be positive")
    for site in cfg["sites"]:
        where = f"proforma.yaml: site {site.get('id', '?')}"
        errors += [f"{where}: missing '{f}'" for f in SITE_FIELDS if f not in site]
        if site.get("format") not in formats:
            errors.append(f"{where}: format '{site.get('format')}' is not under labor.formats")
        if "market" in site and site["market"] not in markets:
            errors.append(f"{where}: market '{site['market']}' is not under markets")
        if "rent_assumed" in site and not isinstance(site["rent_assumed"], bool):
            errors.append(f"{where}: rent_assumed must be true or false")
        errors += [f"{where}: {key} must be a number of 0 or more"
                   for key in ("months_to_open", "soft_costs_pct", "equipment_credit", "purchase_price", "rent_flat_per_year")
                   if key in site and not is_number(site[key])]
    if len(cfg["operating"].get("ramp_year1_pct") or []) != 12:
        errors.append("proforma.yaml: operating.ramp_year1_pct needs 12 monthly values")
    for sc in cfg["scenarios"]:
        if not is_number(sc.get("sales_factor"), 1e-9):
            errors.append(f"proforma.yaml: scenario {sc.get('id', '?')} needs a positive sales_factor")
    return errors


def hero_units(book: Book, volumes: dict, hero: str | None) -> float:
    """Units of the hero product sold a day, counting those inside boxes and packs."""
    if not hero:
        return 0.0

    def inside(pid: str, depth: int = 0) -> float:
        if pid == hero:
            return 1.0
        doc = book.products.get(pid)
        if doc is None or depth > 4:
            return 0.0
        return sum(float(line["qty"]) * inside(line["item"], depth + 1)
                   for line in doc["build"] if line["item"] in book.products)

    return sum(float(par) * inside(pid) for pid, par in volumes.items())


def menu_day(book: Book, volumes: dict | None = None, items_per_order: float = 2.0, hero: str | None = None,
             prices: dict | None = None, at_scale: bool = False, price_index: float = 1.0) -> dict:
    """A format's design day: sales, food cost, prep hours and an estimated order count.

    `volumes` maps product ids to units a day; without it, every product's par_daily is used.
    `prices` replaces a product's suggested retail price for this format only, and `price_index`
    marks every price up or down (a delivery-app menu). `at_scale` counts prep minutes at the
    database's production-kitchen batch sizes.
    """
    prices = prices or {}
    if volumes is None:
        volumes = {pid: float(doc.get("par_daily") or 0) for pid, doc in book.products.items()}
    sales = goods = hours = items = 0.0
    by_category: dict[str, float] = {}
    for pid, par in volumes.items():
        if pid not in book.products:
            raise DBError(f"proforma.yaml: a format's menu lists '{pid}', which is not a product")
        doc, par = book.products[pid], float(par)
        price = float(prices.get(pid, doc["pricing"].get("suggested_retail_usd") or 0)) * price_index
        sales += price * par
        goods += (book.product_cost(pid, CHANNEL) or 0) * par
        hours += book.product_labor(pid, at_scale=at_scale) * par / 60
        by_category[doc["category"]] = by_category.get(doc["category"], 0) + price * par
        if doc["category"] != "add-on":  # a milk swap or a scoop rides on another item
            items += par
    if not sales or not items:
        raise DBError("a format's menu has no volumes, so there are no sales to project")
    orders = items / items_per_order
    return {
        "sales": sales,
        "goods_pct": 100 * goods / sales,
        "hands_on_hours": hours,
        "by_category": by_category,
        "items": items,
        "orders": orders,
        "ticket": sales / orders,
        "hero_units": hero_units(book, volumes, hero),
        "hero_name": book.products[hero]["name"] if hero in book.products else None,
    }


def format_menu(book: Book, f: dict, site_index: float = 1.0) -> dict:
    """A format's design day; for a format with sales channels, its average operating day at a site.

    Each channel has its own menu for a day it trades and the number of days a year it trades; they are
    averaged over the format's operating days. A channel with scales_with_site: false (a market stall,
    office orders) sells the same wherever the kitchen is; the others scale with the site's sales index.
    `sales` stays at the index-1.0 design day and `eff_index` is the site's blended index, so
    sales × eff_index is the site's average operating day.
    """
    ipo = float(f.get("items_per_order", 2.0))
    at_scale = bool(f.get("production_scale"))
    if not f.get("channels"):
        return menu_day(book, f.get("menu"), ipo, f.get("hero"), f.get("prices"), at_scale)
    days = float(f["days_per_year"])
    base = site = goods = hours = items = orders = hero = costs = fees = 0.0
    by_category: dict[str, float] = {}
    channels = []
    for c in f["channels"]:
        m = menu_day(book, c["menu"], float(c.get("items_per_order", ipo)), f.get("hero"),
                     {**(f.get("prices") or {}), **(c.get("prices") or {})}, at_scale, float(c.get("price_index", 1.0)))
        w = float(c["days_per_year"]) / days  # channel days per operating day
        k = site_index if c.get("scales_with_site", True) else 1.0
        cost_pct = float(c.get("cost_pct_of_sales", 0))
        base += m["sales"] * w
        site += m["sales"] * w * k
        goods += m["sales"] * m["goods_pct"] / 100 * w * k
        hours += m["hands_on_hours"] * w * k
        items += m["items"] * w * k
        orders += m["orders"] * w * k
        hero += m["hero_units"] * w * k
        costs += m["sales"] * w * k * cost_pct / 100
        fees += float(c.get("fee_per_day", 0)) * float(c["days_per_year"])
        for cat, v in m["by_category"].items():
            by_category[cat] = by_category.get(cat, 0) + v * w * k
        channels.append({"id": c["id"], "name": c["name"], "days": float(c["days_per_year"]),
                         "day_sales": m["sales"] * k, "day_orders": m["orders"] * k, "ticket": m["ticket"],
                         "weight": m["sales"] * w * k, "cost_pct": cost_pct, "fee_per_day": float(c.get("fee_per_day", 0)),
                         "scales_with_site": bool(c.get("scales_with_site", True)), "note": c.get("note", "")})
    if not base or not orders:
        raise DBError("a format's channels have no volumes, so there are no sales to project")
    for ch in channels:
        ch["share"] = ch.pop("weight") / site
    eff = site / base
    return {
        "sales": base,
        "eff_index": eff,
        "goods_pct": 100 * goods / site,
        "hands_on_hours": hours,
        "by_category": by_category,
        "items": items,
        "orders": orders,
        "ticket": site / orders,
        "hero_units": hero / eff,
        "hero_name": book.products[f["hero"]]["name"] if f.get("hero") in book.products else None,
        "channels": channels,
        "channel_cost_pct": 100 * costs / site,
        "channel_fees_year": fees,
    }


def annual_payment(principal: float, rate_pct: float, years: float) -> float:
    r, n = rate_pct / 100 / 12, years * 12
    if principal <= 0:
        return 0.0
    if r == 0:
        return principal / years
    return 12 * principal * r / (1 - (1 + r) ** -n)


def crew(cfg: dict, fmt: str, mkt: dict | None = None) -> dict:
    """Paid crew hours a day and their average wage at the format's design volume, plus the owner's hours.

    A market's `wages` replace the format's wage for each role it names.
    """
    roles = cfg["labor"]["formats"][fmt]["roles"]
    local = (mkt or {}).get("wages") or {}
    paid = [r for r in roles if not r.get("owner")]
    pay = {r["role"]: float(local.get(r["role"], r["wage"])) for r in paid}
    hours = sum(float(r["hours"]) for r in paid)
    total = sum(float(r["hours"]) * pay[r["role"]] for r in paid)
    return {"hours": hours, "avg_wage": total / hours, "wages": pay,
            "owner_hours": sum(float(r["hours"]) for r in roles if r.get("owner"))}


def owner_target(fmt_cfg: dict) -> float:
    """What an owner-run format should leave its owner; 0 where a hired manager runs the shop."""
    return 0.0 if fmt_cfg.get("manager", True) else float(fmt_cfg.get("owner_pay_target", 0))


def model(cfg: dict, menu: dict, site: dict, scenario: dict) -> dict:
    op, lab = cfg["operating"], cfg["labor"]
    fmt_cfg = lab["formats"][site["format"]]
    mkt = market(cfg, site)  # local overrides; empty for the file's own (Boston) inputs
    fin = {**cfg["financing"], **(fmt_cfg.get("financing") or {})}
    st = {**cfg["startup"], **(fmt_cfg.get("startup") or {}), **(mkt.get("startup") or {})}
    fixed_costs = {**cfg["fixed_costs_per_year"], **(fmt_cfg.get("fixed_costs_per_year") or {}),
                   **(mkt.get("fixed_costs_per_year") or {})}
    days = float(fmt_cfg.get("days_per_year", op["days_per_year"])) - float(mkt.get("closed_days_per_year", 0))
    team = crew(cfg, site["format"], mkt)
    base_hours, wage = team["hours"], team["avg_wage"]
    burden_pct = float(mkt.get("burden_pct", lab["burden_pct"]))
    burden = 1 + burden_pct / 100
    utilities_psf = float(mkt.get("utilities_per_sqft_year", cfg["utilities_per_sqft_year"]))
    price = float(mkt.get("price_index", 1.0))  # local menu prices as a share of the database's
    fixed_share = float(fmt_cfg.get("fixed_share", lab["fixed_share"]))
    ramp = sum(op["ramp_year1_pct"]) / len(op["ramp_year1_pct"]) / 100
    infl = float(op["cost_inflation_pct"]) / 100
    growth = float(op["price_growth_pct"]) / 100
    # Share of the format's design day. A format with channels blends the site's index over the
    # channels that depend on the location (format_menu's eff_index).
    level = float(menu.get("eff_index", site["sales_index"])) * float(scenario["sales_factor"])
    steady = menu["sales"] * price * level * days
    goods_pct = menu["goods_pct"] / price + float(op["cogs_buffer_pts"])
    var_costs = {**cfg["variable_costs_pct_of_sales"], **(fmt_cfg.get("variable_costs_pct_of_sales") or {})}
    var_pct = sum(float(v) for v in var_costs.values())
    channel_pct = float(menu.get("channel_cost_pct", 0))    # commissions and shares paid on channel sales
    channel_fees = float(menu.get("channel_fees_year", 0))  # stall fees, paid whatever the sales
    fixed_base = sum(float(v) for v in fixed_costs.values())
    sqft = float(site["sqft"])
    flat_rent = float(site.get("rent_flat_per_year", 0))    # a commissary or a licence, not priced by area
    managed = bool(fmt_cfg.get("manager", True))
    manager_base = float(mkt.get("manager_salary", lab["manager"]["salary"])) * burden if managed else 0.0

    def year(n: int) -> dict:
        vol = ramp if n == 1 else 1.0
        sales = steady * vol * ((1 + growth) if n == 3 else 1.0)
        mult = (1 + infl) ** (n - 1)
        ratio = level * vol / float(fmt_cfg["design_index"])
        hours_day = base_hours * (fixed_share + (1 - fixed_share) * ratio)
        lines = {
            "cogs": sales * goods_pct / 100,
            "hourly_labor": hours_day * wage * burden * days * mult,
            "manager": manager_base * mult,
            "rent": (sqft * float(site["rent_psf"]) + flat_rent) * (1 + float(site["escalation_pct"]) / 100) ** (n - 1),
            "nnn": sqft * float(site["nnn_psf"]) * mult,
            "utilities": sqft * utilities_psf * mult,
            "variable_opex": sales * var_pct / 100,
            "channel_costs": sales * channel_pct / 100 + channel_fees * mult,
            "fixed_opex": fixed_base * mult,
        }
        ebitda = sales - sum(lines.values())
        return {"year": n, "sales": sales, "daily_sales": sales / days, "hours_day": hours_day, **lines,
                "ebitda": ebitda}

    years = [year(1), year(2), year(3)]
    y1 = years[0]

    # Startup cost
    equipment = sum(float(e["cost"]) for e in cfg["equipment"][site["format"]]) - float(site.get("equipment_credit", 0))
    buildout = sqft * float(site["buildout_psf"])
    occupancy_month = (y1["rent"] + y1["nnn"]) / 12
    monthly_fixed = (y1["rent"] + y1["nnn"] + y1["hourly_labor"] + y1["manager"] + y1["utilities"] + y1["fixed_opex"]) / 12
    startup_lines = {
        "Build-out": buildout,
        "Design, engineering, permits and legal": buildout * float(site.get("soft_costs_pct", st["soft_costs_pct_of_buildout"])) / 100,
        "Equipment": equipment,
        **({"Purchase of the existing fit-out and lease": float(site["purchase_price"])} if site.get("purchase_price") else {}),
        "Furniture and fixtures": float(site["seats"]) * float(st["furniture_per_seat"]) + float(st["furniture_base"]),
        "Signage": float(st["signage"]),
        "Pre-opening payroll and training": (base_hours * 0.6 * wage * burden * 7 * float(st["preopening_payroll_weeks"])
                                             + manager_base / 52 * float(st.get("manager_preopening_weeks", 0))),
        "Opening inventory": float(st["opening_inventory"]),
        "Launch marketing": float(st["launch_marketing"]),
        **{label: float(v) for label, v in {**(fmt_cfg.get("startup_fees") or {}), **(mkt.get("startup_fees") or {})}.items()},
        "Security deposit": occupancy_month * float(st["deposit_months"]),
        "Rent and NNN before opening": occupancy_month * float(site.get("months_to_open", 0)),
        "Contingency": (buildout + equipment) * float(st["contingency_pct"]) / 100,
        "Working capital reserve": monthly_fixed * float(st["working_capital_months"]),
    }
    startup = sum(startup_lines.values())
    loan = startup * float(fin["loan_share_pct"]) / 100
    equity = startup - loan
    debt_service = annual_payment(loan, float(fin["rate_pct"]), float(fin["term_years"]))
    for y in years:
        y["debt_service"] = debt_service
        y["cash_after_debt"] = y["ebitda"] - debt_service
        y["owner_earnings"] = y["ebitda"] + y["manager"]

    # Break-even on Year-2 costs: sales where cash after debt service is zero.
    y2 = years[1]
    design_sales = menu["sales"] * price * float(fmt_cfg["design_index"]) * days
    crew_cost = base_hours * wage * burden * days * (1 + infl)
    fixed_cash = (y2["manager"] + y2["rent"] + y2["nnn"] + y2["utilities"] + y2["fixed_opex"]
                  + channel_fees * (1 + infl) + crew_cost * fixed_share)
    var_rate = (goods_pct + var_pct + channel_pct) / 100 + crew_cost * (1 - fixed_share) / design_sales
    breakeven = (fixed_cash + debt_service) / (1 - var_rate)
    breakeven_ebitda = fixed_cash / (1 - var_rate)
    target = owner_target(fmt_cfg)
    target_daily = (fixed_cash + debt_service + target) / (1 - var_rate) / days if target else None

    y3 = years[2]
    reserve = startup_lines["Working capital reserve"]
    ticket = menu["ticket"] * price
    return {
        "site": site["id"],
        "scenario": scenario["id"],
        "format": site["format"],
        "market": market_id(site),
        "days": days,
        "managed": managed,
        "wages": team["wages"],
        "avg_wage": wage,
        "burden_pct": burden_pct,
        "utilities_psf": utilities_psf,
        "price_index": price,
        "fixed_costs": fixed_costs,
        "variable_costs": var_costs,
        "fixed_share": fixed_share,
        "no_premises": sqft <= 0,
        "flat_rent": flat_rent,
        "channels": [{**ch, "sales_year": steady * ch["share"], "day_sales": ch["day_sales"] * price * float(scenario["sales_factor"])}
                     for ch in menu.get("channels") or []],
        "steady_sales": steady,
        "steady_daily": steady / days,
        "ticket": ticket,
        "orders_daily": steady / days / ticket,
        "hero_units_daily": menu["hero_units"] * level,
        "years": years,
        "startup_lines": startup_lines,
        "startup": startup,
        "loan": loan,
        "equity": equity,
        "debt_service": debt_service,
        "return_on_cash_y2": y2["cash_after_debt"] / equity if equity else None,
        "owner_cash_limit": fin.get("owner_cash_limit"),
        "over_cash_limit": bool(fin.get("owner_cash_limit")) and equity > float(fin["owner_cash_limit"]),
        "breakeven_sales": breakeven,
        "breakeven_daily": breakeven / days,
        "breakeven_orders_daily": breakeven / days / ticket,
        "breakeven_ebitda_daily": breakeven_ebitda / days,
        "breakeven_vs_steady": breakeven / steady if steady else None,
        "owner_pay_target": target or None,
        "owner_target_daily": target_daily,
        "owner_target_orders_daily": target_daily / ticket if target_daily else None,
        "payback_years": startup / y3["ebitda"] if y3["ebitda"] > 0 else None,
        "cash_on_cash_y3": y3["cash_after_debt"] / equity if equity else None,
        "rent_pct_y2": 100 * (y2["rent"] + y2["nnn"]) / y2["sales"] if y2["sales"] else None,
        "base_rent_pct_y2": 100 * y2["rent"] / y2["sales"] if y2["sales"] else None,
        "per_extra_100_daily": (1 - var_rate) * 100 * days,
        "reserve": reserve,
        "reserve_covers_year1": y1["cash_after_debt"] >= -reserve,
        "sales_per_labor_hour_y2": y2["daily_sales"] / y2["hours_day"] if y2["hours_day"] else None,
    }


def rent_ceiling(cfg: dict, menu: dict, site: dict, scenario: dict) -> float | None:
    """The most base rent per sq ft the site can carry in Year 2, other inputs fixed.

    A managed format must still cover its loan; an owner-run one must also leave the owner's target pay.
    """
    target = owner_target(cfg["labor"]["formats"][site["format"]])
    if float(site["sqft"]) <= 0:  # no leased area to price
        return None

    def spare(rent: float) -> float:
        return model(cfg, menu, dict(site, rent_psf=rent), scenario)["years"][1]["cash_after_debt"] - target

    lo, hi = 0.0, 400.0
    if spare(lo) <= 0:
        return None
    if spare(hi) > 0:
        return hi
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if spare(mid) > 0 else (lo, mid)
    return lo


def build(book: Book | None = None) -> dict:
    """Everything the report and the viewer need."""
    book = book or Book()
    cfg = load()
    errors = validate(cfg)
    if errors:
        raise DBError("; ".join(errors))
    formats = cfg["labor"]["formats"]
    menus = {fmt: format_menu(book, f) for fmt, f in formats.items()}
    results: dict[str, dict] = {}
    for s in cfg["sites"]:
        f = formats[s["format"]]
        menu = format_menu(book, f, float(s["sales_index"])) if f.get("channels") else menus[s["format"]]
        results[s["id"]] = {}
        for sc in cfg["scenarios"]:
            r = model(cfg, menu, s, sc)
            r["rent_ceiling_psf"] = rent_ceiling(cfg, menu, s, sc)
            results[s["id"]][sc["id"]] = r
    return {"config": cfg, "menus": menus, "results": results, "crews": {fmt: crew(cfg, fmt) for fmt in formats},
            "market_crews": {mid: {fmt: crew(cfg, fmt, m) for fmt in formats}
                             for mid, m in (cfg.get("markets") or {}).items()}}


# -- report ------------------------------------------------------------------

def usd(value: float | None, k: bool = False) -> str:
    if value is None:
        return "n/a"
    if k:
        return f"−${-value / 1000:,.0f}K" if value < 0 else f"${value / 1000:,.0f}K"
    return f"−${-value:,.0f}" if value < 0 else f"${value:,.0f}"


def pct(part: float | None, whole: float | None) -> str:
    return "n/a" if part is None or not whole else f"{100 * part / whole:.0f}%".replace("-", "−")


LINE_LABELS = [
    ("cogs", "Food and packaging"),
    ("hourly_labor", "Hourly crew, with payroll taxes"),
    ("manager", "General manager, with payroll taxes"),
    ("rent", "Base rent"),
    ("nnn", "NNN charges"),
    ("utilities", "Utilities"),
    ("variable_opex", "Card fees, repairs, supplies, marketing, delivery, other"),
    ("channel_costs", "Delivery commissions, fundraiser shares and market fees"),
    ("fixed_opex", "Insurance, software, accounting, licenses, waste, linens, phone"),
]


def market_label(cfg: dict, mid: str) -> str:
    return ((cfg.get("markets") or {}).get(mid) or {}).get("label") or ("Boston area" if mid == DEFAULT_MARKET else mid)


def render(data: dict) -> str:
    cfg, menus, results = data["config"], data["menus"], data["results"]
    sites = {s["id"]: s for s in cfg["sites"]}
    markets = cfg.get("markets") or {}
    # Sites in market order: the file's own (Boston) market first, then each market as listed.
    market_ids = [DEFAULT_MARKET] + [m for m in markets if m != DEFAULT_MARKET]
    by_market = {mid: [sid for sid in results if market_id(sites[sid]) == mid] for mid in market_ids}
    by_market = {mid: ids for mid, ids in by_market.items() if ids}
    local = {mid: m for mid, m in markets.items() if mid != DEFAULT_MARKET and any(
        k in m for k in ("wages", "burden_pct", "utilities_per_sqft_year", "fixed_costs_per_year", "price_index",
                         "closed_days_per_year", "startup", "startup_fees", "manager_salary"))}
    op, fin, lab = cfg["operating"], cfg["financing"], cfg["labor"]
    cash_limit = fin.get("owner_cash_limit")
    formats = lab["formats"]
    short = {fmt: f["label"].split(":")[0] for fmt, f in formats.items()}
    days_of = {fmt: float(f.get("days_per_year", op["days_per_year"])) for fmt, f in formats.items()}
    hours_of = {fmt: f.get("hours", op.get("hours", "")) for fmt, f in formats.items()}
    buffer = float(op["cogs_buffer_pts"])

    out = [
        "# Pro forma",
        "",
        "Generated by `tools/proforma.py` from `db/proforma.yaml` and the menu database. Do not edit by hand; "
        "change the inputs and rerun the script. All figures are estimates; the sites come from "
        "[`reports/Boston bakery small-shop sites.md`](../reports/Boston%20bakery%20small-shop%20sites.md), "
        "[`reports/Boston bakery site shortlist.md`](../reports/Boston%20bakery%20site%20shortlist.md), "
        "[`reports/Boston bakery site scan.md`](../reports/Boston%20bakery%20site%20scan.md)"
        + (", [`reports/Miami roll bakery feasibility.md`](../reports/Miami%20roll%20bakery%20feasibility.md)"
           if "miami" in markets else "")
        + (" and [`reports/Miami roll house design.md`](../reports/Miami%20roll%20house%20design.md)"
           if "roll_house" in formats else "")
        + ", and none has been confirmed with a broker.",
        "",
        "## Formats",
        "",
        "| Format | Open | Sales on a design day | Orders (est.) | Average order | Food and packaging, with buffer | "
        "Hands-on prep hours | Paid crew hours | Space | Equipment |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for fmt, f in formats.items():
        m, c = menus[fmt], data["crews"][fmt]
        space = sum(float(z["sqft"]) for z in cfg["space_program"][fmt])
        equip = sum(float(e["cost"]) for e in cfg["equipment"][fmt])
        out.append(
            f"| {short[fmt]} | {hours_of[fmt]}; {days_of[fmt]:g} days a year | {usd(m['sales'])} | {m['orders']:.0f} | "
            f"${m['ticket']:.2f} | {m['goods_pct'] + buffer:.1f}% | {m['hands_on_hours']:.1f} | {c['hours']:g} | "
            f"{space:,.0f} sq ft | {usd(equip)} |"
        )
    out.append("")
    for fmt, f in formats.items():
        m = menus[fmt]
        who = (f"A hired general manager runs it ({usd(float(lab['manager']['salary']))} a year)." if f.get("manager", True)
               else "The owner runs it. The P&L pays the owner nothing, so what is left after any debt service is "
                    f"the owner's pay; the target is {usd(owner_target(f))} a year.")
        share = float({**fin, **(f.get("financing") or {})}["loan_share_pct"])
        who += (" Paid for in cash, with no loan." if not share
                else f" Financed {share:g}% with a {fin['term_years']}-year loan at {fin['rate_pct']}%.")
        hero = f" About {m['hero_units']:.0f} {m['hero_name'].lower()}s a day, counting boxes." if m["hero_name"] else ""
        out.append(f"- **{f['label']}.** {who}{hero}")
    out += [
        "",
        "## How sales are projected",
        "",
        "Each format has a design day: its products' daily volumes times their prices. The bakery-café uses every "
        "product's `par_daily`; the roll bakery uses the short menu and volumes listed under its format in "
        "`proforma.yaml`. A site's `sales_index` scales its format's design day to the site, and each scenario "
        "scales it again. The order counts divide the items sold by an assumed items per order, so treat them as "
        f"rough. Year 1 ramps from {op['ramp_year1_pct'][0]}% to {op['ramp_year1_pct'][-1]}% of the steady state, "
        f"averaging {sum(op['ramp_year1_pct']) / 12:.0f}%; Year 3 adds {op['price_growth_pct']}% of price growth. "
        f"Food cost is the menu's cost at distributor prices plus {buffer:g} points for waste beyond the recipes' "
        "allowances, comps, staff meals and price drift.",
        "",
        "| Category | " + " | ".join(f"{short[fmt]}, share of sales" for fmt in formats) + " |",
        "|---|" + "---|" * len(formats),
    ]
    cats = sorted({c for m in menus.values() for c in m["by_category"]},
                  key=lambda c: -max(m["by_category"].get(c, 0) / m["sales"] for m in menus.values()))
    for cat in cats:
        cells = " | ".join(pct(menus[fmt]["by_category"].get(cat, 0), menus[fmt]["sales"]) if menus[fmt]["by_category"].get(cat)
                           else "not sold" for fmt in formats)
        out.append(f"| {cat} | {cells} |")

    # Space
    out += ["", "## Space needed", ""]
    for fmt, zones in cfg["space_program"].items():
        total = sum(float(z["sqft"]) for z in zones)
        out += [f"**{formats[fmt]['label']}: about {total:,.0f} sq ft**", "", "| Zone | Sq ft |", "|---|---|"]
        out += [f"| {z['zone']} | {float(z['sqft']):,.0f} |" for z in zones]
        out += [f"| **Total** | **{total:,.0f}** |", ""]
    out += [
        "The full menu, with lunch, seats and catering, needs about 2,000–2,500 sq ft, a vented hood over the "
        "griddle, gas for the ovens and a walk-in. The roll bakery fits in about 900 sq ft. It bakes in electric "
        "ovens and has no griddle or fryer, so it should not need a grease hood; confirm that with the local "
        "building and health departments before signing a lease.",
    ]

    # Site comparison
    out += ["", "## Sites compared, base scenario"]
    owner_note = " (the owner's pay)"
    for mid, ids in by_market.items():
        out += [
            *(["", f"### {market_label(cfg, mid)}"] if len(by_market) > 1 else []),
            "",
            "| Site | Format | Sq ft | Base rent / NNN per sq ft | Most base rent it can carry | Steady sales a year | "
            "Orders a day | Base rent / with NNN, % of sales | Startup cost | Owner's cash | Cash after debt, Year 1 | "
            "EBITDA, Year 2 | Cash after debt, Year 2 | Return on the owner's cash, Year 2 | Break-even sales a day | Payback |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
        ]
        out += [compare_row(sites[sid], results[sid]["base"], short, owner_note) for sid in ids]
    out += [
        "",
        "Break-even is the daily sales at which Year-2 cash flow after debt service is zero. Payback is the "
        "startup cost divided by Year-3 EBITDA. The most base rent a site can carry is the rent at which Year-2 cash "
        "after debt service falls to zero, or, for an owner-run format, to the owner's target pay, with its NNN "
        "unchanged; an assumed rent is a placeholder until a broker quotes one. The site scan's rent test is base "
        "rent at or under 8% of sales; NNN charges come on top. Year-1 cash after debt has to fit inside the "
        "working capital reserve."
        + (f" The owner would put in up to {usd(float(cash_limit))} without a loan." if cash_limit else "")
        + " A site paid for in cash has no debt service, so its EBITDA and its cash after debt are the same."
        + ("" if not local else " Sites outside Boston use their market's wages, payroll burden, utilities, "
           "insurance and prices: see Markets below."),
    ]
    site_order = [sid for ids in by_market.values() for sid in ids]
    out += site_sections(data, site_order, short, local)
    out += staffing_section(data, short, local)
    out += equipment_section(cfg, formats)
    out += assumptions_section(data, short, days_of, hours_of, local)
    return "\n".join(out) + "\n"


def compare_row(s: dict, r: dict, short: dict, owner_note: str) -> str:
    y1, y2 = r["years"][0], r["years"][1]
    payback = f"{r['payback_years']:.1f} yrs" if r["payback_years"] else "n/a"
    return (
            f"| {s['name']} | {short[s['format']]} | {float(s['sqft']):,.0f} | "
            f"${float(s['rent_psf']):.2f}{' (assumed)' if s.get('rent_assumed') else ''} / ${float(s['nnn_psf']):.2f} | "
            f"{'none' if r['rent_ceiling_psf'] is None else usd(r['rent_ceiling_psf'])} | "
            f"{usd(r['steady_sales'])} | {r['orders_daily']:.0f} | {r['base_rent_pct_y2']:.1f}% / {r['rent_pct_y2']:.1f}% | "
            f"{usd(r['startup'])} | "
            f"{usd(r['equity'])}{' (over the limit)' if r['over_cash_limit'] else ''} | "
            f"{usd(y1['cash_after_debt'])}{'' if r['reserve_covers_year1'] else ' (more than the reserve)'} | "
            f"{usd(y2['ebitda'])} ({pct(y2['ebitda'], y2['sales'])}) | "
            f"{usd(y2['cash_after_debt'])}{'' if r['managed'] else owner_note} | "
            f"{pct(y2['cash_after_debt'], r['equity'])} | "
            f"{usd(r['breakeven_daily'])} ({r['breakeven_orders_daily']:.0f} orders) | {payback} |"
        )


def site_sections(data: dict, site_order: list, short: dict, local: dict) -> list[str]:
    cfg, menus, results = data["config"], data["menus"], data["results"]
    sites = {s["id"]: s for s in cfg["sites"]}
    formats, fin = cfg["labor"]["formats"], cfg["financing"]
    out: list[str] = []
    for sid in site_order:
        by_sc = results[sid]
        s = sites[sid]
        base = by_sc["base"]
        f = formats[s["format"]]
        managed = base["managed"]
        hero_name = menus[s["format"]]["hero_name"]
        last_col = ("Owner's earnings if the owner manages, Year 2" if managed
                    else f"{hero_name.capitalize()}s a day, with boxes" if hero_name else "Orders a day")
        ceiling = 'none' if base['rent_ceiling_psf'] is None else usd(base['rent_ceiling_psf']) + ' a sq ft'
        out += [
            "",
            f"## {s['name']}",
            "",
            f"{s.get('area', '')}. {float(s['sqft']):,.0f} sq ft, {s['seats']} seats, {short[s['format']].lower()} format. "
            f"Sales index {float(s['sales_index']):g} of the format's design day.",
            "",
            f"- **Kitchen:** {s.get('kitchen', '')}",
            f"- **Rent:** {s.get('rent_basis', '')}",
            f"- **Most base rent it can carry:** {ceiling} in the base case"
            + ("" if managed else f", after paying the owner {usd(base['owner_pay_target'])}"),
            *([f"- **Space:** {s['space_note']}"] if s.get("space_note") else []),
            f"- **Time to open:** about {s.get('months_to_open', 0):g} months from lease signing, paying rent throughout",
            *([f"- **Local costs:** {market_costs(cfg, market_id(s), base)}"] if market_id(s) in local else []),
            *([f"- **Equipment credit:** {usd(float(s['equipment_credit']))}, "
               f"{s.get('equipment_credit_note', 'equipment already in place')}"] if s.get("equipment_credit") else []),
            *([f"- **Purchase price:** {usd(float(s['purchase_price']))} asked for the existing fit-out and lease"]
              if s.get("purchase_price") else []),
            f"- **Risks:** {s.get('risks', '')}",
            f"- **Source:** {s.get('source', '')}",
            "",
            f"| Scenario | Sales a day, steady | Orders a day | Sales, Year 2 | EBITDA, Year 2 | Cash after debt, Year 2 | {last_col} |",
            "|---|---|---|---|---|---|---|",
        ]
        for sc in cfg["scenarios"]:
            r = by_sc[sc["id"]]
            y2 = r["years"][1]
            last = usd(y2["owner_earnings"]) if managed else f"{r['hero_units_daily']:.0f}" if hero_name else f"{r['orders_daily']:.0f}"
            out.append(
                f"| {sc['name']} | {usd(r['steady_daily'])} | {r['orders_daily']:.0f} | {usd(y2['sales'])} | "
                f"{usd(y2['ebitda'])} ({pct(y2['ebitda'], y2['sales'])}) | {usd(y2['cash_after_debt'])} | {last} |"
            )
        out += ["", "**Base case, three years**", "", "| Line | Year 1 | Year 2 | Year 3 | Year 2, % of sales |",
                "|---|---|---|---|---|"]
        ys = base["years"]
        out.append(f"| Sales | {' | '.join(usd(y['sales']) for y in ys)} | 100% |")
        for key, label in LINE_LABELS:
            if any(y[key] for y in ys):
                out.append(f"| {label} | {' | '.join(usd(y[key]) for y in ys)} | {pct(ys[1][key], ys[1]['sales'])} |")
        out.append(f"| **EBITDA** | {' | '.join('**' + usd(y['ebitda']) + '**' for y in ys)} | "
                   f"**{pct(ys[1]['ebitda'], ys[1]['sales'])}** |")
        borrowed = base["loan"] > 0
        if borrowed:
            out.append(f"| Debt service | {' | '.join(usd(y['debt_service']) for y in ys)} | "
                       f"{pct(ys[1]['debt_service'], ys[1]['sales'])} |")
        cash_label = ("Cash after debt service" if managed else "Cash after debt service: the owner's pay" if borrowed
                      else "Left for the owner (no loan)")
        out.append(f"| **{cash_label}** | {' | '.join('**' + usd(y['cash_after_debt']) + '**' for y in ys)} | "
                   f"**{pct(ys[1]['cash_after_debt'], ys[1]['sales'])}** |")
        crew_hours = " | ".join(f"{y['hours_day']:.0f}" for y in ys)
        out.append(f"| Paid crew hours a day | {crew_hours} | |")
        labor = ys[1]["cogs"] + ys[1]["hourly_labor"] + ys[1]["manager"]
        out += [
            "",
            f"Prime cost (food, packaging{', hourly crew and manager' if managed else ' and hourly crew, before any owner pay'}) is "
            f"{pct(labor, ys[1]['sales'])} of Year-2 sales; "
            f"sales per paid crew hour are {usd(base['sales_per_labor_hour_y2'])}. Break-even is "
            f"{usd(base['breakeven_daily'])} a day{' after debt service' if borrowed else ''}, about "
            f"{base['breakeven_orders_daily']:.0f} orders ({100 * base['breakeven_vs_steady']:.0f}% of the steady state)"
            + (f", and {usd(base['breakeven_ebitda_daily'])} a day before it" if borrowed else "")
            + ". Each extra $100 a day of sales adds about "
            f"{usd(base['per_extra_100_daily'])} a year of EBITDA once the crew flexes.",
        ]
        if not managed and base["owner_target_daily"]:
            out += [
                "",
                f"The owner isn't paid in this P&L and works about {data['crews'][s['format']]['owner_hours']:g} hours "
                f"a day. Paying the owner {usd(base['owner_pay_target'])} a year takes {usd(base['owner_target_daily'])} "
                f"a day, about {base['owner_target_orders_daily']:.0f} orders.",
            ]
        out += ["", "**Startup cost**", "", "| Item | Cost |", "|---|---|"]
        out += [f"| {k} | {usd(v)} |" for k, v in base["startup_lines"].items()]
        out += [
            f"| **Total** | **{usd(base['startup'])}** |",
            "",
            (f"Financed {100 * base['loan'] / base['startup']:.0f}% with a {fin['term_years']}-year loan at "
             f"{fin['rate_pct']}% ({usd(base['loan'])}, {usd(base['debt_service'])} a year) and "
             f"{usd(base['equity'])} of owner equity." if borrowed
             else f"Paid for in cash, with no loan: {usd(base['equity'])} from the owner, a "
                  f"{pct(ys[1]['cash_after_debt'], base['equity'])} return on it in Year 2."
                  + (f" That is {usd(base['equity'] - float(base['owner_cash_limit']))} more than the "
                     f"{usd(float(base['owner_cash_limit']))} the owner would put in." if base["over_cash_limit"] else "")),
        ]

    return out


def market_costs(cfg: dict, mid: str, r: dict) -> str:
    """One sentence on a market's local costs, from a site's base-case result."""
    m = (cfg.get("markets") or {}).get(mid) or {}
    parts = [f"paid crew average ${r['avg_wage']:.2f} an hour", f"{r['burden_pct']:g}% payroll burden",
             f"utilities ${r['utilities_psf']:g} a sq ft"]
    if m.get("fixed_costs_per_year"):
        parts.append("; ".join(f"{k.replace('_', ' ')} {usd(float(v))}" for k, v in m["fixed_costs_per_year"].items()))
    if r["price_index"] != 1:
        parts.append(f"menu prices at {100 * r['price_index']:.0f}% of the database's")
    if m.get("closed_days_per_year"):
        parts.append(f"{float(m['closed_days_per_year']):g} more days closed a year")
    if m.get("startup_fees"):
        parts.append("; ".join(f"{k.lower()} {usd(float(v))}" for k, v in m["startup_fees"].items()))
    return f"{market_label(cfg, mid)}: " + ", ".join(parts)


def staffing_section(data: dict, short: dict, local: dict) -> list[str]:
    cfg, menus = data["config"], data["menus"]
    lab, formats = cfg["labor"], cfg["labor"]["formats"]
    out = ["", "## Staffing at each format's design volume", ""]
    for fmt, f in formats.items():
        c = data["crews"][fmt]
        lead = (f"plus a general manager at {usd(float(lab['manager']['salary']))}" if f.get("manager", True)
                else f"plus the owner for about {c['owner_hours']:g} hours a day, unpaid in the P&L")
        extra = [mid for mid, m in local.items() if m.get("wages")]
        local_avg = "".join(f"; at {market_label(cfg, mid)} wages ${data['market_crews'][mid][fmt]['avg_wage']:.2f}"
                            for mid in extra)
        out += [f"**{f['label']}**: {c['hours']:g} paid hours a day, average ${c['avg_wage']:.2f} an hour"
                f"{local_avg} before payroll burden, {lead}. The menu database counts "
                f"{menus[fmt]['hands_on_hours']:.1f} hands-on prep and bar hours on a design day; the rest of the "
                "schedule is setup, cleaning, the register and slow periods.", "",
                "| Role | Hours a day | Wage | " + "".join(f"{market_label(cfg, mid)} wage | " for mid in extra) + "Covers |",
                "|---|---|---|" + "---|" * len(extra) + "---|"]
        for r in f["roles"]:
            cells = ["owner" if r.get("owner") else "$%.2f" % float(r["wage"])]
            cells += ["owner" if r.get("owner") else "$%.2f" % data["market_crews"][mid][fmt]["wages"][r["role"]]
                      for mid in extra]
            out.append(f"| {r['role']} | {float(r['hours']):g} | " + " | ".join(cells) + f" | {r.get('note', '')} |")
        out.append("")
    out += [f"{round(100 * float(lab['fixed_share']))}% of paid hours are treated as fixed; the rest flex with sales."]
    return out


def equipment_section(cfg: dict, formats: dict) -> list[str]:
    out = ["", "## Equipment", ""]
    for fmt, items in cfg["equipment"].items():
        total = sum(float(e["cost"]) for e in items)
        out += [f"**{formats[fmt]['label']}: {usd(total)}**", "", "| Item | Cost |", "|---|---|"]
        out += [f"| {e['item']} | {usd(float(e['cost']))} |" for e in items]
        out.append("")
    return out


def assumptions_section(data: dict, short: dict, days_of: dict, hours_of: dict, local: dict) -> list[str]:
    cfg = data["config"]
    op, fin, lab, formats = cfg["operating"], cfg["financing"], cfg["labor"], cfg["labor"]["formats"]
    cash_limit = fin.get("owner_cash_limit")
    var = cfg["variable_costs_pct_of_sales"]
    fixed = cfg["fixed_costs_per_year"]
    fixed_by_format = "; ".join(
        f"{short[fmt].lower()} {usd(sum(float(v) for v in {**fixed, **(f.get('fixed_costs_per_year') or {})}.values()))}"
        for fmt, f in formats.items())
    out = [
        "## Other assumptions",
        "",
        "- **Days and hours:** " + "; ".join(f"{short[fmt].lower()} {days_of[fmt]:g} days a year, {hours_of[fmt]}" for fmt in formats) + ".",
        "- **Variable costs, % of sales:** " + ", ".join(f"{k.replace('_', ' ')} {v}%" for k, v in var.items()) + ".",
        "- **Fixed costs a year:** " + ", ".join(f"{k.replace('_', ' ')} {usd(float(v))}" for k, v in fixed.items())
        + f". Totals by format: {fixed_by_format}.",
        f"- **Utilities:** ${cfg['utilities_per_sqft_year']} a sq ft a year.",
        f"- **Payroll burden:** {lab['burden_pct']}% on all pay.",
        "- **Financing:** " + "; ".join(
            f"{short[fmt].lower()} "
            + ("paid in cash, with no loan" if not float({**fin, **(f.get('financing') or {})}['loan_share_pct'])
               else f"{float({**fin, **(f.get('financing') or {})}['loan_share_pct']):g}% from a {fin['term_years']}-year "
                    f"loan at {fin['rate_pct']}%")
            for fmt, f in formats.items())
        + (f". The owner would put in up to {usd(float(cash_limit))}." if cash_limit else "."),
        f"- **Inflation:** wages, NNN and fixed costs rise {op['cost_inflation_pct']}% a year; base rent rises at "
        "each site's escalation.",
        "- **Before opening:** rent and NNN are paid from lease signing to opening, for each site's months to open; "
        "no free rent is assumed.",
        "- **Not included:** income taxes, depreciation, owner's pay in an owner-run format, owner's draw beyond the "
        "manager line in a managed one, and any landlord build-out allowance or free rent, which would lower the "
        "startup cost.",
    ]
    if local:
        out += ["", "## Markets", "",
                "The inputs above are Boston's. A site in another market replaces them with that market's own:"]
        for mid, m in local.items():
            out += ["", f"**{market_label(cfg, mid)}.** {m.get('note', '')}".rstrip(), ""]
            rows = []
            if m.get("wages"):
                rows += [f"| Wage: {role} | ${float(w):.2f} an hour |" for role, w in m["wages"].items()]
            if "burden_pct" in m:
                rows.append(f"| Payroll burden | {float(m['burden_pct']):g}% (Boston {lab['burden_pct']}%) |")
            if "utilities_per_sqft_year" in m:
                rows.append(f"| Utilities | ${float(m['utilities_per_sqft_year']):g} a sq ft a year "
                            f"(Boston ${cfg['utilities_per_sqft_year']}) |")
            rows += [f"| {k.replace('_', ' ').capitalize()} | {usd(float(v))} a year |"
                     for k, v in (m.get("fixed_costs_per_year") or {}).items()]
            if "price_index" in m:
                rows.append(f"| Menu prices | {100 * float(m['price_index']):.0f}% of the database's |")
            if m.get("closed_days_per_year"):
                rows.append(f"| Extra days closed | {float(m['closed_days_per_year']):g} a year |")
            rows += [f"| {k.replace('_', ' ').capitalize()} (startup) | {usd(float(v))} |"
                     for k, v in (m.get("startup") or {}).items()]
            rows += [f"| {k} (startup) | {usd(float(v))} |" for k, v in (m.get("startup_fees") or {}).items()]
            if "manager_salary" in m:
                rows.append(f"| General manager's salary | {usd(float(m['manager_salary']))} |")
            out += ["| Input | Value |", "|---|---|", *rows]
            if m.get("sources"):
                out += ["", "Sources: " + m["sources"]]
    out += [
        "",
        "## Sources",
        "",
        "- Sites, sizes, rents and kitchen evidence: [`reports/Boston bakery site scan.md`](../reports/Boston%20bakery%20site%20scan.md), "
        "[its candidates CSV](../reports/Boston%20bakery%20site%20scan%20candidates.csv), "
        "[`reports/Boston bakery site shortlist.md`](../reports/Boston%20bakery%20site%20shortlist.md) and "
        "[`reports/Boston bakery small-shop sites.md`](../reports/Boston%20bakery%20small-shop%20sites.md).",
        *(["- Miami sites, rents and local costs: "
           "[`reports/Miami roll bakery feasibility.md`](../reports/Miami%20roll%20bakery%20feasibility.md) and its notes in "
           "[`research_notes/Miami roll bakery feasibility/`](../research_notes/Miami%20roll%20bakery%20feasibility/)."]
          if "miami" in (cfg.get("markets") or {}) else []),
        *(["- The Miami roll house format, its products, prices and sites: "
           "[`reports/Miami roll house design.md`](../reports/Miami%20roll%20house%20design.md) and its notes in "
           "[`research_notes/Miami roll house design/`](../research_notes/Miami%20roll%20house%20design/)."]
          if "roll_house" in formats else []),
        "- Format benchmarks, wages, payroll burden, occupancy and margin norms: "
        "[`digest_5_unit_economics_boston_costs.md`](../research_notes/Boston%20bakery%20market%20matrix/digests/digest_5_unit_economics_boston_costs.md).",
        "- Equipment, hood and build-out cost ranges: "
        "[`gapfill_model_economics.md`](../research_notes/Boston%20bakery%20market%20matrix/gapfill_model_economics.md).",
        "- Menu sales, food cost and prep hours: [`costing.md`](costing.md) and [`production.md`](production.md).",
    ]
    return out



def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate only; do not write the report")
    args = parser.parse_args()
    try:
        data = build()
    except (DBError, KeyError, ValueError, yaml.YAMLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.check:
        print("ok")
        return 0
    REPORT.write_text(render(data), encoding="utf-8")
    print(f"wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
