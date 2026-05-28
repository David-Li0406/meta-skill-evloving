#!/usr/bin/env bash
# CTRF utilities using jq for deterministic test report analysis
# See: lefant-claude-code-plugins/lefant/skills/test-analyzer/skill.md

set -euo pipefail

usage() {
  cat <<EOF
Usage: ctrf-utils.sh <command> [args...]

Commands:
  summary <file>           Show pass/fail summary
  failures <file...>       List failed test names
  failures-detail <file>   Show failures with error messages
  flaky <file>             Show tests with retry attempts
  slowest <N> <file>       Show N slowest tests (default: 10)

Examples:
  ctrf-utils.sh summary /workspace/artifacts/test/vitest.ctrf.json
  ctrf-utils.sh failures-detail /workspace/artifacts/test/*.ctrf.json
  ctrf-utils.sh slowest 5 /workspace/artifacts/test/vitest.ctrf.json

Full jq reference: lefant-claude-code-plugins/lefant/skills/test-analyzer/skill.md
EOF
  exit 1
}

if ! command -v jq >/dev/null 2>&1; then
  echo "Error: jq is required but not installed"
  exit 1
fi

COMMAND="${1:-}"
shift || usage

case "$COMMAND" in
  summary)
    FILE="${1:-}"
    [[ -z "$FILE" ]] && usage
    jq -r '.results.summary |
      "Tests: \(.tests // 0) | Passed: \(.passed // 0) | Failed: \(.failed // 0) | Skipped: \(.skipped // 0) | Duration: \(.duration // 0)ms"' \
      "$FILE"
    ;;

  failures)
    FILES="${@}"
    [[ -z "$FILES" ]] && usage
    jq -r '.results.tests[] | select(.status == "failed") | .name' $FILES 2>/dev/null || true
    ;;

  failures-detail)
    FILES="${@}"
    [[ -z "$FILES" ]] && usage
    jq -r '.results.tests[] | select(.status == "failed") |
      "❌ \(.name)\n   Suite: \(.suite // "N/A")\n   Error: \(.message // "No message")\n   File: \(.filePath // "N/A"):\(.line // "?")\n"' \
      $FILES 2>/dev/null || true
    ;;

  flaky)
    FILE="${1:-}"
    [[ -z "$FILE" ]] && usage
    jq -r '.results.tests[] | select(.retries > 0 or .flaky == true) |
      "⚠️  \(.name) (retries: \(.retries // 0))"' \
      "$FILE" 2>/dev/null || true
    ;;

  slowest)
    N="${1:-10}"
    FILE="${2:-}"
    [[ -z "$FILE" ]] && usage
    jq -r --argjson n "$N" '.results.tests | sort_by(.duration) | reverse |
      limit($n; .[]) | "⏱️  \(.duration)ms - \(.name)"' \
      "$FILE" 2>/dev/null || true
    ;;

  *)
    usage
    ;;
esac
