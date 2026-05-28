#!/bin/bash
set -euo pipefail

# Comprehensive code review orchestrator
# Detects languages and runs appropriate linters, analyzers, and custom checks

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-.}"
OUTPUT_DIR="${2:-.code-review-output}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔍 Code Review Starting${NC}"
echo "Target: $TARGET_DIR"
echo "Output: $OUTPUT_DIR"
echo ""

mkdir -p "$OUTPUT_DIR"

# Detect project types
HAS_PACKAGE_JSON=false
HAS_TSCONFIG=false
HAS_REQUIREMENTS=false
HAS_PYPROJECT=false
HAS_CARGO_TOML=false

[[ -f "$TARGET_DIR/package.json" ]] && HAS_PACKAGE_JSON=true
[[ -f "$TARGET_DIR/tsconfig.json" ]] && HAS_TSCONFIG=true
[[ -f "$TARGET_DIR/requirements.txt" ]] && HAS_REQUIREMENTS=true
[[ -f "$TARGET_DIR/pyproject.toml" ]] && HAS_PYPROJECT=true
[[ -f "$TARGET_DIR/Cargo.toml" ]] && HAS_CARGO_TOML=true

# JavaScript/TypeScript Review
if [[ "$HAS_PACKAGE_JSON" == true ]]; then
  echo -e "${GREEN}📦 JavaScript/TypeScript Project Detected${NC}"

  cd "$TARGET_DIR"

  # ESLint
  if command -v npx &> /dev/null && [[ -f ".eslintrc.json" || -f ".eslintrc.js" || -f "eslint.config.js" ]]; then
    echo "Running ESLint..."
    npx eslint . --format json --output-file "$OUTPUT_DIR/eslint-report.json" 2>/dev/null || true

    if [[ -f "$OUTPUT_DIR/eslint-report.json" ]]; then
      ESLINT_ERRORS=$(jq '[.[] | select(.errorCount > 0)] | length' "$OUTPUT_DIR/eslint-report.json" 2>/dev/null || echo "0")
      echo -e "  ${YELLOW}Found $ESLINT_ERRORS files with errors${NC}"
    fi
  fi

  # TypeScript compiler check
  if [[ "$HAS_TSCONFIG" == true ]] && command -v npx &> /dev/null; then
    echo "Running TypeScript compiler check..."
    npx tsc --noEmit > "$OUTPUT_DIR/tsc-errors.txt" 2>&1 || true

    if [[ -s "$OUTPUT_DIR/tsc-errors.txt" ]]; then
      ERROR_COUNT=$(grep -c "error TS" "$OUTPUT_DIR/tsc-errors.txt" || echo "0")
      echo -e "  ${YELLOW}Found $ERROR_COUNT TypeScript errors${NC}"
    else
      echo -e "  ${GREEN}No TypeScript errors${NC}"
    fi
  fi

  cd - > /dev/null
  echo ""
fi

# Python Review
if [[ "$HAS_REQUIREMENTS" == true ]] || [[ "$HAS_PYPROJECT" == true ]]; then
  echo -e "${GREEN}🐍 Python Project Detected${NC}"

  cd "$TARGET_DIR"

  # Pylint
  if command -v pylint &> /dev/null; then
    echo "Running Pylint..."
    find . -name "*.py" -not -path "*/venv/*" -not -path "*/.venv/*" -not -path "*/node_modules/*" | \
      xargs pylint --output-format=json > "$OUTPUT_DIR/pylint-report.json" 2>/dev/null || true
  fi

  # Flake8
  if command -v flake8 &> /dev/null; then
    echo "Running Flake8..."
    flake8 . --exclude=venv,.venv,node_modules --format=json > "$OUTPUT_DIR/flake8-report.json" 2>/dev/null || true
  fi

  # MyPy
  if command -v mypy &> /dev/null; then
    echo "Running MyPy type checker..."
    mypy . --ignore-missing-imports > "$OUTPUT_DIR/mypy-report.txt" 2>&1 || true
  fi

  cd - > /dev/null
  echo ""
fi

# Rust Review
if [[ "$HAS_CARGO_TOML" == true ]]; then
  echo -e "${GREEN}🦀 Rust Project Detected${NC}"

  cd "$TARGET_DIR"

  # Clippy
  if command -v cargo &> /dev/null; then
    echo "Running Clippy..."
    cargo clippy --message-format=json > "$OUTPUT_DIR/clippy-report.json" 2>&1 || true

    # Check for warnings/errors
    if [[ -f "$OUTPUT_DIR/clippy-report.json" ]]; then
      CLIPPY_WARNINGS=$(grep -c '"level":"warning"' "$OUTPUT_DIR/clippy-report.json" || echo "0")
      echo -e "  ${YELLOW}Found $CLIPPY_WARNINGS Clippy warnings${NC}"
    fi
  fi

  cd - > /dev/null
  echo ""
fi

# Run custom analyzers
echo -e "${BLUE}🔬 Running Custom Analysis${NC}"

# Complexity analysis
if command -v python3 &> /dev/null && [[ -f "$SCRIPT_DIR/analyze_complexity.py" ]]; then
  echo "Analyzing code complexity..."
  python3 "$SCRIPT_DIR/analyze_complexity.py" "$TARGET_DIR" > "$OUTPUT_DIR/complexity-report.json" 2>/dev/null || true
fi

# Code smells detection
if command -v python3 &> /dev/null && [[ -f "$SCRIPT_DIR/detect_code_smells.py" ]]; then
  echo "Detecting code smells..."
  python3 "$SCRIPT_DIR/detect_code_smells.py" "$TARGET_DIR" > "$OUTPUT_DIR/code-smells-report.json" 2>/dev/null || true
fi

echo ""

# Generate final report
echo -e "${BLUE}📊 Generating Review Report${NC}"

if command -v python3 &> /dev/null && [[ -f "$SCRIPT_DIR/generate_review_report.py" ]]; then
  python3 "$SCRIPT_DIR/generate_review_report.py" "$OUTPUT_DIR" > "$OUTPUT_DIR/REVIEW.md"
  echo -e "${GREEN}✅ Review complete!${NC}"
  echo ""
  echo "Results saved to: $OUTPUT_DIR/REVIEW.md"
  echo ""

  # Show summary
  if [[ -f "$OUTPUT_DIR/REVIEW.md" ]]; then
    echo -e "${BLUE}Summary:${NC}"
    head -n 20 "$OUTPUT_DIR/REVIEW.md"
  fi
else
  echo -e "${YELLOW}⚠️  Report generator not found, raw results in $OUTPUT_DIR${NC}"
fi

echo ""
echo -e "${GREEN}Review complete! Check $OUTPUT_DIR for detailed results.${NC}"
