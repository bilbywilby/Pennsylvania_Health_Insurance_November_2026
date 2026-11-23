#!/usr/bin/env bash
# install_addons.sh — Creates 10 operational add-on scripts for the audit packet
# Run: bash scripts/install_addons.sh
# All scripts are pure bash + Python stdlib (Termux-safe, no pip installs)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
echo "=== Installing 10 add-on scripts into scripts/ ==="

# ADD-ON 1: Storage Health Probe
cat > scripts/addon_storage_health.sh << 'ADDON1'
#!/usr/bin/env bash
# addon_storage_health.sh — Dual-mount (bytes + inodes) storage audit
set -euo pipefail
BYTES_THRESHOLD=95
INODE_THRESHOLD=90
MOUNTS=("/" "/data/user/0")
exit_code=0
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│  STORAGE HEALTH PROBE  (thresholds: bytes>${BYTES_THRESHOLD}%, inodes>${INODE_THRESHOLD}%) │"
echo "└─────────────────────────────────────────────────────────────────┘"
for mount in "${MOUNTS[@]}"; do
    if [ ! -d "$mount" ]; then
        echo "  [SKIP] $mount (not present)"
        continue
    fi
    df_output=$(df -P "$mount" 2>/dev/null | tail -1)
    if [ -z "$df_output" ]; then
        echo "  [WARN] $mount (df failed)"
        continue
    fi
    avail_kb=$(echo "$df_output" | awk '{print $4}')
    use_pct=$(echo "$df_output" | awk '{print $5}' | tr -d '%')
    ifdf_output=$(df -iP "$mount" 2>/dev/null | tail -1)
    if [ -n "$ifdf_output" ]; then
        inode_pct=$(echo "$ifdf_output" | awk '{print $5}' | tr -d '%')
    else
        inode_pct="N/A"
    fi
    free_gib=$(awk "BEGIN {printf \"%.2f\", $avail_kb / 1048576}")
    status="OK"
    if [ "$use_pct" -ge "$BYTES_THRESHOLD" ] 2>/dev/null; then
        status="CRITICAL"; exit_code=1
    elif [ "$use_pct" -ge 85 ] 2>/dev/null; then
        status="WARNING"
    fi
    if [ "$inode_pct" != "N/A" ] && [ "$inode_pct" -ge "$INODE_THRESHOLD" ] 2>/dev/null; then
        exit_code=1
    fi
    printf "  [%s] %-15s %s GiB free | bytes: %3s%% | inodes: %3s%%\n" \
        "$status" "$mount" "$free_gib" "$use_pct" "$inode_pct"
done
echo ""
if [ "$exit_code" -eq 0 ]; then
    echo "  Result: ALL HEALTHY"
else
    echo "  Result: THRESHOLD BREACHED"
fi
exit $exit_code
ADDON1

# ADD-ON 2: Git Hygiene Checker
cat > scripts/addon_git_hygiene.sh << 'ADDON2'
#!/usr/bin/env bash
# addon_git_hygiene.sh — Verifies repo is clean, VERSION matches tag, no stray files
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
echo "=== GIT HYGIENE CHECK ==="
fail=0
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    echo "  [FAIL] Working tree is dirty:"
    git status --short | head -20
    fail=1
else
    echo "  [OK]   Working tree clean"
fi
version_file="VERSION"
if [ -f "$version_file" ]; then
    ver=$(cat "$version_file" | tr -d '[:space:]')
    latest_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "none")
    if [ "$latest_tag" = "$ver" ]; then
        echo "  [OK]   VERSION ($ver) matches latest tag"
    else
        echo "  [WARN] VERSION ($ver) != latest tag ($latest_tag)"
    fi
else
    echo "  [WARN] No VERSION file found"
fi
large_untracked=$(git ls-files --others --exclude-standard 2>/dev/null | while read -r f; do
    if [ -f "$f" ]; then
        size=$(wc -c < "$f")
        if [ "$size" -gt 1048576 ]; then
            echo "$f ($size bytes)"
        fi
    fi
done)
if [ -n "$large_untracked" ]; then
    echo "  [WARN] Large untracked files (>1MB):"
    echo "$large_untracked" | sed 's/^/         /'
