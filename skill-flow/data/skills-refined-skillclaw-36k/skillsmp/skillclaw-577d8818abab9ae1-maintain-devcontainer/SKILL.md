---
name: maintain-devcontainer
description: Use this skill when you need to maintain or change the devcontainer environment for a repository, including editing configuration files and managing rebuilds.
---

# Maintain Devcontainer

## Scope

- Single reproducible development environment.
- Definition files: `.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json`, `scripts/devcontainer-post-create.sh`, `your-repo.code-workspace`.

## Change Policy

- Environment changes require project owner approval and a devcontainer rebuild.
- Modify definition files directly; avoid ad-hoc local installs to ensure reproducibility and proper documentation.

## Available Tools

- Base image: `mcr.microsoft.com/devcontainers/base:ubuntu`
- Node and npm
- Common CLIs: `git`, `gh`, `rg`, `jq`, `fd`, `curl`, `tree`, `inotifywait`, `entr`
- IDE for project owner: `code-tunnel`

## Host Binds and Worktrees

- Host binds are defined in `devcontainer.json` and must exist; otherwise, rebuilds will fail.
- Host binds persist caches, OAuth tokens, and configurations across rebuilds.
- Worktrees are located in `/workspaces/worktrees/`.
- Shared resources across worktrees include host binds and `/workspaces/worktrees/shared/`.

## Notes

- Toolchain usage is documented in package-level documentation.
- All agents and the project owner use the same devcontainer on the same Ubuntu 24.04 host OS.
- No other clones of the repo exist, so gitignored changes and caches persist unless removed during worktree removal.