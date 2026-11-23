#!/usr/bin/env bash
# addon_manifest_drift.sh — Compares live file hashes against MANIFEST.sha256
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
MANIFEST="MANIFEST.sha256"
if [ ! -f "$MANIFEST" ]; then
    echo "  [FAIL] $MANIFEST not found"
    exit 1
fi
echo "=== MANIFEST DRIFT DETECTOR ==="
python3 - "$MANIFEST" << 'PYEOF'
import hashlib, sys
from pathlib import Path
manifest_path = Path(sys.argv[1])
manifest = {}
for line in manifest_path.read_text().splitlines():
    if not line.strip() or line.startswith('#'):
        continue
    parts = line.split(None, 1)
    if len(parts) == 2:
        h, rel = parts[0], parts[1].lstrip('*')
        manifest[rel.strip()] = h
current = {}
for p in sorted(Path('.').rglob('*')):
    if not p.is_file():
        continue
    rel = p.relative_to('.').as_posix()
    if rel == 'MANIFEST.sha256' or p.suffix in ('.pyc', '.zip'):
        continue
    if any(part in ('.git', '__pycache__', '.pytest_cache', 'dist') for part in rel.split('/')):
        continue
    current[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
added = sorted(set(current) - set(manifest))
removed = sorted(set(manifest) - set(current))
modified = sorted(
    rel for rel in set(current) & set(manifest)
    if current[rel] != manifest[rel]
)
print(f"  Manifest entries: {len(manifest)}")
print(f"  Current files:    {len(current)}")
print(f"  Added:            {len(added)}")
print(f"  Removed:          {len(removed)}")
print(f"  Modified:         {len(modified)}")
if added:
    print("\n  [+] Added files:")
    for f in added[:20]:
        print(f"      {f}")
if removed:
    print("\n  [-] Removed files:")
    for f in removed[:20]:
        print(f"      {f}")
if modified:
    print("\n  [~] Modified files:")
    for f in modified[:20]:
        print(f"      {f}")
if not (added or removed or modified):
    print("\n  Result: NO DRIFT — manifest is current")
    sys.exit(0)
else:
    print(f"\n  Result: DRIFT DETECTED ({len(added)+len(removed)+len(modified)} change(s))")
    sys.exit(1)
PYEOF
