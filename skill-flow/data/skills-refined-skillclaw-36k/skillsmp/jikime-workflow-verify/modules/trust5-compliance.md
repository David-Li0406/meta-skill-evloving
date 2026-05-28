# TRUST 5 Compliance

Detailed principle checks and scoring for TRUST 5 framework compliance.

## Principle Checks

### [T] Tested

- Unit test coverage > 80%
- Critical paths have tests
- Edge cases covered
- Characterization tests for legacy code

**Verification Commands**:
```bash
# Check coverage
npm test -- --coverage

# Coverage threshold enforcement
npx jest --coverage --coverageThreshold='{"global":{"lines":80}}'
```

### [R] Readable

- No functions > 50 lines
- Cyclomatic complexity < 10
- Clear naming conventions
- Self-documenting code

**Verification Commands**:
```bash
# Check complexity (eslint)
npx eslint --rule 'complexity: ["error", 10]'

# Function length
npx eslint --rule 'max-lines-per-function: ["error", 50]'
```

### [U] Unified

- Follows project architecture
- Consistent error handling
- Uses established patterns
- No duplicate code

**Verification Commands**:
```bash
# Check for duplication
npx jscpd --reporters "console" ./src

# Architecture compliance (custom)
npx madge --circular src/
```

### [S] Secured

- No hardcoded secrets
- Input validation present
- OWASP top 10 addressed
- Dependencies up to date

**Verification Commands**:
```bash
# Secret detection
npx gitleaks detect

# Dependency audit
npm audit --production

# SAST scan
npx semgrep --config=auto
```

### [T] Trackable

- Structured logging
- Error context preserved
- Audit trail where needed
- Observable operations

**Verification Patterns**:
```typescript
// Check for structured logging
logger.info('Operation completed', {
  operation: 'user_create',
  userId: user.id,
  duration: endTime - startTime
});

// Error context preserved
try {
  await operation();
} catch (error) {
  logger.error('Operation failed', {
    error: error.message,
    stack: error.stack,
    context: { userId, action }
  });
  throw error;
}
```

---

## Scoring System

```
Each principle: 0-1 (percentage compliance)

Scoring formula:
- Automated checks pass: 0.4
- Manual review criteria met: 0.3
- Documentation complete: 0.2
- Tests for principle: 0.1

Overall TRUST 5 score: Average of all principles
Target: 0.8+ (80% compliance)
```

## Score Interpretation

| Score | Grade | Recommendation |
|-------|-------|----------------|
| 0.9 - 1.0 | Excellent | Ready for production |
| 0.8 - 0.89 | Good | Minor improvements suggested |
| 0.6 - 0.79 | Fair | Address before major releases |
| < 0.6 | Poor | Significant work needed |

---

Version: 1.0.0
Source: jikime-workflow-verify SKILL.md
