# Compliance Patterns

Patterns for checking compliance with AI Agent Instructions (CLAUDE.md, etc.).

## Instruction File Locations

See `${CLAUDE_PLUGIN_ROOT}/shared/skill-common-workflow.md` Step 2 for the canonical search order.

## Rule Classification

### MUST/MUST NOT Rules

**Keywords**: MUST, MUST NOT, SHALL, SHALL NOT, REQUIRED, ALWAYS, NEVER

These are mandatory rules. Violations are **Major** severity.

**Examples**:
```markdown
- All API endpoints MUST have authentication
- NEVER commit secrets to the repository
- Controllers MUST NOT contain business logic
```

### SHOULD/SHOULD NOT Rules

**Keywords**: SHOULD, SHOULD NOT, RECOMMENDED, PREFER

These are strong recommendations. Violations are **Minor** severity.

**Examples**:
```markdown
- Functions SHOULD have JSDoc comments
- PREFER async/await over raw promises
- Database queries SHOULD use transactions
```

### MAY/CONSIDER Rules

**Keywords**: MAY, OPTIONAL, CONSIDER, CAN

These are suggestions. Violations are **Suggestion** severity.

**Examples**:
```markdown
- You MAY use helper functions for common patterns
- CONSIDER adding performance logging
```

## Common Rule Categories

### Architecture Rules

```markdown
# Example CLAUDE.md section
## Architecture

- MUST use repository pattern for data access
- Services MUST NOT directly access database
- Controllers MUST be thin - delegate to services
- PREFER composition over inheritance
```

**What to Check**:
- Direct database calls in controllers
- Business logic in controllers
- Circular dependencies
- Layer violations (e.g., UI importing from data layer)

### Naming Conventions

```markdown
## Naming

- Files MUST use kebab-case (e.g., user-service.ts)
- Classes MUST use PascalCase
- Functions MUST use camelCase
- Constants SHOULD use UPPER_SNAKE_CASE
- Interfaces MUST be prefixed with 'I' (C#) or not prefixed (TypeScript)
```

**What to Check**:
- File names not matching pattern
- Class/function naming violations
- Inconsistent naming across codebase

### Testing Requirements

```markdown
## Testing

- All public functions MUST have unit tests
- API endpoints MUST have integration tests
- Test files MUST be in __tests__ directory
- Test names SHOULD describe behavior, not implementation
```

**What to Check**:
- New functions without corresponding tests
- Test file location
- Test naming patterns

### Documentation Requirements

```markdown
## Documentation

- Public APIs MUST have JSDoc/XMLDoc comments
- Complex functions SHOULD have inline comments
- README MUST be updated for new features
```

**What to Check**:
- Missing documentation on public functions
- Outdated README after changes

### Security Requirements

```markdown
## Security

- User input MUST be validated before use
- SQL queries MUST use parameterization
- Secrets MUST NOT be hardcoded
- Authentication MUST be required on all /api routes
```

**What to Check**:
- Unvalidated user input
- SQL string concatenation
- Hardcoded credentials
- Missing auth middleware

### Error Handling Requirements

```markdown
## Error Handling

- Async functions MUST handle errors
- API errors MUST return appropriate status codes
- Errors MUST be logged with context
- NEVER expose stack traces in production
```

**What to Check**:
- Empty catch blocks
- Missing error handling
- Sensitive info in error messages

## Checking Process

### Step 1: Parse Instructions

Extract rules from instruction files:
- Identify keyword (MUST, SHOULD, MAY, etc.)
- Extract the requirement
- Note any file patterns (e.g., "applies_to: src/**/*.ts")

### Step 2: Match Files

For each changed file:
- Check if any rules apply based on file path
- Check if any rules apply based on file content/type

### Step 3: Check Compliance

For each applicable rule:
- Analyze the code for compliance
- If violation found, classify severity based on keyword
- Include the exact rule text in the issue

### Step 4: Report Format

```yaml
issues:
  - title: "Missing authentication on API endpoint"
    file: "src/api/admin.ts"
    line: 34
    category: "Compliance"
    severity: "Major"
    rule_violated: "Authentication MUST be required on all /api routes"
    rule_source: "CLAUDE.md:45"
    description: "The /api/admin/stats endpoint has no authentication middleware"
    fix_type: "diff"
    fix_diff: |
      - router.get('/stats', getStats);
      + router.get('/stats', requireAuth, requireAdmin, getStats);
```

## Ignoring Rules

Rules can be silenced with comments:

```javascript
// claude-ignore: no-console
console.log('Debug info');

// eslint-disable-next-line
// @ts-ignore
```

Check for these patterns and don't flag violations that are explicitly silenced.

## Quick Reference

| Keyword | Severity | Action |
|---------|----------|--------|
| MUST, SHALL, REQUIRED, ALWAYS | Major | Must fix |
| MUST NOT, SHALL NOT, NEVER | Major | Must fix |
| SHOULD, RECOMMENDED, PREFER | Minor | Should fix |
| SHOULD NOT | Minor | Should fix |
| MAY, OPTIONAL, CONSIDER | Suggestion | Optional |