else
    echo "  [OK]   No large untracked files"
fi
branch_info=$(git status -sb 2>/dev/null | head -1)
echo "  [INFO] $branch_info"
echo "  [INFO] Last 3 commits:"
git log --oneline -3 2>/dev/null | sed 's/^/         /'
echo ""
if [ "$fail" -eq 0 ]; then
    echo "  Result: PASS"
else
    echo "  Result: FAIL"
fi
exit $fail
ADDON2

# ADD-ON 3: Manifest Drift Detector
cat > scripts/addon_manifest_drift.sh << 'ADDON3'
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
    rel = p.as_posix()
    if any(part in ('.git', '__pycache__', '.pytest_cache') for part in rel.split('/')):
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
ADDON3

# ADD-ON 4: Cache & Artifact Cleaner
cat > scripts/addon_clean_caches.sh << 'ADDON4'
#!/usr/bin/env bash
# addon_clean_caches.sh — Removes build caches, test artifacts, and temp files
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
echo "=== CACHE & ARTIFACT CLEANER ==="
freed=0
targets=(".pytest_cache" "__pycache__" "*.pyc" ".DS_Store")
for target in "${targets[@]}"; do
    while IFS= read -r -d '' match; do
        if [ -d "$match" ]; then
            size=$(du -sk "$match" 2>/dev/null | awk '{print $1}')
            rm -rf "$match"
            freed=$((freed + ${size:-0}))
            echo "  [rm] $match (${size:-0} KB)"
        elif [ -f "$match" ]; then
            rm -f "$match"
            echo "  [rm] $match"
        fi
    done < <(find . -name "$target" -not -path './.git/*' -print0 2>/dev/null || true)
done
find . -type d -empty -not -path './.git*' -not -path '.' -delete 2>/dev/null || true
echo ""
echo "  Freed: ~${freed} KB"
echo "  Result: DONE"
ADDON4

# ADD-ON 5: Packet Integrity Snapshot
cat > scripts/addon_snapshot.sh << 'ADDON5'
#!/usr/bin/env bash
# addon_snapshot.sh — Creates a timestamped tarball of managed packet files
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SNAPSHOT_DIR="${HOME}/.snapshots"
mkdir -p "$SNAPSHOT_DIR"
OUTPUT="${SNAPSHOT_DIR}/packet_${TIMESTAMP}.tar.gz"
echo "=== PACKET INTEGRITY SNAPSHOT ==="
echo "  Output: $OUTPUT"
tar -czf "$OUTPUT" \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='.pytest_cache' \
    --exclude='*.pyc' \
    README.md CHANGELOG.md VERSION HANDOVER.json MANIFEST.sha256 \
    .gitattributes .gitignore audit/ data/ docs/ report/ scripts/ templates/ tests/ \
    2>/dev/null
size=$(wc -c < "$OUTPUT")
size_kb=$((size / 1024))
echo "  Size:   ${size_kb} KB"
echo "  SHA256: $(sha256sum "$OUTPUT" | awk '{print $1}')"
echo "  Result: SNAPSHOT CREATED"
ADDON5

