# JavaScript Research

Comprehensive patterns and best practices for modern JavaScript development.

## ES2020+ Features

### Private Class Fields

```javascript
class BankAccount {
  #balance = 0;  // Private field

  deposit(amount) {
    if (amount > 0) this.#balance += amount;
  }

  get balance() {
    return this.#balance;
  }
}

const account = new BankAccount();
account.deposit(100);
console.log(account.balance);    // 100
console.log(account.#balance);   // SyntaxError
```

### Static Initialization Blocks

```javascript
class Config {
  static #instance;

  static {
    // Complex initialization logic
    this.#instance = new Config();
    this.#instance.load();
  }

  static getInstance() {
    return this.#instance;
  }
}
```

### Top-Level Await

```javascript
// In ES modules
const response = await fetch('/api/config');
export const config = await response.json();
```

### Logical Assignment Operators

```javascript
// ||= assigns if falsy
options.timeout ||= 5000;

// &&= assigns if truthy
user.name &&= user.name.trim();

// ??= assigns if nullish
config.retries ??= 3;
```

### Array Methods

```javascript
// at() - negative indexing
const last = array.at(-1);
const secondLast = array.at(-2);

// findLast / findLastIndex
const lastEven = [1, 2, 3, 4].findLast(n => n % 2 === 0);  // 4

// toSorted / toReversed / toSpliced (non-mutating)
const sorted = array.toSorted((a, b) => a - b);
const reversed = array.toReversed();
const spliced = array.toSpliced(1, 2, 'new');
```

### Object Methods

```javascript
// Object.hasOwn (preferred over hasOwnProperty)
if (Object.hasOwn(obj, 'property')) { }

// Object.groupBy
const grouped = Object.groupBy(users, user => user.role);
// { admin: [...], user: [...] }

// Object.fromEntries
const obj = Object.fromEntries([['a', 1], ['b', 2]]);
// { a: 1, b: 2 }
```

## Asynchronous Patterns

### Promise Combinators

```javascript
// Promise.all - all must succeed
const results = await Promise.all([p1, p2, p3]);

// Promise.allSettled - get all results regardless of success/failure
const results = await Promise.allSettled([p1, p2, p3]);
results.forEach(result => {
  if (result.status === 'fulfilled') {
    console.log(result.value);
  } else {
    console.error(result.reason);
  }
});

// Promise.race - first to settle wins
const fastest = await Promise.race([p1, p2, p3]);

// Promise.any - first to succeed wins (ignores rejections)
const firstSuccess = await Promise.any([p1, p2, p3]);
```

### AbortController

```javascript
const controller = new AbortController();
const { signal } = controller;

// Abort after timeout
setTimeout(() => controller.abort(), 5000);

try {
  const response = await fetch('/api/data', { signal });
  const data = await response.json();
} catch (error) {
  if (error.name === 'AbortError') {
    console.log('Request was aborted');
  }
}
```

### Async Iterators

```javascript
async function* fetchPages(baseUrl) {
  let page = 1;
  while (true) {
    const response = await fetch(`${baseUrl}?page=${page}`);
    const data = await response.json();
    if (data.items.length === 0) break;
    yield data.items;
    page++;
  }
}

for await (const items of fetchPages('/api/users')) {
  items.forEach(processUser);
}
```

## Functional Patterns

### Composition

```javascript
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x);
const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x);

const processUser = pipe(
  normalize,
  validate,
  transform,
  save
);
```

### Currying

```javascript
const curry = fn => {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return (...nextArgs) => curried.apply(this, [...args, ...nextArgs]);
  };
};

const add = curry((a, b, c) => a + b + c);
add(1)(2)(3);  // 6
add(1, 2)(3);  // 6
```

### Memoization

```javascript
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const expensiveOperation = memoize((n) => {
  // Complex calculation
  return n * n;
});
```

### Debounce and Throttle

```javascript
function debounce(fn, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

function throttle(fn, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}
```

## Data Structures

### Map vs Object

```javascript
// Use Map when:
// - Keys are not strings
// - Need to preserve insertion order
// - Frequent additions/deletions

const userSessions = new Map();
userSessions.set(userId, sessionData);
userSessions.get(userId);
userSessions.has(userId);
userSessions.delete(userId);
userSessions.size;

// Use Object when:
// - Keys are strings
// - Need JSON serialization
// - Simple key-value storage
```

### Set

```javascript
const unique = new Set([1, 2, 2, 3]);  // Set {1, 2, 3}
unique.add(4);
unique.has(2);  // true
unique.delete(2);

// Array deduplication
const dedupe = arr => [...new Set(arr)];
```

### WeakMap / WeakSet

