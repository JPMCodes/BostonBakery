#!/usr/bin/env python3
"""Build the bakery pro forma: space, startup cost and three years of P&L per site and scenario.

Usage:
    python3 tools/proforma.py           # validate, then write db/proforma.md
    python3 tools/proforma.py --check   # validate only; exit 1 on any error

Reads db/proforma.yaml and, through tools/costing.py, the menu database: the
planning pars give the menu's steady-state day, its sales, its food-and-packaging
cost and its hands-on prep hours. Requires PyYAML.
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


def load() -> dict:
    if not PROFORMA.exists():
        raise DBError("db/proforma.yaml is missing")
    return yaml.safe_load(PROFORMA.read_text(encoding="utf-8")) or {}


def validate(cfg: dict) -> list[str]:
    errors = [f"proforma.yaml: missing '{key}'" for key in REQUIRED if key not in cfg]
    if errors:
        return errors
    formats = cfg["labor"].get("formats") or {}
    for site in cfg["sites"]:
        where = f"proforma.yaml: site {site.get('id', '?')}"
        errors += [f"{where}: missing '{f}'" for f in SITE_FIELDS if f not in site]
        fmt = site.get("format")
        if fmt not in formats or fmt not in cfg["equipment"] or fmt not in cfg["space_program"]:
            errors.append(f"{where}: format '{fmt}' needs labor.formats, equipment and space_program entries")
    ramp = cfg["operating"].get("ramp_year1_pct") or []
    if len(ramp) != 12:
        errors.append("proforma.yaml: operating.ramp_year1_pct needs 12 monthly values")
    for site in cfg["sites"]:
        if "rent_assumed" in site and not isinstance(site["rent_assumed"], bool):
            errors.append(f"proforma.yaml: site {site.get('id', '?')}: rent_assumed must be true or false")
        for key in ("months_to_open", "soft_costs_pct", "equipment_credit"):
            if key in site and (not isinstance(site[key], (int, float)) or site[key] < 0):
                errors.append(f"proforma.yaml: site {site.get('id', '?')}: {key} must be a number of 0 or more")
    for sc in cfg["scenarios"]:
        if not isinstance(sc.get("sales_factor"), (int, float)) or sc["sales_factor"] <= 0:
            errors.append(f"proforma.yaml: scenario {sc.get('id', '?')} needs a positive sales_factor")
    return errors


def menu_day(book: Book) -> dict:
    """The menu's steady-state day at its planning pars."""
    sales = goods = hours = 0.0
    by_category: dict[str, float] = {}
    for pid, doc in book.products.items():
        par = float(doc.get("par_daily") or 0)
        price = float(doc["pricing"].get("suggested_retail_usd") or 0)
        sales += price * par
        goods += (book.product_cost(pid, CHANNEL) or 0) * par
        hours += book.product_labor(pid) * par / 60
        by_category[doc["category"]] = by_category.get(doc["category"], 0) + price * par
    if not sales:
        raise DBError("the menu has no par_daily volumes, so there are no sales to project")
    return {
        "sales": sales,
        "goods_pct": 100 * goods / sales,
        "hands_on_hours": hours,
        "by_category": by_category,
    }


def annual_payment(principal: float, rate_pct: float, years: float) -> float:
    r, n = rate_pct / 100 / 12, years * 12
    if principal <= 0:
        return 0.0
    if r == 0:
        return principal / years
    return 12 * principal * r / (1 - (1 + r) ** -n)


def crew(cfg: dict, fmt: str) -> tuple[float, float]:
    """(scheduled hourly crew hours a day, average hourly wage) at the format's design volume."""
    roles = cfg["labor"]["formats"][fmt]["roles"]
    hours = sum(float(r["hours"]) for r in roles)
    wages = sum(float(r["hours"]) * float(r["wage"]) for r in roles)
    return hours, wages / hours


