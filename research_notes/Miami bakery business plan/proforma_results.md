# Miami bakery business plan: model results

Generated from `tools/proforma.py` and `db/proforma.yaml` (as of 2026-11-19): formats `roll_popup` (Stage 1) and `roll_kitchen` (Stage 2) with the `markets.miami` costs. Year-2 figures unless stated; low and high are 80% and 120% of estimated sales; "left for the owner" has no owner pay in the costs and no loan. These are model outputs, not research findings; allocations marked as such are the planner's judgment.

## Product line: price, cost and hands-on minutes

Miami price, food-and-packaging cost at distributor estimates, hands-on minutes in 36-roll test batches and at production-kitchen scale (132-roll runs), and sales per hands-on hour at scale.

| Product | Miami price | Food and packaging | % of price | Minutes, test batch | Minutes, production scale | Sales per hands-on hour |
|---|---|---|---|---|---|---|
| Cinnamon Roll | $5.25 | $0.63 | 12% | 3.2 | 1.3 | $234 |
| Guava & Cheese Roll | $5.75 | $0.76 | 13% | 3.4 | 1.5 | $223 |
| Grande Cinnamon Roll | $8.50 | $1.09 | 13% | 5.2 | 2.2 | $235 |
| Roll of the Week (Grande) | $9.50 | $1.34 | 14% | 5.1 | 2.2 | $257 |
| Cinnamon Roll 4-Pack | $19.00 | $1.88 | 10% | 13.0 | 5.9 | $194 |
| Cinnamon Roll Box (6) | $27.00 | $2.51 | 9% | 19.3 | 8.6 | $188 |
| Cinnamon Roll Box (12) | $50.00 | $4.21 | 8% | 38.0 | 16.6 | $181 |
| Mini Roll Party Tray (24) | $38.00 | $3.38 | 9% | 22.4 | 9.5 | $239 |
| Celebration Roll Cake (9-inch) | $45.00 | $3.81 | 8% | 25.0 | 11.7 | $232 |
| Cinnamon Twist Loaf | $19.00 | $1.68 | 9% | 12.4 | 5.5 | $206 |
| Dulce de Leche Twist Loaf | $21.00 | $2.23 | 11% | 11.5 | 5.2 | $245 |
| Take-and-Bake Cinnamon Rolls (6) | $24.00 | $2.42 | 10% | 17.3 | 7.9 | $183 |
| Chocolate Chip Walnut Cookie | $4.75 | $1.20 | 25% | 1.5 | 0.8 | $354 |
| Brownie | $4.75 | $1.01 | 21% | 1.1 | 0.9 | $330 |
| Cookie & Brownie Box (12) | $52.00 | $13.40 | 26% | 16.0 | 11.1 | $280 |
| Iced Coffee (16 oz cold brew) | $4.75 | $0.94 | 20% | 0.9 | 0.9 | $324 |
| Iced Latte (16 oz) | $5.75 | $1.02 | 18% | 1.4 | 1.4 | $242 |
| Latte (12 oz) | $5.25 | $1.15 | 22% | 1.6 | 1.6 | $193 |
| Drip Coffee (12 oz) | $3.75 | $1.04 | 28% | 0.6 | 0.6 | $395 |
| Espresso (double) | $3.25 | $0.71 | 22% | 1.2 | 1.2 | $159 |
| Colada (to share) | $4.25 | $1.41 | 33% | 2.4 | 2.4 | $104 |
| Coffee Traveler (96 oz) | $42.00 | $13.58 | 32% | 4.2 | 4.2 | $605 |

One cinnamon roll takes 3.07 hands-on minutes in test batches and 1.28 at production scale (before the 5% waste allowance): the dough, filling and glaze are made eleven batches at a time and the bench has a sheeter.

## Pop-up design (roll_popup)

Pop-up: markets, pre-order drops, office orders and fundraisers from a rented commissary kitchen. 190 working days a year. Average working day at index 1.0: $1,360, about 85 orders at $16.09; $258,477 a year. Food and packaging 11.9% of sales before the 5.5-point buffer. Hands-on prep and bar hours 6.3 a working day at production scale against 17.7 paid hours (average $20.59). Channel commissions and shares 3.8% of sales, plus $8,800 a year of stall fees.

| Channel | Days a year | Sales on a channel day | Orders on it | Average order | Sales a year | Share |
|---|---|---|---|---|---|---|
| Farmers markets and pop-ups | 80 | $1,935 | 163 | $11.90 | $154,820 | 60% |
| Saturday pre-order pickup | 46 | $992 | 33 | $29.76 | $45,632 | 18% |
| Office, gift and party orders | 150 | $195 | 2 | $104.52 | $29,265 | 11% |
| School, league and church fundraisers | 8 | $3,595 | 155 | $23.19 | $28,760 | 11% |

