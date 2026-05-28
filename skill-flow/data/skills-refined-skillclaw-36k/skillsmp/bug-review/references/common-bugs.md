# Common Bug Patterns

Detailed patterns for bugs by category.

## Null/Undefined Reference

### Unchecked Null Access

**Pattern**: Accessing properties on potentially null objects.

```javascript
// BUG
function getUserName(user) {
  return user.profile.name; // Crashes if user or profile is null
}

// SAFE
function getUserName(user) {
  return user?.profile?.name ?? 'Unknown';
}
```

**.NET**:
```csharp
// BUG
public string GetUserName(User user) {
  return user.Profile.Name; // NullReferenceException
}

// SAFE
public string GetUserName(User user) {
  return user?.Profile?.Name ?? "Unknown";
}
```

**Severity**: Major (crashes), Minor (causes undefined behavior)

### Null Return Values

**Pattern**: Functions that may return null without documentation.

```javascript
// DANGEROUS - caller doesn't know it can return null
function findUser(id) {
  return users.find(u => u.id === id); // undefined if not found
}

// Use later
const user = findUser(id);
console.log(user.name); // Crashes if user not found
```

**Severity**: Major

## Off-by-One Errors

### Array Index Errors

**Pattern**: Using wrong bounds in loops or array access.

```javascript
// BUG - includes non-existent index
for (let i = 0; i <= arr.length; i++) {
  console.log(arr[i]); // arr[arr.length] is undefined
}

// CORRECT
for (let i = 0; i < arr.length; i++) {
  console.log(arr[i]);
}
```

**Pattern**: Fence post errors in counting.

```javascript
// BUG - counts spaces, not words
function countWords(str) {
  return str.split(' ').length - 1;
}

// CORRECT
function countWords(str) {
  return str.trim().split(/\s+/).length;
}
```

**Severity**: Minor to Major

## Async/Promise Issues

### Unhandled Promise Rejection

**Pattern**: Promises without catch handlers.

```javascript
// BUG - unhandled rejection
async function loadData() {
  const data = await fetch('/api/data'); // May throw
  return data.json();
}
loadData(); // No .catch()

// SAFE
loadData().catch(err => console.error(err));
// Or use try/catch in the caller
```

**Severity**: Major

### Race Conditions

**Pattern**: State changed between await calls.

```javascript
// BUG - race condition
async function updateUser(id, data) {
  const user = await getUser(id);
  user.count += 1;
  await saveUser(user); // Another request may have updated count
}

// SAFE - atomic update
async function updateUser(id, data) {
  await db.query('UPDATE users SET count = count + 1 WHERE id = ?', [id]);
}
```

**Severity**: Major to Critical

### Floating Promises

**Pattern**: Async function called without await.

```javascript
// BUG - doesn't wait for save
function handleSubmit(data) {
  saveData(data); // Forgot await!
  showSuccess(); // Shows before save completes
}

// CORRECT
async function handleSubmit(data) {
  await saveData(data);
  showSuccess();
}
```

**Severity**: Major

## Type Coercion Issues

### Loose Equality Bugs

**Pattern**: Using == instead of === with unexpected coercion.

```javascript
// UNEXPECTED
0 == ''       // true
null == undefined  // true
[] == false   // true

// SAFE
0 === ''      // false
null === undefined  // false
[] === false  // false
```

**Severity**: Minor to Major

### String/Number Confusion

**Pattern**: Math on strings or comparisons with type mismatch.

```javascript
// BUG
const total = '10' + 5;  // '105' (string concat)
const sorted = [1, 10, 2].sort();  // [1, 10, 2] (string sort)

// CORRECT
const total = Number('10') + 5;  // 15
const sorted = [1, 10, 2].sort((a, b) => a - b);  // [1, 2, 10]
```

**Severity**: Major

## State Management

### Mutating Shared State

**Pattern**: Modifying objects that are used elsewhere.

```javascript
// BUG
function processItems(items) {
  items.sort(); // Mutates original array!
  return items.slice(0, 5);
}

// SAFE
function processItems(items) {
  return [...items].sort().slice(0, 5);
}
```

**Severity**: Major

### Stale Closure

**Pattern**: Closures capturing outdated values.

```javascript
// BUG - always logs initial count
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    setInterval(() => {
      console.log(count); // Always 0!
    }, 1000);
  }, []);
}

// CORRECT
useEffect(() => {
  setInterval(() => {
    console.log(countRef.current);
  }, 1000);
}, []);
```

**Severity**: Major

## Error Handling

### Swallowed Exceptions

**Pattern**: Catching errors without handling them.

```javascript
// BUG - error silently ignored
try {
  await saveData(data);
} catch (e) {
  // Empty catch
}

// PROPER
try {
  await saveData(data);
} catch (e) {
  logger.error('Failed to save:', e);
  throw e; // Or handle appropriately
}
```

**Severity**: Major

### Wrong Error Type Caught

**Pattern**: Catching too broad or wrong exceptions.

```javascript
// BUG - catches everything
try {
  JSON.parse(input);
} catch (e) {
  return null; // Also catches programmer errors!
}

// BETTER
try {
  JSON.parse(input);
} catch (e) {
  if (e instanceof SyntaxError) {
    return null;
  }
  throw e; // Re-throw unexpected errors
}
```

**Severity**: Minor to Major

## .NET Specific

### IDisposable Not Disposed

**Pattern**: Disposable objects not cleaned up.

```csharp
// BUG - connection may leak
var connection = new SqlConnection(connString);
connection.Open();
// ... use connection
// Missing: connection.Dispose()

// CORRECT
using var connection = new SqlConnection(connString);
connection.Open();
// Automatically disposed
```

**Severity**: Major

### Async Deadlock

**Pattern**: .Result or .Wait() on async code.

```csharp
// DEADLOCK in ASP.NET
public ActionResult Index() {
  var data = GetDataAsync().Result; // Deadlock!
  return View(data);
}

// CORRECT
public async Task<ActionResult> Index() {
  var data = await GetDataAsync();
  return View(data);
}
```

**Severity**: Critical

## Quick Reference

| Bug Type | Typical Severity | Detection |
|----------|-----------------|-----------|
| Null Reference | Major | Static analysis, optional chaining check |
| Off-by-One | Major | Loop bounds, array access |
| Unhandled Promise | Major | Missing await/catch |
| Race Condition | Critical | Concurrent state access |
| Empty Catch | Major | Catch blocks without logging/handling |
| IDisposable Leak | Major | Using statement check |
| Async Deadlock | Critical | .Result/.Wait() usage |
