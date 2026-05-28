---
name: github-release
description: Create GitHub releases with version tags, release notes, and changelog generation from merged PRs
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: version-control
---

## What I do

I create GitHub releases using the `gh` CLI. I draft release notes from merged PRs, propose version bumps, and provide copy-pasteable commands for creating tagged releases.

## When to use me

Use this when:

- You're preparing a tagged release
- You need to generate release notes automatically
- You want to document changes since last release
- You're bumping version numbers (patch/minor/major)

## Common Workflow

```bash
gh release view                # View latest release
gh release create v1.0.0       # Create release from tag
gh release edit v1.0.0         # Edit release notes
gh release delete v1.0.0       # Delete release (local tag persists)
```

## Key Concepts

- **Semantic Versioning**: MAJOR.MINOR.PATCH (e.g., 1.2.0)
- **Release Notes**: Auto-generated from merged PRs
- **Draft Releases**: Preview releases before publishing
- **Pre-releases**: Alpha, beta, RC versions

## Source Files

- `.github/` directory: May contain release workflows
- `package.json`: Version number and release scripts

## Code Patterns

- Use `gh pr list` to find merged PRs since last release
- Categorize changes (Features, Fixes, Breaking, etc.)
- Use `gh release create` with `--title` and `--notes`
- Draft first, then publish when ready

## Operational Constraints

- Always draft release notes before creating release
- Verify version number follows semantic versioning
- Ask clarifying questions if versioning scheme unclear
- Include breaking changes prominently in release notes
