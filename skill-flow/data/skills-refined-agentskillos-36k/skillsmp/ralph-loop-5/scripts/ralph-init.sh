#!/bin/bash
#
# Ralph Init - Initialize a Ralph loop in the current directory
#
# Usage: ralph-init.sh "Task specification..."
#

set -euo pipefail

# Colors
if [[ -t 1 ]] && [[ -z "${NO_COLOR:-}" ]]; then
  GREEN='\033[0;32m'
  YELLOW='\033[0;33m'
  CYAN='\033[0;36m'
  BOLD='\033[1m'
  NC='\033[0m'
else
  GREEN='' YELLOW='' CYAN='' BOLD='' NC=''
fi

log() { echo -e "${CYAN}[ralph-init]${NC} $*"; }
log_success() { echo -e "${GREEN}[ralph-init]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[ralph-init]${NC} $*"; }

RALPH_DIR=".ralph"

# Parse arguments
SPEC=""
MAX_ITERATIONS=25
MAX_ATTEMPTS=5
COMPLETION_PROMISE="DONE"

while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      cat << 'EOF'
Ralph Init - Initialize a Ralph loop

Usage: ralph-init.sh [options] "Task specification..."

Options:
  -h, --help              Show this help
  -n, --max-iterations N  Maximum iterations (default: 25)
  -a, --max-attempts N    Max attempts before blocking (default: 5)
  -p, --promise TEXT      Completion promise (default: DONE)

Example:
  ralph-init.sh "Build a REST API with CRUD. Tests must pass." --promise "ALL_TESTS_PASS"
EOF
      exit 0
      ;;
    -n|--max-iterations)
      MAX_ITERATIONS="$2"
      shift 2
      ;;
    -a|--max-attempts)
      MAX_ATTEMPTS="$2"
      shift 2
      ;;
    -p|--promise)
      COMPLETION_PROMISE="$2"
      shift 2
      ;;
    *)
      # Accumulate non-option args as spec
      if [[ -n "$SPEC" ]]; then
        SPEC="$SPEC $1"
      else
        SPEC="$1"
      fi
      shift
      ;;
  esac
done

if [[ -z "$SPEC" ]]; then
  echo "Error: No task specification provided" >&2
  echo "Usage: ralph-init.sh \"Your task specification...\"" >&2
  exit 1
fi

# Check if already initialized
if [[ -d "$RALPH_DIR" ]]; then
  log_warn "Ralph directory already exists"
  echo ""
  read -p "Reset and reinitialize? [y/N] " -n 1 -r
  echo ""
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log "Aborted"
    exit 0
  fi
  rm -rf "$RALPH_DIR"
fi

# Create directory structure
log "Creating .ralph/ directory structure..."
mkdir -p "$RALPH_DIR/evidence"

# Create spec file
cat > "$RALPH_DIR/spec.md" << EOF
# Task Specification

$SPEC

---

## Success Criteria

When the task is complete, output: \`<promise>$COMPLETION_PROMISE</promise>\`

Only output this when the statement is genuinely TRUE. Do not lie to exit the loop.
EOF

# Create state file
cat > "$RALPH_DIR/state.json" << EOF
{
  "iteration": 0,
  "attempts": 0,
  "status": "pending",
  "max_iterations": $MAX_ITERATIONS,
  "max_attempts": $MAX_ATTEMPTS,
  "completion_promise": "$COMPLETION_PROMISE",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

# Create progress log
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Ralph loop initialized" > "$RALPH_DIR/progress.log"

# Create .gitignore for ralph directory
cat > "$RALPH_DIR/.gitignore" << 'EOF'
# Ignore iteration logs (can be large)
evidence/*.log

# Keep structure visible
!.gitkeep
EOF

# Create .gitkeep in evidence
touch "$RALPH_DIR/evidence/.gitkeep"

log_success "Ralph loop initialized!"
echo ""
echo "Directory structure:"
echo "  $RALPH_DIR/"
echo "  ├── spec.md          # Your task specification"
echo "  ├── state.json       # Loop state"
echo "  ├── progress.log     # Progress tracking"
echo "  └── evidence/        # Iteration logs"
echo ""
echo "Configuration:"
echo "  Max iterations: $MAX_ITERATIONS"
echo "  Max attempts:   $MAX_ATTEMPTS"
echo "  Promise:        $COMPLETION_PROMISE"
echo ""
echo "${BOLD}To run the loop:${NC}"
echo "  ~/.claude/skills/ralph-loop/scripts/ralph.sh"
echo ""
echo "Or with options:"
echo "  ~/.claude/skills/ralph-loop/scripts/ralph.sh --verbose"
echo ""
echo "${BOLD}To monitor:${NC}"
echo "  tail -f $RALPH_DIR/progress.log"
echo "  cat $RALPH_DIR/state.json | jq ."
