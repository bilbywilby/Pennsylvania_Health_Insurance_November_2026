# Pennsylvania ACA Individual and Small Group Market, Plan Year 2027: Forensic Audit Report, November 2026 Update

**Ez_Insurance Pennsylvania Health Insurance Public Information Campaign**

November 8, 2026 | Version 3.0 (supersedes draft 2.0_FINAL_VERIFIED) | Repository: <https://github.com/bilbywilby/Pennsylvania_Health_Insurance_November_2026>

---

## Abstract

This report updates the Plan Year 2027 (PY2027) audit of Pennsylvania's ACA individual and small group markets after the Pennsylvania Insurance Department (PID) approved 2027 rates on September 18, 2026. PID approved an average individual-market increase of 15.97%, down from 17.14% requested, and a small-group increase of 10.28%, down from 11.49%, and reported denying $94.7 million in premium increases ([PID, 2026a](https://www.pa.gov/agencies/insurance/newsroom/pennsylvania-releases-aca-2027-health-insurance-rates)). Three carriers received higher approved than requested rates, and 11 of 14 individual-market carriers were approved above 10%. Pennie enrollment fell from a 2025 peak of about 497,000 to about 417,000 by September 2026. The previous draft's figures of 501,459 and 417,158 could not be verified, and its "requested 16.0%" was in fact the approved rate. All calculations are reproduced in separate subsections and by `scripts/calc_audit.py`. Every claim carries an evidence tier; unverified items are listed in `data/claims_ledger.csv` rather than presented as findings.

*Keywords:* Pennsylvania, Pennie, ACA marketplace, rate review, rating areas, open enrollment, risk pool

---

## 1. Introduction and scope

The audit covers the individual and small-group ACA markets regulated by PID and the individual marketplace run by Pennie, Pennsylvania's state-based exchange. It addresses rate review outcomes, rating-area structure, enrollment, 2027 open enrollment, cost-sharing limits and re-enrollment rules. It does not audit actuarial memoranda or Unified Rate Review Template (URRT) exhibits; where earlier drafts asserted compliance, this report removes the assertion (see Limitations).

Today is November 8, 2026, so Pennie's 2027 open enrollment (OE) is already under way. Phases of the earlier roadmap that were dated Q1 to Q3 2026 are now retrospective.

## 2. Method and evidence tiers

Every data row and claim is tagged with one of the tiers below. Only VERIFIED items, and items labelled with the tier shown, may appear in public text.

| Tier | Meaning |
|---|---|
| VERIFIED | Primary document retrieved and read on 2026-11-08 |
| SECONDARY | Credible outlet or association reporting retrieved 2026-11-08; primary not located or not fetched |
| CARRIED | From earlier project verification or project files; not re-checked this pass |
| UNVERIFIED | No source located; must be bracketed |
| CONTRADICTED | A retrieved source disagrees |
| NOT_FOUND | Searched for and not located as of the date shown |

Excluded citations and quarantined documents are listed in `docs/source_reliability.md`. Rating-area county membership comes from the project's CMS-based crosswalk (`data/public/pa_county_fips_crosswalk.json`, CARRIED); the quarantined cross-sectional analysis is not used.

## 3. Results

### 3.1 PY2027 rate review outcome (VERIFIED)

PID's September 18, 2026 release lists requested and approved average increases for 14 individual-market entities ([PID, 2026a](https://www.pa.gov/agencies/insurance/newsroom/pennsylvania-releases-aca-2027-health-insurance-rates)). Differences are derived in Calculation C3.

| Carrier (PID name) | Requested % | Approved % | Change (pp) |
|---|---:|---:|---:|
| Ambetter Health of Pennsylvania Inc | 40.9 | 35.1 | -5.8 |
| Capital Advantage Assurance Company | 18.3 | 14.8 | -3.5 |
| Geisinger Health Plan | 10.5 | 8.6 | -1.9 |
| Geisinger Quality Options | 13.0 | 10.7 | -2.3 |
| Health Partners Plans Inc | 15.9 | 18.3 | +2.4 |
| Highmark Benefits Group | 21.4 | 19.7 | -1.7 |
| Highmark Inc | 16.2 | 14.5 | -1.7 |
| Keystone Health Plan Central | 33.8 | 33.4 | -0.4 |
| Keystone Health Plan East | 14.7 | 16.0 | +1.3 |
| Oscar Health Plan of PA | 15.4 | 1.4 | -14.0 |
| Partners Insurance Company Inc | 20.5 | 18.8 | -1.7 |
| QCC Insurance Company | 19.9 | 21.3 | +1.4 |
| UPMC Health Network Inc | 12.0 | 9.7 | -2.3 |
| UPMC Health Plan Inc | 15.8 | 13.5 | -2.3 |
| **Individual market, weighted average** | **17.14** | **15.97** | **-1.17** |
| **Small group, weighted average** | **11.49** | **10.28** | **-1.21** |

