---
name: pr-proposer
description: Use this skill when a feature branch is ready for a Pull Request.
---

# PR Proposer Protocol

## 1. Context Gathering
- Identify the current feature branch.
- Extract all entries from `CHANGELOG.md` that are under the `## [Unreleased]` section.

## 2. Drafting the PR
Generate a professional PR description:
- **Title**: Use the most significant conventional commit message.
- **Body**: 
    - **Summary**: A 2-sentence business-level summary of the change.
    - **Detailed Changes**: The bullet points found in the changelog.
    - **Documentation**: Mention that `docs_manifest.yaml` has been synced.

## 3. Tooling
- If the `gh` CLI is installed: Propose `gh pr create --fill`.
- Otherwise: Provide the Markdown block for manual copy-pasting into GitHub.
