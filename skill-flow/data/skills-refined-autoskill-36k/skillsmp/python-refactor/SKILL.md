---
name: python-refactor
description: Assist with automated, safe, and explainable Python refactorings. Detects simple anti-patterns and offers AST-based transformations with patches and unit-test friendly changes.
---

# Python Refactor Skill

## Overview

This skill helps authors and agents perform automated, small, safe Python refactorings. It focuses on detectable, low-risk transformations (formatting to f-strings, simplify boolean expressions, remove unused imports, small function extraction suggestions) and produces patch files or dry-run diffs.

Use this skill when you want a reproducible, reviewable set of refactor suggestions that can be applied automatically or passed to a human reviewer.

## Quick Start

- Use the `scripts/analyze.py` to scan a directory for refactor opportunities.
- Use the `scripts/refactor.py` to generate patches (preview mode by default).
- Use the `scripts/apply_patch.py` to apply confirmed patches safely (creates backups).

## When to use

- Large repositories where repetitive low-risk refactors are needed.
- Codebases with inconsistent formatting or migration to modern Python features (f-strings, type hints).
- As a pre-PR pass to reduce mechanical review comments.

## Scripts

- `scripts/analyze.py`: static analysis for refactor candidates.
- `scripts/refactor.py`: performs AST transforms and outputs unified diffs.
- `scripts/apply_patch.py`: applies diffs to files with backups.

## Resources

- `references/python-style-guide.md`: opinionated style guidance used by the skill.
- `references/refactoring-patterns.md`: patterns the skill recognizes and how it changes code.

## Safety and Scope

This skill only performs transformations that can be verified via unit tests. Always run tests after applying patches and review diffs before committing.
