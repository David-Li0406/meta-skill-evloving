# Examples Pattern Library

> Curated code patterns for common implementation scenarios. Reference these when building PRPs or implementing features.

---

## Purpose

This library contains battle-tested patterns extracted from real projects. Each pattern includes:

- **When to use** - Clear criteria for applicability
- **The pattern** - Actual code you can adapt
- **Common mistakes** - Pitfalls to avoid
- **Validation commands** - How to verify correct implementation
- **Related conventions** - Links to CONVENTIONS.md rules

---

## Pattern Index

| Pattern | Category | Use When |
|---------|----------|----------|
| [API Client](api-client.md) | Integration | Building HTTP clients for external services |
| [Error Handling](error-handling.md) | Resilience | Implementing error boundaries and recovery |
| [Test Fixtures](test-fixtures.md) | Testing | Setting up test data and mocks |
| [Config Loading](config-loading.md) | Infrastructure | Loading and validating configuration |
| [Database Patterns](database-patterns.md) | Data | Common database access patterns |

---

## Quick Reference

### By Problem Type

**"I need to call an external API"**
→ See [API Client](api-client.md) - includes retry logic, circuit breakers, timeouts

**"I need to handle errors gracefully"**
→ See [Error Handling](error-handling.md) - includes error types, recovery, logging

**"I need to set up test data"**
→ See [Test Fixtures](test-fixtures.md) - includes factories, builders, cleanup

**"I need to load configuration"**
→ See [Config Loading](config-loading.md) - includes validation, env vars, secrets

**"I need to query/update the database"**
→ See [Database Patterns](database-patterns.md) - includes transactions, pooling, migrations

---

## By Language

| Language | Patterns Available |
|----------|-------------------|
| TypeScript/JavaScript | All patterns |
| Python | All patterns |
| Go | API Client, Error Handling, Config Loading |
| SQL | Database Patterns |

---

## Using Patterns in PRPs

When generating a PRP, reference applicable patterns in Section 3.5:

```markdown
## 3.5 Relevant Patterns

| Pattern | Application | Customization Needed |
|---------|-------------|---------------------|
| [API Client](examples/api-client.md) | Stripe integration | Add idempotency keys |
| [Error Handling](examples/error-handling.md) | Payment failures | Custom error codes |
```

---

## Contributing New Patterns

When you encounter a reusable pattern during implementation:

1. Check if it already exists here
2. If not, create a new file following the template below
3. Add to this index
4. Reference in the retrospective for tracking

### Pattern Template

```markdown
# Pattern: [Name]

## When to Use This Pattern

[Clear criteria]

## The Pattern

```language
[Code]
```

## Common Mistakes to Avoid

- [Mistake 1]
- [Mistake 2]

## Validation Commands

```bash
[Commands to verify correct implementation]
```

## Related Conventions

- [CONVENTIONS.md reference]

## See Also

- [Related patterns]
```

---

## Pattern Quality Criteria

Every pattern in this library should:

- [ ] Solve a common, recurring problem
- [ ] Be language-agnostic or clearly labeled
- [ ] Include working code (not pseudocode)
- [ ] List at least 2 common mistakes
- [ ] Include validation commands
- [ ] Reference applicable conventions

---

*Library version: 1.0*
*Last updated: 2026-01-19*
*Patterns: 5*
