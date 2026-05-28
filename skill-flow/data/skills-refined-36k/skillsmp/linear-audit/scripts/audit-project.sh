#!/usr/bin/env bash
# linear-audit: audit-project.sh
# Single project audit with 4-specialist fanout

set -euo pipefail

# Parse arguments
TEAM="${1:-}"
MODE="${2:-full}"

if [ -z "$TEAM" ]; then
  echo "Usage: audit-project.sh <TEAM> [mode]"
  echo "  TEAM: ARB, KUM, KOT, SIN, WEB, SAY, SQU, PAL, UTI"
  echo "  mode: full (default), quick, report"
  exit 1
fi

# Map team to project path
get_project_path() {
  case $1 in
    ARB) echo ~/Developer/arbor/arbor-xyz ;;
    KUM) echo ~/Developer/kumori/kumori-xyz ;;
    KOT) echo ~/Developer/koto/koto-xyz ;;
    SIN) echo ~/Developer/sine/sine-xyz ;;
    WEB) echo ~/Developer/webs/webs-xyz ;;
    SAY) echo ~/Developer/saya/saya-xyz ;;
    SQU) echo ~/Developer/squish/squish-xyz ;;
    PAL) echo ~/Developer/pal/pal-xyz ;;
    UTI) echo ~/Developer/utils ;;
    *) echo "unknown" ;;
  esac
}

PROJECT_PATH=$(get_project_path "$TEAM")

if [ "$PROJECT_PATH" = "unknown" ]; then
  echo "Error: Unknown team $TEAM"
  exit 1
fi

if [ ! -d "$PROJECT_PATH" ]; then
  echo "Error: Project path does not exist: $PROJECT_PATH"
  exit 1
fi

