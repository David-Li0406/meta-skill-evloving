---
name: commit-message-generator
description: Use this skill when you need to generate Conventional Commits formatted commit messages based on staged changes or pasted diffs.
---

# Skill body

## Overview

This skill generates commit messages that adhere to the [Conventional Commits](https://www.conventionalcommits.org/) specification. It focuses on capturing the main changes and expressing them in a standard format.

## When to Use

### Use Cases:
- When you need to generate commit messages based on staged changes or pasted diffs.
- When you require assistance in selecting the type/scope or writing a clear subject/body/footer.
- When the diff is large and you need to distill the main intent.

### Avoid Scenarios:
- When there is no diff and the user refuses to provide one.
- When a non-Conventional Commits format is requested.

## Steps to Generate Commit Message

### Step 1: Retrieve Staged Diff

Run the following command:
```bash
GIT_PAGER=cat git diff --staged
```

**Handle Edge Cases:**
- **Empty Output** → Respond: "No staged changes. Please stage files using `git add` or manually paste the diff."
- **Command Failure** → Ask the user to manually paste the staged diff.

### Step 2: Analyze Changes

Identify:
1. **Main Purpose** — What is the core intent of the changes?
2. **Affected Scope** — Which module/component/file is primarily affected?
3. **Breaking Changes** — Are there any breaking changes to the existing API or behavior?

#### Handling Large Diffs (>300 lines)
1. Summarize changes by file/module.
2. Focus on the main purpose.
3. If changes should be split → Suggest: "Consider splitting into multiple commits: [list]"

### Step 3: Generate Commit Message

#### Quick Reference

##### Commit Types

| Type   | When to Use                          |
|--------|--------------------------------------|
| `feat` | A new feature for the user          |
| `fix`  | A bug fix                            |
| `docs` | Documentation only                   |
| `style`| Changes that do not affect code logic|
| `refactor` | Code changes that neither fix a bug nor add a feature |
| `perf` | Performance improvements             |
| `test` | Adding or fixing tests               |
| `build`| Changes to the build system or dependencies |
| `ci`   | CI/CD configuration changes          |
| `chore`| Maintenance or tool changes          |
| `revert`| Reverting a previous commit         |

##### Format Rules

```
<type>[(scope)]: <subject>

[body]

[footer]
```

| Element | Rules |
|---------|-------|
| **Subject** | Imperative mood, ≤72 characters (suggested ≤50), no period at the end |
| **Body** | Explain *what* and *why* (not *how*), wrap at 72 characters, optional |
| **Footer** | `BREAKING CHANGE:`, `Fixes #123`, `Refs #456`, optional |

### Choosing Scope

Scope should be a **noun** describing the affected area:
- Module name: `auth`, `api`, `db`
- Component: `button`, `header`, `modal`
- Feature: `login`, `payment`, `notifications`

If the change is too broad or spans multiple areas, skip the scope.

### Avoid

- ❌ Vague verbs: `update`, `change`, `modify` (unless unavoidable)
- ❌ Past tense: `added`, `fixed` → use `add`, `fix`
- ❌ Starting with articles: `Add a feature` → `Add feature`

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

## Excuses vs Facts

| Excuse | Fact |
|--------|------|
| “No staged changes, just guess” | No diff means no evidence. Request staged diff or pasted changes. |
| “Wording is casual” | Conventional Commits format affects tools and changelogs. |
| “Scope must be included” | Skip scope for broad changes. |

## Red Flags - Stop Immediately

- No staged diff or pasted changes provided.
- Output includes explanations instead of the code block.
- Subject is in past tense or ends with a period.

## Example

```
fix(checkout): prevent duplicate order submission

Race condition allowed double submissions.
```