# Code Review Checklist

Generic review checklist applicable to any language. For language-specific checks, reference `code-implement` resources.

---

## Correctness

- [ ] Logic matches stated requirements
- [ ] Edge cases handled (null, empty, boundary conditions)
- [ ] Error handling present and appropriate
- [ ] Type safety maintained
- [ ] No off-by-one errors

## Style

- [ ] Consistent naming conventions
- [ ] Code is readable without excessive comments
- [ ] No commented-out code
- [ ] Appropriate abstraction level
- [ ] Follows project conventions

## Performance

- [ ] No unnecessary computations
- [ ] Appropriate data structures used
- [ ] No N+1 query patterns
- [ ] Resource cleanup handled (files, connections)

## Security

- [ ] No hardcoded secrets or credentials
- [ ] Input validation at boundaries
- [ ] No injection vulnerabilities (SQL, command, etc.)
- [ ] Safe handling of user-provided paths

## Architecture

- [ ] Single responsibility principle
- [ ] Appropriate coupling between components
- [ ] Clear interfaces and contracts
- [ ] No circular dependencies

## Testing (if applicable)

- [ ] Tests cover the change
- [ ] Edge cases tested
- [ ] Tests are readable and maintainable

---

## Severity Quick Reference

| Severity | Examples |
|----------|----------|
| **Critical** | Security vulnerability, data loss, crash |
| **High** | Logic error, missing validation, unclear behavior |
| **Medium** | Style issue, minor inefficiency, missing docs |
