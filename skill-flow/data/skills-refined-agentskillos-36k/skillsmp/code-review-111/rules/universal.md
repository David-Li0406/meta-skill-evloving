# Universal Code Review Rules

These rules apply to **all languages**. Check every file against these categories.

---

## 1. Naming

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| Descriptive names | Warning | Names should reveal intent (`userCount` not `n`) |
| No single-letter variables | Warning | Except loop indices (`i`, `j`) or lambdas |
| No abbreviations | Info | `customer` not `cust`, `configuration` not `cfg` |
| Consistent casing | Warning | Follow language convention (camelCase, snake_case) |
| Boolean naming | Info | Should read as question: `isValid`, `hasPermission`, `canEdit` |
| No type prefixes | Info | `users` not `arrUsers`, `name` not `strName` |

### Check For

- Variables named `temp`, `data`, `result`, `val`, `item` without context
- Functions named `process`, `handle`, `do`, `manage` without specificity
- Classes/types with generic names like `Manager`, `Helper`, `Utils`, `Service` without domain context

---

## 2. Functions

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| Single responsibility | Warning | One function = one task |
| Length limit | Warning | Ideal: <20 lines, Max: 50 lines |
| Parameter count | Warning | Max 3-4 parameters; use objects for more |
| No side effects | Info | Pure functions when possible |
| Early returns | Info | Guard clauses reduce nesting |
| Verb naming | Info | Functions do things: `calculateTotal`, `validateInput` |

### Check For

- Functions doing multiple unrelated things
- Deeply nested code (>3 levels)
- Functions with boolean parameters that change behavior (split into two functions)
- God functions that do everything

---

## 3. Error Handling

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| No silent failures | Critical | Never swallow errors without logging |
| Specific error types | Warning | Use/create specific error classes |
| Fail fast | Warning | Validate inputs early |
| Graceful degradation | Info | Provide fallbacks where appropriate |
| Error context | Warning | Include relevant info in error messages |
| No generic catches | Warning | Avoid catching all exceptions blindly |

### Check For

```
// BAD: Silent failure
try {
  doSomething();
} catch (e) {
  // nothing
}

// BAD: Generic message
throw new Error("Something went wrong");

// BAD: Catch-all
catch (Exception e) { ... }
```

### Look For

- Empty catch blocks
- `catch (e) { console.log(e) }` without re-throw or recovery
- Error messages without context (file, line, input values)
- Missing error handling on async operations

---

## 4. Security

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| No hardcoded secrets | Critical | API keys, passwords, tokens in code |
| Input validation | Critical | Validate all external input |
| SQL injection | Critical | Use parameterized queries |
| XSS prevention | Critical | Sanitize user content before display |
| Path traversal | Critical | Validate file paths |
| Auth checks | Critical | Verify permissions before actions |

### Check For

- Strings that look like API keys, passwords, or tokens
- User input used directly in queries, commands, or file paths
- `eval()`, `exec()`, or dynamic code execution with user input
- Missing authentication/authorization checks
- Sensitive data in logs or error messages

### Red Flags

```
// Hardcoded secret
const API_KEY = "sk-abc123...";

// SQL injection
query("SELECT * FROM users WHERE id = " + userId);

// Command injection
exec("ls " + userInput);

// Path traversal
readFile("/uploads/" + filename);
```

See [checklists/security.md](../checklists/security.md) for comprehensive security checklist.

---

## 5. Performance

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| Avoid N+1 queries | Warning | Batch database calls |
| No unnecessary loops | Warning | O(n) when O(1) is possible |
| Lazy loading | Info | Load data only when needed |
| Caching | Info | Cache expensive computations |
| Memory leaks | Warning | Clean up subscriptions, listeners, timers |
| Pagination | Info | Don't load unbounded data |

### Check For

- Database queries inside loops
- Loading entire collections when only a subset is needed
- Missing pagination on list endpoints
- Repeated calculations that could be cached
- Event listeners or subscriptions without cleanup

