---
name: error-handling
description: TypeScript/JavaScript error handling best practices. Ensures proper error propagation, typed errors, and async error handling.
priority: critical
rule_count: 7
sources:
  - "You Don't Know JS - Async & Performance (Kyle Simpson)"
  - "Node.js Best Practices (goldbergyoni)"
  - "Effective TypeScript (Dan Vanderkam)"
---

# Error Handling - TypeScript Best Practices

Proper error handling prevents silent failures, improves debugging, and ensures reliability.

## When to Use

- Reviewing async/await error handling
- Checking promise rejection handling  
- Auditing error propagation chains
- Implementing custom error types
- Debugging production errors

**Trigger Phrases:**
- "Review error handling"
- "Check for unhandled promises"
- "Audit error propagation"
- "Find error swallowing"

## Rules Overview

### Critical (3 rules)
Prevent silent failures and debugging nightmares:

1. **critical-error-swallowing** - Never catch and ignore errors
2. **critical-unhandled-rejection** - Handle all promise rejections
3. **critical-throw-non-error** - Only throw Error objects

### High Priority (3 rules)
Improve error clarity and debugging:

4. **high-error-context** - Include context in error messages
5. **high-custom-error-types** - Use typed error classes
6. **high-async-try-catch** - Proper error handling in async/await

### Medium Priority (1 rule)
Code organization:

7. **medium-error-boundaries** - Implement error boundaries at module level

---

## Rule Details

### 1. critical-error-swallowing

**Why it matters:** Silent failures hide bugs and make debugging impossible.

**Detection:**
- Look for empty `catch` blocks
- Check for `catch(e) {}` without logging/rethrowing
- Search for `.catch(() => {})` on promises

**❌ Incorrect:**
```typescript
async function updateUser(id: string, data: UserData) {
  try {
    await db.users.update(id, data);
  } catch (error) {
    // Silent failure! Bug hidden from logs
  }
}

// Or with promises
fetch('/api/data')
  .then(response => response.json())
  .catch(() => {}); // Silently swallows network errors!
```

**✅ Correct:**
```typescript
async function updateUser(id: string, data: UserData) {
  try {
    await db.users.update(id, data);
  } catch (error) {
    logger.error('Failed to update user', { userId: id, error });
    throw error; // Re-throw or handle explicitly
  }
}

// Or return Result type
async function updateUserSafe(id: string, data: UserData): Promise<Result<User, Error>> {
  try {
    const user = await db.users.update(id, data);
    return { ok: true, value: user };
  } catch (error) {
    logger.error('Failed to update user', { userId: id, error });
    return { ok: false, error: error as Error };
  }
}
```

**Impact:** CRITICAL - Silent failures prevent debugging and monitoring

**Reference:** Node.js Best Practices, Error Handling Section

---

### 2. critical-unhandled-rejection

**Why it matters:** Unhandled promise rejections can crash Node.js processes in production.

**Detection:**
- Look for promises without `.catch()`
- Check for async functions called without `await` or `.catch()`
- Search for event emitters without error handlers

**❌ Incorrect:**
```typescript
// Promise rejection not handled
function loadData() {
  fetch('/api/data').then(response => {
    return response.json(); // Rejection if network fails!
  });
  // Missing .catch()!
}

// Async function not awaited
async function saveUser(user: User) {
  db.users.save(user); // Promise not awaited! Rejection lost
}

// Fire-and-forget
async function sendEmail(email: string) {
  await sendEmailService(email); // If this fails, who handles it?
}
sendEmail('user@example.com'); // No await, no .catch()
```

**✅ Correct:**
```typescript
// Handle promise rejection explicitly
async function loadData(): Promise<Data> {
  try {
    const response = await fetch('/api/data');
    return await response.json();
  } catch (error) {
    logger.error('Failed to load data', { error });
    throw new DataLoadError('Unable to fetch data', { cause: error });
  }
}

// Await and handle
async function saveUser(user: User) {
  try {
    await db.users.save(user);
  } catch (error) {
    logger.error('Failed to save user', { user, error });
    throw error;
  }
}

// Fire-and-forget with explicit error handling
async function sendEmailInBackground(email: string) {
  sendEmail(email).catch(error => {
    logger.error('Background email failed', { email, error });
    // Optionally queue for retry
  });
}
```

**Impact:** CRITICAL - Prevents process crashes and data loss

**Reference:** Node.js Best Practices: Promise Rejection Handling

---

### 3. critical-throw-non-error

**Why it matters:** Throwing non-Error objects loses stack traces and breaks error handling.