# Detect project type
detect_project_type() {
  local path=$1
  if [ -d "$path/convex" ]; then
    echo "convex-next"
  elif [ -f "$path/Cargo.toml" ]; then
    echo "cli"
  elif ls -d "$path"/*.xcodeproj 2>/dev/null | head -1 >/dev/null; then
    echo "swift"
  else
    echo "generic"
  fi
}

PROJECT_TYPE=$(detect_project_type "$PROJECT_PATH")

# Create audit directory
AUDIT_DIR="$HOME/.agents/audits/$TEAM-$(date +%Y%m%d)"
mkdir -p "$AUDIT_DIR/briefs"

echo "=== Linear Audit: $TEAM ==="
echo "Project: $PROJECT_PATH"
echo "Type: $PROJECT_TYPE"
echo "Mode: $MODE"
echo "Output: $AUDIT_DIR"
echo ""

# Quick mode: just counts
if [ "$MODE" = "quick" ]; then
  echo "=== Quick Audit ==="

  # Issue counts
  echo "Issue Distribution:"
  linear issue list --team "$TEAM" --json -q | jq 'group_by(.state.name) | map({state: .[0].state.name, count: length})' || echo "Failed to fetch issues"

  # Context check (sample)
  echo ""
  echo "Context Check (sample of 10):"
  SAMPLE=$(linear issue list --team "$TEAM" --limit 10 --json -q | jq -r '.[].identifier')
  WITH_CONTEXT=0
  WITHOUT_CONTEXT=0
  for ISSUE in $SAMPLE; do
    MARKERS=$(linear comment list "$ISSUE" --json -q 2>/dev/null | jq -r '.[].body' | grep -c "issue-context:" || echo "0")
    if [ "$MARKERS" -gt 0 ]; then
      ((WITH_CONTEXT++))
    else
      ((WITHOUT_CONTEXT++))
    fi
  done
  echo "With context: $WITH_CONTEXT"
  echo "Without context: $WITHOUT_CONTEXT"

  exit 0
fi

# Report mode: read existing audit
if [ "$MODE" = "report" ]; then
  LATEST_AUDIT=$(ls -td "$HOME/.agents/audits/$TEAM-"* 2>/dev/null | head -1)
  if [ -z "$LATEST_AUDIT" ] || [ ! -f "$LATEST_AUDIT/AUDIT.md" ]; then
    echo "No existing audit found for $TEAM"
    exit 1
  fi
  cat "$LATEST_AUDIT/AUDIT.md"
  exit 0
fi

# Full mode: 4-specialist fanout
echo "=== Full Audit (4-specialist fanout) ==="

# Generate parent ID
AUDIT_ID="linear-audit-$(date +%Y%m%d-%H%M%S)-$(openssl rand -hex 4)"
echo "Audit ID: $AUDIT_ID"

# Start trace (if agents CLI available)
if command -v agents &>/dev/null; then
  export AGENTS_TRACE_ID=$(agents report start "linear-audit: $TEAM" --agent claude --json -q 2>/dev/null | jq -r '.traceId' || echo "")
  if [ -n "$AGENTS_TRACE_ID" ]; then
    echo "Trace ID: $AGENTS_TRACE_ID"
  fi
fi

# Change to project directory for code analysis
cd "$PROJECT_PATH"

echo ""
echo "=== Phase 1: Code State ==="
{
  echo "Test Coverage:"
  verify --coverage --json -q 2>/dev/null | jq '.summary' || echo "verify not available"

  echo ""
  echo "Build Status:"
  pnpm build 2>&1 | tail -10 || echo "build failed"

  echo ""
  echo "Type Check:"
  pnpm typecheck 2>&1 | tail -10 || echo "typecheck failed"

  echo ""
  echo "Recent Commits:"
  git log --oneline -10 2>/dev/null || echo "no git history"
} > "$AUDIT_DIR/code-state.txt" 2>&1
echo "Code state analysis complete"

echo ""
echo "=== Phase 2: Architecture ==="
{
  echo "Package Dependencies:"
  layer . --format=json -q 2>/dev/null | jq '.summary' || echo "layer not available"

  echo ""
  echo "Cycle Detection:"
  layer . --check-cycles 2>/dev/null || echo "no cycles or layer not available"

  echo ""
  echo "Dead Code:"
  outline --unused -r 2>&1 | head -20 || echo "outline not available"
} > "$AUDIT_DIR/architecture.txt" 2>&1
echo "Architecture analysis complete"

echo ""
echo "=== Phase 3: Linear State ==="
{
  echo "Issue Distribution:"
  linear issue list --team "$TEAM" --json -q | jq 'group_by(.state.name) | map({state: .[0].state.name, count: length})'

  echo ""
  echo "Context Check:"
  ISSUES=$(linear issue list --team "$TEAM" --limit 30 --json -q | jq -r '.[].identifier')
  WITH_CONTEXT=0
  WITHOUT_CONTEXT=0
  STALE=0

  for ISSUE in $ISSUES; do
    MARKERS=$(linear comment list "$ISSUE" --json -q 2>/dev/null | jq -r '.[].body' | grep -c "issue-context:" || echo "0")
    if [ "$MARKERS" -gt 0 ]; then
      ((WITH_CONTEXT++))
      # Check staleness (simplified - just count)
    else
      ((WITHOUT_CONTEXT++))
      echo "NO_CONTEXT: $ISSUE"
    fi
  done

  echo ""
  echo "Summary:"
  echo "With context: $WITH_CONTEXT"
  echo "Without context: $WITHOUT_CONTEXT"

  echo ""
  echo "Vague Issues (no description):"
  linear issue list --team "$TEAM" --json -q | jq -r '.[] | select(.description == null or .description == "") | .identifier'
} > "$AUDIT_DIR/linear-state.txt" 2>&1
echo "Linear state analysis complete"

echo ""
echo "=== Phase 4: Generating Audit Report ==="

# Generate AUDIT.md
cat > "$AUDIT_DIR/AUDIT.md" << EOF
# $TEAM Linear Audit

**Date**: $(date +%Y-%m-%d)
**Project**: $PROJECT_PATH
**Type**: $PROJECT_TYPE
**Audit ID**: $AUDIT_ID

## Executive Summary

Audit of $TEAM project for V1 readiness. See sections below for details.

---

## Code State

\`\`\`
$(cat "$AUDIT_DIR/code-state.txt")
\`\`\`

---

## Architecture

\`\`\`
$(cat "$AUDIT_DIR/architecture.txt")
\`\`\`

---

## Linear State

\`\`\`
$(cat "$AUDIT_DIR/linear-state.txt")
\`\`\`

---

## Next Steps

1. Enrich issues without context using issue-context skill
2. Address any build/type/lint errors
3. Review and close stale issues
4. Re-audit after fixes

---

Generated by linear-audit skill
EOF

echo "Audit report generated: $AUDIT_DIR/AUDIT.md"

# Report completion
if command -v agents &>/dev/null && [ -n "${AGENTS_TRACE_ID:-}" ]; then
  agents report complete "$TEAM audit complete" --confidence 8 2>/dev/null || true
fi

echo ""
echo "=== Audit Complete ==="
echo "Report: $AUDIT_DIR/AUDIT.md"
echo ""
echo "View with: cat $AUDIT_DIR/AUDIT.md"
