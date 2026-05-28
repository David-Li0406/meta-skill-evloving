# Code Review Checklist

Use this checklist before submitting code or when reviewing others' code.

## Architecture & Design

### Clean Architecture Compliance
- [ ] Code is in the correct layer (server/service/repository)
- [ ] Dependencies flow inward (no service importing repository implementations)
- [ ] Interfaces used for dependencies, not concrete types
- [ ] Domain entities have no external dependencies
- [ ] Business logic is in service layer, not controllers
- [ ] SQL queries are in repository layer, not service

### Dependency Injection
- [ ] New services/repositories added to `internal/deployment/wire.go`
- [ ] Wire bindings added for new interfaces
- [ ] Ran `./generate.sh` after Wire config changes
- [ ] Constructor functions are public and follow `New{Type}` pattern
- [ ] Struct implementations are private (lowercase)

### OpenAPI Compliance
- [ ] New endpoints defined in `openapi/api_v1.yaml` first
- [ ] Ran `./generate.sh` after OpenAPI changes
- [ ] Controller implements generated `ServerInterface` methods
- [ ] Request/response types match OpenAPI spec exactly
- [ ] No manual edits to `*_gen.go` files

## Code Quality

### Error Handling
- [ ] All errors are handled (no ignored return values)
- [ ] Service/repository methods return `domain.Error`, not `error`
- [ ] Errors have descriptive messages
- [ ] Errors include appropriate HTTP status codes
- [ ] Errors are wrapped with context using `domain.Wrap()`
- [ ] No panics except in truly exceptional cases
- [ ] Guard rails return 404 (not 403) for access denied

### Context Handling
- [ ] Context is first parameter in all functions
- [ ] Context is passed through all layers
- [ ] User ID extracted from context where needed
- [ ] Client ID extracted for SSE operations
- [ ] Context not stored in structs

### Resource Management
- [ ] Database rows closed with `defer rows.Close()`
- [ ] Transactions rolled back with `defer tx.Rollback()`
- [ ] HTTP response bodies closed
- [ ] Goroutines have clear termination conditions
- [ ] No resource leaks

### Concurrency
- [ ] Shared state properly synchronized
- [ ] SSE channels use non-blocking sends (select with default)
- [ ] Goroutines don't capture loop variables incorrectly
- [ ] No race conditions (run `go test -race`)

## Security

### Authentication & Authorization
- [ ] Guard rail checks before sensitive operations
- [ ] `HasAccessToChecklist` or `IsChecklistOwner` called appropriately
- [ ] User ID comes from validated JWT context, not request parameters
- [ ] Client ID validated where required (SSE, mutations)

### Input Validation
- [ ] User input validated before use
- [ ] SQL uses parameterized queries (pgx.NamedArgs)
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities in responses
- [ ] File paths sanitized (if applicable)

### Data Exposure
- [ ] Sensitive data not logged
- [ ] Error messages don't leak sensitive information
- [ ] Guard rails hide existence of inaccessible resources (404, not 403)
- [ ] No credentials in code or logs

## Database

### Query Quality
- [ ] Uses `pgx.NamedArgs` for parameters, not positional
- [ ] Queries use appropriate indexes (consider performance)
- [ ] Transactions used where needed (multiple operations)
- [ ] Correct isolation level (`pgx.Serializable` for critical operations)
- [ ] Row count checked after DELETE/UPDATE operations

### Schema Compliance
- [ ] Foreign keys have appropriate CASCADE/SET NULL behavior
- [ ] Nullable vs NOT NULL matches domain requirements
- [ ] Database types match Go types (BIGINT → uint, etc.)
- [ ] DBO structs match database schema
- [ ] Queries filter phantom items (`WHERE IS_PHANTOM = FALSE`)

### Migrations
- [ ] `init.sql` updated if schema changes
- [ ] Migration script created for existing deployments
- [ ] Both UP and DOWN migrations provided
- [ ] Migrations tested with sample data

## Testing

### Test Coverage
- [ ] Unit tests for new service methods
- [ ] Tests for success case
- [ ] Tests for all error cases
- [ ] Tests for edge cases (nil, empty, boundaries)
- [ ] Tests for guard rail failures
- [ ] All tests pass (`go test ./...`)

### Test Quality
- [ ] Tests use testify mocks
- [ ] Mock expectations are verified (`AssertExpectations`)
- [ ] Test names follow `Test{Struct}_{Method}_{Scenario}` pattern
- [ ] Table-driven tests for multiple similar scenarios
- [ ] Tests are isolated (no shared state)
- [ ] No brittle tests (testing behavior, not implementation)

### SSE Testing
- [ ] Notification service called after mutations
- [ ] Correct event type used
- [ ] Event payload matches schema
- [ ] Client ID filtering tested (if applicable)

## Code Style

### Naming
- [ ] Variables are descriptive (avoid `x`, `tmp`, `data`)
- [ ] Function names are verb-based (`Delete`, `Find`, `Update`)
- [ ] No abbreviations unless standard (`id`, `url`, `ctx`)
- [ ] Exported names start with capital letter only when needed
- [ ] Interface names use "I" prefix (project convention)

