# Review of the submitted draft and correction log

Reviewed 2026-11-08: the pasted draft (2.0_FINAL_VERIFIED), the uploaded `PA_ACA_Geographic_Rating_Areas.txt`, the pasted operational roadmap, and the pasted review notes ("three corrections need attention"). The numbered correction log (items 1-60) was not included in what I received, so this review is of the final text, and every verdict below is keyed to `data/claims_ledger.csv`.

## Verdict on the pasted review notes

| Note | Verdict | Evidence |
|---|---|---|
| Revert "Section 1340" to 1343 | **Agree.** ACA section 1343 is risk adjustment (42 U.S.C. 18063; 45 CFR 153.10 lists "Section 1343. Risk adjustment"). The uploaded file and the roadmap both still say 1340. | L22 |
| $9,200 is not the 2026 limit | **Agree, and it is further off than the note says.** 2026 is $10,600 / $21,200; **2027 is $12,000 / $24,000**. $9,200 appears to be the 2025 limit. The note's remark that the 2026 figure "was later revised again" is not borne out by the sources I found, which give $10,600. | L34 |
| "All citations hyperlinked to primary sources" is overstated | **Agree.** The works-cited list includes an untitled Google Drive link, a rate-review file whose name contains `_UT_` (probably another state's filing), and PY2021 and PY2023 filing PDFs used for PY2027 claims. See `report/` Appendix A for link specificity. | L39-L41 |
| 501,459 - 417,158 = 84,301 and 16.8% | **Arithmetic agrees; inputs do not.** Neither figure is in any source I found. | L05-L07 |
| Trend compounding 8.71% and 12.44% | **Agree** (1.087065 and 1.124374). The draft's 8.66% and 12.22% are wrong. | L10, L11 |
| 7.4%-9.1% "reconciled" | **Agree it is only consistency, and it is worse than that:** unit cost x utilization gives 7.10% to 9.70%, so the range is not reproducible. | L12 |
| 100.3% racial total is a rounding artifact | **Not shown.** Overlap of Hispanic ethnicity with race categories is a likelier explanation, but unrounded values are needed. | L31 |

## Errors in the draft that the notes did not catch

| Severity | Issue | Ledger |
|---|---|---|
| Critical | The headline "PY2027 +16.0% (Requested)" is wrong: PID requested 17.14% and approved 15.97%. The draft predates or ignores PID's September 18 release. | L02 |
| Critical | Peak enrollment 501,459 and exact 417,158 are unsupported; Pennie reports 497,000 (2025 peak) and 486,000 (2026 OE close); about 417,000 in September 2026. | L05, L06 |
| High | "Fully compliant / Verified" audit outcomes with no audit performed. | L21 |
| High | Six-tier crosswalk hierarchy attributed to 45 CFR 155.335(j) does not match the regulation's structure; network-ID matching is CMS guidance. | L26 |
| High | Enhanced APTC described as capping contributions at 8.5% for incomes up to 400% FPL; the enhancement removed the 400% cutoff. | L13 |
| High | Gross rate increase conflated with net premium change (PID gross 21.5%; Pennie net about 102% for retained enrollees). | L14 |
| Medium | Section 4 of the calculations sums drivers additively after Section 1 argued for compounding; "aligns with 16.0%" never computed. | L15 |
| Medium | Carrier names per rating area do not match PID entity names ("Highmark Care Benefits", "Highmark Health Insurance Co."). | L19 |
| Medium | Historical rate table PY2017-PY2025 unsourced; PY2019 attributed to the reinsurance waiver, which is reported as starting in PY2021. | L28 |
| Medium | Roadmap phases dated Q1-Q3 2026 are written as future actions though the dates have passed. | L36 |
| Medium | KRI formulas are blank in the submitted file. | L37 |
| Medium | The KRI trigger "increase above 10%" fires for 11 of 14 carriers on average, so it does not select anyone. | L45 |
| Low | ">80% subsidized" should be "about 80% (four in five)". | L33 |

## Prior-project items corrected by this pass

- Highmark Benefits Group 21.40% and Geisinger Health Plan 10.46% were labelled as 2026 verified figures; they are PY2027 requested rates (X06, X07).
- The status report's PY2026 per-carrier table lists Partners both -10.1% and 20.5%; 20.5% equals the PY2027 request (X08). Do not use that table for carrier-level year-over-year claims.
- The area reports said final 2027 rates were expected in fall 2026; they were approved September 18.

## What was confirmed

- County totals 67 and nine areas (L17).
- 45 CFR 155.335(j) exists and is the re-enrollment paragraph (L25).
- PID's carrier-level requested and approved rates, statewide averages and $94.7 million denial (L02-L04), re-read in full from the PID release on 2026-11-08.
- Open enrollment November 1, 2026 to January 15, 2027 (L35).

## Not done

- No SERFF filing or actuarial memorandum was opened.
- The CMS 2027 cost-sharing guidance PDF was not fetched (cited through secondary sources).
- The enhanced-credit contribution caps (L13) were not re-sourced; the correction rests on general knowledge and should be confirmed before publication.

## Second batch (received 2026-11-11): three pasted items

### "Working Draft for Reconciliation" (editorial source: usable)

- **Matches PID.** Requested 17.14% and approved 15.97% individual, 11.49% and 10.28% small group; it correctly says the "approximately 16.0%" figure is the approved rate (L48).
- **Correct on §1343 / 42 U.S.C. 18063** (L53) and on the trend range 8.71% to 12.44%.
- **Arithmetic slips:** it prints the low-case product as 0.087113 (should be 0.087065) and the midpoint as 10.58% (10.57% unrounded) (L46, L47).
- **115,336 CSR enrollees is 23% x 501,459 = 115,335.57**, so it is derived, not an independent count (L50, calculation C9). The plan-mix shares and the 46,000 rural gap have no source (L49, L51).
- **Adopted into the beta:** acronyms and definitions, the regulatory table, and Appendices A to D (here C to F).

### "Geographic Rating Area Summaries" (quarantined: do not use)

- Rating-area names and counties are wrong for Areas 2, 3, 4, 5, 6, 7 and 9 (for example it calls Area 2 "Pittsburgh"; Pittsburgh is Area 4, and Area 2 is Cameron, Elk and Potter) (L55).
- Three carrier rates are wrong: Keystone Health Plan East 19.7% (PID 16.0%), Jefferson/Partners 18.4% (18.8%), Highmark Inc 10.7% (14.5%) (L56).
- It says rating-area premium differences reflect population morbidity (L57) and gives a risk-adjustment "transfer by rating area" formula (L58); both are wrong.
- Its per-area ranges omit carriers (L59). Replaced by `report/rating_area_summaries.md` and the nine one-pagers.

### "Repository reconciliation" overview (not used)

- It says the remote contains "token/credential dumps". The owner's `git grep` of origin/main for token, private-key and AWS-key patterns returned nothing, so the claim is unsupported (L60). That is not an all-clear: review the removed files before deciding anything about history.
- Its file checklist matches this packet's layout, which is the only useful part.

