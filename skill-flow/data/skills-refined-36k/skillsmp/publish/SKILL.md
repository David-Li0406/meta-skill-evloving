---
name: publish
description: Release package, publish to npm, cut a release, bump version, deploy. Use when ready to release, need to publish new version, or ship to npm. Handles version bump, PR, merge, tag, and publish.
disable-model-invocation: true
---

# Publish Release

End-to-end release workflow: branch, commit, PR, merge, tag, and publish to npm.

## Prerequisites

Before starting, verify:

- Working directory is clean or has only intended changes
- You're authenticated with GitHub CLI (`gh auth status`)
- GitHub Actions release workflow exists and is properly configured

### Verify Release Infrastructure

Look for a GitHub Actions workflow that handles releases. Common names include:

- `release.yml`, `release.yaml`
- `publish.yml`, `publish.yaml`
- `production.yml`, `production.yaml`
- `npm-publish.yml`, `npm-publish.yaml`

Check `.github/workflows/` for any file matching these patterns. If found, assume it's configured to handle npm publishing when a `v*` tag is pushed.

If no release workflow exists, stop and alert the user:

> No release workflow found in `.github/workflows/`. Create a workflow that triggers on `v*` tags and publishes to npm.

## Process

### 1. Gather Context

Run in parallel:

- `git status` - Check for uncommitted changes
- `git branch --show-current` - Get current branch
- `git log --oneline main..HEAD` - See commits on this branch (if any)
- `jq -r '.version' package.json` - Get current version

### 2. Ask Release Questions

Use AskUserQuestion with these questions:

**Question 1 - Release Type**:

- Header: "Version"
- Question: "What type of release is this?"
- Options:
  - `patch` - Bug fixes, no new features (0.0.X)
  - `minor` - New features, backward compatible (0.X.0)
  - `major` - Breaking changes (X.0.0)
- multiSelect: false

**Question 2 - Squash Commits**:

- Header: "Commits"
- Question: "How should commits be handled?"
- Options:
  - `squash` - Squash all commits into one release commit (Recommended)
  - `keep` - Keep individual commits as-is
- multiSelect: false

Wait for user responses before proceeding.

### 3. Prepare Changes

**If on main branch with uncommitted changes**:

1. Create release branch: `git checkout -b release/v{NEW_VERSION}`
2. Stage all changes: `git add -A`

**If on a feature branch**:

1. Note the branch name for PR creation
2. If squash requested and multiple commits exist, squash them

**Calculate new version**:

```bash
npm version {RELEASE_TYPE} --no-git-tag-version
```

This updates package.json and package-lock.json without creating a git tag.

### 4. Create Release Commit

**If squashing**: Reset commits and create single release commit.

Launch the `committer` agent with prompt:

> Create a release commit for version {NEW_VERSION}. This is a {RELEASE_TYPE} release.
> Include a brief summary of what changed based on the diff.
> Use format: `chore(release): {NEW_VERSION}`

### 5. Create Pull Request

Launch the `pr-creator` agent with prompt:

> Create a release PR for version {NEW_VERSION}.
> Title: `chore(release): v{NEW_VERSION}`
> This is a {RELEASE_TYPE} release.
> Target branch: main

Wait for PR creation confirmation.

### 6. Merge and Tag

After PR is created, ask user:

> PR created. Ready to merge and publish?
>
> - **Yes, merge now** - Merge PR and create release tag
> - **Wait for review** - Stop here, user will merge manually later

**If merging now**:

```bash
# Merge the PR (fast-forward if possible)
gh pr merge --squash --delete-branch

# Switch to main and pull
git checkout main
git pull origin main

# Create annotated tag
git tag -a v{NEW_VERSION} -m "Release v{NEW_VERSION}"

# Push tag to trigger GitHub Actions release
git push origin v{NEW_VERSION}
```

### 7. Confirm Release

After pushing the tag:

1. Get the workflow run ID using the release workflow filename detected earlier:
   ```bash
   gh run list --workflow={WORKFLOW_FILE} --limit 1 --json databaseId,url
   ```
2. Show the user:
   - Version bumped: {OLD_VERSION} → {NEW_VERSION}
   - Tag created: v{NEW_VERSION}
   - GitHub Actions run URL

3. Launch a **background subagent** (`run_in_background: true`) to monitor the release:

```
Watch the GitHub Actions release workflow and report when it completes.

Run: `gh run watch {RUN_ID} --exit-status`

When it completes:
- If successful: Report "Release v{VERSION} published to npm successfully"
- If failed: Report the failure and suggest running `gh run view {RUN_ID} --log-failed` to debug
```

4. Continue the conversation while the workflow runs. The background agent will report results when ready.

## Key Principles

- **Use PR workflow for all changes** - Merging through PRs maintains audit trail and enables review
- **Confirm before merging and tagging** - These actions are irreversible
- **Let GitHub Actions handle npm publish** - The release workflow publishes automatically when tags are pushed
- **Use conventional commits** - Format: `chore(release): vX.Y.Z`
