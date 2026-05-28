# GitHub Actions Troubleshooting Guide

## Common Issues and Solutions

### Workflow Not Triggering

**Problem:** Workflow doesn't run when expected

**Solutions:**

1. **Check branch names:**
   ```yaml
   on:
     push:
       branches: [main]  # Must match exactly
   ```

2. **Verify path filters:**
   ```yaml
   on:
     push:
       paths:
         - 'src/**'  # Path is relative to repo root
   ```

3. **Check workflow syntax:**
   ```bash
   bash .claude/skills/github-actions/scripts/validate-yaml.sh .github/workflows/broken.yml
   ```

### Permission Denied Errors

**Problem:** `Resource not accessible by integration`

**Solutions:**

1. **Add missing permissions:**
   ```yaml
   permissions:
     contents: write
     packages: write
   ```

2. **Configure organization settings:**
   - Settings → Actions → General
   - Enable "Workflow permissions"

3. **Use personal access token:**
   ```yaml
   - uses: actions/checkout@v4
     with:
       token: ${{ secrets.PAT }}
   ```

### Cache Not Restoring

**Problem:** Cache miss every run

**Solutions:**

1. **Check cache key format:**
   ```yaml
   # Bad
   key: ${{ github.sha }}  # Unique every time

   # Good
   key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
   restore-keys: |
     ${{ runner.os }}-node-
   ```

2. **Verify cache paths:**
   ```yaml
   - uses: actions/cache@v4
     with:
       path: |
         ~/.npm
         node_modules  # Include all necessary paths
   ```

### Docker Build Failures

**Problem:** Docker build fails in Actions but works locally

**Solutions:**

1. **Check context:**
   ```yaml
   - uses: docker/build-push-action@v5
     with:
       context: .  # Or specify subdirectory
   ```

2. **Enable buildkit:**
   ```yaml
   - uses: docker/setup-buildx-action@v3
   ```

3. **Check authentication:**
   ```yaml
   - uses: docker/login-action@v3
     with:
       registry: ghcr.io
       username: ${{ github.actor }}
       password: ${{ secrets.GITHUB_TOKEN }}
   ```

### Matrix Job Failures

**Problem:** One matrix job fails and cancels others

**Solutions:**

```yaml
strategy:
  fail-fast: false  # Don't cancel other jobs
  matrix:
    node: [16, 18, 20]
```

### Timeout Errors

**Problem:** Workflow times out

**Solutions:**

1. **Increase timeout:**
   ```yaml
   jobs:
     build:
     timeout-minutes: 60  # Default is 360
   ```

2. **Optimize workflow:**
   - Enable caching
   - Reduce work
   - Use faster runners

3. **Split long jobs:**
   ```yaml
   jobs:
     part1:
       runs-on: ubuntu-latest
     part2:
       needs: part1
       runs-on: ubuntu-latest
   ```

### Secret Not Available

**Problem:** Secret not accessible in workflow

**Solutions:**

1. **Check secret name:**
   ```yaml
   # Case-sensitive
   password: ${{ secrets.MySecret }}  # Not mysecret
   ```

2. **Verify secret scope:**
   - Organization secrets vs repository secrets
   - Environment secrets

3. **Reveal secret for debugging:**
   ```yaml
   - name: Debug secrets
     run: |
       echo "Secret exists: ${{ secrets.MySecret != '' }}"
   ```

### Kubernetes Deployment Failures

**Problem:** kubectl fails in Actions

**Solutions:**

1. **Configure kubeconfig:**
   ```yaml
   - uses: azure/k8s-set-context@v4
     with:
       method: kubeconfig
       kubeconfig: ${{ secrets.KUBE_CONFIG }}
   ```

2. **Verify connection:**
   ```yaml
   - run: kubectl cluster-info
   - run: kubectl get nodes
   ```

3. **Use service account:**
   ```yaml
   - run: |
       kubectl config set-credentials deploy-user \
         --token=${{ secrets.K8S_TOKEN }}
   ```

### Reusable Workflow Issues

**Problem:** Reusable workflow not working

**Solutions:**

1. **Pass secrets explicitly:**
   ```yaml
   jobs:
     call-workflow:
       uses: org/repo/.github/workflows/reusable.yml@main
       secrets: inherit  # Or list specific secrets
   ```

2. **Check input types:**
   ```yaml
   on:
     workflow_call:
       inputs:
         version:
           type: string
           required: true
   ```

## Debugging Techniques

### Enable Debug Logging

Add secrets to repository:
```
ACTIONS_STEP_DEBUG = true
ACTIONS_RUNNER_DEBUG = true
```

Re-run workflow with debug enabled:
- Actions tab → Workflow run → Re-run jobs → Enable debug logging

### Local Testing with act

```bash
# Install act
brew install act

# Dry run
act -n

# Run specific job
act -j build

# Use custom secrets file
act --secret-file .secrets
```

### Conditional Debugging

```yaml
- name: Debug info
  if: github.event_name == 'workflow_dispatch'
  run: |
    echo "Runner OS: ${{ runner.os }}"
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
```

### Workflow Visualization

```bash
# Install gh CLI
brew install gh

# View workflow runs
gh run list --workflow=ci.yml

# View specific run
gh run view <run-id>
gh run view <run-id> --log
```

## Log Analysis

### Extract Errors

```bash
# Download logs
gh run view <run-id> --log > workflow.log

# Find errors
grep -i error workflow.log
grep -i fail workflow.log
```

### Performance Analysis

```bash
# Extract job durations
gh run view <run-id> --json jobs,name,conclusion,duration
```

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Unable to resolve action` | Action reference incorrect | Check action version and repository |
| `Context deadline exceeded` | Network timeout | Increase timeout or optimize job |
| `Cache not found` | No cache match expected | Add restore-keys |
| `Permission denied` | Insufficient permissions | Add permissions block |
| `Job cancelled` | Concurrency group set | Adjust concurrency settings |
| `Container not found` | Wrong image tag | Verify image tags |
| `Invalid workflow file` | YAML syntax error | Validate YAML syntax |

## Getting Help

### Resources

1. **GitHub Actions Documentation**
   - https://docs.github.com/en/actions

2. **Actions Marketplace**
   - https://github.com/marketplace?type=actions

3. **Community Forum**
   - https://github.community/

4. **GitHub Support**
   - https://support.github.com/

### Report Issues

When reporting issues, include:

1. Workflow YAML file
2. Error messages
3. Run logs (sanitized)
4. Repository information (public/private)
5. Steps to reproduce

### Best Practices for Support

1. **Reproduce issue in public repo** - Create minimal reproduction
2. **Sanitize sensitive data** - Remove secrets and tokens
3. **Provide context** - What you're trying to accomplish
4. **Show research** - What you've already tried

## Examples

See specific workflow examples in `assets/examples/` for working implementations.