def model(cfg: dict, menu: dict, site: dict, scenario: dict) -> dict:
    op, lab, fin, st = cfg["operating"], cfg["labor"], cfg["financing"], cfg["startup"]
    days = float(op["days_per_year"])
    fmt_cfg = lab["formats"][site["format"]]
    base_hours, wage = crew(cfg, site["format"])
    burden = 1 + float(lab["burden_pct"]) / 100
    fixed_share = float(lab["fixed_share"])
    ramp = sum(op["ramp_year1_pct"]) / len(op["ramp_year1_pct"]) / 100
    infl = float(op["cost_inflation_pct"]) / 100
    growth = float(op["price_growth_pct"]) / 100
    level = float(site["sales_index"]) * float(scenario["sales_factor"])  # share of the menu's par day
    steady = menu["sales"] * level * days
    goods_pct = menu["goods_pct"] + float(op["cogs_buffer_pts"])
    var_pct = sum(float(v) for v in cfg["variable_costs_pct_of_sales"].values())
    fixed_base = sum(float(v) for v in cfg["fixed_costs_per_year"].values())
    sqft = float(site["sqft"])
    manager_base = float(lab["manager"]["salary"]) * burden

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
            "rent": sqft * float(site["rent_psf"]) * (1 + float(site["escalation_pct"]) / 100) ** (n - 1),
            "nnn": sqft * float(site["nnn_psf"]) * mult,
            "utilities": sqft * float(cfg["utilities_per_sqft_year"]) * mult,
            "variable_opex": sales * var_pct / 100,
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
        "Furniture and fixtures": float(site["seats"]) * float(st["furniture_per_seat"]) + float(st["furniture_base"]),
        "Signage": float(st["signage"]),
        "Pre-opening payroll and training": (base_hours * 0.6 * wage * burden * 7 * float(st["preopening_payroll_weeks"])
                                             + manager_base / 52 * float(st.get("manager_preopening_weeks", 0))),
        "Opening inventory": float(st["opening_inventory"]),
        "Launch marketing": float(st["launch_marketing"]),
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
    design_sales = menu["sales"] * float(fmt_cfg["design_index"]) * days
    crew_cost = base_hours * wage * burden * days * (1 + infl)
    fixed_cash = (y2["manager"] + y2["rent"] + y2["nnn"] + y2["utilities"] + y2["fixed_opex"]
                  + crew_cost * fixed_share)
    var_rate = (goods_pct + var_pct) / 100 + crew_cost * (1 - fixed_share) / design_sales
    breakeven = (fixed_cash + debt_service) / (1 - var_rate)
    breakeven_ebitda = fixed_cash / (1 - var_rate)

    y3 = years[2]
    reserve = startup_lines["Working capital reserve"]
    return {
        "site": site["id"],
        "scenario": scenario["id"],
        "steady_sales": steady,
        "steady_daily": steady / days,
        "years": years,
        "startup_lines": startup_lines,
        "startup": startup,
        "loan": loan,
        "equity": equity,
        "debt_service": debt_service,
        "breakeven_sales": breakeven,
        "breakeven_daily": breakeven / days,
        "breakeven_ebitda_daily": breakeven_ebitda / days,
        "breakeven_vs_steady": breakeven / steady if steady else None,
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
    """The base rent per sq ft at which Year-2 cash after debt service is zero, other inputs fixed."""
    def cash(rent: float) -> float:
        return model(cfg, menu, dict(site, rent_psf=rent), scenario)["years"][1]["cash_after_debt"]
    lo, hi = 0.0, 400.0
    if cash(lo) <= 0:
        return None
    if cash(hi) > 0:
        return hi
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if cash(mid) > 0 else (lo, mid)
    return lo


def build(book: Book | None = None) -> dict:
    """Everything the report and the viewer need."""
    book = book or Book()
    cfg = load()
    errors = validate(cfg)
    if errors:
        raise DBError("; ".join(errors))
    menu = menu_day(book)
    results = {s["id"]: {sc["id"]: model(cfg, menu, s, sc) for sc in cfg["scenarios"]} for s in cfg["sites"]}
    for s in cfg["sites"]:
        for sc in cfg["scenarios"]:
            results[s["id"]][sc["id"]]["rent_ceiling_psf"] = rent_ceiling(cfg, menu, s, sc)
    crews = {}
    for fmt in cfg["labor"]["formats"]:
        hours, wage = crew(cfg, fmt)
        crews[fmt] = {"hours": hours, "avg_wage": wage}
    return {"config": cfg, "menu": menu, "results": results, "crews": crews,
            "days": float(cfg["operating"]["days_per_year"])}


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
    ("fixed_opex", "Insurance, software, accounting, licenses, waste, linens, phone"),
]


