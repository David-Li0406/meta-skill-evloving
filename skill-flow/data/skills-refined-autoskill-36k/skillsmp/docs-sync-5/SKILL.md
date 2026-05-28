---
name: docs-sync
description: Keep documentation consistent in this repo. Use when you need to update or propagate changes across README/AGENTS/CLAUDE/.codex docs.
---

# Docs Sync

Keep documentation consistent and up-to-date for this single-package repo. When updating commands, paths, or tool behavior, propagate changes to all relevant doc files to avoid stale references.

## Scope

Documentation files to consider:

- `README.md`
- `AGENTS.md`
- `CLAUDE.md` (symlink to `AGENTS.md`, do not edit directly)
- `.codex/**` (Codex agent configs and skills)
- Any new doc-like Markdown files added later

## Workflow

1. **Find doc files**: Scan for all documentation files listed in Scope.
2. **Update references consistently**: When changing a command, path, or pattern, update ALL occurrences across all doc files. Never partially update.
3. **Add/update explanations**: When changing a command or config, add or update a short explanation of what it does and why.
4. **Run formatter**: Execute `pnpm format` if you touched Markdown or config files that are formatted.
5. **Run validation (if needed)**: If documentation changes include code or tooling changes, run `pnpm lint`, `pnpm typecheck`, and `pnpm test`. Skip these when edits are doc-only.
6. **Summarize changes**: Report files changed and flag anything that needs human review.

## Guidelines

- Keep docs concise and scannable
- Use consistent terminology across all files
- Prefer examples over lengthy explanations
- Update version numbers/dates if present
- Remove obsolete sections rather than leaving stale content
- When adding new commands, include both the command and a brief explanation
- Do not introduce instructions that conflict with `AGENTS.md`
- Do not edit `CLAUDE.md` directly; update `AGENTS.md` instead
- Mermaid: wrap node text in quotes like `A["Label"]` and `B{"Question?"}` to avoid parse issues with punctuation

## Output Requirements

Always finish with a summary:

- **Files changed**: List of documentation files modified
- **What to review**: Any changes that need human verification (e.g., explanations that may need refinement, removed sections)
- **Validation status**: Commands run, or explicitly note what was skipped
