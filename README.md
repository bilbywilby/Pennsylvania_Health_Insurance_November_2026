# Pennsylvania Health Insurance, November 2026 audit packet

Public-interest audit of Pennsylvania's ACA individual and small-group markets for Plan Year 2027. Status date **2026-11-08**. Repository: <https://github.com/bilbywilby/Pennsylvania_Health_Insurance_November_2026>

## Headline findings (details and sources in the report)

- PID approved 2027 rates on 2026-09-18: individual **+15.97%** (requested 17.14%), small group **+10.28%** (requested 11.49%); **$94.7M** in requested increases denied.
- 11 of 14 individual carriers were approved above 10%; three were approved above their request (Health Partners Plans, Keystone Health Plan East, QCC).
- Open enrollment runs **Nov 1, 2026 to Jan 15, 2027**; enroll by **Dec 15** for Jan 1 coverage.
- The submitted draft's "requested 16.0%", "501,459" and "417,158" are not supported by sources. See `report/REVIEW_OF_SUBMITTED_DRAFT.md`.

## Layout

| Path | Contents |
|---|---|
| `report/PA_ACA_Forensic_Audit_PY2027_November_2026.md` | APA 7 report with calculation subsections C1-C7 |
| `report/REVIEW_OF_SUBMITTED_DRAFT.md` | Proofread and correction log |
| `report/rating_area_summaries.md` | Nine per-area tables (generated) |
| `templates/consumer_open_enrollment_2027.md` | Patient-facing checklist |
| `data/public/` | Crosswalk (single source of truth), PID rates, footprints, enrollment, key dates, limits, calc inputs |
| `data/claims_ledger.csv` | Every claim from the draft with an evidence tier |
| `data/statutes_2026.json`, `docs/source_reliability.md` | Verified and excluded citations; quarantined sources |
| `audit/` | Monthly audit JSON, conflicts register, calculation results |
| `scripts/` | `calc_audit.py`, `build_area_tables.py`, `validate_packet.py`, `hash_manifest.py`, `06_provenance_gate.py`, `push_to_github.sh` |
| `tests/test_packet.py` | Unit tests (stdlib `unittest`) |

## Evidence tiers

VERIFIED (primary read this pass) / SECONDARY (credible reporting) / CARRIED (earlier project work, not re-checked) / UNVERIFIED / CONTRADICTED / NOT_FOUND. A clean validator or gate run means nothing known is contaminated, **not** that every figure is confirmed.

## Run

```bash
python3 scripts/calc_audit.py          # recomputes audit/calc_results.json
python3 scripts/build_area_tables.py   # regenerates area tables
python3 scripts/validate_packet.py     # structure, tiers, report/number consistency
python3 scripts/06_provenance_gate.py  # stray-paste / duplicate-crosswalk / excluded-citation gate
python3 -m unittest discover -s tests -v
python3 scripts/hash_manifest.py       # writes MANIFEST.sha256
```

## Publish

```bash
sh scripts/push_to_github.sh
```

The script validates first and does not use `git clean` or `git reset`. If your global hooks path still emits the known `grep: Invalid range end` error, fix that first (see the handover notes); the push script does not bypass hooks.

## Known open items

See `audit/monthly_audit_2026-11.json` (`action_items`) and `audit/conflicts_register.csv`.