**Detection:**
- Look for `throw 'string'` or `throw { ... }`
- Check for rejection with non-Error: `Promise.reject('string')`
- Search for custom error objects without Error inheritance

**❌ Incorrect:**
```typescript
function validateUser(user: User) {
  if (!user.email) {
    throw 'Email is required'; // String! No stack trace
  }
  if (!user.age || user.age < 18) {
    throw { code: 'UNDERAGE', message: 'Too young' }; // Plain object!
  }
}

// Promise rejection with string
async function loadConfig() {
  if (!configFileExists) {
    return Promise.reject('Config not found'); // No stack trace!
  }
}
```

**✅ Correct:**
```typescript
class ValidationError extends Error {
  constructor(message: string, public field: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

function validateUser(user: User) {
  if (!user.email) {
    throw new ValidationError('Email is required', 'email');
  }
  if (!user.age || user.age < 18) {
    throw new ValidationError('User must be 18 or older', 'age');
  }
}

// Custom error for config issues
class ConfigError extends Error {
  constructor(message: string, public configPath: string) {
    super(message);
    this.name = 'ConfigError';
  }
}

async function loadConfig() {
  if (!configFileExists) {
    throw new ConfigError('Config file not found', './config.json');
  }
}
```

**Impact:** HIGH - Enables proper debugging with stack traces

**Reference:** MDN: Error Objects, Node.js Best Practices

---

### 4. high-error-context

**Why it matters:** Error messages without context make debugging production issues nearly impossible.

**Detection:**
- Look for generic error messages
- Check for errors without relevant data
- Search for missing error context in logs

**❌ Incorrect:**
```typescript
async function processPayment(userId: string, amount: number) {
  try {
    await paymentGateway.charge(userId, amount);
  } catch (error) {
    throw new Error('Payment failed'); // No context!
  }
}

// Logs missing context
function deleteUser(id: string) {
  try {
    db.users.delete(id);
  } catch (error) {
    logger.error('Delete failed'); // Which user? Why?
  }
}
```

**✅ Correct:**
```typescript
class PaymentError extends Error {
  constructor(
    message: string,
    public userId: string,
    public amount: number,
    public cause?: Error
  ) {
    super(message);
    this.name = 'PaymentError';
  }
}

async function processPayment(userId: string, amount: number) {
  try {
    await paymentGateway.charge(userId, amount);
  } catch (error) {
    throw new PaymentError(
      'Payment processing failed',
      userId,
      amount,
      error as Error
    );
  }
}

// Rich logging context
function deleteUser(id: string) {
  try {
    db.users.delete(id);
  } catch (error) {
    logger.error('Failed to delete user', {
      userId: id,
      error: error instanceof Error ? error.message : String(error),
      stack: error instanceof Error ? error.stack : undefined,
      timestamp: new Date().toISOString()
    });
    throw error;
  }
}
```

**Impact:** HIGH - Makes production debugging feasible

**Reference:** Node.js Best Practices: Error Logging

---

### 5. high-custom-error-types

**Why it matters:** Typed errors enable proper error handling and recovery strategies.

**Detection:**
- Look for catching all errors with generic `Error`
- Check for `instanceof Error` without specific types
- Search for error codes in plain error messages

**❌ Incorrect:**
```typescript
try {
  await createUser(userData);
} catch (error) {
  // Can't distinguish between validation, DB, or network errors
  if (error.message.includes('duplicate')) {
    return { error: 'User exists' };
  }
  return { error: 'Unknown error' };
}
```

**✅ Correct:**
```typescript
class ValidationError extends Error {
  constructor(message: string, public field: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

class DuplicateUserError extends Error {
  constructor(public email: string) {
    super(`User with email ${email} already exists`);
    this.name = 'DuplicateUserError';
  }
}

class DatabaseError extends Error {
  constructor(message: string, public operation: string) {
    super(message);
    this.name = 'DatabaseError';
  }
}

async function createUser(userData: UserData) {
  // Validation
  if (!userData.email) {
    throw new ValidationError('Email required', 'email');
  }
  
  // Check duplicates
  const existing = await db.users.findByEmail(userData.email);
  if (existing) {
    throw new DuplicateUserError(userData.email);
  }
  
  // Create user
  try {
    return await db.users.create(userData);
  } catch (error) {
    throw new DatabaseError('Failed to create user', 'INSERT');
  }
}

// Type-safe error handling
try {
  await createUser(userData);
} catch (error) {
  if (error instanceof ValidationError) {
    return { error: `Invalid ${error.field}` };
  }
  if (error instanceof DuplicateUserError) {
    return { error: 'User already exists' };
  }
  if (error instanceof DatabaseError) {
    logger.error('DB operation failed', { error });
    return { error: 'Server error' };
  }
  throw error; // Unknown error
}
```

