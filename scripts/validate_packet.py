#!/usr/bin/env python3
"""validate_packet.py - structural and consistency checks for the November 2026 packet.

Exit 0 = all checks passed; exit 1 = at least one failure. This checks internal consistency
and tiering discipline. It does NOT verify any figure against a primary source.
"""
import csv
import json
import re
import sys
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "data" / "public"
TIERS = {"VERIFIED", "SECONDARY", "CARRIED", "UNVERIFIED", "CONTRADICTED", "NOT_FOUND"}
FAILS, WARNS = [], []


def fail(msg):
    FAILS.append(msg)


def warn(msg):
    WARNS.append(msg)


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_crosswalk():
    xw = json.loads((PUB / "pa_county_fips_crosswalk.json").read_text())
    names = [c["county"] for v in xw.values() for c in v]
    fips = [c["fips"] for v in xw.values() for c in v]
    if len(xw) != 9:
        fail(f"crosswalk has {len(xw)} areas, expected 9")
    if len(names) != 67 or len(set(names)) != 67:
        fail(f"crosswalk has {len(names)} counties ({len(set(names))} unique), expected 67")
    if len(set(fips)) != 67 or not all(re.fullmatch(r"42\d{3}", x) for x in fips):
        fail("crosswalk FIPS codes are not 67 unique 42xxx values")
    csv_rows = rows(PUB / "rating_area_counties.csv")
    if len(csv_rows) != 67:
        fail(f"rating_area_counties.csv has {len(csv_rows)} rows")
    csv_map = {r["county"]: r["rating_area"] for r in csv_rows}
    for a, v in xw.items():
        for c in v:
            if csv_map.get(c["county"]) != a:
                fail(f"CSV/JSON disagree for {c['county']}")


def check_tiers_and_urls():
    for p in list(PUB.glob("*.csv")) + [ROOT / "data" / "claims_ledger.csv"]:
        rs = rows(p)
        if not rs or "tier" not in rs[0]:
            continue
        for i, r in enumerate(rs, start=2):
            t = r["tier"]
            if t not in TIERS:
                fail(f"{p.name}:{i} invalid tier {t!r}")
            url_col = "source_url" if "source_url" in r else None
            if t == "VERIFIED" and url_col and not r[url_col] and p.name != "claims_ledger.csv":
                fail(f"{p.name}:{i} VERIFIED row without source_url")


def check_rates():
    rs = rows(PUB / "py2027_individual_rates_pid_2026-09-18.csv")
    if len(rs) != 14:
        fail(f"expected 14 PID carriers, found {len(rs)}")
    for r in rs:
        D(r["requested_pct"])
        D(r["approved_pct"])
        if r["tier"] != "VERIFIED":
            fail(f"rate row {r['carrier_pid_name']} is not VERIFIED")
    st = {(r["market"], r["metric"]): D(r["value"]) for r in rows(PUB / "py2027_statewide_pid_2026-09-18.csv")}
    if st[("individual", "approved_weighted_avg")] != D("15.97"):
        fail("statewide individual approved != 15.97")
    if st[("individual", "requested_weighted_avg")] != D("17.14"):
        fail("statewide individual requested != 17.14")
    names = {r["carrier_pid_name"] for r in rs}
    for r in rows(PUB / "py2027_carrier_footprint_by_area.csv"):
        n = r["pid_release_name"]
        if n and n not in names:
            fail(f"footprint maps to unknown PID name {n!r}")


def check_report_numbers():
    rep = (ROOT / "report" / "PA_ACA_Forensic_Audit_PY2027_November_2026.md").read_text()
    calc = json.loads((ROOT / "audit" / "calc_results.json").read_text())
    must = [
        calc["C1_trend"]["low"]["compound_pct"] + "%", calc["C1_trend"]["high"]["compound_pct"] + "%",
        calc["C2_attrition"]["A_draft"]["attrition_pct"] + "%", calc["C2_attrition"]["A_draft"]["K"],
        calc["C2_attrition"]["B_peak2025_to_sep2026"]["attrition_pct"] + "%",
        calc["C2_attrition"]["C_oe_close_to_sep2026"]["attrition_pct"] + "%",
        calc["C3_rate_review"]["statewide_individual"]["share_of_requested_increase_removed_pct"] + "%",
        calc["C3_rate_review"]["cumulative_py2026_py2027_individual_pct_illustrative"] + "%",
        calc["C5_oop"]["self_only_change_pct"] + "%", "$" + f"{int(calc['C5_oop']['bronze_cap_130pct_usd']):,}",
        calc["C7_race_sum"]["sum_pct"], "15.97", "17.14", "1343", "$12,000", "$24,000",
        calc["C4_decomposition"]["compound_low"] + "%", calc["C4_decomposition"]["compound_high"] + "%",
    ]
    for s in must:
        if s not in rep:
            fail(f"report is missing expected value {s!r}")
    if "11 of 14" not in rep:
        fail("report missing '11 of 14' (carriers approved above 10%)")
    if calc["C3_rate_review"]["n_approved_over_10pct"] != 11:
        fail("calc results: expected 11 carriers over 10%")
    if calc["C6_counties"]["total"] != 67:
        fail("calc results: county total != 67")
    for bad in ("drive.google.com",):
        for p in (ROOT / "report").glob("*.md"):
            if bad in p.read_text():
                fail(f"{p.name} contains non-primary link host {bad}")
    if re.search(r"\(Requested\)", rep):
        fail("report still labels a rate '(Requested)' in a table header")


def check_json():
    for p in (ROOT / "audit" / "monthly_audit_2026-11.json", ROOT / "data" / "statutes_2026.json",
              PUB / "calc_inputs.json", ROOT / "audit" / "calc_results.json"):
        try:
            json.loads(p.read_text())
        except Exception as e:  # noqa: BLE001
            fail(f"{p.name}: invalid JSON ({e})")


def main():
    for fn in (check_crosswalk, check_tiers_and_urls, check_rates, check_report_numbers, check_json):
        try:
            fn()
        except Exception as e:  # noqa: BLE001
            fail(f"{fn.__name__} raised {type(e).__name__}: {e}")
    for w in WARNS:
        print("[WARN]", w)
    if FAILS:
        print("=== VALIDATION FAILED ===")
        for f in FAILS:
            print("[FAIL]", f)
        return 1
    print("[OK] packet validation passed (consistency only; not a source verification)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
