# Manual OpenShift Deployment Workflow

This guide explains how to manually test and deploy to OpenShift clusters using GitHub Actions.

## Overview

The `openshift-deploy.yml` workflow allows maintainers to:
- Test the MCP server against real OpenShift clusters
- Validate OpenShift-specific features (ClusterVersion, SCCs)
- Deploy to OpenShift clusters for pre-release validation

## Prerequisites

1. **OpenShift Cluster Access**:
   - OpenShift 4.18, 4.19, or 4.20 cluster
   - Cluster admin or namespace admin access

2. **Authentication Token**:
   ```bash
   # Get your OpenShift token
   oc whoami -t
   ```

3. **GitHub Permissions**:
   - Write access to the repository (maintainers only)

## Usage

### Step 1: Trigger Workflow

1. Go to [Actions → OpenShift Deploy](https://github.com/tosin2013/openshift-cluster-health-mcp/actions/workflows/openshift-deploy.yml)
2. Click **Run workflow**
3. Fill in the inputs:
   - **openshift_server**: Your cluster API URL (e.g., `https://api.cluster.example.com:6443`)
   - **openshift_token**: Your authentication token from `oc whoami -t`
   - **namespace**: Target namespace (default: `self-healing-platform`)
   - **deploy**: Check this to deploy after testing (default: false)
   - **openshift_version**: Select your OpenShift version

### Step 2: Monitor Execution

1. Click on the running workflow
2. Watch the logs for:
   - ✅ OpenShift connectivity verified
   - ✅ Integration tests passed
   - ✅ Deployment successful (if enabled)

### Step 3: Verify Deployment

If deployment was enabled:
```bash
# Check pods
oc get pods -n self-healing-platform

# Check logs
oc logs -l app=mcp-server -n self-healing-platform

# Test MCP server
oc port-forward -n self-healing-platform svc/mcp-server 8080:8080
curl http://localhost:8080/health
```

## When to Use This Workflow

**Use for:**
- ✅ Pre-release validation against real OpenShift
- ✅ Testing OpenShift-specific features
- ✅ Deploying to development/staging OpenShift clusters
- ✅ Validating version compatibility (4.18, 4.19, 4.20)

**Don't use for:**
- ❌ Regular PR testing (use automated CI with Kind)
- ❌ Production deployments (use proper release process)

## Security Notes

- **Token Security**: The OpenShift token is NOT stored as a GitHub secret. You must provide it each time you run the workflow.
- **Token Scope**: Use a service account token with minimal required permissions:
  ```bash
  # Create service account with limited scope
  oc create sa mcp-deployer -n self-healing-platform
  oc policy add-role-to-user edit system:serviceaccount:self-healing-platform:mcp-deployer
  oc sa get-token mcp-deployer -n self-healing-platform
  ```
- **Access Control**: Only repository maintainers can trigger this workflow.

## Troubleshooting

**Connection Failed**:
- Verify cluster URL is correct (include port 6443)
- Check token hasn't expired: `oc whoami`
- Ensure network access to cluster API

**Tests Failed**:
- Check pod logs: `kubectl logs -l app=mcp-server`
- Verify RBAC permissions
- Check OpenShift version compatibility

**Deployment Failed**:
- Verify namespace exists or can be created
- Check Helm chart compatibility
- Review deployment logs in GitHub Actions
