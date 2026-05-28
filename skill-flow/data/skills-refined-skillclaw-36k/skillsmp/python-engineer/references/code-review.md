# Code Review Checklist

## Type Safety

- [ ] All function parameters have type hints
- [ ] All return types are annotated
- [ ] `None` returns use `-> None` explicitly
- [ ] Generic types use proper bounds (`TypeVar`)
- [ ] No `Any` or `object` without justification
- [ ] `mypy --strict` passes

## Code Quality

- [ ] Functions are < 20 lines
- [ ] Single responsibility per function/class
- [ ] No nested functions > 2 levels deep
- [ ] Early returns reduce nesting
- [ ] No magic numbers/strings (use constants)
- [ ] Descriptive variable names (no single letters except loops)

## Error Handling

- [ ] Specific exceptions, not bare `except:`
- [ ] Custom exceptions inherit from appropriate base
- [ ] Error messages are actionable
- [ ] Resources cleaned up (context managers)
- [ ] No silent failures

## Testing

- [ ] Tests exist for public APIs
- [ ] Edge cases covered (empty, None, boundary)
- [ ] Error paths tested
- [ ] Test names describe behavior
- [ ] No hardcoded values to make tests pass
- [ ] Minimal mocking

## Security

- [ ] No hardcoded secrets
- [ ] Input validation at boundaries
- [ ] SQL queries use parameterization
- [ ] User input sanitized
- [ ] Sensitive data not logged

## Performance

- [ ] No N+1 queries
- [ ] Large data uses generators
- [ ] Appropriate data structures
- [ ] No premature optimization (but no obvious issues)

## API Design (FastAPI)

- [ ] Proper HTTP status codes
- [ ] Pydantic models for request/response
- [ ] Dependency injection used
- [ ] Async where beneficial
- [ ] Error responses are consistent

## Common Issues

| Issue | Fix |
|-------|-----|
| `dict` for structured data | Use `dataclass` or Pydantic |
| Multiple return types | Use `Union` or split function |
| Long parameter list | Use config object |
| Boolean parameters | Use enum or separate methods |
| Mutable default args | Use `None` + assignment |
| String concatenation in loops | Use `"".join()` or f-strings |
