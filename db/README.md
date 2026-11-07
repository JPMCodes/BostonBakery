# Formula and ingredient database

The bakery's source of truth for ingredients, prices, formulas and approved products. Data lives in CSV and YAML so it can be edited in any text editor or on GitHub. `tools/costing.py` checks it and regenerates the cost report.

## Products

| Product | Status | Suggested price | Notes |
|---|---|---|---|
| [Cinnamon Roll](products/cinnamon_roll.yaml) | approved | $4.75 | 4 oz finished. Approved 2026-11-06; the cooked buttermilk glaze is still pending its first test bake |
| [Blueberry Scone](products/blueberry_scone.yaml) | pending_test | $4.50 | 95 g of dough with fresh and dried blueberries, lemon and sour cream, under a brown-butter crumb; pending a test bake |
| [Mini Vanilla Scone](products/mini_vanilla_scone.yaml) | pending_test | $2.25 | 31 g vanilla bean cream scone under a vanilla bean glaze, 24 to a batch; pending a test bake |
| [Breakfast Sandwich](products/breakfast_sandwich.yaml) | approved | $8.50 | Fried egg, cheddar and harissa on the house sandwich roll. Approved 2026-11-06 |
| [Fennel Sausage Breakfast Sandwich](products/breakfast_sandwich_fennel_sausage.yaml) | approved | $10.25 | The breakfast sandwich plus a 2 oz fennel pork sausage patty. Approved 2026-11-07; the sausage hasn't been chosen or test-built yet |
| [Fennel Herb Salad Bowl](products/fennel_herb_bowl.yaml) | draft | $13.50 | Farro, arugula, shaved fennel, orange, parsley, dill and mint, Parmesan and pepitas; lemon-Dijon vinaigrette on the side. Same-day sale |
| [Cilantro Lime Quinoa Salad](products/cilantro_lime_quinoa_salad.yaml) | draft | $12.50 | Quinoa, black beans, roasted corn, tomatoes, red pepper, cotija and pepitas; cilantro-lime vinaigrette on the side. Holds 2 days; made without wheat |
| [Chicken Salad Scoop](products/add_chicken_salad.yaml) | draft | $3.50 | Add-on for either salad: 100 g of lemon-herb chicken salad in its own lidded, labeled cup |
| [Tuna Salad Scoop](products/add_tuna_salad.yaml) | draft | $3.50 | Add-on for either salad: 100 g of albacore tuna salad in its own lidded, labeled cup |
| [Drip Coffee (12 oz)](products/drip_coffee.yaml) | pending_test | $3.50 | Specialty filter coffee from the batch brewer |
| [Iced Coffee (16 oz cold brew)](products/iced_coffee.yaml) | pending_test | $4.00 | House cold brew, 1:1 with water over ice |
| [Espresso (double)](products/espresso.yaml) | pending_test | $3.50 | 18 g in, 36 g out |
| [Latte (12 oz)](products/latte.yaml) | pending_test | $4.75 | Double espresso and steamed whole milk |
| [Iced Latte (16 oz)](products/iced_latte.yaml) | pending_test | $5.00 | Double espresso over cold milk and ice |
| [Matcha Latte (12 oz)](products/matcha_latte.yaml) | pending_test | $5.25 | 3 g premium latte-grade matcha, unsweetened |
| [Chai Latte (12 oz)](products/chai_latte.yaml) | pending_test | $4.75 | Premium chai concentrate 1:1 with milk |

The drinks stay `pending_test` until the roaster, matcha and chai suppliers are chosen and the espresso is dialed in. The salads and their add-ons are `draft`: written and costed, not yet made in the kitchen. Costs are in [`costing.md`](costing.md); the reasoning behind the prices is in [`pricing.md`](pricing.md).

## Layout

| Path | Holds |
|---|---|
| `ingredients.csv` | Ingredient master: id, name, category, allergens, spec, unit weight, density |
| `ingredient_prices.csv` | Dated price quotes per ingredient and channel; the newest `as_of` per channel wins |
| `formulas/*.yaml` | Sub-recipes (dough, filling, glaze, roll, cooked grains, dressings, protein salads): quantities, method, specs, history |
| `products/*.yaml` | What we sell: build per unit, production steps, QA checks, declared allergens, price, what's tested and what's pending |
| `costing.md` | Generated cost report. Do not edit by hand |
| `pricing.md` | Retail price recommendations and their market basis |
| `viewer.html` | Generated Formula Book viewer: products, formulas and ingredients with costs, prices and methods. Open it in any browser. Do not edit by hand |
| `../tools/costing.py` | Validates everything and regenerates `costing.md` |
| `../tools/build_viewer.py` | Regenerates `viewer.html` from the same data |

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

```bash
python3 tools/build_viewer.py
```

This rebuilds `viewer.html`, a single self-contained page with the data built in. It works offline, with a switch between retail and distributor costs, search, and tabs for products, formulas and ingredients. Rebuild it after every data change too.

The script stops on unknown items, bad units, a yield larger than its inputs, formula cycles, missing pack weights or densities, and declared allergens that don't match the ingredients. It warns, without failing, when an approved product uses a formula that isn't approved yet, or when an ingredient has no price in a channel.

## Conventions

- **Ids:** lowercase `snake_case`. Ingredients and formulas share one namespace, so a product or formula line can point at either. Never rename an id that's in use; retire it and add a new one.
- **Quantities:** formula and product lines use grams (`g`) or counts (`each`).
- **Price packs:** `pack_unit` can be `g`, `kg`, `oz`, `lb`, `ml`, `l`, `fl_oz`, `qt`, `gal` or `each`. Volume packs need `density_g_per_ml`; count packs need `each_g`.
- **Product categories:** every product has a `category` of `pastry`, `sandwich`, `salad`, `add-on` or `drink`, which sets its place in the cost report.
- **Packaging:** cups, lids and other packaging are ingredients with `category` `packaging`, priced per `each`. The report shows them separately, and a product's `waste_pct` applies to its food lines only, not its packaging. Food products are costed with their to-go packaging; for-here orders on a plate skip it.
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
