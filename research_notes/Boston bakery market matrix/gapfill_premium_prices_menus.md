# Gap-fill: Boston premium bakery-cafés — price basket, menu architecture, award/list check and scale data (current to 5 Nov 2026)

> **Method and limits (read first).**
> - This file builds on `premium_artisan_bakery_cafes.md` (the "prior notes") and adds only what those notes lacked. A prior-note figure is repeated only when it is needed to complete a matrix row, and it is marked "(prior)".
> - **Everything new here comes from search-result extracts.** These are the search engine's summaries of the cited pages; I did not read the pages themselves. WebFetch failed at DNS for every host tried this pass: order.flourbakery.com, order.tattebakery.com, bakeybabka.com, lakonparis.com, michette-bakery.com and www.elephantinebakery.com. Hosts had already failed in earlier passes too: flourbakery.com, tattebakery.com, order.toasttab.com, www.toasttab.com, www.bostonmagazine.com, boston.eater.com, www.bostonglobe.com, www.boston.com, www.yelp.com and others. Reading full menus would need these hosts allowed in the session's network settings.
> - All 28 allotted searches were used.
> - The ordering pages (Tatte, Flour, Bakey, Toast, order.online) carry no "last updated" date, so their prices are recorded as "seen 5 Nov 2026". Prices differ by store, so the store is always named.
> - **Grades:**
>   - **[HD]** hard data: a first-party price on the operator's own site or ordering page.
>   - **[HD-DDS]** the operator's own web storefront, run on DoorDash Storefront (order.online). It is probably counter-equivalent, but that is unverified.
>   - **[OC]** owner claim.
>   - **[PR]** press.
>   - **[3P]** third-party aggregator, database, listing or review.
>   - **[3P-del]** delivery app. Observed markups run 18–40% over counter prices.
>   - **[EST]** my own arithmetic or inference.
>   - A year in parentheses, such as (2023), marks data from before 2025.
> - New log IDs start with "G-" so they don't collide with the prior notes' IDs (F1, T1, and so on).

---

## 1. Tatte (Boston units, 2025–2026): croissants, signature pastries, cookie, cake slice, shakshuka, sandwich, drip coffee, latte

### Takeaway
Every Tatte basket cell now has a first-party price. The main ones:

| Item | Price | Store |
|---|---|---|
| Drip coffee | $3.35 | Wellesley |
| Latte | $4.85 | Summer St |
| Traditional shakshuka | $14.00 (other shakshukas $14.50–$15.00) | Wellesley |
| Chicken pita | $13.00 | Copley |
| Cake slices | $5.50–$6.75 | several |
| Individual tarts and the petit nut box | $7.50 | several |

Two caveats. The drip and shakshuka prices come from suburban Wellesley, not a Boston-core store. And Tatte prices by location: Copley is $0.50 above Wellesley on the same items. Its delivery-app prices run about 35–40% above first-party, which is higher than the 10–30% assumed in the prior notes.

### Cited Findings

#### 1a. Completed Tatte basket, Massachusetts stores (all [HD] unless tagged)

