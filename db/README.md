# Formula and ingredient database

The bakery's source of truth for ingredients, prices, formulas and approved products. Data lives in CSV and YAML so it can be edited in any text editor or on GitHub. `tools/costing.py` checks it and regenerates the cost report.

## Products

| Product | Status | Suggested price | Notes |
|---|---|---|---|
| [Cinnamon Roll](products/cinnamon_roll.yaml) | approved | $4.75 | 4 oz finished. Approved 2026-11-06; the cooked buttermilk glaze is still pending its first test bake |
| [Blueberry Scone](products/blueberry_scone.yaml) | pending_test | $4.50 | 95 g of dough with fresh and dried blueberries, lemon and sour cream, under a brown-butter crumb; pending a test bake |
| [Mini Vanilla Scone](products/mini_vanilla_scone.yaml) | pending_test | $2.25 | 31 g vanilla bean cream scone under a vanilla bean glaze, 24 to a batch; pending a test bake |
| [Sour Cream Coffee Cake Slice](products/coffee_cake_slice.yaml) | draft | $4.50 | All-butter sour cream coffee cake with a toasted walnut-cinnamon ribbon and a brown-butter streusel top, after the Original Boston Coffee Cake; 16 slices per 12-cup bundt |
| [Blueberry Muffin](products/blueberry_muffin.yaml) | draft | $4.50 | Jordan Marsh-style: buttery batter streaked with mashed berries, packed with whole fresh blueberries, under a turbinado sugar crust; 130 g of batter in a tulip liner |
| [Chocolate Chip Walnut Cookie](products/cookie_chocolate_chip.yaml) | draft | $4.50 | Levain-style 6 oz cookie, baked from frozen dough in rounds all day |
| [Brownie](products/brownie.yaml) | draft | $4.50 | Thick fudgy brownie with bittersweet chocolate, Dutch cocoa, a shot of house espresso and chips; 16 to a quarter-sheet pan |
| [Breakfast Sandwich](products/breakfast_sandwich.yaml) | approved | $8.50 | Fried egg, cheddar and harissa on the house sandwich roll. Approved 2026-11-06 |
| [Fennel Sausage Breakfast Sandwich](products/breakfast_sandwich_fennel_sausage.yaml) | approved | $10.25 | The breakfast sandwich plus a 2 oz fennel pork sausage patty. Approved 2026-11-07; the sausage hasn't been chosen or test-built yet |
| [Harissa Chicken Sandwich](products/harissa_chicken_sandwich.yaml) | draft | $12.50 | Roast chicken, harissa mayo, arugula and pickled red onion on a nigella-seeded oval house roll |
| [Ham, Cheddar & Olive Tapenade](products/ham_cheddar_tapenade.yaml) | draft | $12.50 | Hardwood-smoked ham, melted cheddar, house olive tapenade and arugula on a cheddar-crusted oval house roll |
| [Fennel Herb Salad Bowl](products/fennel_herb_bowl.yaml) | draft | $12.50 | Farro, arugula, shaved fennel, orange, parsley, dill and mint, Parmesan and pepitas; lemon-Dijon vinaigrette on the side. Same-day sale |
| [Cilantro Lime Quinoa Salad](products/cilantro_lime_quinoa_salad.yaml) | draft | $11.50 | Quinoa, black beans, roasted corn, tomatoes, red pepper, cotija and pepitas; cilantro-lime vinaigrette on the side. Holds 2 days; made without wheat |
| [Red Lentil & Aleppo Pepper Soup](products/red_lentil_soup.yaml) | draft | $7.00 | Vegan one-pot red lentil soup with carrot, cumin, Aleppo pepper and lemon, finished with Aleppo oil; 300 g in a 12 oz cup |
| [Chicken Salad Scoop](products/add_chicken_salad.yaml) | draft | $4.50 | Add-on for either salad: 100 g of lemon-herb chicken salad in its own lidded, labeled cup |
| [Hummus Scoop](products/add_hummus.yaml) | draft | $3.50 | Add-on for either salad: 100 g of house hummus with an olive oil drizzle, in its own lidded, labeled cup |
| [Oat Milk (swap)](products/oat_milk_swap.yaml) | draft | $1.00 | Barista oat milk in place of whole milk in any milk drink, costed net of the milk it replaces |
| [Almond Milk (swap)](products/almond_milk_swap.yaml) | draft | $1.00 | Barista almond milk, the same way; adds tree nuts |
| [Drip Coffee (12 oz)](products/drip_coffee.yaml) | pending_test | $3.50 | Specialty filter coffee from the batch brewer |
| [Iced Coffee (16 oz cold brew)](products/iced_coffee.yaml) | pending_test | $4.00 | House cold brew, 1:1 with water over ice |
| [Espresso (double)](products/espresso.yaml) | pending_test | $3.50 | 18 g in, 36 g out |
| [Latte (12 oz)](products/latte.yaml) | pending_test | $4.75 | Double espresso and steamed whole milk |
| [Iced Latte (16 oz)](products/iced_latte.yaml) | pending_test | $5.00 | Double espresso over cold milk and ice |
| [Matcha Latte (12 oz)](products/matcha_latte.yaml) | pending_test | $5.25 | 3 g premium latte-grade matcha, unsweetened |
| [Chai Latte (12 oz)](products/chai_latte.yaml) | pending_test | $4.75 | Premium chai concentrate 1:1 with milk |
| [Strawberry Chamomile Lemonade](products/lemonade_kids.yaml) | draft | $3.50 | Caffeine-free kids' lemonade made on chamomile tea, 16 oz with ice |
| [Cinnamon Roll 4-Pack](products/cinnamon_roll_4pack.yaml) | draft | $18.00 | Pre-order: four rolls in a window gift box |
| [Whole Sour Cream Coffee Cake](products/coffee_cake_whole.yaml) | draft | $45.00 | Pre-order: the whole 12-cup bundt, serves 16 |
| [Breakfast Pastry Box (12)](products/pastry_box_dozen.yaml) | draft | $50.00 | Catering: 4 cinnamon rolls, 4 scones, 4 muffins |
| [Cookie & Brownie Box (12)](products/cookie_brownie_box.yaml) | draft | $50.00 | Catering: 6 cookies and 6 brownies |
| [Coffee Traveler (96 oz)](products/coffee_traveler.yaml) | draft | $40.00 | Catering: house drip with cups, lids, milk and a sugar kit |

