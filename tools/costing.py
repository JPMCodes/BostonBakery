#!/usr/bin/env python3
"""Validate the bakery formula database and regenerate db/costing.md.

Usage:
    python3 tools/costing.py           # validate, then write db/costing.md
    python3 tools/costing.py --check   # validate only; exit 1 on any error

Reads db/ingredients.csv, db/ingredient_prices.csv, db/formulas/*.yaml and
db/products/*.yaml. Requires PyYAML (pip install pyyaml).
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
CATEGORY_ORDER = ("pastry", "sandwich", "salad", "add-on", "drink")


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
        self._check_cycles()
        self._formula_costs: dict[tuple[str, str], float | None] = {}

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

    def is_packaging(self, item: str) -> bool:
        return item in self.ingredients and self.ingredients[item]["category"] == "packaging"

    def product_cost_parts(self, pid: str, channel: str) -> tuple[float, float] | None:
        """Return (food cost including waste, packaging cost) for one unit.

        The waste allowance applies to food lines only, not packaging.
        """
        product = self.products[pid]
        food = packaging = 0.0
        for line in product["build"]:
            cost = self.line_cost(line, channel)
            if cost is None:
                return None
            if self.is_packaging(line["item"]):
                packaging += cost
            else:
                food += cost
        return food * (1 + product.get("waste_pct", 0) / 100), packaging

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
            found |= self.allergens(line["item"])
        return found

    # -- validation ---------------------------------------------------------

    def validate(self) -> tuple[list[str], list[str]]:
        errors: list[str] = []
        warnings: list[str] = []

        def check_lines(doc: dict, key: str) -> None:
            lines = doc.get(key)
            if not lines:
                errors.append(f"{doc['_path']}: '{key}' is empty")
                return
            for line in lines:
                item, unit = line.get("item"), line.get("unit")
                where = f"{doc['_path']}: {item}"
                if item not in self.ingredients and item not in self.formulas:
                    errors.append(f"{where}: unknown item")
                    continue
                if unit not in USE_UNITS:
                    errors.append(f"{where}: unit must be one of {sorted(USE_UNITS)}")
                    continue
                if not isinstance(line.get("qty"), (int, float)) or line["qty"] <= 0:
                    errors.append(f"{where}: qty must be a positive number")
                    continue
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
            check_lines(doc, "build")
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
    return f"${value:,.2f}"


def qty(value: float, unit: str) -> str:
    if unit == "each":
        return f"{value:g} each"
    return f"{value:,.1f} g".replace(".0 g", " g")


def item_name(book: Book, item: str) -> str:
    if item in book.ingredients:
        return book.ingredients[item]["name"]
    return f"{book.formulas[item]['name']} (formula)"


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
        "plus any packaging listed in the build; labor and energy are not included.",
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
            pack = "not specified*"
        out.append(
            f"| {doc['name']} | {doc.get('category', '')} | {doc['status']} | {money(price)} | "
            f"{money(costs[0])} | {money(costs[1])} | {pack} | {pct} | "
            f"{', '.join(sorted(book.allergens(pid))) or 'none'} |"
        )
    if not all(book.has_packaging(pid) for pid in book.products):
        out += [
            "",
            "Packaging and cost % are shown retail est. / distributor est. *Food packaging isn't "
            "in the builds yet; `pricing.md` assumes $0.25 per item.",
        ]

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
            costs = [book.line_cost(line, ch) for ch in CHANNELS]
            if not book.is_packaging(line["item"]):
                food = [s + (c or 0) for s, c in zip(food, costs)]
            out.append(
                f"| {item_name(book, line['item'])} | {qty(float(line['qty']), line['unit'])} | "
                f"{money(costs[0])} | {money(costs[1])} |"
            )
        waste = doc.get("waste_pct", 0)
        out.append(
            f"| Waste allowance (food only) | {waste:g}% | {money(food[0] * waste / 100)} | "
            f"{money(food[1] * waste / 100)} |"
        )
        totals = [book.product_cost(pid, ch) for ch in CHANNELS]
        out.append(f"| **Unit cost** | | **{money(totals[0])}** | **{money(totals[1])}** |")
        n = doc.get("batch_units") or 1
        if n > 1:
            needs = ", ".join(
                f"{item_name(book, line['item'])} {qty(float(line['qty']) * n, line['unit'])}"
                for line in doc["build"]
            )
            out += ["", f"Batch of {n}: {needs}."]

    out += ["", "## Formulas"]
    for fid, doc in book.formulas.items():
        dough = doc["kind"] == "dough"
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