Signature dough used: about 4,583 kg a year, 92 kg a working week (1,018 classic-roll equivalents a week; a 60-qt mix makes 132).

## Roll kitchen design (roll_kitchen)

Roll kitchen: a production kitchen with a walk-up window, selling boxes through five channels; no seats. 296 working days a year. Average working day at index 1.0: $2,274, about 140 orders at $16.23; $673,011 a year. Food and packaging 13.0% of sales before the 5.5-point buffer. Hands-on prep and bar hours 10.3 a working day at production scale against 30.6 paid hours (average $18.96). Channel commissions and shares 5.4% of sales, plus $6,820 a year of stall fees.

| Channel | Days a year | Sales on a channel day | Orders on it | Average order | Sales a year | Share |
|---|---|---|---|---|---|---|
| Walk-up window and pre-order pickup | 184 | $1,986 | 139 | $14.24 | $365,378 | 54% |
| Farmers markets and pop-ups | 62 | $1,935 | 163 | $11.90 | $119,986 | 18% |
| Office, gift and party orders | 190 | $392 | 4 | $87.70 | $74,428 | 11% |
| School, league and church fundraisers | 18 | $3,595 | 155 | $23.19 | $64,710 | 10% |
| Delivery apps | 184 | $264 | 11 | $23.20 | $48,509 | 7% |

Signature dough used: about 10,455 kg a year, 209 kg a working week (2,323 classic-roll equivalents a week; a 60-qt mix makes 132).

## Sites

| Site | Stage | Sq ft | Rent / NNN per sq ft | Rent and NNN, Year 2 | Sales, Year 2 | Left for the owner: low / base / high | Margin before owner's pay, base | Year 1 | Cash to open | Return on it | Break-even, share of base sales | Most base rent it can carry and pay $60K |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Stage 1: commissary kitchen and market stalls | 1 | 0 | $30,000 a year, assumed | $30,900 | $255,756 | $11K / $39,440 / $68K | 15% | $15,195 | $83,453 | 47% | 72% | n/a |
| Dadeland Plaza, 830 sq ft unit, Pinecrest | 2 | 830 | $55.00 (assumed) / $12.00 (assumed) | $57,278 | $668,463 | $56K / $129,152 / $202K | 19% | $64,541 | $312,719 | 41% | 65% | $136 |
| Café for sale on N Kendall Drive, Kendall | 2 | 1,200 | $40.00 (assumed) / $10.00 (assumed) | $61,800 | $647,909 | $36K / $107,272 / $178K | 17% | $45,233 | $389,314 | 28% | 70% | $78 |
| Restaurant for sale on US-1, Palmetto Bay | 2 | 2,000 | $21.72 / $0.00 | $44,743 | $647,909 | $41K / $111,969 / $183K | 17% | $49,793 | $458,774 | 24% | 68% | $47 |
| Cafeteria for sale by Coral Gables (ZIP 33145) | 2 | 1,100 | $35.53 / $0.00 | $40,255 | $627,354 | $50K / $118,721 / $187K | 19% | $58,281 | $471,934 | 25% | 65% | $87 |
| Ranchuelo's Coffee Shop, 12948 SW 87 Ave, by The Falls (modeled and dropped) | 2 | 1,287 | $27.00 (assumed) / $0.00 | $35,791 | $504,027 | −$4K / $50,450 / $105K | 10% | $3,598 | $341,505 | 15% | 82% | $20 |

Earlier designs at Dadeland Plaza, from their own results files: the Boston-style roll bakery (1,004 sq ft unit) left $8,641 on $405,613; the window-only roll house left $76,408 on $307,857 in the 830 sq ft unit (low $22K, high $131K).

## P&L and startup by site, base case

### Stage 1: commissary kitchen and market stalls

| Line | Year 1 | Year 2 | Year 3 | Year 2, % of sales |
|---|---|---|---|---|
| Sales | $204,605 | $255,756 | $263,429 | 100% |
| Food and packaging | $35,519 | $44,398 | $45,730 | 17% |
| Hourly crew, with payroll taxes | $68,439 | $78,324 | $80,674 | 31% |
| Base rent | $30,000 | $30,900 | $31,827 | 12% |
| Card fees, repairs, supplies, marketing, delivery, other | $17,596 | $21,995 | $22,655 | 9% |
| Delivery commissions, fundraiser shares and market fees | $16,556 | $18,759 | $19,322 | 7% |
| Insurance, software, accounting, licenses, waste, linens, phone | $21,300 | $21,939 | $22,597 | 9% |
| Left for the owner | $15,195 | $39,440 | $40,623 | 15% |

