# Code Review Template

Reference for: PR Review

Use this template structure for code review outputs.

---

## Summary
Good to merge with minor fixes

## Critical

### 1. SQL Injection Risk

**File:** `src/api/users.ts:42`

**Issue:** User input concatenated directly into SQL query

**Code:**
```typescript
const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
```

**Risk:** Attacker can execute arbitrary SQL commands

**Fix:** Use parameterized queries:
```typescript
const query = 'SELECT * FROM users WHERE id = $1';
await db.query(query, [req.params.id]);
```

---

## Important

### 1. Missing Error Handling

**File:** `src/services/payment.ts:67-82`

**Issue:** No try/catch around payment API call

**Impact:** Unhandled promise rejection crashes the process

**Fix:**
```typescript
try {
  const result = await stripe.charges.create(chargeData);
  return result;
} catch (error) {
  logger.error('Payment failed', { error, userId });
  throw new PaymentError('Payment processing failed');
}
```

### 2. Race Condition in Counter

**File:** `src/utils/counter.ts:23-27`

**Issue:** Read-modify-write without locking

**Code:**
```typescript
const current = await db.get('counter');
await db.set('counter', current + 1);
```

**Impact:** Concurrent requests can result in lost increments

**Fix:** Use atomic increment or optimistic locking

---

## Minor

### 1. Overly Broad Exception Catch

**File:** `src/api/posts.ts:91`

**Code:**
```typescript
} catch (error) {
  return res.status(500).send('Error');
}
```

**Issue:** Catches all errors including network issues, validation errors

**Improvement:** Catch specific error types:
```typescript
} catch (error) {
  if (error instanceof ValidationError) {
    return res.status(400).send(error.message);
  }
  logger.error('Unexpected error', { error });
  return res.status(500).send('Internal server error');
}
```

### 2. Magic Number

**File:** `src/utils/cache.ts:12`

**Code:**
```typescript
setTimeout(cleanup, 300000);
```

**Issue:** 300000 is not self-explanatory

**Improvement:**
```typescript
const FIVE_MINUTES_MS = 5 * 60 * 1000;
setTimeout(cleanup, FIVE_MINUTES_MS);
```

---

## Questions

1. **Payment retry logic** - What happens if Stripe is down? Should we queue for retry?

2. **Cache invalidation** - How is the cache invalidated when users update their profile?

---

## Positive Notes

- Good test coverage for the happy path
- Clear variable names throughout
- Proper use of TypeScript types
