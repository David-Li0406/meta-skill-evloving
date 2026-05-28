---
name: commit-message-convention
description: Use this skill when you need to generate clear and standardized Git commit messages following the Conventional Commits specification.
---

# Commit Message Generator

This skill generates commit messages that conform to the [Conventional Commits](https://www.conventionalcommits.org/) specification. The focus is on capturing the main changes and expressing them in a standard format.

## When to Use

Use this skill when:
- You need to generate commit messages based on staged changes or pasted diffs.
- You require assistance in selecting the type/scope or writing a clear subject/body/footer.
- The diff is large, and you need to distill the main intent.

Do not use this skill when:
- There is no diff provided, and the user refuses to supply one.
- A non-Conventional Commits format is requested.

## Steps to Generate Commit Messages

### Step 1: Retrieve Staged Diff

Run the following command to get the staged changes:
```bash
GIT_PAGER=cat git diff --staged
```

**Handle Edge Cases:**
- **Empty Output** → Respond: "No staged changes. Please stage files using `git add` or manually paste the diff."
- **Command Failure** → Ask the user to manually paste the staged diff.

### Step 2: Analyze Changes

Identify:
1. **Main Purpose** — What is the core intent of the changes?
2. **Scope of Impact** — Which module/component/file is primarily affected?
3. **Breaking Changes** — Are there any breaking changes to existing APIs or behaviors?

### Step 3: Generate Commit Message

#### Quick Reference

##### Commit Types

| Type    | When to Use                          |
|---------|--------------------------------------|
| `feat`  | A new feature for the user          |
| `fix`   | A bug fix                           |
| `docs`  | Documentation only                  |
| `style` | Formatting changes, no code change  |
| `refactor` | Code changes that neither fix a bug nor add a feature |
| `perf`  | Performance improvements             |
| `test`  | Adding or fixing tests               |
| `build` | Changes to the build system or dependencies |
| `ci`    | Changes to CI/CD configuration       |
| `chore` | Maintenance or tool changes          |
| `revert`| Reverting a previous commit          |

#### Format Rules

```
<type>[(scope)]: <subject>

[body]

[footer]
```

| Element  | Rules |
|----------|-------|
| **Subject** | Imperative mood, ≤72 characters (suggested ≤50), no period at the end |
| **Body**    | Explain *what* and *why* (not *how*), wrap at 72 characters, optional |
| **Footer**  | `BREAKING CHANGE:`, `Fixes #123`, `Refs #456`, optional |

### Step 4: Self-Check

Before outputting, check:
- [ ] Subject ≤72 characters
- [ ] Uses imperative mood ("add" not "added")
- [ ] Type matches the primary change
- [ ] No vague verbs unless essential
- [ ] Breaking changes noted in footer if applicable

## Output Format

**Only output** the commit message in the code block, without Git commands or explanations. If there is no diff, request the staged diff instead of outputting a commit message.

```
<type>[(scope)]: <subject>

[body]

[footer]
```

## Common Mistakes

- Outputting explanations instead of the code block.
- Using vague verbs or past tense.
- Forcing a scope when changes span multiple areas.
- Omitting `BREAKING CHANGE:` for breaking changes.

## Best Practices

1. **Atomic Commits**: Each commit should represent a single logical change.
2. **Frequent Commits**: Commit often, keeping commits small and focused.
3. **Pre-commit Checks**: Review changes with `git diff` and `git status` before committing.

## Example Commit Messages

### New Feature
```
feat(auth): add OAuth login support

Implement OAuth 2.0 authentication flow to allow users to login
with their Google or GitHub accounts.

Closes #234
```

### Bug Fix
```
fix(cart): prevent negative quantities

Add validation to ensure cart item quantities cannot be negative.
This fixes an issue where users could exploit the quantity input
to create negative totals.

Fixes #567
```

### Breaking Change
```
feat(api): migrate to REST API v2

BREAKING CHANGE: API endpoints have been updated to v2.

Changes:
- All endpoints now use /api/v2 prefix
- Response format changed to include metadata
```

## Conclusion

Good commit messages should:
1. Follow a consistent format.
2. Clearly describe the changes made.
3. Explain the reasons for the changes.
4. Be concise and easy to understand.
5. Facilitate tracking and rollback of changes.