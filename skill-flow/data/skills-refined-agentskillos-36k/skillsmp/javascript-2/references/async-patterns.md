# JavaScript Async Patterns

## Promises

### Creating Promises

```javascript
// Basic promise
const promise = new Promise((resolve, reject) => {
  const result = doSomething();
  if (result.success) {
    resolve(result.data);
  } else {
    reject(new Error(result.error));
  }
});

// Promise.resolve/reject for immediate values
const resolved = Promise.resolve(42);
const rejected = Promise.reject(new Error('Failed'));

// Promisify callback-based functions
function readFileAsync(path) {
  return new Promise((resolve, reject) => {
    fs.readFile(path, 'utf8', (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}

// Node.js util.promisify
const { promisify } = require('util');
const readFile = promisify(fs.readFile);
```

### Chaining

```javascript
fetchUser(id)
  .then(user => fetchOrders(user.id))
  .then(orders => processOrders(orders))
  .then(result => console.log(result))
  .catch(error => console.error('Error:', error))
  .finally(() => cleanup());

// Return values propagate through chain
Promise.resolve(1)
  .then(x => x + 1)        // 2
  .then(x => x * 2)        // 4
  .then(x => console.log(x)); // logs 4
```

### Promise Combinators

```javascript
// Promise.all - wait for all, fail fast
const results = await Promise.all([
  fetchUser(1),
  fetchUser(2),
  fetchUser(3)
]);
// results = [user1, user2, user3]
// Rejects if ANY promise rejects

// Promise.allSettled - wait for all, never fail
const results = await Promise.allSettled([
  fetchUser(1),
  fetchUser(999)  // Might fail
]);
// results = [
//   { status: 'fulfilled', value: user1 },
//   { status: 'rejected', reason: Error }
// ]

// Promise.race - first to settle wins
const result = await Promise.race([
  fetchFromPrimary(),
  fetchFromBackup()
]);

// Promise.any - first to fulfill wins (ES2021)
const result = await Promise.any([
  fetchFromServer1(),
  fetchFromServer2(),
  fetchFromServer3()
]);
// Rejects only if ALL reject
```

## Async/Await

### Basic Usage

```javascript
async function fetchUserData(id) {
  try {
    const user = await fetchUser(id);
    const orders = await fetchOrders(user.id);
    return { user, orders };
  } catch (error) {
    console.error('Failed to fetch:', error);
    throw error;  // Re-throw or handle
  }
}

// Arrow function
const fetchUserData = async (id) => {
  const user = await fetchUser(id);
  return user;
};
```

### Parallel Execution

```javascript
// ❌ Sequential - slow
async function fetchAllSequential(ids) {
  const results = [];
  for (const id of ids) {
    results.push(await fetchItem(id));  // Waits each time
  }
  return results;
}

// ✅ Parallel - fast
async function fetchAllParallel(ids) {
  const promises = ids.map(id => fetchItem(id));
  return Promise.all(promises);
}

// ✅ Parallel with individual error handling
async function fetchAllSafe(ids) {
  const promises = ids.map(async id => {
    try {
      return await fetchItem(id);
    } catch {
      return null;  // Return null for failed items
    }
  });
  return Promise.all(promises);
}
```

### Controlled Concurrency

```javascript
// Limit concurrent operations
async function mapWithLimit(items, limit, fn) {
  const results = [];
  const executing = new Set();

  for (const item of items) {
    const promise = fn(item).then(result => {
      executing.delete(promise);
      return result;
    });

    executing.add(promise);
    results.push(promise);

    if (executing.size >= limit) {
      await Promise.race(executing);
    }
  }

  return Promise.all(results);
}

// Usage
const results = await mapWithLimit(urls, 5, fetchUrl);
```

## Error Handling

### Try/Catch Patterns

```javascript
// Basic try/catch
async function safeFetch(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    if (error.name === 'AbortError') {
      console.log('Request aborted');
    } else {
      console.error('Fetch failed:', error);
    }
    throw error;
  }
}

// Wrapper for cleaner handling
async function to(promise) {
  try {
    const data = await promise;
    return [null, data];
  } catch (error) {
    return [error, null];
  }
}

// Usage
const [error, user] = await to(fetchUser(id));
if (error) {
  // Handle error
}
```

### Error Recovery

```javascript
// Retry with backoff
async function fetchWithRetry(url, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fetch(url);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(Math.pow(2, i) * 1000);  // Exponential backoff
    }
  }
}

// Fallback chain
async function fetchWithFallback(primaryUrl, fallbackUrl) {
  try {
    return await fetch(primaryUrl);
  } catch {
    return await fetch(fallbackUrl);
  }
}
```

