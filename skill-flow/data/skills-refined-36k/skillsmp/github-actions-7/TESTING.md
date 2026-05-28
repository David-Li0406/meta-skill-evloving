# GitHub Actions Skill - Testing Guide

**Purpose:** Comprehensive testing scenarios to validate all functionality of the GitHub Actions skill
**Version:** 1.0.0
**Last Updated:** December 23, 2025

---

## Table of Contents

1. [Pre-Test Setup](#pre-test-setup)
2. [Quick Validation Tests](#quick-validation-tests)
3. [Template-Specific Tests](#template-specific-tests)
4. [Integration Tests](#integration-tests)
5. [Performance Tests](#performance-tests)
6. [Security Tests](#security-tests)
7. [Troubleshooting Failed Tests](#troubleshooting-failed-tests)

---

## Pre-Test Setup

### Prerequisites

1. **GitHub Repository:** Create a test repository (private is fine)
2. **GitHub Actions Enabled:** Settings → Actions → Enable
3. **Required Tools (local testing):**
   ```bash
   # Install act for local workflow testing
   brew install act  # macOS
   # OR
   curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

   # Install yamllint for YAML validation
   pip install yamllint

   # Install jq for JSON parsing (scripts may use it)
   brew install jq  # macOS
   ```

### Test Repository Structure

Create a test repository structure:

```bash
mkdir test-github-actions-skill
cd test-github-actions-skill
git init

# Create test files based on template category
# Node.js test
echo '{"name":"test","version":"1.0.0","scripts":{"test":"echo \"test passed\""}}' > package.json

# Python test
echo 'requests==2.31.0' > requirements.txt

# Go test
cat > go.mod << EOF
module test
go 1.21
EOF

# Docker test
cat > Dockerfile << EOF
FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install
EOF

git add .
git commit -m "Initial commit"
```

---

## Quick Validation Tests

### Test 1: Skill File Validation

**Purpose:** Verify all skill files exist and are valid

**Steps:**
```bash
cd /path/to/3promptidea/.claude/skills/github-actions

# Check file count
find . -type f | wc -l
# Expected: 36 files

# Validate YAML files
for file in $(find . -name "*.yml" -o -name "*.yaml"); do
    echo "Validating $file..."
    yamllint $file || echo "FAILED: $file"
done

# Check script permissions
ls -l scripts/*.sh
# Expected: All should be executable (-rwxr-xr-x)
```

**Expected Result:** All files validate without errors

**Time:** 2 minutes

---

### Test 2: Plugin Metadata Validation

**Purpose:** Verify plugin.json is valid and matches actual files

**Steps:**
```bash
# Validate JSON syntax
cat plugin.json | jq . > /dev/null
echo "JSON is valid"

# Count templates listed vs actual
TEMPLATE_COUNT=$(cat plugin.json | jq '.templates | to_entries | map(.value | length) | add')
echo "Templates in plugin.json: $TEMPLATE_COUNT"
echo "Expected: 22"

# Count actual template files
ACTUAL_COUNT=$(find assets/workflows -name "*.yml" | wc -l)
echo "Actual template files: $ACTUAL_COUNT"

# Verify documentation files
echo "Documentation files:"
cat plugin.json | jq '.documentation[]'
```

**Expected Result:**
- JSON is valid
- 22 templates listed
- 22 actual files
- 5 documentation files listed

**Time:** 1 minute

---

### Test 3: Script Execution Tests

**Purpose:** Test all utility scripts

#### Test 3.1: detect-project.sh

```bash
# Test on a Node.js project
cd /path/to/your/nodejs/project
bash .claude/skills/github-actions/scripts/detect-project.sh

# Expected output:
# ✅ Node.js/TypeScript detected
# 🔹 basic/nodejs-ci.yml recommended
```

#### Test 3.2: validate-yaml.sh

```bash
# Test validation on valid file
bash .claude/skills/github-actions/scripts/validate-yaml.sh \
    assets/workflows/basic/nodejs-ci.yml

# Expected: ✅ Valid YAML

# Test validation on invalid file (create one)
echo "invalid: yml: content:" > /tmp/test.yml
bash .claude/skills/github-actions/scripts/validate-yaml.sh /tmp/test.yml

# Expected: ❌ Invalid YAML
```

#### Test 3.3: generate-workflow.sh

```bash
# Test workflow generation
cd /tmp/test-github-actions-skill
bash .claude/skills/github-actions/scripts/generate-workflow.sh \
    --type=nodejs \
    --output=.github/workflows/ci.yml

# Expected:
# - Creates .github/workflows directory
# - Generates workflow file
# - File validates with validate-yaml.sh
```

**Expected Result:** All scripts execute without errors

**Time:** 5 minutes

---

## Template-Specific Tests

### Test 4: Basic CI Templates

#### Test 4.1: Node.js CI Workflow

**Setup:**
```bash
mkdir -p test-nodejs-ci
cd test-nodejs-ci
git init

# Create package.json
cat > package.json << EOF
{
  "name": "test-nodejs-ci",
  "version": "1.0.0",
  "scripts": {
    "test": "echo \"Running tests...\" && exit 0",
    "lint": "echo \"Linting...\" && exit 0"
  }
}
EOF

# Copy workflow
cp .claude/skills/github-actions/assets/workflows/basic/nodejs-ci.yml \
   .github/workflows/ci.yml

git add .
git commit -m "Test: Add Node.js CI"
git push origin main
```

**Verify:**
1. Go to GitHub Actions tab
2. Check workflow triggered
3. Verify all jobs complete:
   - Lint (success)
   - Test (success)
   - Build (success)

**Expected Result:** All jobs pass

**Time:** 10 minutes

---

#### Test 4.2: Python CI Workflow

**Setup:**
```bash
mkdir -p test-python-ci
cd test-python-ci
git init

# Create requirements.txt
cat > requirements.txt << EOF
pytest==7.4.0
pylint==3.0.0
EOF

# Create test file
cat > test_app.py << EOF
def test_example():
    assert True
EOF

# Copy workflow
cp .claude/skills/github-actions/assets/workflows/basic/python-ci.yml \
   .github/workflows/ci.yml

git add .
git commit -m "Test: Add Python CI"
git push origin main
```

**Verify:**
- Python 3.9, 3.10, 3.11, 3.12 all tested
- Linting passes
- Tests pass

**Expected Result:** Matrix builds for all Python versions pass

**Time:** 15 minutes

---

### Test 5: Docker Templates

#### Test 5.1: Docker Build & Push

**Setup:**
```bash
mkdir -p test-docker-build
cd test-docker-build
git init

# Create Dockerfile
cat > Dockerfile << EOF
FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
CMD ["node", "index.js"]
EOF

# Create package.json
echo '{"name":"test","version":"1.0.0"}' > package.json

# Copy workflow
cp .claude/skills/github-actions/assets/workflows/docker/docker-build-push.yml \
   .github/workflows/build.yml

# Add secrets (GitHub repo settings):
# - CR_PAT (Container registry token)
# - OR use GITHUB_TOKEN for GHCR

git add .
git commit -m "Test: Add Docker build"
git push origin main
```

**Verify:**
1. Docker image builds successfully
2. Image tagged with Git SHA
3. Image pushed to registry
4. Check registry for image

**Expected Result:** Image in registry with tags

**Time:** 15 minutes

---

#### Test 5.2: Docker Multi-Arch Build

**Setup:**
```bash
# Use same repository as Test 5.1
cp .claude/skills/github-actions/assets/workflows/docker/docker-multi-arch.yml \
   .github/workflows/multi-arch.yml

git add .
git commit -m "Test: Add multi-arch build"
git push origin main
```

**Verify:**
1. Builds for amd64, arm64, arm/v7
2. All architectures pushed
3. Manifest created

**Expected Result:** Multi-arch image available

**Time:** 20 minutes (longer build time)

---

### Test 6: Kubernetes Templates

#### Test 6.1: Kubernetes Deployment

**Prerequisites:**
- Kubernetes cluster (EKS, GKE, AKS, or minikube)
- KUBECONFIG secret configured in GitHub

**Setup:**
```bash
mkdir -p test-k8s-deploy
cd test-k8s-deploy
git init

# Create Kubernetes manifests
mkdir -p k8s
cat > k8s/deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: test-app
  template:
    metadata:
      labels:
        app: test-app
    spec:
      containers:
      - name: app
        image: ghcr.io/your-org/test-app:latest
        ports:
        - containerPort: 3000
EOF

# Copy workflow
cp .claude/skills/github-actions/assets/workflows/kubernetes/k8s-deploy.yml \
   .github/workflows/deploy.yml

# Add secrets:
# - KUBECONFIG (base64 encoded kubeconfig file)

git add .
git commit -m "Test: Add K8s deployment"
git push origin main
```

**Verify:**
1. kubectl configures successfully
2. Deployment applies
3. Pods are running
4. Service is accessible

**Expected Result:** Application deployed to cluster

**Time:** 10 minutes

---

#### Test 6.2: Kubernetes Approval Workflow

**Setup:**
```bash
# Use same repository as Test 6.1
cp .claude/skills/github-actions/assets/workflows/kubernetes/k8s-approval-workflow.yml \
   .github/workflows/deploy-prod.yml

# Configure environment in GitHub:
# Settings → Environments → New Environment (production)
# Add required reviewers

git add .
git commit -m "Test: Add approval workflow"
git push origin main
```

**Verify:**
1. Deployment to staging completes
2. Production deployment pauses
3. Approval required in GitHub UI
4. After approval, production deploys

**Expected Result:** Manual approval gate works

**Time:** 15 minutes (plus approval time)

---

### Test 7: Monorepo Templates

#### Test 7.1: Turborepo Workflow

**Setup:**
```bash
mkdir -p test-turborepo
cd test-turborepo
git init

# Initialize Turborepo
npx create-turbo@latest

# Copy workflow
cp .claude/skills/github-actions/assets/workflows/monorepo/monorepo-turbo.yml \
   .github/workflows/ci.yml

# Configure Turbo remote caching (optional)

git add .
git commit -m "Test: Add Turborepo CI"
git push origin main
```

**Verify:**
1. Turborepo detects affected packages
2. Only affected packages build
3. Remote cache stores artifacts
4. Build time reduced vs. full build

**Expected Result:** Incremental builds working

**Time:** 20 minutes

---

#### Test 7.2: Nx Workflow

**Setup:**
```bash
mkdir -p test-nx-workspace
cd test-nx-workspace
git init

# Initialize Nx workspace
npx create-nx-workspace@latest

# Copy workflow
cp .claude/skills/github-actions/assets/workflows/monorepo/monorepo-nx.yml \
   .github/workflows/ci.yml

git add .
git commit -m "Test: Add Nx CI"
git push origin main
```

**Verify:**
1. Nx affected graph generated
2. Only affected tasks run
3. Distributed caching (if configured)
4. Parallel execution

**Expected Result:** Affected-only builds working

**Time:** 20 minutes

---

### Test 8: Security Templates

#### Test 8.1: CodeQL Analysis

**Setup:**
```bash
# Use any existing repository
cp .claude/skills/github-actions/assets/workflows/security/codeql-analysis.yml \
   .github/workflows/codeql.yml

# Enable CodeQL in repo settings:
# Settings → Security → Code scanning

git add .
git commit -m "Test: Add CodeQL"
git push origin main
```

**Verify:**
1. CodeQL workflow runs
2. Analysis completes
3. Results appear in Security tab
4. Alerts created for issues found

**Expected Result:** Code scanning completes

**Time:** 30 minutes (CodeQL is slow)

---

#### Test 8.2: Dependency Review

**Setup:**
```bash
cp .claude/skills/github-actions/assets/workflows/security/dependency-review.yml \
   .github/workflows/dependency-review.yml

git add .
git commit -m "Test: Add dependency review"
git push origin main
```

**Verify:**
1. Dependency review runs
2. Vulnerabilities reported
3. PR comments added (if vulnerabilities found)

**Expected Result:** Dependencies scanned

**Time:** 5 minutes

---

#### Test 8.3: Trivy Scan

**Setup:**
```bash
# For container scanning
cp .claude/skills/github-actions/assets/workflows/security/trivy-scan.yml \
   .github/workflows/trivy.yml

git add .
git commit -m "Test: Add Trivy scan"
git push origin main
```

**Verify:**
1. Trivy runs
2. Vulnerabilities found (or none)
3. SARIF report uploaded
4. Results in Security tab

**Expected Result:** Container scanned

**Time:** 10 minutes

---

### Test 9: Scheduled Workflows

#### Test 9.1: Daily Security Scan

**Setup:**
```bash
cp .claude/skills/github-actions/assets/workflows/scheduled/daily-security-scan.yml \
   .github/workflows/daily-scan.yml

git add .
git commit -m "Test: Add daily security scan"
git push origin main
```

**Verify:**
1. Manually trigger workflow (workflow_dispatch)
2. Verify scan runs
3. Check next scheduled run
4. Verify it will run daily at 00:00 UTC

**Expected Result:** Scheduled workflow configured

**Time:** 5 minutes

---

### Test 10: Advanced Templates

#### Test 10.1: Matrix Build

**Setup:**
```bash
cp .claude/skills/github-actions/assets/workflows/advanced/matrix-build.yml \
   .github/workflows/matrix.yml

git add .
git commit -m "Test: Add matrix build"
git push origin main
```

**Verify:**
1. Matrix jobs run in parallel
2. All OS/version combinations tested
3. Results aggregated

**Expected Result:** 4-6 jobs run in parallel

**Time:** 15 minutes

---

#### Test 10.2: Release Workflow

**Setup:**
```bash
cp .claude/skills/github-actions/assets/workflows/advanced/release-workflow.yml \
   .github/workflows/release.yml

git add .
git commit -m "Test: Add release workflow"
git push origin main

# Create a release tag
git tag v1.0.0
git push origin v1.0.0
```

**Verify:**
1. Release workflow triggers on tag
2. Changelog generated
3. GitHub release created
4. Assets uploaded

**Expected Result:** Release created

**Time:** 10 minutes

---

## Integration Tests

### Test 11: Complete CI/CD Pipeline

**Purpose:** Test end-to-end pipeline with multiple templates

**Setup:**
```bash
mkdir -p test-complete-cicd
cd test-complete-cicd
git init

# Create Node.js app
cat > package.json << EOF
{
  "name": "complete-cicd-test",
  "version": "1.0.0",
  "scripts": {
    "test": "jest",
    "lint": "eslint ."
  }
}
EOF

# Create Dockerfile
cat > Dockerfile << EOF
FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
CMD ["npm", "start"]
EOF

# Create K8s manifests
mkdir -p k8s
cat > k8s/deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: complete-cicd-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: complete-cicd-app
  template:
    metadata:
      labels:
        app: complete-cicd-app
    spec:
      containers:
      - name: app
        image: ghcr.io/your-org/complete-cicd-app:latest
EOF

# Copy workflows
cp .claude/skills/github-actions/assets/workflows/basic/nodejs-ci.yml \
   .github/workflows/01-ci.yml
cp .claude/skills/github-actions/assets/workflows/docker/docker-build-push.yml \
   .github/workflows/02-build.yml
cp .claude/skills/github-actions/assets/workflows/kubernetes/k8s-deploy.yml \
   .github/workflows/03-deploy.yml
cp .claude/skills/github-actions/assets/workflows/security/codeql-analysis.yml \
   .github/workflows/04-security.yml

# Configure secrets and environment
git add .
git commit -m "Test: Complete CI/CD pipeline"
git push origin main
```

**Verify:**
1. CI runs: lint, test, build
2. Security scanning: CodeQL passes
3. Docker: Image builds and pushes
4. K8s: Deploys to cluster
5. Health checks pass

**Expected Result:** Complete pipeline succeeds

**Time:** 30 minutes

---

### Test 12: Monorepo with Selective Deployment

**Purpose:** Test monorepo with path filtering

**Setup:**
```bash
mkdir -p test-monorepo-full
cd test-monorepo-full
git init

# Create monorepo structure
mkdir -p packages/backend
mkdir -p packages/frontend
mkdir -p packages/shared

# Create package.json files
cat > package.json << EOF
{
  "name": "monorepo-root",
  "private": true
}
EOF

cat > packages/backend/package.json << EOF
{
  "name": "backend",
  "version": "1.0.0"
}
EOF

cat > packages/frontend/package.json << EOF
{
  "name": "frontend",
  "version": "1.0.0"
}
EOF

# Copy monorepo workflow
cp .claude/skills/github-actions/assets/workflows/monorepo/monorepo-path-filter.yml \
   .github/workflows/ci.yml

git add .
git commit -m "Test: Monorepo setup"
git push origin main

# Test 1: Modify only backend
echo "// change" >> packages/backend/index.js
git add .
git commit -m "Change backend"
git push origin main

# Verify: Only backend builds

# Test 2: Modify only frontend
echo "// change" >> packages/frontend/index.js
git add .
git commit -m "Change frontend"
git push origin main

# Verify: Only frontend builds
```

**Expected Result:** Only affected paths build

**Time:** 25 minutes

---

## Performance Tests

### Test 13: Caching Effectiveness

**Purpose:** Measure caching improvement

**Setup:**
```bash
# Use repository with dependencies
cd test-nodejs-ci

# Run 1: Cold build (no cache)
git push origin main
# Note build time from Actions tab

# Run 2: Warm build (with cache)
echo "// minor change" >> index.js
git add .
git commit -m "Test cache"
git push origin main
# Note build time

# Calculate improvement
# Cold build time - Warm build time = Time saved
# (Time saved / Cold build time) * 100 = % improvement
```

**Expected Result:**
- Cold build: 3-5 minutes
- Warm build: 30-60 seconds
- Improvement: 70-90%

**Time:** 15 minutes

---

### Test 14: Parallel Job Performance

**Purpose:** Verify parallel execution

**Setup:**
```bash
# Use matrix-build workflow
cd test-matrix-build

# Check Actions tab
# Verify jobs run in parallel
# Note: Look at job start/end timestamps
```

**Expected Result:**
- 4+ jobs run simultaneously
- Total time ≈ longest job, not sum of all jobs

**Time:** 10 minutes

---

## Security Tests

### Test 15: Secret Scanning

**Purpose:** Verify secret detection

**Setup:**
```bash
# Create file with fake secret
echo "AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE" > config.env

git add .
git commit -m "Test: Commit secret (should fail)"
git push origin main
```

**Verify:**
1. Trivy detects secret
2. Workflow fails (if exit-code: '1' configured)
3. Alert created in Security tab

**Expected Result:** Secret detected and blocked

**Time:** 10 minutes

**Cleanup:** Remove secret and commit

---

### Test 16: Vulnerability Scanning

**Purpose:** Detect vulnerable dependencies

**Setup:**
```bash
# Add vulnerable dependency (intentionally)
echo "requests==2.6.0" >> requirements.txt  # Old version with vulnerabilities

git add .
git commit -m "Test: Add vulnerable dependency"
git push origin main
```

**Verify:**
1. Dependency review detects vulnerability
2. PR comment added (if on PR)
3. Security alert created

**Expected Result:** Vulnerability detected

**Time:** 5 minutes

---

## Troubleshooting Failed Tests

### Issue: Workflow Not Triggering

**Diagnosis:**
```bash
# Check branch name
git branch
# Must match workflow 'on.push.branches'

# Check path filters
# If workflow has 'paths-ignore', your file might be excluded

# Check workflow syntax
bash .claude/skills/github-actions/scripts/validate-yaml.sh .github/workflows/your-workflow.yml
```

**Solution:**
- Ensure branch names match exactly
- Remove or adjust path filters for testing
- Fix YAML syntax errors

---

### Issue: Permission Denied

**Diagnosis:**
```bash
# Check workflow permissions
grep -A 5 "permissions:" .github/workflows/your-workflow.yml

# Check required permissions for operation
# - Pushing to registry: packages: write
# - Deploying to K8s: contents: read
# - Creating releases: contents: write
```

**Solution:**
```yaml
permissions:
  contents: read
  packages: write  # Add this for registry push
```

---

### Issue: Cache Not Restoring

**Diagnosis:**
```bash
# Check cache key in workflow
grep -A 10 "actions/cache@" .github/workflows/your-workflow.yml

# Verify key format
key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

**Solution:**
```yaml
# Add restore-keys for partial matches
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

---

### Issue: Matrix Job Failing

**Diagnosis:**
```bash
# Check if fail-fast is enabled
grep -A 3 "fail-fast:" .github/workflows/your-workflow.yml
```

**Solution:**
```yaml
strategy:
  matrix:
    node: [16, 18, 20]
  fail-fast: false  # Let all jobs complete
```

---

### Issue: Docker Build Timeout

**Diagnosis:**
```bash
# Check timeout setting
grep "timeout:" .github/workflows/your-workflow.yml
```

**Solution:**
```yaml
- uses: docker/build-push-action@v5
  with:
    push: true
  timeout-minutes: 60  # Increase timeout
```

---

### Issue: kubectl Connection Failed

**Diagnosis:**
```bash
# Check kubeconfig secret
# Verify secret is base64 encoded

# Test kubeconfig locally
export KUBECONFIG=/path/to/kubeconfig
kubectl get nodes
```

**Solution:**
```yaml
# Encode kubeconfig properly
cat ~/.kube/config | base64 -w 0

# Add to GitHub secrets as KUBECONFIG
```

---

## Test Results Template

Use this template to document your test results:

```markdown
# GitHub Actions Skill Test Results

**Test Date:** [DATE]
**Tester:** [NAME]
**Repository:** [REPO]

## Quick Validation Tests

- [x] Test 1: Skill File Validation - PASS/FAIL
- [x] Test 2: Plugin Metadata Validation - PASS/FAIL
- [x] Test 3: Script Execution Tests - PASS/FAIL

## Template-Specific Tests

### Basic CI
- [x] Test 4.1: Node.js CI - PASS/FAIL
- [x] Test 4.2: Python CI - PASS/FAIL

### Docker
- [x] Test 5.1: Docker Build & Push - PASS/FAIL
- [x] Test 5.2: Multi-Arch Build - PASS/FAIL

### Kubernetes
- [x] Test 6.1: K8s Deployment - PASS/FAIL
- [x] Test 6.2: Approval Workflow - PASS/FAIL

### Monorepo
- [ ] Test 7.1: Turborepo - PASS/FAIL
- [ ] Test 7.2: Nx - PASS/FAIL

### Security
- [ ] Test 8.1: CodeQL - PASS/FAIL
- [ ] Test 8.2: Dependency Review - PASS/FAIL
- [ ] Test 8.3: Trivy - PASS/FAIL

### Advanced
- [ ] Test 10.1: Matrix Build - PASS/FAIL
- [ ] Test 10.2: Release Workflow - PASS/FAIL

## Integration Tests

- [ ] Test 11: Complete CI/CD Pipeline - PASS/FAIL
- [ ] Test 12: Monorepo Selective - PASS/FAIL

## Performance Tests

- [ ] Test 13: Caching Effectiveness - PASS/FAIL
- [ ] Test 14: Parallel Jobs - PASS/FAIL

## Security Tests

- [ ] Test 15: Secret Scanning - PASS/FAIL
- [ ] Test 16: Vulnerability Scanning - PASS/FAIL

## Summary

**Total Tests:** 16
**Passed:** [COUNT]
**Failed:** [COUNT]
**Pass Rate:** [PERCENTAGE]%

## Issues Found

[List any issues discovered]

## Recommendations

[Suggestions for improvement]
```

---

## Conclusion

This testing guide provides comprehensive coverage of all GitHub Actions skill functionality. Run all tests to ensure the skill is working correctly in your environment.

**Estimated Total Testing Time:** 4-6 hours for full test suite

**Quick Validation (Recommended):** Run Tests 1-3 for basic validation (10 minutes)

**Full Validation:** Run all tests before production deployment

---

**Next Steps:**
1. Run quick validation tests
2. Select templates relevant to your use case
3. Run template-specific tests
4. Document results
5. Deploy to production

**Support:**
- See `references/troubleshooting.md` for detailed debugging
- Check workflow logs in GitHub Actions tab
- Enable debug logging: ACTIONS_STEP_DEBUG=true

---

**Generated by:** Claude Code Skill Documenter
**Version:** 1.0.0
**Last Updated:** December 23, 2025