Startup: Equipment $19,000; Signage $1,500; Pre-opening payroll and training $5,096; Opening inventory $5,000; Launch marketing $6,000; Brand, packaging design, website and ordering system $10,000; Company set-up, permits and trademark $5,000; Security deposit $7,500; Rent and NNN before opening $2,500; Contingency $1,900; Working capital reserve $19,956. Total $83,453.
Break-even $183,965 of sales a year (72% of base); paying the owner $60,000 takes $293,181. Sales per paid crew hour $77.

### Dadeland Plaza, 830 sq ft unit, Pinecrest

| Line | Year 1 | Year 2 | Year 3 | Year 2, % of sales |
|---|---|---|---|---|
| Sales | $534,771 | $668,463 | $688,517 | 100% |
| Food and packaging | $98,856 | $123,571 | $127,278 | 18% |
| Hourly crew, with payroll taxes | $174,165 | $194,989 | $200,839 | 29% |
| Base rent | $45,650 | $47,020 | $48,430 | 7% |
| NNN charges | $9,960 | $10,259 | $10,567 | 2% |
| Utilities | $12,450 | $12,824 | $13,208 | 2% |
| Card fees, repairs, supplies, marketing, delivery, other | $51,338 | $64,172 | $66,098 | 10% |
| Delivery commissions, fundraiser shares and market fees | $35,610 | $43,012 | $44,302 | 6% |
| Insurance, software, accounting, licenses, waste, linens, phone | $42,200 | $43,466 | $44,770 | 7% |
| Left for the owner | $64,541 | $129,152 | $133,026 | 19% |

Startup: Build-out $62,250; Design, engineering, permits and legal $9,338; Equipment $104,500; Signage $8,000; Pre-opening payroll and training $8,113; Opening inventory $9,000; Launch marketing $15,000; Security deposit $13,902; Rent and NNN before opening $18,537; Contingency $16,675; Working capital reserve $47,404. Total $312,719.
Break-even $433,055 of sales a year (65% of base); paying the owner $60,000 takes $542,419. Sales per paid crew hour $74.

### Café for sale on N Kendall Drive, Kendall

| Line | Year 1 | Year 2 | Year 3 | Year 2, % of sales |
|---|---|---|---|---|
| Sales | $518,327 | $647,909 | $667,346 | 100% |
| Food and packaging | $95,743 | $119,679 | $123,269 | 18% |
| Hourly crew, with payroll taxes | $172,302 | $192,591 | $198,369 | 30% |
| Base rent | $48,000 | $49,440 | $50,923 | 8% |
| NNN charges | $12,000 | $12,360 | $12,731 | 2% |
| Utilities | $18,000 | $18,540 | $19,096 | 3% |
| Card fees, repairs, supplies, marketing, delivery, other | $49,759 | $62,199 | $64,065 | 10% |
| Delivery commissions, fundraiser shares and market fees | $35,089 | $42,361 | $43,632 | 7% |
| Insurance, software, accounting, licenses, waste, linens, phone | $42,200 | $43,466 | $44,770 | 7% |
| Left for the owner | $45,233 | $107,272 | $110,491 | 17% |

Startup: Build-out $66,000; Design, engineering, permits and legal $9,900; Equipment $84,500; Purchase of the existing fit-out and lease $95,000; Signage $8,000; Pre-opening payroll and training $8,113; Opening inventory $9,000; Launch marketing $15,000; Security deposit $15,000; Rent and NNN before opening $15,000; Contingency $15,050; Working capital reserve $48,750. Total $389,314.
Break-even $452,180 of sales a year (70% of base); paying the owner $60,000 takes $561,655. Sales per paid crew hour $73.

### Restaurant for sale on US-1, Palmetto Bay

| Line | Year 1 | Year 2 | Year 3 | Year 2, % of sales |
|---|---|---|---|---|
| Sales | $518,327 | $647,909 | $667,346 | 100% |
| Food and packaging | $95,743 | $119,679 | $123,269 | 18% |
| Hourly crew, with payroll taxes | $172,302 | $192,591 | $198,369 | 30% |
| Base rent | $43,440 | $44,743 | $46,085 | 7% |
| Utilities | $30,000 | $30,900 | $31,827 | 5% |
| Card fees, repairs, supplies, marketing, delivery, other | $49,759 | $62,199 | $64,065 | 10% |
| Delivery commissions, fundraiser shares and market fees | $35,089 | $42,361 | $43,632 | 7% |
| Insurance, software, accounting, licenses, waste, linens, phone | $42,200 | $43,466 | $44,770 | 7% |
| Left for the owner | $49,793 | $111,969 | $115,328 | 17% |

