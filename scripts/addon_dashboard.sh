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
