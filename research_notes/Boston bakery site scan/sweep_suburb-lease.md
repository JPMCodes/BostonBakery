# Suburb and inner-square lease sweep (Cambridge, Somerville, Brookline, inner suburbs)

Scan date: November 7, 2026. Scope: commercial space for lease (plus businesses for sale and vacated food spaces seen along the way) in Cambridge, Somerville, Brookline and the inner-suburb town centers and lifestyle centers named in the site criteria. Target: 900-3,000 sq ft, ideally second-generation cafe, bakery or restaurant space, rent about $30-55/sq ft/yr.

Method and limits:

- 35 web searches (the cap), all listed in the query log below. LoopNet, Crexi, CityFeet, Showcase, Realmo, CommercialCafe, BizBuySell and BizQuest pages were not opened; their details come from search snippets and the search tool's summaries, which sometimes merge or misattribute listings. Every such row is marked `snippet_only`.
- Pages actually read (`page_read`): Boston.com MLS listing pages and Boston Restaurant Talk (BRT) posts, fetched with curl through the session proxy. WebFetch could not resolve www.boston.com, cambridgeday.com or bostonpads.com; the last two were not retried.
- Sizes, rents and prices are copied as stated. `-1` means not stated. Rent is normalized as monthly rent x 12 / sq ft only where both were given. NNN versus gross is noted where the source says.
- Most snippets carry no date. Rows marked `undated` or dated before May 2026 may be stale and need a broker check.

## Shortlist (best fits on the evidence seen)

| Rank | Kind | Site | Why it fits | Main gap |
|---|---|---|---|---|
| 1 | lease | 1191 Centre St, Newton Centre | 1,894 SF second-generation restaurant; combinable with 951 SF next door (2,845 SF); listing updated June 2026; municipal lots nearby | Rent not published |
| 2 | lease | 1326 Mass Ave (1310-1328), Arlington Heights | 1,412 SF second-generation restaurant "at the epicenter of the Square"; updated August 2026 | Rent not published; not turnkey |
| 3 | lease | 361 Huron Ave, Cambridge (Huron Village) | Listed as "2nd gen cafe space", 1,179-2,358 SF, NNN, BA-1 zoning; listed May 2026 | Rent not published; building also offered for sale |
| 4 | lease | 1385 Washington St, West Newton | 1,200 SF turnkey restaurant at $4,000/mo ($40/SF/yr) | Undated; may be confused with 1383 next door |
| 5 | lease | 173 Amory St, Brookline (BU area) | 1,510 SF second-generation restaurant/QSR, fully fitted for food service, NNN | Undated; rent not published; address (163 vs 173) to confirm |
| 6 | lease | 107R Union St, Newton Centre | Stand-alone restaurant building, hood already in place, new enclosed patio | Size and rent unknown |
| 7 | business_for_sale | Needham (address withheld, MLS 73519495) | Hood in place; 1,387 SF plus basement; about 8 years left on the lease; $5,900/mo base ($51.05/SF/yr) plus about $1,200/mo NNN | Asking price and financials not found |
| 8 | business_for_sale | Lexington Center fast-casual cafe | $165,000 for a brand-new cafe build-out; 1,550 SF at $6,563/mo ($50.81/SF/yr) | Financials only under NDA; lease term unknown |
| 9 | closed_space | 292 Concord Ave, Cambridge (former Nine Winters Bakery) | A bakery fitted out in 2025, closed March 29, 2026 (owner cited family reasons); no new tenant found | Not seen listed; size unknown |
| 10 | lease | 16-18 Eliot St, Harvard Square | 3,000 SF street level plus 1,143 SF lower-level kitchen; licensed for 84 seats | July 1, 2026 availability has passed; rent not published |

Close but weaker: 1248-1260 Cambridge St in Inman Square (turn-key, 2,372 SF, but $60/SF NNN); the Watertown "no key money" lease (3,250 SF closed bar with licenses at $36.92/SF base plus NNN, address withheld); 114-118 Broadway, Somerville ($36/SF plus NNN, turnkey, but 118 is 3,780 SF); 24 College Ave near Davis Square ($200,000 FF&E sale, only 600 SF on the ground floor); Cafe Barada's 2269 Mass Ave space, closing December 5, 2026.

Rents stated for food-capable space ran from $36 to $60/sq ft/yr: $36 plus NNN (118 Broadway), $36.92 plus NNN (Watertown lease), $38 (350 Pleasant St), $40 (1385 Washington St), $50.81 (Lexington cafe), $51.05 plus NNN (Needham), and $60 (1248 Cambridge St NNN; 24-28 High St, Medford).

No in-range availability was found at MarketStreet Lynnfield, Derby Street Shops in Hingham, Assembly Row itself (only adjacent Assembly Square listings), Kendall Square, Wollaston or North Quincy. Burlington, Winchester and Melrose produced only oversized, non-food or business-sale options.

## All candidates

Columns: size in sq ft; rent normalized to $/sq ft/yr; price is the asking price for business sales; `-1` = not stated. Rent as stated, prior use, second-generation evidence, crowd context and caveats for each row follow in "Candidate details".

