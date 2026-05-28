---
name: kubectl-localmesh-operations-and-testing
description: Use this skill for managing kubectl-localmesh operations, including Envoy protocol configuration, service access, and snapshot testing.
---

# kubectl-localmesh Operations and Snapshot Testing

This skill provides guidance on managing kubectl-localmesh operations and executing snapshot tests for Envoy configurations.

## kubectl-localmesh Operations

### Starting kubectl-localmesh

**Recommended Start as a kubectl Plugin (with automatic /etc/hosts update, requires sudo):**

```bash
sudo kubectl localmesh -f services.yaml
```

**Direct Execution:**
```bash
# If built via Task or go install
sudo ./bin/kubectl-localmesh -f services.yaml

# If built directly with go
sudo ./kubectl-localmesh -f services.yaml
```

### /etc/hosts Management Options

**Disable Automatic Update:**

```bash
kubectl localmesh -f services.yaml --update-hosts=false
```

In this case, manually specify the Host header:
```bash
curl -H "Host: users-api.localhost" http://127.0.0.1:80/
```

### Accessing Services

**When /etc/hosts Update is Enabled (Default):**

- **HTTP**: `curl http://billing-api.localhost/health`
- **gRPC**: `grpcurl -plaintext users-api.localhost list`

**When /etc/hosts Update is Disabled:**

```bash
# HTTP
curl -H "Host: billing-api.localhost" http://127.0.0.1:80/health

# gRPC
grpcurl -plaintext -authority users-api.localhost 127.0.0.1:80 list
```

### Stopping and Cleanup

Stopping with **Ctrl+C** automatically:
- Removes /etc/hosts entries
- Stops all port-forward processes
- Stops Envoy processes
- Deletes temporary directories

### Dependency Check

Before starting, check dependencies:

```bash
# Using the script
.claude/skills/kubectl-localmesh-operations/scripts/check-dependencies.sh

# Or check individually
kubectl version --client
envoy --version
bash --version
```

**Required Dependencies:**
- `kubectl`: Access to Kubernetes cluster
- `envoy`: Local proxy (macOS: `brew install envoy`)
- `bash`: For executing port-forward loop scripts

### Troubleshooting

#### Port Conflict

**Symptoms**: `address already in use` error

**Solution**:
1. Change `listener_port` in services.yaml
2. Or stop existing processes using the port

```bash
# Check processes using port 80
lsof -i :80

# Stop the process
kill <PID>
```

#### Envoy Startup Failure

**Symptoms**: Envoy process exits immediately

**Solution**:
1. Check Envoy configuration (use `kubectl-envoy-debugging` skill)
2. Validate debug logs

```bash
# Dump Envoy configuration
./kubectl-localmesh --dump-envoy-config -f services.yaml > /tmp/envoy-config.yaml

# Validate Envoy configuration
envoy --mode validate -c /tmp/envoy-config.yaml

# Check debug logs
sudo ./kubectl-localmesh -f services.yaml -log debug
```

#### Port-Forward Connection Failure

**Symptoms**: `error forwarding port` error

**Solution**:
1. Confirm service existence
2. Check port name/number
3. Verify kubeconfig and cluster connection

```bash
# Check service existence
kubectl get svc -n <namespace>

# Check service details and ports
kubectl describe svc <service> -n <namespace>

# Verify kubeconfig and cluster connection
kubectl cluster-info
kubectl get nodes
```

#### /etc/hosts Update Failure

**Symptoms**: `permission denied` error

**Solution**:
1. Run with sudo
2. Or use `--update-hosts=false` option

```bash
# Run with sudo
sudo ./kubectl-localmesh -f services.yaml

# Or disable /etc/hosts update
./kubectl-localmesh -f services.yaml --update-hosts=false
```

#### Unable to Access Service

**Symptoms**: `connection refused` or `503 Service Unavailable`

**Troubleshooting Steps**:
1. Check if kubectl-localmesh is running
2. Verify port-forward is functioning
3. Check Envoy logs
4. Use curl to check detailed HTTP headers

```bash
# Check port-forward processes
ps aux | grep "kubectl port-forward"

# Use curl for detailed check
curl -v http://users-api.localhost/
```

## Snapshot Testing

### Overview

kubectl-localmesh dynamically generates Envoy configurations and port-forward mappings. Snapshot testing verifies that these generated results are as expected.

### When to Execute Snapshot Tests

**Mandatory Execution Timing:**
1. After changing Envoy configuration generation logic
2. After changing mapping generation logic
3. After modifying dump-envoy-config implementation
4. Before creating a pull request
5. Before committing changes

### Snapshot Update Timing

**When to Update Snapshots:**
1. When intentionally changing Envoy settings
2. When adding new features that should change snapshots
3. When adding new test cases

**⚠️ Do Not Update Snapshots When:**
1. Tests fail without understanding the cause
2. Updating just to pass tests
3. Not reviewing git diff before updating

### Basic Commands

#### Run Tests

```bash
# Run all snapshot tests
testdata/envoy-snapshots/scripts/run-snapshots.sh
```

**Prerequisites:**
- Ensure `task build` has been executed
- `bin/kubectl-localmesh` must exist

#### Update Snapshots

```bash
# Update all snapshots
testdata/envoy-snapshots/scripts/update-snapshots.sh
```

**After Execution:**
```bash
# Always check diffs
git diff testdata/envoy-snapshots/testdata/snapshots/
git diff testdata/envoy-snapshots/testdata/portforward-mappings/
```

### Workflow Examples

#### New Feature Development

```bash
# 1. Build
task build

# 2. Run snapshot tests (check current state)
testdata/envoy-snapshots/scripts/run-snapshots.sh

# 3. Implement feature
# ... edit code ...

# 4. Build
task build

# 5. Run snapshot tests (check changes)
testdata/envoy-snapshots/scripts/run-snapshots.sh

# 6. If changes are as expected, update snapshots
testdata/envoy-snapshots/scripts/update-snapshots.sh

# 7. Review diffs
git diff testdata/envoy-snapshots/testdata/

# 8. Confirm changes are correct and commit
git add .
git commit -m "feat: Add new feature"
```

#### Bug Fixing

```bash
# 1. Build
task build

# 2. Run snapshot tests (confirm bug reproduction)
testdata/envoy-snapshots/scripts/run-snapshots.sh

# 3. Fix bug
# ... edit code ...

# 4. Build
task build

# 5. Run snapshot tests (confirm fix)
testdata/envoy-snapshots/scripts/run-snapshots.sh

# 6. If tests pass, done (no snapshot update needed)
# If tests fail, confirm why expectations changed
git diff testdata/envoy-snapshots/testdata/

# 7. Update snapshots if necessary
testdata/envoy-snapshots/scripts/update-snapshots.sh
```

## Related Skills

- `go-taskfile-workflow`: Build and test execution
- `kubectl-envoy-debugging`: Debugging Envoy configurations
- `kubectl-localmesh-logging-guide`: Understanding log outputs