**Impact:** MEDIUM-HIGH - Enables granular error recovery

**Reference:** Effective TypeScript, Item 27: Use Functional Constructs

---

### 6. high-async-try-catch

**Why it matters:** Missing try-catch in async functions leads to unhandled rejections.

**Detection:**
- Look for async functions without try-catch
- Check for multiple awaits without error handling
- Search for async middleware without error wrapping

**❌ Incorrect:**
```typescript
async function getUserData(id: string) {
  const user = await db.users.find(id); // Might throw!
  const posts = await db.posts.findByUser(id); // Might throw!
  const comments = await db.comments.findByUser(id); // Might throw!
  return { user, posts, comments };
}

// Express/GraphQL resolver without error handling
app.get('/users/:id', async (req, res) => {
  const user = await getUserData(req.params.id); // Unhandled rejection!
  res.json(user);
});
```

**✅ Correct:**
```typescript
async function getUserData(id: string) {
  try {
    const user = await db.users.find(id);
    const posts = await db.posts.findByUser(id);
    const comments = await db.comments.findByUser(id);
    return { user, posts, comments };
  } catch (error) {
    logger.error('Failed to load user data', { userId: id, error });
    throw new DataLoadError(`Unable to load data for user ${id}`);
  }
}

// Express with error handling
app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await getUserData(req.params.id);
    res.json(user);
  } catch (error) {
    next(error); // Pass to error middleware
  }
});

// Or use async wrapper
const asyncHandler = (fn: Function) => (req: Request, res: Response, next: NextFunction) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await getUserData(req.params.id);
  res.json(user);
}));
```

**Impact:** HIGH - Prevents unhandled rejection crashes

**Reference:** Node.js Best Practices: Async Error Handling

---

### 7. medium-error-boundaries

**Why it matters:** Centralized error handling improves code organization and recovery.

**Detection:**
- Look for scattered error handling
- Check for missing top-level error handlers
- Search for duplicate error handling logic

**❌ Incorrect:**
```typescript
// Scattered error handling in each function
async function operation1() {
  try {
    await doSomething();
  } catch (error) {
    logger.error('Op1 failed', { error });
    // Send to monitoring
    // Update metrics
  }
}

async function operation2() {
  try {
    await doSomethingElse();
  } catch (error) {
    logger.error('Op2 failed', { error });
    // Duplicate monitoring code
    // Duplicate metrics code
  }
}
```

**✅ Correct:**
```typescript
// Centralized error boundary
class ErrorBoundary {
  async execute<T>(
    operation: () => Promise<T>,
    context: { operationName: string; metadata?: Record<string, any> }
  ): Promise<T> {
    try {
      return await operation();
    } catch (error) {
      // Centralized logging
      logger.error(`Operation failed: ${context.operationName}`, {
        ...context.metadata,
        error
      });
      
      // Centralized monitoring
      monitoring.recordError(error, context);
      
      // Centralized metrics
      metrics.increment('operation.error', {
        operation: context.operationName
      });
      
      throw error; // Re-throw for caller to handle
    }
  }
}

const errorBoundary = new ErrorBoundary();

// Clean operation code
async function operation1() {
  return errorBoundary.execute(
    () => doSomething(),
    { operationName: 'operation1', metadata: { type: 'data-load' } }
  );
}

async function operation2() {
  return errorBoundary.execute(
    () => doSomethingElse(),
    { operationName: 'operation2', metadata: { type: 'user-action' } }
  );
}

// Express error handler middleware
app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
  logger.error('Request failed', {
    error,
    path: req.path,
    method: req.method
  });
  
  if (error instanceof ValidationError) {
    return res.status(400).json({ error: error.message });
  }
  
  res.status(500).json({ error: 'Internal server error' });
});
```

**Impact:** MEDIUM - Improves code organization and consistency

**Reference:** Node.js Best Practices: Error Handler Middleware

---

## Usage Examples

**Review async error handling:**
```
Check this async code for proper error handling
```

**Audit promise rejections:**
```
Find unhandled promise rejections in this file
```

**Check error propagation:**
```
Review error handling chain for this API endpoint
```

## Summary

Proper error handling ensures:
- ✅ No silent failures (catch-and-ignore)
- ✅ All rejections handled
- ✅ Error objects with stack traces
- ✅ Rich context for debugging
- ✅ Typed errors for recovery
- ✅ Consistent error boundaries

Following these rules prevents production incidents and enables effective debugging.
