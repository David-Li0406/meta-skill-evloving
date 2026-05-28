---
name: dqx-conventional-commit
description: Create conventional commit following DQX standards
compatibility: opencode
metadata:
  workflow: version-control
  audience: all-agents
---

## What I do

Guide you through creating a properly formatted conventional commit that passes DQX's commitizen validation.

---

## Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Required Parts

**Type** (required): Category of change
**Scope** (optional): Area of codebase affected
**Subject** (required): Brief description (max 72 characters)

### Optional Parts

**Body**: Detailed explanation (why, not what)
**Footer**: Issue references, breaking changes

---

## Commit Types

Choose the type that best describes your change:

| Type | When to Use | Example |
|------|-------------|---------|
| **feat** | New feature | `feat(cache): add LRU cache with TTL support` |
| **fix** | Bug fix | `fix(evaluator): resolve type inference issue` |
| **docs** | Documentation only | `docs(api): update MetricProvider examples` |
| **test** | Adding/updating tests | `test(parser): add coverage for edge cases` |
| **refactor** | Code changes (no bugs/features) | `refactor(graph): simplify traversal algorithm` |
| **perf** | Performance improvements | `perf(analyzer): optimize SQL generation` |
| **style** | Formatting changes only | `style(api): fix line length violations` |
| **build** | Build system/dependencies | `build(deps): upgrade pyarrow to 15.0.0` |
| **ci** | CI configuration | `ci(GitHub): add coverage reporting` |
| **chore** | Maintenance tasks | `chore(cleanup): remove deprecated code` |
| **revert** | Revert previous commit | `revert: feat(cache): add LRU cache` |

---

## DQX-Specific Scopes

Use these scopes for DQX modules:

**Core modules**:
- `analyzer` - SQL analysis engine
- `api` - User-facing API
- `graph` - Graph processing
- `evaluator` - Expression evaluation
- `provider` - Metric provider
- `specs` - Assertion specifications
- `validator` - Validation logic

**Supporting modules**:
- `display` - Terminal UI with Rich
- `orm` - Object-relational mapping
- `extensions` - Extensions system
- `common` - Shared utilities
- `dialect` - SQL dialects (DuckDB, BigQuery, Snowflake)
- `functions` - Built-in functions
- `models` - Data models
- `ops` - Operations
- `states` - State management
- `utils` - Utility functions
- `dql` - Data Quality Language parser

**Infrastructure**:
- `deps` - Dependencies
- `config` - Configuration
- `docs` - Documentation
- `tests` - Testing infrastructure
- `ci` - CI/CD
- `agents` - AI agent configuration
- `skills` - OpenCode skills

---

## Subject Line Rules

✅ **Do**:
- Use imperative mood ("add" not "added")
- Start with lowercase
- No period at the end
- Max 72 characters
- Be specific and descriptive

❌ **Don't**:
- Use past tense ("added", "fixed")
- Start with capital letter
- End with period
- Be vague ("update code", "fix bug")

### Examples

✅ Good:
```
feat(cache): add LRU cache with TTL support
fix(parser): handle empty input strings
docs(api): clarify MetricProvider usage
test(graph): add traversal edge cases
```

❌ Bad:
```
feat(cache): Added cache.  # Past tense, capital, period
fix: fixed a bug  # No scope, vague, past tense
Update documentation  # No type, capital, vague
feat(cache): Implement new caching system for metrics.  # Capital, period, too long
```

---

## Body Guidelines

**When to add body**:
- Complex changes need explanation
- Non-obvious reasons for change
- Breaking changes
- Multiple related changes

**Format**:
- Separate from subject with blank line
- Wrap at 72 characters
- Explain **why**, not **what**
- Use bullet points for multiple items

**Example**:
```
feat(analyzer): add query optimization for large datasets

Improve performance for queries with >1M rows by:
- Implementing query result caching
- Adding early termination for LIMIT queries
- Optimizing JOIN operations

Benchmarks show 3x speedup on typical workloads.
```

---

## Footer Guidelines

**Issue references**:
```
Closes #123
Fixes #456
Resolves #789
Refs #101
```

**Breaking changes**:
```
BREAKING CHANGE: remove deprecated `check_all()` method

Use `run_all()` instead. Migration:
- Old: suite.check_all()
- New: suite.run_all()
```

---

## Complete Examples

### Simple feature
```
feat(cache): add LRU cache with TTL support
```

### Bug fix with context
```
fix(evaluator): resolve type inference for nested expressions

The type inference was failing for expressions with more than
two levels of nesting due to incorrect visitor traversal order.

Fixes #234
```

### Breaking change
```
feat(api): redesign MetricProvider constructor

Simplify API by accepting config dict instead of individual params.

BREAKING CHANGE: MetricProvider constructor signature changed

Old:
  provider = MetricProvider(host, port, db, user, password)

New:
  provider = MetricProvider(config={
      "host": host,
      "port": port,
      "database": db,
      "credentials": {"user": user, "password": password}
  })

Migration guide: docs/migration-v2.md

Closes #456
```

### Multiple related changes
```
refactor(graph): improve visitor pattern implementation

- Extract base visitor class for reusability
- Add type hints for all visitor methods
- Simplify traversal logic with generator pattern
- Add comprehensive docstrings

This refactoring improves code maintainability and makes it
easier to implement custom visitors for new use cases.
```

---

## Validation

Your commit message is validated by commitizen hook during pre-commit:
```bash
uv run pre-commit run --all-files
```

**Common validation errors**:

❌ `subject must start with lowercase`:
- Fix: Change first letter to lowercase

❌ `subject is too long (>72 chars)`:
- Fix: Shorten subject, move details to body

❌ `type must be one of [feat, fix, docs, ...]`:
- Fix: Use valid type from list above

❌ `subject must not end with period`:
- Fix: Remove trailing period

---

## When to use me

Use this skill when:
- **Committing code** after each implementation phase
- **Addressing feedback** with fix commits
- **Unsure about format** for your change type
- **Commit rejected** by pre-commit hook

---

## Quick Decision Tree

**Adding new functionality?** → `feat(scope):`
**Fixing a bug?** → `fix(scope):`
**Updating documentation?** → `docs(scope):`
**Adding/updating tests?** → `test(scope):`
**Refactoring code?** → `refactor(scope):`
**Improving performance?** → `perf(scope):`
**Formatting only?** → `style(scope):`
**Dependencies/build?** → `build(deps):`
**Maintenance?** → `chore(scope):`

---

## Reference

Complete details: **AGENTS.md §commit-conventions**

Commitizen validation runs automatically during pre-commit hooks.
