# Source reliability register

Status date: 2026-11-08. This file and `data/statutes_2026.json` are the only places where excluded citations may be written out (they are exempt in `scripts/06_provenance_gate.py`).

## Excluded citations (do not use)

| Citation | Why excluded |
|---|---|
| SB 1071 | A real bill number, but not a health insurance bill. The 2023-24 bill is an appropriation for a university per the 2026-10-09 triage. Earlier project notes called it a police-conduct bill; that description should not be repeated. |
| Act 252-2023 | Not found in official records. Only a few dozen bills became law in 2023, so the number is implausible. |
| § 28-725 and § 29-8719 | Not valid Insurance Code citation formats. Managed-care provisions are in Article XXI of the Insurance Company Law of 1921. |
| Bulletin #23-04 | PID Notice 2023-04 concerns Medicare Supplement guaranteed issue. |
| Geisinger HMO at 9.68% | Fabricated. See the rate tables for real Geisinger figures. |
| Flex Blue PPO | Plan name does not exist. |

## Year-label hazard (new, 2026-11-08)

Two figures that earlier project notes treated as verified are **PY2027 requested** rates, not PY2026 approved rates:

- Highmark Benefits Group 21.40%: PID's 2026-09-18 release lists 21.4% as the PY2027 *request* (approved 19.7%). The August 2026 status report lists 21.0% as the PY2026 approved rate.
- Geisinger Health Plan 10.46%: PID lists 10.5% as the PY2027 request (approved 8.6%). The August 2026 status report lists 11.6% as the PY2026 approved rate.

Always write the plan year and the word requested or approved next to every rate.

## Quarantined documents (standing quarantine)

- "Cross-Sectional Metadata Analysis" (RTF and PDF; project file `PA_Health_Insurance_Audit_Analysis.pdf`): contains county-to-rating-area mappings that disagree with CMS (for example, it places Allegheny in Rating Area 1 and lists 17 counties there) and invented plan names. Its rating-area tables, carrier tables and "Works cited" are not used anywhere in this packet.
- `stage2-analysis-dashboard.jsx` inherits carrier-to-area assignments from that document; do not publish its per-area averages.

## Sources that are not primary

| Source | Treatment |
|---|---|
| Google Drive links in a works-cited list | Not a source. Remove. |
| A rate-review file whose name contains `_UT_` (cited in the submitted draft) | Appears to be another state's actuarial memorandum. Do not cite for Pennsylvania unless the issuer and state are confirmed. |
| PY2021 and PY2023 small-group filing PDFs | Wrong plan year for PY2027 claims. |
| Wire reprints (InsuranceNewsNet, States News Service) | SECONDARY. Use only with the original publisher named; replace with the primary document when located. |