Startup: Build-out $90,000; Design, engineering, permits and legal $13,500; Equipment $79,500; Purchase of the existing fit-out and lease $149,000; Signage $8,000; Pre-opening payroll and training $8,113; Opening inventory $9,000; Launch marketing $15,000; Security deposit $10,860; Rent and NNN before opening $10,860; Contingency $16,950; Working capital reserve $47,990. Total $458,774.
Break-even $443,610 of sales a year (68% of base); paying the owner $60,000 takes $553,086. Sales per paid crew hour $73.

### Cafeteria for sale by Coral Gables (ZIP 33145)

| Line | Year 1 | Year 2 | Year 3 | Year 2, % of sales |
|---|---|---|---|---|
| Sales | $501,883 | $627,354 | $646,175 | 100% |
| Food and packaging | $92,630 | $115,787 | $119,261 | 18% |
| Hourly crew, with payroll taxes | $170,440 | $190,193 | $195,898 | 30% |
| Base rent | $39,083 | $40,255 | $41,463 | 6% |
| Utilities | $16,500 | $16,995 | $17,505 | 3% |
| Card fees, repairs, supplies, marketing, delivery, other | $48,181 | $60,226 | $62,033 | 10% |
| Delivery commissions, fundraiser shares and market fees | $34,569 | $41,711 | $42,962 | 7% |
| Insurance, software, accounting, licenses, waste, linens, phone | $42,200 | $43,466 | $44,770 | 7% |
| Left for the owner | $58,281 | $118,721 | $122,283 | 19% |

Startup: Build-out $60,500; Design, engineering, permits and legal $9,075; Equipment $84,500; Purchase of the existing fit-out and lease $199,000; Signage $8,000; Pre-opening payroll and training $8,113; Opening inventory $9,000; Launch marketing $15,000; Security deposit $9,771; Rent and NNN before opening $9,771; Contingency $14,500; Working capital reserve $44,704. Total $471,934.
Break-even $410,499 of sales a year (65% of base); paying the owner $60,000 takes $520,095. Sales per paid crew hour $71.


## Stress tests: Stage 2 at Dadeland Plaza, 830 sq ft

| Change | Sales, Year 2 | Left for the owner, base | Margin | At 80% of sales | Change against the design |
|---|---|---|---|---|---|
| The design as modeled | $668,463 | $129,152 | 19% | $55,804 | $0K |
| Window at half its design sales | $462,918 | $12,742 | 3% | −$37,324 | −$116K |
| Window at 75% | $565,690 | $70,947 | 13% | $9,240 | −$58K |
| Markets at half | $608,876 | $86,451 | 14% | $21,644 | −$43K |
| Office, gift and party orders at half | $631,501 | $104,333 | 17% | $35,949 | −$25K |
| No fundraisers | $604,190 | $100,241 | 17% | $32,675 | −$29K |
| No delivery apps | $620,282 | $106,595 | 17% | $37,759 | −$23K |
| Markets, orders and fundraisers all at half | $539,777 | $47,178 | 9% | −$9,775 | −$82K |
| Window only: no markets, orders, fundraisers or apps, same crew less the market crew | $362,909 | −$35,354 | −10% | −$72,599 | −$165K |
| A third baker, 40 hours a week (production runs at test-batch speed) | $668,463 | $84,581 | 13% | $14,799 | −$45K |
| Prices 5% lower | $635,136 | $102,656 | 16% | $34,608 | −$26K |
| Prices 5% higher | $701,790 | $155,647 | 22% | $77,000 | $26K |
| Food and packaging 3 points higher | $668,463 | $109,098 | 16% | $39,761 | −$20K |
| Rent $75 + $18 NNN instead of $55 + $12 | $668,463 | $106,924 | 16% | $33,577 | −$22K |
| Rent $40 + $10 NNN | $668,463 | $143,685 | 21% | $70,337 | $15K |

## Stress tests: Stage 1, the pop-up

