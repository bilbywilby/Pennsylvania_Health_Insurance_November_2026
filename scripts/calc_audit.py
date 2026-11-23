#!/usr/bin/env python3
"""calc_audit.py - reproduces every calculation in the November 2026 report.

Inputs : data/public/calc_inputs.json, py2027_individual_rates_pid_2026-09-18.csv,
         pa_county_fips_crosswalk.json
Outputs: audit/calc_results.json (machine-readable) and a printed summary.
Uses Decimal so every figure is exactly reproducible. Run from the repo root:
    python3 scripts/calc_audit.py
"""
import csv
import json
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "data" / "public"


def q(x, places="0.01"):
    return D(x).quantize(D(places), rounding=ROUND_HALF_UP)


def pct(x):
    return q(D(x) * 100)


def compound(rates_pct):
    f = D(1)
    for r in rates_pct:
        f *= 1 + D(str(r)) / 100
    return f


def load_inputs():
    return json.loads((PUB / "calc_inputs.json").read_text())


def c1_trend(inp):
    t = inp["trend_components_pct"]
    out = {}
    for label, i in (("low", 0), ("high", 1)):
        parts = [t["unit_cost"][i], t["utilization"][i], t["morbidity"][i]]
        f = compound(parts)
        trend_only = compound(parts[:2])
        out[label] = {
            "components_pct": parts,
            "compound_factor": str(f.quantize(D("0.000000001"))),
            "compound_pct": str(pct(f - 1)),
            "additive_pct": str(q(sum(D(str(p)) for p in parts))),
            "trend_only_factor": str(trend_only.quantize(D("0.000000001"))),
            "trend_only_pct_ex_morbidity": str(pct(trend_only - 1)),
        }
    return out


def c2_attrition(inp):
    out = {}
    for name, s in inp["enrollment_series"].items():
        b, c = D(s["baseline"]), D(s["current"])
        out[name] = {
            "baseline": s["baseline"], "current": s["current"],
            "net_loss": int(b - c),
            "attrition_pct": str(pct((b - c) / b)),
            "K": str(((c / b)).quantize(D("0.0001"), rounding=ROUND_HALF_UP)),
            "K_below_0_85_trigger": bool(c / b < D(str(inp["kri"]["k_trigger"]))),
            "K_below_0_92_target": bool(c / b < D(str(inp["kri"]["k_target"]))),
        }
    return out


