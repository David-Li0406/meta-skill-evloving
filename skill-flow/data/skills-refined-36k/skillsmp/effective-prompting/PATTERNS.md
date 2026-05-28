# Prompt Patterns

Detailed prompt patterns for specific task types.

## Task Decomposition Prompts

Break complex work into manageable chunks.

### Feature Implementation

```
Implement [feature name].

## Context
@relevant/files.ts
@types/related.ts

## Requirements
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

## Implementation Steps
1. Start with [foundation]
2. Then add [core logic]
3. Finally implement [integration]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] Tests pass
- [ ] TypeScript compiles without errors
```

### System Migration

```
Migrate [system A] to [system B].

## Current State
@path/to/current/implementation

## Target State
- [Description of desired end state]

## Migration Steps
1. Create adapter layer (no breaking changes)
2. Migrate [component 1] behind feature flag
3. Migrate [component 2]
4. Remove adapter layer
5. Clean up feature flags

## Rollback Plan
If issues arise: [rollback steps]

## Validation
- [ ] All existing tests pass
- [ ] New integration tests added
- [ ] Performance benchmarks met
```

## Code Review Prompts

### Security Review

```
Review @src/auth/ for security vulnerabilities.

Focus on:
- SQL injection risks
- XSS vulnerabilities
- Authentication bypass
- Sensitive data exposure
- CSRF protection

For each issue found, provide:
1. Severity (Critical/High/Medium/Low)
2. Location (file:line)
3. Description
4. Remediation
```

### Performance Review

```
ultrathink about performance issues in @src/api/search.ts

Analyze:
- Time complexity of algorithms
- Database query efficiency
- Memory allocation patterns
- Unnecessary re-renders (if React)
- Network request optimization

Provide specific recommendations with code examples.
```

### Architecture Review

```
Review the architecture of @src/services/

Evaluate:
- Separation of concerns
- Dependency injection
- Error handling patterns
- Testability
- Scalability considerations

Compare against:
- SOLID principles
- Clean Architecture patterns
- Our existing conventions in @ARCHITECTURE.md
```

### Pull Request Review

```
Review this PR for:
@git:diff

Focus areas:
- Correctness
- Edge cases
- Test coverage
- Code style consistency
- Documentation updates needed

Format: Comment per file with line-specific feedback.
```

## Debugging Prompts

### Symptom-Based Debugging

```
Debug: [symptom description]

## Reproduction
1. [Step 1]
2. [Step 2]
3. Error occurs

## Expected
[What should happen]

## Actual
[What happens instead]

## Context
@src/relevant/code.ts
@logs/error.log

## Already Tried
- [Attempt 1] - Result: [result]
- [Attempt 2] - Result: [result]

think harder about potential root causes.
```

### Error Message Debugging

```
Getting this error:
[exact error message]

Stack trace:
[stack trace if available]

Context:
@src/file/mentioned/in/stack.ts

Environment:
- Node: [version]
- OS: [os]
- Related packages: [versions]

What's causing this and how do I fix it?
```

### Intermittent Bug Debugging

```
ultrathink about this intermittent bug.

## Symptom
[Behavior that sometimes occurs]

## Frequency
Happens ~[X]% of the time

## Conditions
Seems more likely when:
- [Condition 1]
- [Condition 2]

## Code
@src/suspected/area/

Consider:
- Race conditions
- State management issues
- External service timing
- Cache invalidation
- Memory leaks
```

## Refactoring Prompts

### Extract Component/Module

```
Extract [functionality] from @src/monolith.ts into a separate module.

## Goals
- Single responsibility
- Testable in isolation
- Clear interface

## Constraints
- Keep public API backward compatible
- No runtime behavior changes
- Existing tests must pass

## Steps
1. Identify dependencies
2. Create new module with interface
3. Move implementation
4. Update imports
5. Add unit tests for new module
```

### Improve Code Quality

