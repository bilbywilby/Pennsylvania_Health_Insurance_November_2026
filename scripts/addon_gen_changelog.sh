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
