#!/bin/bash
# ==============================================================================
# Step NN: [STEP TITLE]
# ==============================================================================
# PRP Deliverable: [Which deliverable this implements]
# Gate: [Which gate this belongs to]
# Depends on: [Previous step(s) if any]
# ==============================================================================
# INTENT:
# [Clear description of what this step accomplishes]
# ==============================================================================
# Invariants: INV-70 (LF), INV-71 (mkdir), INV-72 (bash 3.2), INV-76 (python3)
# ==============================================================================

set -e

PROJECT_ROOT="${PROJECT_ROOT:-$(dirname "$0")/..}"
cd "$PROJECT_ROOT"

# INV-74: Verify project root
if [[ ! -f "$PROJECT_ROOT/pyproject.toml" ]] && [[ ! -f "$PROJECT_ROOT/package.json" ]] && [[ ! -f "$PROJECT_ROOT/app.py" ]]; then
    echo "ERROR: PROJECT_ROOT ($PROJECT_ROOT) doesn't look like a project root"
    exit 1
fi

echo "=== Step NN: [STEP TITLE] ==="

# INV-71: Helper function for safe file writes
write_file() {
    mkdir -p "$(dirname "$1")"
    cat > "$1"
}

# ============================================================
# Step Implementation
# ============================================================

# TODO: Implementation here

# ============================================================
# Verification
# ============================================================

echo ""
echo "Step NN complete."
echo "Created/modified:"
echo "  - [file1]"
