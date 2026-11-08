# Production plan and prep labor

This page covers how the menu gets made, where the hands-on hours go, and where items share work. Prep minutes are stored in the data: a `labor` block in every formula and product, and a `par_daily` in every product. `tools/costing.py` totals them in the Prep labor section of [`costing.md`](costing.md), and the viewer shows them in its Labor tab.

All figures below use the planning pars as of 2026-11-08. The minutes are estimates until the first production runs are timed.

## How labor is counted

- **Formulas:** `labor.batch_min` is the hands-on time for one production run. That run makes `labor.production_batches` batches at once; for example, the signature dough mixes three batches in one 20-qt mixer run. The run's minutes are split across every batch, so making things in bigger runs lowers the minutes per unit.
- **Products:** `labor.unit_min` covers the steps written in the product file itself: shaping, finishing, assembly, or building the drink.
- **How it adds up:** a product's minutes are its own steps, plus its share of every sub-recipe it uses, plus the waste allowance. A catering box carries the minutes of the products inside it.
- **Not counted:**
  - Proofing, baking, cooling, steeping and brewing. The oven and the brewer do that work.
  - Taking orders, bagging, cleaning the shop, and management.
- **Rate:** $21.00 an hour, set in [`settings.yaml`](settings.yaml). That's the research's $18.54 BLS baker wage plus about 13% for payroll taxes, workers' comp and paid leave.

## Where the hours go at par

At the current pars the menu sells about $3,630 a day and takes 23.4 hands-on hours, which costs $490, or 14% of sales. Food and packaging are 20% of sales at distributor prices, so food, packaging and prep labor together come to about 33%, before counter staff.

| Category | Hands-on hours a day | Sales a day | Prep labor, % of sales |
|---|---|---|---|
| Pastry | 7.0 | $924 | 16% |
| Sandwiches | 6.5 | $798 | 17% |
| Drinks | 5.7 | $1,288 | 9% |
| Salads | 1.7 | $215 | 16% |
| Pre-order and catering | 1.6 | $192 | 17% |
| Soup | 0.6 | $126 | 10% |
| Add-ons | 0.4 | $86 | 9% |

- **The cinnamon roll uses the most hours of any item:** 3.2 minutes a roll, or 3.2 hours a day at 60 rolls. Its labor ($1.13) costs more than its food and packaging ($0.63). About a third of that time is making the dough. Half is rolling, filling, cutting and glazing.
- **Made-to-order sandwiches take the most labor per unit:**
  - Harissa chicken sandwich: 6.2 minutes.
  - Fennel sausage breakfast sandwich: 5.2 minutes.
  - Breakfast sandwich: 4.7 minutes.
  - The 3–3.5 minutes of griddle and assembly work on the breakfast sandwiches is most of their time.
- **The fennel bowl is the slowest single item:** 6.7 minutes a bowl. At 8 bowls a day that's still under an hour.
- **Drinks are cheap in labor for what they earn:** 5.7 hours a day at the bar, but only 9% of drink sales.
- **The quickest items to make:**
  - Mini scone: 0.8 minutes.
  - Brownie: 1.1 minutes.
  - Cookie and muffin: 1.5 minutes each.
  - Soup: 2.0 minutes a serving, from one pot.

## The daily bake

There's one oven, so group the bakes by temperature and change the setting as few times as possible. Every temperature below is the formula's starting point until the test bakes confirm it.

| When | Oven | What goes in |
|---|---|---|
| 5:00 | 425°F, then 375°F | Muffins straight from the fridge. The batter was scooped the night before |
| 5:30 | 400°F | Blueberry scones and mini vanilla scones, portioned the day before |
| 6:00 | 350°F | Cinnamon rolls, breakfast rolls and lunch rolls, then brownies and coffee cakes. Everything at 350°F goes in one run |
| Mid-morning and early afternoon | 410°F | Cookie rounds from frozen dough, so there are always fresh cookies |
| Mid-afternoon | 425°F | Tomorrow's chicken, roasted after the pastry so it doesn't scent the morning bake |

## Shared work already built in

- **One dough for all the bread:** the signature milk dough makes the cinnamon rolls, the round breakfast rolls and both lunch rolls. At par that's about 15 kg a day, or 13.8 batches, mixed three batches at a time.
- **Free egg wash:** the dough uses egg yolks, and the leftover whites become the egg wash for every roll.
- **Shared mix-ins:**
  - Walnuts go in the coffee cake ribbon and the cookies.
  - Semisweet chips go in the cookies and the brownies.
  - One espresso shot from the bar goes in each brownie pan.
- **One roast, two products:** chicken roasts in 4 kg runs for both the chicken salad and the harissa chicken sandwich.
- **One lemon session:** zest first, then juice. That covers the scones, muffins, minis, dressings, hummus, tapenade, chicken salad and lemonade. The lemonade uses most of the lemons, about 24 a day at par.
- **Shared produce and sauces:**
  - Arugula goes in the fennel bowl and both lunch sandwiches.
  - Harissa goes on the breakfast sandwiches and into the harissa mayo.
  - Red onion and cilantro go in the quinoa salad, its dressing and the pickled onions.
- **One food-processor session:** make the hummus, then the tapenade. Wash the processor in between, because the hummus contains sesame.
- **Make-ahead that clears the morning:**
  - Cookie dough is frozen in balls and keeps a month.
  - Muffin batter is scooped the night before, and scones are portioned ahead.
  - The cinnamon-walnut mix is made six cakes at a time.
  - Glazes are made in 3–4× batches; dressings, pickles and sauces twice a week.
  - Worth testing: an overnight cold proof for shaped cinnamon rolls. If this dough handles it, rolling and shaping move to the quiet afternoon.
- **Catering rides the morning bake:** pastry boxes and roll 4-packs are packed from the day's bake. They add packing minutes, not new production.

## Biggest ways to cut hours

1. **A bigger mixer for the signature dough.** At par the dough takes about 4.6 mixes a day in a 20-qt mixer, close to 3 hours. A 40-qt mixer would do it in two runs and save about an hour and a quarter a day; a 60-qt about an hour and a half. This is the largest single saving on the menu.
2. **Roll the cinnamon rolls in bigger sheets.** Rolling two batches per sheet (24 rolls a log) spreads the roll-out work over twice the rolls. A dough sheeter goes further once volume justifies it.
3. **Speed up the egg station.** The two breakfast sandwiches take 4.1 hours a day, mostly at the griddle. Egg rings and frying six eggs at a time keep the fried egg that won the tasting while cutting the minutes.
4. **Use bottled fresh lemon juice for the lemonade.** It would remove about half the lemonade's prep, at some cost to flavor.
5. **Launch with one salad.** The fennel bowl takes 6.7 minutes a bowl and sells same-day only; the quinoa salad keeps two days.

## Next

Time the first production runs and replace the estimates in each `labor` block. After two weeks of sales, set `par_daily` from the point-of-sale mix.
