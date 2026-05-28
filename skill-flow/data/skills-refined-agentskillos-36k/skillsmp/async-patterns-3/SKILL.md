---
name: async-patterns
description: TypeScript async/await and Promise patterns. Prevent common async mistakes, optimize concurrency, and handle promise rejections correctly.
priority: critical
rule_count: 10
sources:
  - "You Don't Know JS: Async & Performance (Kyle Simpson)"
  - "Node.js Best Practices (goldbergyoni)"
  - "JavaScript: The Definitive Guide (David Flanagan)"
---

# Async Patterns - TypeScript Best Practices

Master async/await, promises, and concurrent operations to build reliable async code.

## When to Use

- Reviewing async/await code
- Optimizing API calls and I/O operations
- Debugging promise-related issues
- Implementing concurrent workflows
- Handling timeouts and cancellation

**Trigger Phrases:**
- "Review async code"
- "Optimize async operations"
- "Fix promise handling"
- "Check concurrent execution"

## Rules Overview

### Critical (3 rules)
Prevent async bugs and unhandled rejections:

1. **critical-promise-not-awaited** - Always await promises or handle with `.then()`
2. **critical-async-without-await** - `async` functions must use `await`
3. **critical-promise-constructor-anti** - Avoid `new Promise()` when unnecessary

### High Priority (4 rules)
Optimize performance and reliability:

4. **high-parallel-sequential-confusion** - Use `Promise.all()` for parallel operations
5. **high-promise-race-timeout** - Implement timeouts with `Promise.race()`
6. **high-async-forEach** - Don't use `forEach()` with async functions
7. **high-promise-chaining** - Prefer async/await over `.then()` chains

### Medium Priority (3 rules)
Code quality improvements:

8. **medium-concurrent-limit** - Limit concurrent operations with pooling
9. **medium-promise-allsettled** - Use `Promise.allSettled()` for fault tolerance
10. **medium-async-iife** - Use top-level await or async IIFE correctly

---

## Rule Details

### 1. critical-promise-not-awaited

**Why it matters:** Forgotten `await` causes promises to execute but results are lost, leading to race conditions.

**Detection:**
- Look for promise-returning functions called without `await`
- Check for `.then()` without `.catch()`
- Search for floating promises in void contexts

**❌ Incorrect:**
```typescript
async function updateUser(id: string, data: UserData) {
  validateData(data); // Forgot await! Promise ignored
  const user = await db.users.find(id);
  user.update(data); // Forgot await! Update might not complete
  return user;
}

async function validateData(data: UserData): Promise<void> {
  // Async validation...
}
```

**✅ Correct:**
```typescript
async function updateUser(id: string, data: UserData) {
  await validateData(data); // Wait for validation
  const user = await db.users.find(id);
  await user.update(data); // Wait for update
  return user;
}

// Or handle explicitly if fire-and-forget is intentional
async function logEvent(event: Event) {
  saveToDatabase(event).catch(err => {
    logger.error('Failed to save event', err);
  });
}
```

**Impact:** CRITICAL - Prevents race conditions and data loss

**Reference:** You Don't Know JS: Promises

---

### 2. critical-async-without-await

**Why it matters:** `async` keyword without `await` is misleading and adds unnecessary overhead.

**Detection:**
- Find `async` functions with no `await` keyword
- Check for synchronous code in async functions
- Look for unnecessary async wrappers

**❌ Incorrect:**
```typescript
async function calculateTotal(items: Item[]): Promise<number> {
  // No await! Should not be async
  return items.reduce((sum, item) => sum + item.price, 0);
}

async function getConfig(): Promise<Config> {
  // Synchronous return wrapped in Promise unnecessarily
  return { apiUrl: process.env.API_URL };
}
```

**✅ Correct:**
```typescript
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

function getConfig(): Config {
  return { apiUrl: process.env.API_URL };
}

// Only use async when actually awaiting
async function loadConfig(): Promise<Config> {
  const data = await fs.readFile('config.json', 'utf8');
  return JSON.parse(data);
}
```

**Impact:** HIGH - Removes misleading code and overhead

**Reference:** MDN: async function

---

### 3. critical-promise-constructor-anti

**Why it matters:** `new Promise()` is rarely needed and often indicates promise anti-patterns.

**Detection:**
- Look for `new Promise((resolve, reject) => ...)`
- Check for wrapping existing promises
- Search for manual promise creation

**❌ Incorrect:**
```typescript
// Anti-pattern: Wrapping existing promise
function getUser(id: string): Promise<User> {
  return new Promise((resolve, reject) => {
    db.users.find(id)
      .then(user => resolve(user))
      .catch(err => reject(err));
  });
}

// Anti-pattern: Wrapping callback when promisify exists
function readFileAsync(path: string): Promise<string> {
  return new Promise((resolve, reject) => {
    fs.readFile(path, 'utf8', (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}
```

