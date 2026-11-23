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
