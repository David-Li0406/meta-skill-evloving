# Conventional Commits Reference

## Types

| Type | Description | Example |
|------|-------------|---------|
| **feat** | New feature for the user | `feat(auth): add OAuth2 login` |
| **fix** | Bug fix for the user | `fix(api): handle null response` |
| **docs** | Documentation only changes | `docs(readme): update install guide` |
| **style** | Formatting, whitespace, semicolons (no code change) | `style(lint): fix indentation` |
| **refactor** | Code change that neither fixes bug nor adds feature | `refactor(core): simplify data flow` |
| **perf** | Performance improvement | `perf(queries): add database index` |
| **test** | Adding or updating tests | `test(auth): add login unit tests` |
| **build** | Build system or external dependencies | `build(deps): upgrade to Node 20` |
| **ci** | CI configuration and scripts | `ci(actions): add deploy workflow` |
| **chore** | Maintenance tasks | `chore(deps): update dependencies` |
| **revert** | Revert a previous commit | `revert: feat(auth): add OAuth2` |

## Scope Guidelines

The scope should identify the area of the codebase affected:

- **Module/package name**: `auth`, `api`, `utils`, `config`
- **Feature area**: `login`, `checkout`, `dashboard`
- **Layer**: `db`, `routes`, `middleware`, `ui`
- **Plugin name** (for monorepos): `git`, `kit`, `para-obsidian`

Scope is optional but recommended for clarity.

## Subject Rules

1. **Imperative mood**: "add" not "added", "fix" not "fixed"
2. **Lowercase**: Start with lowercase letter
3. **No period**: Don't end with a period
4. **Max 100 chars**: Keep the header line short
5. **What, not how**: Describe the change, not implementation

## Body (Optional)

Use the body to explain:
- **What** changed and **why** (not how)
- Breaking changes
- Migration instructions
- Related issues

Separate from subject with a blank line.

## Footer (Optional)

- `BREAKING CHANGE:` for breaking changes
- `Fixes #123` or `Closes #123` for issue references
- `Co-Authored-By:` for pair programming

## Breaking Changes

Indicate breaking changes with:
1. `!` after type/scope: `feat(api)!: change response format`
2. `BREAKING CHANGE:` in footer

```
feat(api)!: change response format

BREAKING CHANGE: Response now returns array instead of object.
Migration: Update client code to handle array response.
```
