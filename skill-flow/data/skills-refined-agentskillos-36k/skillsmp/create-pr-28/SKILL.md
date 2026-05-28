---
name: create-pr
description: Creates or updates a GitHub PR with Jira integration, mermaid diagrams, and AI disclosure. Runs pre-push checks first. Use when ready to submit code for review or update an existing PR. Invoke with /create-pr.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - mcp__atlassian__getJiraIssue
---

# Creating Pull Request

Creates a well-structured PR using the project's template, with Jira integration and visual diagrams.

## Workflow

### 1. Get Branch & Detect Ticket

```bash
git branch --show-current
```

Extract ticket ID from branch (e.g., `feat/TDE-7358-optimize-elevar` → `TDE-7358`).

### 2. Check for Existing PR

```bash
gh pr view --json number,title,body,url 2>/dev/null
```

- If PR exists: will update it
- If no PR: will create new one

### 3. Run Pre-Push Checks

```bash
npm run pre-push
```

If checks fail, stop and report errors. Do not create/update PR with failing checks.

### 4. Fetch Jira Ticket Details

```
mcp__atlassian__getJiraIssue
- cloudId: vuoriclothing.atlassian.net
- issueIdOrKey: <ticket-id>
```

Extract: `fields.summary`, `fields.description`, `fields.issuetype.name`

### 5. Analyze Changes

```bash
git diff main...HEAD --stat
git diff main...HEAD --name-only
git log main...HEAD --oneline
```

Read key changed files to understand what was modified and how components interact.

### 6. Generate PR Content

See [template.md](template.md) for the full PR template.

**Title format:** `<type>: [TICKET-ID] <short description>`

Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`

### 7. Create or Update PR

**New PR:**
```bash
git push -u origin <branch-name>
gh pr create --base main --title "<title>" --body "<body>"
```

**Existing PR:**
```bash
git push
gh pr edit --title "<title>" --body "<body>"
```

### 8. Report Result

Output: PR URL, summary of changes, items needing manual attention.

## Mermaid Diagrams

See [diagrams.md](diagrams.md) for diagram examples and guidelines.

- Use diagrams that accurately represent changes
- Match complexity to PR scope
- Include all affected services for integration changes

## Notes

- Always push changes before creating/updating PR
- If pre-push fails, fix issues first
- Default base branch is `main`
- Do NOT add AI attribution footers to PR description