| Change | Sales, Year 2 | Left for the owner, base | Margin | At 80% of sales | Change against the design |
|---|---|---|---|---|---|
| The design as modeled | $255,756 | $39,440 | 15% | $11,339 | $0K |
| Markets at 60% of design sales | $194,480 | −$5,083 | −3% | −$24,280 | −$45K |
| Markets at 150% (Roll & Dough's reported Saturday) | $332,351 | $95,094 | 29% | $55,862 | $56K |
| No fundraisers | $227,299 | $26,355 | 12% | $871 | −$13K |
| Pre-order drops and office orders at half | $218,702 | $11,803 | 5% | −$10,771 | −$28K |
| Commissary at $4,000 a month | $255,756 | $20,900 | 8% | −$7,201 | −$19K |
| Commissary at $1,750 a month | $255,756 | $48,710 | 19% | $20,609 | $9K |

## What a Stage 2 site must meet

Most base rent the roll kitchen can carry and still leave the owner $60,000 in Year 2, by size, NNN and window index (a former food bay: $55 a sq ft build-out, the $15,000 pop-up credit, 4 months to open):

| Size and NNN | Window index 0.6 | 0.8 | 0.9 | 1.0 | 1.1 |
|---|---|---|---|---|---|
| 850 sq ft, $12 NNN | $26 | $79 | $105 | $132 | $159 |
| 1,000 sq ft, $12 NNN | $18 | $63 | $86 | $108 | $131 |
| 1,200 sq ft, $12 NNN | $10 | $48 | $67 | $86 | $105 |
| 1,500 sq ft, $12 NNN | $3 | $33 | $48 | $63 | $78 |
| 2,000 sq ft, $10 NNN | none | $20 | $31 | $43 | $54 |

Left for the owner at Dadeland Plaza's assumed rent, by window index (other channels at design): 0.4: −$10,540; 0.5: $12,742; 0.6: $36,024; 0.75: $70,947; 0.9: $105,870; 1.0: $129,152; 1.1: $152,434; 1.25: $187,356.

## Stage 3 illustration: filling the one kitchen

The Dadeland Plaza kitchen with no second lease: a second market team (124 stall-days), office orders up 60%, 30 fundraisers, grocers' shelves (loaves and frozen packs at 62% of the window price) and a window 10% busier as the name gets known. Crew added: 30 more baker hours a week, 12 more order-desk hours, a second market crew and a 12-hour driver; a leased van. Illustrative: no grocer has agreed and the volumes are targets, not estimates.

| | Stage 2 design | Stage 3 illustration |
|---|---|---|
| Sales, steady year | $668,463 | $989,540 |
| Paid crew hours a working day | 30.6 | 43.6 |
| Sales per paid crew hour | $74 | $77 |
| Food and packaging, % of sales | 18% | 19% |
| Hourly crew, % of sales | 29% | 28% |
| Rent, NNN and utilities, % of sales | 10% | 7% |
| Left for the owner: low / base / high | $56K / $129,152 / $202K | $141K / $249,797 / $359K |
| Margin before owner's pay | 19% | 25% |
| Margin after paying a manager $70,000 with payroll taxes | 8% | 17% |
| With prices 5% higher | $155,647 (22%) | $289,095 (28%) |

Stage 3 sales by channel: Walk-up window and pre-order pickup $399,200; Farmers markets and pop-ups $238,350; Office, gift and party orders $118,280; School, league and church fundraisers $107,121; Delivery apps $53,000; Grocers' shelves: loaves and frozen packs at wholesale $73,589.

## Channel economics at the Stage 2 design (allocation is judgment)

Each channel's sales less its own food and packaging (with the buffer), the 9.6% of variable costs, its commissions or fees and the selling crew assigned to it. Production labor, rent and overheads are shared and not allocated.

| Channel | Sales a year | Food and packaging | Variable costs | Commissions, shares, fees | Selling crew | Contribution | % of sales |
|---|---|---|---|---|---|---|---|
| Walk-up window and pre-order pickup | $362,909 | $69,842 | $34,839 | $0 | $48,655 | $209,573 | 58% |
| Farmers markets and pop-ups | $119,175 | $22,334 | $11,441 | $7,025 | $14,975 | $63,401 | 53% |
| Office, gift and party orders | $73,925 | $13,495 | $7,097 | $3,696 | $11,473 | $38,164 | 52% |
| School, league and church fundraisers | $64,273 | $9,910 | $6,170 | $19,282 | $3,824 | $25,087 | 39% |
| Delivery apps | $48,182 | $7,990 | $4,625 | $13,009 | $4,265 | $18,292 | 38% |
| **All channels** | $668,463 | | | | | **$354,516** | 53% |

Shared costs in Year 2: production lead, baker and cleaning $111,797; rent and NNN $57,278; utilities $12,824; insurance, software and other fixed costs $43,466. Contribution less shared costs is about $129,152; the model's own figure is $129,152 (the difference is rounding in the crew's flex with sales).

