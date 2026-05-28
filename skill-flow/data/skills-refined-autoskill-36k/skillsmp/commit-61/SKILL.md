---
name: commit
description: Enforce disciplined, file-by-file Git commits using strict verbs, scoped brackets, and short messages. Use when staging, refactoring, fixing, or cleaning code. Especially useful for refactors, audits, and review-friendly history.
---

# Commit Skill

## Core philosophy

Every commit must:

- Represent one intent
- Touch one file (unless explicitly allowed)
- Use a controlled verb
- Include explicit scope in brackets
- Be short, readable, and reviewable

Commits are documentation, not narration.

---

## Commit message format (MANDATORY)

```
<verb>(<scope>): <short message>
```

### Examples

- `refactor(main): simplify request validation`
- `fix(auth): handle missing token edge case`
- `chore(logging): remove unused formatter`
- `docs(api): clarify pagination params`

---

## Allowed verbs (STRICT SET)

Only use one of the following:

- `refactor` -> structural change, no behavior change
- `fix` -> bug fix
- `feat` -> new user-facing capability
- `chore` -> tooling, cleanup, non-prod logic
- `docs` -> documentation only
- `test` -> tests only
- `perf` -> performance improvement
- `style` -> formatting, lint-only changes

If unsure -> default to `refactor`.

---

## Scope rules (`(<scope>)`)

The scope MUST be one of:

- module name e.g but not strictly (`auth`, `users`, `payments`)
- layer (`api`, `service`, `schema`, `db`)
- branch name (`main`, `dev`)
- file stem (`settings`, `config`, `router`)

Avoid vague scopes:

- `misc`
- `stuff`
- `update`

---

## File-by-file enforcement

### Default rule

One commit = one file

If multiple files are staged:

1. Stop
2. Unstage everything
3. Stage only one file
4. Commit
5. Repeat

Multi-file commits are allowed only if:

- files are inseparable (e.g. interface + impl)
- explicitly requested by the user

---

## Workflow to follow (ALWAYS)

### Step 1: Inspect changes

```bash
git status
git diff
```

### Step 2: Select ONE file

```bash
git add path/to/file.py
```

### Step 3: Propose commit message

Before committing:

- State the verb
- State the scope
- State the intent in <= 8 words

### Step 4: Stage and commit (MANDATORY)

Stage exactly one file and commit it. Do not wait for approval unless the user explicitly asks to review first.

```bash
git add path/to/file.py
git commit -m "refactor(main): extract config loading"
```

### Step 5: Repeat for next file

---

## Refactor-specific rules (IMPORTANT)

When using `refactor`:

- Do NOT claim behavior changes
- Do NOT mention performance unless measured
- Focus on structure, clarity, boundaries

Good:

- `refactor(api): extract request parsing`
Bad:
- `refactor(api): fix bug and improve speed`

---

## How to assist the user (assistant behavior)

When this skill is active:

- NEVER suggest bulk commits by default
- ALWAYS ask or infer which single file is being committed
- ALWAYS generate the commit message before committing
- ALWAYS stage the file and perform the commit without waiting for approval, unless the user requests review
- If message is vague -> rewrite it
- If scope is unclear -> infer from file path

If multiple files are changed:

- Propose one commit per file, sequentially

---

## Anti-patterns to block

Do NOT allow:

- "updated stuff"
- "minor changes"
- "fixes"
- commits without scope
- commits with more than one verb
- commits that mix refactor + fix

If detected -> stop and correct.

---

## Example interaction

User:
I refactored `auth/deps.py`

Assistant:
Suggested commit:
`refactor(auth): isolate dependency resolution`

User:
Commit it

Assistant:

- Ensures only `auth/deps.py` is staged
- Commits with the approved message

---

## Mental model

If this commit appeared alone in a pull request,
would a reviewer immediately understand why it exists from the message?

If not -> rewrite.

---

## Why this is powerful (quick coaching insight)

You are doing three high-leverage things here:

1. Reducing cognitive debt
2. Increasing review velocity
3. Signaling seniority silently
