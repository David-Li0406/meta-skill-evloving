#!/usr/bin/env bash
set -euo pipefail

TMP_DIR=$(mktemp -d)
PROJECT_DIR="$TMP_DIR/project"
RUN_LOG="$TMP_DIR/run.log"

resolve_looper_bin() {
    if [ -n "${LOOPER_BIN:-}" ]; then
        printf "%s" "$LOOPER_BIN"
        return 0
    fi

    if command -v looper >/dev/null 2>&1; then
        command -v looper
        return 0
    fi

    # Check for local build
    if [ -x "./bin/looper" ]; then
        printf "%s" "./bin/looper"
        return 0
    fi

    # Check if we can run via go
    if command -v go >/dev/null 2>&1; then
        # Use go run if available
        printf "%s" "go run github.com/nibzard/looper-go/cmd/looper"
        return 0
    fi

    if [ -n "${LOOPER_REPO:-}" ] && [ -x "$LOOPER_REPO/bin/looper" ]; then
        printf "%s" "$LOOPER_REPO/bin/looper"
        return 0
    fi

    echo "Error: looper binary not found. Set LOOPER_BIN, build with 'go build ./cmd/looper', or add to PATH." >&2
    return 1
}

log_contains() {
    local pattern="$1"
    local file="$2"
    if command -v rg >/dev/null 2>&1; then
        rg -m 1 "$pattern" "$file" || true
    else
        grep -m 1 "$pattern" "$file" || true
    fi
}

LOOPER_BIN=$(resolve_looper_bin)

mkdir -p "$PROJECT_DIR"

cat > "$PROJECT_DIR/PROJECT.md" <<'EOF'
# Smoke Test Project

Goal: verify looper runs one iteration and updates to-do.json.
EOF

cat > "$PROJECT_DIR/to-do.json" <<'EOF'
{
  "schema_version": 1,
  "project": {
    "name": "Smoke Test",
    "root": "."
  },
  "source_files": ["PROJECT.md"],
  "tasks": [
    {
      "id": "T10",
      "title": "Create hello.txt",
      "priority": 1,
      "status": "todo"
    },
    {
      "id": "T2",
      "title": "Add README.md",
      "priority": 1,
      "status": "todo"
    }
  ]
}
EOF

(
    cd "$PROJECT_DIR"
    # Use LOOPER_MAX_ITERATIONS for looper-go
    LOOPER_MAX_ITERATIONS=1 $LOOPER_BIN run 2>&1 | tee "$RUN_LOG" || true
)

echo "Temp project: $PROJECT_DIR"
echo "Run log: $RUN_LOG"
echo "Selected task: $(log_contains "^Task:" "$RUN_LOG")"
echo "Summary: $(log_contains "^Summary:" "$RUN_LOG")"

if command -v jq >/dev/null 2>&1; then
    echo "Task statuses:"
    jq -r '.tasks[] | "\(.id)\t\(.status)\t\(.title)"' "$PROJECT_DIR/to-do.json"
else
    echo "to-do.json:"
    cat "$PROJECT_DIR/to-do.json"
fi
