# Conventional Commits Reference

## Commit Types

### `feat` - Features
New functionality visible to the user.

**Use when:**
- Adding a new API endpoint
- Implementing a new UI component
- Adding a new CLI command
- Introducing new business logic

**Examples:**
- `feat(api): add user profile endpoint`
- `feat(ui): add dark mode toggle`
- `feat: implement email notifications`

### `fix` - Bug Fixes
Fixes a bug in existing functionality.

**Use when:**
- Correcting incorrect behavior
- Fixing crashes or errors
- Resolving edge cases
- Patching security vulnerabilities

**Examples:**
- `fix(auth): resolve token expiration race condition`
- `fix(db): handle null values in user query`
- `fix: prevent crash on empty input`

### `docs` - Documentation
Changes to documentation only.

**Use when:**
- Updating README
- Adding/modifying code comments (when comments are the change itself)
- Updating API documentation
- Adding examples or guides

**Examples:**
- `docs: update installation instructions`
- `docs(api): add authentication examples`
- `docs: fix typo in contributing guide`

### `style` - Code Style
Changes that don't affect code meaning.

**Use when:**
- Formatting changes
- Adding/removing whitespace
- Fixing linting errors
- Changing quotes style

**Examples:**
- `style: format with black`
- `style: fix eslint warnings`
- `style(components): consistent indentation`

### `refactor` - Refactoring
Code changes that neither fix bugs nor add features.

**Use when:**
- Restructuring code without changing behavior
- Renaming variables/functions
- Extracting functions or classes
- Moving files
- Simplifying complex code

**Examples:**
- `refactor(auth): extract validation logic`
- `refactor: rename UserManager to UserService`
- `refactor(db): use connection pooling`

### `perf` - Performance
Changes that improve performance.

**Use when:**
- Optimizing algorithms
- Reducing memory usage
- Improving query performance
- Caching implementation

**Examples:**
- `perf(db): add index for user lookups`
- `perf: cache expensive computation`
- `perf(api): batch database queries`

### `test` - Tests
Adding or modifying tests.

**Use when:**
- Adding new test cases
- Fixing broken tests
- Improving test coverage
- Refactoring test code

**Examples:**
- `test(auth): add OAuth flow tests`
- `test: increase coverage for utils`
- `test(api): fix flaky integration test`

### `build` - Build System
Changes to build system or dependencies.

**Use when:**
- Updating dependencies
- Modifying build scripts
- Changing build configuration
- Adding/removing packages

**Examples:**
- `build: upgrade to Python 3.12`
- `build(deps): update fastapi to 0.100`
- `build: add docker multi-stage build`

### `ci` - Continuous Integration
Changes to CI configuration.

**Use when:**
- Modifying GitHub Actions
- Updating CI scripts
- Changing deployment pipelines
- Adding new CI jobs

**Examples:**
- `ci: add automated testing workflow`
- `ci(deploy): add staging environment`
- `ci: fix failing linter job`

### `chore` - Chores
Other changes that don't modify src or test.

**Use when:**
- Updating .gitignore
- Modifying editor config
- Housekeeping tasks
- Release preparation

**Examples:**
- `chore: update .gitignore`
- `chore: configure pre-commit hooks`
- `chore(release): bump version to 2.0.0`

### `revert` - Reverts
Reverts a previous commit.

**Format:**
```
revert: <original commit message>

This reverts commit <hash>.
<optional reason>
```

**Examples:**
- `revert: feat(api): add user profile endpoint`

## Scope Guidelines

Scope should be a noun describing the section of codebase.

### Common Scopes by Project Area

| Area | Suggested Scopes |
|------|------------------|
| Backend | `api`, `db`, `auth`, `core`, `models`, `services` |
| Frontend | `ui`, `components`, `hooks`, `store`, `pages` |
| Infrastructure | `docker`, `k8s`, `terraform`, `ci` |
| Agents | `faq-agent`, `tools`, `prompts` |

### Scope Rules

1. Lowercase only
2. Single word preferred
3. Use hyphens for multi-word: `faq-agent`
4. Be consistent within project
5. Omit scope for cross-cutting changes

## Breaking Changes

Mark breaking changes with "!" or footer.

### When to Mark Breaking

- Removing public API endpoints
- Changing function signatures
- Modifying data structures
- Removing configuration options
- Changing default behavior

### Format Options

**With "!":**
```
feat(api)!: change response format to JSON:API
```

**With footer:**
```
feat(api): change response format to JSON:API

BREAKING CHANGE: Response structure now follows JSON:API spec.
Clients must update their parsers.
```

## Validation Checklist

Before committing, verify:

- [ ] Type is appropriate for the change
- [ ] Scope matches affected area (if used)
- [ ] Description is clear and concise
- [ ] First line under 72 characters
- [ ] Uses imperative mood ("add" not "added")
- [ ] No period at end of first line
- [ ] Breaking changes are marked
- [ ] Commit is atomic (one logical change)
