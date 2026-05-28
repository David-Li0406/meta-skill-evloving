---
name: semantic-commits
description: Guide to writing standard, parseable commit messages (Conventional Commits).
---
# Semantic Commits Skill

## 1. The Philosophy
We use **Conventional Commits** to generate changelogs and determine SemVer bumps automatically. A commit message has three parts:
`type(scope): description`

## 2. Commit Types
Choose the correct type based on your change:

| Type | Meaning | SemVer Impact |
| :--- | :--- | :--- |
| **`feat`** | A new feature | **MINOR** |
| **`fix`** | A bug fix | **PATCH** |
| **`docs`** | Documentation only | PATCH |
| **`style`** | Formatting (white-space, etc) | PATCH |
| **`refactor`** | Code change that neither fixes a bug nor adds a feature | PATCH |
| **`perf`** | Code change that improves performance | PATCH |
| **`test`** | Adding missing tests or correcting existing tests | PATCH |
| **`chore`** | Build process, aux tools, dependency updates | PATCH |

## 3. Formatting Rules
1.  **Scope (Optional):** The component being changed (e.g., `auth`, `orders`, `cli`).
2.  **Description:** concise, imperative mood ("add" not "added").
3.  **Body (Optional):** Context, motivation, and references (breaking changes go here).

## 4. Examples

**Feature:**
```text
feat(billing): add stripe webhook handler
```

**Bug Fix:**
```text
fix(validation): allow international phone numbers
```

**Breaking Change:**
```text
feat(api): remove legacy search endpoint

BREAKING CHANGE: The /api/search endpoint has been removed. Use /api/v2/search instead.
```
