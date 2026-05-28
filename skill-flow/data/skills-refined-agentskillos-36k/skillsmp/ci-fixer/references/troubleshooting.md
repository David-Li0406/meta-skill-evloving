# CI/CD Troubleshooting Guide

<vercel_issues>

## Vercel Build Failures

<memory_issues>

### Out of Memory (OOM)

**Symptoms:**

- Build cancelled with memory error
- Process killed unexpectedly
- "JavaScript heap out of memory"

**Solutions:**

```bash
# Enable memory report
VERCEL_DEBUG_MEMORY_REPORT=1 vercel build

# Increase Node memory (in build command)
NODE_OPTIONS='--max-old-space-size=4096' bun run build

# For Next.js, in next.config.js:
module.exports = {
  experimental: {
    workerThreads: false,
    cpus: 1
  }
}
```

**Prevention:**

- Analyze bundle size: `npx @next/bundle-analyzer`
- Use dynamic imports for large modules
- Upgrade to Pro/Enterprise for more memory
  </memory_issues>

<module_not_found>

### Module Not Found

**Symptoms:**

- "Cannot find module 'xxx'"
- "Module not found: Can't resolve 'xxx'"

**Solutions:**

```bash
# Check if package is in dependencies (not devDependencies for production)
cat package.json | jq '.dependencies'

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# For monorepos, check workspace configuration
npm ls <package-name>
```

**Common causes:**

- Package in devDependencies but needed at build time
- Missing peer dependencies
- Incorrect import path (case sensitivity)
- Missing `@types/*` packages for TypeScript
  </module_not_found>

<build_timeout>

### Build Timeout (45 min limit)

**Symptoms:**

- Build cancelled after 45 minutes
- "Build exceeded maximum duration"

**Solutions:**

```bash
# Use build cache effectively
vercel deploy  # Don't use --force unless necessary

# Skip unnecessary steps
SKIP_ENV_VALIDATION=1 bun run build

# For Next.js ISR, reduce pages built at build time
# In getStaticPaths:
export async function getStaticPaths() {
  return { paths: [], fallback: 'blocking' }
}
```

**Optimization tips:**

- Enable Turborepo/Nx caching
- Use `next build` with `output: 'standalone'`
- Reduce number of pages generated at build time
  </build_timeout>

<env_var_issues>

### Environment Variable Issues

**Symptoms:**

- "undefined" values in app
- Different behavior in preview vs production

**Debug:**

```bash
# List all env vars
vercel env ls

# Pull to local
vercel pull
cat .vercel/.env.*.local

# Check in build logs what's available
echo "Available env vars:"
vercel build --debug 2>&1 | grep -i "environment"
```

**Common issues:**

- Var only set for Production, not Preview
- Missing `NEXT_PUBLIC_` prefix for client-side vars
- Var set after deployment (need redeploy)
  </env_var_issues>

<cache_issues>

### Build Cache Issues

**Symptoms:**

- Old code still appearing
- Dependencies not updating
- Inconsistent builds

**Solutions:**

```bash
# Force fresh build
vercel deploy --force

# Or via env var
VERCEL_FORCE_NO_BUILD_CACHE=1 vercel deploy

# Clear Turborepo cache
TURBO_FORCE=1 bun run build

# Via dashboard: Deployments > Redeploy > Uncheck "Use existing Build Cache"
```

</cache_issues>
</vercel_issues>

<github_actions_issues>

## GitHub Actions Failures

<artifact_issues>

### Artifact Issues

**Symptoms:**

- "no valid artifacts found to download"
- Artifact expired
- Wrong artifact downloaded

**Solutions:**

```bash
# List artifacts for a run
gh api repos/{owner}/{repo}/actions/runs/{run_id}/artifacts

# Check artifact name exactly
gh run view <run-id> --json artifacts -q '.artifacts[].name'

# Download from specific run (not latest)
gh run download <run-id> -n "exact-artifact-name"
```

**Common causes:**

- Artifact name mismatch (case sensitive)
- Artifact expired (default 90 days)
- Downloading from wrong workflow run
- Matrix jobs uploading to same artifact name
  </artifact_issues>

<permission_issues>

### Permission Denied

**Symptoms:**

- "Resource not accessible by integration"
- "Permission denied"
- 403 errors

**Solutions:**

```yaml
# Add permissions to workflow
jobs:
  build:
    permissions:
      contents: read
      packages: write
      actions: read

# For GITHUB_TOKEN in workflow_run events
permissions:
  actions: read
  checks: write
```

**Check token permissions:**

```bash
gh auth status
gh api user
```

</permission_issues>

<timeout_issues>

### Job Timeout

**Symptoms:**

