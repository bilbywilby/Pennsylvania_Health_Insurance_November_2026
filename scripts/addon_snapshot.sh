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
