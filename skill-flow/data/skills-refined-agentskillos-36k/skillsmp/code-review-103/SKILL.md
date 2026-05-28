---
name: code-review
description: Perform thorough code reviews focusing on security, performance, best practices, and maintainability. Use when reviewing PRs, checking code quality, or auditing existing code.
---

# Code Review

Systematic code review methodology for identifying issues, security vulnerabilities, and optimization opportunities.

## Review Phases

### Phase 1: Preparation

1. **Understand Context**
   - Read PR description and linked issues
   - Understand the feature/fix being implemented
   - Check if there are related changes in other PRs
   - Review the commit history for context

2. **Identify Standards**
   - Check project's coding standards
   - Review existing patterns in the codebase
   - Note any specific requirements (performance, security)

### Phase 2: Systematic Analysis

Work through each category methodically:

## Security Review

### Input Validation

```javascript
// BAD: No validation
app.post('/user', (req, res) => {
  db.query(`SELECT * FROM users WHERE id = ${req.body.id}`);
});

// GOOD: Parameterized + validated
app.post('/user', (req, res) => {
  const schema = z.object({ id: z.number().positive() });
  const { id } = schema.parse(req.body);
  db.query('SELECT * FROM users WHERE id = ?', [id]);
});
```

### Authentication & Authorization

```javascript
// BAD: Missing auth check
app.delete('/api/posts/:id', async (req, res) => {
  await Post.findByIdAndDelete(req.params.id);
});

// GOOD: Verify ownership
app.delete('/api/posts/:id', authenticate, async (req, res) => {
  const post = await Post.findById(req.params.id);
  if (post.authorId !== req.user.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  await post.delete();
});
```

### Security Checklist

- [ ] SQL/NoSQL injection prevented (parameterized queries)
- [ ] XSS prevented (output encoding, CSP headers)
- [ ] CSRF protection in place
- [ ] Sensitive data not logged or exposed
- [ ] API keys/secrets not hardcoded
- [ ] File uploads validated and sanitized
- [ ] Rate limiting on sensitive endpoints
- [ ] Proper error messages (no stack traces in production)

## Performance Review

### N+1 Query Detection

```javascript
// BAD: N+1 queries
const posts = await Post.find();
for (const post of posts) {
  const author = await User.findById(post.authorId); // Query per post!
}

// GOOD: Eager loading
const posts = await Post.find().populate('author');
```

### Memory & Resource Management

```javascript
// BAD: Memory leak - event listener not removed
useEffect(() => {
  window.addEventListener('resize', handleResize);
}, []);

// GOOD: Cleanup function
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

### Performance Checklist

- [ ] No N+1 queries (use eager loading)
- [ ] Expensive operations cached appropriately
- [ ] Database queries use proper indexes
- [ ] Large datasets paginated
- [ ] Async operations properly awaited
- [ ] No unnecessary re-renders (React)
- [ ] Memory leaks prevented (cleanup handlers)
- [ ] Heavy computations memoized or offloaded

## Code Quality Review

### Naming & Readability

```javascript
// BAD: Unclear names
const d = new Date();
const x = users.filter(u => u.a > 18);

// GOOD: Descriptive names
const currentDate = new Date();
const adultUsers = users.filter(user => user.age > 18);
```

### Error Handling

```javascript
// BAD: Swallowed errors
try {
  await saveData();
} catch (e) {}

// GOOD: Proper error handling
try {
  await saveData();
} catch (error) {
  logger.error('Failed to save data', { error, context });
  throw new AppError('Save failed', { cause: error });
}
```

### Code Quality Checklist

- [ ] Clear, descriptive naming conventions
- [ ] Functions are single-purpose (< 30 lines ideal)
- [ ] Cyclomatic complexity reasonable (< 10)
- [ ] No code duplication (DRY principle)
- [ ] Proper error handling throughout
- [ ] Edge cases considered
- [ ] Magic numbers/strings extracted to constants
- [ ] Comments explain "why", not "what"

## Design Patterns Review

### SOLID Principles

```javascript
// BAD: Violates Single Responsibility
class UserService {
  async createUser(data) { /* ... */ }
  async sendEmail(user) { /* ... */ }
  async generateReport() { /* ... */ }
}