*Note.* Source: PID (2026a). PID attributed the higher approved rates for Health Partners Plans to less healthy membership confirmed through federal risk adjustment, and for Keystone Health Plan East and QCC to worsening medical and drug trends. These are average changes; individual premiums vary by age, location, plan and subsidy. Per-carrier small-group approved rates were not retrieved.

PID also stated that individual and small-group insurers paid $845 million more in 2025 medical and prescription drug claims than in 2024, a 13% increase, and cited the lapse of enhanced premium tax credits and the Medicaid and enrollment changes in H.R. 1 as added pressure on the market ([PID, 2026a](https://www.pa.gov/agencies/insurance/newsroom/pennsylvania-releases-aca-2027-health-insurance-rates)). PID's release gives consumer contacts that are reused in `templates/consumer_open_enrollment_2027.md`. For comparison, the PY2026 weighted average approved increase was 21.5% (SECONDARY; [InsuranceNewsNet, 2026](https://insurancenewsnet.com/oarticle/pennie-customers-likely-to-see-increase-in-aca-costs)).

**Year-label warning.** The figures 21.40% (Highmark Benefits Group) and 10.46% (Geisinger Health Plan) in earlier project notes match PID's PY2027 *requested* rates (21.4% and 10.5%), not PY2026 approved rates. See `docs/source_reliability.md`.

### 3.2 Rating areas and carrier footprints

Pennsylvania has nine rating areas covering 67 counties (Calculation C6; [CMS, n.d.](https://www.cms.gov/cciio/programs-and-initiatives/health-insurance-market-reforms/pa-gra)). Table 3 combines the project's area-level carrier footprint (CARRIED from the September 8, 2026 area reports) with PID's approved rates (VERIFIED). Ranges are unweighted across carriers; no verified enrollment weights exist, so no averages are reported.

**Table 3**

| Rating area | Counties | Entities listed | With PID rate | Lowest approved % | Highest approved % |
|---|---:|---:|---:|---|---|
| 1 | 8 | 5 | 4 | 9.7 (UPMC Health Network) | 35.1 (Ambetter) |
| 2 | 3 | 6 | 5 | 8.6 (Geisinger Health Plan) | 35.1 (Ambetter) |
| 3 | 13 | 9 | 8 | 1.4 (Oscar) | 35.1 (Ambetter) |
| 4 | 10 | 4 | 3 | 9.7 (UPMC Health Network) | 35.1 (Ambetter) |
| 5 | 7 | 7 | 6 | 8.6 (Geisinger Health Plan) | 35.1 (Ambetter) |
| 6 | 10 | 10 | 9 | 1.4 (Oscar) | 35.1 (Ambetter) |
| 7 | 4 | 8 | 7 | 1.4 (Oscar) | 35.1 (Ambetter) |
| 8 | 5 | 8 | 7 | 1.4 (Oscar) | 35.1 (Ambetter) |
| 9 | 7 | 8 | 7 | 8.6 (Geisinger Health Plan) | 35.1 (Ambetter) |

*Note.* "Entities listed" counts every entity listed for at least one county in the area, so it overstates choice in any single county. In every area one entity (Ambetter Health Solutions of Pennsylvania) is listed but absent from PID's release. Full per-area tables are in `report/rating_area_summaries.md`.

Earlier drafts named "dominant carriers" per area using entity names that do not match PID filings (for example "Highmark Care Benefits"); those labels are withdrawn (ledger L19). The statement that rating-area factors range from below 1.00 to higher values in Area 8 is unsourced and is also withdrawn (L20).

### 3.3 Enrollment

Sourced Pennie counts are in `data/public/enrollment_series.csv`. Pennie reported a record 497,000 enrollees in 2025 and 486,000 at the close of 2026 open enrollment, then a further decline of more than 40,000 in four months ([Pennie, 2026](https://agency.pennie.com/?p=12805); [PORH, 2026a](https://www.porh.psu.edu/pennie-enrollment-continues-to-drop/)). A hospital association summary gives 443,024 on June 1, 2026 ([HAP, 2026](https://www.haponline.org/News/HAP-News-Articles/Latest-News/millions-drop-aca-insurance-coverage-after-open-enrollment)), and a legislators' release reports 417,000 enrolled as of September 2026 ([Pennsylvania House Democrats, 2026](https://www.pahouse.com/ACD/InTheNews/NewsRelease/?id=145107)). The draft's 501,459 peak and exact 417,158 figure were not found in any source (L05, L06) and are not used. Calculation C2 shows how the attrition figure depends on the baseline.

Reporting also shows a shift in plan mix: Silver sign-ups fell 20% while Bronze rose 33% (SECONDARY; [InsuranceNewsNet, 2026b](https://insurancenewsnet.com/oarticle/160000-pennsylvanians-off-health-insurance-exchange-after-price-hikes)). Counts of people who left differ by source and definition (85,000, about 92,000, 120,000); see `audit/conflicts_register.csv`, item X05.

### 3.4 2027 open enrollment and eligibility changes

Pennie's board reinstated the November 1, 2026 to January 15, 2027 window ([PORH, 2026b](https://www.porh.psu.edu/pa-health-insurance-exchange-2027-open-enrollment-period-returns-to-november-1-2026-january-15-2027/)). Enrolling by December 15 starts coverage January 1; enrolling December 16 to January 15 starts coverage February 1 ([WHYY, 2026b](https://whyy.org/articles/affordable-care-act-health-insurance-open-enrollment/); [PHLP, 2026](https://www.phlp.org/en/news/pennie-open-enrollment-what-s-changing-for-2027-coverage)). The October 15 to December 15 schedule in the August status report is superseded.

According to PHLP (2026; SECONDARY), from January 1, 2027 premium tax credits and cost-sharing reductions are limited to lawful permanent residents, Cuban/Haitian entrants and COFA migrants; Pennie estimates 20,000 to 30,000 Pennsylvanians will lose eligibility for tax credits; and passive renewal remains in 2027 but enrollees are advised to log in, with an annual affirmation requirement starting with the fall 2027 enrollment for 2028 coverage.

### 3.5 Cost-sharing limits

For PY2027 the maximum annual cost-sharing limit is $12,000 self-only and $24,000 family, up from $10,600 and $21,200 in 2026 (Calculation C5; SECONDARY via [healthinsurance.org](https://www.healthinsurance.org/glossary/out-of-pocket-maximum-limit/), citing [CMS, 2026](https://www.cms.gov/files/document/2027-papi-parameters-guidance-2026-01-29.pdf), which should be opened and confirmed before publication). The $9,200 figure in the earlier draft, labelled as the 2026 limit, appears to be the 2025 limit and is withdrawn. Embedded individual caps within family plans cannot exceed the self-only limit.

### 3.6 Re-enrollment and the Plan ID crosswalk

45 CFR § 155.335(j) is the exchange re-enrollment provision ([45 CFR § 155.335, n.d.](https://www.law.cornell.edu/cfr/text/45/155.335)). The six-tier hierarchy in the earlier draft, including network-ID matching, movement of one metal level and cross-issuer mapping, was attributed to that paragraph but could not be matched to the regulation's text and is withdrawn pending a line-by-line check against eCFR (L26). The crosswalk submission deadlines of June 10 and August 31, 2026 are also unverified (L24).

### 3.7 Single risk pool and rate-review framework (descriptive)

Issuers file through SERFF with a URRT and an actuarial memorandum, and PID reviews requests against supporting data ([PID, 2026a](https://www.pa.gov/agencies/insurance/newsroom/pennsylvania-releases-aca-2027-health-insurance-rates)). Single risk pool, geographic rating, actuarial value and risk adjustment requirements are federal standards (45 CFR §§ 156.80, 154.215, 156.135 and Part 153; CARRIED, [eCFR Part 153](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-B/part-153)). Risk adjustment is ACA section 1343 ([42 U.S.C. § 18063](https://www.govinfo.gov/link/uscode/42/18063); VERIFIED). The earlier draft cited "Section 1340"; that is incorrect and any edit to 1340 should be reverted. This packet does not assert that any filing is compliant, because no filing exhibits were audited.

### 3.8 Plan taxonomy (reference)

| Concept | Working definition |
|---|---|
| HMO / EPO | In-network coverage except emergencies; HMOs generally require a primary care referral for specialists |
| PPO / POS | Broader networks with out-of-network benefits at higher cost sharing |
| Deductible, coinsurance, copay | Standard cost-sharing mechanics; OOP maximum caps total EHB cost sharing |
| Embedded vs aggregate | Embedded: each family member's spending is capped at the individual limit; aggregate: the family threshold applies to all |

*Note.* General definitions, unsourced in this packet; the drug-tier taxonomy in the earlier draft is omitted as non-audit content.

## 4. Calculations

Each subsection states why the calculation is done, how, and what limits its use. All results are reproduced by `python3 scripts/calc_audit.py` and checked by `tests/test_packet.py`.

### C1. Composite medical cost trend (corrects the earlier draft)

*Why.* Cost components act sequentially (a price rise applies to a volume that has itself risen), so compounding is the appropriate method.

*How.* Using the earlier draft's assumed component ranges (UNVERIFIED): unit cost 5.0% to 6.5%, utilization 2.0% to 3.0%, morbidity adjustment 1.5% to 2.5%.

Low: (1.050)(1.020)(1.015) = 1.087065, so **8.71%**.
High: (1.065)(1.030)(1.025) = 1.124374, so **12.44%**.

The earlier draft printed 1.086615 (8.66%) and 1.122184 (12.22%); neither is the product of its own factors. Additive sums are 8.50% and 12.00%.

*Limits.* Unit cost times utilization alone gives 7.10% to 9.70%, so the "7.4% to 9.1% historical range" claimed as reconciled cannot be reproduced and has no source (L12). Both PID's requested (17.14%) and approved (15.97%) averages exceed the high composite of 12.44%, so these three components do not by themselves explain the filed increases.

### C2. Enrollment attrition under three baselines

*Why.* The attrition rate and the K indicator both depend on the baseline, and the earlier draft mixed a 2025 peak with a 2026 count.

*How.* Net loss = baseline - current; attrition = net loss / baseline; K = current / baseline.

| Baseline | Baseline N | Current N | Net loss | Attrition | K |
|---|---:|---:|---:|---:|---:|
| A. Draft figures (UNVERIFIED) | 501,459 | 417,158 | 84,301 | 16.81% | 0.8319 |
| B. 2025 peak to Sept 2026 (SECONDARY) | 497,000 | 417,000 | 80,000 | 16.10% | 0.8390 |
| C. 2026 OE close to Sept 2026 (SECONDARY) | 486,000 | 417,000 | 69,000 | 14.20% | 0.8580 |

*Reading.* The K < 0.85 audit trigger fires under A and B but not under C. A "mid-year" indicator should use the plan-year start (C), and a year-over-year indicator should be labelled as such. Pennie's statement that about one in three 2025 enrollees are no longer enrolled measures turnover, not net change ([Pennie, 2026](https://agency.pennie.com/?p=12805)).

### C3. Rate review outcomes

*Why.* To quantify how much PID reduced requests and where review raised rates.

*How.* Change in points = approved - requested. Premium-level effect = (1 + approved) / (1 + requested) - 1.

- Statewide individual: 15.97 - 17.14 = **-1.17 points**; (1.1597 / 1.1714) - 1 = **-1.00%** premium level; the review removed 1.17 / 17.14 = **6.83%** of the requested increase.
- Statewide small group: 10.28 - 11.49 = **-1.21 points**.
- Carrier level: largest cut Oscar -14.0 points; approved above request: Health Partners Plans (+2.4), Keystone Health Plan East (+1.3), QCC (+1.4).
- Carriers with approved increase above 10%: **11 of 14**; those at or below 10% are Geisinger Health Plan (8.6), UPMC Health Network (9.7) and Oscar (1.4).
- Cumulative illustration: (1.215)(1.1597) = 1.4090, or **+40.90%** across PY2026 and PY2027.

*Limits.* The cumulative figure multiplies two different years' weighted averages (enrollment mixes differ) and is gross, not what any enrollee pays after subsidy. Pennie reported a 102% average net premium increase for enrollees who kept coverage in 2026 (see `data/claims_ledger.csv`, L14).

### C4. PY2027 driver scenario (illustrative only)

*Why.* The earlier draft decomposed the request into driver ranges and said the result "aligns" with 16.0% without computing it.

*How.* Ranges (UNVERIFIED, unsourced): base trend 8.0% to 9.0%, morbidity 1.5% to 2.5%, specialty drugs 3.0% to 4.0%, reinsurance and risk adjustment 1.0% to 2.0%.

| Method | Low | High | Midpoint |
|---|---:|---:|---:|
| Additive | 13.50% | 17.50% | 15.50% |
| Compounded | 14.04% | 18.52% | 16.28% |

PID's requested (17.14%) and approved (15.97%) averages fall inside both ranges, so the scenario cannot discriminate between them. It is a sensitivity illustration, not a finding.

### C5. Cost-sharing limit change

*Why.* To correct the cap used in the earlier draft and quantify the 2027 increase.

*How.* 12,000 / 10,600 = 1.13208, so **+13.21%**; family 24,000 / 21,200 gives the same. The family limit is exactly twice the self-only limit. Some Bronze plans may reach 130% of the limit: 1.30 x 12,000 = **$15,600** (SECONDARY).

### C6. County verification

*Why.* To confirm complete, non-overlapping coverage.

*How.* 8 + 3 + 13 + 10 + 7 + 10 + 4 + 5 + 7 = **67** counties, 67 unique names, 9 areas, computed from the crosswalk file.

### C7. Demographic percentage check

*Why.* To test a table that the earlier draft explained away.

*How.* 65 + 7.4 + 3.6 + 3.3 + 21 = **100.3**. The excess of 0.3 points is not explained by the stated reason, and the figures have no source (L31). Hispanic ethnicity may overlap race categories, which would produce a sum above 100, but unrounded source values are needed to confirm this.

## 5. Key risk indicators (reconstructed definitions)

The formula text for these indicators was blank in the submitted file (L37), so these are reconstructions to be confirmed.

| Indicator | Definition | Threshold in draft | Status |
|---|---|---|---|
| K_attrition | Active enrollment / baseline enrollment | Target >= 0.92; trigger < 0.85 | Baseline must be stated (C2) |
| R_CSR | CSR-variant Silver enrollees / CSR-eligible enrollees | >= 0.75 | No data located |
| Delta P_cross | (2027 gross premium - 2026 gross premium) / 2026 premium for a crosswalked plan | > 10% triggers outreach | 11 of 14 carriers exceed 10% on average (C3) |

## 6. Recommendations

1. **Separate morbidity from trend in public filing summaries.** PID already explains some approvals by risk adjustment results (Health Partners Plans); requiring a consistent line item would let the public compare carriers.
2. **Tier the passive re-enrollment outreach trigger.** Because 11 of 14 carriers exceed the 10% threshold on average, it would flag most renewals. Consider a tiered trigger (for example plan-level increase above the statewide approved average, or net premium change after subsidy).
3. **Collect county-level Cost-Sharing Reduction uptake before running rural campaigns.** The Silver-to-Bronze shift is documented statewide (SECONDARY), but the rural estimate of 15% to 22% is unsourced. Rating Areas 2, 3 and 5 remain reasonable pilot targets.
4. **Check crosswalk network overlap line by line against CMS plan-crosswalk guidance** and eCFR text before asserting any regulatory requirement.
5. **Publish enrollment definitions.** Terminations, net change and turnover are being reported as if interchangeable (X05).
6. **Obtain** PID's per-carrier small-group approved rates and the PY2026 per-carrier table before any year-over-year carrier comparison (X08).

## 7. Limitations

- No actuarial memoranda, URRT exhibits or SERFF filings were reviewed this pass; no compliance conclusions are drawn.
- Carrier footprints are area-level and carried from September 8, 2026.
- Several enrollment figures are rounded or reprinted; Pennie's primary dataset was not located.
- Items marked CARRIED were not re-checked on November 8, 2026.
- PID figures are weighted averages; individual premiums depend on age, county, plan and subsidy.

## References

Centers for Medicare & Medicaid Services. (n.d.). *Pennsylvania geographic rating areas*. <https://www.cms.gov/cciio/programs-and-initiatives/health-insurance-market-reforms/pa-gra>

Centers for Medicare & Medicaid Services. (2026, January 29). *Premium adjustment percentage, maximum annual limitation on cost sharing, reduced maximum annual limitation on cost sharing, and required contribution percentage for the 2027 benefit year*. <https://www.cms.gov/files/document/2027-papi-parameters-guidance-2026-01-29.pdf>

Cornell Law School Legal Information Institute. (n.d.). *45 CFR § 155.335: Annual eligibility redetermination*. <https://www.law.cornell.edu/cfr/text/45/155.335>

Electronic Code of Federal Regulations. (n.d.). *45 CFR Part 153: Standards related to reinsurance, risk corridors, and HHS risk adjustment under the Affordable Care Act*. <https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-B/part-153>

Hospital and Healthsystem Association of Pennsylvania. (2026, July 1). *Millions drop ACA insurance coverage after open enrollment*. <https://www.haponline.org/News/HAP-News-Articles/Latest-News/millions-drop-aca-insurance-coverage-after-open-enrollment>

healthinsurance.org. (n.d.). *Out-of-pocket maximum limit*. <https://www.healthinsurance.org/glossary/out-of-pocket-maximum-limit/>

InsuranceNewsNet. (2026a). *Pennie customers likely to see increase in ACA costs*. <https://insurancenewsnet.com/oarticle/pennie-customers-likely-to-see-increase-in-aca-costs>

InsuranceNewsNet. (2026b). *160,000 Pennsylvanians off health insurance exchange after price hikes*. <https://insurancenewsnet.com/oarticle/160000-pennsylvanians-off-health-insurance-exchange-after-price-hikes>

Pennie. (2026, June 9). *Pennsylvanians dropping health coverage through Pennie citing higher plan costs as the number one reason* [Press release]. <https://agency.pennie.com/?p=12805>

Pennsylvania House Democratic Caucus. (2026, September 10). *Legislators pushing for healthcare coverage respond to new PENNIE enrollment numbers*. <https://www.pahouse.com/ACD/InTheNews/NewsRelease/?id=145107>

Pennsylvania Health Law Project. (2026, August 28). *Pennie open enrollment: What's changing for 2027 coverage*. <https://www.phlp.org/en/news/pennie-open-enrollment-what-s-changing-for-2027-coverage>

Pennsylvania Insurance Department. (2026a, September 18). *Pennsylvania Insurance Department releases Affordable Care Act 2027 health insurance rates*. <https://www.pa.gov/agencies/insurance/newsroom/pennsylvania-releases-aca-2027-health-insurance-rates>

Pennsylvania Insurance Department. (2026b). *Affordable Care Act health rate filings*. <https://www.pa.gov/agencies/insurance/posted-filings-reports-company-orders/posted-product-and-rate-filings/aca-health-rate-filings>

Pennsylvania Office of Rural Health. (2026a). *Pennie enrollment continues to drop*. <https://www.porh.psu.edu/pennie-enrollment-continues-to-drop/>

Pennsylvania Office of Rural Health. (2026b). *PA Health Insurance Exchange 2027 open enrollment period returns to November 1, 2026-January 15, 2027*. <https://www.porh.psu.edu/pa-health-insurance-exchange-2027-open-enrollment-period-returns-to-november-1-2026-january-15-2027/>

U.S. Government Publishing Office. (n.d.). *42 U.S.C. § 18063: Risk adjustment*. <https://www.govinfo.gov/link/uscode/42/18063>

WHYY. (2026a). *Pennsylvania ACA health insurers propose double-digit premium increases for 2027*. <https://whyy.org/articles/premium-increases-2027-pennie-pennsylvania-aca/>

WHYY. (2026b). *Pa., N.J., Del. to kick off ACA open enrollment on Nov. 1 for 2027 health coverage*. <https://whyy.org/articles/affordable-care-act-health-insurance-open-enrollment/>

## Appendix A. Link specificity

| Link | Level |
|---|---|
| PID 2026a release | Pinpoint (specific release page) |
| PID 2026b rate filings | Landing page; per-carrier filing documents not linked |
| CMS 2026 cost-sharing guidance | Pinpoint URL, not opened this pass |
| CMS rating areas | Pinpoint page; county table not re-checked |
| 45 CFR § 155.335 | Section level; paragraph (j) text not quoted |
| eCFR Part 153 | Part level only |
| 42 U.S.C. § 18063 | Section level |
| Pennie, PORH, PHLP, WHYY, HAP, InsuranceNewsNet, House Democrats | Article level; not primary datasets except the Pennie release |

## Appendix B. Items withdrawn from the earlier draft

See `data/claims_ledger.csv` (45 rows) and `report/REVIEW_OF_SUBMITTED_DRAFT.md`. Items include the 501,459 and 417,158 enrollment figures, the "requested 16.0%" label, the historical PY2017 to PY2025 rate table, the demographic table, the six-tier crosswalk hierarchy, "Section 1340", the $9,200 cap and all "fully compliant" audit outcomes.
