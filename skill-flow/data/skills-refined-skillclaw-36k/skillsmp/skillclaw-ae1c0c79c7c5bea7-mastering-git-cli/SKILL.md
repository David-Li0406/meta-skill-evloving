---
name: mastering-git-cli
description: Use this skill when working with Git repositories, commits, branches, merging, rebasing, and CI/CD integration to streamline your development workflows.
---

# Git CLI Skill (2025 Edition)

Production-ready Git workflows and automation for modern development.

> **Compatibility:** Git 2.38+ recommended. Git 2.51+ for full SHA-256/Reftable support.

## Triggers

This skill activates on:
- `git` commands and version control questions
- Merge conflicts, rebase operations, cherry-pick decisions
- Worktree setup and submodule management
- Branch strategy and repository troubleshooting
- Large repo optimization (Scalar, sparse checkout, blobless clones)
- CI/CD git integration and performance tuning

## Quick Start

### Most Common Patterns

```bash
# Clone and start working (use switch, not checkout)
git clone <url> && cd <repo>
git switch -c feature-x

# Commit workflow
git add -A && git commit -m "feat: description"
git push -u origin feature-x

# Merge feature to main
git switch main && git pull
git merge --no-ff feature-x
git push

# Large repo? Use partial clone
git clone --filter=blob:none <url>
```

### Modern Git Config (2025 Defaults)

```bash
# Core workflow
git config --global pull.rebase true
git config --global push.autoSetupRemote true
git config --global merge.conflictStyle zdiff3
git config --global diff.algorithm histogram
git config --global rerere.enabled true
git config --global rebase.autoStash true

# Performance (essential for large repos)
git config --global core.fsmonitor true
git config --global fetch.prune true
git config --global feature.manyFiles true

# SSH signing (simpler than GPG)
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true

# Enable background maintenance
git maintenance start
```

## Decision Trees

### Merge vs Rebase vs Cherry-pick

```
Need to integrate changes?
│
├─ All commits from a branch?
│  ├─ Shared branch (pushed/collaborative) → MERGE
│  └─ Local-only branch → REBASE (cleaner) or MERGE
│
└─ Specific commits only?
   └─ CH
```