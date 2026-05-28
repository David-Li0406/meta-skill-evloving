---
name: git-commit
description: Create commit messages following conventions or sensible defaults. Use when committing code changes, writing commit messages or managing git history.
license: MIT
compatibility: opencode, claude code, copilot
metadata:
    author: Vasil Kotsev
    audience: contributors
    version: "1.0.0"
---

# Git Commit Messages

When working on codebases that leverage `git` as the `VCS`, ensure that
any existing conventions like [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/#specification)
are leveraged for code that you have generated, staged & plan to commit.
If no such conventions are set-up in the repository, fallback to sensible defaults

## Prerequisites

Before committing, ensure you're working on a feature branch, not the main branch.

```sh
# Check current branch
git branch --show-current
```

If you're on `main` or `master`, create a new branch first:

```sh
git checkout -b <type>/<short-description>
```

## Branch Naming Conventions

Use the following branch naming convention:

- `<type>/<short-description>`

### Branch Types

| Type      | Purpose                     |
| --------- | --------------------------- |
| `feature` | New feature                 |
| `fix`     | Bug fix                     |
| `docs`    | Documentation               |
| `ci`      | CI related changes          |
| `chore`   | Maintenance related changes |

### Branch Examples

- `feature/introduce-otel`
- `fix/wrong-validation`
- `chore/bump-dependencies`

## Staging Documents

- Prefer committing concise stuff, don't include a lot of changes in a single commit
- Don't stage documents that include secrets, API keys or other sensitive information
- Stash any previous unrelated changes, done by the person contributing to this
  codebase, before you stage and commit anything else. Save those stashes with
  some kind of a human readable name

## Message Format

If conventions like `Conventional Commits` are in-place, use those and ignore
the defaults below. Look through the `git log` history to determine if
these conventions are used.

```txt
<subject>

<body?>

<footer?>
```

### Subject Line Rules

- Use imperative, present tense: "Add feature" not "Added feature"
- Capitalize the first letter
- No period at the end
- Maximum 80 characters

### Body Guidelines

- Explain **what** and **why**, not how
- Use imperative mood and present tense
- Include motivation for the change
- Contrast with previous behavior when relevant

### Principles

- Each commit should be a single, stable change
- Commits should be independently reviewable
- The repository should be in a working state after each commit

### Commit Message Examples

The examples below are for the sensible defaults, they don't
follow any specific convention. Ignore them if a convention
is used in this repository.

```txt
Optimize integration test infrastructure

Contains full refactor of the integration test suite.
Introduces the following changes:

    * Full API configuration with a dedicated E2E environment config
    * Respawn - tool for intelligent DB clean-up between tests
    * Reseeding mechanism
    * Custom MS SQL Server 2022 Docker image with tmpfs support
    * Smaller alpine based images, whenever possible
    * And more...

End result is that the Integration Tests NUKE target now runs in one minute in local
environments and around 3 minutes in CI pipelines (due to not leveraging image caches).
Reducing the evaluation time in the build agents from ~28 minutes to ~3 minutes flat.
```

```txt
Opt-out of .NET CLI telemetry in GHA workflows
```

## Hooks

If `git hooks` are setup for this repository ensure that:

- They pass
- Don't commit anything with the `--no-verify` argument
