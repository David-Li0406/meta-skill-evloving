#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)
ARTIFACTS_DIR="$REPO_ROOT/artifacts/codex"
REPORT="$ARTIFACTS_DIR/format-report.txt"
TARGET=${DOTNET_FORMAT_TARGET:-infra-monitor.slnx}
EXTRA_ARGS=("$@")

mkdir -p "$ARTIFACTS_DIR"

{
  echo "dotnet format verification report"
  echo "Target: $TARGET"
  echo "Args: ${EXTRA_ARGS[*]:-(none)}"
  echo
  echo "== dotnet format (verify-no-changes) =="
} > "$REPORT"

set +e
(dotnet format "$TARGET" --verify-no-changes "${EXTRA_ARGS[@]}") >> "$REPORT" 2>&1
FORMAT_STATUS=$?

{
  echo
  echo "== dotnet format analyzers (verify-no-changes) =="
} >> "$REPORT"

(dotnet format analyzers "$TARGET" --verify-no-changes "${EXTRA_ARGS[@]}") >> "$REPORT" 2>&1
ANALYZER_STATUS=$?
set -e

if [[ $FORMAT_STATUS -ne 0 || $ANALYZER_STATUS -ne 0 ]]; then
  echo "One or more checks failed. See $REPORT for details." >&2
  exit 1
fi

echo "All format/analyzer checks passed. Report: $REPORT"
