/* The Miami page's model: tools/proforma.py's arithmetic, ported so the page can recompute as the
   assumptions move. tools/build_miami.py embeds this file in the page and checks it against the
   Python model on every build. No DOM here: `MiamiModel(D)` takes the page's data and returns `run`.

   A lever state S (every field optional):
     v       {channel id: share of the plan's volume}, 1 = the plan
     price   multiplier on every listed menu price (rounded to the cent, as a reprice would be)
     prices  {product id: price} replacing a product's window price
     food    points added to food and packaging as a share of sales
     wage    multiplier on every hourly wage
     rent, nnn   per sq ft a year, replacing the site's; flat = a commissary's rent a year
     baker   true adds the format's extra baker
     manager true pays a hired manager, so the owner steps back
     flex    false holds the crew at the plan's hours when a channel's volume moves
     index   replaces the site's sales index */
function MiamiModel(D) {
  "use strict";
  var op = D.op;
  var sum = function (xs) { var t = 0; for (var i = 0; i < xs.length; i++) t += xs[i]; return t; };
  var vals = function (o) { return Object.keys(o || {}).map(function (k) { return +o[k]; }); };
  var cents = function (x) { return Number(x.toFixed(2)); };

  function linePrice(line, S) {
    var pid = line[0], base = line[2], listed = line[3];
    var p = S.prices && S.prices[pid] != null ? +S.prices[pid] : base;
    return listed && S.price != null && S.price !== 1 ? cents(p * S.price) : p;
  }

  /* format_menu: each channel's own day, then the average working day at this site. */
  function menu(F, kSite, S) {
    var t = { base: 0, design0: 0, site: 0, site0: 0, goods: 0, hours: 0, items: 0, orders: 0, hero: 0, costs: 0, fees: 0, chans: [] };
    F.channels.forEach(function (c) {
      var sales = 0, sales0 = 0, goods = 0, hours = 0, items = 0, hero = 0;
      c.lines.forEach(function (line) {
        var P = D.products[line[0]], par = line[1];
        sales += linePrice(line, S) * c.pi * par;
        sales0 += line[2] * c.pi * par;
        goods += P.cost * par;
        hours += P.min * par / 60;
        if (P.cat !== "add-on") items += par;
        hero += par * P.hero;
      });
      var v = S.v && S.v[c.id] != null ? +S.v[c.id] : 1;
      var w = c.days / F.fmt_days;
      var k = c.scales ? kSite : 1;
      var orders = items / c.ipo;
      t.base += sales * v * w;
      t.design0 += sales0 * w;
      t.site += sales * v * w * k;
      t.site0 += sales0 * v * w * k;
      t.goods += goods * v * w * k;
      t.hours += hours * v * w * k;
      t.items += items * v * w * k;
      t.orders += orders * v * w * k;
      t.hero += hero * v * w * k;
      t.costs += sales * v * w * k * c.cost_pct / 100;
      var fees = v > 0 ? c.fee * c.days : 0;  // no stall booked, no fee
      t.fees += fees;
      t.chans.push({
        id: c.id, v: v, k: k, days: c.days, fees: fees, cost_pct: c.cost_pct,
        day_sales: sales * v * k, day_orders: orders * v * k, day_items: items * v * k, day_hours: hours * v * k,
        ticket: orders ? sales / orders : 0, goods_pct: sales ? 100 * goods / sales : 0, weight: sales * v * w * k
      });
    });
    return t;
  }

  function annualPayment(principal, ratePct, years) {
    var r = ratePct / 100 / 12, n = years * 12;
    if (principal <= 0) return 0;
    if (r === 0) return principal / years;
    return 12 * principal * r / (1 - Math.pow(1 + r, -n));
  }

  function run(fid, site, S) {
    S = S || {};
    var F = D.formats[fid];
    var kSite = (S.index != null ? +S.index : site.sales_index) + (F.index_gain || 0);
    var M = menu(F, kSite, S);
    var days = F.days, pidx = F.price_index;
    var wageMult = S.wage != null ? +S.wage : 1;
    var roles = F.roles.filter(function (r) { return !r.owner; }).map(function (r) {
      var extra = S.baker && F.extra_baker && r.role === F.extra_baker.role ? F.extra_baker.hours : 0;
      return { role: r.role, hours: r.hours + extra, wage: r.wage * wageMult, note: r.note };
    });
    var baseHours = sum(roles.map(function (r) { return r.hours; }));
    var wage = baseHours ? sum(roles.map(function (r) { return r.hours * r.wage; })) / baseHours : 0;
    var burden = 1 + F.burden_pct / 100;
    var fs = F.fixed_share;
    var steady = M.site * pidx * days;
    var goodsPct = (M.site ? 100 * M.goods / M.site / pidx : 0) + op.cogs_buffer + (S.food || 0);
    var varPct = sum(vals(F.var_costs));
    var chanPct = M.site ? 100 * M.costs / M.site : 0;
    var fixedBase = sum(vals(F.fixed_costs));
    var sqft = site.sqft;
    var rentPsf = S.rent != null ? +S.rent : site.rent_psf;
    var nnnPsf = S.nnn != null ? +S.nnn : site.nnn_psf;
    var flat = S.flat != null ? +S.flat : (site.rent_flat || 0);
    var esc = site.escalation_pct / 100;
    var managerBase = F.managed ? F.manager_salary * burden : 0;
    var hired = S.manager ? D.manager_hire.salary * burden : 0;  // flat, as the plan quotes it
    var eff = M.base ? M.site / M.base : 0;
    var flexOn = S.flex !== false;
    // Volume against the format's design day: what the crew's variable hours follow.
    var R = (flexOn ? (M.design0 ? M.site0 / M.design0 : 0) : eff) / F.design_index;

    function year(n) {
      var vol = n === 1 ? op.ramp : 1;
      var yf = vol * (n === 3 ? 1 + op.growth : 1);
      var sales = steady * yf;
      var mult = Math.pow(1 + op.infl, n - 1);
      var share = fs + (1 - fs) * R * vol;
      var hoursDay = baseHours * share;
      var y = {
        year: n, sales: sales, daily_sales: sales / days, hours_day: hoursDay, hours_share: share, vol: vol, yf: yf, mult: mult,
        cogs: sales * goodsPct / 100,
        hourly_labor: hoursDay * wage * burden * days * mult,
        manager: managerBase * mult,
        hired_manager: hired,
        rent: (sqft * rentPsf + flat) * Math.pow(1 + esc, n - 1),
        nnn: sqft * nnnPsf * mult,
        utilities: sqft * F.utilities_psf * mult,
        variable_opex: sales * varPct / 100,
        channel_costs: sales * chanPct / 100 + M.fees * mult,
        fixed_opex: fixedBase * mult
      };
      y.ebitda = sales - y.cogs - y.hourly_labor - y.manager - y.hired_manager - y.rent - y.nnn - y.utilities
        - y.variable_opex - y.channel_costs - y.fixed_opex;
      // Each channel's sales less the costs that are its own: food and packaging, the costs that
      // run with sales, and its commissions and fees. The crew, the rent and the overheads are shared.
      y.channels = M.chans.map(function (ch) {
        var s = ch.weight * pidx * days * yf;
        var goods = s * (ch.goods_pct / pidx + op.cogs_buffer + (S.food || 0)) / 100;
        var variable = s * varPct / 100;
        var own = s * ch.cost_pct / 100 + ch.fees * mult;
        return { id: ch.id, sales: s, goods: goods, variable: variable, own: own, brings: s - goods - variable - own,
                 share: M.site ? ch.weight / M.site : 0, orders: ch.day_orders * ch.days * (days / F.fmt_days) * vol };
      });
      return y;
    }

    var years = [year(1), year(2), year(3)];
    var y1 = years[0], y2 = years[1], y3 = years[2];

    var st = F.st;
    var equipment = sum(F.equipment.map(function (e) { return e.cost; })) - (site.equipment_credit || 0);
    var buildout = sqft * site.buildout_psf;
    var occMonth = (y1.rent + y1.nnn) / 12;
    var monthlyFixed = (y1.rent + y1.nnn + y1.hourly_labor + y1.manager + y1.utilities + y1.fixed_opex) / 12;
    var lines = [];
    lines.push(["Build-out", buildout]);
    lines.push(["Design, engineering, permits and legal",
                buildout * (site.soft_costs_pct != null ? site.soft_costs_pct : st.soft_costs_pct_of_buildout) / 100]);
    lines.push(["Equipment", equipment]);
    if (site.purchase_price) lines.push(["Purchase of the existing fit-out and lease", site.purchase_price]);
    lines.push(["Furniture and fixtures", site.seats * st.furniture_per_seat + st.furniture_base]);
    lines.push(["Signage", st.signage]);
    lines.push(["Pre-opening payroll and training",
                baseHours * 0.6 * wage * burden * 7 * st.preopening_payroll_weeks
                + managerBase / 52 * (st.manager_preopening_weeks || 0)]);
    lines.push(["Opening inventory", st.opening_inventory]);
    lines.push(["Launch marketing", st.launch_marketing]);
    Object.keys(F.startup_fees || {}).forEach(function (k) { lines.push([k, F.startup_fees[k]]); });
    lines.push(["Security deposit", occMonth * st.deposit_months]);
    lines.push(["Rent and NNN before opening", occMonth * (site.months_to_open || 0)]);
    lines.push(["Contingency", (buildout + equipment) * st.contingency_pct / 100]);
    lines.push(["Working capital reserve", monthlyFixed * st.working_capital_months]);
    var startup = sum(lines.map(function (l) { return l[1]; }));
    var loan = startup * F.fin.loan_share_pct / 100;
    var equity = startup - loan;
    var debt = annualPayment(loan, F.fin.rate_pct, F.fin.term_years);
    years.forEach(function (y) { y.debt_service = debt; y.left = y.ebitda - debt; });

    // Break-even on Year-2 costs, with every channel moving together from where it stands.
    var crewCost = baseHours * wage * burden * days * (1 + op.infl);
    var laborFixed = flexOn ? crewCost * fs : crewCost * (fs + (1 - fs) * R);
    var fixedCash = y2.manager + y2.hired_manager + y2.rent + y2.nnn + y2.utilities + y2.fixed_opex
      + M.fees * (1 + op.infl) + laborFixed;
    var varRate = (goodsPct + varPct + chanPct) / 100 + (flexOn && steady ? crewCost * (1 - fs) * R / steady : 0);
    var breakeven = varRate < 1 ? (fixedCash + debt) / (1 - varRate) : null;
    var target = F.managed ? 0 : (F.owner_pay_target || 0);

    var ceiling = null;
    if (sqft > 0) {
      ceiling = rentPsf + (y2.left - target) / (sqft * (1 + esc));
      ceiling = ceiling <= 0 ? null : Math.min(ceiling, 400);
    }

    return {
      format: fid, site: site.id, days: days, years: years, menu: M, roles: roles,
      base_hours: baseHours, avg_wage: wage, burden: burden, fixed_share: fs, flex: flexOn, volume: R,
      steady_sales: steady, goods_pct: goodsPct, var_pct: varPct, channel_pct: chanPct,
      orders_daily: M.orders, ticket: M.orders ? M.site * pidx / M.orders : 0, hero_daily: M.hero, hands_on_hours: M.hours,
      startup_lines: lines, startup: startup, loan: loan, equity: equity, debt_service: debt,
      rolls_forward: occMonth * st.deposit_months + monthlyFixed * st.working_capital_months,
      breakeven_sales: breakeven, breakeven_vs_steady: breakeven != null && steady ? breakeven / steady : null,
      owner_pay_target: target || null, rent_psf: rentPsf, nnn_psf: nnnPsf, flat_rent: flat, rent_ceiling_psf: ceiling,
      return_on_cash_y2: equity ? y2.left / equity : null,
      payback_years: y3.ebitda > 0 ? startup / y3.ebitda : null,
      sales_per_labor_hour_y2: y2.hours_day ? y2.daily_sales / y2.hours_day : null,
      cash_limit: F.fin.owner_cash_limit || null
    };
  }

  /* Where one lever, moved alone, brings a year's result to `goal`. The model is linear in each lever. */
  function solve(fid, site, S, set, x0, step, n, goal) {
    var at = function (x) { var T = JSON.parse(JSON.stringify(S)); set(T, x); return run(fid, site, T).years[n - 1].left; };
    var a = at(x0), b = at(x0 + step);
    var slope = (b - a) / step;
    if (!isFinite(slope) || Math.abs(slope) < 1e-9) return null;
    return x0 + ((goal || 0) - a) / slope;
  }

  return { run: run, solve: solve, linePrice: linePrice };
}
if (typeof module !== "undefined") module.exports = MiamiModel;
