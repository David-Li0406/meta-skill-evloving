# Integration Test Suite

Comprehensive integration tests for the OpenShift Cluster Health MCP Server.

## Overview

The `integration_test.sh` script tests all MCP server functionality across **all release branches**:
- `main` - Latest features (includes Prompts capability)
- `release-4.18` - OpenShift 4.18 compatible
- `release-4.19` - OpenShift 4.19 compatible
- `release-4.20` - OpenShift 4.20 compatible

## Features

### Version-Aware Testing
The script automatically detects which branch it's running on and adapts tests accordingly:
- **Prompts capability** - Only tested on `main` branch (new feature)
- **Coordination Engine tools** - Tested if CE is enabled
- **Core functionality** - Tested on all branches

### Test Coverage

1. **Server Health** - Basic health and readiness checks
2. **MCP Capabilities** - Validates tools, resources, and prompts capabilities
3. **Tools Listing** - Verifies all expected tools are registered
4. **Resources Listing** - Verifies all expected resources are available
5. **Prompts Listing** - Validates prompts (main branch only)
6. **Session Management** - Tests session creation and lifecycle
7. **Tool Execution** - Tests tool invocation with sessions
8. **Resource Read** - Tests resource access with sessions
9. **Cache Performance** - Validates caching and hit rates
10. **Coordination Engine** - Tests CE features if enabled
11. **Timeout Enforcement** - Verifies timeout handling

## Prerequisites

### Required Tools
- `curl` - HTTP requests
- `jq` - JSON parsing
- `git` - Branch detection

Install on RHEL/Fedora:
```bash
sudo dnf install curl jq git
```

### Running MCP Server

The server must be running before tests:

```bash
# Build the server
cd /home/lab-user/openshift-cluster-health-mcp
make build

# Start the server
./bin/mcp-server
```

Or use environment variables:
```bash
export MCP_TRANSPORT=http
export MCP_HTTP_HOST=0.0.0.0
export MCP_HTTP_PORT=8080
./bin/mcp-server
```

## Usage

### Basic Usage

Run all tests:
```bash
cd /home/lab-user/openshift-cluster-health-mcp
./test/integration_test.sh
```

### Custom Server URL

Test against a different server:
```bash
MCP_SERVER_HOST=192.168.1.100 MCP_SERVER_PORT=9090 ./test/integration_test.sh
```

### Testing Coordination Engine Features

Enable Coordination Engine before starting the server:
```bash
export ENABLE_COORDINATION_ENGINE=true
export COORDINATION_ENGINE_URL=http://coordination-engine:8081
./bin/mcp-server
```

Then run tests:
```bash
./test/integration_test.sh
```

## Running Tests on Different Branches

### On main branch (with Prompts)
```bash
git checkout main
./bin/mcp-server &
./test/integration_test.sh
```

Expected output:
```
Branch: main
OpenShift Version: main
✅ Prompts capability: true (NEW!)
✅ Found 6 prompts: diagnose-cluster-issues, investigate-pods, ...
```

### On release-4.20
```bash
git checkout release-4.20
./bin/mcp-server &
./test/integration_test.sh
```

Expected output:
```
Branch: release-4.20
OpenShift Version: 4.20
⚠️  Prompts capability: false (expected on main branch only)
[SKIP] Prompts not supported on branch release-4.20
```

### On release-4.19
```bash
git checkout release-4.19
./bin/mcp-server &
./test/integration_test.sh
```

### On release-4.18
```bash
git checkout release-4.18
./bin/mcp-server &
./test/integration_test.sh
```

## Test Output

### Success Example
```
==========================================
  MCP Server Integration Test Suite
==========================================

Branch: main
OpenShift Version: main
Server URL: http://localhost:8080

[PASS] Server health endpoint responds
[PASS] Server ready endpoint responds

[PASS] MCP server name: openshift-cluster-health-mcp, version: 0.1.0
[PASS] Tools capability: true
[PASS] Resources capability: true
[PASS] Prompts capability: true (NEW!)

[PASS] Found 8 tools: get-cluster-health, list-pods, ...
[PASS] NEW: Coordination Engine tool 'get-remediation-recommendations' present

[PASS] Found 4 resources: cluster://health, cluster://nodes, ...
[PASS] NEW: Coordination Engine resource 'cluster://remediation-history' present

[PASS] Found 6 prompts: diagnose-cluster-issues, investigate-pods, ...

==========================================
  Test Summary
==========================================

Passed: 35
Failed: 0

✅ All tests passed!
```

