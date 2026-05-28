---
name: greenhouse-releases
description: Release pipeline and deployment workflows for the Greenhouse application. Use when managing releases with pipelinectl, deploying applications with lotus, checking deployment health, summarizing release information, or working with PR dev instances.
---

# Greenhouse Releases

**Critical Rule:** NEVER merge Pull Requests manually. The release pipeline handles this.

## Tools

### pipelinectl

POSIX-compliant CLI for managing release pipelines.

**Commands:**

```bash
pipelinectl list --all                              # View all historical releases
pipelinectl show <release-id>                       # Show release details (only needs release ID)
pipelinectl logs <release-id>                       # Get release logs
pipelinectl start --pull-request-url <URL> --no-watch  # Start release (app name inferred from cwd)
pipelinectl promote-to <stage> --no-watch           # Promote release
pipelinectl cancel <release-id> --no-watch          # Cancel release
```

**Notes:**

- Commands `promote-to`, `start`, and `cancel` require `--no-watch` flag
- Application name inferred from current directory or `.release-pipeline` file
- Release stages: assembling → canary → stable

### lotus

Tool for application deployments.

**PR Dev Instances:**

```bash
lotus <command> --environment pr-<number> --space dev --region use1
```

**Deployment:**

```bash
lotus deploy --auto-pr  # Auto-create and handle GitOps PRs
```

**Health Check:**

```bash
kubectl get po -n greenhouse -l lotus.greenhouse.io/environment=<instance_name>
```

Instance is ready when:

- `*-web-*` and `-post-deploy-worker` pods are `Running`, OR
- `-predeploy-` pod has `Completed` status

### white-pages-client

Retrieve user information from internal systems:

```bash
one --by-github-login <login>  # Get full name from GitHub login
```

## Release Information Workflow

When summarizing a release:

1. Find latest release ID: `pipelinectl list --all`
2. Get included PRs: `pipelinectl show <ID>`
3. For each PR:
   - Fetch PR details using `github.get_pull_request`
   - Resolve author's real name: `white-pages-client one --by-github-login <login>`
   - Fetch commits: `github.list_commits` with PR's `head.sha`
4. Present summary with: PR title, URL, author's real name, commit messages

## Output

Write summaries to markdown files under `.scratch/` directory.