### Red Flags

```
// N+1 query
for (const user of users) {
  const orders = await db.query("SELECT * FROM orders WHERE user_id = ?", user.id);
}

// Unbounded data
const allUsers = await db.query("SELECT * FROM users");

// Missing cleanup
useEffect(() => {
  const interval = setInterval(tick, 1000);
  // No cleanup!
}, []);
```

See [checklists/performance.md](../checklists/performance.md) for comprehensive performance checklist.

---

## 6. Maintainability

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| DRY | Warning | Don't Repeat Yourself (but avoid premature abstraction) |
| Single source of truth | Warning | One place for each piece of knowledge |
| Low coupling | Info | Minimize dependencies between modules |
| High cohesion | Info | Related code stays together |
| SOLID principles | Info | Apply where appropriate |
| Magic numbers | Warning | Use named constants |

### Check For

- Copy-pasted code blocks (3+ similar blocks = refactor)
- Hard-coded values without explanation
- Circular dependencies
- God objects/classes that know too much
- Feature envy (class using another class's data excessively)

### Red Flags

```
// Magic numbers
if (status === 3) { ... }
setTimeout(fn, 86400000);

// Duplication
function validateEmail(email) { ... }
function checkEmail(email) { /* same logic */ }

// Feature envy
function process(order) {
  const tax = order.items.reduce(...) * order.taxRate * order.region.taxMultiplier;
  // Should be order.calculateTax()
}
```

---

## 7. Testing

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| Edge cases | Warning | Test boundaries, nulls, empty inputs |
| Isolation | Warning | Tests shouldn't depend on each other |
| Clear assertions | Info | One concept per test |
| Descriptive names | Info | Test name describes scenario and expectation |
| No test logic | Warning | Tests should be straightforward |
| Mock boundaries | Info | Mock external services, not internal logic |

### Check For

- Tests without assertions
- Tests with multiple unrelated assertions
- Shared mutable state between tests
- Tests that only work in sequence
- Flaky tests (pass/fail inconsistently)

### Red Flags

```
// No assertion
test("creates user", () => {
  createUser({ name: "test" });
});

// Multiple concerns
test("user flow", () => {
  const user = createUser();
  expect(user.id).toBeDefined();
  const order = createOrder(user);
  expect(order.total).toBe(100);
  // Too many things!
});

// Test logic
test("calculates correctly", () => {
  for (const i of [1, 2, 3]) {
    expect(calculate(i)).toBe(i * 2);
  }
});
```

---

## 8. Documentation

### Rules

| Rule | Severity | Description |
|------|----------|-------------|
| Complex logic explained | Warning | Non-obvious code needs comments |
| Public APIs documented | Info | Exported functions/classes need docs |
| No obvious comments | Info | Don't comment what code clearly shows |
| Update with code | Warning | Stale comments are worse than none |
| README accuracy | Info | Matches actual setup/usage |

### Check For

- Outdated comments that don't match the code
- Missing documentation on public interfaces
- Comments explaining "what" instead of "why"
- TODO/FIXME comments older than 6 months (estimate from git)

### Good vs Bad

```
// BAD: Obvious
// Increment counter
counter++;

// BAD: Outdated
// Returns user or null
function getUser() { throw new Error(); }

// GOOD: Explains why
// Use binary search since users are pre-sorted by ID
const user = binarySearch(users, targetId);

// GOOD: Documents edge case
// Empty array returns 0, not undefined, for backward compatibility
```

---

## Summary Checklist

Before completing review, ensure you've checked:

- [ ] All names are descriptive and follow conventions
- [ ] Functions are focused and reasonably sized
- [ ] Errors are handled, logged, and informative
- [ ] No security vulnerabilities (secrets, injection, validation)
- [ ] No obvious performance issues (N+1, unbounded queries)
- [ ] Code is DRY without being over-abstracted
- [ ] Tests cover edge cases and are isolated
- [ ] Complex logic is documented
