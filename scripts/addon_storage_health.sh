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