```javascript
// Keys must be objects, allows garbage collection
const metadata = new WeakMap();

function process(obj) {
  if (!metadata.has(obj)) {
    metadata.set(obj, { processed: true, timestamp: Date.now() });
  }
  return metadata.get(obj);
}
// When obj is garbage collected, metadata entry is too
```

## Module Patterns

### Barrel Exports

```javascript
// index.js
export { UserService } from './user-service.js';
export { AuthService } from './auth-service.js';
export { default as config } from './config.js';

// Consumer
import { UserService, AuthService, config } from './services/index.js';
```

### Dynamic Imports

```javascript
// Code splitting
const module = await import('./heavy-module.js');

// Conditional loading
if (condition) {
  const { feature } = await import('./feature.js');
  feature();
}

// With error handling
try {
  const plugin = await import(`./plugins/${name}.js`);
} catch {
  console.warn(`Plugin ${name} not found`);
}
```

## Error Handling Patterns

### Error Cause

```javascript
try {
  await fetchData();
} catch (error) {
  throw new Error('Failed to load data', { cause: error });
}

// Access original error
catch (error) {
  console.error(error.message);  // 'Failed to load data'
  console.error(error.cause);    // Original error
}
```

### Result Pattern

```javascript
class Result {
  constructor(value, error) {
    this.value = value;
    this.error = error;
  }

  static ok(value) {
    return new Result(value, null);
  }

  static err(error) {
    return new Result(null, error);
  }

  isOk() { return this.error === null; }
  isErr() { return this.error !== null; }
}

async function safeFetch(url) {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return Result.ok(data);
  } catch (error) {
    return Result.err(error);
  }
}

const result = await safeFetch('/api/users');
if (result.isOk()) {
  processUsers(result.value);
} else {
  handleError(result.error);
}
```

## Performance Considerations

### Avoid Memory Leaks

```javascript
// BAD: Event listener not removed
element.addEventListener('click', handler);

// GOOD: Clean up
const controller = new AbortController();
element.addEventListener('click', handler, { signal: controller.signal });
// Later: controller.abort() removes all listeners

// BAD: Closure holding reference
function createHandler(largeData) {
  return () => console.log(largeData.length);
}

// GOOD: Extract what you need
function createHandler(dataLength) {
  return () => console.log(dataLength);
}
```

### Efficient Iterations

```javascript
// For large arrays, traditional for loop is fastest
for (let i = 0; i < arr.length; i++) { }

// for...of is clean and handles iterables
for (const item of arr) { }

// Avoid creating intermediate arrays
// BAD
arr.filter(x => x > 0).map(x => x * 2).reduce((a, b) => a + b, 0);

// GOOD: Single pass
arr.reduce((sum, x) => x > 0 ? sum + x * 2 : sum, 0);
```

## Security Considerations

### Input Validation

```javascript
// Validate and sanitize all inputs
function processUserInput(input) {
  if (typeof input !== 'string') {
    throw new TypeError('Input must be a string');
  }
  if (input.length > 1000) {
    throw new RangeError('Input too long');
  }
  return input.trim();
}
```

### Avoid eval and new Function

```javascript
// NEVER do this with user input
eval(userInput);                    // Code injection
new Function(userInput)();          // Code injection
setTimeout(userInput, 1000);        // Code injection if string

// Safe alternatives
JSON.parse(jsonString);             // For JSON data
```

### Prototype Pollution Prevention

```javascript
// Dangerous: Object from user input
const obj = JSON.parse(userInput);
if (obj.__proto__ || obj.constructor) {
  throw new Error('Prototype pollution attempt');
}

// Safer: Create null-prototype object
const safeObj = Object.create(null);
Object.assign(safeObj, JSON.parse(userInput));
```

## Testing Best Practices

### Test Structure

```javascript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create a user with valid data', async () => {
      // Arrange
      const userData = { name: 'Test', email: 'test@example.com' };

      // Act
      const user = await userService.createUser(userData);

      // Assert
      expect(user.id).toBeDefined();
      expect(user.name).toBe('Test');
    });

    it('should throw ValidationError for invalid email', async () => {
      const userData = { name: 'Test', email: 'invalid' };

      await expect(userService.createUser(userData))
        .rejects.toThrow(ValidationError);
    });
  });
});
```

### Mocking

```javascript
// Mock modules
jest.mock('./api-client', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: '1', name: 'Test' }),
}));

// Mock timers
jest.useFakeTimers();
jest.advanceTimersByTime(1000);

// Spy on methods
const spy = jest.spyOn(console, 'error').mockImplementation();
// ... test code
expect(spy).toHaveBeenCalledWith('error message');
spy.mockRestore();
```
