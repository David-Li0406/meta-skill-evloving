# Verification Checklist

Detailed verification patterns by task type.

## Code Changes

### Functionality
- [ ] Feature works as described in requirements
- [ ] All acceptance criteria met
- [ ] Edge cases handled appropriately
- [ ] Error states handled gracefully
- [ ] No regressions in existing functionality

### Code Quality
- [ ] No linting errors or warnings
- [ ] No TypeScript/type errors
- [ ] Follows project coding conventions
- [ ] No hardcoded values (use env vars/config)
- [ ] No commented-out code left behind
- [ ] No TODO/FIXME without tracking issue

### Testing
- [ ] Existing tests still pass
- [ ] New tests added for new functionality
- [ ] Tests cover happy path and edge cases
- [ ] Test names are descriptive

### Security
- [ ] No secrets/credentials in code
- [ ] Input validation in place
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Auth/authz checks present where needed

---

## Documentation Changes

### Accuracy
- [ ] Information is technically correct
- [ ] Code examples work as shown
- [ ] Links are valid and point to correct destinations
- [ ] Version numbers/dates are current

### Completeness
- [ ] All required sections present
- [ ] Prerequisites clearly stated
- [ ] Step-by-step instructions are complete
- [ ] Expected outcomes described

### Clarity
- [ ] Easy to understand for target audience
- [ ] Consistent terminology throughout
- [ ] Proper formatting and structure
- [ ] No grammatical errors

---

## Configuration Changes

### Validity
- [ ] Syntax is valid (JSON/YAML/etc.)
- [ ] All required fields present
- [ ] Field values are correct types
- [ ] No duplicate keys

### Functionality
- [ ] Configuration loads without error
- [ ] Settings take effect as expected
- [ ] Defaults are sensible
- [ ] Environment-specific values handled correctly

### Security
- [ ] Sensitive values use secrets management
- [ ] Access permissions are appropriate
- [ ] No overly permissive settings

---

## Database Changes

### Schema
- [ ] Migrations run successfully
- [ ] Rollback scripts exist and work
- [ ] Indexes added for query patterns
- [ ] Foreign keys/constraints are correct

### Data
- [ ] Existing data preserved or migrated
- [ ] Default values make sense
- [ ] No data loss scenarios

---

## API Changes

### Contract
- [ ] Endpoint behaves as documented
- [ ] Request/response schemas are correct
- [ ] Error responses are consistent
- [ ] Versioning handled appropriately

### Compatibility
- [ ] Backward compatible (or breaking change documented)
- [ ] Clients can still function
- [ ] Deprecation warnings added if needed

---

## Common Pitfalls

Things to always check:

1. **Environment mismatch** - Works locally but not in staging/prod
2. **Missing env vars** - New variables not added to deployment
3. **Hardcoded URLs** - Should be environment-specific
4. **Incomplete cleanup** - Debug code, console.logs left in
5. **Missing error handling** - Unhappy paths not considered
6. **Assumption violations** - Code assumes things that aren't guaranteed
7. **Race conditions** - Concurrent access issues
8. **Memory leaks** - Resources not properly released