# ADD-ON 6: Dependency Audit
cat > scripts/addon_dep_audit.sh << 'ADDON6'
#!/usr/bin/env bash
# addon_dep_audit.sh — Scans all .py files for imports, verifies stdlib-only
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
echo "=== DEPENDENCY AUDIT (stdlib-only verification) ==="
python3 << 'PYEOF'
import ast, sys
from pathlib import Path
STDLIB = {
    'abc','argparse','array','ast','asyncio','atexit','base64','binascii',
    'bisect','builtins','bz2','calendar','collections','colorsys','configparser',
    'contextlib','contextvars','copy','csv','ctypes','dataclasses','datetime',
    'dbm','decimal','difflib','dis','email','encodings','enum','errno',
    'faulthandler','fnmatch','fractions','ftplib','functools','gc','getopt',
    'getpass','gettext','glob','gzip','hashlib','heapq','hmac','html','http',
    'imaplib','importlib','inspect','io','ipaddress','itertools','json',
    'keyword','linecache','locale','logging','lzma','mailbox','marshal','math',
    'mimetypes','mmap','multiprocessing','netrc','numbers','operator','optparse',
    'os','pathlib','pdb','pickle','pkgutil','platform','plistlib','poplib',
    'posixpath','pprint','profile','pstats','pty','pwd','py_compile','pydoc',
    'queue','quopri','random','re','readline','reprlib','resource','rlcompleter',
    'runpy','sched','secrets','select','selectors','shelve','shlex','shutil',
    'signal','site','smtplib','socket','socketserver','sqlite3','ssl','stat',
    'statistics','string','stringprep','struct','subprocess','sys','sysconfig',
    'syslog','tabnanny','tarfile','tempfile','termios','test','textwrap',
    'threading','time','timeit','token','tokenize','trace','traceback',
    'tracemalloc','tty','types','typing','unicodedata','unittest','urllib',
    'uu','uuid','venv','warnings','wave','weakref','webbrowser','wsgiref',
    'xml','xmlrpc','zipapp','zipfile','zipimport','zlib','__future__','concurrent',
    'tomllib','graphlib','graphlib','lib2to3','distutils','idlelib','tkinter'
}
all_imports = set()
files_scanned = 0
for py in sorted(Path('.').rglob('*.py')):
    if any(part in ('.git', '__pycache__', '.pytest_cache') for part in py.parts):
        continue
    files_scanned += 1
    try:
        tree = ast.parse(py.read_text())
    except SyntaxError:
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                all_imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                all_imports.add(node.module.split('.')[0])
third_party = sorted(all_imports - STDLIB)
print(f"  Files scanned:  {files_scanned}")
print(f"  Unique imports: {len(all_imports)}")
print(f"  All stdlib:     {'YES' if not third_party else 'NO'}")
if third_party:
    print(f"\n  [WARN] Non-stdlib imports detected:")
    for mod in third_party:
        print(f"         {mod}")
    sys.exit(1)
else:
    print("\n  Result: PASS — zero external dependencies confirmed")
PYEOF
ADDON6

# ADD-ON 7: Cross-Reference Validator
cat > scripts/addon_xref_validate.sh << 'ADDON7'
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
ADDON7

# ADD-ON 8: Changelog Generator from Git
cat > scripts/addon_gen_changelog.sh << 'ADDON8'
#!/usr/bin/env bash
# addon_gen_changelog.sh — Generates a CHANGELOG entry from git log since last tag
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
echo "=== CHANGELOG GENERATOR ==="
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
CURRENT_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "unreleased")
DATE=$(date +%Y-%m-%d)
if [ -z "$LAST_TAG" ]; then
    RANGE="HEAD"
    RANGE_LABEL="$CURRENT_TAG"
else
    RANGE="${LAST_TAG}..HEAD"
    RANGE_LABEL="$CURRENT_TAG"
fi
echo "  Range: $RANGE"
echo "  Label: $RANGE_LABEL"
COMMITS=$(git log --oneline --no-merges "$RANGE" 2>/dev/null || git log --oneline -10)
COUNT=$(echo "$COMMITS" | grep -c . || echo 0)
echo "  Commits: $COUNT"
{
    echo ""
    echo "## $RANGE_LABEL ($DATE)"
    echo ""
    echo "$COMMITS" | while IFS= read -r line; do
        msg="${line#* }"
        case "$msg" in
            feat:*)     echo "- **Feature:** ${msg#feat: }" ;;
            fix:*)      echo "- **Fix:** ${msg#fix: }" ;;
            chore:*)    echo "- **Chore:** ${msg#chore: }" ;;
            docs:*)     echo "- **Docs:** ${msg#docs: }" ;;
            test:*)     echo "- **Test:** ${msg#test: }" ;;
            refactor:*) echo "- **Refactor:** ${msg#refactor: }" ;;
            *)          echo "- $msg" ;;
        esac
    done
    echo ""
} > /tmp/changelog_entry.md
if [ -f "CHANGELOG.md" ]; then
    HEADER=$(head -1 "CHANGELOG.md")
    {
        echo "$HEADER"
        cat /tmp/changelog_entry.md
        tail -n +2 "CHANGELOG.md"
    } > CHANGELOG.md.tmp && mv CHANGELOG.md.tmp CHANGELOG.md
    echo "  [OK] CHANGELOG.md updated"
