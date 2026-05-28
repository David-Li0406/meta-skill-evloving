---
name: repo-bootstrap
description: Bootstrap a new project repo created from this template (GitHub Actions permissions, init flow, and Windsurf copy-pack sync).
---

## When to use

Use this when you just created a new repository from this template and want the safest, fastest path to a usable project setup.

## Checklist

1) Verify GitHub Actions permissions

- See `docs/github-actions-setup.md`.
- Confirm:
  - Workflow permissions: **Read and write**
  - Allow GitHub Actions to create and approve pull requests

2) (Optional) Run the GitHub permissions smoke test

- Run **Smoke Test - GitHub Permissions**.
- Confirm that it creates a PR.

3) Run interactive initialization in Windsurf

- Run `/init-project`.
- Ensure it creates/updates:
  - `orga/domain/project-brief.md`
  - baseline domain docs under `orga/domain/`
  - project-specific Windsurf customizations under `docs/windsurf/`

4) Apply the mechanical initialization PR

- Run GitHub Actions workflow **Initialize Project**.
- Merge the PR.

5) Confirm Windsurf sync

- Ensure `.windsurf/` reflects `docs/windsurf/` (rules, workflows, skills).
- If you maintain multiple repos from this template, keep `docs/windsurf/` as the copy-pack.
