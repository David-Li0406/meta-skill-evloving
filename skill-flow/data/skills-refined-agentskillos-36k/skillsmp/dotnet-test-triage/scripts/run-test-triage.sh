#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)
ARTIFACTS_DIR="$REPO_ROOT/artifacts/codex"
RESULTS_DIR="$ARTIFACTS_DIR/test-results"
OUTPUT_MD="$ARTIFACTS_DIR/test-failures.md"
OUTPUT_FILTER="$ARTIFACTS_DIR/test-filter.txt"
PARSER="$REPO_ROOT/.codex/skills/dotnet-test-triage/scripts/collect-test-failures.py"

mkdir -p "$RESULTS_DIR"

DOTNET_TEST_CMD=${DOTNET_TEST_CMD:-dotnet test}
read -r -a DOTNET_CMD <<< "$DOTNET_TEST_CMD"
DOTNET_CMD+=("$@")
DOTNET_CMD+=(--results-directory "$RESULTS_DIR" -- --report-trx)

set +e
"${DOTNET_CMD[@]}"
TEST_STATUS=$?
set -e

python3 "$PARSER" "$RESULTS_DIR" "$OUTPUT_MD" "$OUTPUT_FILTER"

exit $TEST_STATUS
