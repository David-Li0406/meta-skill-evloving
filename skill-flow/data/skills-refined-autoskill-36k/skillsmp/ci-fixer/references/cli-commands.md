# CLI Commands Quick Reference

Quick reference for CI/CD debugging. For detailed commands, see:

- [GitHub CLI Reference](github-cli.md)
- [Vercel CLI Reference](vercel-cli.md)

---

## GitHub Actions - Most Used

```bash
# List runs for current branch
gh run list --branch $(git branch --show-current) --limit 5

# Watch a run in real-time
gh run watch <run-id>

# Get failed logs only
gh run view <run-id> --log-failed

# Re-run failed jobs
gh run rerun <run-id> --failed

# Download artifacts
gh run download <run-id> --dir /tmp/artifacts
```

---

## Vercel - Most Used

```bash
# List recent deployments
vercel ls --output json | head -5

# Get deployment details
vercel inspect <deployment-url>

# Stream runtime logs
vercel logs <deployment-url>

# Pull env vars locally
vercel pull --yes

# Build locally to reproduce issues
vercel build --debug
```

---

## Netlify - Most Used

```bash
# Check status
netlify status

# List sites
netlify sites:list

# Get recent deploys
netlify deploys

# View deploy details
netlify deploys --json | jq '.[0]'

# Build locally to reproduce
netlify build --dry-run

# View build logs
netlify build
```

---

## Local Verification Commands

### Lint

```bash
bun run lint
npx eslint . --fix
npx prettier --check .
npx prettier --write .
```

### Type Check

```bash
npx tsc --noEmit
bun run typecheck
```

### Tests

```bash
npm test
bun run test:ci
npx jest
npx vitest run
```

### Build

```bash
bun run build
npx next build
npx vite build
```

---

## One-Liners

```bash
# Get latest run ID for current branch
gh run list --branch $(git branch --show-current) -L1 --json databaseId -q '.[0].databaseId'

# Get latest failed run
gh run list --status failure -L1 --json databaseId -q '.[0].databaseId'

# Re-run latest failed
gh run rerun $(gh run list --status failure -L1 --json databaseId -q '.[0].databaseId') --failed

# Get Vercel deployment URL for current commit
vercel ls --output json | jq -r --arg sha "$(git rev-parse HEAD)" '.[] | select(.meta.githubCommitSha == $sha) | .url'
```
