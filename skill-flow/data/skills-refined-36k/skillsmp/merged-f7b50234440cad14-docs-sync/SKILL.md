---
name: docs-sync
description: Use this skill to analyze the main branch implementation and configuration for missing, incorrect, or outdated documentation in the `docs/` directory. It is applicable when auditing doc coverage, syncing docs with code, or proposing doc updates/structure changes.
---

# Docs Sync

## Overview

Identify documentation coverage gaps and inaccuracies by comparing main branch features and configuration options against the current docs structure, then propose targeted improvements.

## Workflow

1. **Confirm scope and base branch**
   - Identify the current branch and default branch (usually `main`).
   - Prefer analyzing the current branch to keep work aligned with in-flight changes.
   - If the current branch is not `main`, analyze only the diff vs `main` to scope doc updates.
   - Avoid switching branches if it would disrupt local changes; use `git show main:<path>` or `git worktree add` when needed.

2. **Build a feature inventory from the selected scope**
   - If on `main`: inventory the full surface area and review docs comprehensively.
   - If not on `main`: inventory only changes vs `main` (feature additions/changes/removals).
   - Focus on user-facing behavior: public exports, configuration options, environment variables, CLI commands, default values, and documented runtime behaviors.
   - Capture evidence for each item (file path + symbol/setting).
   - Use targeted search to find option types and feature flags (e.g., `rg "Options"`, `rg "process.env"`, `rg "export"`).
   - For OpenAI platform features, invoke `$openai-knowledge` to pull current details from the OpenAI Developer Docs MCP server, treating the SDK source code as the source of truth when discrepancies appear.

3. **Doc-first pass: review existing pages**
   - Walk each relevant page under `docs/` (excluding `docs/ja`, `docs/ko`, and `docs/zh`).
   - Identify missing mentions of important, supported options (opt-in flags, env vars), customization points, or new features.
   - Propose additions where users would reasonably expect to find them on that page.

4. **Code-first pass: map features to docs**
   - Review the current docs information architecture under `docs/` and `mkdocs.yml`.
   - Determine the best page/section for each feature based on existing patterns and the API reference structure.
   - Identify features that lack any doc page or have a page but no corresponding content.
   - Note when a structural adjustment would improve discoverability.
   - When improving reference pages, treat the corresponding docstrings/comments in the source code as the source of truth.

5. **Detect gaps and inaccuracies**
   - **Missing**: features/configs present in main but absent in docs.
   - **Incorrect/outdated**: names, defaults, or behaviors that diverge from main.
   - **Structural issues** (optional): pages overloaded, missing overviews, or mis-grouped topics.

6. **Produce a Docs Sync Report and ask for approval**
   - Provide a clear report with evidence, suggested doc locations, and proposed edits.
   - Ask the user whether to proceed with doc updates.

7. **If approved, apply changes (English only)**
   - Edit only English docs in `docs/**`.
   - Do **not** edit `docs/ja`, `docs/ko`, or `docs/zh`.
   - Keep changes aligned with the existing docs style and navigation.
   - Update `mkdocs.yml` when adding or renaming pages.
   - Build docs with `make build-docs` after edits to verify the docs site still builds.

## Output format

Use this template when reporting findings:

Docs Sync Report

- Doc-first findings
  - Page + missing content → evidence + suggested insertion point
- Code-first gaps
  - Feature + evidence → suggested doc page/section (or missing page)
- Incorrect or outdated docs
  - Doc file + issue + correct info + evidence
- Structural suggestions (optional)
  - Proposed change + rationale
- Proposed edits
  - Doc file → concise change summary
- Questions for the user

## References

- `references/doc-coverage-checklist.md`