**✅ Correct:**
```typescript
// Just return the promise directly
async function getUser(id: string): Promise<User> {
  return db.users.find(id);
}

// Use util.promisify for callbacks
import { promisify } from 'util';
const readFileAsync = promisify(fs.readFile);

// Only use new Promise for true async bridging
function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

**Impact:** HIGH - Simplifies code and avoids subtle bugs

**Reference:** You Don't Know JS: Promise Anti-Patterns

---

### 4. high-parallel-sequential-confusion

**Why it matters:** Sequential execution when parallel is possible wastes time.

**Detection:**
- Look for multiple awaits that don't depend on each other
- Check for independent API calls done sequentially
- Search for loops with await inside

**❌ Incorrect:**
```typescript
async function loadUserData(userId: string) {
  // Sequential: ~3 seconds total if each takes 1s
  const user = await db.users.find(userId);
  const posts = await db.posts.findByUser(userId);
  const comments = await db.comments.findByUser(userId);
  return { user, posts, comments };
}
```

**✅ Correct:**
```typescript
async function loadUserData(userId: string) {
  // Parallel: ~1 second total
  const [user, posts, comments] = await Promise.all([
    db.users.find(userId),
    db.posts.findByUser(userId),
    db.comments.findByUser(userId)
  ]);
  return { user, posts, comments };
}

// When there are dependencies
async function loadUserWithPosts(userId: string) {
  const user = await db.users.find(userId); // Must wait
  const posts = await db.posts.findByUser(user.id); // Depends on user
  return { user, posts };
}
```

**Impact:** HIGH - Significant performance improvement

**Reference:** JavaScript: The Definitive Guide, Async

---

### 5. high-promise-race-timeout

**Why it matters:** Operations without timeouts can hang indefinitely.

**Detection:**
- Check for network calls without timeout
- Look for missing timeout configuration
- Search for infinite wait scenarios

**❌ Incorrect:**
```typescript
async function fetchData(url: string) {
  // No timeout! Might hang forever
  const response = await fetch(url);
  return response.json();
}
```

**✅ Correct:**
```typescript
function timeout(ms: number): Promise<never> {
  return new Promise((_, reject) => {
    setTimeout(() => reject(new Error('Timeout')), ms);
  });
}

async function fetchWithTimeout(url: string, timeoutMs: number = 5000) {
  const response = await Promise.race([
    fetch(url),
    timeout(timeoutMs)
  ]);
  return response.json();
}

// Or use AbortController (modern)
async function fetchWithAbort(url: string, timeoutMs: number = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  
  try {
    const response = await fetch(url, { signal: controller.signal });
    return await response.json();
  } finally {
    clearTimeout(timeoutId);
  }
}
```

**Impact:** HIGH - Prevents hanging operations

**Reference:** MDN: Promise.race()

---

### 6. high-async-forEach

**Why it matters:** `forEach` doesn't wait for async callbacks, causing unexpected behavior.

**Detection:**
- Look for `array.forEach(async item => ...)`
- Check for async callbacks in forEach
- Search for await inside forEach

**❌ Incorrect:**
```typescript
async function processUsers(users: User[]) {
  users.forEach(async user => {
    await updateUser(user); // Won't wait!
  });
  console.log('Done'); // Prints before updates complete!
}
```

**✅ Correct:**
```typescript
// Sequential processing
async function processUsersSequential(users: User[]) {
  for (const user of users) {
    await updateUser(user);
  }
  console.log('Done'); // All updates complete
}

// Parallel processing
async function processUsersParallel(users: User[]) {
  await Promise.all(users.map(user => updateUser(user)));
  console.log('Done'); // All updates complete
}

