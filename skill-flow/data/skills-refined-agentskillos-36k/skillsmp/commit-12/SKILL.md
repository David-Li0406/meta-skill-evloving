---
name: commit
description: Creates logical git commits from working tree changes. Use when finishing work, saving progress, or organizing changes into commits.
---

# Commit

Create one or more logical commits from staged/unstaged changes.

## Workflow

- [ ] Review changes in working tree
- [ ] Group related changes into logical units
- [ ] Create commits with well-crafted messages
- [ ] Verify commit history

## Step 1: Review Changes

```bash
git status
git diff --stat
git diff  # detailed view if needed
```

## Step 2: Group Logical Changes

Split unrelated changes into separate commits.
Each commit should be **atomic**—one logical change that can be understood, reviewed, and reverted independently.
When in doubt, ask.

**Good groupings:**
- All changes for a single bug fix
- All changes for a single feature
- Refactoring separate from behavior changes
- Test additions separate from implementation

**Signs you need multiple commits:**
- Changes touch unrelated subsystems
- Commit message needs "and" to describe changes
- Some changes are refactoring, others are features

## Step 3: Stage and Commit

For each logical unit:

```bash
git add <files>           # or git add -p for partial staging
git commit -m "Subject line here"
```

For commits needing a body:
```bash
git commit  # opens editor
```

## How to Write a Git Commit Message

1. **Separate subject from body with a blank line**
2. **Limit subject line to ~50 characters** (72 max)
3. **Capitalize the subject line**
4. **Do not end the subject line with a period**
5. **Use imperative mood** ("Add feature" not "Added feature")
7. **Use body to explain *what* and *why*, not *how***

### The Imperative Test

A good subject line completes this sentence:
> If applied, this commit will **_your subject line_**

✅ Good:
- "Refactor authentication for readability"
- "Fix null pointer in user validation"
- "Add caching to database queries"

❌ Bad:
- "Fixed bug" (past tense, vague)
- "Fixing the thing" (present participle)
- "More changes" (meaningless)

### When to Add a Body

Add a body when context isn't obvious from the diff:
- Explain *why* the change was made
- Note side effects or non-obvious consequences
- Reference related issues or discussions

```
Add rate limiting to API endpoints

The service was vulnerable to abuse from automated clients
making excessive requests. This adds a token bucket algorithm
limiting clients to 100 requests per minute.

Resolves: #423
```

### Simple Changes

Single-line messages are fine for simple changes:
```bash
git commit -m "Fix typo in README"
git commit -m "Remove unused import"
```

## Step 4: Verify

```bash
git log --oneline -5
```

Check that:
- Each commit is a logical unit
- Subject lines are clear and imperative
- History tells a coherent story

## Quick Reference

| Rule | Example |
|------|---------|
| Imperative mood | "Add" not "Added" or "Adds" |
| 50 char subject | Keep it concise |
| Capitalize | "Fix bug" not "fix bug" |
| No trailing period | "Fix bug" not "Fix bug." |
| Blank line before body | Required if body present |
| 72 char body wrap | For readability |