## Async Iteration

### For-await-of

```javascript
async function* asyncGenerator() {
  for (let i = 0; i < 3; i++) {
    yield await fetchItem(i);
  }
}

// Consuming async generator
for await (const item of asyncGenerator()) {
  console.log(item);
}

// With streams
async function processStream(readable) {
  for await (const chunk of readable) {
    process(chunk);
  }
}
```

### AsyncIterator Protocol

```javascript
const asyncIterable = {
  [Symbol.asyncIterator]() {
    let i = 0;
    return {
      async next() {
        if (i < 3) {
          const value = await fetchItem(i++);
          return { value, done: false };
        }
        return { done: true };
      }
    };
  }
};

for await (const item of asyncIterable) {
  console.log(item);
}
```

## Cancellation

### AbortController

```javascript
// Create controller
const controller = new AbortController();
const { signal } = controller;

// Pass to fetch
fetch(url, { signal })
  .then(response => response.json())
  .catch(error => {
    if (error.name === 'AbortError') {
      console.log('Fetch cancelled');
    }
  });

// Cancel after timeout
setTimeout(() => controller.abort(), 5000);

// Or cancel manually
cancelButton.onclick = () => controller.abort();
```

### AbortSignal.timeout (Modern)

```javascript
// Built-in timeout signal
try {
  const response = await fetch(url, {
    signal: AbortSignal.timeout(5000)
  });
} catch (error) {
  if (error.name === 'TimeoutError') {
    console.log('Request timed out');
  }
}

// Combine signals
const controller = new AbortController();
const timeoutSignal = AbortSignal.timeout(5000);

const response = await fetch(url, {
  signal: AbortSignal.any([controller.signal, timeoutSignal])
});
```

### Custom Cancellable Operations

```javascript
function cancellableOperation(signal) {
  return new Promise((resolve, reject) => {
    // Check if already aborted
    if (signal?.aborted) {
      reject(signal.reason);
      return;
    }

    // Listen for abort
    signal?.addEventListener('abort', () => {
      cleanup();
      reject(signal.reason);
    });

    // Do work
    doAsyncWork().then(resolve).catch(reject);
  });
}
```

## Common Patterns

### Debounce

```javascript
function debounce(fn, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

// Usage: Only search after user stops typing
const debouncedSearch = debounce(search, 300);
input.addEventListener('input', e => debouncedSearch(e.target.value));
```

### Throttle

```javascript
function throttle(fn, limit) {
  let inThrottle;
  return function (...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Usage: Limit scroll handler
window.addEventListener('scroll', throttle(handleScroll, 100));
```

### Singleton Promise

```javascript
// Ensure only one request at a time
let pendingRequest = null;

async function fetchOnce(url) {
  if (pendingRequest) {
    return pendingRequest;
  }

  pendingRequest = fetch(url)
    .then(r => r.json())
    .finally(() => {
      pendingRequest = null;
    });

  return pendingRequest;
}
```

### Queue

```javascript
class AsyncQueue {
  constructor(concurrency = 1) {
    this.concurrency = concurrency;
    this.running = 0;
    this.queue = [];
  }

  async push(task) {
    return new Promise((resolve, reject) => {
      this.queue.push({ task, resolve, reject });
      this.process();
    });
  }

  async process() {
    while (this.running < this.concurrency && this.queue.length > 0) {
      const { task, resolve, reject } = this.queue.shift();
      this.running++;

      try {
        resolve(await task());
      } catch (error) {
        reject(error);
      } finally {
        this.running--;
        this.process();
      }
    }
  }
}

// Usage
const queue = new AsyncQueue(3);
urls.forEach(url => queue.push(() => fetch(url)));
```

## Anti-Patterns

```javascript
// ❌ Mixing callbacks and promises
fetchUser(id, (err, user) => {
  fetchOrders(user.id).then(...)  // Confusing
});

// ❌ Unnecessary async
async function getValue() {
  return 42;  // Don't need async for sync values
}

// ❌ await in a loop when parallel is possible
for (const id of ids) {
  await processItem(id);  // Sequential when could be parallel
}

// ❌ Swallowing errors
try {
  await riskyOperation();
} catch {
  // Silent failure - bad!
}

// ❌ Not handling promise rejection
fetchData();  // Unhandled rejection if it fails

// ✅ Handle it
fetchData().catch(console.error);
// or
await fetchData();
```
