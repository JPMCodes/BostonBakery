# Verification batch 1: Boston-area bakery site candidates

Checked: 2026-11-07. This file covers 20 candidates taken from the sweep notes in this folder (`sweep_boston-lease.md`, `sweep_suburb-lease.md`, `sweep_business-for-sale.md`, `sweep_vacated-food-spaces.md`).

## How the checks were done

- **City records (Boston addresses):** queried the City of Boston food-establishment inspection data on data.boston.gov (resource `4582bec6-2b4f-4f9e-bc55-cbaa73117f4c`) for a range of street numbers around each address. Also searched the Licensing Board licence list (`04dc653b-1789-4374-9669-b07df7233344`, which includes Common Victualler licences) and the active food-licence list (`f1e13724-284d-478c-b8bc-ef042aa5b70b`). Both lists had been downloaded earlier and were searched locally. Inspection comments were then searched for "hood", "grease", "exhaust", "fryer" and "walk-in" to find evidence of kitchen equipment.
- **boston.com listing pages:** re-read 8 MLS pages today to confirm each listing's market status.
- **Boston Restaurant Talk:** searched 672 posts (2025-10-15 to 2026-11-06), saved by an earlier sweep, for openings and closings at these addresses.
- **Web searches:** 15 searches (listed at the end).
- **Sites not read directly:** LoopNet, Crexi, CityFeet, Showcase, BizQuest and BizBuySell pages were not fetched (they block automated access). Details from those sites come from search snippets and are marked as such.
- **uphamscorner.org could not be reached:** the host is not on this session's allowed network list, so the 750 Dudley St entry rests on a search snippet and the earlier sweep. The site has to be allowed in the session's network settings before it can be checked here.
- **Raw data files:** saved in `/tmp/claude-0/-home-user-BostonBakery/f936cb80-2548-5c6e-84ff-5b8b8418bc02/scratchpad/downloads/verify_batch_1/`.

**Scoring** uses the task rubric: size 0-2, rent or deal 0-2, second-generation food space 0-3, location 0-2, status 0-1. Annual rent = size x rent per sq ft; sales needed = annual rent / 0.08. In the tables, "-" means not stated.

## Bottom line

**Best live leads (score 9; active or likely active):**
1. **3089-3091 Washington St, Egleston Square:** live on boston.com. Star Fish Market held a food permit here from Nov 2024 to early 2026, and city inspections recorded a **hood system (Feb 2025) and a grease trap (Feb 2026)**. 1,490 sq ft at $29 = $43,210/yr, which needs about $540K in sales. The lease type is not stated, and the square draws mostly local traffic.
2. **349 Centre St, Jamaica Plain:** live. It was a restaurant for more than ten years (Tacos El Charro, then The Old Havana until 2022), and inspections recorded a hood over the fryolators, exhaust and a grease trap. The current listing describes an office-style renovation, so the kitchen may be gone. Rent is $30/sq ft for the full 2,380 sq ft, or $3,950/month for a 1,200 sq ft partial (about $593K in sales needed). The listing says zoning allows restaurant use.
3. **250 Huntington Ave #1, Symphony:** live. This is the former Ginger Exchange (2013-2024). Inspections recorded hood filters over the wok station and walk-ins, and the listing includes 3 walk-ins and all fixtures. **Rent conflict:** this lease listing says $4,000/month, but the same broker's active sale listing for the same restaurant says **$14,000/month** ($60.76/sq ft, about $2.1M in sales needed). Confirm the rent first.
4. **34 Harvard Ave, Allston Village:** almost certainly The Draft's former space. The Licensing Board pulled The Draft's liquor licence in Jan 2026, and the Boston Globe reported on 2026-08-20 that the building sits empty. Inspections recorded a hood, fryers and a basement walk-in. Rent is on request plus NNN. Inspections in 2025 also found heavy rodent activity, leaks and wall damage in the lower level.
5. **1105 Mass Ave, Cambridge (Harvard Sq east edge):** former Zoe's, then Beyond Full, which closed in June 2026. A "for lease" sign was seen in July 2026, and no new tenant has been reported. The listing mentions a large hood and 2 walk-ins. The only rate found, $35/sq ft, is from the 2024 listing.
6. **Roslindale former pizza shop (BizQuest BW2472318):** turnkey, with equipment the listing calls "excellent". About 1,400 sq ft at $29 NNN with 3% annual increases, a 5-year term plus one 5-year option. The address is withheld.
7. **Lexington Center fast-casual cafe (BizQuest BW2476956):** asking $165,000 for a new build-out of 1,550 sq ft with 12 seats. Rent is $6,563/month ($50.81/sq ft, which needs about $985K in sales). Revenue, earnings and lease term are not stated.

**Already taken (marked leased_or_sold):**
- **1260-1270 River St, Hyde Park:** Sunrise Cafe Bagels & Diner was licensed in Aug-Oct 2026 and has been open since mid-October 2026 in the former Papa Gino's space.
- **912 Beacon St:** the city now lists a Common Victualler licence for Teaholic Boston Inc covering a "1,000SF takeout-only boba milk tea shop" at this address.
- **23 S Huntington Ave:** Kohinoor Flames Inc received a Common Victualler licence on 2026-10-16 for the 1,274 sq ft restaurant, with the board note "temporarily closed under renovations".

