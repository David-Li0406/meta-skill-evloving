# Container Registry Setup

This document explains how to set up automated container builds and pushes to Quay.io.

## Overview

The GitHub Actions workflow `.github/workflows/container.yml` automatically:

- Builds the container image on every push to `main`
- Pushes images to Quay.io with appropriate tags
- Scans images for security vulnerabilities
- Verifies the container starts correctly

## Required Secrets

You need to configure the following GitHub repository secrets:

### 1. QUAY_USERNAME

Your Quay.io username or robot account name.

**To create a robot account on Quay.io:**

1. Go to <https://quay.io/>
2. Navigate to your organization → Settings → Robot Accounts
3. Click "Create Robot Account"
4. Name it something like `openshift_cluster_health_mcp_ci`
5. Grant it **Write** permissions to the repository
6. Copy the username (format: `organization+robot_name`)

### 2. QUAY_PASSWORD

Your Quay.io password or robot account token.

**For robot account:**

1. When creating the robot account, Quay.io will show you the token
2. Copy this token - you won't be able to see it again!
3. Store it securely

## Setting Up GitHub Secrets

1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret:
   - Name: `QUAY_USERNAME`
   - Value: Your Quay.io username or robot account name
   - Click **Add secret**
   - Repeat for `QUAY_PASSWORD`

## Image Registry Configuration

The workflow is configured to push to:

```
quay.io/takinosh/openshift-cluster-health-mcp
```

**To use your own Quay.io organization:**

1. Edit `.github/workflows/container.yml`
2. Update the `IMAGE_NAMESPACE` environment variable:

   ```yaml
   env:
     IMAGE_NAMESPACE: your-quay-username  # Change this
   ```

## Image Tags

The workflow creates multiple tags:

| Tag Type | Example | When Created |
|----------|---------|--------------|
| Git SHA | `main-abc1234-20260101-120000` | Every push to main |
| Branch | `main` | Every push to branch |
| Latest | `latest` | Push to main branch only |
| Version | `v1.0.0`, `1.0`, `1` | When you create git tags |
| PR | `pr-123` | On pull requests (build only) |

## Creating a Release

To create a versioned release:

```bash
# Tag your release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

This will create the following tags on Quay.io:

- `v1.0.0`
- `1.0`
- `1`
- `latest`

## Pulling Images

### Latest development build

```bash
podman pull quay.io/takinosh/openshift-cluster-health-mcp:latest
```

### Specific version

```bash
podman pull quay.io/takinosh/openshift-cluster-health-mcp:v1.0.0
```

### Specific commit

```bash
podman pull quay.io/takinosh/openshift-cluster-health-mcp:main-abc1234-20260101-120000
```

## Running the Container

### HTTP Mode (default)

```bash
podman run -p 8080:8080 \
  -e MCP_TRANSPORT=http \
  quay.io/takinosh/openshift-cluster-health-mcp:latest
```

### With OpenShift Cluster Access

```bash
podman run -p 8080:8080 \
  -e MCP_TRANSPORT=http \
  -v ~/.kube/config:/kubeconfig:ro \
  -e KUBECONFIG=/kubeconfig \
  quay.io/takinosh/openshift-cluster-health-mcp:latest
```

## Security Scanning

The workflow automatically scans images with Trivy for:

- Critical vulnerabilities
- High severity vulnerabilities

Scan results are displayed in the GitHub Actions logs.

## Troubleshooting

### Build fails with "unauthorized" error

- Check that `QUAY_USERNAME` and `QUAY_PASSWORD` secrets are set correctly
- Verify the robot account has write permissions to the repository

### Image is too large

- Target size: < 100MB
- The workflow will warn if the image exceeds this
- Check the Dockerfile for unnecessary dependencies

### Container fails to start

- Check the "Verify Container Deployment" job logs in GitHub Actions
- Test locally: `podman run quay.io/takinosh/openshift-cluster-health-mcp:latest`

## Making the Repository Public on Quay.io

By default, Quay.io repositories are private. To make it public:

1. Go to <https://quay.io/>
2. Navigate to your repository
3. Click **Settings**
4. Under **Repository Visibility**, click **Make Public**
5. Confirm the action

This allows anyone to pull the image without authentication.
