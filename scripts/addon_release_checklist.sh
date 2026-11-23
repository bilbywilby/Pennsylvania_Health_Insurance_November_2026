#!/usr/bin/env bash
# addon_release_checklist.sh — Sequentially runs all validation gates
# NOTE: hash_manifest.py runs LAST (write step) so drift check sees pre-existing state
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   RELEASE CHECKLIST — FULL VALIDATION PIPELINE          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
PASS=0
FAIL=0
TOTAL=0
RESULTS=()
run_check() {
    local name="$1"
    local cmd="$2"
    TOTAL=$((TOTAL + 1))
    printf "  [%2d] %-35s " "$TOTAL" "$name"
    if eval "$cmd" > /dev/null 2>&1; then
        echo "PASS"
        PASS=$((PASS + 1))
        RESULTS+=("PASS  $name")
    else
        echo "FAIL"
        FAIL=$((FAIL + 1))
        RESULTS+=("FAIL  $name")
    fi
}
# Read-only checks first
run_check "Build area tables"        "python3 scripts/build_area_tables.py"
run_check "Calc audit"               "python3 scripts/calc_audit.py"
run_check "Validate packet"          "python3 scripts/validate_packet.py"
run_check "Provenance gate"          "python3 scripts/06_provenance_gate.py"
run_check "Pytest suite"             "pytest -q"
run_check "Storage health"           "bash scripts/addon_storage_health.sh"
run_check "Git hygiene"              "bash scripts/addon_git_hygiene.sh"
run_check "Manifest drift"           "bash scripts/addon_manifest_drift.sh"
run_check "Dependency audit"         "bash scripts/addon_dep_audit.sh"
run_check "Cross-reference"          "bash scripts/addon_xref_validate.sh"
# Write step last (expected to dirty tree if drift existed)
run_check "Hash manifest (update)"   "python3 scripts/hash_manifest.py"
echo ""
echo "──────────────────────────────────────────────────────────"
printf "  SUMMARY: %d/%d passed, %d failed\n" "$PASS" "$TOTAL" "$FAIL"
echo "──────────────────────────────────────────────────────────"
echo ""
for r in "${RESULTS[@]}"; do
    echo "  $r"
done
echo ""
if [ "$FAIL" -eq 0 ]; then
    echo "  ALL CHECKS PASSED — ready for release"
    exit 0
else
    echo "  $FAIL CHECK(S) FAILED — fix before release"
    exit 1
fi
