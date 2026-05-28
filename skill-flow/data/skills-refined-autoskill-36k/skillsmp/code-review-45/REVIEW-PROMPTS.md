# Review Prompts

Effective prompts for different types of code reviews with Claude Code.

## Security Reviews

### Comprehensive Security Audit

```
ultrathink security review of @src/auth/ @src/api/

Examine:
1. Authentication
   - Password handling (hashing, storage)
   - Session management
   - Token generation and validation
   - Multi-factor auth flows

2. Authorization
   - Access control checks
   - Role/permission validation
   - Resource ownership verification
   - Privilege escalation paths

3. Input Handling
   - Validation completeness
   - Sanitization
   - SQL injection vectors
   - NoSQL injection vectors
   - Command injection

4. Output Encoding
   - XSS prevention
   - Content-Type headers
   - Response data filtering

5. Cryptography
   - Algorithm choices
   - Key management
   - Random number generation

6. Configuration
   - Secrets in code
   - Debug modes
   - Error verbosity

Format findings as:
[CRITICAL|HIGH|MEDIUM|LOW] - [Category] - [File:Line]
Description: [What's wrong]
Attack: [How it could be exploited]
Fix: [How to remediate]
```

### API Security Review

```
Security review @src/api/

For each endpoint, verify:
- [ ] Authentication required (or intentionally public)
- [ ] Authorization checks present
- [ ] Input validated and sanitized
- [ ] Rate limiting applied
- [ ] Sensitive data not logged
- [ ] Error messages don't leak info
- [ ] CORS configured correctly
- [ ] Content-Type enforced

List any endpoints missing these protections.
```

### Dependency Security

```
Review package.json and lock file for:
- Known vulnerabilities (check recent CVEs)
- Outdated packages with security patches
- Unnecessary dependencies that increase attack surface
- Dev dependencies in production

Suggest:
1. Immediate updates needed
2. Packages to audit further
3. Packages to consider replacing
```

### Data Handling Review

```
Review @src/services/ @src/repositories/ for data security:

Personal Data:
- Is PII identified and protected?
- Encryption at rest?
- Encryption in transit?
- Access logging?

Sensitive Operations:
- Audit trail for changes?
- Soft delete vs hard delete?
- Data retention policies enforced?

Data Leakage:
- Logs contain sensitive data?
- Error messages expose internals?
- Debug endpoints in production?
```

## Performance Reviews

### General Performance Audit

```
Performance review @src/services/

Analyze:
1. Time Complexity
   - Nested loops
   - Recursive calls
   - Algorithm efficiency

2. Space Complexity
   - Large object creation
   - Memory leaks
   - Unbounded collections

3. I/O Operations
   - Database queries per request
   - External API calls
   - File system operations

4. Async Patterns
   - Proper await usage
   - Parallel vs sequential
   - Promise handling

For each issue:
- Location: [file:line]
- Impact: [estimated severity]
- Current: [what's happening]
- Optimized: [better approach]
- Tradeoff: [any downsides]
```

### Database Performance

```
Review @src/repositories/ for database performance:

Query Patterns:
- [ ] N+1 queries identified
- [ ] Proper use of JOINs vs multiple queries
- [ ] SELECT * avoided (explicit columns)
- [ ] LIMIT used for large datasets
- [ ] Pagination implemented correctly

Indexing:
- [ ] Queries use available indexes
- [ ] Missing indexes identified
- [ ] Over-indexing avoided

Transactions:
- [ ] Appropriate transaction scope
- [ ] Deadlock potential
- [ ] Lock contention points

Connection Management:
- [ ] Connection pooling used
- [ ] Connections properly released
- [ ] Timeout handling
```

### Frontend Performance

```
Performance review @src/components/

React-specific:
- Unnecessary re-renders
- Missing memoization
- Heavy computations in render
- Large component trees
- Prop drilling depth

Bundle Impact:
- Large dependencies imported
- Tree-shaking opportunities
- Dynamic imports for code splitting

Data Fetching:
- Overfetching
- Cache usage
- Loading state handling
- Request deduplication
```

### API Response Performance

```
Review @src/api/ for response performance:

Payload Size:
- Unnecessary fields returned
- Nested objects depth
- Array sizes unbounded

Processing:
- Heavy computation in request path
- Blocking operations
- Background job candidates

Caching:
- Cacheable responses identified
- Cache headers set correctly
- Invalidation strategy clear
```

## Style and Consistency Reviews

### Code Style Review

```
Style review @src/ against project conventions:

Reference:
@.eslintrc.js
@.prettierrc
@tsconfig.json

Check:
1. Naming Conventions
   - Variables: camelCase
   - Constants: UPPER_SNAKE
   - Classes: PascalCase
   - Files: consistent pattern

2. Structure
   - Import ordering
   - Export patterns
   - File organization

3. TypeScript Usage
   - Type annotations
   - Any usage
   - Null handling
   - Generic patterns

4. Comments
   - JSDoc presence
   - Comment quality
   - TODO/FIXME tracking

Only report deviations from established patterns.
```

### React Style Review

```
Style review @src/components/

Check against React best practices:
- Functional components used
- Hooks follow rules
- Props properly typed
- Default props pattern
- Children pattern
- Event handler naming
- State organization
- Effect dependencies
- Cleanup functions
```

### API Style Review

```
Style review @src/api/ for consistency:

REST Conventions:
- Resource naming (plural, kebab-case)
- HTTP method usage
- Status code appropriateness
- Error response format

Code Patterns:
- Handler structure
- Validation approach
- Error handling
- Response formatting
- Middleware usage
```

### Test Style Review

