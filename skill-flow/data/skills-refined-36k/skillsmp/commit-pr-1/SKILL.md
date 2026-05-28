---
name: commit-pr
description: Create commits and PRs with GitOps deployment awareness. Use when committing code or creating pull requests.
allowed-tools: Bash, Read, Grep
---

# Commit and PR Workflow

Create commits and pull requests with awareness of the GitOps deployment pipeline.

## Deployment Pipeline (GitOps/Argo CD)

**Merging a PR to main triggers automatic deployment:**

1. GitHub Actions builds Docker images → pushes to GHCR
2. GHA updates `helm/missing-table/values-doks.yaml` with new image tags
3. Argo CD detects helm changes → syncs to DOKS cluster (~2-3 min)

**No manual build/push needed.** Just merge the PR and Argo handles deployment.

## Workflow

### Creating a Commit

1. Stage only the relevant files (don't use `git add .`)
2. Use conventional commit format:
   - `feat:` - New features
   - `fix:` - Bug fixes
   - `chore:` - Maintenance
   - `refactor:` - Code restructuring
   - `docs:` - Documentation
3. Include `Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>` in commit message

### Creating a PR

1. Push the branch: `git push origin <branch-name>`
2. Create PR with `gh pr create`
3. Include summary and test plan in PR body
4. After PR is created, inform the user of the PR URL

### After PR is Merged

When the user says they merged the PR:

1. **Do NOT manually build or push images** - GHA handles this
2. **Do NOT run `./build-and-push.sh`** - this is for local dev only
3. Simply wait for the pipeline:
   - CI runs tests (~1-2 min)
   - CI builds and pushes images (~2 min)
   - CI updates helm values
   - Argo CD syncs (~1 min)
4. If asked to verify deployment, check:
   ```bash
   kubectl get pods -n missing-table
   kubectl get applications -n argocd missing-table
   ```

## Common Issues

### Deployment not updating?
Force Argo refresh:
```bash
kubectl -n argocd patch application missing-table --type=merge -p '{"metadata":{"annotations":{"argocd.argoproj.io/refresh":"hard"}}}'
```

### Check current image versions:
```bash
kubectl get pods -n missing-table -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[0].image}{"\n"}{end}'
```
