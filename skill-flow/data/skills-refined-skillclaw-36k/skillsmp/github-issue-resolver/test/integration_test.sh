#!/bin/bash
set -e

# MCP Server Integration Test Script
# Works across all release branches (4.18, 4.19, 4.20, main)
# Tests MCP server capabilities, prompts, resources, and tools

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test configuration
MCP_SERVER_HOST="${MCP_SERVER_HOST:-localhost}"
MCP_SERVER_PORT="${MCP_SERVER_PORT:-8080}"
MCP_SERVER_URL="http://${MCP_SERVER_HOST}:${MCP_SERVER_PORT}"
SESSION_ID=""
TEST_RESULTS=()
TESTS_PASSED=0
TESTS_FAILED=0

# Detect current branch and version
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
OPENSHIFT_VERSION=""

if [[ "$CURRENT_BRANCH" =~ release-4\.18 ]]; then
    OPENSHIFT_VERSION="4.18"
elif [[ "$CURRENT_BRANCH" =~ release-4\.19 ]]; then
    OPENSHIFT_VERSION="4.19"
elif [[ "$CURRENT_BRANCH" =~ release-4\.20 ]]; then
    OPENSHIFT_VERSION="4.20"
else
    OPENSHIFT_VERSION="main"
fi

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
    TEST_RESULTS+=("PASS: $1")
    ((TESTS_PASSED++))
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
    TEST_RESULTS+=("FAIL: $1")
    ((TESTS_FAILED++))
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_skip() {
    echo -e "${YELLOW}[SKIP]${NC} $1"
}

# HTTP request helper with error handling
http_get() {
    local url="$1"
    local description="$2"
    local response
    local http_code

    response=$(curl -s -w "\n%{http_code}" "$url" 2>/dev/null)
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)

    if [[ "$http_code" == "200" ]]; then
        echo "$body"
        return 0
    else
        log_error "$description - HTTP $http_code"
        return 1
    fi
}

http_post() {
    local url="$1"
    local data="$2"
    local description="$3"
    local response
    local http_code

    response=$(curl -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -d "$data" "$url" 2>/dev/null)
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)

    if [[ "$http_code" == "200" ]] || [[ "$http_code" == "201" ]]; then
        echo "$body"
        return 0
    else
        log_error "$description - HTTP $http_code"
        return 1
    fi
}

