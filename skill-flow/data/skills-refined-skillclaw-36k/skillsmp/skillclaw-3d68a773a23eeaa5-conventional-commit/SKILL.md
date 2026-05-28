---
name: conventional-commit
description: Use this skill when committing code changes to generate standardized git commit messages following the Conventional Commits 1.0.0 specification.
---

# Conventional Commit Generator

Generate commit messages following [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

## Workflow

1. Run `git status` and `git diff HEAD` to analyze changes.
2. Stage files: user-specified only, or `git add -A` for all.
3. Determine type and scope from changes.
4. Generate commit message incorporating user hints.
5. Commit using HEREDOC format to preserve formatting:

   ```bash
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <description>

   <body>

   <footer>
   EOF
   )"
   ```

6. Output: `<hash> <subject>`

## Scope Boundaries

**DO:** Analyze git changes, generate messages, stage files, commit.

**DO NOT:** Modify code, push (unless asked), create branches, amend without request.

## Commit Format

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

## Type Selection

| Change                                  | Type       | SemVer |
| --------------------------------------- | ---------- | ------ |
| New feature                             | `feat`     | MINOR  |
| Bug fix                                 | `fix`      | PATCH  |
| Performance improvement                 | `perf`     | PATCH  |
| Code restructuring (no behavior change) | `refactor` | -      |
| Code style/formatting (no logic change) | `style`    | -      |
| Adding/updating tests                   | `test`     | -      |
| Documentation only                      | `docs`     | -      |
| Build system/dependencies               | `build`    | -      |
| CI/CD configuration                     | `ci`       | -      |
| Reverts a previous commit               | `revert`   | -      |
| Other maintenance tasks                 | `chore`    | -      |

> **Note:** Only `feat` and `fix` have SemVer implications. Breaking changes (any type with exclamation mark or `BREAKING CHANGE` footer) trigger MAJOR.

## Subject Line

- **Max length:** 72 characters (50 recommended for readability).
- **Format:** `type(scope): description` or `type: description`.
- **Mood:** Imperative present tense ("add" not "added" or "adds").
- **Case:** Lowercase first letter.
- **Punctuation:** No trailing period.

## Scope

Scope provides context for the change and can be omitted if not applicable.