// GOOD: Separated responsibilities
class UserService {
  async createUser(data) { /* ... */ }
}
class EmailService {
  async sendEmail(user) { /* ... */ }
}
class ReportService {
  async generateReport() { /* ... */ }
}
```

### Design Checklist

- [ ] Single Responsibility Principle followed
- [ ] Open/Closed Principle (extensible without modification)
- [ ] Dependencies injected, not hardcoded
- [ ] Appropriate abstraction levels
- [ ] Design patterns used correctly
- [ ] No over-engineering for current requirements

## Testing Review

### Test Coverage

```javascript
// BAD: Only happy path
it('creates user', async () => {
  const user = await createUser({ name: 'John' });
  expect(user.name).toBe('John');
});

// GOOD: Edge cases and errors
describe('createUser', () => {
  it('creates user with valid data', async () => {
    const user = await createUser({ name: 'John', email: 'john@test.com' });
    expect(user.name).toBe('John');
  });

  it('throws on duplicate email', async () => {
    await createUser({ name: 'John', email: 'john@test.com' });
    await expect(
      createUser({ name: 'Jane', email: 'john@test.com' })
    ).rejects.toThrow('Email already exists');
  });

  it('validates required fields', async () => {
    await expect(createUser({})).rejects.toThrow('Name is required');
  });
});
```

### Testing Checklist

- [ ] Unit tests for business logic
- [ ] Integration tests for API endpoints
- [ ] Edge cases covered
- [ ] Error scenarios tested
- [ ] Mocks used appropriately (not over-mocked)
- [ ] Tests are deterministic (no flaky tests)
- [ ] Test descriptions are clear

## Documentation Review

- [ ] Public APIs documented
- [ ] Complex logic explained
- [ ] README updated if needed
- [ ] Breaking changes noted
- [ ] Types/interfaces documented

## Review Output Format

Structure feedback as:

### Critical Issues (Must Fix)

Issues that block merging:
- Security vulnerabilities
- Data loss risks
- Breaking changes without migration
- Failing tests

### Warnings (Should Fix)

Issues that should be addressed:
- Performance concerns
- Code maintainability
- Missing error handling
- Incomplete tests

### Suggestions (Nice to Have)

Improvements for consideration:
- Refactoring opportunities
- Better naming
- Additional documentation
- Alternative approaches

### Positive Notes

What's done well:
- Good patterns followed
- Clean code
- Thorough testing
- Clear documentation

## Common Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| God Object | Class does too much | Split into focused classes |
| Spaghetti Code | Unclear flow | Extract functions, use patterns |
| Copy-Paste | Duplicated code | Extract shared utilities |
| Premature Optimization | Complex without need | Keep simple, optimize when needed |
| Magic Numbers | Unclear constants | Named constants |
| Callback Hell | Nested callbacks | async/await, Promises |
| Tight Coupling | Hard to test/change | Dependency injection |

## Language-Specific Checks

### JavaScript/TypeScript

- [ ] `===` used instead of `==`
- [ ] Proper TypeScript types (no `any` abuse)
- [ ] async/await error handling
- [ ] No prototype pollution risks
- [ ] ESLint/Prettier rules followed

### React

- [ ] Hooks rules followed
- [ ] Keys provided for lists
- [ ] useEffect dependencies correct
- [ ] No state mutations
- [ ] Proper component composition

### PHP/WordPress

- [ ] Escaping output (esc_html, esc_attr, etc.)
- [ ] Nonces for form submissions
- [ ] Capability checks for actions
- [ ] Prepared statements for queries
- [ ] WordPress coding standards followed

### Python

- [ ] Type hints used
- [ ] Context managers for resources
- [ ] Exception handling specific
- [ ] PEP 8 followed
- [ ] Requirements pinned
