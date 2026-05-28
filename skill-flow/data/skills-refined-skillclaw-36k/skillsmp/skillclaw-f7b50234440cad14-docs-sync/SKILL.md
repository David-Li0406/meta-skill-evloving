---
name: docs-sync
description: Use this skill when you need to audit documentation coverage, sync documentation with code changes, or propose updates to the documentation structure.
---

# Skill body

## Overview

Identify documentation gaps and inaccuracies by comparing the main branch features and configuration options against the current documentation structure, then propose targeted improvements.

## Workflow

1. **Confirm Scope and Base Branch**
   - Identify the current branch and default branch (usually `main`).
   - Prefer analyzing the current branch to keep work aligned with in-flight changes.
   - If the current branch is not `main`, analyze only the diff vs `main` to scope documentation updates.
   - Avoid switching branches if it would disrupt local changes; use `git show main:<path>` or `git worktree add` when needed.

2. **Build a Feature Inventory from the Selected Scope**
   - If on `main`: inventory the full surface area and review documentation comprehensively.
   - If not on `main`: inventory only changes vs `main` (feature additions/changes/removals).
   - Focus on user-facing behavior: public exports, configuration options, environment variables, CLI commands, default values, and documented runtime behaviors.
   - Capture evidence for each item (file path + symbol/setting).
   - Use targeted search to find option types and feature flags (for example: `rg "Options"`, `rg "process.env"`, `rg "export"`).
   - For OpenAI platform features, invoke `$openai-knowledge` to pull current details from the OpenAI Developer Docs MCP server, treating the SDK source code as the source of truth when discrepancies appear.

3. **Doc-First Pass: Review Existing Pages**
   - Walk each relevant page under `docs/` (excluding translated docs under `docs/ja`, `docs/ko`, and `docs/zh`).
   - Identify missing mentions of important, supported options (opt-in flags, environment variables), customization points, or new features.
   - Propose additions where users would reasonably expect to find them on that page.

4. **Code-First Pass: Map Features to Docs**
   - Review the current documentation information architecture and determine the best page/section for each feature based on existing patterns.
   - Propose structural changes to improve documentation clarity and accessibility.

5. **Report and Approval**
   - Compile findings and proposed changes into a report.
   - Seek approval before making any edits to the documentation.