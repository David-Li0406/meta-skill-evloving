# GitHub Actions Onboarding for OpenShift Cluster Health MCP

Welcome! This guide will walk you through setting up GitHub Actions to run integration tests against your OpenShift cluster.

## 🎯 Goal

Enable GitHub Actions to automatically test your code against a live OpenShift cluster on every push/PR.

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ Access to your GitHub repository settings
- ✅ `oc` CLI installed and working
- ✅ Currently logged into your OpenShift cluster
- ✅ Cluster admin permissions (to create service accounts)

**Verify you're ready:**
```bash
# Check you're logged in
oc whoami

# Check cluster access
oc get nodes

# Check you have admin rights
oc auth can-i create clusterrole
```

If all commands work, you're ready! 🚀

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Create Service Account (2 min)

We'll create a dedicated service account with read-only permissions for GitHub Actions.

**Run this command from your project directory:**

```bash
./scripts/setup-github-actions-sa.sh
```

**What this does:**
- Creates `github-actions-sa` service account
- Grants **read-only** cluster access
- Generates a **1-year** authentication token
- Shows you the credentials to add to GitHub

**Example output:**
```
OPENSHIFT_SERVER:
https://api.cluster-t2wns.t2wns.sandbox1039.opentlc.com:6443

OPENSHIFT_TOKEN:
eyJhbGciOiJSUzI1NiIsImtpZCI6IlBMTkhNMG1QUjFqd...
```

📝 **Copy both values** - you'll need them in the next step!

---

### Step 2: Add Secrets to GitHub (2 min)

Now we'll store those credentials securely in GitHub.

**Go to your repository secrets page:**
```
https://github.com/tosin2013/openshift-cluster-health-mcp/settings/secrets/actions
```

Or navigate manually:
1. Go to your repo: https://github.com/tosin2013/openshift-cluster-health-mcp
2. Click **Settings** (top navigation)
3. Click **Secrets and variables** → **Actions** (left sidebar)

**Add the first secret:**
1. Click **"New repository secret"**
2. Name: `OPENSHIFT_SERVER`
3. Value: (paste the server URL from Step 1)
   ```
   https://api.cluster-t2wns.t2wns.sandbox1039.opentlc.com:6443
   ```
4. Click **"Add secret"**

**Add the second secret:**
1. Click **"New repository secret"** again
2. Name: `OPENSHIFT_TOKEN`
3. Value: (paste the long token from Step 1)
4. Click **"Add secret"**

**Verify secrets are added:**
You should now see both secrets listed:
- ✅ `OPENSHIFT_SERVER`
- ✅ `OPENSHIFT_TOKEN`

---

### Step 3: Test the Setup (1 min)

**Push your code to trigger CI:**

```bash
# If you have uncommitted changes
git add .
git commit -m "test: verify GitHub Actions with OpenShift"

# Push to trigger workflow
git push origin main
```

**Watch it run:**
1. Go to: https://github.com/tosin2013/openshift-cluster-health-mcp/actions
2. Click on the latest workflow run
3. Watch the steps execute

**You should see:**
- ✅ Set up OpenShift kubeconfig (Optional) - **SUCCESS**
- ✅ Verify OpenShift connectivity (Optional) - **SUCCESS**
  - Should show: "✓ Connected to OpenShift cluster"
  - Should show: "✓ Cluster is accessible"
- ✅ Run tests - **SUCCESS**
  - Should show: "Running tests WITH OpenShift cluster access..."
  - Integration tests should pass

---

## 🔍 Troubleshooting

### Issue: "Service account already exists"

**Fix:**
```bash
# Delete and recreate
oc delete sa github-actions-sa -n default
./scripts/setup-github-actions-sa.sh
```

### Issue: "kubectl: command not found" in GitHub Actions

**This is normal!** The workflow automatically installs kubectl. If you see this error:
- Check that the "Verify OpenShift connectivity" step completed successfully
- The workflow should have installed kubectl before this error

### Issue: "Unauthorized" in GitHub Actions

