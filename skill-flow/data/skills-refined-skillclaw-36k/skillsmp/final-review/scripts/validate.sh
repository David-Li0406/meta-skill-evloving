#!/bin/bash
# Pop-CLI Final Review Validation Script
# Runs automated checks for code quality

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Track failures
FAILED=0

print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_failure() {
    echo -e "${RED}✗ $1${NC}"
    FAILED=1
}

print_warning() {
    echo -e "${YELLOW}! $1${NC}"
}

print_info() {
    echo -e "${BLUE}→ $1${NC}"
}

# Navigate to project root
cd "$(git rev-parse --show-toplevel)" || exit 1

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                    Pop-CLI Final Review Validation                       ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check 1: Formatting
print_header "1. Checking Code Formatting (cargo +nightly fmt)"

if cargo +nightly fmt --all -- --check 2>/dev/null; then
    print_success "Code formatting is correct"
else
    print_failure "Formatting issues found. Run: cargo +nightly fmt --all"
fi

# Check 2: Clippy
print_header "2. Running Clippy Linter"

if cargo clippy --all-targets --all-features -- -D warnings 2>&1; then
    print_success "Clippy found no warnings"
else
    print_failure "Clippy warnings found"
fi

# Check 3: Unit Tests
print_header "3. Running Unit Tests"

if cargo test --workspace 2>&1; then
    print_success "All unit tests passed"
else
    print_failure "Some unit tests failed"
fi

# Check 4: Documentation
print_header "4. Building Documentation"

if cargo doc --no-deps 2>&1 | grep -v "^$"; then
    print_success "Documentation builds successfully"
else
    print_failure "Documentation build failed"
fi

# Check 5: Check for common issues
print_header "5. Checking for Common Issues"

# Check for unwrap in library code
UNWRAP_COUNT=$(grep -r "\.unwrap()" --include="*.rs" crates/pop-contracts crates/pop-chains crates/pop-common 2>/dev/null | grep -v "#\[test\]" | grep -v "mod tests" | wc -l | tr -d ' ')
if [ "$UNWRAP_COUNT" -gt 0 ]; then
    print_warning "Found $UNWRAP_COUNT potential unwrap() calls in library code"
    echo "         Review these for proper error handling:"
    grep -rn "\.unwrap()" --include="*.rs" crates/pop-contracts crates/pop-chains crates/pop-common 2>/dev/null | grep -v "#\[test\]" | grep -v "mod tests" | head -5
else
    print_success "No unwrap() calls in library code"
fi

# Check for TODO/FIXME comments
TODO_COUNT=$(grep -rE "(TODO|FIXME|XXX|HACK)" --include="*.rs" crates/ 2>/dev/null | wc -l | tr -d ' ')
if [ "$TODO_COUNT" -gt 0 ]; then
    print_warning "Found $TODO_COUNT TODO/FIXME comments"
else
    print_success "No TODO/FIXME comments found"
fi

# Check for debug prints
DEBUG_COUNT=$(grep -rE "(println!|dbg!|eprintln!)" --include="*.rs" crates/ 2>/dev/null | grep -v "#\[test\]" | grep -v "mod tests" | wc -l | tr -d ' ')
if [ "$DEBUG_COUNT" -gt 0 ]; then
    print_warning "Found $DEBUG_COUNT debug print statements"
else
    print_success "No debug print statements found"
fi

# Summary
print_header "Summary"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════════════════╗"
    echo "║                     All automated checks passed!                         ║"
    echo "║                                                                          ║"
    echo "║  Please complete the manual review checklist before committing.          ║"
    echo "╚══════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    exit 0
else
    echo -e "${RED}"
    echo "╔══════════════════════════════════════════════════════════════════════════╗"
    echo "║                    Some checks failed - see above                        ║"
    echo "║                                                                          ║"
    echo "║  Fix the issues before proceeding with commit/PR.                        ║"
    echo "╚══════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    exit 1
fi
