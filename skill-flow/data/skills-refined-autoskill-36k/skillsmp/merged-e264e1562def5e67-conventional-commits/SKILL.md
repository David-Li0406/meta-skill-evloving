---
name: conventional-commits
description: Use this skill to format Git commit messages according to the Conventional Commits specification, ensuring consistency and supporting automated changelog generation.
---

# Conventional Commits

Format all commit messages according to the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This enables automated changelog generation, semantic versioning, and better commit history.

## Message Structure

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Commit Types

| Type             | Purpose                                   | SemVer |
|------------------|-------------------------------------------|--------|
| `feat`           | A new feature                             | MINOR  |
| `fix`            | A bug fix                                 | PATCH  |
| `docs`           | Documentation only changes                | -      |
| `style`          | Changes that do not affect the meaning of the code | -      |
| `refactor`       | A code change that neither fixes a bug nor adds a feature | -      |
| `perf`          | A code change that improves performance    | -      |
| `test`           | Adding missing tests or correcting existing tests | -      |
| `build`          | Changes to the build process or auxiliary tools | -      |
| `ci`             | CI/CD configuration                       | -      |
| `chore`          | Changes that don't modify src or test files | -      |
| `revert`         | Reverts a previous commit                 | -      |

## Guidelines

1. **Subject Line**: Keep it concise (under 50 characters), use imperative mood, and do not end with a period.
2. **Description**: Must immediately follow the colon and space after the type/scope. Use imperative mood and keep it clear.
3. **Body**: Optional longer description providing additional context, explaining the "what" and "why" of the change, not the "how". Wrap at 72 characters.
4. **Footers**: Use for referencing issues or indicating breaking changes. Use `BREAKING CHANGE:` for significant changes.

## Breaking Changes

Indicate breaking changes using either method:

1. Using `!` in the type/scope:
   ```
   feat!: send an email to the customer when a product is shipped
   ```

2. Using `BREAKING CHANGE` footer:
   ```
   feat: allow provided config object to extend other configs

   BREAKING CHANGE: `extends` key in config file is now used for extending other config files
   ```

## Examples

### Simple Feature
```
feat: add user authentication
```

### Feature with Scope
```
feat(auth): add OAuth2 support
```

### Bug Fix with Body
```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.
```

### Breaking Change
```
feat!: migrate to new API client

BREAKING CHANGE: The API client interface has changed. All methods now
return Promises instead of using callbacks.
```

### Documentation Update
```
docs: correct spelling of CHANGELOG
```

## Quality Checks

Before committing, verify:

- [ ] Message accurately describes the changes
- [ ] Type correctly categorizes the change
- [ ] Scope (if used) is meaningful and consistent
- [ ] Breaking changes are properly marked with `!` or footer
- [ ] Description is clear and under 50 characters
- [ ] Body wraps at 72 characters (if present)

## When to Use

Use this format for:
- All git commits
- Commit message generation
- Pull request merge commits
- When the user asks about commit messages or git commits

## Common Mistakes to Avoid

❌ `Added new feature` (past tense, capitalized)  
✅ `feat: add new feature` (imperative, lowercase)

❌ `fix: bug` (too vague)  
✅ `fix: resolve null pointer exception in user service`

❌ `feat: add feature` (redundant)  
✅ `feat: add user profile page`

❌ `feat: Added OAuth support.` (past tense, period)  
✅ `feat: add OAuth support`