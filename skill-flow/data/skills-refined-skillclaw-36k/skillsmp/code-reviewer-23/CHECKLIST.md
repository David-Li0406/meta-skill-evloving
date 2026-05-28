# Code Review Checklist

Use this checklist when performing code reviews.

## Quality

- [ ] Variable and function names are descriptive and consistent
- [ ] Functions are focused (single responsibility)
- [ ] No duplicated code (DRY principle)
- [ ] Comments explain "why", not "what"
- [ ] No dead code or commented-out code
- [ ] Magic numbers are extracted to named constants
- [ ] Error messages are helpful and actionable
- [ ] Logging is appropriate (not too verbose, not missing critical info)

## Error Handling

- [ ] All promises have error handling (.catch or try/catch)
- [ ] Errors are handled at the appropriate level
- [ ] User-facing errors are friendly, developer errors are detailed
- [ ] Null/undefined cases are handled
- [ ] Edge cases are considered (empty arrays, zero values, etc.)

## Architecture

- [ ] Dependencies flow in one direction (no circular deps)
- [ ] Components/modules have clear boundaries
- [ ] Interfaces/contracts are well-defined
- [ ] Coupling is minimal between modules
- [ ] Changes don't require modifications to unrelated code
- [ ] Design patterns are used consistently

## Performance

- [ ] No unnecessary re-renders (React: memo, useMemo, useCallback used appropriately)
- [ ] Heavy computations are memoized or debounced
- [ ] Network requests are batched where possible
- [ ] Resources are cleaned up (intervals, subscriptions, event listeners)
- [ ] Images and assets are optimized and lazy-loaded
- [ ] No N+1 query patterns

## Security

- [ ] User input is validated and sanitized
- [ ] No sensitive data in logs or error messages
- [ ] Authentication/authorization checks are in place
- [ ] No SQL injection, XSS, or command injection vulnerabilities
- [ ] Secrets are not hardcoded

## Testing

- [ ] New code has appropriate test coverage
- [ ] Tests are meaningful (not just for coverage)
- [ ] Edge cases are tested
- [ ] Tests are independent and deterministic
- [ ] Mocks/stubs are appropriate and not excessive

## Documentation

- [ ] Public APIs have JSDoc/docstrings
- [ ] Complex logic has explanatory comments
- [ ] README updated if behavior changes
- [ ] Breaking changes are documented
