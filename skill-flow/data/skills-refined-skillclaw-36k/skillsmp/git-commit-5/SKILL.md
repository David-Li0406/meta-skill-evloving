---
name: git-commit
description: Conventional commit format, type selection, and commit best practices
---

## Critical Rules

- Never run `git add` unless explicitly requested
- Examine actual diff content to determine type, not filenames
- When uncertain about body inclusion, err toward including it

## Conventional Commits

Format: `type(scope): description`

Types: feat, fix, docs, style, refactor, test, chore, build, ci, perf, revert

## Subject Line

- Max 72 characters (enforced by commitlint)
- Describe what the change accomplishes, not what you did
- Imperative mood, lowercase type, no trailing period

Do NOT: use past tense, restate the diff, write generic messages ("fix bug")

## When to Include a Body

Include body when ANY apply:

- feat/fix type (explain why, not just what)
- Non-obvious root cause or design decision
- Change affects 5+ files or 100+ lines
- Breaking changes or migration needed

Skip body when ALL apply:

- Mechanical change (rename, formatting, dependency bump)
- Subject fully captures intent
- Diff is self-explanatory

## Body

- Separate from subject with blank line
- Explain WHY: motivation, tradeoffs, alternatives considered
- Hard-wrap at 72 characters
- Use exactly two `-m` flags: one for subject, one for entire body
- For multi-line body, use `$'...\n...'` syntax: `git commit -m "subject" -m $'line one\nline two'`

## Type Selection

Determine from AGENTS.md project context:

- Source code changes -> feat/fix
- Tooling, config, dependencies -> chore
- CI/CD pipelines -> ci
- Documentation -> docs

If unclear, ask before committing.

## Hook Failures

If rejected by commitlint: read error, fix violation, retry.

If pre-commit auto-fixes files: `git update-index --again`, retry.

If validation error: stop and report. Do not bypass hooks.
