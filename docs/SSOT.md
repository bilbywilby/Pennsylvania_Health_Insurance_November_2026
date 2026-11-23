# Single source of truth map

Rule: every fact lives in exactly one authoritative file. Everything else (report text, summaries, tables) is derived and is checked against it by `scripts/validate_packet.py`. If two files disagree, the authoritative file wins and the other is a bug.

| Fact | Authoritative file | Derived or checked in | Tier |
|---|---|---|---|
| PY2027 carrier requested and approved rates | `data/public/py2027_individual_rates_pid_2026-09-18.csv` | `report/PA_ACA_Forensic_Audit_PY2027_November_2026.md`, `report/rating_area_summaries.md` | VERIFIED |
| PY2027 statewide averages, denied dollars | `data/public/py2027_statewide_pid_2026-09-18.csv` | report section 3.1 | VERIFIED |
| County to rating area (67 counties, 9 areas) | `data/public/pa_county_fips_crosswalk.json` | `data/public/rating_area_counties.csv`, all area tables | CARRIED |
| Carrier footprint by rating area | `data/public/py2027_carrier_footprint_by_area.csv` | `data/public/py2027_area_rate_ranges.csv` | CARRIED |
| Enrollment counts | `data/public/enrollment_series.csv` | report section 3.3 and calculation C2 | SECONDARY / CARRIED |
| Calculation inputs | `data/public/calc_inputs.json` | `audit/calc_results.json` (generated), report section 4 | mixed (per input) |
| Cost-sharing limits | `data/public/oop_limits.csv` | report section 3.5, calculation C5 | SECONDARY |
| Key dates (open enrollment etc.) | `data/public/key_dates.csv` | `templates/consumer_open_enrollment_2027.md` | SECONDARY |
| Verified and excluded citations | `data/statutes_2026.json` | `docs/source_reliability.md` | CARRIED / VERIFIED |
| Status of every claim from the submitted draft | `data/claims_ledger.csv` | `report/REVIEW_OF_SUBMITTED_DRAFT.md` | per row |
| Disagreements between sources | `audit/conflicts_register.csv` | report limitations | per row |
| Monthly audit state | `audit/monthly_audit_2026-11.json` | `HANDOVER.json` (action items) | per field |
| Sources, links and tiers | `data/public/source_inventory.csv` | report references, appendix D | per row |
| Release version | `VERSION` | README, CHANGELOG, report header, `HANDOVER.json` | n/a |
| Plan ID crosswalk test results | `audit/crosswalk_test_log_template.csv` (header only; no cases run) | report appendix F | n/a |

## Generated files (never edit by hand)

`audit/calc_results.json` and `audit/calc_schedule.csv` (from `scripts/calc_audit.py`), `report/rating_area_summaries.md`, `report/one_pagers/rating_area_1.md` to `rating_area_9.md` and `data/public/py2027_area_rate_ranges.csv` (from `scripts/build_area_tables.py`), `HANDOVER.json` (from `scripts/generate_handover.py`), `MANIFEST.sha256` (from `scripts/hash_manifest.py`). CI fails if regenerating them changes the committed files.

## Update procedure

1. Edit the authoritative file only.
2. `python3 scripts/calc_audit.py && python3 scripts/build_area_tables.py && python3 scripts/generate_handover.py`
3. Update report wording that quotes changed numbers; `python3 scripts/validate_packet.py` fails if a quoted figure no longer matches.
4. `python3 scripts/06_provenance_gate.py && python3 -m unittest discover -s tests`
5. Bump `VERSION`, the CHANGELOG heading, the README and report headers, and `AS_OF` in `scripts/generate_handover.py` when cutting a release.
6. `python3 scripts/hash_manifest.py` (always last), then commit.
