---
name: gh-actions-pr-permissions-troubleshoot
description: Troubleshoot GitHub Actions failures when creating branches or pull requests (GITHUB_TOKEN permissions, org policies, GH_PR_TOKEN fallback).
---

## Symptoms

- Workflow can push a branch but cannot open a PR.
- Error contains:
  - "GitHub Actions is not permitted to create or approve pull requests."

## Checklist

1) Confirm repository settings

- See `docs/github-actions-setup.md`.
- Repository settings -> Actions -> General -> Workflow permissions:
  - Select **Read and write permissions**.
  - Enable **Allow GitHub Actions to create and approve pull requests**.

2) Confirm the workflow requests permissions

- Check the workflow file contains:
  - `permissions: contents: write`
  - `permissions: pull-requests: write`

3) Fallback if org policy blocks PR creation

- Create a fine-grained PAT with:
  - Contents: Read and write
  - Pull requests: Read and write
- Store it as repository secret: `GH_PR_TOKEN`.

4) Re-run the PR-creating workflow

- Re-run **Smoke Test - GitHub Permissions**.
- Confirm it creates a PR.
