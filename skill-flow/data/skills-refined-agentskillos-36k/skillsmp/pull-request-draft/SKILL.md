---
name: pull-request-draft
description: Generate pull request titles and descriptions from current repo changes or diffs. Use when asked to draft a PR title/body, summarize changes for a PR, fill a PR template, or propose multiple PR title options.
---

# Pull Request Drafting

## Workflow

1. Inspect repo context
   - Check `git status` and `git diff` (and `git diff --staged` if staged).
   - If commits exist, scan recent commits for intent and scope.
   - Look for PR templates in common locations (e.g. `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `PULL_REQUEST_TEMPLATE.md`, or template folders).
   - If a template exists, follow it exactly.

2. Determine scope and audience
   - Identify the primary change type (feature, fix, refactor, docs, chores, tests).
   - Find any ticket/issue IDs in branch names, commits, or file paths; include if present.
   - Avoid speculation; only use evidence from the diff or repository context.

3. Draft output
   - Title: concise (<= 72 chars), imperative mood, include scope/ticket if standard.
   - Body: Markdown with clear sections. Prefer the template if present; otherwise use:
     - Summary (1–3 bullets)
     - Changes (bulleted list of notable edits)
     - Testing (what ran or “Not run (reason)”)
     - Risks/Notes (edge cases, migrations, rollouts)
     - Screenshots (for UI changes)
     - Related issues (if any)

4. Ask only necessary questions
   - If key details are missing (testing, rollout, breaking changes), ask brief follow‑ups.
   - If you can proceed, include TODO placeholders instead of blocking.

## Output Format

Provide output as:

Title: <single line>

```markdown
<PR body>
```

If helpful, include up to 2 alternative titles after the main one.

## Guardrails

- Do not invent facts. If uncertain, mark as TODO or ask.
- Preserve any existing checklist items or template sections.
- Keep language professional and review‑friendly.
