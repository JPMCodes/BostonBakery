#!/usr/bin/env python3
"""Validate the bakery formula database and regenerate db/costing.md.

Usage:
    python3 tools/costing.py           # validate, then write db/costing.md
    python3 tools/costing.py --check   # validate only; exit 1 on any error

Reads db/settings.yaml, db/ingredients.csv, db/ingredient_prices.csv,
db/formulas/*.yaml and db/products/*.yaml. Requires PyYAML (pip install pyyaml).
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db"
REPORT = DB / "costing.md"
SETTINGS = DB / "settings.yaml"

# Price channels, in report column order.
CHANNELS = {"retail_est": "Retail est.", "distributor_est": "Distributor est."}

WEIGHT_G = {"g": 1.0, "kg": 1000.0, "oz": 28.349523125, "lb": 453.59237}
VOLUME_ML = {
    "ml": 1.0,
    "l": 1000.0,
    "fl_oz": 29.5735295625,
    "qt": 946.352946,
    "gal": 3785.411784,
}
USE_UNITS = {"g", "each"}
STATUSES = {"draft", "pending_test", "approved", "retired"}
# Product categories, in report order.
CATEGORY_ORDER = ("pastry", "sandwich", "salad", "soup", "add-on", "drink", "catering")


class DBError(Exception):
    """A data problem that makes the database unusable."""


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(value: str | None) -> float | None:
    value = (value or "").strip()
    return float(value) if value else None


def load_ingredients() -> dict[str, dict]:
    ingredients: dict[str, dict] = {}
    for row in read_csv(DB / "ingredients.csv"):
        iid = row["id"].strip()
        if iid in ingredients:
            raise DBError(f"ingredients.csv: duplicate id {iid!r}")
        row["each_g"] = num(row.get("each_g"))
        row["density_g_per_ml"] = num(row.get("density_g_per_ml"))
        row["price_ref"] = (row.get("price_ref") or "").strip() or None
        row["allergens"] = {
            a.strip() for a in (row.get("allergens") or "").split(";") if a.strip()
        }
        ingredients[iid] = row
    for iid, row in ingredients.items():
        ref = row["price_ref"]
        if ref and (ref not in ingredients or ingredients[ref]["price_ref"]):
            raise DBError(f"ingredients.csv: {iid} has an invalid price_ref {ref!r}")
        if ref and not row["each_g"]:
            raise DBError(f"ingredients.csv: {iid} uses price_ref but has no each_g")
    return ingredients


def load_prices(ingredients: dict) -> dict[tuple[str, str], dict]:
    """Return the latest price row for each (ingredient, channel)."""
    latest: dict[tuple[str, str], dict] = {}
    for line_no, row in enumerate(read_csv(DB / "ingredient_prices.csv"), start=2):
        where = f"ingredient_prices.csv line {line_no}"
        iid, channel = row["ingredient_id"].strip(), row["channel"].strip()
        unit = row["pack_unit"].strip()
        if iid not in ingredients:
            raise DBError(f"{where}: unknown ingredient {iid!r}")
        if channel not in CHANNELS:
            raise DBError(f"{where}: unknown channel {channel!r}")
        if unit not in WEIGHT_G and unit not in VOLUME_ML and unit != "each":
            raise DBError(f"{where}: unknown pack_unit {unit!r}")
        if unit in VOLUME_ML and not ingredients[iid]["density_g_per_ml"]:
            raise DBError(f"{where}: {iid} is priced by volume but has no density")
        row.update(
            pack_unit=unit,
            pack_size=float(row["pack_size"]),
            price_usd=float(row["price_usd"]),
        )
        key = (iid, channel)
        if key not in latest or row["as_of"] >= latest[key]["as_of"]:
            latest[key] = row
    return latest


def load_settings() -> dict:
    if not SETTINGS.exists():
        raise DBError("db/settings.yaml is missing")
    doc = yaml.safe_load(SETTINGS.read_text(encoding="utf-8")) or {}
    rate = (doc.get("labor") or {}).get("rate_usd_per_hour")
    if not isinstance(rate, (int, float)) or rate <= 0:
        raise DBError("db/settings.yaml: labor.rate_usd_per_hour must be a positive number")
    return doc


def load_yaml_dir(name: str) -> dict[str, dict]:
    docs: dict[str, dict] = {}
    for path in sorted((DB / name).glob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        doc["_path"] = path.relative_to(ROOT).as_posix()
        if doc.get("id") in docs:
            raise DBError(f"{doc['_path']}: duplicate id {doc.get('id')!r}")
        docs[doc["id"]] = doc
    return docs


class Book:
    """The loaded database, with costing helpers."""

    def __init__(self) -> None:
        self.settings = load_settings()
        self.labor_rate = float(self.settings["labor"]["rate_usd_per_hour"])
        self.ingredients = load_ingredients()
        self.prices = load_prices(self.ingredients)
        self.formulas = load_yaml_dir("formulas")
        products = load_yaml_dir("products")
        order = {name: rank for rank, name in enumerate(CATEGORY_ORDER)}
        self.products = dict(
            sorted(
                products.items(),
                key=lambda kv: (order.get(kv[1].get("category"), len(order)), kv[1].get("name", "")),
            )
        )
        clash = set(self.formulas) & set(self.ingredients)
        if clash:
            raise DBError(f"ids used for both a formula and an ingredient: {sorted(clash)}")
        clash = set(self.products) & (set(self.formulas) | set(self.ingredients))
        if clash:
            raise DBError(f"product ids also used for a formula or ingredient: {sorted(clash)}")
        self._check_cycles()
        self._check_product_cycles()
        self._formula_costs: dict[tuple[str, str], float | None] = {}
        self._formula_labor: dict[str, float] = {}

    def _check_cycles(self) -> None:
        """Fail if any formula uses itself, directly or through other formulas."""
        done: set[str] = set()

        def visit(fid: str, path: tuple) -> None:
            if fid in done:
                return
            if fid in path:
                raise DBError("formula cycle: " + " -> ".join(path + (fid,)))
            for line in self.formulas[fid].get("ingredients") or []:
                if line.get("item") in self.formulas:
                    visit(line["item"], path + (fid,))
            done.add(fid)

        for fid in self.formulas:
            visit(fid, ())

    def _check_product_cycles(self) -> None:
        """Fail if a bundle product contains itself, directly or through other products."""
        done: set[str] = set()

        def visit(pid: str, path: tuple) -> None:
            if pid in done:
                return
            if pid in path:
                raise DBError("product cycle: " + " -> ".join(path + (pid,)))
            for line in self.products[pid].get("build") or []:
                if line.get("item") in self.products:
                    visit(line["item"], path + (pid,))
            done.add(pid)

        for pid in self.products:
            visit(pid, ())

    # -- unit costs ---------------------------------------------------------

    def unit_costs(self, iid: str, channel: str) -> tuple[float | None, float | None]:
        """Return (usd_per_g, usd_per_each) for an ingredient in a channel."""
        ing = self.ingredients[iid]
        if ing["price_ref"]:
            _, ref_each = self.unit_costs(ing["price_ref"], channel)
            if ref_each is None:
                return None, None
            return ref_each / ing["each_g"], ref_each
        row = self.prices.get((iid, channel))
        if row is None:
            return None, None
        size, unit, price = row["pack_size"], row["pack_unit"], row["price_usd"]
        if unit == "each":
            per_each = price / size
            return (per_each / ing["each_g"] if ing["each_g"] else None), per_each
        if unit in WEIGHT_G:
            grams = size * WEIGHT_G[unit]
        else:
            grams = size * VOLUME_ML[unit] * ing["density_g_per_ml"]
        per_g = price / grams
        return per_g, per_g * ing["each_g"] if ing["each_g"] else None

    def line_grams(self, line: dict) -> float | None:
        item, qty = line["item"], float(line["qty"])
        if line["unit"] == "g":
            return qty
        if item in self.products:
            return None
        if item in self.ingredients:
            each_g = self.ingredients[item]["each_g"]
            return qty * each_g if each_g else None
        yld = self.formulas[item]["yield"]
        return qty * yld["grams"] / yld["units"]

    def line_cost(self, line: dict, channel: str, stack: tuple = ()) -> float | None:
        item, qty, unit = line["item"], float(line["qty"]), line["unit"]
        if item in self.ingredients:
            per_g, per_each = self.unit_costs(item, channel)
            rate = per_g if unit == "g" else per_each
            return None if rate is None else rate * qty
        if item in self.products:
            inner = self.product_food_cost(item, channel)
            return None if inner is None else inner * qty
        batch = self.formula_cost(item, channel, stack)
        if batch is None:
            return None
        yld = self.formulas[item]["yield"]
        return batch * qty / (yld["grams"] if unit == "g" else yld["units"])

    def formula_cost(self, fid: str, channel: str, stack: tuple = ()) -> float | None:
        key = (fid, channel)
        if key in self._formula_costs:
            return self._formula_costs[key]
        if fid in stack:
            raise DBError("formula cycle: " + " -> ".join(stack + (fid,)))
        total: float | None = 0.0
        for line in self.formulas[fid]["ingredients"]:
            cost = self.line_cost(line, channel, stack + (fid,))
            if cost is None:
                total = None
                break
            total += cost
        self._formula_costs[key] = total
        return total

    def signed_line_cost(self, line: dict, channel: str) -> float | None:
        """A line's cost, negative for a credit line (something the product replaces)."""
        cost = self.line_cost(line, channel)
        return None if cost is None else (-cost if line.get("credit") else cost)

    def is_packaging(self, item: str) -> bool:
        return item in self.ingredients and self.ingredients[item]["category"] == "packaging"

    def product_food_cost(self, pid: str, channel: str) -> float | None:
        """Food cost of one unit with no waste allowance and no packaging.

        This is what a product costs when it goes inside a bundle, such as a
        catering box, which has its own packaging and its own waste allowance.
        """
        total = 0.0
        for line in self.products[pid]["build"]:
            if self.is_packaging(line["item"]):
                continue
            cost = self.signed_line_cost(line, channel)
            if cost is None:
                return None
            total += cost
        return total

    def product_cost_parts(self, pid: str, channel: str) -> tuple[float, float] | None:
        """Return (food cost including waste, packaging cost) for one unit.

        The waste allowance applies to food lines only, not packaging.
        """
        product = self.products[pid]
        food = packaging = 0.0
        for line in product["build"]:
            cost = self.signed_line_cost(line, channel)
            if cost is None:
                return None
            if self.is_packaging(line["item"]):
                packaging += cost
            else:
                food += cost
        return food * (1 + product.get("waste_pct", 0) / 100), packaging

    # -- labor --------------------------------------------------------------

    def formula_labor(self, fid: str) -> float:
        """Hands-on minutes for one batch of a formula as written, sub-recipes included.

        labor.batch_min is the hands-on time for one production run, which
        makes labor.production_batches batches of the formula at once.
        """
        if fid in self._formula_labor:
            return self._formula_labor[fid]
        doc = self.formulas[fid]
        lab = doc.get("labor") or {}
        own = float(lab.get("batch_min", 0)) / float(lab.get("production_batches", 1) or 1)
        total = own + sum(self.line_labor(line) for line in doc["ingredients"])
        self._formula_labor[fid] = total
        return total

    def line_labor(self, line: dict) -> float:
        """Hands-on minutes carried by one formula or product line."""
        item, qty, unit = line["item"], float(line["qty"]), line["unit"]
        if line.get("credit") or item in self.ingredients:
            return 0.0
        if item in self.products:
            return self.product_labor(item, with_waste=False) * qty
        yld = self.formulas[item]["yield"]
        return self.formula_labor(item) * qty / (yld["grams"] if unit == "g" else yld["units"])

    def product_labor(self, pid: str, with_waste: bool = True) -> float:
        """Hands-on minutes per unit sold: the product's own steps plus its sub-recipes."""
        doc = self.products[pid]
        own = float((doc.get("labor") or {}).get("unit_min", 0))
        total = own + sum(self.line_labor(line) for line in doc["build"])
        return total * (1 + doc.get("waste_pct", 0) / 100) if with_waste else total

    def labor_cost(self, minutes: float) -> float:
        return minutes * self.labor_rate / 60

    def labor_breakdown(self, pid: str) -> list[tuple[str, float]]:
        """Where a product's minutes come from, before the waste allowance."""
        doc = self.products[pid]
        parts = []
        for line in doc["build"]:
            minutes = self.line_labor(line)
            if minutes > 0:
                parts.append((item_name(self, line["item"]), minutes))
        own = float((doc.get("labor") or {}).get("unit_min", 0))
        if own:
            parts.append(("own steps", own))
        return parts

    def product_cost(self, pid: str, channel: str) -> float | None:
        parts = self.product_cost_parts(pid, channel)
        return None if parts is None else sum(parts)

    def has_packaging(self, pid: str) -> bool:
        return any(self.is_packaging(line["item"]) for line in self.products[pid]["build"])

    def allergens(self, item: str) -> set[str]:
        if item in self.ingredients:
            return set(self.ingredients[item]["allergens"])
        doc = self.formulas.get(item) or self.products[item]
        lines = doc.get("ingredients") or doc.get("build")
        found: set[str] = set()
        for line in lines:
            if not line.get("credit"):
                found |= self.allergens(line["item"])
        return found

    # -- validation ---------------------------------------------------------

    def validate(self) -> tuple[list[str], list[str]]:
        errors: list[str] = []
        warnings: list[str] = []

        def is_number(value, minimum: float = 0.0, strict: bool = False) -> bool:
            ok = isinstance(value, (int, float)) and not isinstance(value, bool)
            return ok and (value > minimum if strict else value >= minimum)

        def check_lines(doc: dict, key: str, in_product: bool = False) -> None:
            lines = doc.get(key)
            if not lines:
                errors.append(f"{doc['_path']}: '{key}' is empty")
                return
            for line in lines:
                item, unit = line.get("item"), line.get("unit")
                where = f"{doc['_path']}: {item}"
                known = item in self.ingredients or item in self.formulas or (in_product and item in self.products)
                if not known:
                    errors.append(f"{where}: unknown item")
                    continue
                if unit not in USE_UNITS:
                    errors.append(f"{where}: unit must be one of {sorted(USE_UNITS)}")
                    continue
                if not isinstance(line.get("qty"), (int, float)) or line["qty"] <= 0:
                    errors.append(f"{where}: qty must be a positive number")
                    continue
                if line.get("credit") and (not in_product or item not in self.ingredients or self.is_packaging(item)):
                    errors.append(f"{where}: a credit line must be a food ingredient in a product build")
                if item in self.products and unit != "each":
                    errors.append(f"{where}: a product inside a bundle is counted with unit 'each'")
                if item in self.formulas and unit == "each" and not self.formulas[item]["yield"].get("units"):
                    errors.append(f"{where}: used by count but the formula has no yield.units")
                if item not in self.ingredients:
                    continue
                for channel, label in CHANNELS.items():
                    per_g, per_each = self.unit_costs(item, channel)
                    if (per_g, per_each) == (None, None):
                        warnings.append(f"{where}: no {label} price")
                    elif (per_g if unit == "g" else per_each) is None:
                        errors.append(f"{where}: its {label} price can't be converted to '{unit}'; add each_g")

        for fid, doc in self.formulas.items():
            for field in ("name", "kind", "status", "version", "yield", "ingredients"):
                if field not in doc:
                    errors.append(f"{doc['_path']}: missing '{field}'")
            if doc.get("status") not in STATUSES:
                errors.append(f"{doc['_path']}: status must be one of {sorted(STATUSES)}")
            if not (doc.get("yield") or {}).get("grams"):
                errors.append(f"{doc['_path']}: yield.grams is required")
                continue
            lab = doc.get("labor")
            if lab is None:
                warnings.append(f"{doc['_path']}: no labor.batch_min, so its prep minutes count as zero")
            elif not is_number(lab.get("batch_min")) or not is_number(lab.get("production_batches", 1), strict=True):
                errors.append(f"{doc['_path']}: labor.batch_min must be 0 or more and labor.production_batches above 0")
            check_lines(doc, "ingredients")
            grams = [self.line_grams(line) for line in doc.get("ingredients") or []]
            if None not in grams and doc["yield"]["grams"] > sum(grams) + 0.5:
                errors.append(f"{doc['_path']}: yield ({doc['yield']['grams']} g) exceeds inputs ({sum(grams):g} g)")

        for pid, doc in self.products.items():
            for field in ("name", "status", "version", "build", "pricing"):
                if field not in doc:
                    errors.append(f"{doc['_path']}: missing '{field}'")
            if doc.get("status") not in STATUSES:
                errors.append(f"{doc['_path']}: status must be one of {sorted(STATUSES)}")
            if doc.get("category") not in CATEGORY_ORDER:
                errors.append(f"{doc['_path']}: category must be one of {list(CATEGORY_ORDER)}")
            lab = doc.get("labor")
            if lab is None:
                warnings.append(f"{doc['_path']}: no labor.unit_min, so its own prep minutes count as zero")
            elif not is_number(lab.get("unit_min")):
                errors.append(f"{doc['_path']}: labor.unit_min must be 0 or more")
            if "par_daily" in doc and not is_number(doc["par_daily"]):
                errors.append(f"{doc['_path']}: par_daily must be 0 or more")
            check_lines(doc, "build", in_product=True)
            if errors:
                continue
            declared = set(doc.get("allergens_declared") or [])
            computed = self.allergens(pid)
            if declared != computed:
                errors.append(
                    f"{doc['_path']}: allergens_declared {sorted(declared)} "
                    f"does not match ingredients {sorted(computed)}"
                )
            for line in doc["build"]:
                sub = self.formulas.get(line["item"])
                if sub and doc["status"] == "approved" and sub["status"] != "approved":
                    warnings.append(f"{doc['_path']}: approved product uses {sub['status']} formula {sub['id']}")
        return errors, warnings