def read_rates():
    rows = []
    with open(PUB / "py2027_individual_rates_pid_2026-09-18.csv", newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def c3_rate_review(inp):
    rows = read_rates()
    carriers = []
    for r in rows:
        req, app = D(r["requested_pct"]), D(r["approved_pct"])
        carriers.append({
            "carrier": r["carrier_pid_name"], "requested": str(req), "approved": str(app),
            "delta_pp": str(app - req),
            "premium_level_change_vs_request_pct": str(pct((1 + app / 100) / (1 + req / 100) - 1)),
        })
    up = [c["carrier"] for c in carriers if D(c["delta_pp"]) > 0]
    over10 = [c["carrier"] for c in carriers if D(c["approved"]) > D(str(inp["kri"]["delta_p_cross_trigger_pct"]))]
    st = {"ind_req": D("17.14"), "ind_app": D("15.97"), "sg_req": D("11.49"), "sg_app": D("10.28")}
    return {
        "carriers": carriers,
        "n_carriers": len(carriers),
        "raised_after_review": up,
        "approved_over_10pct": over10,
        "n_approved_over_10pct": len(over10),
        "statewide_individual": {
            "delta_pp": str(st["ind_app"] - st["ind_req"]),
            "share_of_requested_increase_removed_pct": str(pct((st["ind_req"] - st["ind_app"]) / st["ind_req"])),
            "premium_level_vs_request_pct": str(pct((1 + st["ind_app"] / 100) / (1 + st["ind_req"] / 100) - 1)),
        },
        "statewide_small_group": {"delta_pp": str(st["sg_app"] - st["sg_req"])},
        "cumulative_py2026_py2027_individual_pct_illustrative": str(
            pct((1 + D(str(inp["py2026_approved_weighted_avg_pct"])) / 100) * (1 + st["ind_app"] / 100) - 1)
        ),
    }


def c4_decomposition(inp):
    d = inp["driver_decomposition_pct_illustrative_unsourced"]
    lo = [v[0] for v in d.values()]
    hi = [v[1] for v in d.values()]
    add_lo, add_hi = sum(D(str(x)) for x in lo), sum(D(str(x)) for x in hi)
    cmp_lo, cmp_hi = pct(compound(lo) - 1), pct(compound(hi) - 1)
    return {
        "additive_low": str(add_lo), "additive_high": str(add_hi), "additive_mid": str((add_lo + add_hi) / 2),
        "compound_low": str(cmp_lo), "compound_high": str(cmp_hi), "compound_mid": str((cmp_lo + cmp_hi) / 2),
        "pid_requested": "17.14", "pid_approved": "15.97",
        "requested_inside_compound_range": bool(cmp_lo <= D("17.14") <= cmp_hi),
        "approved_inside_compound_range": bool(cmp_lo <= D("15.97") <= cmp_hi),
    }


def c5_oop(inp):
    o = inp["oop"]
    return {
        "self_only_change_pct": str(pct(D(o["y2027"]) / D(o["y2026"]) - 1)),
        "family_change_pct": str(pct(D(o["family_2027"]) / D(o["family_2026"]) - 1)),
        "bronze_cap_130pct_usd": str(int(D(o["y2027"]) * D(str(o["bronze_multiplier"])))),
        "family_is_2x_self_only": o["family_2027"] == 2 * o["y2027"],
    }


def c6_counties():
    xw = json.loads((PUB / "pa_county_fips_crosswalk.json").read_text())
    sizes = {k: len(v) for k, v in xw.items()}
    allc = [c["county"] for v in xw.values() for c in v]
    return {"by_area": sizes, "total": sum(sizes.values()), "unique": len(set(allc)), "areas": len(xw)}


def c7_race(inp):
    return {"sum_pct": str(sum(D(str(v)) for v in inp["race_ethnicity_pct_draft"].values()))}


def c8_metal(inp):
    shares = inp["metal_tier_projection_pct_draft"]
    total = sum(D(str(v)) for v in shares.values())
    return {"n_tiers": len(shares), "sum_pct": str(total), "is_100": total == D("100")}


def c9_csr(inp):
    c = inp["csr_draft"]
    prod = D(c["reported_share_pct"]) / 100 * D(c["reference_enrollment"])
    share = D(c["reported_count"]) / D(c["reference_enrollment"]) * 100
    return {
        "product": str(prod.quantize(D("0.01"))), "product_rounded": str(prod.quantize(D("1"), rounding=ROUND_HALF_UP)),
        "reported_count": c["reported_count"], "difference": str((D(c["reported_count"]) - prod).quantize(D("0.01"))),
        "implied_share_pct": str(share.quantize(D("0.01"))),
        "matches_derivation_within_1": bool(abs(D(c["reported_count"]) - prod) < 1),
    }


def schedule(res, inp):
    t, a, r3 = res["C1_trend"], res["C2_attrition"], res["C3_rate_review"]
    rows = []

    def add(i, name, formula, inputs, result, tier, note=""):
        rows.append([i, name, formula, inputs, result, tier, note])
    for k in ("low", "high"):
        add("C1-" + k, "Composite medical cost trend (" + k + ")", "(1+c)(1+u)(1+m)-1",
            "c,u,m = " + ", ".join(str(x) + "%" for x in t[k]["components_pct"]), t[k]["compound_pct"] + "%", "UNVERIFIED",
            "assumed component ranges from the submitted draft; additive " + t[k]["additive_pct"] + "%; cost x utilization only " + t[k]["trend_only_pct_ex_morbidity"] + "%")
    for k, v in a.items():
        add("C2-" + k.split("_")[0], "Enrollment attrition", "net=base-current; pct=net/base; K=current/base",
            "base=%s, current=%s" % (v["baseline"], v["current"]), "net=%s; %s%%; K=%s" % (v["net_loss"], v["attrition_pct"], v["K"]),
            "UNVERIFIED" if k.startswith("A") else "SECONDARY", "K<0.85 trigger: %s" % v["K_below_0_85_trigger"])
    s = r3["statewide_individual"]
    add("C3-statewide", "Requested to approved, individual market", "a-r; (1+a)/(1+r)-1; (r-a)/r", "r=17.14%, a=15.97%",
        "%s pp; %s%%; %s%%" % (s["delta_pp"], s["premium_level_vs_request_pct"], s["share_of_requested_increase_removed_pct"]), "VERIFIED", "PID 2026-09-18")
    add("C3-over10", "Carriers approved above 10%", "count(approved>10)", "14 PID carriers", "%d of %d" % (r3["n_approved_over_10pct"], r3["n_carriers"]), "VERIFIED", "")
    add("C3-cumulative", "Cumulative PY2026 and PY2027 (illustrative)", "(1+0.215)(1+0.1597)-1", "21.5%, 15.97%",
        r3["cumulative_py2026_py2027_individual_pct_illustrative"] + "%", "SECONDARY", "different enrollment mixes; gross, not net")
    d4 = res["C4_decomposition"]
    add("C4-additive", "Driver scenario, additive", "sum of ranges", "8-9, 1.5-2.5, 3-4, 1-2 (%)", "%s%% to %s%% (mid %s%%)" % (d4["additive_low"], d4["additive_high"], d4["additive_mid"]), "UNVERIFIED", "illustrative")
    add("C4-compound", "Driver scenario, compounded", "product of (1+x)-1", "same ranges", "%s%% to %s%% (mid %s%%)" % (d4["compound_low"], d4["compound_high"], d4["compound_mid"]), "UNVERIFIED", "illustrative")
    o = res["C5_oop"]
    add("C5-change", "Cost-sharing limit change 2026 to 2027", "12000/10600-1", "10,600 and 12,000 USD", o["self_only_change_pct"] + "%", "SECONDARY", "family 21,200 to 24,000 gives the same %")
    add("C5-bronze", "Bronze cap at 130%", "1.30 x 12000", "12,000 USD", o["bronze_cap_130pct_usd"] + " USD", "SECONDARY", "")
    c6 = res["C6_counties"]
    add("C6", "County total", "sum of counties by area", "crosswalk JSON", "%d counties, %d unique, %d areas" % (c6["total"], c6["unique"], c6["areas"]), "CARRIED", "")
    add("C7", "Demographic percentage sum", "sum of categories", "65, 7.4, 3.6, 3.3, 21", res["C7_race_sum"]["sum_pct"], "UNVERIFIED", "draft table; no source")
    c8 = res["C8_metal"]
    add("C8", "Plan-mix sum", "sum of tier shares", "1.5, 47.8, 13.0, 21.5, 15.4, 0.8", c8["sum_pct"], "UNVERIFIED", "arithmetic only; shares unsourced")
    c9 = res["C9_csr"]
    add("C9", "CSR enrollee count versus 23% of 501,459", "0.23 x 501459", "23%, 501,459, reported 115,336", "%s (rounds to %s; diff %s)" % (c9["product"], c9["product_rounded"], c9["difference"]), "UNVERIFIED", "count equals the percentage times an unverified base, so it is not independent")
    return rows


def main():
    inp = load_inputs()
    res = {
        "C1_trend": c1_trend(inp), "C2_attrition": c2_attrition(inp), "C3_rate_review": c3_rate_review(inp),
        "C4_decomposition": c4_decomposition(inp), "C5_oop": c5_oop(inp), "C6_counties": c6_counties(),
        "C7_race_sum": c7_race(inp),
        "C8_metal": c8_metal(inp), "C9_csr": c9_csr(inp),
    }
    out = ROOT / "audit" / "calc_results.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")
    with open(ROOT / "audit" / "calc_schedule.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "calculation", "formula", "inputs", "result", "input_tier", "note"])
        w.writerows(schedule(res, inp))
    print(json.dumps(res, indent=2, sort_keys=True))
    print(f"\n[OK] wrote {out.relative_to(ROOT)} and audit/calc_schedule.csv")


if __name__ == "__main__":
    main()
