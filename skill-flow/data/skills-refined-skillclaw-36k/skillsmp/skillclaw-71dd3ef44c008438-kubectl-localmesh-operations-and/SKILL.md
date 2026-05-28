---
name: kubectl-localmesh-operations-and-testing
description: Use this skill when you need to manage and test the kubectl-localmesh environment, including Envoy configuration and service operations.
---

# Skill body

## Overview

This skill provides guidance on managing the kubectl-localmesh environment, including starting services, managing configurations, and running snapshot tests for Envoy settings.

## Allowed Tools

- Bash
- Read

## Starting kubectl-localmesh

To start kubectl-localmesh as a kubectl plugin (recommended, with automatic /etc/hosts updates, requires sudo):

```bash
sudo kubectl localmesh -f services.yaml
```

To run directly:

```bash
# If built via Task or go install
sudo ./bin/kubectl-localmesh -f services.yaml

# If built directly with go
sudo ./kubectl-localmesh -f services.yaml
```

## Managing /etc/hosts

### Disable Automatic Updates

To disable automatic updates to /etc/hosts:

```bash
kubectl localmesh -f services.yaml --update-hosts=false
```

When disabled, specify the Host header manually:

```bash
curl -H "Host: users-api.localhost" http://127.0.0.1:80/
```

### Accessing Services

#### With Automatic /etc/hosts Updates (Default)

- **HTTP**: `curl http://billing-api.localhost/health`
- **gRPC**: `grpcurl -plaintext users-api.localhost list`

#### Without Automatic Updates

```bash
# HTTP
curl -H "Host: billing-api.localhost" http://127.0.0.1:80/health

# gRPC
grpcurl -plaintext -authority users-api.localhost 127.0.0.1:80 list
```

## Stopping and Cleaning Up

To stop kubectl-localmesh, use **Ctrl+C**. This will automatically:

- Remove /etc/hosts entries
- Stop all port-forward processes
- Stop the Envoy process
- Delete temporary directories

### Verify Clean Exit

Check that no entries remain in /etc/hosts:

```bash
grep "kubectl-localmesh" /etc/hosts
```

Check for remaining port-forward processes:

```bash
ps aux | grep "kubectl port-forward"
```

Check for remaining Envoy processes:

```bash
ps aux | grep envoy
```

## Snapshot Testing

### When to Run Snapshot Tests

Run snapshot tests in the following scenarios:

1. After changing Envoy configuration generation logic.
2. After modifying mapping generation logic.
3. Before creating a pull request to ensure all changes are as intended.
4. Before committing to verify no unintended impacts on other settings.

### Running Tests

To run all snapshot tests:

```bash
testdata/envoy-snapshots/scripts/run-snapshots.sh
```

**Prerequisites:**
- Ensure the binary is built with `task build`.
- The binary `bin/kubectl-localmesh` must exist.

### Updating Snapshots

To update snapshots when expected behavior changes:

```bash
testdata/envoy-snapshots/scripts/update-snapshots.sh
```

**Always review changes:**

```bash
git diff testdata/envoy-snapshots/testdata/snapshots/
git diff testdata/envoy-snapshots/testdata/portforward-mappings/
```

### Troubleshooting

#### Port Conflict

**Symptoms**: `address already in use` error.

**Solution**:
1. Change `listener_port` in services.yaml.
2. Stop existing processes using the port.

```bash
# Check which process is using port 80
lsof -i :80

# Stop the process
kill <PID>
```

#### Envoy Startup Failure

**Symptoms**: Envoy process exits immediately.

**Solution**:
1. Check Envoy configuration.
2. Review debug logs.

```bash
# Dump Envoy configuration
./kubectl-localmesh --dump-envoy-config -f services.yaml > /tmp/envoy-config.yaml

# Validate Envoy configuration
envoy --mode validate -c /tmp/envoy-config.yaml

# Check debug logs
sudo ./kubectl-localmesh -f services.yaml -log debug
```