The drinks stay `pending_test` until the roaster, matcha and chai suppliers are chosen and the espresso is dialed in. Items marked `draft` are written and costed but not yet made in the kitchen. Costs are in [`costing.md`](costing.md), the reasoning behind the prices in [`pricing.md`](pricing.md), and the production plan and labor in [`production.md`](production.md). The pro forma, with space needs, startup cost and three years of P&L for three candidate sites, is in [`proforma.md`](proforma.md).

## Layout

| Path | Holds |
|---|---|
| `ingredients.csv` | Ingredient master: id, name, category, allergens, spec, unit weight, density |
| `ingredient_prices.csv` | Dated price quotes per ingredient and channel; the newest `as_of` per channel wins |
| `formulas/*.yaml` | Sub-recipes (dough, cake batter, filling, glaze, roll, cooked grains, dressings, sauces, pickles, chicken salad, hummus, soup): quantities, method, specs, history |
| `products/*.yaml` | What we sell: build per unit, production steps, QA checks, declared allergens, price, what's tested and what's pending |
| `costing.md` | Generated cost report. Do not edit by hand |
| `pricing.md` | Retail price recommendations and their market basis |
| `production.md` | Production plan, prep-labor summary and where items share work |
| `settings.yaml` | Shared settings: the hourly labor rate |
| `proforma.yaml` | Pro forma inputs: candidate sites, staffing, space program, equipment, operating costs, startup costs, financing and sales scenarios |
| `proforma.md` | Generated pro forma report. Do not edit by hand |
| `viewer.html` | Generated Formula Book viewer: products, formulas, ingredients, labor and the pro forma. Open it in any browser. Do not edit by hand |
| `../tools/costing.py` | Validates everything and regenerates `costing.md` |
| `../tools/proforma.py` | Runs the pro forma and regenerates `proforma.md` |
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
python3 tools/proforma.py
```

This reruns the pro forma and rewrites `proforma.md`. Its sales and food cost come from the products, so rerun it after any price, cost or `par_daily` change as well as after editing `proforma.yaml`.

```bash
python3 tools/build_viewer.py
```

This rebuilds `viewer.html`, a single self-contained page with the data built in. It works offline, with a switch between retail and distributor costs, search, and tabs for products, formulas, ingredients, labor and the pro forma. Rebuild it after every data change too.

The script stops on unknown items, bad units, a yield larger than its inputs, formula cycles, missing pack weights or densities, and declared allergens that don't match the ingredients. It warns, without failing, when an approved product uses a formula that isn't approved yet, or when an ingredient has no price in a channel.

## Conventions

- **Ids:** lowercase `snake_case`. Ingredients, formulas and products share one namespace, so a line can point at any of them. Never rename an id that's in use; retire it and add a new one.
- **Quantities:** formula and product lines use grams (`g`) or counts (`each`).
- **Price packs:** `pack_unit` can be `g`, `kg`, `oz`, `lb`, `ml`, `l`, `fl_oz`, `qt`, `gal` or `each`. Volume packs need `density_g_per_ml`; count packs need `each_g`.
- **Product categories:** every product has a `category` of `pastry`, `sandwich`, `salad`, `soup`, `add-on`, `drink` or `catering`, which sets its place in the cost report.
- **Packaging:** cups, lids and other packaging are ingredients with `category` `packaging`, priced per `each`. The report shows them separately, and a product's `waste_pct` applies to its food lines only, not its packaging. Food products are costed with their to-go packaging; for-here orders on a plate skip it.
- **`price_ref`:** costs an item as one unit of another. An egg yolk costs one whole egg, and its white goes to egg wash.
- **Allergens:** semicolon-separated, using US major-allergen names (milk, egg, wheat, soy, peanuts, tree nuts, fish, shellfish, sesame). Every product must list `allergens_declared`, and it must match its ingredients.
- **Status:** `draft` → `pending_test` → `approved` → `retired`. Approve a formula only after a test bake, and say what was tested in `history`.
- **Changes:** for any change to an approved formula or product, bump `version` and add a `history` entry.
- **Formula yields:** `yield.grams` is what comes out after cooking or trimming. Add `yield.units` when the formula makes countable pieces.
- **Prep labor:** every formula has `labor.batch_min`, the hands-on minutes for one production run, and `labor.production_batches`, how many batches that run makes. Every product has `labor.unit_min`, the hands-on minutes for its own steps (shaping, finishing, assembly, building a drink), and `par_daily`, its planned daily sales. Don't count oven, proof, brew or steep time, taking orders or bagging. The report adds each product's share of its sub-recipes and its waste allowance, and prices the minutes at the rate in `settings.yaml`.
- **Bundles:** a product line can point at another product (unit `each`), as the catering boxes do. The bundle takes the inner product's food cost and labor but not its packaging or waste allowance.
- **Credit lines:** `credit: true` on a product line subtracts that ingredient's cost and ignores its allergens. The milk swaps use it to cost oat or almond milk net of the whole milk they replace.

## Pro forma

`tools/proforma.py` adds up each product's price times its `par_daily` to get the menu's steady-state day, with its food-and-packaging cost at distributor prices. Each site in `proforma.yaml` has a `format` (`cafe` or `counter`, which sets its crew, space program and equipment) and a `sales_index`, the share of that day it should reach once it's established. Each scenario scales sales again. From those the script builds three years of P&L (Year 1 ramps up month by month), the startup cost and its financing, break-even and payback.

- **Add a site:** copy a site block in `proforma.yaml`, set its size, seats, rent, NNN, build-out cost per sq ft and `sales_index`, and say in `rent_basis` and `source` where the numbers came from.
- **Change the crew:** edit the roles under `labor.formats`. The crew is sized for the format's `design_index` share of the par day, and `fixed_share` of its hours don't flex with sales.
- **Treat the outputs as estimates:** the sales indexes are judgment calls, and no site's rent or condition has been confirmed with a broker.

## Updating prices

Add a row to `ingredient_prices.csv` with a newer `as_of` date and keep the old rows as history. There are two channels today: `retail_est` (US grocery estimates) and `distributor_est` (foodservice estimates). Replace the estimates with real invoices and quotes as they arrive. To track a real supplier as its own channel, add it to `CHANNELS` in `tools/costing.py`.

## Adding a formula or product

1. Copy an existing YAML file in `formulas/` or `products/` and give it a new `id`.
2. Point each line's `item` at an ingredient or formula id. Add any new ingredient to `ingredients.csv`, with a price in each channel.
3. Run `python3 tools/costing.py` and fix anything it reports.
