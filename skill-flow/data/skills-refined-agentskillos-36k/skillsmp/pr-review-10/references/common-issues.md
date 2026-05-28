# Common Code Review Issues

Reference for: PR Review

Quick reference for frequently found issues in code reviews.

## Security

### Hardcoded Secrets
```javascript
// ❌ Bad
const API_KEY = "sk_live_abc123";

// ✓ Good
const API_KEY = process.env.API_KEY;
```

### SQL Injection
```javascript
// ❌ Bad
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✓ Good
const query = 'SELECT * FROM users WHERE id = $1';
db.query(query, [userId]);
```

### XSS Vulnerabilities
```jsx
// ❌ Bad
<div dangerouslySetInnerHTML={{__html: userInput}} />

// ✓ Good
<div>{DOMPurify.sanitize(userInput)}</div>
```

### Weak Password Requirements
```javascript
// ❌ Bad
if (password.length < 6) return false;

// ✓ Good
if (password.length < 12 || !/[A-Z]/.test(password) || !/[0-9]/.test(password)) {
  return false;
}
```

## Error Handling

### Swallowed Errors
```javascript
// ❌ Bad
try {
  await riskyOperation();
} catch (e) {
  // Silent failure
}

// ✓ Good
try {
  await riskyOperation();
} catch (error) {
  logger.error('Operation failed', { error, context });
  throw new OperationError('Failed to complete operation');
}
```

### Missing Null Checks
```javascript
// ❌ Bad
const name = user.profile.name.toUpperCase();

// ✓ Good
const name = user?.profile?.name?.toUpperCase() ?? 'Unknown';
```

### Unhandled Promise Rejections
```javascript
// ❌ Bad
async function loadData() {
  const data = await fetchData(); // Can reject
  return data;
}

// ✓ Good
async function loadData() {
  try {
    const data = await fetchData();
    return data;
  } catch (error) {
    logger.error('Failed to load data', { error });
    return null;
  }
}
```

## Performance

### N+1 Queries
```javascript
// ❌ Bad
for (const post of posts) {
  post.author = await User.findById(post.authorId);
}

// ✓ Good
const authorIds = posts.map(p => p.authorId);
const authors = await User.findByIds(authorIds);
const authorMap = new Map(authors.map(a => [a.id, a]));
posts.forEach(post => {
  post.author = authorMap.get(post.authorId);
});
```

### Missing Indexes
```javascript
// ❌ Bad: Querying without index
User.find({ email: 'user@example.com' }); // No index on email

// ✓ Good: Add index
// In migration:
await db.createIndex('users', { email: 1 });
```

### Unnecessary Re-renders
```jsx
// ❌ Bad
function Component({ data }) {
  const processed = expensiveOperation(data); // Runs every render
  return <div>{processed}</div>;
}

// ✓ Good
function Component({ data }) {
  const processed = useMemo(() => expensiveOperation(data), [data]);
  return <div>{processed}</div>;
}
```

## Logic Bugs

### Off-by-One Errors
```javascript
// ❌ Bad
for (let i = 0; i <= array.length; i++) {  // <= is wrong
  console.log(array[i]);
}

// ✓ Good
for (let i = 0; i < array.length; i++) {
  console.log(array[i]);
}
```

### Race Conditions
```javascript
// ❌ Bad
let counter = 0;
async function increment() {
  const current = counter;
  await someAsyncOperation();
  counter = current + 1; // Race condition
}

// ✓ Good
let counter = 0;
const lock = new AsyncLock();
async function increment() {
  await lock.acquire('counter', async () => {
    counter++;
  });
}
```

### Type Coercion Bugs
```javascript
// ❌ Bad
if (value == null) { // Matches both null and undefined

// ✓ Good
if (value === null) { // Only null
if (value === undefined) { // Only undefined
if (value == null) { // Explicitly want both (rare)
```

## Code Quality

### Magic Numbers
```javascript
// ❌ Bad
setTimeout(cleanup, 86400000);

// ✓ Good
const ONE_DAY_MS = 24 * 60 * 60 * 1000;
setTimeout(cleanup, ONE_DAY_MS);
```

### Deeply Nested Code
```javascript
// ❌ Bad
if (user) {
  if (user.isActive) {
    if (user.hasPermission) {
      if (!user.isBanned) {
        doSomething();
      }
    }
  }
}

// ✓ Good
if (!user) return;
if (!user.isActive) return;
if (!user.hasPermission) return;
if (user.isBanned) return;
doSomething();
```

### Poor Variable Names
```javascript
// ❌ Bad
const d = new Date();
const x = users.filter(u => u.a);

// ✓ Good
const currentDate = new Date();
const activeUsers = users.filter(user => user.isActive);
```

### Commented-Out Code
```javascript
// ❌ Bad
function process(data) {
  // const old = transform(data);
  // return old.map(x => x.value);
  return data.map(item => item.value);
}

// ✓ Good
function process(data) {
  return data.map(item => item.value);
}
// If you need history, use git
```

## TypeScript Issues

### Explicit Any
```typescript
// ❌ Bad
function process(data: any) {
  return data.value;
}

// ✓ Good
function process(data: { value: string }) {
  return data.value;
}
```

### Type Casting
```typescript
// ❌ Bad
const value = (data as User).name;

// ✓ Good: Type narrowing
if ('name' in data) {
  const value = data.name;
}
```

### Missing Return Type
```typescript
// ❌ Bad
async function fetchUser(id: string) {
  return await db.users.findById(id);
}

// ✓ Good
async function fetchUser(id: string): Promise<User | null> {
  return await db.users.findById(id);
}
```

## Testing

### Testing Implementation Details
```javascript
// ❌ Bad
expect(component.state.count).toBe(1);

// ✓ Good
expect(screen.getByText('Count: 1')).toBeInTheDocument();
```

### Brittle Selectors
```javascript
// ❌ Bad
await page.click('.MuiButton-root:nth-child(2)');

// ✓ Good
await page.click('[data-testid="submit-button"]');
```

### Missing Edge Cases
```javascript
// ❌ Bad: Only tests happy path
test('divides numbers', () => {
  expect(divide(10, 2)).toBe(5);
});

// ✓ Good: Tests edge cases
test('divides numbers', () => {
  expect(divide(10, 2)).toBe(5);
  expect(divide(10, 3)).toBeCloseTo(3.33);
  expect(() => divide(10, 0)).toThrow('Division by zero');
  expect(divide(0, 10)).toBe(0);
});
```

## Quick Reference

| Issue | Search Pattern | Severity |
|-------|---------------|----------|
| Hardcoded secrets | `grep -r "api_key.*=\|password.*="` | Critical |
| SQL injection | `grep -r "query.*+\|execute.*%"` | Critical |
| Console.log | `grep -r "console\\.log"` | Low |
| Any type | `grep -r ": any"` | Important |
| Type casting | `grep -r " as \|<.*>"` | Important |
| TODO | `grep -r "TODO\|FIXME"` | Varies |