```
Style review @src/**/*.test.ts

Check:
- Test naming conventions
- Describe/it structure
- Arrange-Act-Assert pattern
- Mock usage and cleanup
- Assertion specificity
- Test isolation
- Coverage of edge cases
```

## Architecture Reviews

### Module Architecture

```
ultrathink about the architecture of @src/orders/

Evaluate:
1. Boundaries
   - Clear module interface?
   - Internal vs exported?
   - Dependencies direction?

2. Responsibilities
   - Single responsibility?
   - Separation of concerns?
   - Business logic location?

3. Dependencies
   - Dependency injection?
   - Hard-coded dependencies?
   - Circular dependencies?

4. Coupling
   - Tight coupling points?
   - Shared mutable state?
   - Interface vs implementation?

5. Cohesion
   - Related functionality grouped?
   - Feature completeness?
   - Module size appropriate?

Diagram the current structure and suggest improvements.
```

### API Design Review

```
ultrathink about the API design in @src/api/

Evaluate:
1. Resource Modeling
   - Domain concepts mapped correctly?
   - Relationships clear?
   - Naming intuitive?

2. Operations
   - CRUD complete where needed?
   - Custom actions appropriate?
   - Batch operations considered?

3. Versioning
   - Version strategy?
   - Breaking change handling?
   - Deprecation approach?

4. Extensibility
   - Easy to add endpoints?
   - Schema evolution?
   - Feature flags?
```

### Data Flow Review

```
Review data flow through @src/

Trace a request from:
1. API entry point
2. Validation layer
3. Business logic
4. Data access
5. Response formatting

For each layer:
- What transforms happen?
- What can fail?
- How are errors handled?
- What's logged?

Identify:
- Unnecessary transformations
- Data loss points
- Error swallowing
- Logging gaps
```

## Code Quality Reviews

### Error Handling Review

```
Review @src/ for error handling:

Check:
1. Errors Caught
   - All async operations try/caught?
   - Promise rejections handled?
   - Event errors caught?

2. Error Types
   - Specific error classes used?
   - Error context preserved?
   - Stack traces maintained?

3. Error Response
   - User-friendly messages?
   - Consistent format?
   - Appropriate HTTP status?

4. Error Recovery
   - Retry logic where appropriate?
   - Fallback behavior?
   - Graceful degradation?

5. Error Logging
   - Sufficient context logged?
   - Sensitive data excluded?
   - Alert-worthy errors identified?
```

### Testability Review

```
Review @src/services/ for testability:

Evaluate:
1. Dependency Injection
   - Dependencies injectable?
   - Hard-coded dependencies?
   - Configuration externalized?

2. Side Effects
   - Pure functions isolated?
   - I/O at boundaries?
   - Global state avoided?

3. Interfaces
   - Mockable interfaces?
   - Abstraction appropriate?
   - Contract clarity?

4. Complexity
   - Cyclomatic complexity?
   - Branch coverage feasibility?
   - Edge cases identifiable?

For each hard-to-test area, suggest refactoring.
```

### Documentation Review

```
Review @src/ for documentation quality:

Check:
1. Public APIs
   - JSDoc complete?
   - Parameters documented?
   - Return values described?
   - Examples provided?

2. Complex Logic
   - Comments explain "why"?
   - Algorithm documented?
   - Edge cases noted?

3. Configuration
   - Options documented?
   - Defaults explained?
   - Environment variables listed?

4. README/Guides
   - Setup instructions current?
   - Examples working?
   - Troubleshooting covered?

Rate documentation: [Complete|Adequate|Needs Work|Missing]
```

## Specialized Reviews

### Migration Review

```
Review migration in @src/migrations/

Check:
1. Schema Changes
   - Backward compatible?
   - Data preserved?
   - Constraints added safely?

2. Data Migration
   - Large table handling?
   - Batching implemented?
   - Progress tracking?

3. Rollback
   - Down migration works?
   - Data recoverable?
   - Tested rollback?

4. Deployment
   - Zero-downtime possible?
   - Sequence with code deploy?
   - Feature flags needed?
```

### Concurrency Review

```
Review @src/services/ for concurrency issues:

Check:
1. Race Conditions
   - Check-then-act patterns
   - Shared state mutations
   - Read-modify-write operations

2. Deadlocks
   - Lock ordering
   - Nested locks
   - Resource contention

3. Atomicity
   - Multi-step operations
   - Transaction boundaries
   - Rollback handling

4. Thread Safety
   - Shared state access
   - Singleton patterns
   - Global variables
```

### Accessibility Review

```
Review @src/components/ for accessibility:

Check:
1. Semantic HTML
   - Proper heading hierarchy
   - Landmark regions
   - Lists for lists

2. ARIA
   - Labels for interactive elements
   - Live regions for updates
   - Role attributes correct

3. Keyboard
   - All functions keyboard accessible
   - Focus management
   - Tab order logical

4. Visual
   - Color contrast
   - Focus indicators
   - Text scaling

5. Screen Reader
   - Alt text for images
   - Form labels
   - Error announcements
```

## Review Response Formats

### Tabular Format

```
Format findings as a table:

| Severity | Type | Location | Issue | Fix |
|----------|------|----------|-------|-----|
| HIGH | Security | auth.ts:42 | No rate limit | Add rate limiter |
```

### Structured JSON

```
Return findings as JSON:
{
  "summary": "...",
  "critical": [...],
  "high": [...],
  "medium": [...],
  "low": [...],
  "positive": [...]
}
```

### PR Comment Format

```
Format as GitHub PR comments:

### Security: Input validation missing

**File:** `src/api/users.ts` (line 42)

Current code allows unsanitized input:
\`\`\`typescript
// problematic code
\`\`\`

Suggested fix:
\`\`\`typescript
// fixed code
\`\`\`
```