| # | Kind | Title | Address | Town | Size | Rent $/sf/yr | Price | Date seen | Basis | URL |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | lease | 2nd-gen cafe space, Huron Village | 361 Huron Ave | Cambridge (West Cambridge / Huron Village) | 2,358 | -1 | -1 | 2026-05-04 (LoopNet market date); CommercialCafe updated 2026-05-12 | snippet_only | https://www.cityfeet.com/cont/listing/361-huron-ave-cambridge-ma-02138/cs40389671 |
| 2 | lease | Turn-key restaurant/bar, Inman Square | 1248-1260 Cambridge St | Cambridge (Inman Square) | 2,372 | 60 | -1 | undated | snippet_only | https://www.showcase.com/1248-1260-cambridge-st-cambridge-ma-02139/34594831/ |
| 3 | lease | Licensed 84-seat restaurant, Harvard Square | 16-18 Eliot St | Cambridge (Harvard Square) | 3,000 | -1 | -1 | 2026-04-03 (listing updated); available date 2026-07-01 | snippet_only | https://www.commercialcafe.com/commercial-property/us/ma/cambridge/18-eliot-street/ |
| 4 | lease | Small ex-restaurant/cafe unit, Harvard Square | 1430 Massachusetts Ave | Cambridge (Harvard Square) | 850 | -1 | -1 | undated | snippet_only | https://www.cityfeet.com/cont/listing/1430-massachusetts-ave-cambridge-ma-02138/cs27866897 |
| 5 | lease | Corner retail with new systems, Mass Ave at Hudson St | 1674 Massachusetts Ave | Cambridge (between Harvard and Porter Squares) | 2,464 | -1 | -1 | undated | snippet_only | https://www.commercialsearch.com/commercial-property/us/ma/cambridge/1674-massachusetts-avenue/ |
| 6 | lease | Column-free retail/flex, Porter Square | 1847-1855 Massachusetts Ave | Cambridge (Porter Square / North Cambridge) | 3,000 | -1 | -1 | undated | snippet_only | https://www.raveis.com/prop/73369850/1847-1855-massachusetts-cambridge-ma-02140 |
| 7 | lease | Corner space at Cambridge and Columbia Sts | 1036 Cambridge St | Cambridge (between Inman Square and East Cambridge) | 2,364 | -1 | -1 | undated | snippet_only | https://www.cityfeet.com/cont/listing/1036-cambridge-st-cambridge-ma-02141/cs37546663 |
| 8 | lease | Former S&S Restaurant, Inman Square (oversized) | 1334 Cambridge St | Cambridge (Inman Square) | 9,000 | -1 | -1 | undated | snippet_only | https://www.crexi.com/lease/properties/1243485/massachusetts-1334-cambridge-street |
| 9 | lease | Former Whole Heart Provisions space near Central Square | 300 Massachusetts Ave (per search summary) | Cambridge (Central Square / University Park) | -1 | -1 | -1 | undated (article likely several years old) | snippet_only | https://www.cambridgeday.com/?p=97299 |
| 10 | lease | Restaurant space near Lechmere | 293 Cambridge St | Cambridge (East Cambridge) | 3,171 | -1 | -1 | undated | snippet_only | https://www.commercialcafe.com/commercial-property/us/ma/cambridge/urban-retail-restaurant-space/ |
| 11 | lease | Restaurant/entertainment-zoned space, Central Square | 296 Green St | Cambridge (Central Square) | -1 | 18 | -1 | undated | snippet_only | https://realmo.com/bars/for-lease/ma/cambridge/ |
| 12 | lease | Turnkey 2nd-gen restaurant, 114-118 Broadway | 114-118 Broadway | Somerville (Broadway, East Somerville) | 3,780 | 36 | -1 | undated | snippet_only | https://www.bizquest.com/real-estate-for-lease/114-118-broadway-for-lease-somerville/BW2372507/ |
| 13 | lease | Retail/restaurant storefront, Holland St | 51 Holland St | Somerville (Holland St between Davis and Teele Squares) | 1,840 | -1 | -1 | 2026-05 (listing updated May 2026) | snippet_only | https://www.crexi.com/lease/properties/1038602/massachusetts-51-holland-st-somerville |
| 14 | lease | 'Prime Somerville Cafe Opportunity', Columbia St | 495 Columbia St | Somerville (02143) | 1,021 | -1 | -1 | undated | snippet_only | https://bostonpads.com/massachusetts-real-estate-investment/somerville-73294361 |
| 15 | lease | Small commercial space, Union Square | 257 Washington St | Somerville (Union Square) | -1 | -1 | -1 | undated | snippet_only | https://bmnboston.com/property/257-washington-st-somerville-ma-02143-for-rent-73468662 |
| 16 | lease | Restaurant-designated space, Assembly Square | 74 Middlesex Ave | Somerville (Assembly Square) | 2,600 | -1 | -1 | undated (a 2024 listing also noted) | snippet_only | https://commercialsearch.com/commercial-property/us/ma/somerville/74-middlesex-ave |
| 17 | lease | Retail/restaurant corner at Elm St and Bowers Ave (oversized) | 212 Elm St | Somerville (Davis Square) | 5,469 | -1 | -1 | undated | snippet_only | https://www.crexi.com/lease/properties/1105996/massachusetts-212-elm-street |
| 18 | lease | Former restaurant with kitchen, short-term only (oversized) | 96 Middlesex Ave | Somerville (Assembly Square area) | 8,607 | -1 | -1 | undated | snippet_only | https://www.crexi.com/lease/properties/919742/massachusetts-96-middlesex-avenue-somerville-ma |
| 19 | lease | New restaurant space at VERGE, Medford St | 16-20 Medford St | Somerville | 3,360 | -1 | -1 | undated (delivery Q3 2025) | snippet_only | https://issuu.com/corbett-brands/docs/updated_verge_brochure_5.16 |
| 20 | lease | Built-out restaurant/QSR unit near BU | 173 Amory St | Brookline (near Boston University, 02446) | 1,510 | -1 | -1 | undated | snippet_only | https://www.cityfeet.com/cont/listing/173-amory-st-brookline-ma-02446/cs38305265 |
| 21 | lease | Former restaurant, Pelham Hall lower level | 1284 Beacon St (lower level, Pelham Hall) | Brookline (Coolidge Corner) | -1 | -1 | -1 | undated | snippet_only | https://www.cityfeet.com/cont/listing/1284-beacon-st-brookline-ma-02446/cs22350060 |
| 22 | lease | Street retail on a food block, Washington Square | 1630 Beacon St | Brookline (Washington Square) | 2,008 | -1 | -1 | 2026-03-30 (listing updated) | snippet_only | https://www.propertyshark.com/cre/commercial-property/us/ma/brookline/1630-beacon-street/ |
| 23 | lease | Newly vacant retail suite, Brookline Village | 60-62 Harvard St #1B (also #1A) | Brookline (Brookline Village) | -1 | 38 | -1 | 2025-09 (start date; 168 days on market) | snippet_only | https://bmnboston.com/property/60-62-harvard-brookline-ma-02445-for-rent-73428041 |
| 24 | lease | Tiny restaurant unit, Cypress St | 6-12 Cypress St | Brookline (Brookline Village) | 600 | 64 | -1 | undated | snippet_only | https://www.cityfeet.com/cont/listing/6-12-cypress-st-brookline-ma-02445/cs28763974 |
| 25 | lease | 2nd-gen 257-seat restaurant, Coolidge Corner (oversized) | 1280 Beacon St (1278-1290 Beacon St) | Brookline (Coolidge Corner) | 9,175 | -1 | -1 | 2026-03 (brochure revised March 2026; available Q1 2026) | snippet_only | https://www.commercialcafe.com/commercial-property/us/ma/brookline/1278-1290-beacon-street/ |
| 26 | lease | Restaurant with full liquor license, Washington Square (oversized) | 1627 Beacon St | Brookline (Washington Square) | 5,000 | -1 | -1 | undated | snippet_only | https://loopnet.com/Listing/1627-Beacon-St-Brookline-MA/33542828 |
| 27 | lease | Route 9 restaurant with parking (oversized) | 1180 Boylston St | Brookline (Route 9) | 6,834 | -1 | -1 | undated | snippet_only | https://www.commercialsearch.com/commercial-property/us/ma/brookline/1180-boylston-street/ |
| 28 | lease | 2nd-gen restaurant plus adjacent retail, Newton Centre | 1191 Centre St (1185-1197 Centre St) | Newton (Newton Centre) | 1,894 | -1 | -1 | 2026-06 (listing updated June 2026) | snippet_only | https://www.cbre.com/properties/properties-for-lease/retail/details/US-SMPL-167115/1191-centre-street-1191-centre-street-newton-ma-02459 |
| 29 | lease | 1,200 SF turnkey restaurant, West Newton | 1385 Washington St | Newton (West Newton) | 1,200 | 40 | -1 | undated | snippet_only | https://www.raveis.com/prop/73445933/1385-washington-st-newton-ma-02465 |
| 30 | lease | Retail/office storefront, West Newton | 1383 Washington St | Newton (West Newton) | 1,200 | 30 | -1 | undated | snippet_only | https://www.loopnet.ca/Listing/1383-Washington-St-Newton-MA/38172669 |
| 31 | lease | Stand-alone restaurant building with hood, Newton Centre | 107R Union St | Newton (Newton Centre) | -1 | -1 | -1 | undated | snippet_only | https://elliman.com/listing/107r-union-st-newton-ma-02459/13200260 |
| 32 | lease | Former pizza restaurant, Four Corners | 1158 Beacon St | Newton (Four Corners) | 2,608 | -1 | -1 | undated | snippet_only | https://realmo.com/listing/12479274 |
| 33 | lease | 2nd-gen restaurant (3,400 SF), Newton Corner | 275 Washington St | Newton (Newton Corner) | 3,400 | -1 | -1 | undated | snippet_only | https://www.commercialcafe.com/commercial-property/us/ma/newton/275-washington-street/ |
| 34 | lease | Restaurant/retail on the Needham St corridor (oversized) | 141-165 Needham St | Newton (Newton Upper Falls) | 4,600 | -1 | -1 | undated | snippet_only | https://commercialsearch.com/commercial-property/us/ma/newton/141-needham-street |
| 35 | lease | Retail with restaurant use, Newtonville | 835-855 Washington St | Newton (Newtonville) | -1 | -1 | -1 | undated | snippet_only | https://www.commercialsearch.com/commercial-property/us/ma/newton/835-855-washington-street/ |
| 36 | lease | Closed tapas/whiskey bar lease, no key money | Address withheld | Watertown | 3,250 | 36.92 | -1 | undated | snippet_only | https://www.bizquest.com/real-estate-for-lease/restaurant-lease-in-watertown-no-key-money/BW2399964/ |
| 37 | lease | The Maximilian, restaurant-ready unit, Watertown Square | 104-108 Main St | Watertown (Watertown Square) | 3,041 | -1 | -1 | 2026-06-01 (date in the flyer file name) | snippet_only | https://images.loopnet.ca/d2/8WgzErcj_HTGItBbl8wAqyEf8USj4jzk5Qpvy05Y02I/20260601104106MainSt%201.pdf |
| 38 | lease | WaterMills ground-floor restaurant space | 350 Pleasant St | Watertown | 3,780 | 38 | -1 | undated (recent LoopNet ID) | snippet_only | https://www.loopnet.com/Listing/350-Pleasant-St-Watertown-MA/41818524/ |
| 39 | lease | 1,412 SF 2nd-gen restaurant, Arlington Heights | 1326 Massachusetts Ave (1310-1328 Massachusetts Ave) | Arlington (Arlington Heights) | 1,412 | -1 | -1 | 2026-08 (listing updated August 2026) | snippet_only | https://www.commercialcafe.com/commercial-property/us/ma/arlington/1310-1328-massachusetts-ave/ |
| 40 | lease | Retail in the new Majestic Mill Brook building | 1025 Massachusetts Ave | Arlington | 1,732 | 38 | -1 | 2025-12 (Realmo page last updated December 2025) | snippet_only | https://realmo.com/coffee-shops/for-lease/ma/middlesex-county |
| 41 | lease | Retail/office storefront near Arlington Center | 713-725 Massachusetts Ave | Arlington (near Arlington Center) | 2,015 | 38 | -1 | undated | snippet_only | https://www.commercialsearch.com/commercial-property/us/ma/arlington/713-725-massachusetts-ave |
| 42 | lease | Former Starbucks cafe near Tufts (likely leased) | 177 College Ave (Joyce Cummings Center) | Medford (Tufts University) | 1,300 | -1 | -1 | 2026-04-16 (listing updated) | snippet_only | https://www.commercialcafe.com/commercial-property/us/ma/medford/177-college-ave/ |
| 43 | lease | Small cafe/smoothie storefront, Medford Square | 24-28 High St | Medford (Medford Square) | 688 | 60 | -1 | undated | snippet_only | https://www.cityfeet.com/cont/listing/24-28-high-st-medford-ma-02155/cs39242139 |
| 44 | lease | Shell restaurant space near Tufts (oversized) | 402 Boston Ave | Medford (Tufts / Medford Hillside) | 3,850 | -1 | -1 | 2026-04-16 (listing updated) | snippet_only | https://www.propertyshark.com/cre/commercial-property/us/ma/medford/402-boston-ave/ |
| 45 | lease | New cafe space listed on Realmo, Riverside Ave | 34 Riverside Ave | Medford (Medford Square) | -1 | -1 | -1 | 2025-12 (Realmo page last updated December 2025) | snippet_only | https://realmo.com/coffee-shops/for-lease/ma/middlesex-county |
| 46 | lease | Storefront with restaurant use, Belmont St | 285 Belmont St | Belmont (listed under Cushing Square) | 2,537 | -1 | -1 | undated | snippet_only | https://www.cityfeet.com/cont/listing/285-285-belmont-st-belmont-ma-02478/cs34951019 |
| 47 | lease | 1,300 SF restaurant, Waverley Square (likely stale) | 687 Belmont St | Belmont (Waverley Square) | 1,300 | 23.08 | -1 | undated | snippet_only | https://www.cityfeet.com/cont/listing/687-belmont-st-belmont-ma-02478/cs35758858 |
| 48 | lease | Free-standing former bank, Cushing Square | 63 Trapelo Rd | Belmont (Cushing Square) | 3,000 | -1 | -1 | undated | snippet_only | https://raveis.com/prop/73270354/63-trapelo-rd-belmont-ma-02478 |
| 49 | lease | Wellesley Square street retail (cafe or restaurant allowed) | 34 & 48-50 Central St | Wellesley (Wellesley Square) | -1 | -1 | -1 | undated | snippet_only | https://www.commercialsearch.com/commercial-property/us/ma/wellesley/34-48-50-central-st/ |
| 50 | lease | Central Plaza retail spaces, Wellesley Square | 74 Central St (Central Plaza) | Wellesley (Wellesley Square) | -1 | -1 | -1 | undated | snippet_only | https://www.commercialsearch.com/commercial-property/us/ma/wellesley/central-plaza/ |
| 51 | lease | Lower-level specialty space, downtown Needham | 990-992 Great Plain Ave | Needham (Needham Center) | 4,282 | -1 | -1 | undated | snippet_only | https://www.commercialsearch.com/commercial-property/us/ma/needham/990-992-great-plain-avenue-1/ |
| 52 | lease | 2nd-gen restaurant in the Giroux Building, Lexington Center | 1833 Massachusetts Ave (The Giroux Building) | Lexington (Lexington Center) | -1 | -1 | -1 | undated | snippet_only | https://www.commercialsearch.com/commercial-property/us/ma/lexington/the-giroux-building |
| 53 | lease | Former restaurant (4,560 SF), Lexington Center | 27 Waltham St | Lexington (Lexington Center) | 4,560 | -1 | -1 | undated | snippet_only | https://raveis.com/prop/73239309/27-waltham-st-lexington-ma-02421 |
| 54 | lease | Retail/office space, historic Lexington Center | 1844 Massachusetts Ave | Lexington (Lexington Center) | -1 | -1 | -1 | undated | snippet_only | https://www.raveis.com/property/flyer/20908101 |
| 55 | lease | 2nd-gen restaurant space, Quincy Center (oversized) | 1495 Hancock St | Quincy (Quincy Center) | 5,350 | -1 | -1 | 2026-06 (updated June 2026; first listed June 2025) | snippet_only | https://www.cityfeet.com/cont/listing/1495-hancock-st-quincy-ma-02169/cs36094790 |
| 56 | lease | Vacant standalone commercial building, Brooks Ave | 16 Brooks Ave | Quincy (02169) | 2,090 | 20.10 | -1 | 2026-09-03 (date added); Available on 2026-11-07 | page_read | https://www.boston.com/listings/268-l-3208-73396618/buy/02169 |
| 57 | lease | Pad at the Legacy Place entrance (oversized) | 850 Providence Hwy | Dedham (Legacy Place entrance) | 6,600 | -1 | -1 | undated | snippet_only | https://www.commercialcafe.com/commercial-property/us/ma/dedham/850-providence-hwy/ |
| 58 | lease | Space at Legacy Place (Avison Young) | 770 Legacy Place | Dedham (Legacy Place) | -1 | -1 | -1 | undated | snippet_only | https://avisonyoung.us/properties/770-legacy-place-dedham-lease |
| 59 | lease | End-cap needing renovation, Main St | 881-889 Main St | Winchester | -1 | -1 | -1 | 2026-05-27 (listing posted) | snippet_only | https://www.loopnet.ca/Listing/881-889-Main-St-Winchester-MA/40672088/ |
| 60 | lease | Office/retail storefront, Winchester Center | 535 Main St | Winchester (Winchester Center) | -1 | -1 | -1 | 2026-01-01 (availability date) | snippet_only | https://www.loopnet.ca/Listing/535-Main-St-Winchester-MA/38456117 |
| 61 | lease | Multi-use space pitched for a bakery (town withheld) | Address withheld | Arlington, Belmont, Watertown, Waltham or Newton (withheld) | -1 | -1 | -1 | undated | snippet_only | https://bizquest.com/real-estate-for-lease/multiple-use-space-for-lease-in-densely-populated-and-high-traffic-area/BW2358503 |
| 62 | business_for_sale | Built-out QSR steps from Davis Square, FF&E sale | 24 College Ave | Somerville (Davis Square) | 600 | 60 | $200,000 | 2026-08-29 (date added); 70 days on market, Available on 2026-11-07 | page_read | https://www.boston.com/listings/268-l-23473-73569759/buy/02144 |
| 63 | business_for_sale | Established restaurant near the Red Line, Quincy | Address withheld (listed as '9999 Copland St') | Quincy (02169) | 1,850 | -1 | $160,000 | 2026-08-31 (date added); 68 days on market, Available on 2026-11-07 | page_read | https://www.boston.com/listings/268-l-18485-73570259/buy/02169 |
| 64 | business_for_sale | Breakfast/lunch restaurant with building, Broadway near Ball Square | 704 Broadway | Somerville (02144) | -1 | -1 | $2,150,000 | 2026-09-03 (date added); 65 days on market, Available on 2026-11-07 | page_read | https://www.boston.com/listings/268-l-21854-73502637/buy/02144 |
| 65 | business_for_sale | Free-standing restaurant building with FF&E by Watertown Mall | 71-73 Elm St | Watertown | -1 | -1 | $635,000 | 2026-10-07 (date added); 31 days on market, Available on 2026-11-07 | page_read | https://www.boston.com/listings/268-l-1398-73580699/buy/02472 |
| 66 | business_for_sale | Fast-casual cafe, Lexington Center | Lexington Center (street address not stated) | Lexington (Lexington Center) | 1,550 | 50.81 | $165,000 | undated | snippet_only | https://www.bizquest.com/business-for-sale/lexington-center-fast-casual-cafe-for-sale/BW2476956/ |
| 67 | business_for_sale | Restaurant business with hood, Needham (address withheld) | Address withheld ('000 Confidential', Needham 02492) | Needham | 1,387 | 51.05 | -1 | undated | snippet_only | https://www.raveis.com/prop/73519495/000-confidential-needham-ma-02492 |
| 68 | business_for_sale | Turnkey cafe, Central Square | Central Square (street address not stated) | Cambridge (Central Square) | -1 | -1 | $200,000 | undated | snippet_only | https://www.bizbuysell.com/massachusetts/coffee-shops-and-cafes-for-sale/ |
| 69 | business_for_sale | Boba cafe near BU, Brookline | Near Boston University (street address not stated) | Brookline | -1 | -1 | $1,200,000 | undated | snippet_only | https://www.bizbuysell.com/massachusetts/coffee-shops-and-cafes-for-sale/ |
| 70 | business_for_sale | Boba and coffee shop, Newton Centre | 212 Sumner St | Newton (Newton Centre) | -1 | -1 | -1 | 2025-12 (Realmo page last updated December 2025) | snippet_only | https://realmo.com/coffee-shops/for-lease/ma/middlesex-county |
| 71 | business_for_sale | Restaurant with patio, Assembly Row | Assembly Row (street address not stated) | Somerville (Assembly Row) | 1,500 | -1 | -1 | undated | snippet_only | https://www.bizbuysell.com/business-opportunity/somerville-ma-assembly-row-1st-class-restaurant-space/2519320/ |
| 72 | business_for_sale | Turnkey restaurant business, Teele Square | 1148 Broadway | Somerville (Teele Square) | -1 | -1 | -1 | undated | snippet_only | https://commercialpropertiesforsale.c21.com/property/1148-broadway-street-somerville-ma-02144-C2183125899 |
| 73 | business_for_sale | Italian pizzeria with 7 years of lease, Melrose | Melrose (street address not stated) | Melrose | 350 | -1 | $100,000 | undated | snippet_only | https://www.bizbuysell.com/massachusetts/melrose/american-restaurants-for-sale |
| 74 | business_for_sale | Full-service restaurant with 40-seat bar, Burlington | Burlington (street address not stated) | Burlington | -1 | -1 | -1 | undated | snippet_only | https://www.bizquest.com/business-for-sale/burlington-restaurant-with-40-seat-bar/BW2428070/ |
| 75 | business_for_sale | Restaurant with two hoods, Watertown | Watertown (street address not stated) | Watertown | -1 | -1 | -1 | undated | snippet_only | https://images.bizquest.com/business-for-sale/watertown-restaurant-with-two-hoods-for-sale/BW2416108 |
| 76 | closed_space | Closed bakery (Nine Winters), West Cambridge | 292 Concord Ave | Cambridge (West Cambridge) | -1 | -1 | -1 | 2026-03-18 (post) | mixed | https://bostonrestaurants.blogspot.com/2026/03/nine-winters-bakery-in-cambridge-is.html |
| 77 | closed_space | Cafe Barada closing, North Cambridge | 2269 Massachusetts Ave | Cambridge (North Cambridge) | -1 | -1 | -1 | 2026-10-29 (post); closing 2026-12-05 | page_read | https://bostonrestaurants.blogspot.com/2026/10/cafe-barada-in-north-cambridge-is.html |
| 78 | closed_space | Closed coffee shop (Lola's), West Medford | 17 Playstead Rd | Medford (West Medford) | -1 | -1 | -1 | 2026-04-08 (post) | page_read | https://bostonrestaurants.blogspot.com/2026/04/lolas-coffee-and-more-in-west-medford.html |
| 79 | closed_space | Closed Comella's, Melrose Main St | 478A Main St | Melrose | -1 | -1 | -1 | 2026-03-25 (post) | page_read | https://bostonrestaurants.blogspot.com/2026/03/comellas-in-melrose-has-closed.html |
| 80 | closed_space | Closed Melty, Washington St, Dedham | 290 Washington St | Dedham | -1 | -1 | -1 | 2026-03-19 (post) | page_read | https://bostonrestaurants.blogspot.com/2026/03/melty-in-dedham-has-closed.html |
| 81 | closed_space | Closed Abbott's Frozen Custard, Lexington Center | 1853 Massachusetts Ave | Lexington (Lexington Center) | -1 | -1 | -1 | 2026-08-10 (post) | page_read | https://bostonrestaurants.blogspot.com/2026/08/abbotts-frozen-custard-in-lexington-has.html |
| 82 | closed_space | Closed Shine's Fresh Asian, Belmont Center | 30 Leonard St | Belmont (Belmont Center) | -1 | -1 | -1 | 2025-11-19 (post) | page_read | https://bostonrestaurants.blogspot.com/2025/11/shines-fresh-asian-in-belmont-center.html |
| 83 | closed_space | Closed Thai Amarin, Newton Corner | 287 Centre St | Newton (Newton Corner) | -1 | -1 | -1 | 2026-07-07 (post) | page_read | https://bostonrestaurants.blogspot.com/2026/07/thai-amarin-in-newton-corner-has-closed.html |
| 84 | closed_space | Closed Kostas Pizza & Seafood, Chestnut St | 315 Chestnut St | Needham | -1 | -1 | -1 | 2026-06-01 (post) | page_read | https://bostonrestaurants.blogspot.com/2026/06/kostas-pizza-seafood-in-needham-has.html |
| 85 | closed_space | Closed Mochiko Hawaiian, Newtonville | Newtonville (street address not stated in source) | Newton (Newtonville) | -1 | -1 | -1 | 2026-10-02 (post) | page_read | https://bostonrestaurants.blogspot.com/2026/10/mochiko-hawaiian-in-newtonville-and.html |
| 86 | closed_space | Closed Golden Temple, Washington Square (large) | 1651 Beacon St | Brookline (Washington Square) | -1 | -1 | -1 | 2026-06-28 (post) | page_read | https://bostonrestaurants.blogspot.com/2026/06/golden-temple-in-brookline-has-closed.html |
| 87 | closed_space | Closed Yas Chicken (ex-Qdoba), Middlesex Turnpike | 90 Middlesex Turnpike | Burlington | -1 | -1 | -1 | 2026-07-08 (post) | page_read | https://bostonrestaurants.blogspot.com/2026/07/yas-chicken-in-burlington-has-closed.html |
| 88 | closed_space | Closed Temazcal and Jack's Coal Fired Pizza, Burlington | 2 Wall St | Burlington | -1 | -1 | -1 | 2026-11-03 (post) | page_read | https://bostonrestaurants.blogspot.com/2026/11/temazcal-tequila-cantina-jacks-coal.html |

## Candidate details

1. **2nd-gen cafe space, Huron Village** (lease), 361 Huron Ave, Cambridge (West Cambridge / Huron Village).
   - Rent as stated: Rate upon request; NNN (CommercialCafe); quoted rate excludes utilities, property expenses and building services (LoopNet).
   - Prior use: Cafe (listing: '2nd gen cafe space'). Second-generation evidence: LoopNet: '2nd gen cafe space available for lease on Huron Ave'; hood and grease trap not stated.
   - Crowd context: Huron Village neighborhood strip in West Cambridge; source names no crowd generator. Source: LoopNet / CityFeet / CommercialCafe / Showcase (search snippets).
   - Notes: First-floor suite divisible 1,179-2,358 SF; zoning BA-1; building built 1916; renewal options; 'available immediately' on one site. A separate Showcase listing (40045442) offers 361 Huron Ave as a storefront FOR SALE. About 6 months old: confirm availability.
2. **Turn-key restaurant/bar, Inman Square** (lease), 1248-1260 Cambridge St, Cambridge (Inman Square).
   - Rent as stated: $60.00/SF/yr NNN ($11,860/mo on CityFeet).
   - Prior use: Bar/restaurant (seats 99 diners plus bar; 40 draft lines). Second-generation evidence: Marketed as turn-key restaurant; FF&E available for sale; hood and grease trap not stated.
   - Crowd context: Inman Square; source names no crowd generator. Source: Showcase / CityFeet / LoopNet (search snippets).
   - Notes: Available now; 5-year lease term. Base rent alone is above the $30-55 target, before NNN. Building 4,744 SF, built 1876. A separate LoopNet listing (40541948) markets 1248-1260 Cambridge St as a 'redevelopment or owner-user opportunity', so the building may be sold. One summary tied it to a '323 Prospect St, formerly Wit's End' listing; not confirmed.
3. **Licensed 84-seat restaurant, Harvard Square** (lease), 16-18 Eliot St, Cambridge (Harvard Square).
   - Rent as stated: Contact for pricing.
   - Prior use: Restaurant (existing restaurant licensed for 84 seats). Second-generation evidence: Existing restaurant licensed for 84 seats; 1,143 SF lower level for kitchen and back-of-house.
   - Crowd context: Harvard Square; source names no crowd generator. Source: CommercialCafe / CommercialSearch / PropertyShark / LoopNet (search snippets); broker Conviser Property Group.
   - Notes: 3,000 SF street level plus 1,143 SF lower level (4,143 SF total). The July 1, 2026 available date has passed, so it may be leased. Building size given as 4,350 or 4,496 SF by different sites.
4. **Small ex-restaurant/cafe unit, Harvard Square** (lease), 1430 Massachusetts Ave, Cambridge (Harvard Square).
   - Rent as stated: Rate upon request; lease term negotiable.
   - Prior use: Previously fitted out as a restaurant or cafe (search summary); another snippet says built out as standard retail. Second-generation evidence: Conflicting: 'previously fitted-out restaurant or cafe space' vs 'built out as standard retail'; no hood stated.
   - Crowd context: Harvard Square; source names no crowd generator. Source: CityFeet (search snippet).
   - Notes: 850 SF first-floor suite, just under the 900 SF minimum; available now. Older listing ID (27866897), so possibly stale.
5. **Corner retail with new systems, Mass Ave at Hudson St** (lease), 1674 Massachusetts Ave, Cambridge (between Harvard and Porter Squares).
   - Rent as stated: not stated.
   - Prior use: not stated. Second-generation evidence: none stated (new mechanical systems and storefront glass/entry).
   - Crowd context: Mass Ave between Harvard and Porter Squares. Source: CommercialSearch / CommercialCafe (search snippet).
   - Notes: About 2,464 SF corner plus 2,200 SF basement; available now. Not a food space: needs hood, grease trap and permits.
6. **Column-free retail/flex, Porter Square** (lease), 1847-1855 Massachusetts Ave, Cambridge (Porter Square / North Cambridge).
   - Rent as stated: not stated.
   - Prior use: not stated. Second-generation evidence: none stated; zoning said to allow food and beverage use.
   - Crowd context: Porter Square area; 40 ft of glass frontage. Source: Raveis (MLS 73369850) (search snippet).
   - Notes: About 3,000 SF column-free retail/flex; zoning welcomes retail, food and beverage, medical and gallery uses. Full build-out likely.
7. **Corner space at Cambridge and Columbia Sts** (lease), 1036 Cambridge St, Cambridge (between Inman Square and East Cambridge).
   - Rent as stated: Contact for pricing.
   - Prior use: not stated. Second-generation evidence: none stated.
   - Crowd context: Corner of Cambridge and Columbia Streets. Source: CityFeet (search snippet).
   - Notes: Available now per snippet. Prior use and food infrastructure unknown.
8. **Former S&S Restaurant, Inman Square (oversized)** (lease), 1334 Cambridge St, Cambridge (Inman Square).
   - Rent as stated: Not disclosed.
   - Prior use: Restaurant (S&S Restaurant; offered for the first time in over 100 years). Second-generation evidence: Described as fully second-generation restaurant (former S&S).
   - Crowd context: Inman Square. Source: Crexi / CommercialCafe (search snippets).
   - Notes: 9,000 SF street level plus 7,000 SF basement: three times the 3,000 SF ceiling unless subdivided. Partial match only.
9. **Former Whole Heart Provisions space near Central Square** (lease), 300 Massachusetts Ave (per search summary), Cambridge (Central Square / University Park).
   - Rent as stated: not stated.
   - Prior use: Restaurant (Whole Heart Provisions, per Cambridge Day photo caption). Second-generation evidence: Advertised as second-generation restaurant space (search summary); Graffito SP listing.
   - Crowd context: Near the Takeda entry at University Park (office/lab campus), edge of Central Square. Source: Cambridge Day photo caption in search results (site not fetchable) plus search summary.
   - Notes: Could not open Cambridge Day (host blocked). The 300 Mass Ave address comes from the search summary. Office/lab-adjacent, which the criteria disfavor. Treat as stale until checked.
10. **Restaurant space near Lechmere** (lease), 293 Cambridge St, Cambridge (East Cambridge).
   - Rent as stated: Pricing on request.
   - Prior use: not stated (listed as restaurant space). Second-generation evidence: Listed as restaurant space; no equipment stated.
   - Crowd context: Close to Lechmere T station. Source: Search summary of CommercialCafe/CommercialSearch results.
   - Notes: URL attribution uncertain: the summary gave the address without tying it to a result; this 'Urban Retail/Restaurant Space' listing is the likeliest match. Immediate availability per summary; slightly above 3,000 SF.
11. **Restaurant/entertainment-zoned space, Central Square** (lease), 296 Green St, Cambridge (Central Square).
   - Rent as stated: $18/SF/yr (NNN or gross not stated).
   - Prior use: not stated; zoned restaurant/entertainment (night club, lounge, theatre). Second-generation evidence: none stated beyond restaurant/entertainment zoning.
   - Crowd context: Central Square. Source: Realmo (search snippet).
   - Notes: URL is the Realmo Cambridge bars page the summary most likely drew on (attribution uncertain). The low rent suggests a lower-level or nightlife space; size and availability not stated.
12. **Turnkey 2nd-gen restaurant, 114-118 Broadway** (lease), 114-118 Broadway, Somerville (Broadway, East Somerville).
   - Rent as stated: $36/SF/yr plus NNN ($3.00/SF/mo).
   - Prior use: Restaurant with full kitchen and bar (listed in BizBuySell's brewery real-estate category). Second-generation evidence: Turnkey second-generation restaurant space with full kitchen, bar and outdoor seating potential.
   - Crowd context: not stated. Source: BizQuest / BizBuySell 'Lease Only' (search snippets); LoopNet property record.
   - Notes: 118 Broadway is 3,780 SF plus basement, seating 180 inside and 24 outside (above the ceiling). The 114 Broadway portion is 2,697 SF (range 2,697-6,477 SF); whether it has kitchen infrastructure is not stated. 5-year lease plus two 5-year options. BizQuest ID suggests a 2025 listing: confirm still available.
13. **Retail/restaurant storefront, Holland St** (lease), 51 Holland St, Somerville (Holland St between Davis and Teele Squares).
   - Rent as stated: Contact for pricing.
   - Prior use: not stated (restaurant listed as an additional use). Second-generation evidence: none stated; restaurant is a marketed use.
   - Crowd context: Summaries place it near Davis Square and Teele Square. Source: Crexi / CommercialCafe / CommercialSearch (search snippets).
   - Notes: Available immediately; renewal option. Crave Cafe was reported moving into the former Renee's Cafe on Holland St (a different storefront).
14. **'Prime Somerville Cafe Opportunity', Columbia St** (lease), 495 Columbia St, Somerville (02143).
   - Rent as stated: not stated.
   - Prior use: not stated (marketed as a cafe opportunity). Second-generation evidence: none stated.
   - Crowd context: not stated. Source: Boston Pads MLS mirror (search summary).
   - Notes: URL attribution uncertain: the summary named the listing without tying it to a result; this Boston Pads page (MLS 73294361) is the likeliest (the other Boston Pads Somerville result, 73468662, is 257 Washington St). bostonpads.com could not be opened. May be a business sale rather than a lease.
15. **Small commercial space, Union Square** (lease), 257 Washington St, Somerville (Union Square).
   - Rent as stated: $1,500/mo (size not stated).
   - Prior use: not stated (commercial space). Second-generation evidence: none stated.
   - Crowd context: Union Square; nearby cafes Bloc and Fortissimo Coffeehouse (per summary). Source: BMN Boston / Boston Pads (MLS 73468662) (search snippets).
   - Notes: At $1,500/mo probably far below 900 SF; not described as a food space.
16. **Restaurant-designated space, Assembly Square** (lease), 74 Middlesex Ave, Somerville (Assembly Square).
   - Rent as stated: Available upon request.
   - Prior use: not stated (restaurant-designated). Second-generation evidence: none stated.
   - Crowd context: Assembly Square, next to the Assembly Row lifestyle center. Source: CommercialSearch (search snippet).
   - Notes: A '65 Mystic Ave' 2,600 SF restaurant opportunity in the same summary may be the same space. Possibly stale (2024 reference).
17. **Retail/restaurant corner at Elm St and Bowers Ave (oversized)** (lease), 212 Elm St, Somerville (Davis Square).
   - Rent as stated: not stated.
   - Prior use: not stated. Second-generation evidence: none stated.
   - Crowd context: Davis Square area; Ball Square listed as a nearby point of interest. Source: Crexi / CommercialCafe (search snippet).
   - Notes: Above the 3,000 SF ceiling; partial match only.
18. **Former restaurant with kitchen, short-term only (oversized)** (lease), 96 Middlesex Ave, Somerville (Assembly Square area).
   - Rent as stated: not stated.
   - Prior use: Restaurant. Second-generation evidence: Former restaurant space with a kitchen.
   - Crowd context: Assembly Square area. Source: Crexi (search snippet).
   - Notes: Short-term lease, 3 years maximum, and nearly three times the size ceiling: poor fit.
19. **New restaurant space at VERGE, Medford St** (lease), 16-20 Medford St, Somerville.
   - Rent as stated: not stated.
   - Prior use: New construction. Second-generation evidence: none (new build).
   - Crowd context: not stated. Source: VERGE leasing brochure on Issuu (search snippet).
   - Notes: Q3 2025 delivery date has passed; may be leased. Slightly above 3,000 SF; first-generation space.
20. **Built-out restaurant/QSR unit near BU** (lease), 173 Amory St, Brookline (near Boston University, 02446).
   - Rent as stated: Rate upon request; NNN; quoted rate excludes utilities, property expenses and building services.
   - Prior use: Restaurant / quick-service (relet). Second-generation evidence: Marketed as a second-generation restaurant or quick-service unit fully fitted out for food service.
   - Crowd context: Boston University area, high-traffic retail strip; building tenants include Boba Tea Company. Source: LoopNet / CityFeet (search snippets).
   - Notes: Available immediately; negotiable terms; relet by a prior tenant. One summary placed it in Coolidge Corner, but the listings say the BU area. A LoopNet property record shows 163 Amory St with the same 1,510 SF: confirm the address.
21. **Former restaurant, Pelham Hall lower level** (lease), 1284 Beacon St (lower level, Pelham Hall), Brookline (Coolidge Corner).
   - Rent as stated: NNN; terms negotiable.
   - Prior use: Restaurant. Second-generation evidence: Former restaurant space, built out for restaurants and cafes.
   - Crowd context: Coolidge Corner. Source: CityFeet / LoopNet (search snippets).
   - Notes: Lower level, so weak street visibility; size not stated. Old listing ID (22350060): possibly stale.
22. **Street retail on a food block, Washington Square** (lease), 1630 Beacon St, Brookline (Washington Square).
   - Rent as stated: Pricing on request.
   - Prior use: not stated. Second-generation evidence: none stated.
   - Crowd context: Washington Square; co-tenants Stoked Pizza, Barre3, Bartaco, Caffe Nero, Barcelona Wine Bar. Source: PropertyShark / CommercialSearch (search snippet).
   - Notes: Food-heavy block but the space is not described as food-ready. Golden Temple at 1651 Beacon St, nearby, closed in June 2026.
23. **Newly vacant retail suite, Brookline Village** (lease), 60-62 Harvard St #1B (also #1A), Brookline (Brookline Village).
   - Rent as stated: $38/SF (per listing).
   - Prior use: not stated (retail). Second-generation evidence: none stated.
   - Crowd context: 0.25 mi (5-minute walk) to the Brookline Village Green Line station. Source: BMN Boston / Raveis / Barrett Sotheby's (MLS 73428041, 73428038) (search snippets).
   - Notes: Possibly stale (more than six months old). Kimco's Brookline Village center at 9 Harvard St is listed as fully leased with a waitlist.
24. **Tiny restaurant unit, Cypress St** (lease), 6-12 Cypress St, Brookline (Brookline Village).
   - Rent as stated: $3,200/mo.
   - Prior use: Restaurant (listed as restaurant for lease). Second-generation evidence: Listed as a restaurant for lease; equipment not stated.
   - Crowd context: Brookline Village. Source: CityFeet (search snippet).
   - Notes: 600 SF is below the 900 SF minimum; $3,200 x 12 / 600 = $64/SF/yr. Building built 1935. Older listing ID: possibly stale.
25. **2nd-gen 257-seat restaurant, Coolidge Corner (oversized)** (lease), 1280 Beacon St (1278-1290 Beacon St), Brookline (Coolidge Corner).
   - Rent as stated: not stated.
   - Prior use: Restaurant (fully equipped, licensed for 257 seats). Second-generation evidence: Second-generation restaurant with fully equipped kitchen and 257-seat license.
   - Crowd context: Coolidge Corner (North Brookline). Source: CommercialCafe / LoopNet brochure (search snippets); broker Conviser Property Group.
   - Notes: Divisible 6,000-9,175 SF: still at least double the ceiling. Partial match.
26. **Restaurant with full liquor license, Washington Square (oversized)** (lease), 1627 Beacon St, Brookline (Washington Square).
   - Rent as stated: $9,000 (period not stated; if monthly, about $21.60/SF/yr).
   - Prior use: Restaurant. Second-generation evidence: Restaurant location with a full liquor license.
   - Crowd context: Washington Square. Source: LoopNet / Raveis / Corcoran (search snippets).
   - Notes: 5,000 SF is above the ceiling. Old LoopNet ID and several MLS numbers (73303252, 73322487) suggest a long-running or re-listed space.
27. **Route 9 restaurant with parking (oversized)** (lease), 1180 Boylston St, Brookline (Route 9).
   - Rent as stated: not stated.
   - Prior use: Restaurant property. Second-generation evidence: Listed as a restaurant property.
   - Crowd context: Route 9 with 20 parking spaces (car-oriented). Source: CommercialSearch / CommercialCafe (search snippet); Conviser Property Group.
   - Notes: Too large and car-oriented; partial.
28. **2nd-gen restaurant plus adjacent retail, Newton Centre** (lease), 1191 Centre St (1185-1197 Centre St), Newton (Newton Centre).
   - Rent as stated: Contact broker for pricing.
   - Prior use: Restaurant. Second-generation evidence: CBRE: '1,894 SF second generation restaurant space'.
   - Crowd context: Newton Centre; municipal lots nearby (Triangle 126 spaces, Pleasant St 76, Pelham St 88). Source: CBRE / CommercialCafe / CommercialSearch / Realmo (search snippets).
   - Notes: Combinable with an adjacent 951 SF retail unit for up to 2,845 SF, which suits the bakery-cafe format. Available immediately; renewal option; no sublease. Realmo shows only the 951 SF unit (1185-1197 Centre St): confirm which suites remain.
29. **1,200 SF turnkey restaurant, West Newton** (lease), 1385 Washington St, Newton (West Newton).
   - Rent as stated: $4,000/mo (NNN or gross not stated).
   - Prior use: Restaurant (turnkey). Second-generation evidence: Listed as turnkey restaurant space.
   - Crowd context: West Newton village center; source names no crowd generator. Source: Raveis / Elliman / BMN Boston (MLS 73445933) (search snippets).
   - Notes: $4,000 x 12 / 1,200 = $40/SF/yr. An earlier summary called neighbouring 1383 Washington St a turnkey former Shogun Sushi space; a follow-up search found no Shogun reference and placed the turnkey listing at 1385. Fits the 1,200 SF counter format.
30. **Retail/office storefront, West Newton** (lease), 1383 Washington St, Newton (West Newton).
   - Rent as stated: $3,000/mo.
   - Prior use: Retail/office (previously a long-term tenant). Second-generation evidence: none stated.
   - Crowd context: West Newton village center. Source: LoopNet / Raveis / Boston Pads (MLS 73182878, 73232759) (search snippets).
   - Notes: 1,200 SF is LoopNet's figure; Boston Pads gives SQFT N/A and the same 1,200 SF appears for 1385, so the listings may be mixed up. $3,000 x 12 / 1,200 = $30/SF/yr. A Boston Pads 'commercial for sale' page suggests the building may also be for sale.
31. **Stand-alone restaurant building with hood, Newton Centre** (lease), 107R Union St, Newton (Newton Centre).
   - Rent as stated: not stated.
   - Prior use: Restaurant (stand-alone building). Second-generation evidence: Kitchen hood system already in place; newly renovated; new enclosed patio.
   - Crowd context: Newton Centre; large sign rights on the building; no crowd generator named. Source: Douglas Elliman / EV Real Estate / CommercialSearch (search snippets).
   - Notes: Strong second-generation evidence (hood in place), but size and rent unknown.
32. **Former pizza restaurant, Four Corners** (lease), 1158 Beacon St, Newton (Four Corners).
   - Rent as stated: not stated.
   - Prior use: Pizza restaurant. Second-generation evidence: Former pizza restaurant; equipment not stated.
   - Crowd context: not stated. Source: Search summary of Realmo/CommercialSearch results.
   - Notes: URL attribution uncertain (the summary gave the address without tying it to a result). Former pizza use may mean a hood exists: confirm.
33. **2nd-gen restaurant (3,400 SF), Newton Corner** (lease), 275 Washington St, Newton (Newton Corner).
   - Rent as stated: not stated.
   - Prior use: Restaurant. Second-generation evidence: 3,400 SF second-generation restaurant space (search summary).
   - Crowd context: Newton Corner. Source: CommercialCafe (search snippet).
   - Notes: Slightly above 3,000 SF; one of several spaces in the building. Thai Amarin (287 Centre St, Newton Corner) closed nearby in June 2026.
34. **Restaurant/retail on the Needham St corridor (oversized)** (lease), 141-165 Needham St, Newton (Newton Upper Falls).
   - Rent as stated: NNN; pricing not stated.
   - Prior use: not stated. Second-generation evidence: none stated.
   - Crowd context: Busy road with 515 parking spaces (car-oriented). Source: CommercialSearch (search snippets).
   - Notes: Up to 4,600 SF; summaries cite both 141 and 165 Needham St for the same size, probably one development. Car-oriented strip.
35. **Retail with restaurant use, Newtonville** (lease), 835-855 Washington St, Newton (Newtonville).
   - Rent as stated: not stated.
   - Prior use: not stated (restaurant is a designated use). Second-generation evidence: none stated.
   - Crowd context: Newtonville village center. Source: CommercialSearch (search snippet).
   - Notes: Size not stated. Mochiko Hawaiian in Newtonville closed in October 2026, so another food space may be free in the village.
36. **Closed tapas/whiskey bar lease, no key money** (lease), Address withheld, Watertown.
   - Rent as stated: $10,000/mo base plus NNN; 10-year initial term.
   - Prior use: Tapas and whiskey bar/restaurant (currently closed). Second-generation evidence: Turn-key; equipment in good condition; full liquor and entertainment licenses; 100+ seats plus outdoor seating.
   - Crowd context: 'Densely populated area of Watertown with an excellent mix of businesses, residents and lots of foot traffic'. Source: BizQuest / BizBuySell / BusinessesForSale 'Lease Only' (search snippets).
   - Notes: $10,000 x 12 / 3,250 = $36.92/SF/yr base. Historical sales of the prior operator $1.7-2.0M. No key money; first and last month plus security deposit. Slightly above 3,000 SF. BizQuest ID suggests a 2025 listing: confirm still available.
37. **The Maximilian, restaurant-ready unit, Watertown Square** (lease), 104-108 Main St, Watertown (Watertown Square).
   - Rent as stated: not stated.
   - Prior use: not stated. Second-generation evidence: 3,041 SF unit 'equipped for potential restaurant use' (not a former restaurant).
   - Crowd context: Directly across the street from the public library and city hall. Source: LoopNet flyer PDF (search snippet).
   - Notes: Other units are 2,617 SF and 758 SF. 3,041 SF is at the ceiling.
38. **WaterMills ground-floor restaurant space** (lease), 350 Pleasant St, Watertown.
   - Rent as stated: $11,970/mo (Weichert shows $38).
   - Prior use: not stated (ground-floor restaurant space). Second-generation evidence: Described as ground-floor restaurant space; equipment not stated.
   - Crowd context: not stated. Source: LoopNet / CityFeet / Weichert (search snippets).
   - Notes: $11,970 x 12 / 3,780 = $38.00/SF/yr. Above the 3,000 SF ceiling.
39. **1,412 SF 2nd-gen restaurant, Arlington Heights** (lease), 1326 Massachusetts Ave (1310-1328 Massachusetts Ave), Arlington (Arlington Heights).
   - Rent as stated: Contact for pricing.
   - Prior use: Restaurant. Second-generation evidence: 'Rare second-generation restaurant space'; listing says not turnkey.
   - Crowd context: 'At the epicenter of the Square' (Arlington Heights). Source: CommercialCafe / CommercialSearch (search snippets).
   - Notes: Available immediately; renewal option; no sublease. A 2019 BRT post reported The Heights Pub leasing 1314 Mass Ave (former Balich 5 & 10); whether that is this unit is unknown. Good fit for the 1,200 SF counter format.
40. **Retail in the new Majestic Mill Brook building** (lease), 1025 Massachusetts Ave, Arlington.
   - Rent as stated: $38/SF/yr.
   - Prior use: New construction. Second-generation evidence: none (new mixed-use development).
   - Crowd context: not stated. Source: Realmo (search snippets).
   - Notes: The only retail space in the Majestic Mill Brook mixed-use development. First-generation space; possibly stale.
41. **Retail/office storefront near Arlington Center** (lease), 713-725 Massachusetts Ave, Arlington (near Arlington Center).
   - Rent as stated: $38/SF/yr, modified gross.
   - Prior use: Currently used as a day space. Second-generation evidence: none stated.
   - Crowd context: Mass Ave; source names no crowd generator. Source: CommercialSearch (search snippet).
   - Notes: Not a food space. Colette Bakery opened at 681 Mass Ave, Arlington Center, in October 2026 (BRT), a direct competitor nearby.
42. **Former Starbucks cafe near Tufts (likely leased)** (lease), 177 College Ave (Joyce Cummings Center), Medford (Tufts University).
   - Rent as stated: Contact for pricing.
   - Prior use: Cafe (Starbucks, closed). Second-generation evidence: Marketed as 'Prime Cafe Space Near Tufts'; restaurant use; former Starbucks.
   - Crowd context: Near Tufts University and the MBTA Green Line. Source: CommercialCafe / CommercialSearch / Realmo (search snippets); WhatNow and Patch news.
   - Notes: Likely NOT available: WhatNow reports Pavement Coffeehouse signed a 10-year lease for this space and Patch reports Pavement signage is up. Campus building.
43. **Small cafe/smoothie storefront, Medford Square** (lease), 24-28 High St, Medford (Medford Square).
   - Rent as stated: $60.00/SF/yr.
   - Prior use: not stated (pitched as a cafe or smoothie bar). Second-generation evidence: none stated.
   - Crowd context: Downtown Medford, street level. Source: LoopNet / CityFeet (search snippets).
   - Notes: Below 900 SF and above the target rent.
44. **Shell restaurant space near Tufts (oversized)** (lease), 402 Boston Ave, Medford (Tufts / Medford Hillside).
   - Rent as stated: not stated.
   - Prior use: Shell. Second-generation evidence: none (shell build).
   - Crowd context: Near Tufts University. Source: PropertyShark / CommercialCafe (search snippet).
   - Notes: Shell condition; availability date TBD; above 3,000 SF.
45. **New cafe space listed on Realmo, Riverside Ave** (lease), 34 Riverside Ave, Medford (Medford Square).
   - Rent as stated: Pricing on request.
   - Prior use: New construction (cafe space). Second-generation evidence: none (newly constructed cafe space).
   - Crowd context: Realmo text says near Tufts University and the MBTA Green Line. Source: Realmo (search snippet).
   - Notes: Possible mix-up: the same 'newly constructed cafe space near Tufts and the Green Line' wording belongs to 177 College Ave, and 34 Riverside Ave is in Medford Square, not near Tufts. Verify before relying.
46. **Storefront with restaurant use, Belmont St** (lease), 285 Belmont St, Belmont (listed under Cushing Square).
   - Rent as stated: Rate on request.
   - Prior use: not stated. Second-generation evidence: none stated; restaurant use noted among amenities.
   - Crowd context: not stated. Source: CityFeet / LoopNet (search snippets).
   - Notes: Available now; LoopNet lists 2,537-5,479 SF as retail. Older listing ID (34951019): possibly stale.
47. **1,300 SF restaurant, Waverley Square (likely stale)** (lease), 687 Belmont St, Belmont (Waverley Square).
   - Rent as stated: $2,500/mo.
   - Prior use: Restaurant. Second-generation evidence: Listed as a restaurant.
   - Crowd context: Waverley Square commercial area. Source: CityFeet / LoopNet (search snippets).
   - Notes: $2,500 x 12 / 1,300 = $23.08/SF/yr. A LoopNet page for this address says it is no longer advertised, so probably stale.
48. **Free-standing former bank, Cushing Square** (lease), 63 Trapelo Rd, Belmont (Cushing Square).
   - Rent as stated: not stated.
   - Prior use: Bank branch (BayBank/Citizens), then an insurance office. Second-generation evidence: none.
   - Crowd context: Cushing Square. Source: Raveis (MLS 73270354) (search snippet).
   - Notes: Raw conversion; MLS number suggests an older listing.
49. **Wellesley Square street retail (cafe or restaurant allowed)** (lease), 34 & 48-50 Central St, Wellesley (Wellesley Square).
   - Rent as stated: Contact for pricing; NNN.
   - Prior use: not stated. Second-generation evidence: none stated; marketed for retail, medical, fitness, cafe or restaurant use.
   - Crowd context: Center of Wellesley Square. Source: CommercialSearch / CommercialCafe / PropertyShark (search snippets).
   - Notes: Two spaces totaling 8,856 SF; individual sizes not stated.
50. **Central Plaza retail spaces, Wellesley Square** (lease), 74 Central St (Central Plaza), Wellesley (Wellesley Square).
   - Rent as stated: not stated.
   - Prior use: not stated. Second-generation evidence: none stated.
   - Crowd context: Nearby restaurants: Bocado Tapas Bar, Amarin of Thailand II, Tutto Italiano, Cafe Mangal, Rice Burg. Source: CommercialSearch (search snippet).
   - Notes: Three retail spaces designated street retail; not described as food-ready.
51. **Lower-level specialty space, downtown Needham** (lease), 990-992 Great Plain Ave, Needham (Needham Center).
   - Rent as stated: not stated.
   - Prior use: not stated. Second-generation evidence: none stated.
   - Crowd context: Downtown Needham. Source: CommercialSearch / CommercialCafe (search snippet).
   - Notes: Lower level and above 3,000 SF: weak fit.
52. **2nd-gen restaurant in the Giroux Building, Lexington Center** (lease), 1833 Massachusetts Ave (The Giroux Building), Lexington (Lexington Center).
   - Rent as stated: not stated.
   - Prior use: Restaurant. Second-generation evidence: Described as second-generation restaurant space.
   - Crowd context: Mass Ave near Emery Park, Lexington Center. Source: CommercialSearch / CommercialCafe (search snippets).
   - Notes: One space available; Realmo's 32,317 SF figure is probably the building, not the space. Abbott's Frozen Custard at 1853 Mass Ave closed nearby (August 2026).
53. **Former restaurant (4,560 SF), Lexington Center** (lease), 27 Waltham St, Lexington (Lexington Center).
   - Rent as stated: not stated; similar-sized lower level offered rent-free.
   - Prior use: Restaurant. Second-generation evidence: Former restaurant space.
   - Crowd context: Lexington Center. Source: Raveis (MLS 73239309) (search snippet).
   - Notes: Above the 3,000 SF ceiling; MLS number suggests an older listing.
54. **Retail/office space, historic Lexington Center** (lease), 1844 Massachusetts Ave, Lexington (Lexington Center).
   - Rent as stated: $35 (unit not stated).
   - Prior use: not stated. Second-generation evidence: none stated.
   - Crowd context: Historic Lexington Center. Source: Raveis flyer (search snippet).
   - Notes: Not a food space.
55. **2nd-gen restaurant space, Quincy Center (oversized)** (lease), 1495 Hancock St, Quincy (Quincy Center).
   - Rent as stated: Rate upon request.
   - Prior use: Restaurant. Second-generation evidence: About 5,350 SF of second-generation restaurant space; another listing describes 3,600+ SF 'built out as restaurants and cafes'.
   - Crowd context: Hancock St, Quincy Center. Source: LoopNet / CityFeet / CommercialSearch (search snippets).
   - Notes: Two spaces; both above 3,000 SF unless divisible.
56. **Vacant standalone commercial building, Brooks Ave** (lease), 16 Brooks Ave, Quincy (02169).
   - Rent as stated: $3,500/mo, triple net.
   - Prior use: not stated (vacant). Second-generation evidence: none stated.
   - Crowd context: Street parking only; source names no crowd generator. Source: Boston.com real estate (MLS PIN 73396618; V & E Realty).
   - Notes: Two separate spaces with private entrances plus a finished lower level. Lease page shows a placeholder size; 2,090 SF is from the same property's sale listing (MLS 73396614, $599,000), so $3,500 x 12 / 2,090 = $20.10/SF/yr is approximate. Not a food space; side-street location.
57. **Pad at the Legacy Place entrance (oversized)** (lease), 850 Providence Hwy, Dedham (Legacy Place entrance).
   - Rent as stated: Contact for pricing; NNN.
   - Prior use: not stated. Second-generation evidence: none stated.
   - Crowd context: At the signalized entrance to Legacy Place (lifestyle center). Source: CommercialCafe / CommercialSearch (search snippet).
   - Notes: Restaurant, retail or medical use; immediate availability; more than double the size ceiling.
58. **Space at Legacy Place (Avison Young)** (lease), 770 Legacy Place, Dedham (Legacy Place).
   - Rent as stated: not stated.
   - Prior use: not stated. Second-generation evidence: none stated.
   - Crowd context: Legacy Place lifestyle center. Source: Avison Young (search result title only).
   - Notes: Only the result title was seen; size, use and rent unknown.
59. **End-cap needing renovation, Main St** (lease), 881-889 Main St, Winchester.
   - Rent as stated: not stated.
   - Prior use: not stated (end-cap 'in need of renovation'). Second-generation evidence: none stated; a pizza restaurant is an existing tenant in the building.
   - Crowd context: not stated. Source: LoopNet (search snippet).
   - Notes: Size and rent unknown.
60. **Office/retail storefront, Winchester Center** (lease), 535 Main St, Winchester (Winchester Center).
   - Rent as stated: not stated.
   - Prior use: Office/retail. Second-generation evidence: none stated.
   - Crowd context: Strong pedestrian traffic, nearby parking, close to shops, restaurants and the commuter rail. Source: LoopNet (search snippet).
   - Notes: Not a food space; available since January 2026.
61. **Multi-use space pitched for a bakery (town withheld)** (lease), Address withheld, Arlington, Belmont, Watertown, Waltham or Newton (withheld).
   - Rent as stated: not stated.
   - Prior use: not stated. Second-generation evidence: none stated; marketed as ideal for non-food businesses or a bakery and ice cream shop or juice bar.
   - Crowd context: 'Densely populated and high traffic area'. Source: BizQuest real estate for lease (search snippet).
   - Notes: BizQuest ID suggests a 2025 listing: possibly stale.
62. **Built-out QSR steps from Davis Square, FF&E sale** (business_for_sale), 24 College Ave, Somerville (Davis Square).
   - Rent as stated: About $3,000/mo plus NNN (about $450/mo); new lease to be negotiated with the landlord. Asking price: $200,000; revenue: -1; SDE/cash flow: -1.
   - Prior use: Quick-service restaurant (12 seats). Second-generation evidence: Fully built-out quick-service restaurant; FF&E included; hood not stated.
   - Crowd context: High foot traffic, steps from Davis Square Station and Tufts University. Source: Boston.com real estate (MLS PIN 73569759; Berkshire Hathaway HomeServices Commonwealth Real Estate).
   - Notes: 600 SF ground floor plus 600 SF basement for prep and storage. $3,000 x 12 / 600 = $60/SF/yr on the ground floor ($30 counting the basement). FF&E asset sale only; revenue, SDE and remaining lease term not stated. Ground floor is below the 900 SF minimum.
63. **Established restaurant near the Red Line, Quincy** (business_for_sale), Address withheld (listed as '9999 Copland St'), Quincy (02169).
   - Rent as stated: not stated (leased location). Asking price: $160,000; revenue: -1; SDE/cash flow: -1.
   - Prior use: Restaurant (25+ seats). Second-generation evidence: Sale includes kitchen equipment, machinery and fixtures; hood not stated.
   - Crowd context: Near the Red Line T. Source: Boston.com real estate (MLS PIN 73570259; Dream Realty).
   - Notes: Business only; about 1,850 SF total including about 230 SF of storage. Cuisine, revenue, SDE and lease term not stated.
64. **Breakfast/lunch restaurant with building, Broadway near Ball Square** (business_for_sale), 704 Broadway, Somerville (02144).
   - Rent as stated: n/a (real estate included). Asking price: $2,150,000; revenue: -1; SDE/cash flow: -1.
   - Prior use: Breakfast and lunch restaurant. Second-generation evidence: Operating restaurant; full liquor license and full bar and tap system included.
   - Crowd context: not stated. Source: Boston.com real estate (MLS PIN 73502637; The Mahoney Group).
   - Notes: Business and real estate sold together; lot 0.08 acres; annual tax $20,441.90; financials not stated. Address is on the Ball Square stretch of Broadway (inferred from the address). Far above a first-shop budget.
65. **Free-standing restaurant building with FF&E by Watertown Mall** (business_for_sale), 71-73 Elm St, Watertown.
   - Rent as stated: n/a (building for sale). Asking price: $635,000; revenue: -1; SDE/cash flow: -1.
   - Prior use: Restaurant. Second-generation evidence: Code-compliant full kitchen with venting, refrigerators, seating and basement dry storage; all FF&E included.
   - Crowd context: Directly abuts the Watertown Mall, close to Arsenal Yards. Source: Boston.com real estate (MLS PIN 73580699; City Realty Group).
   - Notes: A building sale, not a lease, sold as-is; lot 0.07 acres; annual tax $8,160; building size not stated. An owner-occupier route with a vented kitchen in place.
66. **Fast-casual cafe, Lexington Center** (business_for_sale), Lexington Center (street address not stated), Lexington (Lexington Center).
   - Rent as stated: $6,563/mo. Asking price: $165,000; revenue: -1; SDE/cash flow: -1.
   - Prior use: Fast-casual cafe (12 seats). Second-generation evidence: Brand-new first-class fast-casual build-out suited to sandwiches, soups, bowls, smoothies, drinks or coffee; ADA compliant.
   - Crowd context: Lexington Center. Source: BizQuest BW2476956 (search snippets).
   - Notes: $6,563 x 12 / 1,550 = $50.81/SF/yr. Cash flow, revenue and EBITDA not disclosed (available under NDA). Lease term not stated. Seller wants to focus on other interests.
67. **Restaurant business with hood, Needham (address withheld)** (business_for_sale), Address withheld ('000 Confidential', Needham 02492), Needham.
   - Rent as stated: $5,900/mo base plus about $1,200/mo NNN (about $61.43/SF/yr all-in on the first floor). Asking price: -1; revenue: -1; SDE/cash flow: -1.
   - Prior use: Restaurant. Second-generation evidence: Hood ventilation systems; basement storage.
   - Crowd context: Busy commercial area near a large public parking lot. Source: Raveis / Gillach Group (MLS 73519495) (search snippets).
   - Notes: About 8 years left on the lease (meets the 5+ year preference). 1,387 SF first floor plus full basement. $5,900 x 12 / 1,387 = $51.05/SF/yr base. Asking price, revenue and SDE not found.
68. **Turnkey cafe, Central Square** (business_for_sale), Central Square (street address not stated), Cambridge (Central Square).
   - Rent as stated: not stated. Asking price: $200,000; revenue: -1; SDE/cash flow: -1.
   - Prior use: Cafe. Second-generation evidence: Turnkey cafe; equipment not stated.
   - Crowd context: Central Square. Source: BizBuySell (search summary of category pages).
   - Notes: The individual listing URL was not identified. Size, rent, revenue and SDE unknown.
69. **Boba cafe near BU, Brookline** (business_for_sale), Near Boston University (street address not stated), Brookline.
   - Rent as stated: $6,000/mo. Asking price: $1,200,000; revenue: -1; SDE/cash flow: -1.
   - Prior use: Boba/bubble-tea cafe. Second-generation evidence: Operating cafe.
   - Crowd context: Near Boston University. Source: BizBuySell (search summary of category pages).
   - Notes: Down payment $300,000. Size, revenue and SDE not captured; individual listing URL not identified.
70. **Boba and coffee shop, Newton Centre** (business_for_sale), 212 Sumner St, Newton (Newton Centre).
   - Rent as stated: not stated. Asking price: -1; revenue: -1; SDE/cash flow: -1.
   - Prior use: Boba and coffee shop. Second-generation evidence: Operating coffee shop.
   - Crowd context: Newton Centre. Source: Realmo (search summary).
   - Notes: Price, size, rent and financials not captured; possibly stale.
71. **Restaurant with patio, Assembly Row** (business_for_sale), Assembly Row (street address not stated), Somerville (Assembly Row).
   - Rent as stated: not stated. Asking price: -1; revenue: -1; SDE/cash flow: -1.
   - Prior use: Restaurant. Second-generation evidence: Marketed as '1st class restaurant space' with patio.
   - Crowd context: Assembly Row lifestyle center. Source: BizBuySell 2519320 (search snippet).
   - Notes: About 1,500 SF plus patio; sold as a business, not leased directly. Price and financials not captured.
72. **Turnkey restaurant business, Teele Square** (business_for_sale), 1148 Broadway, Somerville (Teele Square).
   - Rent as stated: not stated. Asking price: -1; revenue: -1; SDE/cash flow: -1.
   - Prior use: Restaurant (well established). Second-generation evidence: Turnkey; all equipment included.
   - Crowd context: Teele Square. Source: Century 21 Commercial (search snippet).
   - Notes: Price, size and financials not captured.
73. **Italian pizzeria with 7 years of lease, Melrose** (business_for_sale), Melrose (street address not stated), Melrose.
   - Rent as stated: $3,690/mo; 7 years remaining on the lease. Asking price: $100,000; revenue: -1; SDE/cash flow: -1.
   - Prior use: Pizzeria (25 seats). Second-generation evidence: Pizzeria with build-out and equipment.
   - Crowd context: not stated. Source: BizBuySell (search snippet).
   - Notes: The stated 350 sq ft conflicts with 25 seats, so rent was not normalized. Seven years left on the lease meets the 5+ year preference.
74. **Full-service restaurant with 40-seat bar, Burlington** (business_for_sale), Burlington (street address not stated), Burlington.
   - Rent as stated: not stated. Asking price: -1; revenue: -1; SDE/cash flow: -1.
   - Prior use: Full-service restaurant with bar. Second-generation evidence: Turnkey full-service restaurant.
   - Crowd context: 'High-traffic Burlington'. Source: BizQuest BW2428070 (search snippet).
   - Notes: Probably larger than needed; price and financials not captured.
75. **Restaurant with two hoods, Watertown** (business_for_sale), Watertown (street address not stated), Watertown.
   - Rent as stated: not stated. Asking price: -1; revenue: -1; SDE/cash flow: -1.
   - Prior use: Restaurant. Second-generation evidence: Two hoods (per listing title).
   - Crowd context: not stated. Source: BizQuest BW2416108 (search result title).
   - Notes: Only the title was seen; price, size, rent and financials unknown; BizQuest ID suggests a 2025 listing.
76. **Closed bakery (Nine Winters), West Cambridge** (closed_space), 292 Concord Ave, Cambridge (West Cambridge).
   - Rent as stated: not stated.
   - Prior use: Bakery (Nine Winters Bakery, open July 2025 to March 29, 2026). Second-generation evidence: Former bakery fitted out in 2025; equipment and hood not stated.
   - Crowd context: not stated. Source: Boston Restaurant Talk (page read); follow-up web search.
   - Notes: The owner cited family reasons; the post does not mention sales. A November 2026 search found no new tenant or listing; the city database lists the owner as CONCORD-WALDEN, LLC. A recent bakery fit-out, so possibly the closest match to a former bakery. Size unknown.
77. **Cafe Barada closing, North Cambridge** (closed_space), 2269 Massachusetts Ave, Cambridge (North Cambridge).
   - Rent as stated: not stated.
   - Prior use: Full-service Lebanese restaurant (at this address since 2002). Second-generation evidence: Long-running restaurant kitchen; hood not stated.
   - Crowd context: not stated. Source: Boston Restaurant Talk (page read).
   - Notes: Full-service dining ends December 5, 2026; the owners mention 'future endeavors', so they may keep the space. Size unknown.
78. **Closed coffee shop (Lola's), West Medford** (closed_space), 17 Playstead Rd, Medford (West Medford).
   - Rent as stated: not stated.
   - Prior use: Coffee shop (Lola's Coffee and More 2023-2026; earlier Nourish Your Soul). Second-generation evidence: Two successive cafe tenants; equipment not stated.
   - Crowd context: not stated. Source: Boston Restaurant Talk (page read).
   - Notes: Closed suddenly after a sale to a new owner fell through, so the owner may still sell the fit-out. Size unknown, probably small.
79. **Closed Comella's, Melrose Main St** (closed_space), 478A Main St, Melrose.
   - Rent as stated: not stated.
   - Prior use: Italian fast-casual restaurant (Comella's franchise). Second-generation evidence: Former restaurant; hood not stated.
   - Crowd context: Main Street, Melrose. Source: Boston Restaurant Talk (page read).
   - Notes: Closed March 20, 2026 after franchisee 'operational and financial challenges'. Re-let status unknown. Colette Bakery already operates in Melrose.
80. **Closed Melty, Washington St, Dedham** (closed_space), 290 Washington St, Dedham.
   - Rent as stated: not stated.
   - Prior use: Fast-casual grilled cheese and melts (September 2024 to March 2026). Second-generation evidence: Restaurant fitted out in 2024; hood not stated.
   - Crowd context: not stated. Source: Boston Restaurant Talk (page read).
   - Notes: Closed March 8, 2026, citing a challenging environment. On Washington St, not at Legacy Place. Size unknown.
81. **Closed Abbott's Frozen Custard, Lexington Center** (closed_space), 1853 Massachusetts Ave, Lexington (Lexington Center).
   - Rent as stated: not stated.
   - Prior use: Frozen custard shop. Second-generation evidence: Food shop described as 'fully set up inside' while dark.
   - Crowd context: Lexington Center. Source: Boston Restaurant Talk (page read).
   - Notes: Dark for months before closing permanently. A dessert counter, so a Type 1 hood is unlikely. Size unknown.
82. **Closed Shine's Fresh Asian, Belmont Center** (closed_space), 30 Leonard St, Belmont (Belmont Center).
   - Rent as stated: not stated.
   - Prior use: Asian fusion restaurant (2016-2025; earlier Asai). Second-generation evidence: Two successive restaurant tenants; hood not stated.
   - Crowd context: Belmont Center. Source: Boston Restaurant Talk (page read).
   - Notes: Closed about a year ago; may already be re-let (not checked). Size unknown.
83. **Closed Thai Amarin, Newton Corner** (closed_space), 287 Centre St, Newton (Newton Corner).
   - Rent as stated: not stated.
   - Prior use: Thai restaurant (long-standing). Second-generation evidence: Long-running restaurant; hood not stated.
   - Crowd context: Newton Corner. Source: Boston Restaurant Talk (page read).
   - Notes: Closed mid-to-late June 2026; no successor known at posting. Size unknown.
84. **Closed Kostas Pizza & Seafood, Chestnut St** (closed_space), 315 Chestnut St, Needham.
   - Rent as stated: not stated.
   - Prior use: Pizza and Greek-Italian restaurant (about 30 years). Second-generation evidence: Long-running pizza and seafood kitchen; hood not stated.
   - Crowd context: not stated. Source: Boston Restaurant Talk (page read).
   - Notes: Closed at the end of May 2026. Size unknown.
85. **Closed Mochiko Hawaiian, Newtonville** (closed_space), Newtonville (street address not stated in source), Newton (Newtonville).
   - Rent as stated: not stated.
   - Prior use: Fast-casual Hawaiian fried chicken and bubble tea (2022-2026). Second-generation evidence: Former fried-chicken restaurant; equipment and hood not stated.
   - Crowd context: not stated. Source: Boston Restaurant Talk (page read).
   - Notes: The post gives no street address. Size unknown.
86. **Closed Golden Temple, Washington Square (large)** (closed_space), 1651 Beacon St, Brookline (Washington Square).
   - Rent as stated: not stated.
   - Prior use: Chinese-American restaurant with bar and dance floor (66 years). Second-generation evidence: Long-running restaurant kitchen; hood not stated.
   - Crowd context: Beacon Street, Washington Square. Source: Boston Restaurant Talk (page read).
   - Notes: Probably far above 3,000 SF (high arched ceiling, booths, dance floor); size not stated.
87. **Closed Yas Chicken (ex-Qdoba), Middlesex Turnpike** (closed_space), 90 Middlesex Turnpike, Burlington.
   - Rent as stated: not stated.
   - Prior use: Fried chicken quick-service (2024-2026); earlier Qdoba. Second-generation evidence: Two successive quick-service restaurant tenants; hood not stated.
   - Crowd context: Middlesex Turnpike; source names no crowd generator. Source: Boston Restaurant Talk (page read).
   - Notes: Size unknown; car-oriented corridor.
88. **Closed Temazcal and Jack's Coal Fired Pizza, Burlington** (closed_space), 2 Wall St, Burlington.
   - Rent as stated: not stated.
   - Prior use: Mexican restaurant and adjacent coal-fired pizza restaurant. Second-generation evidence: Two restaurant kitchens; hood not stated.
   - Crowd context: not stated. Source: Boston Restaurant Talk (page read).
   - Notes: Just closed. Sizes not stated; probably full-service scale.

## Leads seen but not recorded as candidates

Left out because they were stale, already re-let, non-food and outside the size range, located elsewhere, or too thinly described to check:

- Cambridge: 2172-2180 Mass Ave (6,409 SF former restaurant with patio); a "Commonwealth" corner restaurant (6,530 SF); 561-563 Cambridge St (second-generation retail, available May 1, 2026, size unknown); 1739 Mass Ave (1,468 SF former bank, $52/SF sublease); 684 Mass Ave, Central Square (LoopNet 36346539, no details); 1-5 Bennett St (1,164 SF "retail/restaurant", garbled summary); 2420 Mass Ave (MLS 73538401, no details); 201 Alewife Brook Pkwy (6,500 SF with a Dunkin'); 222 Jacobs St (life-science building, possibly South Boston); New Concept Cafe start-up in Central Cambridge (BizQuest BW2502429); "Prime Cambridge turn-key restaurant space" (BizQuest BW2412625, title only); a famous Harvard/Inman sandwich shop for sale (BizQuest BW2517513); Turing Tavern, Inman (Urban Hearth is taking it).
- Somerville: 321 Washington St, Union Square (about 1,000 SF retail/office at $5,500/mo, about $66/SF); 1244 Broadway (1,250 SF retail at $2,000/mo, about $19/SF, not food); 321 Broadway, Winter Hill ("ideal corner for coffee shop/cafe", no longer advertised); 65 Mystic Ave (2,600 SF, possibly the same as 74 Middlesex Ave); 130 Broadway; 377 Summer St and 490 Broadway (office); Curiosity Brewing's 5,877 SF Davis Square lease (taken); City of Somerville RFP for a Nibble shared kitchen in Bow Market (city tenant search, deadline passed); Somerville cafe with catering for sale (BizQuest BW2262883, title only, older ID); a neighborhood restaurant and a pizzeria for sale (BizBuySell 2433368, BizQuest BW2490813).
- Brookline: 310 Harvard St (1,600 SF, second floor); 1004 Beacon St Gateway (new 2,205-8,200 SF suites); 399 Chestnut Hill Ave (no details).
- Newton: 93 Union St, Newton Centre (8,300 SF restaurant/bar); "275 Centre St" (probably a conflation of 1191 Centre St and 275 Washington St); a wine bar/cafe space ($155,000) and a Newton Centre full-service restaurant ($235,000) for sale; "Attractive Newton Restaurant" (BizBuySell 2416390) and a Newton fast-casual pizza asset sale (BizQuest BW2454732).
- Watertown: 75-85 Main St (5,900 SF retail); 125-135 Mount Auburn St (no size); 385 Main St (no details); Pizza Roma (Bougie Pizza Co. replacing it); Home Taste (rebranding).
- Arlington: 459 Mass Ave (restaurant 1,700-3,400 SF at $31/SF NNN), 464-478 Mass Ave (2,500 SF restaurant at $36/SF NNN) and 430-432 Mass Ave ($25/SF NNN), all from a town document dated February 2021, so stale; 626 Mass Ave #101 (sublease, confusing pricing); 80 Broadway (new build-out, no details); 645R and 25 Mass Ave (no details); Colette Bakery opened at 681 Mass Ave in October 2026 (a competitor, not a site).
- Medford and Melrose: 92 High St B4 (2019 listing); Snappy Pattys, 454 High St, West Medford (Rory O'Connors Irish Pub moving in); Smashburger (Cilantro's) and Real Italian Gusto (Ebisuya) both re-let; 681-697 Main St, Melrose (4,400 SF new mixed-use at $60/SF, not food-ready, URL not pinned down); "Turnkey Restaurant Space - Melrose Shoppes" (TenantBase; location not confirmed as Melrose, MA).
- Belmont: 89 Trapelo Rd (4,600 SF, 2022 sale record); 60 Leonard St (former CVS); 130 Trapelo Rd (office at $22/SF).
- Needham and Wellesley: 935-957 Great Plain Ave (second-floor office); 283 Chestnut St (LoopNet for-lease brochure, not read); the former Rice Barn space (taken by Taberna); 276 Washington St and Central Block, Wellesley (no details).
- Lexington: 235 Bedford St ($38/SF, use unknown).
- Quincy: "209 Quincy Ave, 3,600 SF second-generation restaurant" (summary only, no matching result); President Plaza (retail only).
- Dedham: 300 Providence Hwy (6,250 SF former restaurant on Route 1); Hooters (closed, large).
- Hingham: One Derby St (office; lists a Starbucks tenant with a lease end of August 30, 2026, not confirmed vacant); Derby Corporate Center and Derby Street Office Park (office); 175 Derby St (MLS 73467195, no details).
- Burlington: 211 Middlesex Tpke (restaurant and catering facility, terms unknown); 47 Middlesex Tpke (3,728 SF retail); Cummings TC128 cafe space in an office building at the I-95 Woburn/Burlington line (office-atrium type, excluded by the criteria); Smith & Wollensky (closed, large); Osteria Nino (Citrus & Salt taking it).
- Winchester: "Wrenly Residences" ground-floor restaurant space (town not confirmed); Judkin Green office condos.
- Outside this sweep's area (for the Boston-neighborhood sweeps): Home.stead Bakery and Cafe, Fields Corner (closing, June 2026); Bruegger's, West Roxbury (closed, September 2026); Dugout Cafe, Boston (closed, January 2026).

## Query log

Web searches (35 of 35 allowed):

1. second generation restaurant space for lease Cambridge MA 2026: 1334 Cambridge St, 18 Eliot St, 293 Cambridge St, 300 Mass Ave, 2172-2180 Mass Ave, 561-563 Cambridge St.
2. former cafe space for lease Somerville MA hood: 495 Columbia St, 51 Holland St, 96 Middlesex Ave, 257 Washington St, 114-118 Broadway.
3. restaurant space for lease Brookline MA Coolidge Corner Brookline Village: 1284 and 1280 Beacon St, 6-12 Cypress St, 1180 Boylston St, 1627 Beacon St, 173 Amory St.
4. restaurant cafe space for lease Newton MA Newton Centre Newtonville West Newton: 1191 Centre St, 107R Union St, 93 Union St, 1383 Washington St, 275 Washington St, 835-855 Washington St.
5. restaurant space for lease Watertown MA Watertown Square second generation: The Maximilian (104-108 Main St), 350 Pleasant St, the no-key-money lease.
6. restaurant cafe space for lease Arlington MA Massachusetts Ave Arlington Center Capitol Square: 1310-1328 Mass Ave, 713-725 Mass Ave, the 2021 town list.
7. restaurant cafe space for lease Medford MA Medford Square West Medford Melrose Main Street: 177 College Ave, 402 Boston Ave, 24-28 High St, 681-697 Main St (Melrose).
8. restaurant space for lease Belmont MA Belmont Center Cushing Square Waverley Square: 285 Belmont St, 63 and 89 Trapelo Rd, 687 Belmont St.
9. restaurant cafe space for lease Needham Center Wellesley Square MA 2026: 34 and 48-50 Central St, Central Plaza, 990-992 Great Plain Ave, the Needham business opportunity.
10. restaurant cafe space for lease Quincy MA Wollaston Quincy Center North Quincy 2026: 1495 Hancock St.
11. restaurant cafe space for lease Lexington Center Winchester Center MA: Giroux Building, 27 Waltham St, 1844 Mass Ave, the Lexington cafe for sale.
12. Legacy Place Dedham MarketStreet Lynnfield Derby Street Hingham available space for lease restaurant: 850 Providence Hwy, 770 Legacy Place; nothing at MarketStreet or Derby Street.
13. restaurant cafe space for lease Melrose MA Burlington MA turnkey restaurant: Melrose pizzeria sale, Burlington restaurant sale, 118 Broadway turnkey.
14. cafe bakery space for lease Porter Square Harvard Square Cambridge MA former cafe: 1430, 1674 and 1847-1855 Mass Ave, 361 Huron Ave.
15. restaurant space for lease Davis Square Union Square Ball Square Somerville MA 2026: 51 Holland St, 212 Elm St, 321 Washington St.
16. cafe space for lease Central Square Inman Square Kendall Cambridge MA restaurant hood available now: 1248-1260 Cambridge St, 1036 Cambridge St, 296 Green St.
17. Brookline MA Harvard Street Washington Square Brookline Village cafe bakery space for lease 2026: 60-62 Harvard St, 1630 Beacon St.
18. "former bakery" space for lease Massachusetts Cambridge Somerville Newton Arlington Brookline: BizQuest multi-use space, 1158 Beacon St (Newton).
19. Somerville Magoun Square Teele Square Winter Hill Assembly Row turnkey restaurant cafe space for lease: 74 Middlesex Ave, Assembly Row sale, 1148 Broadway sale.
20. Hingham Square Derby Street Winchester Center restaurant cafe space for lease 2026: 881-889 and 535 Main St (Winchester); Hingham office only.
21. "lease only" cafe OR bakery OR "coffee shop" Massachusetts turnkey Newton Brookline Cambridge Arlington Watertown bizbuysell: Central Square cafe, BU boba cafe, 1025 Mass Ave (Arlington).
22. "1191 Centre Street" Newton restaurant space lease: size, combinability, availability.
23. "361 Huron Ave" Cambridge cafe space for lease second generation: size range, NNN, BA-1, May 2026 dates.
24. "177 College Ave" Medford cafe space near Tufts for lease: leased to Pavement Coffeehouse.
25. "1310" Massachusetts Ave Arlington Heights second generation restaurant space lease: 1,412 SF, not turnkey.
26. "1248" Cambridge St Inman Square turn-key restaurant lease $60 NNN: $60/SF NNN, 99 seats, FF&E for sale.
27. "18 Eliot Street" Cambridge Harvard Square restaurant lease 3,000 SF: lower level 1,143 SF, 84 seats, Conviser.
28. "292 Concord Ave" Cambridge Nine Winters bakery space new tenant OR lease: no new tenant found.
29. "118 Broadway" Somerville turnkey second generation restaurant space lease square feet rent: $36/SF plus NNN, 3,780 SF, 5+5+5 years.
30. Watertown MA restaurant lease "no key money" turn-key 3,250 square feet $10,000 per month address: terms confirmed; address withheld.
31. "Lexington Center" fast casual cafe for sale $165,000 cash flow revenue lease: financials not disclosed.
32. Needham MA restaurant business opportunity $5,900 month NNN 1,387 sq ft first floor full basement lease years remaining: hood, about 8 years left.
33. realmo coffee shop cafe space for lease Middlesex County MA Cambridge Somerville Newton Arlington: 1025 Mass Ave, 34 Riverside Ave, 212 Sumner St.
34. "1383 Washington St" West Newton turnkey restaurant former Shogun lease square feet: turnkey listing is 1385 Washington St, $4,000/mo.
35. "173 Amory St" Brookline restaurant cafe space for lease 1,510 SF built out: second-generation QSR, NNN, relet.

Pages fetched (no search cost):

- WebFetch: cambridgeday.com and bostonpads.com failed (host not resolvable), not retried; www.boston.com also failed in WebFetch but worked with curl through the proxy.
- curl, Boston.com MLS pages: 24 College Ave, Somerville (MLS 73569759); Quincy restaurant (MLS 73570259); 704 Broadway, Somerville (MLS 73502637); 71-73 Elm St, Watertown (MLS 73580699); 16 Brooks Ave, Quincy (MLS 73396618); one expired listing (MLS 73505899, redirected to search).
- curl, Boston.com listing searches (commercial, for sale, under $750,000 and under $50,000) for the 18 target towns: few results, mostly offices; searching by MLS number does not work.
- curl, Boston Restaurant Talk searches ("closed" plus each of 18 towns; "bakery has closed", "cafe has closed", "coffee has closed", "bakery closing", "cafe closing", "donut closed", "bagel closed") and 21 posts, including six weekly roundups from 2026. Rapid requests sometimes returned 503 and were retried after a pause.
