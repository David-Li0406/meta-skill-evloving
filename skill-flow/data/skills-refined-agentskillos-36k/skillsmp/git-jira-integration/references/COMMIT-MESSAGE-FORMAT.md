# Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/) specification for consistent, machine-readable commit messages.

## Format

```
<type>(<scope>)?: <description>

[optional body]

[optional footer(s)]
```

## Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat: add login page` |
| `fix` | Bug fix | `fix: resolve null pointer` |
| `docs` | Documentation | `docs: update API docs` |
| `style` | Formatting (no code change) | `style: fix indentation` |
| `refactor` | Code restructuring | `refactor: extract auth module` |
| `perf` | Performance improvement | `perf: optimize query` |
| `test` | Add/fix tests | `test: add unit tests` |
| `build` | Build system changes | `build: update webpack config` |
| `ci` | CI configuration | `ci: add GitHub Actions` |
| `chore` | Maintenance | `chore: update dependencies` |
| `revert` | Revert commit | `revert: revert "feat: add X"` |

## Scope (Optional)

Indicates the area of codebase affected:

```
feat(auth): add OAuth support
fix(api): handle timeout errors
docs(readme): add installation steps
```

## Breaking Changes

Mark breaking changes with `!` after type/scope:

```
feat!: remove deprecated API
feat(auth)!: change token format
```

Or use footer:

```
feat: update authentication

BREAKING CHANGE: JWT tokens now required
```

## Issue References

Include Jira issue keys in commit message:

### In Subject
```
feat: add login feature (PROJ-123)
```

### In Footer
```
feat: add login feature

Implements login with OAuth 2.0

Refs: PROJ-123
```

### Multiple Issues
```
feat: update authentication

Refs: PROJ-123, PROJ-124
Closes: PROJ-125
```

## Subject Line Rules

1. Use imperative mood: "add" not "added" or "adds"
2. Don't capitalize first letter (after type)
3. No period at the end
4. Keep under 72 characters
5. Be specific and descriptive

### Good Examples
```
feat: add user authentication with JWT
fix: resolve race condition in data fetching
docs: add API endpoint documentation
```

### Bad Examples
```
feat: Added stuff          # Past tense, vague
fix: Fixed bug.           # Period at end
FEAT: ADD FEATURE         # Uppercase
```

## Body (Optional)

Use body for:
- Explaining motivation for change
- Contrasting with previous behavior
- Technical details

Wrap at 100 characters per line.

```
fix: resolve memory leak in event handler

The event handler was not properly cleaned up when
component unmounted, causing memory accumulation over
time.

Solution: Add cleanup in useEffect return function.
```

## Footer (Optional)

Use for:
- Issue references: `Refs: PROJ-123`
- Breaking changes: `BREAKING CHANGE: ...`
- Co-authors: `Co-authored-by: Name <email>`

```
feat: implement dark mode

Add support for system-wide dark mode preference
with manual override option.

Refs: PROJ-123
Co-authored-by: Alice <alice@example.com>
```

## Validation

Use `devflow_git_validate_commit` to check:

```
devflow_git_validate_commit(
  message: "feat(auth): add OAuth support\n\nRefs: PROJ-123",
  projectKey: "PROJ",
  requireIssueKey: true
)
```

Returns validation status with:
- Parsed type, scope, description
- Found issue keys
- Validation issues and suggestions