// Or use for-await-of for async iterables
async function processStream(iterable: AsyncIterable<User>) {
  for await (const user of iterable) {
    await updateUser(user);
  }
}
```

**Impact:** HIGH - Fixes subtle async bugs

**Reference:** Node.js Best Practices: Async Iteration

---

### 7. high-promise-chaining

**Why it matters:** Long `.then()` chains are harder to read than async/await.

**Detection:**
- Look for 3+ chained `.then()` calls
- Check for nested `.then()` callbacks
- Search for error handling in chains

**❌ Incorrect:**
```typescript
function loadAndProcess(userId: string) {
  return db.users.find(userId)
    .then(user => {
      return db.posts.findByUser(user.id);
    })
    .then(posts => {
      return posts.map(post => ({
        ...post,
        wordCount: post.content.split(' ').length
      }));
    })
    .then(enrichedPosts => {
      return db.posts.saveMany(enrichedPosts);
    })
    .catch(err => {
      logger.error('Processing failed', err);
      throw err;
    });
}
```

**✅ Correct:**
```typescript
async function loadAndProcess(userId: string) {
  try {
    const user = await db.users.find(userId);
    const posts = await db.posts.findByUser(user.id);
    
    const enrichedPosts = posts.map(post => ({
      ...post,
      wordCount: post.content.split(' ').length
    }));
    
    return await db.posts.saveMany(enrichedPosts);
  } catch (err) {
    logger.error('Processing failed', err);
    throw err;
  }
}
```

**Impact:** MEDIUM-HIGH - Improves readability

**Reference:** You Don't Know JS: Async Patterns

---

### 8. medium-concurrent-limit

**Why it matters:** Unbounded concurrency can overwhelm resources.

**Detection:**
- Look for `Promise.all()` with large arrays
- Check for parallel API calls without limits
- Search for resource-intensive parallel operations

**❌ Incorrect:**
```typescript
async function processAllUsers(userIds: string[]) {
  // If userIds has 10,000 items, creates 10,000 concurrent requests!
  const results = await Promise.all(
    userIds.map(id => expensiveOperation(id))
  );
  return results;
}
```

**✅ Correct:**
```typescript
async function processWithLimit<T, R>(
  items: T[],
  fn: (item: T) => Promise<R>,
  concurrency: number = 10
): Promise<R[]> {
  const results: R[] = [];
  const executing: Promise<void>[] = [];
  
  for (const item of items) {
    const promise = fn(item).then(result => {
      results.push(result);
    });
    
    executing.push(promise);
    
    if (executing.length >= concurrency) {
      await Promise.race(executing);
      executing.splice(executing.findIndex(p => p === promise), 1);
    }
  }
  
  await Promise.all(executing);
  return results;
}

async function processAllUsers(userIds: string[]) {
  // Max 10 concurrent operations
  const results = await processWithLimit(
    userIds,
    id => expensiveOperation(id),
    10
  );
  return results;
}
```

**Impact:** MEDIUM - Prevents resource exhaustion

**Reference:** Node.js Best Practices: Concurrency Control

---

### 9. medium-promise-allsettled

**Why it matters:** `Promise.all()` fails fast - one rejection fails all. Sometimes you need all results.

**Detection:**
- Look for `Promise.all()` where individual failures are acceptable
- Check for try-catch around each promise
- Search for independent operations that should not fail together

**❌ Incorrect:**
```typescript
async function sendNotifications(users: User[]) {
  // One failure stops all notifications!
  await Promise.all(
    users.map(user => sendEmail(user.email))
  );
}

// Or wrapping each to avoid fail-fast
async function sendNotificationsSafe(users: User[]) {
  await Promise.all(
    users.map(async user => {
      try {
        await sendEmail(user.email);
      } catch (err) {
        logger.error('Email failed', { user, err });
      }
    })
  );
}
```

**✅ Correct:**
```typescript
async function sendNotifications(users: User[]) {
  const results = await Promise.allSettled(
    users.map(user => sendEmail(user.email))
  );
  
  const successful = results.filter(r => r.status === 'fulfilled').length;
  const failed = results.filter(r => r.status === 'rejected');
  
  logger.info(`Sent ${successful} emails, ${failed.length} failed`);
  
  // Log individual failures
  failed.forEach((result, i) => {
    if (result.status === 'rejected') {
      logger.error('Email failed', {
        user: users[i],
        error: result.reason
      });
    }
  });
}
```

**Impact:** MEDIUM - Improves fault tolerance

**Reference:** MDN: Promise.allSettled()

---

### 10. medium-async-iife

**Why it matters:** Top-level await is limited; async IIFE needs care.

**Detection:**
- Look for misused async IIFE
- Check for missing error handling
- Search for unnecessary wrapping

**❌ Incorrect:**
```typescript
// File-level code with async IIFE and no error handling
(async () => {
  const config = await loadConfig();
  startServer(config);
})(); // Silent failures!

// Unnecessary wrapping
(async () => {
  return await getData();
})().then(data => console.log(data));
```

**✅ Correct:**
```typescript
// Proper async IIFE with error handling
(async () => {
  try {
    const config = await loadConfig();
    await startServer(config);
  } catch (error) {
    logger.error('Startup failed', error);
    process.exit(1);
  }
})();

// Or use top-level await (ES2022+)
const config = await loadConfig();
await startServer(config);

// When IIFE needed, keep it simple
const data = await (async () => {
  return await getData();
})();
console.log(data);
```

**Impact:** LOW-MEDIUM - Prevents silent failures

**Reference:** MDN: IIFE, Top-level await

---

## Usage Examples

**Review async function:**
```
Check this async code for promise handling issues
```

**Optimize performance:**
```
Find sequential operations that could be parallel
```

**Debug timeout issues:**
```
Add timeouts to these API calls
```

## Summary

Async patterns ensure:
- ✅ All promises awaited or handled
- ✅ Parallel execution where possible
- ✅ Timeouts prevent hanging
- ✅ Proper forEach alternatives
- ✅ Fault-tolerant concurrent operations
- ✅ Readable async/await over chains

Master these patterns to build reliable async applications.