| ID | Basket item | Price | Store / size | Date | Grade | Source |
|---|---|---|---|---|---|---|
| (prior T1) | Plain croissant | $4.50 | South Boston; each | seen 5 Nov 2026 | HD | [South Boston ordering](https://order.tattebakery.com/order/tatte-bakery-south-boston/item-turmeric-honey-latte-12-oz_85eaf103-4575-43e5-b590-e434d1fdc98f) |
| (prior T2) | Chocolate croissant (the menu has no item called "pain au chocolat") | $5.25 | South Boston | seen 5 Nov 2026 | HD | same as above |
| (prior T3) | Almond croissant | $5.25 | South Boston | seen 5 Nov 2026 | HD | same as above |
| G-T1 | Pistachio croissant (pistachio filling, crumbled pistachio; 580 cal) | $5.00 | **Store not identified.** The results included a DC (Dupont) page, and the item was out of stock at DC Capitol Crossing. **May be a DC price.** | seen 5 Nov 2026 | HD, store uncertain | [Tatte ordering (Dupont page extract)](https://order.tattebakery.com/order/tatte-bakery-dupont/item-plain-croissant_d8f89880-ab5f-40db-8fe8-c108cd1245bf) |
| G-T2 | Sour cherry cheese danish (croissant dough, sweet cheese, sour cherry) | $4.75 | Charlestown | seen 5 Nov 2026 | HD | [Charlestown ordering](https://order.tattebakery.com/order/tatte-charlestown/item-linzer-cookie_7c3712b6-737f-4170-beda-d6e44b809dc0) |
| G-T3 | Petit mixed nut box (honey caramel; cashew, hazelnut, walnut, pecan, pistachio) | $7.50 | Pier 4 (Seaport) | seen 5 Nov 2026 | HD | [Pier 4 ordering](https://order.tattebakery.com/order/tatte-bakery-pier-4-pier-4/item-feta-pistachio-pita_80fd2287-ff70-4989-a509-617ac34c45cf) |
| G-T4 | Mixed nut tart slice (about 1,040–1,060 cal) | $6.75 (out of stock) | "Main Street" store and Newton Centre | seen 5 Nov 2026 | HD | [Main Street ordering](https://order.tattebakery.com/order/tatte-bakery-main-street/item-lemon-poppyseed-loaf-cake-slice_9ff99c6d-2c19-416f-8e3a-fce288b7e124) |
| (prior T4) | Cookie: halva chocolate-chunk (in the "Tatte Favorites" group) | $4.00 | South Boston | seen 5 Nov 2026 | HD | [South Boston ordering](https://order.tattebakery.com/order/tatte-bakery-south-boston/item-anniversary-tote_ae25d495-e9e5-4579-851a-7f42431d29a0) |
| (prior T5) | Cookie: chocolate sandwich cookie with tahini buttercream | $3.00 | South Boston | seen 5 Nov 2026 | HD | same as above |
| G-T5 | Cake slice: lemon poppyseed loaf cake (830 cal) | $5.50 | "Main Street" store | seen 5 Nov 2026 | HD | [Main Street ordering](https://order.tattebakery.com/order/tatte-bakery-main-street/item-lemon-poppyseed-loaf-cake-slice_9ff99c6d-2c19-416f-8e3a-fce288b7e124) |
| G-T6 | Cake slice: pear tart tatin (caramelized Bosc pears) | $6.50 at Main Street (out of stock); $6.75 at High Street | two stores | seen 5 Nov 2026 | HD | [High Street ordering](https://order.tattebakery.com/order/tatte-bakery-high-street/item-raspberry-tea-cake-gf_5dcf59cb-380a-44aa-b3c4-4ea904871990) |
| G-T7 | Cake slice: orange upside-down cake (candied orange, almond streusel) | $6.75 | Newton Centre | seen 5 Nov 2026 | HD | [Newton Centre ordering](https://order.tattebakery.com/order/tatte-bakery-newton-centre/item-lemon-mint-tart_e5e3b5a9-4f4d-4de0-9168-5e7cf72c67c4) |
| G-T8 | Individual tarts: lemon mint tart (480 cal); pear tart with almond cream (890 cal, out of stock) | $7.50 each | Newton Centre | seen 5 Nov 2026 | HD | same as above |
| G-T9 | Individual tarts: gluten-free krembo tarts, vanilla-lime and passionfruit | $7.50 each | South Boston | seen 5 Nov 2026 | HD | [South Boston ordering](https://order.tattebakery.com/order/tatte-bakery-south-boston/item-turmeric-honey-latte-12-oz_85eaf103-4575-43e5-b590-e434d1fdc98f) |
| G-T10 | **Traditional shakshuka** (eggs poached in tomato sauce with chili, peppers, onion and cumin; feta, parsley; house challah; 1,010 cal) | **$14.00** | Wellesley | seen 5 Nov 2026 | HD | [Wellesley ordering](https://order.tattebakery.com/order/tatte-bakery-wellesley/item-breakfast-sandwich_95d80bff-faa1-44c4-bdee-4e5632445f65) |
| G-T11 | Other shakshukas: corn & spinach (with sourdough; 1,240 cal); potato, mushroom & bacon; lamb meatball & labneh. Gluten-friendly versions come with GF bread. | $14.50 / $15.00 / $15.00 | Wellesley | seen 5 Nov 2026 | HD | same as above |
| (prior T8) | Traditional shakshuka on a delivery app | $19.55 | Copley, Uber Eats | 2026 listing | 3P-del | [Uber Eats Copley](https://www.ubereats.com/store/tatte-bakery-&-cafe-copley-square/ugHYivg8UtCyP3ENvrCVKg) |
| G-T12 | Breakfast sandwich: halloumi sunny-side (fried egg, spinach; on the all-day menu) | $9.85 | Copley or Wellesley page; the extract does not say which | seen 5 Nov 2026 | HD | [Copley ordering](https://order.tattebakery.com/order/tatte-bakery-copley-square/item-kids-sandwich_dc2255cb-bc0f-473d-a5af-b58f560c1523); [Wellesley ordering](https://order.tattebakery.com/order/tatte-bakery-wellesley/item-kids-sandwich_dc2255cb-bc0f-473d-a5af-b58f560c1523) |
| G-T13 | **Lunch sandwich: chicken pita** (roasted chicken breast; chopped tomato, cucumber and red-onion salad) | **$13.00 at Copley**; $12.50 at Wellesley | two stores | seen 5 Nov 2026 | HD | same as above |
| G-T14 | Lunch salad: chicken, baby kale & chickpea (mint halloumi, dill-labneh dressing) | $15.00 at Copley; $14.50 at Wellesley | two stores | seen 5 Nov 2026 | HD | same as above |
| G-T15 | **Drip coffee** (T1 Drip Blend, hot batch brew) | **$3.35** | Wellesley; size not stated | seen 5 Nov 2026 | HD | [Wellesley ordering](https://order.tattebakery.com/order/tatte-bakery-wellesley/item-iced-decaf-black-sesame-latte-16-oz_57c8bc32-859d-49de-a471-61a0a1be97a6) |
| G-T16 | Red eye (drip plus a double espresso) | $3.85 | Wellesley | seen 5 Nov 2026 | HD | same as above |
| G-T17 | Café au lait (T1 drip with steamed milk) | Shown as "+$3.85" for 12 oz and "+$4.25" for 16 oz. This is an add-on-style display; no base price was shown. | Charlestown | seen 5 Nov 2026 | HD | [Charlestown ordering](https://order.tattebakery.com/order/tatte-charlestown/item-cafe-au-lait_be15cca6-8b47-4168-98bd-238426a65092) |
| G-T18 | **Latte** (double shot, steamed milk, microfoam) | **$4.85.** The listing gives "190 or 230" calories, which implies two sizes; the size for $4.85 is not stated. | Summer Street | seen 5 Nov 2026 | HD | [Summer Street ordering](https://order.tattebakery.com/order/tatte-bakery-summer-street-summer-street/item-12-oz-tumbler-i-love-you-a-latte_d00b0526-a336-431d-88a0-32afc160c3d9) |
| (prior T9) | Latte on a delivery app | $6.60 | Copley, Uber Eats | 2026 listing | 3P-del | [Uber Eats Copley](https://www.ubereats.com/store/tatte-bakery-&-cafe-copley-square/ugHYivg8UtCyP3ENvrCVKg) |
| G-T19 | Merchandise: limited-edition 12 oz Miir tumbler | $22.00 (out of stock) | Summer Street | seen 5 Nov 2026 | HD | [Summer Street ordering](https://order.tattebakery.com/order/tatte-bakery-summer-street-summer-street/item-12-oz-tumbler-i-love-you-a-latte_d00b0526-a336-431d-88a0-32afc160c3d9) |

#### 1b. Items seen on Massachusetts ordering pages with no price in the extract
- **Items:**
  - Linzer cookie (Charlestown) — [Charlestown](https://order.tattebakery.com/order/tatte-charlestown/item-linzer-cookie_7c3712b6-737f-4170-beda-d6e44b809dc0)
  - Feta pistachio pita (Pier 4) — [Pier 4](https://order.tattebakery.com/order/tatte-bakery-pier-4-pier-4/item-feta-pistachio-pita_80fd2287-ff70-4989-a509-617ac34c45cf)
  - Gluten-free meze breakfast (One Boston Place, Washington St) — [One Boston Place](https://order.tattebakery.com/order/tatte-bakery-one-boston-place-washington-st/item-gf-meze-breakfast_add7018c-3134-440a-b357-eafdd16faa54)
  - Gluten-free raspberry tea cake (High Street) — [High Street](https://order.tattebakery.com/order/tatte-bakery-high-street/item-raspberry-tea-cake-gf_5dcf59cb-380a-44aa-b3c4-4ea904871990)
  - Iced decaf black-sesame latte, 16 oz (Wellesley) — [Wellesley](https://order.tattebakery.com/order/tatte-bakery-wellesley/item-iced-decaf-black-sesame-latte-16-oz_57c8bc32-859d-49de-a471-61a0a1be97a6)
  - "I Love You a Latte" tea latte with vanilla (Summer Street) — [Summer Street](https://order.tattebakery.com/order/tatte-bakery-summer-street-summer-street/item-12-oz-tumbler-i-love-you-a-latte_d00b0526-a336-431d-88a0-32afc160c3d9)
  - Kids' sandwich: toasted challah with cheddar — [Wellesley](https://order.tattebakery.com/order/tatte-bakery-wellesley/item-kids-sandwich_dc2255cb-bc0f-473d-a5af-b58f560c1523)
  - A shakshuka sweatshirt (merchandise) — [Wellesley](https://order.tattebakery.com/order/tatte-bakery-wellesley/item-breakfast-sandwich_95d80bff-faa1-44c4-bdee-4e5632445f65)
- **Store names in this pass's ordering URLs (Massachusetts):** Copley Square, Charlestown, Summer Street, South Boston, Pier 4, High Street, Main Street, One Boston Place (Washington St), Newton Centre, Wellesley. The towns for "Main Street" and "High Street" were not identified — see the URLs above.

### Inferences
- **[EST] Sample checks, before tax.** These mix stores:

  | Order | Total |
  |---|---|
  | Plain croissant + latte | $9.35 |
  | Halloumi breakfast sandwich + latte | $14.70 |
  | Chicken pita + drip | $16.35 |
  | Traditional shakshuka + latte | $18.85 |

- **[EST] Tatte prices by location.**
  - Copley is $0.50 above Wellesley on both chicken items: +4.0% on the pita and +3.4% on the salad.
  - The pear tart tatin slice differs by $0.25 between two stores.
  - The prior notes found Boston $0.25–$0.50 above DC.
  - So a traditional shakshuka at a Boston-core store is probably about $14.50 rather than $14.00. This is unverified.
- **[EST] Tatte's delivery markup is above the prior notes' assumption.**
  - Latte: Uber Eats $6.60 vs. $4.85 first-party, a +36% markup.
  - Shakshuka: Uber Eats $19.55 vs. $14.00 at Wellesley, +40%. Against an assumed $14.50 Copley counter price it is about +35%.
  - The stores and cup sizes may differ, but both comparisons exceed the 10–30% range.
- **[EST] Tatte vs. Flour:**
  - Drip $3.35 vs. $3.50.
  - Latte $4.85 vs. $4.50.
  - Plain croissant $4.50 at both.
  - Cake slice $5.50–$6.75 vs. Flour's $6.30.
  - Tatte's lunch pita ($13.00) is $3 below Flour's BLT ($16.00).
  - Tatte's signature-style sweets (nut box, krembo tarts, lemon mint tart) sit at $7.50, the same price as specialty viennoiserie at the independents (section 3).
- **[EST] Likely signature lines.** The nut tart comes in two formats (a $6.75 slice and a $7.50 petit box). Shakshuka comes in four flavors, plus gluten-free versions, plus a sweatshirt. These are the clearest signs of signature lines. No owner statement confirms them as best-sellers.

### Gaps
- No first-party shakshuka or drip price from a Boston-core store; both came from Wellesley. No in-store croissant breakfast sandwich price.
- Cup sizes for the latte and drip; the café au lait base price.
- Which store the $5.00 pistachio croissant is from; it may be a DC price.
- Which towns the "Main Street" and "High Street" stores are in.
- Prices for Tatte's whole cakes and special orders; any owner-named best-sellers.

---

## 2. Flour: pain au chocolat, muffin, scone, brownie, cookie, cake slice, whole cake, egg sandwich, bread

### Takeaway
Flour's empty cells are now filled from its own ordering and catering pages:

| Item | Price |
|---|---|
| Brioche au chocolat (no laminated pain au chocolat surfaced) | $4.75 |
| Muffins | $4.50–$5.00 |
| Brownie | $5.00 |
| Cake slice | $6.30 |
| Breakfast egg sandwich | $10.00 |
| Homestyle multigrain loaf / focaccia loaf | $8.00 / $7.50 |
| Whole cakes, fall 2026 (6" / 8" / 10" / half-sheet) | $40–$42 / $57 / $74 / $147 |

The 8" cake rose from $55 (Valentine's 2025) to $57 (fall 2026), about +3.6%.

### Cited Findings

#### 2a. Completed Flour daily-case basket (all [HD], seen 5 Nov 2026 unless dated)

| ID | Item | Price | Store / notes | Source |
|---|---|---|---|---|
| (prior F1) | Plain croissant | $4.50 | Beacon Hill (other stores the same) | [Beacon Hill ordering](https://order.flourbakery.com/order/flour-bakery-cafe-beacon-hill-f9-209-cambridge-st/item-flour_bbf778c3-7c5c-4d5e-8be8-dcb7805e70a4) |
| G-F1 | **"Brioche au chocolat"** (buttery brioche filled with chocolate and pastry cream). This is Flour's nearest equivalent to a pain au chocolat; no item named "pain au chocolat" surfaced. | **$4.75** | Beacon Hill | [Beacon Hill ordering](https://order.flourbakery.com/order/flour-bakery-cafe-beacon-hill-f9-209-cambridge-st/item-sugar-brioche-bun_d4a8b25a-7f8c-4c7a-bf53-fabf2c1c93ed) |
| G-F2 | **Muffins** | **$4.50–$5.00.** Gingerbread muffin with coffee glaze $4.50; pumpkin muffin (in range, no exact price); gluten-free orange poppy seed $5.00 (prior F6). | several stores | [Seaport ordering](https://order.flourbakery.com/order/flourseaport/item-slice-of-lemon-raspberry-cake_baec2eae-8cc7-47ff-a042-44ffff18be40); [Beacon Hill](https://order.flourbakery.com/order/flour-bakery-cafe-beacon-hill-f9-209-cambridge-st/item-breakfast-pizza_c61c9e83-4e47-48ee-8ee4-1089482af3b3) |
| (prior F5) | Scones (lemon ginger; currant spelt oat; oatmeal maple pecan) | $4.50–$4.75 | Beacon Hill | [Beacon Hill ordering](https://order.flourbakery.com/order/flour-bakery-cafe-beacon-hill-f9-209-cambridge-st/item-breakfast-pizza_c61c9e83-4e47-48ee-8ee4-1089482af3b3) |
| G-F3 | **Brownie** (made with tcho chocolate; listed as "now gluten free!") | **$5.00** | Central Sq. A flourless brownie bite is also listed; its price was not captured. | [Central Sq ordering](https://order.flourbakery.com/order/flourcentralsq/item-hot-chocolate_c07f26c8-0a54-49f2-9d95-db32794a5c5c); [Central Sq](https://order.flourbakery.com/order/flourcentralsq/item-iced-mocha_dacb7544-f24e-4c92-a5ca-96273d74b03c) |
| (prior F8) | Cookie: "tcho" chocolate chip | $3.50 | Beacon Hill | [Beacon Hill ordering](https://order.flourbakery.com/order/flour-bakery-cafe-beacon-hill-f9-209-cambridge-st/item-batch-iced-coffee_9b001651-460f-40d1-a93c-315ce3946a6d) |
| G-F4 | **Cake slice:** vanilla celebration, coconut ("fluffy coconut cake filled with coconut buttercream"), midnight chocolate, lemon raspberry | **$6.30** | Beacon Hill, Seaport and others | [Seaport ordering](https://order.flourbakery.com/order/flourseaport/item-slice-of-lemon-raspberry-cake_baec2eae-8cc7-47ff-a042-44ffff18be40) |
| G-F5 | **Breakfast egg sandwich** (focaccia roll, ham or bacon, cheddar, arugula, tomato, dijonnaise) | **$10.00** | Cambridgeport; South End $10.00 (out of stock at capture) | [Cambridgeport ordering](https://order.flourbakery.com/order/flourcambridgeport/item-overnight-oats_37ca2823-273e-40d5-8a3b-c3679bb36d9c); [South End ordering](https://order.flourbakery.com/order/floursouthend/item-banana-bread_c1c5ec03-3b89-46d1-ace8-104cccf9a40a) |
| G-F6 | Kids' breakfast egg sandwich; kids' ham & cheese (sliced ham and cheddar on soft white focaccia) | $7.00; $6.50 | same pages | same as above |
| G-F7 | **Bread:** homestyle multigrain loaf; focaccia loaf (about 12 slices; sometimes out of stock); cranberry pepita loaf (a mildly sweet sourdough with honey, pepitas and cranberries; price not captured) | **$8.00; $7.50**; n/a | Beacon Hill pages | [Beacon Hill ordering](https://order.flourbakery.com/order/flour-bakery-cafe-beacon-hill-f9-209-cambridge-st/item-breakfast-pizza_c61c9e83-4e47-48ee-8ee4-1089482af3b3); [Beacon Hill](https://order.flourbakery.com/order/flour-bakery-cafe-beacon-hill-f9-209-cambridge-st/item-flour_bbf778c3-7c5c-4d5e-8be8-dcb7805e70a4) |
| — | Items listed with no price captured: vanilla filled donut (Central Sq); overnight oats (Cambridgeport) | n/a | — | [Central Sq donut](https://order.flourbakery.com/order/flourcentralsq/item-vanilla-filled-donut_d358bb72-4079-4c87-b33a-3e281439db5f); [Cambridgeport oats](https://order.flourbakery.com/order/flourcambridgeport/item-overnight-oats_37ca2823-273e-40d5-8a3b-c3679bb36d9c) |

#### 2b. Whole cakes and pre-order cake prices

| ID | Program / date | Cake | 6" | 8" | 10" | Half-sheet | Grade | Source |
|---|---|---|---|---|---|---|---|---|
| G-F8 | **Fall 2026 catering menu** (valid 9 Sep–1 Dec 2026) | Midnight chocolate | $42 | $57 | $74 | $147 | HD | [Flour catering](https://www.flourbakery.com/catering) |
| G-F8 | Same | Carrot; Boston cream pie | $40 | $57 | not captured | not captured | HD | same |
| G-F8 | Same | Lemon raspberry; vanilla celebration. The extract says these "follow the same size pricing"; exact cells were not captured. | — | — | — | — | HD | same |
| G-F9 | **Thanksgiving 2026 pre-order** | Celebration cake | — | $57 | $74 | — | HD | [Flour Thanksgiving](https://www.flourbakery.com/thanksgiving) |
| G-F9 | Same | Triple chocolate mousse cake | — | $60 | — | — | HD | same |
| G-F9 | Same | Vegan chocolate bundt, one size only: **$45** (no 6"/8"/10" ladder) | — | — | — | — | HD | same |
| G-F10 | Older menu page (undated) | Coconut cake, sold by the slice or as an 8" whole cake | — | $57 | — | — | HD (undated) | [Flour menu](https://www.flourbakery.com/menu) |
| G-F11 | **Valentine's 2025** | Midnight chocolate; lemon raspberry | (6" pages exist; prices not captured) | **$55; $55** | (a 10" vanilla celebration page exists) | — | HD | [Midnight 8" Val 2025](https://www.flourbakery.com/products/midnight-chocolate-cake-8-valentines-2025); [Lemon raspberry 8" Val 2025](https://shop.flourbakery.com/products/lemon-raspberry-cake-8-valentines-2025); [Midnight 6" Val 2025](https://www.flourbakery.com/products/midnight-chocolate-cake-6-valentines-2025?v=46437008998570); [Carrot 6" Val 2025](https://shop.flourbakery.com/products/carrot-cake-6-valentines-2025); [Vanilla celebration 10" Val 2025](https://shop.flourbakery.com/products/birthday-cake-10-valentines-2025) |
| — | Wedding cakes | A separate page exists; prices not captured | — | — | — | — | HD | [Flour wedding cakes](https://www.flourbakery.com/wedding-cakes) |

Catering contact per the extract: catering@flourbakery.com — [Flour catering](https://www.flourbakery.com/catering).

### Inferences
- **[EST] Cake price increase.** The 8" cake went from $55 (Feb 2025) to $57 (fall 2026), +3.6%. This is in line with the prior notes' +5% on the apple pie and +4.8% on the sticky-bun 4-pack.
- **[EST] Cake size ladder.**
  - Midnight chocolate: 6"→8" +36%; 8"→10" +30%; 10"→half-sheet +99%.
  - Per square inch of a round cake: $1.49 at 6", $1.13 at 8", $0.94 at 10". Bigger cakes are progressively cheaper per unit of cake.
  - An 8" cake at $57 costs about 9 slices' worth at the $6.30 slice price.
- **[EST] The egg sandwich after the egg-cost increase.** It is now $10.00. The prior notes say Flour added $0.50 because of egg costs in early 2025, which implies about $9.50 before. The pre-increase price was not observed.
- **[EST] Sample Flour checks, before tax:**

  | Order | Total |
  |---|---|
  | Croissant + latte | $9.00 |
  | Egg sandwich + latte | $14.50 |
  | Muffin + drip | $8.00–$8.50 |
  | BLT + drip | $19.50 |
  | Cake slice + latte | $10.80 |

- **[EST] No laminated chocolate item.** Flour's chocolate pastry is brioche-based, at $4.75. That is $0.50 below Tatte's and Bakey's chocolate croissants ($5.25) and $0.75–$1.00 below La Saison and Elephantine (section 3).
- **[EST] Bread is a minor line.** Only three loaves surfaced ($7.50–$8.00) and no baguette. Flour's case is built on brioche, quick breads, cakes and savory breakfast rather than bread.

### Gaps
- Exact prices for the pumpkin muffin and other non-gluten-free muffins (only the gingerbread price is exact); the cranberry pepita loaf; the flourless brownie bite; the lemon-meringue pie slice.
- Fall 2026 prices for each size of the lemon raspberry and vanilla celebration cakes, and the 10" and half-sheet prices for carrot and Boston cream.
- Wedding-cake pricing; cup sizes for coffee drinks; whether Flour sells any baguette.
- Whether prices are the same at all 11 stores. Every price seen matched across stores, but coverage was partial.

---

## 3. Independents: Clear Flour, Iggy's (incl. Imagine), Colette, Elephantine, Michette, Lakon Paris, Bakey, Sofra, La Saison, Hi-Rise, Petsi — croissant, signature, cookie, loaf, latte and sandwich prices

### Takeaway
New first-party prices now cover:
- **La Saison:** a $6.00 latte, a $3.75–$4.00 cookie, an $11.00 breakfast sandwich, and a **confirmed Charlestown store at 221 Main St**.
- **Bakey:** a $5.55 latte, and a $5.25 chocolate croissant at Faneuil Hall.
- **Sofra:** $14.00 pitas.
- **Elephantine:** a full croissant ladder via its DoorDash-run storefront: pain au chocolat $5.50, almond $6.25, ham & cheese $7.50, pistachio $8.00–$8.50.
- **Imagine:** a $5 croissant (press).

The latte price ladder runs Flour $4.50 < Tatte $4.85 < Bakey $5.55 < La Saison $6.00, with specialty lattes at $7.25.

Still without any current price: Clear Flour, Colette (newest price is from 2022), Michette (first-party), Lakon (first-party), Hi-Rise beverages and pastry, and a Petsi slice. Only older press or third-party data exists for these.

### Cited Findings

#### 3a. New price log by operator

**La Saison** [HD, Toast; seen 5 Nov 2026]
- **Charlestown store confirmed.** Toast lists "LA SAISON Bakery" at 221 Main Street, Charlestown, as well as 407 Concord Ave, Cambridge. The prior notes had this store from one blog only — [Toast Charlestown](https://order.toasttab.com/online/la-saison-bakery-c); [Toast Charlestown (local)](https://www.toasttab.com/local/order/la-saison-bakery-c/r-e9b2b982-fc2c-41d9-be35-d319d484548a).
- **Lattes:**
  - Plain latte $6.00 (Charlestown) — [Toast Charlestown](https://order.toasttab.com/online/la-saison-bakery-c).
  - Halva latte (tahini) $7.25 and saffron latte $7.25 (Cambridge) — [Toast Halva Latte](https://order.toasttab.com/online/lasaison-bakery/item-halva-latte-tahini_528ce3e5-c08a-41b1-be64-dbfbc06dde4d).
  - A pistachio latte is listed at Charlestown; its price was not captured — [Toast Pistachio Latte](https://order.toasttab.com/online/la-saison-bakery-c/item-pistachio-latte_c2ba9239-20ed-4b04-a205-6e60a89eee38).
- **Cookies.** Brown-butter chocolate-chip cookie: $4.00 at Charlestown, $3.75 at Cambridge. Also listed: a vegan classic chocolate chip and a gluten-free fudge cookie — [Toast Charlestown](https://order.toasttab.com/online/la-saison-bakery-c); [Toast Cambridge](https://www.toasttab.com/local/order/lasaison-bakery/r-6a8ade1b-7fae-487e-91ee-0eb897851e80).
- **Breakfast.** "Egg Bun" (egg patty, avocado, tomato, bacon, Dijon) $11.00 at Cambridge. Ham & cheese brioche $9.50 (out of stock) — [Toast Cambridge](https://www.toasttab.com/local/order/lasaison-bakery/r-6a8ade1b-7fae-487e-91ee-0eb897851e80).
- **Bundle.** "For Two": 2 sandwiches and 2 cookies for $31.50 (out of stock on one Charlestown page) — [Toast Charlestown](https://order.toasttab.com/online/la-saison-bakery-c).
- **Listed with no price captured:** #33 grilled cheese (Cambridge), "Loghm" sandwich (Charlestown; likely the Persian *loghmeh* [EST]), muesli bar and multigrain sourdough — [#33 grilled cheese](https://www.toasttab.com/local/order/lasaison-bakery/item-33-grilled-cheese_ef510e69-6f91-4d77-a0f7-5fa8221cb4a0); [Loghm](https://order.toasttab.com/online/la-saison-bakery-c/item-loghm-sandwich_112d7c95-24e8-4b8d-aa55-eec20b6417aa); [muesli bar](https://order.toasttab.com/online/la-saison-bakery-c/item-muesli-bar_c24fc666-0432-4047-80c7-4dc12c732b7c); [multigrain sourdough](https://toast.app/r/lasaison-bakery/order/r-6a8ade1b-7fae-487e-91ee-0eb897851e80/item-multi-grain-sourdough_dc2b8a32-e426-42aa-9e06-68e0138a7461).

**Bakey** [HD, Toast-run ordering at bakeybabka.com/order; seen 5 Nov 2026]
- **Latte** (double shot, steamed milk) $5.55, Kendall Square (238 Main St) — [Bakey Kendall ordering](https://bakeybabka.com/order/bakey-kendall-square-238-main-st/item-bakey-brownies-bites-platter_c3e7fd05-8880-4295-99e8-a1dd430429e1); [Bakey Brookline iced latte](https://bakeybabka.com/order/bakey-brookline-370-harvard-street/item-iced-latte_82b5cea1-66c9-4999-be8c-bfa0520de932).
- **Chocolate croissant** $5.25 at Faneuil Hall / Quincy Market. This matches the Tremont St Toast price in the prior notes (B2) — [Bakey Faneuil Hall](https://bakeybabka.com/order/bakey-fanuel-hall-299-faneyil-hall-market-place/item-chocolate-croissant_68a213f9-68c6-4436-8969-100bb894fb6c). The store's URL reads "299 Faneuil Hall Market Place"; the prior notes give 4 S Market St.
- **Florida, for comparison only (Hallandale Beach):** croissant sandwich (fresh cheese and vegetables) $17.99; chocolate-chip cookie $2.50 — [Bakey Hallandale](https://bakeybabka.com/order/bakey-holindale-668-west-hallandale-beach-boulevard/item-jam_ab14fc9d-c068-412e-b7ba-d26fd2045b7b).
- **Massachusetts items listed with no price captured:**
  - Cheese burekas and potato burekas (Tremont) — [cheese burekas](https://bakeybabka.com/order/bakeybabka/item-cheese-burekas_5c85f1fc-b18f-4700-a689-365ed0cda958); [potato burekas](https://toast.app/r/bakeybabka/order/r-bf1d525d-854a-4e07-8ecc-5c8502c687d3/item-potato-burekas_1f70adc2-3258-4c3c-9505-327d1b4e43ea)
  - London Fog, 16 oz (Tremont) — [London Fog](https://bakeybabka.com/order/bakeybabka/item-london-fog-16oz_5a238a1d-7d24-4659-9ef1-821c29f52fbe)
  - Brownie-bites platter (Kendall; catering) — [platter](https://bakeybabka.com/order/bakey-kendall-square-238-main-st/item-bakey-brownies-bites-platter_c3e7fd05-8880-4295-99e8-a1dd430429e1)
  - Retail tahini (Brookline) — [tahini](https://toast.app/r/bakey-brookline-370-harvard-street/order/r-51497424-6862-4cba-820e-b2a1ff504943/item-tahini_9b71e375-1e16-485f-b81f-910024e309a3)

**Sofra** [HD, Toast; seen 5 Nov 2026]
- **Pitas.** Sausage pita $14.00 and chicken shawarma pita $14.00 (Cambridge) — [Toast Sausage Pita](https://order.toasttab.com/online/sofra-cambridge/item-sausage-pita_5e82c3b9-5dfc-474b-92b5-d78654c4de41).
- **The Allston store has a live Toast menu** (partly fills the prior gap on its 2026 status). Listed: Greek pita (out of stock), sour cherry bar, simit, and a whole Black Sea cornbread; prices not captured — [Greek pita](https://www.toasttab.com/local/order/sofra-allston/item-greek-pita_1af96de3-d92f-4039-b9eb-83327d2f9296); [sour cherry bar](https://order.toasttab.com/online/sofra-allston/item-sour-cherry-bar_b5bd62a4-6e2a-4cc6-9f3f-b759129dc6e5); [simit](https://toast.app/r/sofra-allston/order/item-simit_6e3a8f1c-e341-461a-bba8-bfb7c226fd74); [whole cornbread](https://order.toasttab.com/online/sofra-allston/item-black-sea-cornbread-whole_2ec96cbf-7945-4143-99ee-adda179b2962).
- **Latte not found.** A $5.93 latte in the results belongs to an unrelated "Sofra Breakfast and Lunch" in Allen, Texas and is excluded — [Texas Sofra](https://www.toasttab.com/local/order/sofra-breakfast-and-lunch-503-w-mcdermott-dr-130/item-chefs-special-french-toast_425b86be-db3d-4475-8a7a-940b26a2e2d9).

**Elephantine** [HD-DDS, the operator's order.online storefront for 332 Congress St; page copyright 2026]
- **Croissant prices:** pain au chocolat $5.50; almond croissant $6.25; ham & cheese croissant $7.50; pistachio croissant $8.00; chocolate-pistachio croissant $8.50. No plain butter croissant price was found — [order.online Elephantine](https://order.online/store/elephantine-38663766).
- **Conflict.** A second order.online page lists the chocolate-pistachio croissant at $4.00. It is probably a stale or different menu; treat the $8.50 as current — [order.online (alt)](https://order.online/store/-38663766/).
- **Origin and opening:**
  - Listings place Elephantine Bakery in **Portsmouth, NH** — [TableAgent Portsmouth](https://tableagent.com/portsmouth/elephantine-bakery/); [Foodle](https://foodle.pro/thefoodreview/meals/portsmouth/elephantine-bakery/49972).
  - A NECN / Boston Restaurant Talk headline reads "bakery honored as NH's best opening new location in Boston's Fort Point neighborhood." That this is Elephantine is my inference [EST] — [NECN](https://necn.com/news/local/bakery-honored-as-nhs-best-opening-new-location-in-bostons-fort-point-neighborhood/3328417).
  - NBC Boston's headline: "Elephantine Bakery opens in Boston's Fort Point neighborhood" — [NBC Boston](https://www.nbcboston.com/news/local/elephantine-bakery-opens-in-bostons-fort-point-neighborhood/3807119/).
  - The Harvard Crimson (14 Oct 2025) called it "Seaport's newest addition" — [Crimson 10/14/25](https://api.thecrimson.com/article/2025/10/14/elephantine-bakery-review).
  - Taken together, the Boston store opened in 2025 [PR]. The owners' names were still not found.

**Imagine (Iggy's croissant café)** [PR]
- **Croissant $5,** per a Cambridge Day article. The article's date is not shown in the extract; it is probably 2024 opening coverage [EST]. It gives the address as 358 Huron Ave, Huron Village — [Cambridge Day](https://www.cambridgeday.com/?p=144142).
- **Background.** Iggy's had planned "a coffee-and-croissants cafe" since Oct 2022 — [Cambridge Day 10/7/22](https://www.cambridgeday.com/2022/10/07/iggys-bread-plans-a-coffee-and-croissants-cafe).
- **Conflicting listing.** A Boston Calendar event listing gives 348 Huron Ave and the name "Kismet." It is probably an error — [Boston Calendar](https://www.thebostoncalendar.com/events/new-cambridge-croissant-cafe-now-open).
- **Iggy's baguette at retail** (from the sibling notes `chains_franchises_wholesale_channels.md`, [3P reseller]): $4.25 at Formaggio Kitchen South End and $4.50 at Formaggio Kendall — [Formaggio South End](https://southendgifts.formaggiokitchen.com/Iggys-Bakery-French-Baguette-p406009750); [Formaggio Kendall](https://kendallcurbside.formaggiokitchen.com/Iggys-Country-Baguette-p695756030).

**Michette** [PR (2023)]
- **2023 prices.** Boston Globe review (3 Aug 2023): "Patisserie $3-$5; breads and savory items $4.15-$10.50." Online ordering ran through Lunchbox (eat.lunchbox.io). The review warns that "if you just appear at Michette, you run the risk of not finding what you want" — [Globe 8/3/23](https://www.bostonglobe.com/2023/08/03/lifestyle/exceptional-baguettes-michette-tiny-artisanal-east-somerville-bakery); [PressReader 8/6/23](https://www.pressreader.com/usa/boston-sunday-globe/20230806/282754886218955).
- **Baguettes are a hero item.** The Globe's headline: "Exceptional baguettes and more at Michette" (2023) — same source.
- **2026 first-party prices not found.** Only the DoorDash prices in the prior notes exist ($5.75–$7.47) — [DoorDash](https://www.doordash.com/store/michette-somerville-30678667/).

**Colette** [PR (2022)]
- **2022 prices.** The Tech review (28 Apr 2022): from "$3 for a croissant to $6.40 for their priciest tart." Reviewers single out the classic croissant, the croissant bicolore (chocolate-hazelnut cream) and the croissant aux amandes — [The Tech 4/28/22](https://thetech.com/2022/04/28/colette-bakery).
- **Founding date settled toward 2020.** A Globe headline of 26 May 2020 reads "Colette French bakery comes to life in Medford"; a Feb 2021 Globe feature followed. A Globe headline of 13 Sep 2022 says Colette opened its second bakery, in Melrose — [Globe 5/26/20](https://www.bostonglobe.com/2020/05/26/lifestyle/colette-french-bakery-comes-life-medford); [Globe 2/18/21](https://www.bostonglobe.com/2021/02/18/lifestyle/they-opened-french-bakery-medford-with-taste-home); [Globe 9/13/22](https://www.bostonglobe.com/2022/09/13/lifestyle/colette-opens-second-bakery-melrose).
- **2025–26 prices not found.**

**Clear Flour** [3P]
- **No current item prices found.**
- **Price signals.** Time Out puts it in price tier 1 of 4; Superpages lists "$$" — [Time Out](https://www.timeout.com/boston/restaurants/clear-flour-bread); [Superpages](https://cars.superpages.com/brookline-ma/bpp/clear-flour-bakery-1128852).
- **Product.** Bakes baguettes, boules, bâtards and loaves daily, with no dough conditioners or preservatives — [MapQuest](https://www.mapquest.com/us/massachusetts/clear-flour-bread-247019).
- **Unattributed, so not used as a finding:** one search summary said late-2025 Yelp reviews mention long lines and a "pretzel croissant." The source page could not be isolated; see Gaps.

**Lakon Paris** [3P]
- **No first-party price list found.**
- A third-party listing rates the price range "$$$$." Reviewers call prices steep but say the croissants are worth it — [Frankiapp](https://frankiapp.com/business/lakon-paris-patisserie-130645.md); [Wanderlog](https://wanderlog.com/place/details/6129053/lakon-paris-patisserie).
- **Menu.** The extract describes "award-winning butter croissants" plus rotating monthly specialties: cube croissants, danishes and savory scones. It came from one of these two third-party pages; the extract did not say which — [Boston Uncovered](https://bostonuncovered.com/lakon-paris-patisserie/); [Wanderlog](https://wanderlog.com/place/details/6129053/lakon-paris-patisserie).
- **Other channels.**
  - Catering through ezCater, with a $150 food-and-beverage delivery minimum — [ezCater](https://www.ezcater.com/catering/lakon-paris-patisserie-boston).
  - A "Lakon Paris Pastry Club" subscription listed on Table22; terms not captured — [Table22](https://app.table22.com/product/lakon-paris-pastry-club).
- **A partnership store.** A Boston Magazine headline reads "Boston Pastry Powerhouses Join Forces for a New Lakon Paris Patisserie Location"; the content was not captured — [Boston Mag](https://www.bostonmagazine.com/?p=2723364).

**Petsi Pies** [3P / PR]
- **8" Classic Apple, $22.99.** Pre-order through Mahoney's, with pickup at its Winchester farmstand on 25–27 Nov. The year is not stated; those dates fit Thanksgiving 2025 (27 Nov 2025) [EST] — [Mahoney's](https://shop.mahoneysgarden.com/?p=160240).
- **Sizes.** Pies come large, medium or small. The small is 5" and "serves one to two." A small summer peach pie was $10 (Aug 2024) — [Cambridge Day 8/21/24](https://www.cambridgeday.com/2024/08/21/petsi-pies-summer-peach-pie/).
- **Weak signals.** An undated listing says pies "start at $9" [3P, low reliability] — [Atly](https://www.atly.com/location/PetsiPies). A customer review says wedding pies were charged at the regular large-pie price, with no wedding upcharge — [WeddingWire](https://weddingwire.com/reviews/petsi-pies-cambridge/59ebdcbe5908b4c7.html).
- **No 2025–26 slice price found.**

**Hi-Rise.** Not searched this pass because the budget went to higher-priority gaps. The prior notes' sandwich and loaf prices stand.

#### 3b. Consolidated premium price matrix (prior notes + this pass; "n/f" = not found)
Values are first-party [HD] unless tagged. G- IDs are new this pass; "(prior)" values are from the prior notes. Each operator's subsection above, and the prior notes' log, give the URL for each number.

| Operator | Plain croissant | Pain au choc / choc croissant | Almond croissant | Signature item | Cookie | Cake slice / tart | Loaf / baguette | Breakfast sandwich | Lunch sandwich / plate | Drip | Latte |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Tatte** (MA) | $4.50 (prior) | $5.25 (prior) | $5.25 (prior) | Nut box $7.50; cheese danish $4.75; shakshuka $14.00 (Wellesley) | $3.00–$4.00 (prior) | $5.50–$6.75 slice; $7.50 tart | n/f | $9.85 (halloumi) | $13.00 chicken pita (Copley) | $3.35 (Wellesley) | $4.85 |
| **Flour** | $4.50 (prior) | $4.75 (brioche au chocolat) | $5.50 (prior) | Sticky bun $5.25 (prior) | $3.50 (prior); brownie $5.00 | $6.30 slice; 8" cake $57 | $7.50 focaccia / $8.00 multigrain | $10.00 | $16.00 BLT (prior) | $3.50 (prior) | $4.50 (prior) |
| **La Saison** | $5.50 (prior) | $5.50–$5.75 (prior) | n/f | Kouign-amann $6.00 (prior) | $3.75 Cambridge / $4.00 Charlestown | n/f | $11.00 sourdough (prior; pairing uncertain) | $11.00 Egg Bun; $9.50 ham & cheese brioche | n/f | n/f | $6.00 (Charlestown); $7.25 specialty |
| **Bakey** | n/f | $5.25 (Tremont, Faneuil Hall) | n/f | Babka slice $6.90 (prior) | n/f (FL $2.50) | — | Babka loaf $21.42 [3P-del] (prior) | n/f | n/f | n/f | $5.55 (Kendall) |
| **Elephantine** [HD-DDS] | n/f | $5.50 | $6.25 | Pistachio $8.00; choc-pistachio $8.50; ham & cheese $7.50 | n/f | n/f | n/f | n/f | n/f | n/f | n/f |
| **Sofra** | — | — | — | Morning bun $6.00 (prior) | $2.75–$3.50 shortbreads (prior) | n/f | $5.00–$5.50 cornbread (prior) | $5.50 spanakopita (prior) | $14.00 pitas | n/f | n/f |
| **Michette** | n/f (2023: pastry $3–$5 [PR]) | $7.47 choc-pistachio [3P-del] (prior) | $7.47 [3P-del] (prior) | Cardamom bun $5.75 [3P-del] (prior) | n/f | n/f | (2023: breads/savory $4.15–$10.50 [PR]) | n/f | n/f | n/f | n/f |
| **Lakon** | n/f | $5.50 (older review [3P], prior) | n/f | Cube croissant ≈$8.99–$9+ [3P] (prior) | n/f | n/f | — | n/f | n/f | n/f | n/f |
| **Imagine / Iggy's** | $5 [PR] | n/f | n/f | — | n/f | — | Iggy's baguette $4.25–$4.50 [3P reseller] | n/f | n/f | n/f | n/f |
| **Clear Flour** | $2.50 [3P, stale] (prior) | n/f | n/f | Flavored croissants $4.50 [3P] (prior) | n/f | — | Baguette $2.50–$3.00 [3P, stale] (prior) | — | — | n/f | n/f |
| **Colette** | (2022: $3 [PR]) | n/f | n/f | Tarts up to $6.40 (2022) [PR] | n/f | (2022: tart ≤$6.40) | n/f | n/f | n/f | n/f | n/f |
| **Hi-Rise** | n/f | n/f | n/f | — | n/f | — | Luce loaf $7.00 / $9.50 [3P] (prior) | Hummus toast $7.50 (prior) | $9.50–$19.00; Georgia Reuben $12 / $19.50 (prior) | n/f | n/f |
| **Petsi** | — | — | — | 10" pie $35–$38 (2024) (prior); 8" apple $22.99 [3P reseller]; 5" pie $10 (2024) [PR] | — | Slice $5 (2020) (prior) | — | — | — | — | — |

### Inferences
- **[EST] Latte price ladder.** Flour $4.50, Tatte $4.85 (+8% over Flour), Bakey $5.55 (+23%), La Saison $6.00 (+33%), with La Saison's specialty lattes at $7.25. Independents charge $0.70–$1.50 more per latte than the two chains.
- **[EST] Chocolate-pastry ladder.** Flour brioche au chocolat $4.75 < Tatte and Bakey $5.25 < Elephantine $5.50 ≈ La Saison $5.50–$5.75.
- **[EST] Almond croissants** run $5.25 (Tatte) and $5.50 (Flour) to $6.25 (Elephantine), and $7.47 on Michette's DoorDash listing.
- **[EST] The specialty-format premium is large.** Elephantine's pistachio croissants ($8.00–$8.50) cost 60–70% more than the $5.00 Tatte pistachio croissant, whose store is uncertain. Its ham & cheese ($7.50) costs 20% more than Flour's ($6.25). This matches the prior notes' $7–$9 tier for viral formats (Lakon cube, Michette specialties).
- **[EST] Narrow bands for cookies and sandwiches:**

  | Item | Band | Data points |
  |---|---|---|
  | Cookie | $3.00–$4.00 | Flour, Tatte, La Saison. This is below the ~$4.50–$5 Levain anchor in the sibling chains notes. |
  | Breakfast sandwich | $9.50–$11.00 | Tatte $9.85, Flour $10.00, La Saison $9.50–$11.00 |
  | Lunch pita or sandwich | $13–$16 | Tatte $13, Sofra $14, Flour $16. Hi-Rise is wider at $9.50–$25. |

- **[EST] Uniform vs. tiered pricing.**
  - **Uniform:** Bakey charges $5.25 for a chocolate croissant at both Tremont St and the tourist-heavy Faneuil Hall store.
  - **Tiered:** Tatte, as section 1 shows, and La Saison, whose cookie costs $0.25 more at Charlestown than at Cambridge.
- **[EST] Inflation at Colette and Michette can't be measured yet.** Their latest prices are $3 croissants (Colette, 2022) and $3–$5 pastries (Michette, 2023), while 2026 independent croissants sit at $5–$6. If they rose as much as La Saison (+17% since 2022), Colette's croissant would be about $3.50 today. But no 2025–26 Colette or Michette first-party price exists to test that.
- **[EST] Off-premise channels at the independents.** Lakon's ezCater listing and Table22 pastry club, Bakey's platters and retail jars, and La Saison's "For Two" bundle all reach past the counter. These are smaller versions of Flour's pre-order catalog.

### Gaps
- **No current first-party prices** for Clear Flour, Colette, Michette (its Lunchbox page did not surface), Lakon (its own site was blocked) or Hi-Rise beverages and pastry.
- **Missing cells by operator:**
  - Elephantine: plain croissant, latte, sandwich, cookie.
  - Imagine: latte, sandwich, current-dated croissant price.
  - Bakey (Boston): cookie, sandwich, in-store babka loaf.
  - Sofra: latte.
  - La Saison: almond croissant, lunch-sandwich prices.
  - Petsi: 2025–26 slice price.
- **Unknown:** Elephantine's owners. What the "Pastry Powerhouses Join Forces" Lakon store is.
- **Unattributed:** the late-2025 Yelp mentions of long lines and a "pretzel croissant" at Clear Flour. The source page could not be isolated, so they are not used as a finding.

---

## 4. Approximate SKU counts by category for Tatte, Flour, Sofra, Bakey, Lakon and Michette

### Takeaway
A full SKU count is impossible without fetching the menus, and every menu host is blocked. The counts below are **lower bounds**: distinct items observed in search extracts across the prior notes and this pass.

| Operator | Items observed | Architecture |
|---|---|---|
| Flour | ≈42 (+≈13 pre-order) | Breakfast-pastry and quick-bread led, with a deep cake and pie pre-order catalog |
| Tatte | ≈38 | Café-restaurant; cakes, tarts and savory plates outnumber viennoiserie |
| Sofra | ≈21 | Most savory and plate-heavy of the independents |
| Bakey | ≈15 | Narrow and babka-centric |
| Michette | ≈11 | Viennoiserie-led |
| Lakon | ≈5–6 | Viennoiserie-led |

At Michette and Lakon, savory food and sandwiches appear mainly at the larger second sites (Michette Cambridge, Lakon Brighton).

### Cited Findings

#### 4a. Observed distinct items by category ([EST] counts from the sources in sections 1–3 and the prior notes; these are lower bounds, not menus)

| Operator | Viennoiserie & enriched | Bread (retail loaves) | Cookies / bars | Cakes / tarts / pies (incl. slices) | Savory pastry & breakfast | Sandwiches / plates / salads | Drinks | Other (retail, merch, pre-order) | Observed total |
|---|---|---|---|---|---|---|---|---|---|
| **Tatte** (MA pages) | 4 (+1 store uncertain) | 0 seen | 3 | 10 | 7 | 4 | 7 | 3 merch | **≈38–39** |
| **Flour** | 7, plus 8 muffins / scones / quick breads / donut | 3 | 3 | 5 slices; plus 8 whole-cake flavors and 4–5 holiday pies (pre-order) | 5 | 3 | 8 | Dog treat; sticky-bun packs and kit; catering platters | **≈42 daily-case, + ≈13 pre-order** |
| **Sofra** | 2 | 2 | 5 | 1 (special) | 3 | 5 | ≥1 | 2 packaged, plus cookie boxes | **≈21** |
| **Bakey** | 3 croissant formats + 3 babka flavors (sold by slice, loaf or 24") | ≥1 | 1 (platter) | — | 2 | 0 seen in MA | 3 | 2 retail jars | **≈15** |
| **Lakon** | ≥4 | 0 seen | 0 seen | Plated desserts at Brighton (count n/f) | ≥1 | Sandwiches at Brighton (count n/f) | n/f | Catering; pastry-club subscription | **≈5–6** |
| **Michette** | 6, plus canelés | ≥1 (baguette) | ≥1 | 0 seen | Spanakopita croissant (counted under viennoiserie) | ≥1 (Cambridge lunch) | ≥1 | — | **≈10–11** |

#### 4b. Items behind the counts (with sources)

**Tatte** (sources in section 1 and prior notes rows T1–T5 and T8–T10):
- **Viennoiserie:** plain, chocolate and almond croissants; sour cherry cheese danish. The pistachio croissant's store is uncertain.
- **Cookies:** halva chocolate-chunk, chocolate sandwich cookie, linzer.
- **Cakes and tarts:**
  - Slices: lemon poppyseed loaf, pear tart tatin, mixed nut tart, orange upside-down cake.
  - Individual: lemon mint tart, pear tart with almond cream, gluten-free raspberry tea cake, two gluten-free krembo tarts, petit mixed nut box.
- **Savory breakfast:** four shakshukas, halloumi sunny-side sandwich, croissant breakfast sandwich (3P), gluten-free meze breakfast.
- **Lunch:** chicken pita, feta pistachio pita, kids' sandwich, chicken / kale / chickpea salad.
- **Drinks:** T1 drip, red eye, café au lait, latte, turmeric & honey latte, iced decaf black-sesame latte, "I Love You a Latte."
- **Merchandise:** anniversary tote, shakshuka sweatshirt, Miir tumbler.

**Flour** (sources in section 2 and prior notes section 2):
- **Viennoiserie and brioche:** plain, almond and ham & cheese croissants; kouign amann; sugar brioche bun; sticky bun; brioche au chocolat.
- **Quick breads:** 3 muffins, 3 scones, banana bread, vanilla filled donut.
- **Bread:** multigrain, focaccia, cranberry pepita.
- **Cookies and bars:** tcho chocolate chip, brownie, flourless brownie bite.
- **Slices:** lemon meringue pie; vanilla celebration, coconut, midnight chocolate and lemon raspberry cakes.
- **Savory breakfast:** egg sandwich, kids' egg sandwich, breakfast pizza, Rhode Island–style bakery pizza, overnight oats.
- **Lunch:** BLT, everything-spiced tuna salad, kids' ham & cheese.
- **Drinks:** house drip, batch iced coffee, latte, pumpkin spice latte, iced mocha, hot chocolate, lemon limeade, bottled water.
- **Pre-order:** 8 cake flavors; Thanksgiving pumpkin (plus a gluten-free version), pecan, sweet potato and apple pies, plus the "piefecta."

**Sofra** (sources in section 3 and prior notes section 2):
- **Sweet pastry:** morning bun, Sultan's Delight.
- **Bread:** Black Sea cornbread, simit.
- **Cookies and bars:** ma'amoul shortbread, pistachio shortbread, kourabiedes, sour cherry bar, sesame-cashew bites.
- **Special-order cake:** Turkish mosaic cake.
- **Savory pastry:** cheese borek, spanakopita, topik.
- **Plates:** sausage, chicken shawarma and Greek pitas; lamb saganaki; Turkish breakfast.
- **Drinks:** Mexican Coke (no others seen).
- **Packaged:** pita chips, morning-bun ice cream.

**Bakey** (sources in section 3 and prior notes section 2):
- **Babka:** chocolate, raspberry and ChocoBanana pecan, sold by the slice, as a loaf or at 24".
- **Croissants:** chocolate, goat-cheese, "Broissant."
- **Savory:** cheese and potato burekas.
- **Other:** brownie-bites platter; bread loaves.
- **Drinks:** latte, iced latte, London Fog.
- **Retail jars:** tahini, jam.

**Lakon** (sources in section 3 and prior notes section 2):
- **Viennoiserie:** butter croissant, chocolate croissant, cube croissants (milk cream plus rotating monthly flavors), danishes.
- **Savory:** savory scones.
- **Brighton only:** plated desserts and sandwiches.

**Michette** (prior notes section 2; Globe 2023 in section 3):
- **Croissants:** pistachio-chocolate, almond, spanakopita.
- **Other viennoiserie:** pain suisse, cardamom bun. A "twice-baked croissant" was mentioned in one extract and is not verified.
- **Other:** canelés, baguette and breads, cookies, sandwiches (Cambridge lunch), coffee.

### Inferences
- **[EST] Tatte is a café-restaurant first and a bakery second.** About 17 of its 38 observed items are cakes, tarts and savory plates, and only 4–5 are viennoiserie. Beverages and plates (shakshuka at $14–$15) probably drive a large share of the ticket. This fits the prior notes' estimate of about $1.5–1.7M in sales per café.
- **[EST] Flour's breadth is in breakfast pastry and pre-order.** About 15 of its 42 daily-case items are viennoiserie and quick breads. A pre-order cake and pie catalog of about 13 SKUs, with four sizes, works as a second business line.
- **[EST] Specialist independents run narrow cases** of about 5–15 visible items, built around one hero (babka, cube croissant, cardamom bun). Savory food and sandwiches arrive only with bigger second sites (Lakon Brighton, Michette Cambridge, Sofra Allston), consistent with the prior notes.
- **[EST, low confidence] Full menus are probably larger.** Search extracts surface only part of each menu, so true menus are likely meaningfully larger than these lower bounds, especially for drinks, where size and milk variants multiply SKUs. I found no basis for a precise multiplier.

### Gaps
- Full menus, and so true SKU counts, for all six operators. This needs the ordering hosts (order.tattebakery.com, order.flourbakery.com, bakeybabka.com, order.toasttab.com, lakonparis.com, michette-bakery.com) allowed for fetching.
- Daypart splits: which items are breakfast-only and which are all-day.
- How often rotating items change, for example Lakon's monthly specialties.

---

## 5. Boston Magazine Best of Boston 2024 and 2025 bakery winners, Eater Boston's bakery map, and missing premium operators

### Takeaway
- **Best of Boston 2024 Best Bakery: Yafa Bakery & Café,** which also won Best New Bakery in 2023 and, per the prior notes, Best Baklava in 2026.
- **Best of Boston 2025 Best Bakery: not confirmed.** The 2025 bakery-adjacent winners found are:
  - Imagine: Best New Bakery-Café.
  - Levain: Best Cookie (it won again in 2026).
  - Lionheart Confections: Best Donut.
  - Verveine Café & Bakery: Best Gluten-Free Spot.
- **Eater Boston's bakery map could not be retrieved.**
- **Missing from the premium roster:** Yafa (a three-time winner), plus Verveine and Lionheart.

### Cited Findings

#### 5a. Best of Boston (Boston Magazine), bakery-related winners

| Year | Category | Winner | Grade | Source |
|---|---|---|---|---|
| 2021 | Best Croissants | La Saison | PR | [BoB 2021 La Saison](https://www.bostonmagazine.com/best-of-boston-archive/2021/la-saison-bakery/) |
| 2022 | **Best Bakery** | La Saison | PR | [BoB 2022 La Saison](https://bostonmagazine.com/best-of-boston-archive/2022/la-saison/) |
| 2023 | Best Slice of Cake | La Saison | PR | Per a search extract of La Saison's honors list, "2021 (Best Croissants), 2022 (Best Bakery), and 2023 (Best Slice of Cake)," most likely from Boston Magazine's bakery guide — [Boston Mag bakery guide](https://www.bostonmagazine.com/?p=2808187); [BoB 2022 La Saison](https://bostonmagazine.com/best-of-boston-archive/2022/la-saison/) |
| 2023 | Best New Bakery | Yafa Bakery & Café | PR | Extract quote: "Best of Boston winner, 2023 (Best New Bakery) and 2024 (Best Bakery)" — [Boston Mag bakery roundup](https://www.bostonmagazine.com/restaurants/best-bakeries-boston/); [Boston Mag bakery guide](https://www.bostonmagazine.com/?p=2808187); [Best Bakery archive](https://www.bostonmagazine.com/best-of-boston-archive/award/bakery/) |
| 2023 | A Best of Boston award (category not shown in extract; likely "Best Loaded Croissant" [EST]) | Lakon Paris Patisserie | PR | [BoB 2023 Lakon](https://www.bostonmagazine.com/best-of-boston-archive/2023/lakon-paris-patisserie/); [Best Loaded Croissant category](https://www.bostonmagazine.com/best-of-boston-archive/award/loaded-croissant/) |
| **2024** | **Best Bakery** | **Yafa Bakery & Café** | PR | same as the Yafa 2023 row |
| 2024 | Other bakery categories | Not captured. The 2024 winners hub exists, but its contents did not surface. | — | [BoB 2024 winners](https://www.bostonmagazine.com/best-of-boston-archive/year/2024/) |
| **2025** | **Best Bakery** | **Not confirmed** (see the conflict note below) | — | [Best Bakery archive](https://www.bostonmagazine.com/best-of-boston-archive/award/bakery/) |
| 2025 | Best New Bakery-Café | Imagine (Iggy's), 358 Huron Ave, Cambridge | PR | [BoB 2025 Imagine](https://www.bostonmagazine.com/best-of-boston-archive/2025/imagine-2/) |
| 2025 | Best Cookie | Levain Bakery (a New York chain) | PR | [BoB 2025 restaurants](https://www.bostonmagazine.com/restaurants/2025/07/08/best-of-boston-2025-restaurants/) |
| 2025 | Best Donut | Lionheart Confections | PR | same as above |
| 2025 | Best Gluten-Free Spot | Verveine Café & Bakery | PR | same as above |
| Undated | "Best Croissant" (singular) category page | Its current listing is Clear Flour Bread; year not shown. Clear Flour also has Best of Boston entries for 2010 and 2012. | PR | [Best Croissant category](https://www.bostonmagazine.com/best-of-boston-archive/award/croissant/); [BoB 2010](https://bostonmagazine.com/best-of-boston-archive/2010/clear-flour-bread-4/); [BoB 2012](https://www.bostonmagazine.com/best-of-boston-archive/2012/clear-flour-bread-6/) |
| 2026 (prior) | Best Bakery | Michette. Also Levain (Best Cookie), Yafa (Best Baklava), Elephantine (Best Hot Chocolate). | PR | [BoB 2026](https://www.bostonmagazine.com/restaurants/2026/07/10/best-of-boston-2026-restaurants/) |

**Conflict note.** One search extract described the Best Bakery archive page as listing Michette "ahead of the 2024 winner, La Saison." Two other sources contradict this:
- La Saison's own Boston Magazine honors list gives its Best Bakery as 2022 — [BoB 2022 La Saison](https://bostonmagazine.com/best-of-boston-archive/2022/la-saison/).
- Yafa's listing says "2024 (Best Bakery)" — [Boston Mag bakery roundup](https://www.bostonmagazine.com/restaurants/best-bakeries-boston/).

I treat 2024 = Yafa as the better-supported answer. The 2025 Best Bakery winner stays unknown.

Media coverage of the 2025 list: Boston.com covered it on 24 Jun 2025 (date from the URL) — [Boston.com](https://www.boston.com/food/food-news/2025/06/24/boston-magazine-2025-best-of-boston/); Boston Magazine published a roundup, "All the Best of Boston 2025 Food Winners" — [Boston Mag](https://www.bostonmagazine.com/?p=2803164).

#### 5b. Eater Boston and other 2025–26 lists
- **Eater Boston's bakery map was not retrieved.** A search limited to boston.eater.com returned no results, and fetching was blocked in an earlier pass.
  - A radio-station article, undated, refers to Eater Boston's roundup of "the most essential bakeries in Boston," with items "from chocolate mousse to Persian flatbreads" — [Rock 92.9](https://rock929rocks.com/?p=332354).
  - A Wanderlog list updated 30 May 2026 says it draws on sources including Eater Boston — [Wanderlog](https://wanderlog.com/list/geoCategory/19669/).
  - Neither gives the map's entries.
- **Boston Globe Magazine, 9 Jul 2025:** a 15-bakery list highlighting Middle Eastern flavors and savory steamed buns. The names were not captured — [Globe 7/9/25](https://www.bostonglobe.com/2025/07/09/magazine/french-pastries-best-boston-bakeries).
- **Other current lists surfaced but not mined:**
  - Beli "Best Bakeries in Boston" — [Beli](https://lists.beliapp.com/boston-ma/bakeries/index.html)
  - Tasting Table "16 Best Bakeries in Boston" — [Tasting Table](https://www.tastingtable.com/1420489/absolute-best-bakeries-boston/)
  - Time Out — [Time Out](https://www.timeout.com/boston/restaurants/best-bakeries-in-boston)
  - The Food Lens — [Food Lens](https://thefoodlens.com/boston/guides/bakeries)
  - Boston Moms "14 Best Cookie Spots" — [Boston Moms](https://bostonmoms.com/?p=22406)

#### 5c. Roster check: premium or premium-adjacent operators missing from the prior matrix
- **Yafa Bakery & Café.** Best New Bakery 2023, Best Bakery 2024 and Best Baklava 2026 make it Boston Magazine's most-awarded bakery in 2023–26. It is not in the premium roster or any sibling note beyond the 2026 baklava mention. Its location, format and prices were not captured — [Boston Mag bakery roundup](https://www.bostonmagazine.com/restaurants/best-bakeries-boston/); [BoB 2026](https://www.bostonmagazine.com/restaurants/2026/07/10/best-of-boston-2026-restaurants/).
- **Verveine Café & Bakery.** A gluten-free bakery-café, Best Gluten-Free Spot 2025. Absent from all notes — [BoB 2025](https://www.bostonmagazine.com/restaurants/2025/07/08/best-of-boston-2025-restaurants/).
- **Lionheart Confections.** Best Donut 2025. Absent from all notes — same source.
- **Levain Bakery.** Best Cookie in both 2025 and 2026. It is covered in the sibling chains notes, not the premium roster — [BoB 2025](https://www.bostonmagazine.com/restaurants/2025/07/08/best-of-boston-2025-restaurants/).
- **Elephantine.** Already listed, but now known to be a Portsmouth, NH bakery whose Boston store opened in 2025 (section 3).
- **Still unresolved from the prior notes:**
  - "Fuful Bakery," which is on Yelp's top 10.
  - Vinal Bakery (Somerville), praised by The Infatuation, has no matrix row.
  - Japonaise is covered in the Asian/Latin sibling notes.

### Inferences
- **[EST] Best Bakery rotates among small specialists.** The winner went La Saison (2022) → Yafa (2024) → Michette (2026). The two big chains, Tatte and Flour, did not appear in any 2021–26 bakery category found. Small specialists with a hero item win the editorial awards, while the chains win on footprint.
- **[EST] Awards cluster around one hero item.** The categories won are croissants (La Saison, Clear Flour, Lakon's loaded croissant), cake (La Saison), baklava (Yafa), hot chocolate (Elephantine) and gluten-free (Verveine). The award system rewards a single standout item, which reinforces the hero-item strategy noted in the prior notes.
- **[EST] Yafa may be the most important omission.** Its run of three awards suggests a premium Middle Eastern bakery-café, potentially a direct comparable for Sofra. Format and pricing are unverified.

### Gaps
- The 2025 Best Bakery winner, and the 2024 winners in the croissant, bread, new-bakery and cookie categories.
- Eater Boston's current bakery-map entries.
- The names on the Globe's July 2025 15-bakery list.
- Yafa's location, owner, format and prices; Verveine's and Lionheart's details.

---

## 6. Revenue, average ticket or transactions/day for premium operators other than Tatte

### Takeaway
No credible revenue, average-ticket or transactions-per-day figure was found for any premium operator other than Tatte. The only numbers are:
- **Flour:** a ZoomInfo database estimate of $91.7M in revenue with 201–500 employees. This implies about $8.3M per store, roughly 5× Tatte's per-café figure, so it is implausible and should not be used.
- **Lakon:** owner and press figures from 2023 on production volume. It went from about 1,000 croissants per weekend day to about 2,000 at its two shops, "but even that isn't enough."

### Cited Findings
- **Flour revenue (third-party database, unreliable).** ZoomInfo lists revenue of "$91.7 Million" and 201–500 employees. Flour is private and publishes no financials [3P] — [ZoomInfo](https://www.zoominfo.com/c/flour-bakery/26053306).
- **Stale store counts in Flour profiles.** Goldbelly and a Massachusetts Conference for Women bio say "nine" stores, against 11 actual in 2026 per the prior notes. The Goldbelly listing confirms a national e-commerce shipping channel [3P] — [Goldbelly](https://goldbelly.com/flour-bakery-cafe); [MA Conference for Women](https://www.maconferenceforwomen.org/joanne-chang/).
- **Chang background [PR].** Chang opened the first Flour in the South End in 2000. With her husband Christopher Myers she co-owns the sister restaurant Myers+Chang (opened 2007). She won the 2016 James Beard Award for Outstanding Baker — [WGBH](https://wgbh.org/people/joanne-chang). The extract was ambiguous about whether Myers was also a Flour co-founder, so that is not asserted here.
- **Other Flour profiles that surfaced without figures:** Baking Business ("Flour Bakery focuses on growth opportunities"), Craft.co and a 2014 Bay State Banner profile — [Baking Business](https://www.bakingbusiness.com/articles/32298-flour-bakery-focuses-on-growth-opportunities?v=preview); [Craft.co](https://craft.co/flour-bakery-cafe); [Bay State Banner 2014](https://baystatebanner.com/2014/11/20/entrepreneur-joanne-chang-leaves-career-in-business-consulting-to-start-successful-flour-bakery/).
- **Lakon production (2023) [PR / OC].**
  - Per the Globe: "Where once they were making 1,000 croissants each weekend day, they are now making about 2,000 — at both locations — but even that isn't enough." The extract attributes this to someone named Grossi, whose role is not shown — [Globe 4/18/23](https://www.bostonglobe.com/2023/04/18/lifestyle/lakon-paris-patisserie-croissants-are-worth-lining-up); [PressReader 4/19/23](https://www.pressreader.com/usa/the-boston-globe/20230419/282398403715152).
  - Owner Urupong "Kope" Kharuharat said the high demand prompted him and his wife, Vichaya "Jenny" Kiangkaew, to open a second store [OC] — [Globe 4/26/23](https://www.bostonglobe.com/2023/04/26/lifestyle/lakon-paris-patisseries-viral-croissants).
- **Lakon catering signal.** The ezCater listing has a $150 delivery minimum [3P] — [ezCater](https://www.ezcater.com/catering/lakon-paris-patisserie-boston).
- **No figures found** for Bakey, Sofra, Michette, Colette, La Saison, Clear Flour, Iggy's, Elephantine, Hi-Rise or Petsi in this pass. The prior notes' Flour sticky-bun volume (about 220k a year, 2019) and Iggy's roughly 400 wholesale accounts (2024) remain the only other volume data.

### Inferences
- **[EST] Sanity check on ZoomInfo.** $91.7M ÷ 11 stores ≈ $8.3M per store. That is about 5× Tatte's $1.5–1.7M per café, derived from Restaurant Business sales and unit counts in the prior notes. Flour's stores are smaller counter-service cafés, so the database figure is very likely inflated, perhaps by counting catering, shipping or another entity. If Flour's stores did $1–2.5M each — an assumption, not data — the company would be about $11–27M a year.
- **[EST] Lakon volume, illustrative only.** Take 2,000 croissants on a weekend day across both shops. At 2026 price points of $5.50–$9.00, sold out, they would gross about $11k–$18k that day. At an assumed 2–3 pastries per purchase, that is roughly 700–1,000 transactions across two shops, or about 350–500 per shop on a peak day. The production figure is from 2023, and the price and basket-size assumptions are mine.
- **[EST] Sample checks stand in for average ticket.** No observed average ticket exists. The constructed checks in sections 1–3 range from about $9.00–$11.50 for a croissant and latte (Flour $9.00; Tatte $9.35; Bakey $10.80 with a chocolate croissant; La Saison $11.50) to about $14.50–$19.50 for breakfast or lunch with a drink. Treat these as upper and lower bounds for a single-person ticket, not as measured averages.

### Gaps
- Any disclosed revenue, average ticket, or transactions per day for Flour, Bakey, Lakon, Sofra, Michette, Colette or La Saison.
- Current (2025–26) Lakon production volume, and its store count when the figure was given. The 2023 quote predates the Brighton and Seaport stores.
- Boston Business Journal coverage, which could hold financial detail; bizjournals.com is blocked for fetching, and no BBJ extract surfaced.
- Toast, Square or other platform benchmark data for Boston bakery-café tickets.