def render(data: dict) -> str:
    cfg, menu, results = data["config"], data["menu"], data["results"]
    days = data["days"]
    sites = {s["id"]: s for s in cfg["sites"]}
    op = cfg["operating"]
    fin = cfg["financing"]
    out = [
        "# Pro forma",
        "",
        "Generated by `tools/proforma.py` from `db/proforma.yaml` and the menu database. Do not edit by hand; "
        "change the inputs and rerun the script. All figures are estimates; the sites come from "
        "[`reports/Boston bakery site scan.md`](../reports/Boston%20bakery%20site%20scan.md) and none has been "
        "confirmed with a broker.",
        "",
        "## How sales are projected",
        "",
        f"The menu's planning pars (`par_daily` in each product) add up to **{usd(menu['sales'])} of sales a day**, "
        f"or {usd(menu['sales'] * days)} a year over {days:g} days, with food and packaging at "
        f"{menu['goods_pct']:.0f}% of sales at distributor prices and {menu['hands_on_hours']:.1f} hands-on prep "
        "hours. Each site's `sales_index` scales that day to the site, and each scenario scales it again. "
        f"Year 1 ramps from {op['ramp_year1_pct'][0]}% to {op['ramp_year1_pct'][-1]}% of the steady state, "
        f"averaging {sum(op['ramp_year1_pct']) / 12:.0f}%; Year 3 adds {op['price_growth_pct']}% of price growth. "
        f"Food cost carries {op['cogs_buffer_pts']} extra points for comps, staff meals and price drift.",
        "",
        "| Category | Share of the par day |",
        "|---|---|",
    ]
    for cat, amount in sorted(menu["by_category"].items(), key=lambda kv: -kv[1]):
        out.append(f"| {cat} | {pct(amount, menu['sales'])} |")

    # Space
    out += ["", "## Space needed", ""]
    for fmt, zones in cfg["space_program"].items():
        label = cfg["labor"]["formats"][fmt]["label"]
        total = sum(float(z["sqft"]) for z in zones)
        out += [f"**{label}: about {total:,.0f} sq ft**", "", "| Zone | Sq ft |", "|---|---|"]
        out += [f"| {z['zone']} | {float(z['sqft']):,.0f} |" for z in zones]
        out += [f"| **Total** | **{total:,.0f}** |", ""]
    out += [
        "The full menu, with lunch, seats and catering, needs about 2,000–2,500 sq ft. A space near 1,500 sq ft "
        "works as a counter bakery with a short lunch list. Either way it needs a vented hood over the griddle, "
        "gas for the ovens, and room for a walk-in or a bank of reach-ins.",
    ]

    # Site comparison
    out += [
        "",
        "## Sites compared, base scenario",
        "",
        "| Site | Format | Sq ft | Base rent / NNN per sq ft | Most base rent it can carry | Steady sales a year | Base rent / with NNN, % of sales | Startup cost | "
        "Cash after debt, Year 1 | EBITDA, Year 2 | Cash after debt, Year 2 | Break-even sales a day | Payback |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for sid, by_sc in results.items():
        r = by_sc["base"]
        s = sites[sid]
        y1, y2 = r["years"][0], r["years"][1]
        payback = f"{r['payback_years']:.1f} yrs" if r["payback_years"] else "n/a"
        out.append(
            f"| {s['name']} | {s['format']} | {float(s['sqft']):,.0f} | "
            f"${float(s['rent_psf']):.2f}{' (assumed)' if s.get('rent_assumed') else ''} / ${float(s['nnn_psf']):.2f} | "
            f"{'none' if r['rent_ceiling_psf'] is None else usd(r['rent_ceiling_psf'])} | "
            f"{usd(r['steady_sales'])} | {r['base_rent_pct_y2']:.1f}% / {r['rent_pct_y2']:.1f}% | {usd(r['startup'])} | "
            f"{usd(y1['cash_after_debt'])}{'' if r['reserve_covers_year1'] else ' (more than the reserve)'} | "
            f"{usd(y2['ebitda'])} ({pct(y2['ebitda'], y2['sales'])}) | {usd(y2['cash_after_debt'])} | "
            f"{usd(r['breakeven_daily'])} | {payback} |"
        )
    out += [
        "",
        "Break-even is the daily sales at which Year-2 cash flow after debt service is zero. Payback is the "
        "startup cost divided by Year-3 EBITDA. The most base rent a site can carry is the rent at which Year-2 cash "
        "after debt service falls to zero, with its NNN unchanged; an assumed rent is a placeholder until a broker "
        "quotes one. The site scan's rent test is base rent at or under 8% of sales; "
        "NNN charges come on top. Year-1 cash after debt has to fit inside the working capital reserve.",
    ]

    # Per site
    for sid, by_sc in results.items():
        s = sites[sid]
        base = by_sc["base"]
        out += [
            "",
            f"## {s['name']}",
            "",
            f"{s.get('area', '')}. {float(s['sqft']):,.0f} sq ft, {s['seats']} seats, {s['format']} format. "
            f"Sales index {float(s['sales_index']):g} of the menu's par day.",
            "",
            f"- **Kitchen:** {s.get('kitchen', '')}",
            f"- **Rent:** {s.get('rent_basis', '')}",
            f"- **Most base rent it can carry:** "
            f"{'none' if base['rent_ceiling_psf'] is None else usd(base['rent_ceiling_psf']) + ' a sq ft'} in the base case",
            *([f"- **Space:** {s['space_note']}"] if s.get("space_note") else []),
            f"- **Time to open:** about {s.get('months_to_open', 0):g} months from lease signing, paying rent throughout",
            *([f"- **Equipment credit:** {usd(float(s['equipment_credit']))}, "
               f"{s.get('equipment_credit_note', 'equipment already in place')}"] if s.get("equipment_credit") else []),
            f"- **Risks:** {s.get('risks', '')}",
            f"- **Source:** {s.get('source', '')}",
            "",
            "| Scenario | Sales a day, steady | Sales, Year 2 | EBITDA, Year 2 | Cash after debt, Year 2 | "
            "Owner's earnings if the owner manages, Year 2 |",
            "|---|---|---|---|---|---|",
        ]
        for sc in cfg["scenarios"]:
            r = by_sc[sc["id"]]
            y2 = r["years"][1]
            out.append(
                f"| {sc['name']} | {usd(r['steady_daily'])} | {usd(y2['sales'])} | "
                f"{usd(y2['ebitda'])} ({pct(y2['ebitda'], y2['sales'])}) | {usd(y2['cash_after_debt'])} | "
                f"{usd(y2['owner_earnings'])} |"
            )
        out += ["", "**Base case, three years**", "", "| Line | Year 1 | Year 2 | Year 3 | Year 2, % of sales |",
                "|---|---|---|---|---|"]
        ys = base["years"]
        out.append(f"| Sales | {' | '.join(usd(y['sales']) for y in ys)} | 100% |")
        for key, label in LINE_LABELS:
            out.append(f"| {label} | {' | '.join(usd(y[key]) for y in ys)} | {pct(ys[1][key], ys[1]['sales'])} |")
        out.append(f"| **EBITDA** | {' | '.join('**' + usd(y['ebitda']) + '**' for y in ys)} | "
                   f"**{pct(ys[1]['ebitda'], ys[1]['sales'])}** |")
        out.append(f"| Debt service | {' | '.join(usd(y['debt_service']) for y in ys)} | "
                   f"{pct(ys[1]['debt_service'], ys[1]['sales'])} |")
        out.append(f"| **Cash after debt service** | {' | '.join('**' + usd(y['cash_after_debt']) + '**' for y in ys)} | "
                   f"**{pct(ys[1]['cash_after_debt'], ys[1]['sales'])}** |")
        crew_hours = " | ".join(f"{y['hours_day']:.0f}" for y in ys)
        out.append(f"| Scheduled crew hours a day | {crew_hours} | |")
        out += [
            "",
            f"Prime cost (food, packaging, hourly crew and manager) is "
            f"{pct(ys[1]['cogs'] + ys[1]['hourly_labor'] + ys[1]['manager'], ys[1]['sales'])} of Year-2 sales; "
            f"sales per scheduled crew hour are {usd(base['sales_per_labor_hour_y2'])}. Break-even is "
            f"{usd(base['breakeven_daily'])} a day after debt service "
            f"({100 * base['breakeven_vs_steady']:.0f}% of the steady state) and "
            f"{usd(base['breakeven_ebitda_daily'])} a day before it. Each extra $100 a day of sales adds about "
            f"{usd(base['per_extra_100_daily'])} a year of EBITDA once the crew flexes.",
            "",
            "**Startup cost**",
            "",
            "| Item | Cost |",
            "|---|---|",
        ]
        out += [f"| {k} | {usd(v)} |" for k, v in base["startup_lines"].items()]
        out += [
            f"| **Total** | **{usd(base['startup'])}** |",
            "",
            f"Financed {fin['loan_share_pct']}% with a {fin['term_years']}-year loan at {fin['rate_pct']}% "
            f"({usd(base['loan'])}, {usd(base['debt_service'])} a year) and {usd(base['equity'])} of owner equity.",
        ]

    # Staffing and equipment
    out += ["", "## Staffing at each format's design volume", ""]
    for fmt, f in cfg["labor"]["formats"].items():
        c = data["crews"][fmt]
        out += [f"**{f['label']}**: {c['hours']:g} scheduled hours a day, average ${c['avg_wage']:.2f} an hour "
                f"before {cfg['labor']['burden_pct']}% payroll burden, plus a general manager at "
                f"{usd(float(cfg['labor']['manager']['salary']))}.", "",
                "| Role | Hours a day | Wage | Covers |", "|---|---|---|---|"]
        out += [f"| {r['role']} | {float(r['hours']):g} | ${float(r['wage']):.2f} | {r.get('note', '')} |"
                for r in f["roles"]]
        out.append("")
    out += [
        f"At the menu's par day the café crew is scheduled {data['crews']['cafe']['hours']:g} hours against "
        f"{menu['hands_on_hours']:.1f} hands-on prep and bar hours from the menu database, which leaves the rest "
        f"for setup, cleaning, the register and slow periods. {round(100 * float(cfg['labor']['fixed_share']))}% of "
        "scheduled hours are treated as fixed; the rest flex with sales.",
        "",
        "## Equipment",
        "",
    ]
    for fmt, items in cfg["equipment"].items():
        total = sum(float(e["cost"]) for e in items)
        out += [f"**{cfg['labor']['formats'][fmt]['label']}: {usd(total)}**", "", "| Item | Cost |", "|---|---|"]
        out += [f"| {e['item']} | {usd(float(e['cost']))} |" for e in items]
        out.append("")

    # Assumptions
    var = cfg["variable_costs_pct_of_sales"]
    fixed = cfg["fixed_costs_per_year"]
    out += [
        "## Other assumptions",
        "",
        f"- **Days and hours:** {days:g} days a year, {op.get('hours', '')}.",
        "- **Variable costs, % of sales:** " + ", ".join(f"{k.replace('_', ' ')} {v}%" for k, v in var.items()) + ".",
        "- **Fixed costs a year:** " + ", ".join(f"{k.replace('_', ' ')} {usd(float(v))}" for k, v in fixed.items()) + ".",
        f"- **Utilities:** ${cfg['utilities_per_sqft_year']} a sq ft a year.",
        f"- **Inflation:** wages, NNN and fixed costs rise {op['cost_inflation_pct']}% a year; base rent rises at "
        "each site's escalation.",
        "- **Before opening:** rent and NNN are paid from lease signing to opening, for each site's months to open; "
        "no free rent is assumed.",
        "- **Not included:** income taxes, depreciation, owner's draw beyond the manager line, and any "
        "landlord build-out allowance or free rent, which would lower the startup cost.",
        "",
        "## Sources",
        "",
        "- Sites, sizes, rents and kitchen evidence: [`reports/Boston bakery site scan.md`](../reports/Boston%20bakery%20site%20scan.md) "
        "and [its candidates CSV](../reports/Boston%20bakery%20site%20scan%20candidates.csv).",
        "- Format benchmarks, wages, payroll burden, occupancy and margin norms: "
        "[`digest_5_unit_economics_boston_costs.md`](../research_notes/Boston%20bakery%20market%20matrix/digests/digest_5_unit_economics_boston_costs.md).",
        "- Equipment, hood and build-out cost ranges: "
        "[`gapfill_model_economics.md`](../research_notes/Boston%20bakery%20market%20matrix/gapfill_model_economics.md).",
        "- Menu sales, food cost and prep hours: [`costing.md`](costing.md) and [`production.md`](production.md).",
    ]
    return "\n".join(out) + "\n"


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
