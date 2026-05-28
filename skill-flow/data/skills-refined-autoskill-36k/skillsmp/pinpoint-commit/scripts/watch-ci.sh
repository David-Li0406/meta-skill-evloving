#!/usr/bin/env bash
# Monitor GitHub Actions CI for a PR with timeout

set -euo pipefail

PR_NUMBER="${1:-}"
TIMEOUT_SECONDS="${2:-600}"  # Default 10 minutes

if [ -z "$PR_NUMBER" ]; then
    echo "Usage: $0 <pr-number> [timeout-seconds]"
    exit 1
fi

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo "Error: gh CLI not found. See installation instructions at: https://cli.github.com/manual/installation"
    exit 1
fi

echo "⏳ Monitoring CI for PR #$PR_NUMBER (timeout: ${TIMEOUT_SECONDS}s)..."

start_time=$(date +%s)
check_interval=30

while true; do
    current_time=$(date +%s)
    elapsed=$((current_time - start_time))

    if [ $elapsed -gt $TIMEOUT_SECONDS ]; then
        echo ""
        echo "⏱️  Timeout after ${elapsed}s"
        echo "Some checks may still be running."
        echo "View status: gh pr checks $PR_NUMBER"
        exit 2
    fi

    # Get check status
    checks_json=$(gh pr checks "$PR_NUMBER" --json name,status,conclusion 2>/dev/null || echo "[]")

    if [ "$checks_json" = "[]" ]; then
        echo "[$(printf '%02d:%02d' $((elapsed/60)) $((elapsed%60)))] No checks found yet..."
        sleep $check_interval
        continue
    fi

    # Parse checks with jq
    total_checks=$(echo "$checks_json" | jq '. | length')
    completed_checks=$(echo "$checks_json" | jq '[.[] | select(.status == "COMPLETED")] | length')
    success_checks=$(echo "$checks_json" | jq '[.[] | select(.conclusion == "SUCCESS")] | length')
    failed_checks=$(echo "$checks_json" | jq '[.[] | select(.conclusion == "FAILURE")] | length')

    # Print status
    echo "[$(printf '%02d:%02d' $((elapsed/60)) $((elapsed%60)))] Checks: $completed_checks/$total_checks complete, $success_checks passed, $failed_checks failed"

    # Check if all completed
    if [ "$completed_checks" -eq "$total_checks" ]; then
        echo ""
        if [ "$failed_checks" -gt 0 ]; then
            echo "❌ CI checks failed ($failed_checks failed)"
            echo ""
            echo "Failed checks:"
            echo "$checks_json" | jq -r '.[] | select(.conclusion == "FAILURE") | "  - \(.name)"'
            exit 1
        else
            echo "✅ All CI checks passed! (${elapsed}s)"
            exit 0
        fi
    fi

    sleep $check_interval
done
