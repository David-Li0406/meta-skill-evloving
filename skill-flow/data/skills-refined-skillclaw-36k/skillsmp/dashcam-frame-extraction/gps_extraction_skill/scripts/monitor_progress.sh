#!/bin/bash
################################################################################
# Monitor GPS Extraction Progress
#
# Usage: ./monitor_progress.sh
################################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"

echo "GPS Extraction Progress Monitor"
echo "Press Ctrl+C to exit"
echo ""

while true; do
    clear
    echo "======================================================================="
    echo "GPS EXTRACTION PROGRESS - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "======================================================================="
    echo ""

    # GPU Status
    if command -v nvidia-smi &> /dev/null; then
        echo "GPU Status:"
        nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader | \
            awk -F', ' '{printf "  Utilization: %s | Memory: %s / %s | Temp: %s\n", $1, $2, $3, $4}'
        echo ""
    fi

    # Progress from logs
    if [ -d "$SCRIPT_DIR/logs" ]; then
        PROGRESS_FILES=$(find "$SCRIPT_DIR/logs" -name "progress_shard_*.log" 2>/dev/null)
        if [ -n "$PROGRESS_FILES" ]; then
            TOTAL_PROCESSED=$(wc -l $PROGRESS_FILES 2>/dev/null | tail -1 | awk '{print $1}')
            echo "Images Processed: ${TOTAL_PROCESSED:-0}"
            echo ""
        fi
    fi

    # Latest log entries
    if [ -f "$SCRIPT_DIR/logs/extraction.log" ]; then
        echo "Recent Log Entries:"
        tail -10 "$SCRIPT_DIR/logs/extraction.log" | sed 's/^/  /'
    fi

    echo ""
    echo "======================================================================="

    sleep 2
done
