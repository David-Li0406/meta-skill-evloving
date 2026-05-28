---
name: bootstrap-qcow2-create-pr
description: Create or update GitHub pull requests for bootstrap-qcow2 using the in-repo Crystal helper Bootstrap::CodexUtils.create_pull_request (no gh/CLI dependencies). Use when automating PR creation from inside the container or sysroot namespace.
---

# Create a PR using `Bootstrap::CodexUtils`

Use the in-repo helper to create PRs via the GitHub REST API without relying on `gh`.

## Preconditions

- You have a branch pushed to `origin` (e.g. `codex/my-branch`).
- A GitHub token exists in `/work/.git-credentials` (or pass an explicit path to `create_pull_request`).

## Create the PR

From the repo root (`/work/bootstrap-qcow2` when live-bound):

```sh
./bin/bq2 github-pr-create --title "PR title" --head codex/my-branch --body-file pr-body.md
```

## Notes

- If the API call fails, the helper raises with the HTTP status/body to copy into debugging output.
- Updating an existing PR body/title requires a PATCH request; reuse the same token/headers pattern (see `src/codex_utils.cr`).
- Pass `--repo owner/name` when running outside a git checkout (e.g., staged snapshots) and inference fails.
- Defaults to `/work/.git-credentials` when present (override with `--credentials`).
