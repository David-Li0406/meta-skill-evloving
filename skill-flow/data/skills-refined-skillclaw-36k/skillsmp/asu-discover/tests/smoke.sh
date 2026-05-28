#!/usr/bin/env bash
# smoke.sh - Regression smoke tests for asu-discover skill
# Covers brittle points: set -e interactions, YAML parsing, pattern loading, DNS detection
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export SKILL_DIR
cd "$SKILL_DIR"

# Test counters
PASSED=0
FAILED=0
SKIPPED=0

# Colors (disable if not tty)
if [[ -t 1 ]]; then
    GREEN='\033[0;32m'
    RED='\033[0;31m'
    YELLOW='\033[0;33m'
    NC='\033[0m'
else
    GREEN='' RED='' YELLOW='' NC=''
fi

pass() { ((PASSED++)) || true; echo -e "${GREEN}✓${NC} $1"; }
fail() { ((FAILED++)) || true; echo -e "${RED}✗${NC} $1"; }
skip() { ((SKIPPED++)) || true; echo -e "${YELLOW}-${NC} $1 (skipped: $2)"; }

# Run command, expect success
run() {
    local name="$1"; shift
    if "$@" >/dev/null 2>&1; then
        pass "$name"
    else
        fail "$name"
    fi
}

# Run command, expect failure
run_expect_fail() {
    local name="$1"; shift
    if "$@" >/dev/null 2>&1; then
        fail "$name"
    else
        pass "$name"
    fi
}

# Run command, expect output to contain string
run_expect_output() {
    local name="$1"
    local expected="$2"
    shift 2
    local output
    if output=$("$@" 2>&1) && [[ "$output" == *"$expected"* ]]; then
        pass "$name"
    else
        fail "$name"
    fi
}

# Source libraries for direct function tests
source "$SKILL_DIR/scripts/lib/db.sh"
source "$SKILL_DIR/scripts/lib/yaml.sh"
SCRIPT_DIR="$SKILL_DIR/scripts"  # Required by dns.sh
source "$SKILL_DIR/scripts/lib/dns.sh"

echo "=== asu-discover Smoke Tests ==="
echo ""

# -----------------------------------------------------------------------------
# Prerequisites
# -----------------------------------------------------------------------------
echo "--- Prerequisites ---"

# Check yq is installed (required dependency)
if command -v yq &>/dev/null; then
    pass "yq installed"
else
    echo "ERROR: yq is required. Install with: brew install yq"
    exit 1
fi

DB_EXISTS=false
if db_exists; then
    pass "db exists"
    DB_EXISTS=true
else
    skip "db exists" "run 'index build' first"
fi
echo ""

# -----------------------------------------------------------------------------
# Index Operations (require DB)
# -----------------------------------------------------------------------------
echo "--- Index Operations ---"
if $DB_EXISTS; then
    run "index stats" ./scripts/discover.sh index stats
    run "get_repo_count --all" bash -c "source scripts/lib/db.sh && [[ \$(get_repo_count --all) -gt 0 ]]"
    run "get_repo_count --active" bash -c "source scripts/lib/db.sh && [[ \$(get_repo_count --active) -ge 0 ]]"
    run "get_repo_count --archived" bash -c "source scripts/lib/db.sh && [[ \$(get_repo_count --archived) -ge 0 ]]"
    run "get_prefix_stats" bash -c "source scripts/lib/db.sh && get_prefix_stats 5"
else
    skip "index stats" "no db"
    skip "get_repo_count --all" "no db"
    skip "get_repo_count --active" "no db"
    skip "get_repo_count --archived" "no db"
    skip "get_prefix_stats" "no db"
fi
echo ""

# -----------------------------------------------------------------------------
# Pattern Loading
# -----------------------------------------------------------------------------
echo "--- Pattern Loading ---"
run "pattern --list" ./scripts/discover.sh pattern --list
run "pattern --name eel" ./scripts/discover.sh pattern --name eel
run "pattern --name eel --brief" ./scripts/discover.sh pattern --name eel --brief
run "pattern --name vault --type typescript" ./scripts/discover.sh pattern --name vault --type typescript
run_expect_fail "pattern --name nonexistent" ./scripts/discover.sh pattern --name nonexistent
echo ""

# -----------------------------------------------------------------------------
# YAML Parsing
# -----------------------------------------------------------------------------
echo "--- YAML Parsing ---"
run "yaml_validate" yaml_validate "$SKILL_DIR/config/domains.yaml"
run "yaml_get_all_patterns" bash -c "export DOMAINS_YAML='$SKILL_DIR/config/domains.yaml' && source $SKILL_DIR/scripts/lib/yaml.sh && [[ -n \$(yaml_get_all_patterns) ]]"
run "yaml_get_domain_field" bash -c "export DOMAINS_YAML='$SKILL_DIR/config/domains.yaml' && source $SKILL_DIR/scripts/lib/yaml.sh && [[ -n \$(yaml_get_domain_field peoplesoft triggers) ]]"
echo ""

# -----------------------------------------------------------------------------
# DNS Commands
# -----------------------------------------------------------------------------
echo "--- DNS Commands ---"
run_expect_output "dns-validate *.asu.edu → infoblox" "infoblox" ./scripts/discover.sh dns-validate --domain test.asu.edu
run_expect_output "dns-validate *.example.com → cloudflare" "cloudflare" ./scripts/discover.sh dns-validate --domain test.example.com
run "dns-examples" ./scripts/discover.sh dns-examples
echo ""

# -----------------------------------------------------------------------------
# Search/Context (require DB)
# -----------------------------------------------------------------------------
echo "--- Search/Context ---"
if $DB_EXISTS; then
    run "search --local-only" ./scripts/discover.sh search --query "terraform" --local-only
    run "context --local-only" ./scripts/discover.sh context --query "kafka" --local-only
    run "expand" ./scripts/discover.sh expand --query "vault"
else
    skip "search --local-only" "no db"
    skip "context --local-only" "no db"
    skip "expand" "no db"
fi
echo ""

# -----------------------------------------------------------------------------
# Edge Cases
# -----------------------------------------------------------------------------
echo "--- Edge Cases ---"
if $DB_EXISTS; then
    # Test SQL escaping with special characters
    run "search with special chars" ./scripts/discover.sh search --query "test'with;chars" --local-only
fi

# Test index verify with --dry-run (no API calls needed)
run "index verify --dry-run" ./scripts/discover.sh index verify --dry-run
run "index verify --dry-run --limit 3" ./scripts/discover.sh index verify --dry-run --limit 3

if ! $DB_EXISTS; then
    skip "search with special chars" "no db"
fi
echo ""

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo "=== Results: ${PASSED} passed, ${FAILED} failed, ${SKIPPED} skipped ==="
exit $((FAILED > 0 ? 1 : 0))
