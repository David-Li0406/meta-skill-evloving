---
name: github-releases
description: manage versioning, tags, changelogs, and release assets
metadata:
  category: github
---

# GitHub Releases

## What is it?

This skill manages the **delivery phase** of software development. It enables agents to create and manage GitHub Releases, tags, and associated assets (binaries, documentation, etc.).

## Success Criteria

- Releases are created with semantic tags (e.g., `v1.2.3`).
- Draft releases are used for preparation and verified before publishing.
- Assets are successfully uploaded and verified.
- Changelogs are generated or provided in the release notes.

## Why use it?

- **Version management**: Create and manage semantic versioned releases
- **Asset distribution**: Upload and share binaries, documentation, and artifacts
- **Draft workflow**: Safely prepare releases before publishing
- **Changelog automation**: Generate or manage release notes efficiently
- **Tag synchronization**: Keep git tags and releases properly aligned

## Prerequisites

- **GitHub CLI**: `gh` command-line tool must be installed and authenticated (`gh auth login`)
- **Repository Permissions**: Push or admin access to create/manage releases and tags
- **Semantic Versioning**: Understanding of SemVer (e.g., `v1.2.3`) or project versioning convention

## When to use this skill

- "Create a new release `v1.0.0` for the current main branch."
- "Upload the `dist/app.zip` asset to the latest release."
- "What is the latest release for this project?"
- "Update the release notes for `v0.9.0-beta`."
- "Download the binary from the latest stable release."

## What this skill can do

- **Management**: Create, Edit, List, and Delete releases.
- **Assets**: Upload, Download, and Delete release assets.
- **Versioning**: Manage tags associated with releases.
- **Verification**: Verify attestations for releases and assets.

## What this skill will NOT do

- Manage GitHub Actions workflows (use `github-action-creator`).
- Manage project boards (use `github-projects`).
- Write code or fix bugs (use `github-issues` and local editing).
- Automatically determine next version numbers (use external tools like `release-please` or `semantic-release`).
- Manage source code commits or pull requests (use `github-issues` and `github-pr-flow`).
- Create changelogs from scratch (can only include provided notes; consider `release-please` for automation).

## How to use this skill

1. **Discovery**: Use `list_releases` (MCP) or `gh release list` (CLI) to see existing releases.
2. **Identification**: Use `get_latest_release` or `get_release_by_tag` to get specific metadata.
3. **Creation**: Use `gh release create <tag>` to trigger a new release. Use the `--draft` flag for safety.
4. **Assets**: Use `gh release upload` to attach files after the release object exists.

### Validation Steps
- Always verify the release exists after creation: `gh release view <tag>`
- Confirm assets uploaded successfully: `gh release view <tag> --jq '.assets[].name'`
- Test artifact downloads before announcing: `gh release download <tag> --dir ./test`

## Error Handling & Validation

### Common Issues
- **Tag already exists**: Ensure tag name is unique or specify `--target` to point to a different commit
- **Authentication failed**: Run `gh auth login` and verify repository access
- **Asset upload fails**: Check file size limits and network connection
- **Release not found**: Verify tag spelling and that release is published (not in draft state)

## Tool usage rules

### CLI vs MCP Operations
- **Informational (MCP preferred)**: `list_releases`, `get_latest_release`, `get_release_by_tag` work via MCP tools
- **Write operations (CLI required)**: Create, Edit, Upload, Delete require `gh release` CLI or direct API calls
- **MCP tools are read-only** for releases; all modifications use CLI

### Release Management Best Practices
- **Safety First**: Always create releases as **drafts** (`--draft`) if the environment is sensitive or if user verification is required.
- **Tagging**: Ensure the tag name follows the project's versioning convention (usually SemVer `vX.Y.Z`).
- **Targeting**: Specify the target branch or commit SHA (`--target`) if not releasing from the default branch.
- **Cleanup**: Use `--cleanup-tag` when deleting old releases to also remove git tags.
- **Prerelease Flag**: Use `--prerelease` for alpha, beta, rc versions to avoid marking as stable.
- **Release Notes**: Reference related PRs/issues using `#123` format for better traceability.


## Examples

See [references/examples.md](references/examples.md) for concrete CLI and API examples.

## Limitations

- MCP read tools (`list_releases`, etc.) should be preferred for informational queries.
- Write operations (Create, Edit, Upload) MUST use the `gh release` CLI or direct API calls.