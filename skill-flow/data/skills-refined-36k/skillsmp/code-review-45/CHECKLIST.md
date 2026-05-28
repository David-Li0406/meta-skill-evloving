# Code Review Checklists

Comprehensive checklists for thorough code reviews. Use these as prompts or reference.

## General Review Checklist

```
Review @file using this checklist:

Logic and Correctness:
- [ ] Code does what it's supposed to do
- [ ] Edge cases handled
- [ ] Boundary conditions checked
- [ ] Off-by-one errors avoided
- [ ] Null/undefined handled
- [ ] Type conversions correct

Error Handling:
- [ ] All errors caught appropriately
- [ ] Error messages helpful
- [ ] Errors logged with context
- [ ] Recovery/fallback where appropriate
- [ ] No silent failures

Code Quality:
- [ ] Single responsibility principle
- [ ] DRY - no unnecessary duplication
- [ ] Functions reasonably sized
- [ ] Names descriptive and consistent
- [ ] Comments explain "why" not "what"

Testing:
- [ ] Unit tests for new code
- [ ] Edge cases tested
- [ ] Error paths tested
- [ ] Tests actually test something

Report findings by category.
```

## Security Checklist

```
Security review @file:

Authentication:
- [ ] Auth required where needed
- [ ] Password handling secure
- [ ] Session management proper
- [ ] Token expiration set
- [ ] Logout clears all tokens

Authorization:
- [ ] Access control checked
- [ ] Role verification present
- [ ] Resource ownership validated
- [ ] No privilege escalation

Input Validation:
- [ ] All inputs validated
- [ ] Input types verified
- [ ] Length limits enforced
- [ ] Special characters handled
- [ ] File uploads restricted

Injection Prevention:
- [ ] SQL injection prevented
- [ ] NoSQL injection prevented
- [ ] XSS prevented
- [ ] Command injection prevented
- [ ] Path traversal prevented

Data Protection:
- [ ] Sensitive data encrypted
- [ ] PII properly handled
- [ ] Secrets not in code
- [ ] Logs don't leak data
- [ ] Error messages safe

Report any violations with severity.
```

## Performance Checklist

```
Performance review @file:

Algorithmic:
- [ ] Time complexity acceptable
- [ ] Space complexity acceptable
- [ ] No unnecessary iterations
- [ ] Early exits where possible
- [ ] Appropriate data structures

Database:
- [ ] No N+1 queries
- [ ] Queries use indexes
- [ ] No SELECT *
- [ ] Pagination for large sets
- [ ] Connections properly managed

Memory:
- [ ] No memory leaks
- [ ] Large objects cleaned up
- [ ] Streams used for big data
- [ ] Caching appropriate
- [ ] No unbounded growth

Async:
- [ ] Parallel where beneficial
- [ ] No unnecessary awaits
- [ ] Promise handling correct
- [ ] Timeouts configured
- [ ] Backpressure handled

Network:
- [ ] Payload sizes reasonable
- [ ] Compression used
- [ ] Caching headers set
- [ ] Request deduplication
- [ ] Connection reuse

Flag any performance concerns.
```

## API Endpoint Checklist

```
Review API endpoint @file:

Request Handling:
- [ ] HTTP method appropriate
- [ ] Path RESTful
- [ ] Query params validated
- [ ] Body validated
- [ ] Headers checked

Authentication & Authorization:
- [ ] Auth middleware applied
- [ ] Permissions verified
- [ ] Rate limiting configured
- [ ] CORS configured

Response:
- [ ] Status codes correct
- [ ] Response format consistent
- [ ] Error format standardized
- [ ] No data leakage
- [ ] Content-Type set

Documentation:
- [ ] Endpoint documented
- [ ] Request format documented
- [ ] Response format documented
- [ ] Error cases documented
- [ ] Examples provided

Report any missing items.
```

## React Component Checklist

```
Review React component @file:

Structure:
- [ ] Functional component (not class)
- [ ] Props properly typed
- [ ] Props have defaults where needed
- [ ] Component size reasonable
- [ ] Logic extracted to hooks

Hooks:
- [ ] Hooks at top level
- [ ] Dependencies array correct
- [ ] Cleanup in useEffect
- [ ] No infinite loops
- [ ] Memoization appropriate

Rendering:
- [ ] No render side effects
- [ ] Keys on list items
- [ ] Conditional rendering clean
- [ ] Loading states handled
- [ ] Error states handled

Performance:
- [ ] Unnecessary re-renders avoided
- [ ] Heavy computation memoized
- [ ] Large lists virtualized
- [ ] Images optimized
- [ ] Code splitting used

Accessibility:
- [ ] Semantic HTML used
- [ ] ARIA labels present
- [ ] Keyboard navigation works
- [ ] Focus management proper
- [ ] Color contrast adequate

Report any violations.
```

## Database Code Checklist

```
Review database code @file:

Queries:
- [ ] Parameterized queries used
- [ ] No string concatenation for SQL
- [ ] Indexes utilized
- [ ] Efficient JOINs
- [ ] Pagination implemented

Transactions:
- [ ] Transaction scope appropriate
- [ ] Rollback on errors
- [ ] Isolation level correct
- [ ] Deadlock potential minimized
- [ ] Connection released

Schema:
- [ ] Constraints defined
- [ ] Types appropriate
- [ ] Nullable fields intentional
- [ ] Foreign keys present
- [ ] Indexes defined

Migrations:
- [ ] Backward compatible
- [ ] Rollback tested
- [ ] Data preserved
- [ ] Performance impact assessed
- [ ] Deployed safely

Report any database concerns.
```

