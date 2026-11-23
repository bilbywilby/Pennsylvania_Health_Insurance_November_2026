# PA Health Repositories Reconciliation Report (Nov 23, 2026)

## Source Repositories & Extracted Snapshots
- November 2026 Repo: `/data/data/com.termux/files/home/pa_health_repos/Pennsylvania_Health_Insurance_November_2026`
- October 2026 Repo: `/data/data/com.termux/files/home/pa_health_repos/Pennsylvania_Health_Insurance_October_2026`
- September 2026 Repo: `/data/data/com.termux/files/home/pa_health_repos/Pennsylvania_Healthcare_September_2026`
- Extracted Sept 2026 Archives (`14`):
  - `Ez_Brand-main (4)`: 17 files (0 .py, 3 data, 7 md/txt, 0 pdf/docx)
  - `PA_Rating_Area_Reports_2027`: 9 files (0 .py, 0 data, 0 md/txt, 9 pdf/docx)
  - `Pennsylvania_Healthcare_August_2026-main (2)`: 10 files (0 .py, 1 data, 5 md/txt, 4 pdf/docx)
  - `Pennsylvania_Healthcare_August_2026-main (3)`: 10 files (0 .py, 1 data, 5 md/txt, 4 pdf/docx)
  - `Pennsylvania_Healthcare_July_2026-main`: 27 files (0 .py, 0 data, 3 md/txt, 16 pdf/docx)
  - `equicare-public-healthcare-equity-utility-main`: 103 files (0 .py, 6 data, 3 md/txt, 0 pdf/docx)
  - `fairmed-pa-public-healthcare-equity-utility-main`: 98 files (0 .py, 6 data, 3 md/txt, 0 pdf/docx)
  - `keystone-health-advocate-pa-medical-rights-wiki-forensic-tool-main`: 114 files (0 .py, 6 data, 3 md/txt, 0 pdf/docx)
  - `keystone-health-forensic-navigator-blueprint-main`: 100 files (0 .py, 6 data, 3 md/txt, 0 pdf/docx)
  - `legacy-health-insurance-navigator-main`: 114 files (0 .py, 6 data, 3 md/txt, 0 pdf/docx)
  - `pa-health-audit-advocacy-platform-main`: 132 files (0 .py, 8 data, 3 md/txt, 0 pdf/docx)
  - `pennsylvania-health-insurance-audit-2026-main`: 27 files (12 .py, 5 data, 3 md/txt, 0 pdf/docx)
  - `pennsylvania-health-insurance-audit-2026-main (1)`: 27 files (12 .py, 5 data, 3 md/txt, 0 pdf/docx)
  - `statuspulse-service-health-incident-reporting-dashboard-beta-main`: 89 files (0 .py, 6 data, 3 md/txt, 0 pdf/docx)

## Crosswalk & Statute Comparison
- `statutes_2026.json` identical (Nov vs Sept): `False`
- `rating_area_counties.csv` (Nov) data rows: `67`
- `rating_areas_2026.csv` (Sept) data rows: `9`
- `derived_area_metrics.json` (Oct) present: `True`

## Key Findings & SSOT Notes
- `Pennsylvania_Health_Insurance_November_2026` serves as the canonical PY2027 audit & release pipeline.
- Extracted Sept 2026 `.zip` archives are cataloged in `reconciliation/extracted_sept2026_inventory.json`.
