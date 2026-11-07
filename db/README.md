# Formula and ingredient database

The bakery's source of truth for ingredients, prices, formulas and approved products. Data lives in CSV and YAML so it can be edited in any text editor or on GitHub. `tools/costing.py` checks it and regenerates the cost report.

## Approved products

| Product | Suggested price | Notes |
|---|---|---|
| [Cinnamon Roll](products/cinnamon_roll.yaml) | $4.75 | 4 oz finished. Approved 2026-11-06; the cooked buttermilk glaze is still pending its first test bake |
| [Breakfast Sandwich](products/breakfast_sandwich.yaml) | $8.50 | Fried egg, cheddar and harissa on the house sandwich roll. Approved 2026-11-06 |
| [Fennel Sausage Breakfast Sandwich](products/breakfast_sandwich_fennel_sausage.yaml) | $10.00 | The breakfast sandwich plus a 2 oz fennel pork sausage patty. Approved 2026-11-07; the sausage hasn't been chosen or test-built yet |

Costs are in [`costing.md`](costing.md); the reasoning behind the prices is in [`pricing.md`](pricing.md).

## Layout

| Path | Holds |
|---|---|
| `ingredients.csv` | Ingredient master: id, name, category, allergens, spec, unit weight, density |
| `ingredient_prices.csv` | Dated price quotes per ingredient and channel; the newest `as_of` per channel wins |
| `formulas/*.yaml` | Sub-recipes (dough, filling, glaze, roll): quantities, method, specs, history |
| `products/*.yaml` | What we sell: build per unit, production steps, QA checks, declared allergens, price, what's tested and what's pending |
| `costing.md` | Generated cost report. Do not edit by hand |
| `pricing.md` | Retail price recommendations and their market basis |
| `../tools/costing.py` | Validates everything and regenerates `costing.md` |

## Run the checks

```bash
pip install pyyaml
```

```bash
python3 tools/costing.py
```

```bash
python3 tools/costing.py --check
```

The first command validates and rewrites `costing.md`. `--check` validates only and exits non-zero on any error. Run it after every change and commit the regenerated report with the data.

The script stops on unknown items, bad units, a yield larger than its inputs, formula cycles, missing pack weights or densities, and declared allergens that don't match the ingredients. It warns, without failing, when an approved product uses a formula that isn't approved yet, or when an ingredient has no price in a channel.

## Conventions

- **Ids:** lowercase `snake_case`. Ingredients and formulas share one namespace, so a product or formula line can point at either. Never rename an id that's in use; retire it and add a new one.
- **Quantities:** formula and product lines use grams (`g`) or counts (`each`).
- **Price packs:** `pack_unit` can be `g`, `kg`, `oz`, `lb`, `ml`, `l`, `fl_oz`, `qt`, `gal` or `each`. Volume packs need `density_g_per_ml`; count packs need `each_g`.
- **`price_ref`:** costs an item as one unit of another. An egg yolk costs one whole egg, and its white goes to egg wash.
- **Allergens:** semicolon-separated, using US major-allergen names (milk, egg, wheat, soy, peanuts, tree nuts, fish, shellfish, sesame). Every product must list `allergens_declared`, and it must match its ingredients.
- **Status:** `draft` → `pending_test` → `approved` → `retired`. Approve a formula only after a test bake, and say what was tested in `history`.
- **Changes:** for any change to an approved formula or product, bump `version` and add a `history` entry.
- **Formula yields:** `yield.grams` is what comes out after cooking or trimming. Add `yield.units` when the formula makes countable pieces.

## Updating prices

Add a row to `ingredient_prices.csv` with a newer `as_of` date and keep the old rows as history. There are two channels today: `retail_est` (US grocery estimates) and `distributor_est` (foodservice estimates). Replace the estimates with real invoices and quotes as they arrive. To track a real supplier as its own channel, add it to `CHANNELS` in `tools/costing.py`.

## Adding a formula or product

1. Copy an existing YAML file in `formulas/` or `products/` and give it a new `id`.
2. Point each line's `item` at an ingredient or formula id. Add any new ingredient to `ingredients.csv`, with a price in each channel.
3. Run `python3 tools/costing.py` and fix anything it reports.