```
Refactor @src/legacy/code.ts to improve maintainability.

Current issues:
- [Issue 1: e.g., 500 line function]
- [Issue 2: e.g., deep nesting]
- [Issue 3: e.g., magic numbers]

Maintain:
- All existing functionality
- Test compatibility
- API contracts

Apply:
- Extract method pattern
- Guard clauses
- Named constants
- TypeScript strict mode
```

### Pattern Standardization

```
Standardize error handling across @src/api/

## Current State
Multiple approaches:
- Some use try/catch
- Some use .catch()
- Some don't handle errors

## Target Pattern
```typescript
// Standard error handling
try {
  const result = await operation();
  return { success: true, data: result };
} catch (error) {
  logger.error('Operation failed', { error, context });
  throw new AppError('OPERATION_FAILED', error);
}
```

## Apply this pattern to all API handlers.
```

## Documentation Prompts

### API Documentation

```
Generate API documentation for @src/api/users.ts

Include:
- Endpoint summary
- Request parameters (path, query, body)
- Response schema with examples
- Error responses
- Authentication requirements
- Rate limits if applicable

Format: OpenAPI 3.0 compatible YAML
```

### Code Documentation

```
Add documentation to @src/utils/encryption.ts

For each function:
- JSDoc comment with description
- @param for each parameter
- @returns description
- @throws for errors
- @example with usage

Don't document obvious getters/setters.
```

### Architecture Documentation

```
Document the architecture of @src/services/payment/

Create a markdown file covering:
1. Overview and purpose
2. Component diagram (mermaid)
3. Data flow
4. External dependencies
5. Configuration requirements
6. Error handling strategy
7. Scaling considerations
```

### README Generation

```
Generate a README.md for @src/packages/utils/

Include:
- Package description
- Installation
- Quick start example
- API reference (brief)
- Configuration options
- Contributing guidelines

Tone: Professional, concise
```

## Testing Prompts

### Unit Test Generation

```
Write unit tests for @src/services/calculator.ts

Cover:
- Happy path for each public method
- Edge cases (empty input, max values, null)
- Error conditions
- Boundary values

Use:
- Vitest/Jest syntax
- Descriptive test names
- AAA pattern (Arrange, Act, Assert)
- Minimal mocking
```

### Integration Test Generation

```
Write integration tests for the user registration flow.

## Flow
1. POST /api/register with user data
2. Verify user created in database
3. Verify welcome email queued
4. Verify JWT returned

## Setup Needed
- Test database
- Mock email service
- Clean state between tests

## Cover
- Success case
- Duplicate email
- Invalid input
- Database failure
- Email service failure
```

### E2E Test Generation

```
Write Playwright E2E tests for the login flow.

## User Journey
1. Visit /login
2. Enter credentials
3. Click submit
4. Verify redirect to /dashboard
5. Verify user menu shows name

## Test Cases
- Valid credentials
- Invalid password
- Account locked
- Remember me checkbox
- Forgot password link

Use data-testid attributes for selectors.
```

### Test Improvement

```
Improve test coverage for @src/services/order.ts

Current coverage: @coverage/order.ts.html

Add tests for:
- Uncovered branches
- Error paths
- Edge cases identified in coverage report

Don't duplicate existing tests in @tests/order.test.ts
```

## Prompt Chaining

Chain prompts for complex workflows.

### Research -> Implement -> Test

```
# Prompt 1: Research
Research best practices for implementing [feature].
Consider: security, performance, maintainability.
Summarize top 3 approaches with trade-offs.

# Prompt 2: Implement
Implement approach [N] from previous research.
@relevant/context.ts
Follow constraints: [list]

# Prompt 3: Test
Write comprehensive tests for the implementation.
Cover the edge cases identified in research phase.
```

### Audit -> Plan -> Execute

```
# Prompt 1: Audit
Audit @src/legacy/ for technical debt.
Categorize by: severity, effort, impact.
Output: prioritized list.

# Prompt 2: Plan
Create a refactoring plan for top 5 issues.
Include: steps, risks, time estimates.

# Prompt 3: Execute
Execute step 1 of the refactoring plan.
Checkpoint after each file changed.
```