**Causes:**
1. Secrets not added to GitHub
2. Token expired (shouldn't happen for 1 year)
3. Service account was deleted

**Fix:**
```bash
# Regenerate token
oc create token github-actions-sa -n default --duration=8760h

# Update the OPENSHIFT_TOKEN secret in GitHub with new token
```

### Issue: "Could not list nodes" in GitHub Actions

**This means the connection works but permissions might be wrong.**

**Verify service account permissions:**
```bash
# Should return "yes"
oc auth can-i get nodes --as=system:serviceaccount:default:github-actions-sa
oc auth can-i list pods --as=system:serviceaccount:default:github-actions-sa

# Should return "no" (read-only account)
oc auth can-i delete pods --as=system:serviceaccount:default:github-actions-sa
```

**Fix permissions:**
```bash
# Delete and recreate with correct permissions
oc delete clusterrolebinding github-actions-readonly-binding
./scripts/setup-github-actions-sa.sh
```

### Issue: Tests pass locally but fail in CI

**Common causes:**

1. **Network latency** - GitHub Actions runners are slower
   ```bash
   # Tests might timeout - check test timeouts
   grep -r "time.Second" internal/
   ```

2. **Different namespaces** - CI might not access the same namespace
   ```bash
   # Check what namespace the service account can access
   oc auth can-i list pods --as=system:serviceaccount:default:github-actions-sa -n default
   ```

3. **Missing resources** - Resources exist locally but not in cluster
   ```bash
   # Verify resources exist
   oc get all -n default
   ```

---

## 🔒 Security FAQ

### Is it safe to store my cluster token in GitHub?

**Yes, with these caveats:**

✅ **Safe because:**
- GitHub Secrets are encrypted at rest
- Only GitHub Actions can access them (not visible in UI after adding)
- Service account has **read-only** access (can't modify anything)
- Token is specific to this repository

⚠️ **But remember:**
- Don't print secrets in logs
- Rotate token annually
- Monitor service account usage

### What can this service account do?

**It can:**
- ✅ List and get cluster resources (nodes, pods, deployments)
- ✅ Read KServe InferenceServices
- ✅ Monitor cluster health
- ✅ Run integration tests

**It CANNOT:**
- ❌ Create, update, or delete resources
- ❌ Execute commands in pods
- ❌ Access secrets or configmaps
- ❌ Change RBAC permissions

**Verify yourself:**
```bash
# Test read permissions (should work)
oc auth can-i get pods --as=system:serviceaccount:default:github-actions-sa

# Test write permissions (should fail)
oc auth can-i delete pods --as=system:serviceaccount:default:github-actions-sa
oc auth can-i create deployments --as=system:serviceaccount:default:github-actions-sa
```

### How long does the token last?

- **Duration:** 1 year
- **Created:** Check with `oc get sa github-actions-sa -n default -o yaml`
- **Rotation:** Set a calendar reminder for 11 months from now

### Can I use my personal token instead?

**You can, but it's not recommended:**

❌ Personal tokens expire in 24 hours
❌ Tied to your user account (breaks if you leave)
❌ Has your full permissions (overly permissive)
✅ Service account: 1-year token, minimal permissions, team-friendly

---

## 📊 What Gets Tested?

When you push code, GitHub Actions will:

1. **Build** - Compile all packages
2. **Unit Tests** - Test individual components
3. **Integration Tests** - Test against live cluster:
   - Cluster health checks
   - Pod listing and filtering
   - Node information retrieval
   - KServe InferenceService queries (if KServe enabled)
4. **Race Detection** - Check for concurrency issues
5. **Code Coverage** - Generate coverage reports
6. **Linting** - Code quality checks
7. **Security Scanning** - Vulnerability detection
8. **Helm Validation** - Chart linting

---

## 🎯 Success Criteria

After setup, your GitHub Actions should:

✅ **Connect to OpenShift cluster** - "✓ Connected to OpenShift cluster"
✅ **List cluster nodes** - "✓ Cluster is accessible"
✅ **Run tests with cluster access** - "Running tests WITH OpenShift cluster access..."
✅ **All tests pass** - Green checkmarks on all test jobs
✅ **Coverage report uploaded** - Codecov integration working

---

## 🔄 Maintenance

### Monthly
- Check GitHub Actions runs are passing
- Review service account audit logs

### Annually (11 months from setup)
- Rotate service account token:
  ```bash
  oc create token github-actions-sa -n default --duration=8760h
  ```
- Update `OPENSHIFT_TOKEN` secret in GitHub

### When team members leave
- No action needed! Service account is not tied to individuals

---

## 📚 Additional Resources

- **Full setup guide:** [docs/github-actions-setup.md](github-actions-setup.md)
- **Quick start:** [GITHUB_ACTIONS_QUICKSTART.md](../GITHUB_ACTIONS_QUICKSTART.md)
- **Security model:** [docs/adrs/007-rbac-based-security-model.md](adrs/007-rbac-based-security-model.md)
- **Script documentation:** [scripts/README.md](../scripts/README.md)

---

## ✅ Checklist

Use this to track your progress:

- [ ] Verified I'm logged into OpenShift (`oc whoami`)
- [ ] Ran `./scripts/setup-github-actions-sa.sh`
- [ ] Copied `OPENSHIFT_SERVER` value
- [ ] Copied `OPENSHIFT_TOKEN` value
- [ ] Added `OPENSHIFT_SERVER` secret to GitHub
- [ ] Added `OPENSHIFT_TOKEN` secret to GitHub
- [ ] Pushed code to trigger workflow
- [ ] Verified "Set up OpenShift kubeconfig" step succeeded
- [ ] Verified "Verify OpenShift connectivity" step succeeded
- [ ] Verified tests ran with cluster access
- [ ] All CI checks passed ✅
- [ ] Set calendar reminder to rotate token in 11 months

---

**Need help?** Open an issue or check the troubleshooting section above.

**Ready to start?** → [Step 1: Create Service Account](#step-1-create-service-account-2-min)