# -- report ------------------------------------------------------------------


def money(value: float | None) -> str:
    if value is None:
        return "n/a"
    if 0 < value < 0.005:
        return "<$0.01"
    if value < 0:
        return f"−${-value:,.2f}"
    return f"${value:,.2f}"


def minutes(value: float) -> str:
    return f"{value:,.1f} min"


def qty(value: float, unit: str) -> str:
    if unit == "each":
        return f"{value:g} each"
    return f"{value:,.1f} g".replace(".0 g", " g")


def item_name(book: Book, item: str) -> str:
    if item in book.ingredients:
        return book.ingredients[item]["name"]
    if item in book.products:
        return f"{book.products[item]['name']} (product)"
    return f"{book.formulas[item]['name']} (formula)"


def render_labor(book: Book) -> list[str]:
    """The prep-labor section: minutes per unit, daily hours at par, and where the minutes go."""
    ch = "distributor_est"
    rate = book.labor_rate
    rows = []
    for pid, doc in book.products.items():
        price = doc["pricing"].get("suggested_retail_usd") or 0
        par = float(doc.get("par_daily") or 0)
        mins = book.product_labor(pid)
        cost = book.product_cost(pid, ch) or 0
        prime = cost + book.labor_cost(mins)
        rows.append((pid, doc, price, par, mins, cost, prime, mins * par / 60))
    rows.sort(key=lambda r: -r[7])
    total_hours = sum(r[7] for r in rows)
    sales = sum(r[2] * r[3] for r in rows)
    goods = sum(r[5] * r[3] for r in rows)
    labor_usd = total_hours * rate
    out = [
        "",
        "## Prep labor",
        "",
        f"Hands-on minutes per unit sold at ${rate:,.2f} an hour (`db/settings.yaml`), including each "
        "sub-recipe's share of its production run and the waste allowance. Proofing, baking, cooling, "
        "steeping and brewing time isn't counted, and neither is taking orders or bagging. Daily hours "
        "use the planning par in each product file (`par_daily`); change the pars to match real sales.",
        "",
        "| Product | Category | Par/day | Min/unit | Labor $/unit | Prime cost % of price, distributor | Labor h/day | Share of hours |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for pid, doc, price, par, mins, cost, prime, hours in rows:
        share = f"{100 * hours / total_hours:.0f}%" if total_hours else "n/a"
        prime_pct = f"{100 * prime / price:.0f}%" if price else "n/a"
        out.append(
            f"| {doc['name']} | {doc.get('category', '')} | {par:g} | {mins:.1f} | "
            f"{money(book.labor_cost(mins))} | {prime_pct} | {hours:.1f} | {share} |"
        )
    out.append(f"| **Total** | | | | | | **{total_hours:.1f}** | 100% |")
    if sales:
        out += [
            "",
            f"At these pars: about {money(sales)} of sales a day and {total_hours:.1f} hands-on hours "
            f"({money(labor_usd)}, {100 * labor_usd / sales:.0f}% of sales). Food and packaging at "
            f"distributor prices are {100 * goods / sales:.0f}% of sales, so food, packaging and prep "
            f"labor together are {100 * (goods + labor_usd) / sales:.0f}%. Counter staff, cleaning, "
            "management and payroll overhead beyond the hourly rate come on top.",
        ]
    out += [
        "",
        "### Where the minutes go: baked goods and sandwiches",
        "",
        "Minutes per unit before the waste allowance. \"Own steps\" are the shaping, finishing or "
        "assembly in the product file; the rest is each sub-recipe's share.",
        "",
        "| Product | Min/unit | Breakdown |",
        "|---|---|---|",
    ]
    for pid, doc in book.products.items():
        if doc.get("category") not in ("pastry", "sandwich"):
            continue
        parts = book.labor_breakdown(pid)
        total = sum(m for _, m in parts)
        detail = "; ".join(f"{name.replace(' (formula)', '')} {m:.2f}" for name, m in parts)
        out.append(f"| {doc['name']} | {total:.1f} | {detail} |")
    return out


def render(book: Book, warnings: list[str]) -> str:
    out: list[str] = []
    as_of = max(row["as_of"] for row in book.prices.values())
    labels = list(CHANNELS.values())
    out += [
        "# Costing report",
        "",
        "Generated by `tools/costing.py` from the files in `db/`. Do not edit by hand; "
        "change the data and rerun the script.",
        "",
        f"Prices as of {as_of}. **Retail est.** = US grocery or small-pack estimates; "
        "**Distributor est.** = foodservice and wholesale estimates. Both are estimates until "
        "replaced with real quotes in `db/ingredient_prices.csv`. Unit costs cover ingredients "
        "plus any packaging listed in the build. Prep labor is shown separately (see Prep labor) "
        "and added into prime cost; energy is not included.",
        "",
        "## Products",
        "",
        f"| Product | Category | Status | Price | Unit cost, {labels[0].lower()} | "
        f"Unit cost, {labels[1].lower()} | Packaging in unit cost | Cost % of price | Allergens |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for pid, doc in book.products.items():
        costs = [book.product_cost(pid, ch) for ch in CHANNELS]
        price = doc["pricing"].get("suggested_retail_usd")
        pct = " / ".join("n/a" if c is None or not price else f"{100 * c / price:.0f}%" for c in costs)
        if book.has_packaging(pid):
            parts = [book.product_cost_parts(pid, ch) for ch in CHANNELS]
            pack = " / ".join(money(None if p is None else p[1]) for p in parts)
        else:
            pack = "none"
        out.append(
            f"| {doc['name']} | {doc.get('category', '')} | {doc['status']} | {money(price)} | "
            f"{money(costs[0])} | {money(costs[1])} | {pack} | {pct} | "
            f"{', '.join(sorted(book.allergens(pid))) or 'none'} |"
        )
    out += ["", "Packaging and cost % are shown retail est. / distributor est."]

    out += render_labor(book)

    for pid, doc in book.products.items():
        out += [
            "",
            f"### {doc['name']} (`{pid}`), per unit",
            "",
            f"| Item | Qty | {labels[0]} | {labels[1]} |",
            "|---|---|---|---|",
        ]
        food = [0.0 for _ in CHANNELS]
        for line in doc["build"]:
            costs = [book.signed_line_cost(line, ch) for ch in CHANNELS]
            if not book.is_packaging(line["item"]):
                food = [s + (c or 0) for s, c in zip(food, costs)]
            label = item_name(book, line["item"]) + (", replaced (credit)" if line.get("credit") else "")
            out.append(
                f"| {label} | {qty(float(line['qty']), line['unit'])} | "
                f"{money(costs[0])} | {money(costs[1])} |"
            )
        waste = doc.get("waste_pct", 0)
        out.append(
            f"| Waste allowance (food only) | {waste:g}% | {money(food[0] * waste / 100)} | "
            f"{money(food[1] * waste / 100)} |"
        )
        totals = [book.product_cost(pid, ch) for ch in CHANNELS]
        out.append(f"| **Unit cost** | | **{money(totals[0])}** | **{money(totals[1])}** |")
        mins = book.product_labor(pid)
        lab = book.labor_cost(mins)
        out.append(f"| Prep labor | {minutes(mins)} | {money(lab)} | {money(lab)} |")
        prime = [None if t is None else t + lab for t in totals]
        out.append(f"| **Prime cost (unit cost + labor)** | | **{money(prime[0])}** | **{money(prime[1])}** |")
        n = doc.get("batch_units") or 1
        if n > 1:
            needs = ", ".join(
                f"{item_name(book, line['item'])} {qty(float(line['qty']) * n, line['unit'])}"
                for line in doc["build"]
            )
            out += ["", f"Batch of {n}: {needs}."]

    out += ["", "## Formulas"]
    for fid, doc in book.formulas.items():
        dough = doc["kind"] in ("dough", "batter")  # show baker's %
        flour = sum(
            float(line["qty"])
            for line in doc["ingredients"]
            if line["unit"] == "g"
            and line["item"] in book.ingredients
            and book.ingredients[line["item"]]["category"] == "flour"
        )
        staged = any(line.get("stage") for line in doc["ingredients"])
        head = ("| Stage " if staged else "") + "| Item | Qty |" + (" Baker's % |" if dough else "")
        out += [
            "",
            f"### {doc['name']} (`{fid}`), {doc['status']}",
            "",
            f"{head} {labels[0]} | {labels[1]} |",
            "|" + "---|" * (head.count("|") + 1),
        ]
        for line in doc["ingredients"]:
            costs = [book.line_cost(line, ch) for ch in CHANNELS]
            stage = f"| {line.get('stage', '')} " if staged else ""
            bakers = ""
            if dough:
                bakers = f" {100 * float(line['qty']) / flour:.1f}% |" if line["unit"] == "g" and flour else " |"
            out.append(
                f"{stage}| {item_name(book, line['item'])} | "
                f"{qty(float(line['qty']), line['unit'])} |{bakers} {money(costs[0])} | {money(costs[1])} |"
            )
        totals = [book.formula_cost(fid, ch) for ch in CHANNELS]
        inputs = sum(book.line_grams(line) or 0 for line in doc["ingredients"])
        yld = doc["yield"]
        lead = "| **Batch** | " if staged else "| **Batch** "
        pad = " |" if dough else ""
        out.append(
            f"{lead}| **{inputs:,.0f} g in, {yld['grams']:,} g out** |{pad} "
            f"**{money(totals[0])}** | **{money(totals[1])}** |"
        )
        per = [None if t is None else 1000 * t / yld["grams"] for t in totals]
        line = f"Cost per kg of yield: {money(per[0])} retail est., {money(per[1])} distributor est."
        if yld.get("units"):
            each = [None if t is None else t / yld["units"] for t in totals]
            line += f" Per unit: {money(each[0])} / {money(each[1])}."
        out += ["", line]
        lab = doc.get("labor")
        if lab:
            runs = float(lab.get("production_batches", 1) or 1)
            own = float(lab.get("batch_min", 0)) / runs
            out += [
                "",
                f"Prep labor: {float(lab.get('batch_min', 0)):g} hands-on min per production run of "
                f"{runs:g} batch{'es' if runs != 1 else ''}, so {own:.1f} min per batch; "
                f"{book.formula_labor(fid):.1f} min per batch including sub-recipes.",
            ]

    out += [
        "",
        "## Ingredient prices",
        "",
        "Latest price per ingredient and channel. Sources are in `db/ingredient_prices.csv`.",
        "",
        f"| Ingredient | Id | {labels[0]} per kg | {labels[1]} per kg | Per each (retail / distributor) |",
        "|---|---|---|---|---|",
    ]
    for iid, ing in book.ingredients.items():
        costs = [book.unit_costs(iid, ch) for ch in CHANNELS]
        per_kg = [money(None if g is None else g * 1000) for g, _ in costs]
        each = " / ".join(money(e) for _, e in costs) if ing["each_g"] else ""
        out.append(f"| {ing['name']} | `{iid}` | {per_kg[0]} | {per_kg[1]} | {each} |")

    if warnings:
        out += ["", "## Warnings", ""] + [f"- {w}" for w in warnings]
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate only; do not write the report")
    args = parser.parse_args()
    try:
        book = Book()
        errors, warnings = book.validate()
    except (DBError, KeyError, ValueError, yaml.YAMLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    if not args.check:
        REPORT.write_text(render(book, warnings), encoding="utf-8")
        print(f"wrote {REPORT.relative_to(ROOT)}")
    else:
        print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
