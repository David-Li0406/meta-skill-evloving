# Common Code Anti-Patterns

Patterns to watch for during code review.

## Logic Errors

### Silent Failures
```javascript
// Bad: Error swallowed silently
try {
  await saveData();
} catch (e) {
  // nothing
}

// Good: Error handled or propagated
try {
  await saveData();
} catch (e) {
  logger.error('Failed to save:', e);
  throw new SaveError('Data save failed', { cause: e });
}
```

### Unchecked Return Values
```python
# Bad: Return value ignored
file.write(data)

# Good: Check for errors
bytes_written = file.write(data)
if bytes_written != len(data):
    raise IOError("Incomplete write")
```

### Race Conditions
```javascript
// Bad: Check-then-act race condition
if (!cache.has(key)) {
  cache.set(key, await fetchData(key));
}
return cache.get(key);

// Good: Atomic operation
return cache.getOrSet(key, () => fetchData(key));
```

## Security Issues

### Command Injection
```python
# Bad: User input in shell command
os.system(f"grep {user_input} file.txt")

# Good: Use library functions or escape
import shlex
subprocess.run(["grep", shlex.quote(user_input), "file.txt"])
```

### SQL Injection
```javascript
// Bad: String concatenation
query(`SELECT * FROM users WHERE id = ${userId}`)

// Good: Parameterized query
query('SELECT * FROM users WHERE id = $1', [userId])
```

### Path Traversal
```python
# Bad: Direct path join
path = os.path.join(base_dir, user_filename)

# Good: Validate path stays within base
path = os.path.join(base_dir, user_filename)
if not os.path.realpath(path).startswith(os.path.realpath(base_dir)):
    raise SecurityError("Path traversal detected")
```

## Performance Issues

### N+1 Query Problem
```python
# Bad: Query in loop
for user in users:
    posts = db.query(f"SELECT * FROM posts WHERE user_id = {user.id}")

# Good: Batch query
user_ids = [u.id for u in users]
posts = db.query("SELECT * FROM posts WHERE user_id IN (%s)", user_ids)
```

### Unnecessary Work in Loops
```javascript
// Bad: Regex compiled in each iteration
for (const line of lines) {
  if (line.match(/pattern/)) { ... }
}

// Good: Compile once
const pattern = /pattern/;
for (const line of lines) {
  if (pattern.test(line)) { ... }
}
```

### Memory Leaks
```javascript
// Bad: Event listener never removed
element.addEventListener('click', handler);

// Good: Clean up on unmount
element.addEventListener('click', handler);
return () => element.removeEventListener('click', handler);
```

## Maintainability Issues

### Magic Numbers
```python
# Bad: Unexplained constant
if len(password) < 8:
    raise Error("Too short")

# Good: Named constant
MIN_PASSWORD_LENGTH = 8
if len(password) < MIN_PASSWORD_LENGTH:
    raise Error(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
```

### Deep Nesting
```javascript
// Bad: Deeply nested conditionals
if (user) {
  if (user.isActive) {
    if (user.hasPermission) {
      doSomething();
    }
  }
}

// Good: Early returns
if (!user) return;
if (!user.isActive) return;
if (!user.hasPermission) return;
doSomething();
```

### God Functions
```python
# Bad: Function doing too many things
def process_order(order):
    validate_order(order)
    calculate_totals(order)
    apply_discounts(order)
    check_inventory(order)
    process_payment(order)
    send_confirmation(order)
    update_analytics(order)

# Good: Single responsibility
def process_order(order):
    validated = validate_order(order)
    priced = calculate_order_total(validated)
    return submit_order(priced)
```

## Async Issues

### Unhandled Promise Rejections
```javascript
// Bad: Promise rejection unhandled
fetchData().then(processData);

// Good: Handle errors
fetchData()
  .then(processData)
  .catch(handleError);

// Or with async/await
try {
  const data = await fetchData();
  await processData(data);
} catch (error) {
  handleError(error);
}
```

### Missing Await
```javascript
// Bad: Forgot await
async function save() {
  validate();     // This is async!
  return store(); // May run before validation
}

// Good: Await async operations
async function save() {
  await validate();
  return store();
}
```

## Testing Anti-Patterns

### Testing Implementation, Not Behavior
```javascript
// Bad: Testing internal state
expect(component.state.isLoading).toBe(true);

// Good: Testing observable behavior
expect(screen.getByText('Loading...')).toBeInTheDocument();
```

### Flaky Tests
```javascript
// Bad: Timing-dependent
await sleep(100);
expect(result).toBe('done');

// Good: Wait for condition
await waitFor(() => expect(result).toBe('done'));
```
