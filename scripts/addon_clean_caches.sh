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
