#!/usr/bin/env bash
# addon_xref_validate.sh — Cross-checks HANDOVER.json figures against calc_results.json
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
echo "=== CROSS-REFERENCE VALIDATOR ==="
python3 << 'PYEOF'
import json, sys
from pathlib import Path
handover = json.loads(Path("HANDOVER.json").read_text())
calc = json.loads(Path("audit/calc_results.json").read_text())
errors = []
checks = 0
r3 = calc["C3_rate_review"]
kf = handover.get("current_state", {}).get("key_findings", {})
if kf.get("carriers_in_pid_release") != r3["n_carriers"]:
    errors.append(f"carriers_in_pid_release: HANDOVER={kf.get('carriers_in_pid_release')} vs calc={r3['n_carriers']}")
checks += 1
if kf.get("carriers_approved_over_10pct") != r3["n_approved_over_10pct"]:
    errors.append(f"carriers_approved_over_10pct: HANDOVER={kf.get('carriers_approved_over_10pct')} vs calc={r3['n_approved_over_10pct']}")
checks += 1
r4 = calc["C4_decomposition"]
if kf.get("individual_approved_pct") and abs(float(kf["individual_approved_pct"]) - r4["pid_approved"]) > 0.01:
    errors.append(f"individual_approved_pct: HANDOVER={kf['individual_approved_pct']} vs calc={r4['pid_approved']}")
checks += 1
if kf.get("individual_requested_pct") and abs(float(kf["individual_requested_pct"]) - r4["pid_requested"]) > 0.01:
    errors.append(f"individual_requested_pct: HANDOVER={kf['individual_requested_pct']} vs calc={r4['pid_requested']}")
checks += 1
r2 = calc["C2_attrition"]["A_draft"]
if "attrition_K" in kf:
    if abs(float(kf["attrition_K"]) - float(r2["K"])) > 0.001:
        errors.append(f"attrition_K: HANDOVER={kf['attrition_K']} vs calc={r2['K']}")
    checks += 1
r6 = calc["C6_counties"]
if kf.get("rating_areas") and kf["rating_areas"] != r6["areas"]:
    errors.append(f"rating_areas: HANDOVER={kf['rating_areas']} vs calc={r6['areas']}")
checks += 1
print(f"  Checks performed: {checks}")
print(f"  Errors:           {len(errors)}")
if errors:
    print("\n  [FAIL] Mismatches found:")
    for e in errors:
        print(f"         {e}")
    sys.exit(1)
else:
    print("  Result: PASS — all cross-references consistent")
PYEOF