else
    {
        echo "# Changelog"
        cat /tmp/changelog_entry.md
    } > CHANGELOG.md
    echo "  [OK] CHANGELOG.md created"
fi
rm -f /tmp/changelog_entry.md
echo "  Result: DONE"
ADDON8

# ADD-ON 9: Terminal Status Dashboard
cat > scripts/addon_dashboard.sh << 'ADDON9'
#!/usr/bin/env bash
# addon_dashboard.sh — One-shot terminal status display
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   PENNSYLVANIA ACA AUDIT PACKET — STATUS DASHBOARD     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
version=$(cat VERSION 2>/dev/null || echo "unknown")
tag=$(git describe --tags --always 2>/dev/null || echo "none")
echo "  Version:  $version"
echo "  Tag:      $tag"
echo ""
branch=$(git branch --show-current 2>/dev/null || echo "detached")
dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
ahead=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "?")
behind=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo "?")
echo "  Branch:   $branch (dirty: $dirty, ahead: $ahead, behind: $behind)"
echo ""
total_files=$(find . -type f -not -path './.git/*' -not -path './__pycache__/*' -not -path './.pytest_cache/*' | wc -l | tr -d ' ')
py_files=$(find . -name '*.py' -not -path './.git/*' | wc -l | tr -d ' ')
csv_files=$(find . -name '*.csv' -not -path './.git/*' | wc -l | tr -d ' ')
md_files=$(find . -name '*.md' -not -path './.git/*' | wc -l | tr -d ' ')
echo "  Files:    $total_files total ($py_files .py, $csv_files .csv, $md_files .md)"
echo ""
test_count=$(grep -c 'def test_' tests/test_packet.py 2>/dev/null || echo 0)
echo "  Tests:    $test_count defined in test_packet.py"
echo ""
if [ -d "/data/user/0" ]; then
    df -h /data/user/0 2>/dev/null | tail -1 | awk '{printf "  Storage:  %s used of %s (%s) on /data/user/0\n", $3, $2, $5}'
else
    df -h / 2>/dev/null | tail -1 | awk '{printf "  Storage:  %s used of %s (%s) on /\n", $3, $2, $5}'
fi
echo ""
last_commit=$(git log -1 --format="%h %s (%ar)" 2>/dev/null || echo "n/a")
echo "  Last:     $last_commit"
echo ""
echo "══════════════════════════════════════════════════════════"
ADDON9

# ADD-ON 10: Release Checklist Runner (hash_manifest LAST for idempotency)
cat > scripts/addon_release_checklist.sh << 'ADDON10'
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
ADDON10

# Make all executable
chmod +x scripts/addon_*.sh
echo ""
echo "=== INSTALL COMPLETE ==="
echo ""
echo "  10 add-on scripts installed:"
echo "    addon_storage_health.sh      — Dual-mount bytes/inode probe"
echo "    addon_git_hygiene.sh         — Repo cleanliness & tag verification"
echo "    addon_manifest_drift.sh      — Hash drift detection (no rewrite)"
echo "    addon_clean_caches.sh        — Remove __pycache__, .pytest_cache, etc."
echo "    addon_snapshot.sh            — Timestamped tarball archive"
echo "    addon_dep_audit.sh           — Verify stdlib-only (no pip deps)"
echo "    addon_xref_validate.sh       — HANDOVER.json vs calc_results.json"
echo "    addon_gen_changelog.sh       — Auto-generate CHANGELOG from git log"
echo "    addon_dashboard.sh           — One-shot terminal status display"
echo "    addon_release_checklist.sh   — Full validation pipeline runner"
