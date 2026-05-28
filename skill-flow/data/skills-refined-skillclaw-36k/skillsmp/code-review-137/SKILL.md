---
name: code-review
description: Conduct comprehensive code reviews using software engineering best practices, clean code principles (SOLID, DRY, KISS, YAGNI), security checks, and performance analysis. Use when reviewing code changes, pull requests, new implementations, or entire files for quality, maintainability, security, and performance. Provides structured findings with severity levels and actionable recommendations.
---

# Code Review

## Overview

Perform systematic code reviews covering eight critical pillars: functionality, readability, security, performance, error handling, testing, standards, and architecture. Apply clean code principles and best practices to identify issues and provide actionable recommendations.

## When to Use This Skill

Trigger code review when:
- Reviewing pull requests or code changes
- Analyzing new implementations or features
- Auditing existing code for quality issues
- Checking code before production deployment
- Teaching or mentoring developers
- Investigating bugs or performance issues

## Review Workflow

### Step 1: Pre-Review Context

Before analyzing code, understand:
- **Purpose**: What problem does this code solve?
- **Scope**: Single file, feature, or entire module?
- **Tech stack**: Programming language, frameworks, libraries
- **Existing patterns**: Project conventions, architectural patterns

### Step 2: Eight-Pillar Analysis

Apply systematic checks across eight critical areas:

#### 1. Functionality
- **Logic correctness**: Does code work as intended?
- **Edge cases**: Handles null, empty, boundary conditions?
- **Requirements**: Meets stated objectives?
- **Business logic**: Correct calculations, flows, rules?

#### 2. Readability
- **Naming**: Clear, descriptive variable/function names?
- **Structure**: Logical organization, appropriate abstraction?
- **Comments**: Explains "why", not "what"?
- **Formatting**: Consistent indentation, spacing, style?
- **Complexity**: Functions small, single-purpose?

#### 3. Security
- **Input validation**: Sanitized, validated, escaped?
- **Injection prevention**: SQL, XSS, command injection safe?
- **Authentication**: Proper auth checks, session management?
- **Authorization**: Role-based access controls?
- **Data protection**: Encryption at rest/transit, no hardcoded secrets?
- **Dependencies**: Known vulnerabilities in packages?

See `references/security-checklist.md` for detailed security checks.

#### 4. Performance
- **Algorithm efficiency**: Appropriate Big O complexity?
- **Memory usage**: Leaks, excessive allocations, proper cleanup?
- **Data structures**: Optimal choices (HashMap vs Array)?
- **Database queries**: N+1 problems, missing indexes, proper joins?
- **Caching**: Opportunities for caching expensive operations?
- **Resource management**: Proper connection/file handle cleanup?

See `references/performance-checklist.md` for detailed performance checks.

#### 5. Error Handling
- **Exception handling**: Specific catches, no silent failures?
- **Validation**: Input validation with clear error messages?
- **Logging**: Appropriate log levels, useful context?
- **Recovery**: Graceful degradation, retry logic where appropriate?
- **User feedback**: Clear, actionable error messages?

#### 6. Testing
- **Coverage**: Critical paths tested?
- **Quality**: Tests clear, maintainable, independent?
- **Edge cases**: Boundary conditions, error scenarios tested?
- **Integration**: External dependencies mocked appropriately?
- **Reliability**: Tests deterministic, not flaky?

#### 7. Standards & Clean Code
Apply clean code principles:
- **SOLID principles**: See `references/principles.md`
- **DRY** (Don't Repeat Yourself): No code duplication?
- **KISS** (Keep It Simple): Avoids unnecessary complexity?
- **YAGNI** (You Aren't Gonna Need It): No premature optimization?
- **Project conventions**: Follows established patterns, linting rules?

#### 8. Architecture
- **Separation of concerns**: Clear responsibilities?
- **Coupling**: Loose coupling between modules?
- **Cohesion**: High cohesion within modules?
- **Scalability**: Handles growth, load increases?
- **Maintainability**: Easy to modify, extend, debug?

### Step 3: Structured Reporting

Organize findings by severity:

**Critical** - Must fix before merge:
- Security vulnerabilities
- Data loss risks
- Breaking changes
- Critical logic errors

**Major** - Should fix before merge:
- Performance issues
- Poor error handling
- Significant maintainability problems
- Violated clean code principles

**Minor** - Consider fixing:
- Style inconsistencies
- Minor optimizations
- Documentation gaps
- Naming improvements

**Format:**
```
## [SEVERITY] Category: Issue Title

**Location**: file.ts:42-56

**Issue**: Describe what's wrong

**Why it matters**: Explain impact

**Recommendation**: Specific fix with code example if helpful
```

### Step 4: Actionable Recommendations

For each finding, provide:
1. **Specific fix**: Not just "improve this", but "extract to method X"
2. **Code example**: Show before/after when helpful
3. **Rationale**: Explain why change improves code
4. **Priority**: Based on severity level

## Example Review

```
## [Critical] Security: SQL Injection Vulnerability

**Location**: userService.ts:145-148

**Issue**: User input directly concatenated into SQL query
```javascript
const query = `SELECT * FROM users WHERE username = '${username}'`;
```

**Why it matters**: Allows attackers to inject malicious SQL, compromising database security

**Recommendation**: Use parameterized queries
```javascript
const query = 'SELECT * FROM users WHERE username = ?';
const result = await db.execute(query, [username]);
```

---

## [Major] Clean Code: Violates Single Responsibility Principle

**Location**: OrderController.ts:23-89

**Issue**: Controller handles HTTP, business logic, database access, email notifications - four responsibilities

**Why it matters**: Changes to any concern require modifying this class, increasing bug risk and reducing testability

**Recommendation**: Extract into separate services
- `OrderService` for business logic
- `OrderRepository` for database
- `EmailService` for notifications
Controller only handles HTTP concerns
```

## Resources

### references/principles.md
Detailed explanation of clean code principles:
- SOLID principles with examples
- DRY, KISS, YAGNI guidelines
- Common code smells and anti-patterns

Load when reviewing architecture, design patterns, or code organization.

### references/security-checklist.md
Comprehensive security checks:
- Input validation patterns
- Injection prevention techniques
- Authentication/authorization best practices
- Encryption requirements
- Secret management

Load when reviewing user input handling, auth flows, or data protection.

### references/performance-checklist.md
Performance optimization checks:
- Algorithm complexity analysis
- Memory management patterns
- Database optimization techniques
- Caching strategies
- Profiling guidance

Load when reviewing performance-critical code or diagnosing slowness.

## Review Tips

1. **Start broad, then detailed**: Understand overall structure before line-by-line
2. **Be specific**: "Extract lines 42-56 to `validateUser()`" > "improve structure"
3. **Explain why**: Help developer learn, don't just list issues
4. **Prioritize**: Focus on critical/major issues first
5. **Balance**: Acknowledge good code, not just problems
6. **Context matters**: Consider project constraints, deadlines, tech debt