# Feature detection - check if prompts are available
detect_prompts_support() {
    local caps
    caps=$(http_get "$MCP_SERVER_URL/mcp/capabilities" "Capabilities check" 2>/dev/null)

    if echo "$caps" | jq -e '.capabilities.prompts == true' > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Feature detection - check if Coordination Engine is enabled
detect_coordination_engine() {
    local tools
    tools=$(http_get "$MCP_SERVER_URL/mcp/tools" "Tools check" 2>/dev/null)

    if echo "$tools" | jq -e '.tools[] | select(.name == "list-incidents")' > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Test 1: Server health check
test_server_health() {
    log_info "Test 1: Server Health Check"

    if http_get "$MCP_SERVER_URL/health" "Health endpoint" > /dev/null; then
        log_success "Server health endpoint responds"
    fi

    if http_get "$MCP_SERVER_URL/ready" "Ready endpoint" > /dev/null; then
        log_success "Server ready endpoint responds"
    fi
}

# Test 2: MCP capabilities
test_mcp_capabilities() {
    log_info "Test 2: MCP Capabilities"

    local caps
    if caps=$(http_get "$MCP_SERVER_URL/mcp/capabilities" "MCP capabilities"); then
        local name=$(echo "$caps" | jq -r '.name')
        local version=$(echo "$caps" | jq -r '.version')
        local tools=$(echo "$caps" | jq -r '.capabilities.tools')
        local resources=$(echo "$caps" | jq -r '.capabilities.resources')
        local prompts=$(echo "$caps" | jq -r '.capabilities.prompts')

        log_success "MCP server name: $name, version: $version"
        log_success "Tools capability: $tools"
        log_success "Resources capability: $resources"

        if [[ "$prompts" == "true" ]]; then
            log_success "Prompts capability: $prompts (NEW!)"
        else
            log_warn "Prompts capability: $prompts (expected on main branch only)"
        fi
    fi
}

# Test 3: Tools listing
test_tools_listing() {
    log_info "Test 3: Tools Listing"

    local tools
    if tools=$(http_get "$MCP_SERVER_URL/mcp/tools" "Tools listing"); then
        local count=$(echo "$tools" | jq -r '.count')
        local tool_names=$(echo "$tools" | jq -r '.tools[].name' | tr '\n' ', ' | sed 's/,$//')

        log_success "Found $count tools: $tool_names"

        # Check for expected core tools
        if echo "$tools" | jq -e '.tools[] | select(.name == "get-cluster-health")' > /dev/null; then
            log_success "Core tool 'get-cluster-health' present"
        fi

        if echo "$tools" | jq -e '.tools[] | select(.name == "list-pods")' > /dev/null; then
            log_success "Core tool 'list-pods' present"
        fi

        # Check for new CE tools (may not exist on all branches)
        if echo "$tools" | jq -e '.tools[] | select(.name == "get-remediation-recommendations")' > /dev/null; then
            log_success "NEW: Coordination Engine tool 'get-remediation-recommendations' present"
        fi

        if echo "$tools" | jq -e '.tools[] | select(.name == "create-incident")' > /dev/null; then
            log_success "NEW: Coordination Engine tool 'create-incident' present"
        fi
    fi
}

# Test 4: Resources listing
test_resources_listing() {
    log_info "Test 4: Resources Listing"

    local resources
    if resources=$(http_get "$MCP_SERVER_URL/mcp/resources" "Resources listing"); then
        local count=$(echo "$resources" | jq -r '.count')
        local resource_uris=$(echo "$resources" | jq -r '.resources[].uri' | tr '\n' ', ' | sed 's/,$//')

        log_success "Found $count resources: $resource_uris"

        # Check for expected core resources
        if echo "$resources" | jq -e '.resources[] | select(.uri == "cluster://health")' > /dev/null; then
            log_success "Core resource 'cluster://health' present"
        fi

        if echo "$resources" | jq -e '.resources[] | select(.uri == "cluster://nodes")' > /dev/null; then
            log_success "Core resource 'cluster://nodes' present"
        fi

        # Check for new CE resource (may not exist on all branches)
        if echo "$resources" | jq -e '.resources[] | select(.uri == "cluster://remediation-history")' > /dev/null; then
            log_success "NEW: Coordination Engine resource 'cluster://remediation-history' present"
        fi
    fi
}

# Test 5: Prompts listing (version-aware)
test_prompts_listing() {
    log_info "Test 5: Prompts Listing"

    if detect_prompts_support; then
        local prompts
        if prompts=$(http_get "$MCP_SERVER_URL/mcp/prompts" "Prompts listing"); then
            local count=$(echo "$prompts" | jq -r '.count')
            local prompt_names=$(echo "$prompts" | jq -r '.prompts[].name' | tr '\n' ', ' | sed 's/,$//')

            log_success "Found $count prompts: $prompt_names"

            # Check for expected prompts
            local expected_prompts=("diagnose-cluster-issues" "investigate-pods" "check-anomalies" "optimize-data-access")
            for prompt_name in "${expected_prompts[@]}"; do
                if echo "$prompts" | jq -e ".prompts[] | select(.name == \"$prompt_name\")" > /dev/null; then
                    log_success "Core prompt '$prompt_name' present"
                else
                    log_warn "Core prompt '$prompt_name' not found"
                fi
            done

            # Check for CE prompts
            if echo "$prompts" | jq -e '.prompts[] | select(.name == "predict-and-prevent")' > /dev/null; then
                log_success "NEW: CE prompt 'predict-and-prevent' present"
            fi

            if echo "$prompts" | jq -e '.prompts[] | select(.name == "correlate-incidents")' > /dev/null; then
                log_success "NEW: CE prompt 'correlate-incidents' present"
            fi
        fi
    else
        log_skip "Prompts not supported on branch $CURRENT_BRANCH (expected on main only)"
    fi
}

# Test 6: Session management
test_session_management() {
    log_info "Test 6: Session Management"

    # Create session
    local session
    if session=$(http_post "$MCP_SERVER_URL/mcp/session" '{}' "Session creation"); then
        SESSION_ID=$(echo "$session" | jq -r '.session_id')
        local ttl=$(echo "$session" | jq -r '.ttl_seconds')

        log_success "Session created: $SESSION_ID (TTL: ${ttl}s)"

        # Get session info
        if http_get "$MCP_SERVER_URL/mcp/session?sessionid=$SESSION_ID" "Session info" > /dev/null; then
            log_success "Session info retrieved successfully"
        fi
    fi
}

# Test 7: Tool execution (with session)
test_tool_execution() {
    log_info "Test 7: Tool Execution"

    if [[ -z "$SESSION_ID" ]]; then
        log_warn "No session ID, skipping tool execution test"
        return
    fi

    # Test get-cluster-health tool
    local tool_url="$MCP_SERVER_URL/mcp/tools/get-cluster-health/call?sessionid=$SESSION_ID"
    local result

    if result=$(http_post "$tool_url" '{"include_details": false}' "get-cluster-health tool"); then
        local status=$(echo "$result" | jq -r '.result.status // .result.overall_status')
        log_success "get-cluster-health executed: status=$status"
    fi
}

# Test 8: Resource read (with session)
test_resource_read() {
    log_info "Test 8: Resource Read"

    if [[ -z "$SESSION_ID" ]]; then
        log_warn "No session ID, skipping resource read test"
        return
    fi

    # Test cluster://health resource
    local resource_url="$MCP_SERVER_URL/mcp/resources/health/read?sessionid=$SESSION_ID"
    local result

    if result=$(http_post "$resource_url" '{}' "cluster://health resource"); then
        local status=$(echo "$result" | jq -r '.content.status // .content.overall_status')
        log_success "cluster://health read successfully: status=$status"
    fi
}

# Test 9: Cache performance
test_cache_performance() {
    log_info "Test 9: Cache Performance"

    local cache_stats
    if cache_stats=$(http_get "$MCP_SERVER_URL/cache/stats" "Cache statistics"); then
        local hits=$(echo "$cache_stats" | jq -r '.hits // 0')
        local misses=$(echo "$cache_stats" | jq -r '.misses // 0')
        local hit_rate=$(echo "$cache_stats" | jq -r '.hit_rate_percent // 0')

        log_success "Cache stats - Hits: $hits, Misses: $misses, Hit Rate: ${hit_rate}%"

        # Test cache by reading same resource twice
        if [[ -n "$SESSION_ID" ]]; then
            local resource_url="$MCP_SERVER_URL/mcp/resources/health/read?sessionid=$SESSION_ID"

            # First read (cache miss expected)
            local start1=$(date +%s%N)
            http_post "$resource_url" '{}' "First read" > /dev/null
            local end1=$(date +%s%N)
            local duration1=$(( (end1 - start1) / 1000000 ))

            # Second read (cache hit expected)
            local start2=$(date +%s%N)
            http_post "$resource_url" '{}' "Second read" > /dev/null
            local end2=$(date +%s%N)
            local duration2=$(( (end2 - start2) / 1000000 ))

            log_success "First read: ${duration1}ms, Second read: ${duration2}ms"

            if [[ $duration2 -lt $duration1 ]]; then
                log_success "Cache is working (second read faster)"
            fi
        fi
    fi
}

# Test 10: Coordination Engine features (if available)
test_coordination_engine() {
    log_info "Test 10: Coordination Engine Features"

    if detect_coordination_engine; then
        log_success "Coordination Engine integration detected"

        # Test list-incidents tool if session available
        if [[ -n "$SESSION_ID" ]]; then
            local incidents_url="$MCP_SERVER_URL/mcp/tools/list-incidents/call?sessionid=$SESSION_ID"
            if http_post "$incidents_url" '{"status": "active", "severity": "all"}' "list-incidents tool" > /dev/null; then
                log_success "Coordination Engine tool execution successful"
            fi
        fi

        # Test cluster://incidents resource if session available
        if [[ -n "$SESSION_ID" ]]; then
            local resource_url="$MCP_SERVER_URL/mcp/resources/incidents/read?sessionid=$SESSION_ID"
            if http_post "$resource_url" '{}' "cluster://incidents resource" > /dev/null; then
                log_success "Coordination Engine resource read successful"
            fi
        fi
    else
        log_skip "Coordination Engine not enabled (set ENABLE_COORDINATION_ENGINE=true)"
    fi
}

# Test 11: Timeout enforcement
test_timeout_enforcement() {
    log_info "Test 11: Timeout Enforcement"

    # The timeout is configured at 10 seconds, so this test just verifies
    # that requests don't hang indefinitely
    if [[ -n "$SESSION_ID" ]]; then
        local tool_url="$MCP_SERVER_URL/mcp/tools/get-cluster-health/call?sessionid=$SESSION_ID"

        local start=$(date +%s)
        http_post "$tool_url" '{}' "Timeout test" > /dev/null || true
        local end=$(date +%s)
        local duration=$((end - start))

        if [[ $duration -lt 15 ]]; then
            log_success "Request completed within timeout window (${duration}s < 15s)"
        else
            log_error "Request took too long: ${duration}s (possible timeout issue)"
        fi
    fi
}

# Main test execution
main() {
    echo ""
    echo "=========================================="
    echo "  MCP Server Integration Test Suite"
    echo "=========================================="
    echo ""
    echo "Branch: $CURRENT_BRANCH"
    echo "OpenShift Version: $OPENSHIFT_VERSION"
    echo "Server URL: $MCP_SERVER_URL"
    echo ""

    # Check if server is running
    if ! curl -s "$MCP_SERVER_URL/health" > /dev/null 2>&1; then
        log_error "MCP server is not running at $MCP_SERVER_URL"
        echo ""
        echo "Please start the server first:"
        echo "  cd /home/lab-user/openshift-cluster-health-mcp"
        echo "  ./bin/mcp-server"
        echo ""
        exit 1
    fi

    log_success "MCP server is running"
    echo ""

    # Run all tests
    test_server_health
    echo ""

    test_mcp_capabilities
    echo ""

    test_tools_listing
    echo ""

    test_resources_listing
    echo ""

    test_prompts_listing
    echo ""

    test_session_management
    echo ""

    test_tool_execution
    echo ""

    test_resource_read
    echo ""

    test_cache_performance
    echo ""

    test_coordination_engine
    echo ""

    test_timeout_enforcement
    echo ""

    # Print summary
    echo "=========================================="
    echo "  Test Summary"
    echo "=========================================="
    echo ""
    echo -e "${GREEN}Passed:${NC} $TESTS_PASSED"
    echo -e "${RED}Failed:${NC} $TESTS_FAILED"
    echo ""

    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo -e "${GREEN}✅ All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}❌ Some tests failed${NC}"
        exit 1
    fi
}

# Run main function
main "$@"