### Failure Example
```
[FAIL] Server health endpoint responds - HTTP 404
[FAIL] MCP capabilities - HTTP 500

==========================================
  Test Summary
==========================================

Passed: 10
Failed: 2

❌ Some tests failed
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_SERVER_HOST` | `localhost` | MCP server hostname |
| `MCP_SERVER_PORT` | `8080` | MCP server port |
| `MCP_SERVER_URL` | `http://localhost:8080` | Full server URL (overrides host/port) |

## Exit Codes

- `0` - All tests passed
- `1` - Some tests failed or server not running

## Troubleshooting

### Server not running
```
[FAIL] MCP server is not running at http://localhost:8080

Please start the server first:
  cd /home/lab-user/openshift-cluster-health-mcp
  ./bin/mcp-server
```

**Solution:** Start the MCP server in another terminal.

### jq command not found
```
./test/integration_test.sh: line 42: jq: command not found
```

**Solution:** Install jq:
```bash
sudo dnf install jq
```

### Permission denied
```
bash: ./test/integration_test.sh: Permission denied
```

**Solution:** Make the script executable:
```bash
chmod +x ./test/integration_test.sh
```

### Prompts tests fail on release branches
This is **expected behavior**. Prompts are only available on the `main` branch. On release branches, you'll see:
```
[SKIP] Prompts not supported on branch release-4.20 (expected on main only)
```

### Coordination Engine tests skipped
If you see:
```
[SKIP] Coordination Engine not enabled (set ENABLE_COORDINATION_ENGINE=true)
```

Start the server with CE enabled:
```bash
export ENABLE_COORDINATION_ENGINE=true
export COORDINATION_ENGINE_URL=http://coordination-engine:8081
./bin/mcp-server
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Integration Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.24'

      - name: Build MCP Server
        run: make build

      - name: Start MCP Server
        run: ./bin/mcp-server &
        env:
          MCP_TRANSPORT: http

      - name: Wait for server
        run: sleep 5

      - name: Run Integration Tests
        run: ./test/integration_test.sh
```

### Jenkins Example
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'make build'
            }
        }
        stage('Test') {
            steps {
                sh './bin/mcp-server &'
                sh 'sleep 5'
                sh './test/integration_test.sh'
            }
        }
    }
}
```

## Performance Benchmarks

Expected performance targets:

| Metric | Target | Notes |
|--------|--------|-------|
| Health check | < 50ms | Basic endpoint |
| Capabilities | < 100ms | Metadata only |
| Resource read (cached) | < 100ms | Cache hit |
| Resource read (uncached) | < 1s | Fresh data |
| Tool execution | < 5s | Simple tools |
| Prompt generation | < 100ms | Template rendering |

## Adding New Tests

To add a new test:

1. Create a test function:
```bash
test_my_new_feature() {
    log_info "Test N: My New Feature"

    # Your test logic here
    if some_condition; then
        log_success "Feature works"
    else
        log_error "Feature broken"
    fi
}
```

2. Call it in `main()`:
```bash
main() {
    # ... existing tests ...
    test_my_new_feature
    echo ""
    # ...
}
```

3. Use helper functions:
   - `http_get(url, description)` - GET request
   - `http_post(url, data, description)` - POST request
   - `log_success(message)` - Mark test as passed
   - `log_error(message)` - Mark test as failed
   - `log_skip(message)` - Skip test
   - `detect_prompts_support()` - Check if prompts available
   - `detect_coordination_engine()` - Check if CE enabled

## Branch-Specific Testing

The script uses automatic branch detection to adapt tests. To add branch-specific logic:

```bash
if [[ "$CURRENT_BRANCH" =~ release-4\.18 ]]; then
    # 4.18-specific tests
elif [[ "$CURRENT_BRANCH" == "main" ]]; then
    # main branch tests (latest features)
else
    # Common tests
fi
```

Or use feature detection:
```bash
if detect_prompts_support; then
    # Test prompts (available on main)
else
    log_skip "Prompts not available on this branch"
fi
```

## Contributing

When adding new MCP server features:

1. Add corresponding tests to `integration_test.sh`
2. Use feature detection for version compatibility
3. Update this README with new test descriptions
4. Ensure tests pass on all release branches

## Support

For issues or questions:
- GitHub Issues: https://github.com/openshift-aiops/openshift-cluster-health-mcp/issues
- Documentation: https://github.com/openshift-aiops/openshift-cluster-health-mcp/tree/main/docs
