---
name: devcontainer-maintenance
description: Use this skill when maintaining or changing the devcontainer environment for the repo, including editing definition files or requesting environment rebuilds.
---

# Devcontainer Maintenance

## Scope

- Single reproducible development environment.
- Definition files: `.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json`, `scripts/devcontainer-post-create.sh`, `ai-forecasting-hackathon.code-workspace`.

## Change Policy

- Environment changes require project owner approval and a devcontainer rebuild.
- Modify definition files directly, avoiding ad-hoc local installs to ensure reproducibility and documentation.

## Available Tools

- Base image: `mcr.microsoft.com/devcontainers/base:ubuntu`
- Node and npm
- Common CLIs: `git`, `gh`, `rg`, `jq`, `fd`, `curl`, `tree`, `inotifywait`, `entr`
- IDE for project owner: `code-tunnel`

## Host Binds and Worktrees

- Host binds are defined in `devcontainer.json` and must exist for rebuilds to succeed.
- Host binds persist caches, OAuth tokens, and configs across rebuilds.
- Worktrees are located in `/workspaces/worktrees/`.
- Shared across worktrees: host binds and `/workspaces/worktrees/shared/`.

## Notes

- Toolchain usage is documented in package-level documentation.
- All agents and the project owner use the same devcontainer on the same Ubuntu 24.04 host OS.
- No other clones of the repo exist, so gitignored changes and caches persist unless removed during worktree removal.