## Test Code Checklist

```
Review tests @file:

Structure:
- [ ] Descriptive test names
- [ ] Arrange-Act-Assert pattern
- [ ] One assertion per test (ideally)
- [ ] Tests independent
- [ ] No test interdependence

Coverage:
- [ ] Happy path tested
- [ ] Error paths tested
- [ ] Edge cases tested
- [ ] Boundary conditions tested
- [ ] Null/undefined tested

Quality:
- [ ] Tests actually verify behavior
- [ ] No false positives
- [ ] Reasonable assertions
- [ ] Mocks appropriate
- [ ] Cleanup performed

Maintainability:
- [ ] Tests are readable
- [ ] Setup not duplicated
- [ ] Test data clear
- [ ] No magic values
- [ ] Comments where needed

Report any test quality issues.
```

## TypeScript Checklist

```
Review TypeScript code @file:

Types:
- [ ] No 'any' without justification
- [ ] Types specific (not too broad)
- [ ] Unions/intersections used properly
- [ ] Generics appropriate
- [ ] Type guards present

Null Safety:
- [ ] Null checks present
- [ ] Optional chaining used
- [ ] Nullish coalescing used
- [ ] Strict null checks honored
- [ ] Assertions justified

Interfaces:
- [ ] Interfaces for objects
- [ ] Types for unions/primitives
- [ ] No redundant properties
- [ ] Inheritance sensible
- [ ] Exported where needed

Best Practices:
- [ ] Readonly where appropriate
- [ ] Const assertions used
- [ ] Enums for fixed sets
- [ ] Template literals typed
- [ ] Function overloads clear

Report any TypeScript issues.
```

## Error Handling Checklist

```
Review error handling in @file:

Catching:
- [ ] All async operations wrapped
- [ ] Promise rejections handled
- [ ] Specific errors caught
- [ ] Not catching and ignoring
- [ ] Re-throwing with context

Types:
- [ ] Custom error classes used
- [ ] Error hierarchy sensible
- [ ] Error codes consistent
- [ ] Stack traces preserved
- [ ] Original error included

Responses:
- [ ] User messages helpful
- [ ] Technical details logged
- [ ] No sensitive data exposed
- [ ] Status codes appropriate
- [ ] Retry info provided

Recovery:
- [ ] Fallback behavior defined
- [ ] Retry logic appropriate
- [ ] Circuit breakers present
- [ ] Graceful degradation
- [ ] User can recover

Report any error handling gaps.
```

## Git Commit Checklist

```
Review commits in this PR:

Messages:
- [ ] Follow conventional commits
- [ ] Subject under 50 chars
- [ ] Body explains "why"
- [ ] References issues
- [ ] No typos

Content:
- [ ] Each commit atomic
- [ ] Related changes grouped
- [ ] No WIP commits
- [ ] No merge commits (if rebase flow)
- [ ] Build passes each commit

Hygiene:
- [ ] No secrets committed
- [ ] No debug code
- [ ] No commented code
- [ ] No large files
- [ ] .gitignore respected

Report any commit issues.
```

## Documentation Checklist

```
Review documentation in @file:

Code Comments:
- [ ] Public APIs documented
- [ ] Complex logic explained
- [ ] "Why" not "what"
- [ ] Examples provided
- [ ] Kept up to date

JSDoc:
- [ ] @param for parameters
- [ ] @returns for return value
- [ ] @throws for errors
- [ ] @example for usage
- [ ] @deprecated if applicable

README:
- [ ] Purpose explained
- [ ] Installation documented
- [ ] Usage examples
- [ ] Configuration listed
- [ ] Contributing guide

API Docs:
- [ ] All endpoints documented
- [ ] Request/response formats
- [ ] Authentication explained
- [ ] Error codes listed
- [ ] Examples provided

Report any documentation gaps.
```

## Quick Checklists

### Minimal Review (5 min)

```
Quick review @file:
- [ ] Does it work?
- [ ] Any obvious bugs?
- [ ] Security red flags?
- [ ] Tests present?
```

### Standard Review (15 min)

```
Standard review @file:
- [ ] Logic correct
- [ ] Errors handled
- [ ] Code clean
- [ ] Tests adequate
- [ ] No security issues
- [ ] Docs updated
```

### Deep Review (30+ min)

```
Deep review @file:
[Use full checklists from above for:]
- [ ] Security
- [ ] Performance
- [ ] Code quality
- [ ] Testing
- [ ] Architecture
- [ ] Documentation
```

## Using Checklists

### Request Specific Checklist

```
Run the security checklist on @src/auth/
```

### Combine Checklists

```
Review @src/api/users.ts using:
- API endpoint checklist
- Security checklist
- Error handling checklist
```

### Custom Checklist

```
Review @file using this custom checklist:
- [ ] Custom check 1
- [ ] Custom check 2
- [ ] Custom check 3
```
