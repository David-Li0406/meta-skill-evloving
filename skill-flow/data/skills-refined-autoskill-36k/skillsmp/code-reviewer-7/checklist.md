# Code Review Checklist

Detailed checklist for thorough code reviews.

## Correctness

### Logic
- [ ] Code implements the intended functionality
- [ ] All code paths are reachable and tested
- [ ] Loop termination conditions are correct
- [ ] Boundary conditions handled (empty arrays, null values, zero)
- [ ] Off-by-one errors checked

### Error Handling
- [ ] All potential errors are caught or propagated
- [ ] Error messages are descriptive and actionable
- [ ] Resources are cleaned up on error (finally blocks, defer)
- [ ] Async errors are properly awaited/caught
- [ ] Network/IO failures handled gracefully

### Data Handling
- [ ] Input validation on all external data
- [ ] Type conversions are safe
- [ ] Null/undefined checks where needed
- [ ] Data mutations are intentional
- [ ] Immutability preserved where expected

## Security

### Input Validation
- [ ] User input is validated before use
- [ ] SQL queries use parameterized statements
- [ ] File paths are sanitized
- [ ] URLs are validated before fetch
- [ ] JSON/XML parsing has size limits

### Authentication/Authorization
- [ ] Auth checks on protected endpoints
- [ ] Permissions verified before actions
- [ ] Session handling is secure
- [ ] Tokens stored securely

### Sensitive Data
- [ ] No hardcoded secrets or API keys
- [ ] Passwords not logged or exposed
- [ ] PII handled according to policy
- [ ] Encryption used for sensitive storage

### Common Vulnerabilities
- [ ] No command injection (shell commands)
- [ ] No path traversal (../ attacks)
- [ ] No XSS (HTML escaping)
- [ ] No CSRF (token validation)
- [ ] No SQL injection

## Performance

### Efficiency
- [ ] No unnecessary computations in loops
- [ ] Appropriate data structures used
- [ ] Caching used where beneficial
- [ ] Database queries are indexed
- [ ] N+1 query problems avoided

### Resource Usage
- [ ] Memory allocations minimized
- [ ] File handles properly closed
- [ ] Connection pools used appropriately
- [ ] Large data sets paginated

### Async Operations
- [ ] Parallel operations where beneficial
- [ ] Proper timeout handling
- [ ] Retry logic with backoff
- [ ] Circuit breakers for external services

## Maintainability

### Code Structure
- [ ] Functions have single responsibility
- [ ] Classes/modules are cohesive
- [ ] Dependencies are minimal and explicit
- [ ] No circular dependencies

### Naming
- [ ] Variables/functions have descriptive names
- [ ] Naming follows project conventions
- [ ] No misleading names
- [ ] Consistent terminology

### Documentation
- [ ] Public APIs are documented
- [ ] Complex algorithms have explanatory comments
- [ ] TODO comments have issue references
- [ ] README updated if needed

### Code Style
- [ ] Consistent formatting
- [ ] No dead code
- [ ] No commented-out code
- [ ] Import statements organized

## Testing

### Coverage
- [ ] Unit tests for business logic
- [ ] Integration tests for external dependencies
- [ ] Edge cases covered
- [ ] Error paths tested

### Test Quality
- [ ] Tests are independent
- [ ] Tests have clear assertions
- [ ] Test names describe behavior
- [ ] No flaky tests introduced

## Specific to This Project

### Task Management (if applicable)
- [ ] TASK.md acceptance criteria addressed
- [ ] PROGRESS.md updated
- [ ] Dependencies correctly declared
- [ ] Follows existing patterns in codebase
