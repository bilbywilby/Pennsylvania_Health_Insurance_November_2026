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


def main():
    inp = load_inputs()
    res = {
        "C1_trend": c1_trend(inp), "C2_attrition": c2_attrition(inp), "C3_rate_review": c3_rate_review(inp),
        "C4_decomposition": c4_decomposition(inp), "C5_oop": c5_oop(inp), "C6_counties": c6_counties(),
        "C7_race_sum": c7_race(inp),
    }
    out = ROOT / "audit" / "calc_results.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")
    print(json.dumps(res, indent=2, sort_keys=True))
    print(f"\n[OK] wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
