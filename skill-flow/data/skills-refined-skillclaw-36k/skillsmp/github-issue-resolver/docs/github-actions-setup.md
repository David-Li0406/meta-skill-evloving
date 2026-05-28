# GitHub Actions Setup for OpenShift Integration

This document explains how to configure GitHub Actions to run integration tests against your OpenShift cluster.

## Prerequisites

- Access to your GitHub repository settings
- OpenShift cluster access token
- OpenShift cluster API server URL

## Step 1: Gather OpenShift Credentials

You need two pieces of information from your OpenShift cluster:

### 1. Cluster API Server URL

```bash
# Get the API server URL from your current kubeconfig
kubectl cluster-info | grep "Kubernetes control plane"

# Or from oc CLI
oc whoami --show-server
```

Example: `https://api.cluster-t2wns.t2wns.sandbox1039.opentlc.com:6443`

### 2. Authentication Token

```bash
# Get your current authentication token
oc whoami -t

# Or login to get a new token
oc login --token=<your-token> --server=<your-server>
```

Example: `sha256~YOUR_TOKEN_WILL_BE_MUCH_LONGER_THAN_THIS_EXAMPLE`

## Step 2: Add Secrets to GitHub Repository

1. Navigate to your GitHub repository: https://github.com/tosin2013/openshift-cluster-health-mcp

2. Click **Settings** (top menu)

3. In the left sidebar, click **Secrets and variables** → **Actions**

4. Click **New repository secret**

5. Add the first secret:
   - **Name:** `OPENSHIFT_SERVER`
   - **Value:** Your cluster API server URL (e.g., `https://api.cluster-t2wns.t2wns.sandbox1039.opentlc.com:6443`)
   - Click **Add secret**

6. Add the second secret:
   - **Name:** `OPENSHIFT_TOKEN`
   - **Value:** Your authentication token (paste the actual token from step 1)
   - Click **Add secret**

## Step 3: Verify the Secrets

After adding the secrets:

1. Go to **Actions** tab in your repository
2. Click on the latest workflow run
3. Check the "Set up OpenShift kubeconfig" step - it should show as completed
4. Check the "Verify OpenShift connectivity" step - it should successfully connect to the cluster

## Security Considerations

### ⚠️ Token Expiration

OpenShift tokens typically expire after a certain period (usually 24 hours for login tokens). You have several options:

**Option A: Service Account Token (Recommended)**

Create a long-lived service account token:

```bash
# Create a service account
oc create sa github-actions-sa

# Grant necessary permissions (read-only cluster viewer)
oc adm policy add-cluster-role-to-user cluster-reader -z github-actions-sa

# Get the service account token
oc create token github-actions-sa --duration=8760h  # 1 year

# Use this token as OPENSHIFT_TOKEN secret
```

**Option B: Manual Token Refresh**

- Update the `OPENSHIFT_TOKEN` secret when it expires
- Set up calendar reminders to refresh the token

**Option C: Use GitHub Self-Hosted Runner**

- Run the GitHub Actions runner on a machine with persistent cluster access
- No need to manage tokens in secrets

### 🔒 Principle of Least Privilege

The service account should have minimal permissions:

```yaml
# Recommended RBAC for GitHub Actions
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: github-actions-readonly
rules:
  # Cluster health monitoring
  - apiGroups: [""]
    resources: ["nodes", "pods", "namespaces", "events"]
    verbs: ["get", "list", "watch"]

  # KServe InferenceServices (if testing KServe features)
  - apiGroups: ["serving.kserve.io"]
    resources: ["inferenceservices"]
    verbs: ["get", "list"]
```

### 🛡️ Network Security

The token provides access to your OpenShift cluster from the internet. Consider:

- **IP Whitelisting:** Configure OpenShift to only accept connections from GitHub Actions IP ranges
- **Read-Only Access:** Ensure the service account has no write/delete permissions
- **Audit Logging:** Monitor access logs for the service account

### 🔑 Secret Rotation

Best practices for secret rotation:

1. **Rotate tokens every 90 days** (or per your security policy)
2. **Use GitHub Environments** for additional protection:
   - Go to Settings → Environments → New environment
   - Set up required reviewers for production deployments
3. **Monitor secret usage** in Actions logs

## Troubleshooting

### Connection Failed

If the "Verify OpenShift connectivity" step fails:

```bash
# Check if the cluster is accessible from external networks
curl -k https://api.cluster-t2wns.t2wns.sandbox1039.opentlc.com:6443/version

# Verify token is valid
oc whoami --token=<your-token> --server=<your-server>
```

### Token Expired

Error: `error: You must be logged in to the server (Unauthorized)`

**Solution:** Regenerate and update the token:

```bash
# Get a new token
oc login --token=<new-token> --server=<your-server>
oc whoami -t

# Update the OPENSHIFT_TOKEN secret in GitHub
```

### Tests Fail in CI but Pass Locally

Common causes:

1. **Network latency:** GitHub Actions runners may have higher latency to your cluster
2. **Permissions:** Service account may have fewer permissions than your user account
3. **Namespace access:** Check if the service account can access required namespaces

```bash
# Test service account permissions
oc auth can-i get pods --as=system:serviceaccount:default:github-actions-sa
oc auth can-i list nodes --as=system:serviceaccount:default:github-actions-sa
```

## Alternative: Use OpenShift GitHub Actions

For a more maintainable solution, consider using official OpenShift GitHub Actions:

```yaml
- name: Log in to OpenShift
  uses: redhat-actions/oc-login@v1
  with:
    openshift_server_url: ${{ secrets.OPENSHIFT_SERVER }}
    openshift_token: ${{ secrets.OPENSHIFT_TOKEN }}
    insecure_skip_tls_verify: true

- name: Run tests
  run: go test -v ./...
```

## Monitoring

Set up alerts for:

- **Token expiration warnings** (7 days before expiry)
- **Failed authentication attempts** in OpenShift audit logs
- **Unusual API usage patterns** from the service account

## References

- [GitHub Actions: Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [OpenShift: Service Accounts](https://docs.openshift.com/container-platform/latest/authentication/using-service-accounts-in-applications.html)
- [Red Hat OpenShift GitHub Actions](https://github.com/redhat-actions)
