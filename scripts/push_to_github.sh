#!/usr/bin/env bash
# push_to_github.sh - validate, commit and push this packet. Never cleans or resets.
set -euo pipefail
REMOTE="https://github.com/bilbywilby/Pennsylvania_Health_Insurance_November_2026.git"
cd "$(dirname "$0")/.."

echo ">>> validate"
python3 scripts/calc_audit.py >/dev/null
python3 scripts/build_area_tables.py
python3 scripts/validate_packet.py
python3 scripts/06_provenance_gate.py
python3 -m unittest discover -s tests

echo ">>> manifest"
python3 scripts/hash_manifest.py

echo ">>> git"
[ -d .git ] || git init
git branch -M main
git remote get-url origin >/dev/null 2>&1 || git remote add origin "$REMOTE"
git add -A
if git diff --cached --quiet; then
  echo "nothing to commit"
else
  git commit -m "docs: add November 2026 audit packet (PY2027 approved rates, corrections, calculations)"
fi
git push -u origin main
echo "[OK] pushed to $(git remote get-url origin)"