- Job cancelled after timeout
- "The job running on runner xxx has exceeded the maximum execution time"

**Solutions:**

```yaml
jobs:
  build:
    timeout-minutes: 60 # Increase timeout (max 360 for private repos)
    steps:
      - name: Long step
        timeout-minutes: 30 # Per-step timeout
```

**Prevention:**

- Add step timeouts for flaky operations
- Use matrix to parallelize
- Cache dependencies
  </timeout_issues>

<cache_gh_issues>

### Cache Issues

**Symptoms:**

- Cache miss every time
- "Cache not found for key"
- Stale cache

**Debug:**

```bash
# List caches
gh cache list
gh cache list --json id,key,createdAt,sizeInBytes

# Delete specific cache
gh cache delete <cache-id>

# Delete all caches
gh cache delete --all
```

**Common causes:**

- Cache key changes (dependency lockfile hash)
- Cache evicted (7 day limit, 10GB total)
- Different runner OS than cached
  </cache_gh_issues>

<checkout_issues>

### Checkout Issues

**Symptoms:**

- "fatal: reference is not a tree"
- Wrong commit checked out
- Missing files

**Solutions:**

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0 # Full history
    ref: ${{ github.event.pull_request.head.sha }} # Exact commit
    submodules: recursive # Include submodules
```

</checkout_issues>

<workflow_run_issues>

### Workflow Run Event Issues

**Symptoms:**

- workflow_run not triggering
- Can't download artifacts from triggering workflow

**Solutions:**

```yaml
# Correct workflow_run setup
on:
  workflow_run:
    workflows: ["CI"]  # Exact name from triggering workflow
    types: [completed]

# Download artifacts from triggering workflow
- uses: dawidd6/action-download-artifact@v2
  with:
    workflow: ci.yml
    run_id: ${{ github.event.workflow_run.id }}
```

</workflow_run_issues>
</github_actions_issues>

<debugging_scripts>

## Debugging Scripts

### Save All CI State

```bash
#!/bin/bash
PROJECT="${1:-$(basename $(pwd))}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT="/tmp/$PROJECT/ci-debug-$TIMESTAMP"
mkdir -p $OUTPUT

echo "Collecting CI state..."

# Vercel state
mkdir -p $OUTPUT/vercel
vercel ls --output json > $OUTPUT/vercel/deployments.json 2>/dev/null
vercel env ls > $OUTPUT/vercel/env-vars.txt 2>/dev/null

# GitHub state
mkdir -p $OUTPUT/github
gh run list --limit 20 --json databaseId,status,conclusion,name,headBranch,createdAt > $OUTPUT/github/runs.json

# Get latest failure
FAILED=$(jq -r '[.[] | select(.conclusion=="failure")][0].databaseId // empty' $OUTPUT/github/runs.json)
if [ -n "$FAILED" ]; then
    echo "Getting logs for failed run: $FAILED"
    gh run view $FAILED --log-failed > $OUTPUT/github/failed-logs.txt 2>&1
    gh run download $FAILED --dir $OUTPUT/github/artifacts 2>/dev/null
fi

# Git state
git log --oneline -10 > $OUTPUT/git-log.txt
git status > $OUTPUT/git-status.txt
git branch -a > $OUTPUT/git-branches.txt

echo "CI state saved to: $OUTPUT"
ls -la $OUTPUT
```

### Compare Two Deployments

```bash
#!/bin/bash
DEPLOY1="$1"
DEPLOY2="$2"
OUTPUT="/tmp/compare-deployments"
mkdir -p $OUTPUT

vercel inspect $DEPLOY1 > $OUTPUT/deploy1.txt
vercel inspect $DEPLOY2 > $OUTPUT/deploy2.txt

diff $OUTPUT/deploy1.txt $OUTPUT/deploy2.txt > $OUTPUT/diff.txt

echo "Differences:"
cat $OUTPUT/diff.txt
```

</debugging_scripts>

<quick_fixes>

## Quick Fix Checklist

### Vercel Build Failed

- [ ] Pull latest env: `vercel pull`
- [ ] Build locally: `vercel build --debug`
- [ ] Check error in logs (look for red text)
- [ ] Try force deploy: `vercel deploy --force`

### GitHub Action Failed

- [ ] View failed logs: `gh run view <id> --log-failed`
- [ ] Re-run with debug: `gh run rerun <id> --debug`
- [ ] Check permissions in workflow file
- [ ] Verify secrets are set: `gh secret list`

### Both Failing

- [ ] Check if recent code change broke build
- [ ] Verify dependencies: `npm ci` locally
- [ ] Check for env var differences
- [ ] Review recent changes: `git diff HEAD~5`
      </quick_fixes>