### Formatting
- [ ] Code formatted with `gofmt` or `goimports`
- [ ] Consistent indentation (tabs, not spaces)
- [ ] No trailing whitespace
- [ ] Import statements grouped correctly (standard, external, internal)
- [ ] Line length reasonable (< 120 characters)

### Comments
- [ ] Public functions have doc comments
- [ ] Complex logic explained (WHY, not WHAT)
- [ ] No commented-out code
- [ ] TODO comments have context or issue numbers
- [ ] No misleading or outdated comments

### Code Smells
- [ ] No magic numbers (use named constants)
- [ ] No duplicated code (DRY principle)
- [ ] Functions are focused (single responsibility)
- [ ] Functions are reasonably sized (< 50 lines as guideline)
- [ ] No deeply nested conditionals (max 3-4 levels)
- [ ] No overly complex conditions (extract to named functions)

## Project-Specific

### SSE Notifications
- [ ] Events published after successful mutations
- [ ] Correct event type from OpenAPI spec (`EventEnvelope`)
- [ ] Event payload matches schema
- [ ] Non-blocking publish pattern used
- [ ] Client ID available in context

### Guard Rails
- [ ] `HasAccessToChecklist` for read/write operations
- [ ] `IsChecklistOwner` for owner-only operations
- [ ] Returns `error.NewChecklistNotFoundError(id)` on access denial
- [ ] Guard rail called before business logic

### Linked List Ordering
- [ ] Phantom items filtered in queries (`IS_PHANTOM = FALSE`)
- [ ] Order changes use `NEXT_ITEM_ID`/`PREV_ITEM_ID` updates
- [ ] Queries use `CHECKLIST_ITEMS_ORDERED_VIEW` for ordered results
- [ ] Reordering handles edge cases (first, last, middle)

### Configuration
- [ ] Environment variables defined in `application.yaml`
- [ ] Default values provided with `${VAR:default}` syntax
- [ ] No hardcoded configuration in code
- [ ] Sensitive config (DB password, secrets) from env vars

## Performance

### Query Optimization
- [ ] No N+1 query problems
- [ ] Queries fetch only needed columns
- [ ] Pagination implemented for large result sets
- [ ] Indexes exist for commonly filtered columns

### Memory Management
- [ ] Large slices pre-allocated if size known
- [ ] Streaming used for large datasets
- [ ] Resources released promptly (no long-lived connections)
- [ ] SSE channels have buffer limits

### Unnecessary Work
- [ ] No repeated calculations (cache if expensive)
- [ ] No premature optimization
- [ ] Guard conditions early (fail fast)
- [ ] Defers placed correctly (not in loops)

## Documentation

### Code Documentation
- [ ] CLAUDE.md updated if architecture changes
- [ ] README updated if setup changes
- [ ] OpenAPI spec has descriptions for new endpoints
- [ ] API documentation accurate

### Comments
- [ ] Complex algorithms explained
- [ ] Non-obvious design decisions documented
- [ ] External dependencies documented
- [ ] Known limitations noted

## Pre-Commit Checklist

Run these commands before committing:

```bash
# 1. Code generation (if OpenAPI or Wire changed)
./generate.sh

# 2. Format code
gofmt -w .

# 3. Vet code
go vet ./...

# 4. Run tests
go test ./...

# 5. Check for race conditions
go test -race ./...

# 6. Build
go build ./...
```

## Common Issues

### Issue: "Wire build failed"
- [ ] Check `internal/deployment/wire.go` syntax
- [ ] Ensure all providers are defined
- [ ] Verify interface bindings are correct
- [ ] Run `./generate.sh` to see detailed error

### Issue: "Tests failing"
- [ ] Check mock expectations match actual calls
- [ ] Verify all interface methods implemented in mocks
- [ ] Look for nil pointer dereferences
- [ ] Check context.Background() vs actual context

### Issue: "SSE not working"
- [ ] Verify Client ID header sent
- [ ] Check notification service wired correctly
- [ ] Ensure event published after mutation
- [ ] Verify guard rail on SSE endpoint

### Issue: "Access denied but should work"
- [ ] Check user ID in context (JWT middleware)
- [ ] Verify guard rail logic
- [ ] Check database shares/ownership
- [ ] Look for guard rail called with wrong parameters

## Review Severity Levels

### 🔴 Critical (Must Fix)
- Security vulnerabilities
- Data corruption risks
- Memory leaks or resource leaks
- Broken core functionality
- Incorrect layer separation (violates Clean Architecture)

### 🟡 Important (Should Fix)
- Missing error handling
- Missing tests for new code
- Performance issues
- Confusing naming
- Missing guard rail checks

### 🟢 Minor (Nice to Have)
- Code style inconsistencies
- Missing comments on complex code
- Refactoring opportunities
- Documentation improvements

## Sign-Off

Before marking code as ready for merge:

- [ ] All tests pass locally
- [ ] Code builds without warnings
- [ ] Manual testing completed (if applicable)
- [ ] CLAUDE.md updated if needed
- [ ] No console.log or debug code left in
- [ ] Git commit message is descriptive

---

**Remember**: The goal is maintainable, secure, correct code - not perfect code. Balance thoroughness with pragmatism.