**Weaker leads:**
- **1211 Commonwealth Ave:** $60/sq ft and raw space.
- **2070 Centre St:** raw retail with no food history.
- **152 Liverpool St:** a new shell with no food history.
- **879-881 Blue Hill Ave:** a vacant building of 7,000+ sq ft, size of the unit not stated.
- **167 Mass Ave:** 2,900 sq ft, rent unpublished, food use ended around 2015.
- **1248-1260 Cambridge St:** $60/sq ft NNN, which needs about $1.78M in sales, and the building may be redeveloped.
- **361 Huron Ave:** the listing is 6 months old.
- **Boston cafe asset sale BW2482986:** priced at 4.3x seller earnings, with rent at 24% of sales.
- **Davis Square cafe:** thin, conflicting data.
- **750 Dudley St:** cheap, but availability is unconfirmed.

## Summary table

| # | Candidate | Kind | Status | Fit | SF | Rent $/SF/yr | Annual rent | Sales needed at 8% | 2nd-gen |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 3089-3091 Washington St (Egleston Sq) | lease | active | 9 | 1,490 | 29 | $43,210 | $540,125 | confirmed (hood + grease trap in city inspections) |
| 2 | 349 Centre St (JP), full / #A partial | lease | active | 9 | 2,380 / 1,200 | 30 / 39.50 | $71,400 / $47,400 | $892,500 / $592,500 | likely (restaurant to 2022; renovated since) |
| 3 | 250 Huntington Ave #1 (Symphony) | lease | active | 9 | 2,765 (+1,500 storage) | 17.36 (or 60.76, see notes) | $48,000 (or $168,000) | $600,000 (or $2.1M) | confirmed (hood, walk-ins) |
| 4 | 34 Harvard Ave (Allston) | lease | likely_active | 9 | 2,181 | - (NNN) | - | - | confirmed (hood, fryers, walk-in) |
| 5 | 1105 Mass Ave (Cambridge) | lease | likely_active | 9 | 2,500 | 35 (2024 rate) | $87,500 | $1,093,750 | confirmed (large hood, 2 walk-ins) |
| 6 | Roslindale former pizza shop (BW2472318) | lease | likely_active | 9 | 1,400 | 29 NNN | $40,600 (listing says $46,690) | $507,500 ($583,625) | confirmed (former pizza shop, equipped) |
| 7 | Lexington Center fast-casual cafe (BW2476956) | business for sale | likely_active | 9 | 1,550 | 50.81 | $78,756 | $984,444 | confirmed (operating cafe) |
| 8 | 750 Dudley St (Upham's Corner) | lease | stale_or_unclear | 8 | 1,720 | 20.93 | $36,000 | $450,000 | confirmed (Paraiso Restaurant; hood noted 2014) |
| 9 | Davis Square "Charming Cafe" | business for sale | likely_active | 8 | - (800-1,000?) | 36 | - | - | confirmed (operating cafe; hood doubtful) |
| 10 | 1248-1260 Cambridge St (Inman) | lease | stale_or_unclear | 8 | 2,372 | 60 NNN | $142,320 | $1,779,000 | confirmed (former Wit's End bar/restaurant) |
| 11 | 1260-1270 River St (Hyde Park) | lease | leased_or_sold | 8 | 1,934 | 28 NNN | $54,152 | $676,900 | confirmed (ex-Papa Gino's) |
| 12 | High-Traffic Boston Cafe (BW2482986) | business for sale | likely_active | 7 | 1,750 | 31.89 base | $55,808 | $697,594 | confirmed (newly built cafe/bakery) |
| 13 | 912 Beacon St (Kenmore) | lease | leased_or_sold | 7 | 1,000 | - | - | - | confirmed (Gong Cha) |
| 14 | 23 S Huntington Ave (JP/Mission Hill) | lease | leased_or_sold | 7 | 1,274 | - | - | - | confirmed (Wok 'N Talk) |
| 15 | 361 Huron Ave (Cambridge) | lease | stale_or_unclear | 7 | 2,358 (divisible 1,179) | - (NNN) | - | - | confirmed per listing ("2nd gen cafe") |
| 16 | 1211 Commonwealth Ave (Allston) | lease | active | 6 | 2,000 | 60 | $120,000 | $1,500,000 | no |
| 17 | 152 Liverpool St (East Boston) | lease | likely_active | 6 | 1,185 | 35 NNN | $41,475 | $518,438 | no (first-generation) |
| 18 | 2070 Centre St (West Roxbury) | lease | active | 6 | 1,250 | 31.68 | $39,600 | $495,000 | no |
| 19 | 167 Mass Ave (Back Bay/Fenway) | lease | likely_active | 6 | 2,900 | - | - | - | likely (Bangkok City to ~2015) |
| 20 | 879-881 Blue Hill Ave (Dorchester) | lease | active | 6 | - | 25 | - | - | unknown |

## Candidate details

### 1. 3089-3091 Washington St, Boston 02119 (Egleston Square). Key `3089 washington|roxbury`
- **Status: active.** On boston.com the listing (MLS 73497894) shows "Market Status: Available", added 9/28/2026 and 40 days on market, re-read 2026-11-07.
- **Space and rent:** "Turnkey 1,490 SF... at $29 per sf"; countertops, deep freezer, "restaurant quality equipment", employee restroom. Lease type not stated. $29 x 1,490 = $43,210/yr, which needs about $540K in sales at 8%.
- **Second generation: confirmed.** Star Fish Market held an Eating & Drinking permit at 3089 Washington St (licence 581615, issued 2024-11-14, now inactive). Inspection notes:
  - 2025-02-03: "Hood system observed heavily soiled... Hood sticker expires: 2.19.25"
  - 2026-02-12: "Grease trap covered with plastic film and cardboard" and "2026 Health Permit is unpaid"
- **Licence and zoning:** no active permit or Common Victualler licence at the address; a new operator needs both. Food use was permitted here until 2026. Zoning not stated.
- **Traffic:** prime corner in Egleston Square next to a municipal lot, Santander Bank and McDonald's; MBTA bus (listing). Neighborhood traffic, with no weekend destination named.
- **Risks:**
  - NNN may come on top of the $29.
  - The hood and grease trap were last seen in 2025-26, and the 2026 inspection noted a leaking sink drain.
  - A fish-market tenant means cleanup and odor work.
- **Fit: 9** (size 2, rent 2, second-gen 3, location 1, status 1).

### 2. 349 Centre St, Boston 02130 (Jamaica Plain). Key `349 centre|jamaica`
- **Status: active.** Two boston.com listings, both "Available" as of 2026-11-07, added 9/16/2026, 52 days on market:
  - full space, MLS 73578246: 2,380 sq ft at $5,950/month
  - partial #A, MLS 73578251: 1,200 sq ft at $3,950/month
- **Rent:** full space $30/sq ft, $71,400/yr, about $892,500 in sales needed. Partial #A $39.50/sq ft, $47,400/yr, about $592,500. Lease type not stated.
- **Second generation: likely.** City records show restaurants here from about 2011 to 2022:
  - Tacos El Charro (licences 19287 and 76711), then The Old Havana (licence 123900, expired 2023-01-01).
  - Inspections recorded "panels above the fryolators" (hood), "wall mounted exhaust" and "clean and degrease greasetrap" (2019-2022).
  - Today's listing describes a renovated flex layout (two open areas, two private rooms, updated flooring, renovated bathroom, large basement) and names no kitchen, so the hood may have been removed.
- **Licence and zoning:** the listing says "flexible zoning suitable for... office, restaurant, retail, and service". No active permit; a new permit and Common Victualler licence are needed.
- **Traffic:** corner on JP's Centre St between Jackson Square (Orange Line) and Hyde Square, "great visibility" (listing).
- **Risks:**
  - Kitchen equipment is probably stripped.
  - Lease type is unknown.
  - The partial would share the space with another tenant.
- **Fit: 9** (2, 2, 2, 2, 1).

### 3. 250 Huntington Ave #1, Boston 02115 (Symphony). Key `250 huntington|fenway`
- **Status: active.** The boston.com lease listing (MLS 73594131) shows "Available", added 10/22/2026, 16 days on market.
- **Rent conflict:**
  - The lease listing: "Landlord will give new owner long term lease monthly is **4k** (tax excluded)". That is $48,000/yr, $17.36/sq ft on 2,765 sq ft, or $11.25 including the storage.
  - The same broker's **sale** listing for the same restaurant (MLS 73498139, "Available", added 9/3/2026, price field $1) has otherwise identical text but says "monthly is **14k** (tax excluded)". That is $168,000/yr, $60.76/sq ft, and about $2.1M in sales at 8%.
  - The $14K figure fits the location and the long time the space has sat unsold better. One of the two is probably a typo.
- **Business-sale history:** BMN Boston showed MLS 73498139 at **$20,000** (listed 2026-04-08), and an earlier MLS 73333901 was listed at $10,000 on 2025-02-10.
- **Real-estate tax:** the lease listing shows $20,000/yr, excluded from the rent.
- **Second generation: confirmed.** Ginger Exchange (licence 86534, 2013 to 2024; the city marked it "not required" on 2024-10-31, i.e. closed), and before it Betty's Wok & Noodle Diner. Inspections recorded "Hood filters above the wok station", a fryer and walk-in units. The listing offers 2,765 sq ft plus 1,500 sq ft of storage with 3 walk-ins, a liquor room, 2 offices and a locker room, and "all business fixtures as is".
- **Licence:** no active permit or Common Victualler licence at 250 Huntington (only Symphony Hall at 251). A new operator needs both.
- **Traffic:** across from Symphony Hall; near the Huntington Theatre, Berklee Performance Center, Boston Conservatory, Northeastern, Wentworth and the Symphony Green Line stop. Evening, weekend and student crowds.
- **Risks:**
  - The rent conflict above.
  - Real-estate tax passed through on top of the rent.
  - Fixtures are sold as-is with no warranty.
  - The space has been dark since late 2024.
  - It is larger than a counter bakery needs.
- **Fit: 9** (size 2, rent 1 because the two listings conflict, second-gen 3, location 2, status 1).

### 4. 34 Harvard Ave, Boston 02134 (Allston Village). Key `34 harvard|allston`
- **Status: likely_active.**
  - Broker listing (Boston Realty Advisors, via CommercialCafe and CommercialSearch snippets): "2nd gen restaurant", 2,181 sq ft, NNN, rent on request, renewal option, "available immediately", updated 2026-06-15.
  - The Draft Bar & Grille at 32-34 Harvard Ave was shut down after the Licensing Board indefinitely pulled its liquor licence for repeated underage-drinking violations (Axios 2026-01-08; CBS Boston).
  - The Boston Globe (2026-08-20) says the building now sits empty.
  - The city food permit (licence 28545) is inactive, with "HE_NotReq" logged 2026-08-20.
  - No new tenant was found.
- **Second generation: confirmed.** Inspections recorded "Hood sticker expired January 2025 - Schedule hood cleaning", "hood vents with grease buildup", fryers on the hot line and a basement walk-in cooler. The Licensing Board record describes "two rooms and kitchen on first floor; cellar for stock", a seasonal rear patio and capacity 175.
- **Licence:** Metro Dining's all-alcohol Common Victualler licence still appears in the city list (expiring 2026-12-31) but was pulled by the board, so there is nothing to inherit. A new Common Victualler licence is needed.
- **Traffic:** Harvard Ave at the Commonwealth Ave end of Allston Village, near the Green Line Harvard Ave stop. Student-heavy. The Globe reports local businesses leaving Harvard Ave.
- **Risks:**
  - Rent unknown, with NNN on top.
  - Inspections in June and Aug 2025 found heavy rodent activity, pipes leaking into buckets, damaged walls and excess equipment in the lower level.
  - The layout is bar-oriented.
  - Student seasonality.
- **Fit: 9** (2, 1, 3, 2, 1).

### 5. 1105 Massachusetts Ave, Cambridge 02138. Key `1105 massachusetts|cambridge`
- **Status: likely_active.**
  - Boston Restaurant Talk (2026-07-01): Beyond Full closed, with a "for lease" sign in the window.
  - No new tenant appears in Boston Restaurant Talk posts through 2026-11-06 or in two searches.
  - The only broker listing found is CRG Commercial's LoopNet listing from 2024-09-18: about 2,500 sq ft at about $35/sq ft, rate excluding some expenses.
  - Verani shows MLS 73291906 as "sold", probably the 2025 lease to Beyond Full.
  - Cafe Sushi also occupies this address (a 10,000 sq ft, two-unit property).
- **Rent:** 2,500 x $35 = $87,500/yr, about $1.09M in sales. That is bakery-cafe scale.
- **Second generation: confirmed.** The listing mentions an "excessively large hood system", 2 walk-ins, a large storage room, a counter/bar, 114-person occupancy and a former beer and wine licence. Diner use: Zoe's, then Beyond Full (Aug 2025 to Jun 2026).
- **Traffic:** "just outside Harvard Square" on the stretch toward Central Square. Student and visitor traffic.
- **Risks:**
  - The current asking rent is unknown (the $35 is from 2024), so rent is scored as unknown.
  - Two operators have closed here since 2024.
  - NNN or gross not stated.
- **Fit: 9** (2, 1, 3, 2, 1).

### 6. Roslindale former pizza shop (BizQuest BW2472318). Key `url:https://images bizquest com/real-estate-for-lease/pizzeria-fast-casual-space-for-lease-roslindale/bw2472318`
- **Status: likely_active.** Still shown on BizQuest's Massachusetts and Roslindale real-estate category pages (search 2026-11-07). The listing is undated.
- **Terms (snippet):** "turnkey restaurant space... previously operated as a successful pizza shop"; "BASE RENT: $29 SF/ $46,690 annual with 3% annual increases"; about 1,400 RSF; NNN; 5-year term plus one 5-year option; street parking only; "equipment is in excellent condition".
- **Rent math:** 1,400 x $29 = $40,600, needing $507,500 in sales. The stated $46,690 implies about 1,610 sq ft and needs $583,625.
- **Second generation: confirmed** (former pizza shop, equipped). Hood not stated.
- **Address:** withheld. City data shows recent Roslindale pizza closures (Nicholas Sub & Pizza at 600 Hyde Park Ave, permit lapsed 2026-01-01; Domino's at 4640 Washington St, inactive 2026), but neither is tied to this listing.
- **Risks:** NNN on top; size conflict; unknown location within Roslindale; undated listing.
- **Fit: 9** (2, 2, 3, 1, 1).

### 7. Lexington Center fast-casual cafe (BizQuest BW2476956). Key `url:https://www bizbuysell com/massachusetts/lexington/coffee-shops-and-cafes-for-sale/`
- **Status: likely_active.** The BizQuest listing and Lexington category pages are indexed as of 2026-11-07. The listing is undated.
- **Terms (snippet):** asking **$165,000** (earlier snapshots showed $160,000 to $185,000); 1,550 sq ft; ADA compliant; 12 seats; new build-out suited to sandwiches, soups, salads, bowls, smoothies and coffee; rent **$6,563/month** ($78,756/yr = $50.81/sq ft); shared parking of about 70 spaces.
- **Not stated:** revenue, seller's earnings, lease remaining and whether the lease transfers.
- **Rent math:** about $985K in sales needed at 8%, which is above a counter bakery's $0.6-0.8M.
- **Second generation: confirmed** (operating cafe). Hood not stated.
- **Traffic:** Lexington Center, a historic town center with weekend visitors.
- **Fit: 9** (size 2, deal 1 because financials are unknown, 3, 2, 1).

### 8. 750 Dudley St, Boston 02125 (Upham's Corner). Key `750 dudley|dorchester`
- **Status: stale_or_unclear.**
  - The only source is the Upham's Corner Main Street vacancy list: "750 Dudley Street, formerly Paradiso Restaurant", 1,720 sq ft, $3,000/month plus utilities and CAM, updated about 2026-02-10 per the earlier sweep. The page could not be fetched from here.
  - No broker listing was found.
  - No food or Common Victualler licence has been issued at the address since then.
  - The neighboring 748 Dudley St (a former furniture store, $4,800/month, tenant pays taxes, insurance and water) is live on boston.com (MLS 73469396). 749 Dudley across the street (6,300 sq ft) was listed at $29 in 2025.
- **Rent:** $36,000/yr ($20.93/sq ft), needing $450K in sales.
- **Second generation: confirmed.** Paraiso Restaurant held licence 76033 to about 2019-2020 (expired 2020-01-01); earlier, Seven 50 Grille. Inspections recorded "Clean overhead hood and all attachments" (2014) and walk-in cooler notes (2016-2017). The vacancy list says "built out".
- **Risks:**
  - Vacant about 6 years, so the condition of the equipment is unknown.
  - CAM and utilities come on top of the rent.
  - Availability is not confirmed.
- **Fit: 8** (2, 2, 3, 1, 0).

### 9. Davis Square "Charming Cafe for Sale," Somerville. Key `url:https://vantagepointretail com/restaurants/`
- **Status: likely_active.** BizQuest's Somerville food & beverage for-sale page lists "Davis Square Somerville - Charming Cafe for Sale" at **$165,000**, asset sale, lease only, **$36.00/SF/year** (search 2026-11-07).
- **Not stated:** size, seats and financials.
- **Possible match:** a Vantage Point snippet block shows the same $165,000 price for a "1,000 SF + full basement" cafe/restaurant leasehold at $3,158/month NNN plus about $650/month tax and water (about $45.70/sq ft all-in), lease to October 2029. That tie is inferred from the price, not confirmed.
- **Conflicting snippet:** another snippet showed 800 sq ft with no hood. Because of the conflict, size is reported as not stated.
- **Second generation: confirmed** (operating cafe, leasehold improvements and furniture, fixtures and equipment included). A hood is doubtful.
- **Traffic:** Davis Square, a Red Line square with weekend crowds.
- **Risks:**
  - No financials.
  - Size and lease details are inferred.
  - The lease may run only to Oct 2029 with no option seen.
  - Possibly no hood.
  - The broker page mixes several listings.
- **Fit: 8** (size 1 because unknown, deal 1, 3, 2, 1).

### 10. 1248-1260 Cambridge St, Cambridge 02139 (Inman Square). Key `1248 cambridge|cambridge`
- **Status: stale_or_unclear.** A Godino & Company listing (Showcase, CityFeet, LoopNet 34594831) offers a "fully equipped bar and restaurant, formerly operated by Wit's End" at the corner of Cambridge and Prospect streets: 2,372 sq ft at $11,860/month ($60/sq ft NNN), 99 diners plus bar seating, 40 draft lines, furniture and fixtures for sale, 5-year term. The listing is undated. LoopNet 40541948 separately markets the 4,744 sq ft building as a redevelopment or owner-user opportunity. No closure or opening news was found for this address; the Turing Tavern and Urban Hearth moves concern 1281 Cambridge St.
- **Rent:** $142,320/yr base, plus NNN, needing about $1.78M in sales.
- **Second generation: confirmed** (operating bar and restaurant build-out). Hood and grease trap not stated.
- **Fit: 8** (2, 1, 3, 2, 0).
- **Verdict:** too expensive, and the building may be sold.

### 11. 1260-1270 River St, Hyde Park (Cleary Square). Key `1260 river|hyde`
- **Status: leased_or_sold.**
  - Sunrise Cafe Bagels & Diner LLC received Common Victualler licence LB-634380 on 2026-08-28 for 1270 River St: "1,840SF... seating for 34 patrons, a commercial kitchen". Its food permit was issued 2026-10-01.
  - Boston Restaurant Talk (2026-09-09, updated Oct 14) says it opened in the former Papa Gino's space in Cleary Square. Papa Gino's permit expired 2026-01-01, and its last inspection was 2025-09-09.
  - The listing's MLS 73449276 was "695 Truman/1270 River".
- **Small residual risk:** the listing could have been the corner unit at 695 Truman Hwy (a former Domino's with no food permit since early 2024).
- **Fit: 8** (2, 2, 3, 1, 0), but the space is taken.

### 12. "High-Traffic Boston Cafe Opportunity – Flexible Concept" (BizQuest BW2482986). Key `url:https://images bizquest com/asset-sales/high-traffic-boston-cafe-opportunity-flexible-concept/bw2482986`
- **Status: likely_active.** The listing page is still indexed on 2026-11-07, with no sold flag. It is undated.
- **Terms (snippets, fragmentary):**
  - Asking $275,000 (other snippets showed $549,000 or $49,000).
  - Revenue $322,744; seller's earnings $64,317. The ask is 0.85x revenue and 4.3x earnings.
  - Rent $4,651/month base plus $1,750/month NNN, 1,750 sq ft ($31.89 base, $43.89 all-in). All-in occupancy of $76,812/yr is 24% of current sales.
  - Lease remaining not stated. Neighborhood confidential. The seller is moving.
- **Second generation: confirmed** (newly built cafe and bakery). Hood not stated.
- **Fit: 7** (2, deal 0, 3, 1, 1).

### 13. 912 Beacon St, Boston 02215 (Kenmore / Brookline line). Key `912 beacon|fenway/kenmore`
- **Status: leased_or_sold.** The Licensing Board list now includes Common Victualler licence LB-637124 for **Teaholic Boston Inc** at 912 Beacon St: "1,000SF Takeout-only boba milk tea shop... The rear area consists of a food preparation/kitchen space, back office". That matches the listing's 1,000 sq ft turnkey cafe with a rear prep kitchen (Atlantic Retail, updated 2026-04-24). Gong Cha has held the city permit here since 2024; reviews describe it as newly opened in mid-2025.
- **Second generation: confirmed.** A new tea-shop operator appears to have the space.
- **Fit: 7** (2, 1, 3, 1, 0).

### 14. 23 South Huntington Ave, Boston 02130. Key `23 south|jamaica`
- **Status: leased_or_sold.** Common Victualler licence LB-635903 was issued 2026-10-16 to **Kohinoor Flames Inc**: "A 1,274SF Full-service restaurant... 24 seats and a fully equipped kitchen... basement... storage". The board note reads "10 16 2026 – Temporarily Closed Under Renovations". This is the space CBRE marketed in May 2026.
- **Second generation: confirmed.** Wok 'N Talk was here 2011-2023; inspections recorded a hood over the fryolators, a grease trap and a basement walk-in.
- **Fit: 7** (2, 1, 3, 1, 0).

### 15. 361 Huron Ave, Cambridge 02138 (Huron Village). Key `361 huron|cambridge`
- **Status: stale_or_unclear.**
  - The listing ("2nd gen cafe space", first floor divisible 1,179-2,358 sq ft, BA-1 zoning, NNN, rate on request) dates from LoopNet 2026-05-04 and CommercialCafe 2026-05-12. No newer evidence was found (one search returned nothing).
  - A Showcase listing also offers the building for sale.
  - Next door at 359 Huron Ave, Fupo Cafe closed in Jan 2026 and Sumi House opened in Mar 2026 (Boston Restaurant Talk). Confirm the listing is not that space.
- **Second generation: confirmed per the listing.** The prior cafe could not be identified; hood and grease trap not stated.
- **Fit: 7** (2, 1, 3, 1, 0).

### 16. 1211 Commonwealth Ave, Boston 02134 (Allston). Key `1211 commonwealth|allston`
- **Status: active.** boston.com MLS 73327918 shows "Available", added 9/3/2026, 64 days on market. The MLS number suggests a first listing around early 2025.
- **Terms:** about 2,000 sq ft plus an optional 700 sq ft lower level; $60 in the price field (appears to be $/sq ft/yr), which is $120,000/yr and needs $1.5M in sales.
- **Second generation: no.** There is no food-licence record at 1211 Comm Ave; the neighbors at 1213 (Five Guys, Habibi's Lounge, Banchan & Co., which opened in Apr 2026) are separate. The listing names no kitchen.
- **Fit: 6** (2, 1, 0, 2, 1).

### 17. 152-154 Liverpool St, Boston 02128 (East Boston). Key `152 liverpool|east`
- **Status: likely_active.**
  - CBRE, CommercialCafe and CommercialSearch show a 1,185 sq ft restaurant-designated unit, "available immediately", contact for pricing, updated 2026-05-07.
  - The CBRE page header says "Available March 2024".
  - An MLS copy at $35/sq ft NNN was removed 2025-10-01 and later shown active again.
  - No tenant news, and no food licence at 150-156 Liverpool St.
- **Second generation: no.** This is a first-generation shell in a building from about 2020; venting not stated.
- **Fit: 6** (2, 2, 0, 1, 1).

### 18. 2070 Centre St, Boston 02132 (West Roxbury). Key `2070 centre|west`
- **Status: active.** boston.com MLS 73594011 shows "Available", added 10/22/2026.
- **Terms:** 1,250 sq ft at $3,300/month ($31.68/sq ft, $39,600/yr, $495K sales needed); lease terms negotiable; real-estate tax of $25,240/yr shown.
- **Second generation: no.** There is no food-licence record at 2066-2074 Centre St. The listing calls it "PRIME RETAIL SPACE" and suggests child care, salon, cafe or office.
- **Fit: 6** (2, 2, 0, 1, 1).

### 19. 167 Massachusetts Ave, Boston 02115. Key `167 massachusetts|back`
- **Status: likely_active.** CommercialCafe, CommercialSearch and CityFeet show about 2,900 sq ft (3,000 on CityFeet) of restaurant-designated space with an open layout "ready for a redesign", rent on request, updated 2026-06-05 and 2026-04-16 (GraffitoSP brokers).
- **Second generation: likely.** Bangkok City Restaurant was here until about 2015 (licence 19392, expired 2016-01-01), and no food permit has been issued since.
- **Fit: 6** (size 1, rent 1, 2, 1, 1).

### 20. 879-881 Blue Hill Ave, Boston 02124 (Dorchester). Key `879 blue|dorchester`
- **Status: active.** boston.com MLS 73489797 shows "Available", added 9/3/2026, 65 days on market.
- **Terms:** a "massive mixed-use commercial building", vacant, $25 in the price field, unit #2 separately at $3,000/month; real-estate tax of $63,589/yr shown.
- **Second generation: unknown.** El Punto Restaurant & Lounge holds an all-alcohol Common Victualler licence (issued 2024-08-30, expires 2026-12-31) for "7,380SF on first floor... Kitchen, bar, lounge... seating capacity of 240". The licence is flagged "2026 TEMP CLOSED NEED DOCS Do Not Issue". There are no health-inspection records at 875-885 Blue Hill Ave, so it is unclear whether a kitchen ever operated.
- **Fit: 6** (size 1, 2, 1, 1, 1).

## City-record lookups (Boston addresses)

Street-number ranges were searched in the inspection data. Licence numbers are the city's.

| Address | Food permits on record (latest first) | Licensing Board (Common Victualler) |
|---|---|---|
| 746-754 Dudley St | New Ho Toy, 746 (active); Paraiso Restaurant, 750 (to 2020); Seven 50 Grille, 750 (to 2010) | New Ho Toy, 746 |
| 246-254 Huntington Ave | Ginger Exchange, 250 (2013 to 2024); Betty's Wok & Noodle Diner, 250 (to 2013) | Symphony Hall, 251 only |
| 3085-3095 Washington St | Star Fish Market, 3089 (Nov 2024 to early 2026, inactive); La Parada, 3094 (active); La Peraviana Market, 3093 (active) | La Parada, 3094; Castillo Egleston Liquors, 3086 |
| 1207-1215 Commonwealth Ave | 1213: Five Guys, Habibi's Lounge, Banchan & Co. (Apr 2026); House of Shawarma (to 2024); 1215: Berezka market. Nothing at 1211 | none |
| 150-156 Liverpool St | none | none |
| 345-353 Centre St | Rizzo's Pizza, 347 (active); The Old Havana, 349 (to 2022); Tacos El Charro, 349 | Rizzo's Pizza, 347 |
| 2066-2074 Centre St | none | none |
| 30-38 Harvard Ave | The Draft Bar & Grill, 32 (inactive; "not required" 2026-08-20) | Metro Dining (The Draft), 32-34: all-alcohol Common Victualler licence and billiards licence |
| 163-171 Mass Ave | Bangkok City Restaurant, 167 (to ~2015) | none |
| 908-916 Beacon St | Gong Cha, 912 (permit 2024); Sol Azteca, 914 (active) | Teaholic Boston Inc, 912 (new); Sol Azteca, 912-914A |
| 1256-1274 River St | Sunrise Cafe Bagels & Diner, 1270 (Oct 2026); Papa Gino's, 1270 (to 2025); River Grille, 1263 (to 2023) | Sunrise Cafe, 1270 (issued 2026-08-28); Boston Restaurant Bar & Grills, 1263-1269 |
| 690-699 Truman Hwy | Domino's, 695 (to early 2024) | none |
| 19-27 S Huntington Ave | Wok 'N Talk, 23 (to 2023) | Kohinoor Flames Inc, 23 (issued 2026-10-16, under renovation) |
| 875-885 Blue Hill Ave | none (Sun Pizza at 870, across the street) | El Punto Restaurant & Lounge, 879-881 (all-alcohol; flagged temporarily closed) |

## Searches used (15 of 15)

1. `"1105 Massachusetts Ave" Cambridge restaurant space for lease 2026`: only the 2024 CRG listing and $35/sq ft; Verani shows MLS 73291906 as sold.
2. `"750 Dudley" Dorchester restaurant space lease OR leased OR opening 2026`: the vacancy list names "750 Dudley Street, formerly Paradiso Restaurant"; no current broker listing; 749 Dudley listed at $29 (2025).
3. `"The Draft" Bar Grille "34 Harvard Ave" Allston closed OR closing OR lease 2026`: licence pulled Jan 2026 (Axios, CBS); Globe 2026-08-20 says the building is empty.
4. `Roslindale pizzeria fast-casual space for lease "$29" ...`: BizQuest BW2472318 terms (NNN, 5+5 years, equipment in excellent condition, street parking); address not given.
5. `"High-Traffic Boston Cafe Opportunity" Flexible Concept ...`: listing still indexed; no new figures.
6. `"Davis Square" Somerville "Charming Cafe" for sale ...`: BizQuest $165,000, asset sale, lease only, $36/sq ft/yr.
7. `Lexington Center MA fast casual cafe for sale 1,550 square feet ...`: BizQuest BW2476956, $165,000, 12 seats, $6,563/month, shared parking.
8. `"361 Huron" Cambridge cafe OR bakery OR restaurant 2026`: nothing relevant.
9. `"1248 Cambridge" OR "1248-1260 Cambridge" Street Inman Square ...`: Godino & Co. listing of the former Wit's End bar and restaurant; no sale or closure news.
10. `"167 Massachusetts Ave" OR "167 Mass Ave" Boston former restaurant space for lease 2,900`: updated 2026-06-05; rent on request; GraffitoSP.
11. `"250 Huntington Ave" Boston restaurant for sale OR for lease Symphony ...`: sale MLS 73498139 at $20,000 (Apr 2026); earlier $10,000 (Feb 2025).
12. `Teaholic "912 Beacon" Boston OR "Gong Cha" "912 Beacon" ...`: Gong Cha opened about mid-2025; nothing on Teaholic.
13. `"Davis Square Somerville - Charming Cafe for Sale" $165,000 ...`: nothing new.
14. `"152 Liverpool" East Boston retail restaurant space ...`: still listed (May 2026 update); no tenant.
15. `Cambridge "1105 Mass" OR "former Beyond Full" OR "former Zoe's" ...`: no new tenant found.

## Sources

**City data**
- Food establishment inspections: https://data.boston.gov/dataset/food-establishment-inspections (API resource `4582bec6-2b4f-4f9e-bc55-cbaa73117f4c`)
- Licensing Board licences (Common Victualler): https://data.boston.gov/api/3/action/datastore_search?resource_id=04dc653b-1789-4374-9669-b07df7233344
- Active food establishment licences: https://data.boston.gov/api/3/action/datastore_search?resource_id=f1e13724-284d-478c-b8bc-ef042aa5b70b

**boston.com listings (read 2026-11-07)**
- 250 Huntington, lease: https://www.boston.com/listings/268-l-23502-73594131/rent/02115/
- 250 Huntington, sale: https://www.boston.com/listings/268-l-23502-73498139/buy/02115/
- 3089-3091 Washington: https://www.boston.com/listings/268-l-21001-73497894/rent/02119/
- 1211 Commonwealth: https://www.boston.com/listings/268-l-23461-73327918/rent/02134/
- 349 Centre, full: https://www.boston.com/listings/268-l-21945-73578246/rent/02130/
- 349 Centre, partial: https://www.boston.com/listings/268-l-21945-73578251/rent/02130/
- 2070 Centre: https://www.boston.com/listings/268-l-20610-73594011/rent/02132/
- 879-881 Blue Hill: https://www.boston.com/listings/268-l-6301-73489797/rent/02124/
- 748 Dudley: https://www.boston.com/listings/268-l-2736822-73469396/rent/02125/

**Boston Restaurant Talk**
- Beyond Full closed: https://bostonrestaurants.blogspot.com/2026/07/beyond-full-in-cambridges-harvard.html
- Sunrise Cafe Bagels and Diner opening: https://bostonrestaurants.blogspot.com/2026/09/sunrise-cafe-bagels-and-diner-to-open.html
- Fupo Cafe closed: https://bostonrestaurants.blogspot.com/2026/01/fupo-cafe-in-cambridges-huron-village.html
- Sumi House opened: https://bostonrestaurants.blogspot.com/2026/03/sumi-house-opens-in-former-fupo-cafe.html
- Turing Tavern closed (1281 Cambridge St): https://bostonrestaurants.blogspot.com/2025/12/the-turing-tavern-in-cambridges-inman.html

**News**
- Axios, The Draft shut down (2026-01-08): https://www.axios.com/local/boston/2026/01/08/the-draft-in-allston-shut-down-after-underage-drinking
- CBS Boston, The Draft: https://www.cbsnews.com/amp/boston/news/the-draft-allston-bar-shut-down-underage-drinking
- Boston Globe, Harvard Ave businesses leaving (2026-08-20): https://www.bostonglobe.com/2026/08/20/business/allston-harvard-ave-local-businesses-leaving/

**Listings seen through search snippets**
- 1105 Mass Ave:
  - https://loopnet.com/Listing/1105-Massachusetts-Ave-Cambridge-MA/33223782
  - https://raveis.com/prop/73291906/1105-massachusetts-cambridge-ma-02138
  - https://www.verani.com/ma-real-estate/cambridge/1105-massachusetts-mls-73291906
  - https://commercialcafe.com/commercial-property/us/ma/cambridge/1105-massachusetts-avenue
- 750 Dudley:
  - https://uphamscorner.org/commercial-vacancies (not reachable from this session)
  - https://www.commercialsearch.com/commercial-property/us/ma/boston/749-dudley-street
- 34 Harvard Ave: https://www.commercialcafe.com/commercial-property/us/ma/boston/34-harvard-ave/
- 167 Mass Ave:
  - https://www.commercialsearch.com/commercial-property/us/ma/boston/167-mass-ave/
  - https://www.cityfeet.com/cont/listing/167-massachusetts-ave-boston-ma-02115/cs40481371
- 912 Beacon: https://www.commercialcafe.com/commercial-property/us/ma/boston/912-beacon-st-1/
- 23 S Huntington: https://www.cbre.com/properties/properties-for-lease/retail/details/US-SMPL-192225/23-south-huntington-avenue-boston-ma-02130
- 152 Liverpool:
  - https://www.cbre.com/properties/properties-for-lease/retail/details/US-SMPL-71435/152-liverpool-street-boston-ma-02128
  - https://www.commercialcafe.com/commercial-property/us/ma/boston/152-liverpool-street/
- 250 Huntington, sale history:
  - https://bmnboston.com/property/250-huntington-ave-boston-ma-02115-for-sale-73498139
  - https://bmnboston.com/property/250-huntington-ave-boston-ma-02115-for-sale-73333901/
- Roslindale pizza shop:
  - https://images.bizquest.com/real-estate-for-lease/pizzeria-fast-casual-space-for-lease-roslindale/BW2472318
  - https://www.bizquest.com/food-and-beverage-real-estate-listings-in-massachusetts
- Boston cafe asset sale: https://images.bizquest.com/asset-sales/high-traffic-boston-cafe-opportunity-flexible-concept/BW2482986
- Davis Square cafe: https://www.bizquest.com/food-and-beverage-businesses-for-sale-in-somerville-ma/
- Lexington Center cafe: https://www.bizquest.com/business-for-sale/lexington-center-fast-casual-cafe-for-sale/BW2476956/
- 361 Huron: https://www.cityfeet.com/cont/listing/361-huron-ave-cambridge-ma-02138/cs40389671
- 1248-1260 Cambridge St:
  - https://www.showcase.com/1248-1260-cambridge-st-cambridge-ma-02139/34594831/
  - https://www.cityfeet.com/cont/listing/1248-1260-cambridge-st-cambridge-ma-02139/cs34594831
