# Scripts Directory

This directory contains utility scripts for OpenShift Cluster Health MCP development and deployment.

## Available Scripts

### `setup-github-actions-sa.sh`

Creates a service account with read-only cluster access for GitHub Actions CI/CD integration.

**Purpose:**
- Enables GitHub Actions to run integration tests against your OpenShift cluster
- Creates a long-lived service account token (1 year)
- Configures minimal read-only permissions following principle of least privilege

**Prerequisites:**
- `oc` CLI installed and configured
- Logged in to OpenShift cluster with admin permissions
- Cluster admin access (to create ClusterRole and ClusterRoleBinding)

**Usage:**

```bash
# Run the script
./scripts/setup-github-actions-sa.sh

# Follow the prompts
# Copy the generated OPENSHIFT_SERVER and OPENSHIFT_TOKEN
# Add them to GitHub repository secrets
```

**What it does:**

1. Creates service account `github-actions-sa` in `default` namespace
2. Creates ClusterRole `github-actions-readonly` with permissions:
   - Read pods, nodes, namespaces, events
   - Read deployments, statefulsets, daemonsets
   - Read KServe InferenceServices
   - Read OpenShift routes and projects
3. Creates ClusterRoleBinding to bind the role to service account
4. Generates a 1-year token for the service account
5. Outputs the token and cluster URL for GitHub Secrets

**Security:**

The service account has **read-only** access:
- ✅ Can list and get cluster resources
- ✅ Can watch for resource changes
- ❌ Cannot create, update, or delete resources
- ❌ Cannot execute commands in pods
- ❌ Cannot access secrets or configmaps

**Testing the service account:**

```bash
# Test read permissions (should work)
oc auth can-i get pods --as=system:serviceaccount:default:github-actions-sa
oc auth can-i list nodes --as=system:serviceaccount:default:github-actions-sa

# Test write permissions (should fail)
oc auth can-i delete pods --as=system:serviceaccount:default:github-actions-sa
oc auth can-i create deployments --as=system:serviceaccount:default:github-actions-sa
```

**Token Rotation:**

The token expires after 1 year. To rotate:

```bash
# Delete the old service account and recreate
oc delete sa github-actions-sa -n default
./scripts/setup-github-actions-sa.sh

# Update the OPENSHIFT_TOKEN secret in GitHub
```

## Adding More Scripts

When adding new scripts to this directory:

1. Make them executable: `chmod +x scripts/your-script.sh`
2. Add a shebang: `#!/bin/bash`
3. Include error handling: `set -euo pipefail`
4. Document usage with comments
5. Update this README

## Related Documentation

- [GitHub Actions Setup Guide](../docs/github-actions-setup.md) - Detailed instructions for configuring GitHub Actions
- [RBAC Security Model ADR](../docs/adrs/007-rbac-based-security-model.md) - Security architecture decisions
