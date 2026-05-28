#!/bin/bash
# Ralph v2 Test Utilities
# Source this in test-NN.sh scripts: source ./test-utils.sh

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0
FAILED_TESTS=()

# Colors (if terminal supports)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# ============================================================
# Core Test Functions
# ============================================================

check_file() {
    local file="$1"
    local desc="${2:-File exists: $1}"
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $desc"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $desc"
        echo "  Expected file: $file"
        FAILED_TESTS+=("$desc")
        ((TESTS_FAILED++))
        return 1
    fi
}

check_dir() {
    local dir="$1"
    local desc="${2:-Directory exists: $1}"
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $desc"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $desc"
        echo "  Expected directory: $dir"
        FAILED_TESTS+=("$desc")
        ((TESTS_FAILED++))
        return 1
    fi
}

check_contains() {
    local file="$1"
    local string="$2"
    local desc="${3:-File contains expected content}"
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗${NC} $desc"
        echo "  File not found: $file"
        FAILED_TESTS+=("$desc")
        ((TESTS_FAILED++))
        return 1
    fi
    if grep -q -- "$string" "$file"; then
        echo -e "${GREEN}✓${NC} $desc"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $desc"
        echo "  Expected to find: $string"
        echo "  In file: $file"
        FAILED_TESTS+=("$desc")
        ((TESTS_FAILED++))
        return 1
    fi
}

check_not_contains() {
    local file="$1"
    local string="$2"
    local desc="${3:-File does not contain prohibited content}"
    if [ ! -f "$file" ]; then
        echo -e "${YELLOW}?${NC} $desc (file not found, passing)"
        ((TESTS_PASSED++))
        return 0
    fi
    if grep -q -- "$string" "$file"; then
        echo -e "${RED}✗${NC} $desc"
        echo "  Should NOT contain: $string"
        FAILED_TESTS+=("$desc")
        ((TESTS_FAILED++))
        return 1
    else
        echo -e "${GREEN}✓${NC} $desc"
        ((TESTS_PASSED++))
        return 0
    fi
}

check_command() {
    local cmd="$1"
    local desc="${2:-Command succeeds: $1}"
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $desc"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $desc"
        echo "  Command failed: $cmd"
        FAILED_TESTS+=("$desc")
        ((TESTS_FAILED++))
        return 1
    fi
}

check_output() {
    local cmd="$1"
    local expected="$2"
    local desc="${3:-Command output contains expected}"
    local output
    output=$(eval "$cmd" 2>&1) || true
    if echo "$output" | grep -q -- "$expected"; then
        echo -e "${GREEN}✓${NC} $desc"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $desc"
        echo "  Expected output to contain: $expected"
        echo "  Actual output: $output"
        FAILED_TESTS+=("$desc")
        ((TESTS_FAILED++))
        return 1
    fi
}

check_http() {
    local url="$1"
    local expected="${2:-200}"
    local desc="${3:-HTTP $expected from $url}"
    local status
    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null) || status="000"
    if [ "$status" = "$expected" ]; then
        echo -e "${GREEN}✓${NC} $desc"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $desc"
        echo "  Expected: HTTP $expected"
        echo "  Got: HTTP $status"
        FAILED_TESTS+=("$desc")
        ((TESTS_FAILED++))
        return 1
    fi
}

# INV-76: Python3 check
check_python_import() {
    local module="$1"
    local desc="${2:-Python import: $module}"
    if python3 -c "import $module" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $desc"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $desc"
        echo "  Failed to import: $module"
        FAILED_TESTS+=("$desc")
        ((TESTS_FAILED++))
        return 1
    fi
}

check_python_exec() {
    local code="$1"
    local desc="${2:-Python exec succeeds}"
    if python3 -c "$code" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $desc"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $desc"
        echo "  Python code failed"
        FAILED_TESTS+=("$desc")
        ((TESTS_FAILED++))
        return 1
    fi
}

# ============================================================
# File Writing (INV-71: creates parent dirs)
# ============================================================

write_file() {
    local path="$1"
    mkdir -p "$(dirname "$path")"
    cat > "$path"
}

append_file() {
    local path="$1"
    local content="$2"
    mkdir -p "$(dirname "$path")"
    echo "$content" >> "$path"
}

# ============================================================
# Project Root Verification (INV-74)
# ============================================================

verify_project_root() {
    local root="$1"
    if [[ ! -f "$root/pyproject.toml" ]] && [[ ! -f "$root/package.json" ]] && [[ ! -f "$root/CLAUDE.md" ]] && [[ ! -f "$root/app.py" ]]; then
        echo -e "${RED}ERROR: PROJECT_ROOT ($root) doesn't look like a project root${NC}"
        return 1
    fi
    return 0
}

# ============================================================
# Playwright Verification Output
# ============================================================

playwright_verify() {
    local json="$1"
    cat << PLAYWRIGHT_VERIFY
$json
PLAYWRIGHT_VERIFY
}

# ============================================================
# Report Results
# ============================================================

report_results() {
    echo ""
    echo "============================================"
    echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed"
    echo "============================================"
    if [ $TESTS_FAILED -gt 0 ]; then
        echo ""
        echo "Failed tests:"
        for test in "${FAILED_TESTS[@]}"; do
            echo "  - $test"
        done
        exit 1
    else
        echo "All tests passed!"
        exit 0
    fi
}

# ============================================================
# Dev Server Helpers
# ============================================================

wait_for_server() {
    local url="$1"
    local timeout="${2:-30}"
    local elapsed=0
    echo "Waiting for server at $url..."
    while [ $elapsed -lt $timeout ]; do
        if curl -s --max-time 2 "$url" > /dev/null 2>&1; then
            echo "Server ready after ${elapsed}s"
            return 0
        fi
        sleep 1
        ((elapsed++))
    done
    echo "Server not ready after ${timeout}s"
    return 1
}
