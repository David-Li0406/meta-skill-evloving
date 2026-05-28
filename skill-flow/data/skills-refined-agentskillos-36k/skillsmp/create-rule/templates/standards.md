# [Language/Framework] Standards

Brief description of what standards this rule enforces.

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | snake_case | `user_count` |
| Functions | snake_case | `get_user()` |
| Classes | PascalCase | `UserService` |
| Constants | UPPER_SNAKE | `MAX_RETRIES` |

## Preferred Patterns

### Pattern 1: [Name]

Explain when to use this pattern.

```language
// Good
example_good_code()

// Bad
example_bad_code()
```

### Pattern 2: [Name]

Explain when to use this pattern.

```language
// Good
example_good_code()

// Bad
example_bad_code()
```

## Error Handling

Describe error handling conventions.

```language
// Preferred approach
try:
    risky_operation()
except SpecificError as e:
    handle_error(e)
```

## Quick Checklist

Before committing, verify:

- [ ] Naming follows conventions
- [ ] Preferred patterns used
- [ ] Error handling is appropriate
- [ ] [Add more items]
