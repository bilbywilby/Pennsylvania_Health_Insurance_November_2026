## [Unreleased - 2026-11-23]

- Added `2026-10-01` Pennie enrollment row (`406984`, tier `SECONDARY`) to `data/public/enrollment_series.csv`.
- Rebuilt `report/rating_area_summaries.md` and `data/public/py2027_area_rate_ranges.csv` via `scripts/build_area_tables.py`.
- Recomputed `audit/calc_results.json` via `scripts/calc_audit.py` and re-verified `validate_packet.py`, `06_provenance_gate.py`, and `pytest`.

# Changelog

## 3.0.0 - 2026-11-08

- Added: PID's September 18, 2026 approved 2027 rates (14 individual-market entities, statewide and small-group averages, $94.7M denied).
- Added: reproducible calculations (`scripts/calc_audit.py`) with Decimal arithmetic and unit tests.
- Added: 45-row claims ledger, conflicts register, source-reliability register, per-area summaries, consumer open-enrollment checklist, monthly audit JSON.
- Changed: report rewritten in APA 7 with evidence tiers; calculations in separate subsections.
- Corrected: PY2027 "requested 16.0%" (approved 15.97%, requested 17.14%); trend compounding 8.71% / 12.44%; ACA section 1343 (not 1340); 2027 cost-sharing limit $12,000 / $24,000 (not $9,200); open enrollment dates.
- Withdrawn: 501,459 and 417,158 enrollment figures, six-tier crosswalk hierarchy, compliance conclusions, historical rate table, demographic table.
