# Bug Review Example Output

This is an example of the expected output format for a bug review.

---

## Bug Review

**Scope:** src/services/PaymentService.ts, src/utils/calculations.ts
**Project Type:** Node.js/TypeScript

### Findings

| Severity | Count |
|----------|-------|
| Critical | 1 |
| Major | 2 |
| Minor | 1 |

### Critical Issues (Must Fix)

**1. Race Condition in Balance Update** `Critical` `Bugs`
`src/services/PaymentService.ts:67-75`

Balance is read, modified, and saved without atomic operation. Concurrent requests can cause incorrect balances.

```typescript
async function deductBalance(userId: string, amount: number) {
  const user = await getUser(userId);
  user.balance -= amount;  // Another request may have changed balance
  await saveUser(user);    // Overwrites with stale data
}
```

**Fix prompt** (copy to Claude Code):
> Fix the race condition in deductBalance in src/services/PaymentService.ts:67-75:
> 1. Use a database transaction with row locking
> 2. Or use an atomic update: UPDATE users SET balance = balance - ? WHERE id = ? AND balance >= ?
> 3. Check the affected rows count to verify the deduction succeeded

---

### Major Issues (Should Fix)

**2. Null Reference on Optional Field** `Major` `Bugs`
`src/services/PaymentService.ts:34`

Accessing `user.paymentMethod.id` without checking if paymentMethod exists.

```typescript
const methodId = user.paymentMethod.id; // Crashes if no payment method
```

**Fix**:
```diff
- const methodId = user.paymentMethod.id;
+ const methodId = user.paymentMethod?.id;
+ if (!methodId) {
+   throw new Error('User has no payment method configured');
+ }
```

---

**3. Unhandled Promise Rejection** `Major` `Bugs`
`src/services/PaymentService.ts:89-92`

Async function called without error handling. Failures will crash the process.

```typescript
function processWebhook(data: WebhookData) {
  updatePaymentStatus(data.paymentId, data.status); // No await, no catch
  return { received: true };
}
```

**Fix**:
```diff
- function processWebhook(data: WebhookData) {
-   updatePaymentStatus(data.paymentId, data.status);
-   return { received: true };
- }
+ async function processWebhook(data: WebhookData) {
+   try {
+     await updatePaymentStatus(data.paymentId, data.status);
+   } catch (error) {
+     logger.error('Failed to update payment status:', error);
+     // Consider: retry logic or dead-letter queue
+   }
+   return { received: true };
+ }
```

---

### Minor Issues

**4. Off-by-One in Pagination** `Minor` `Bugs`
`src/utils/calculations.ts:23`

Page calculation uses `<=` instead of `<`, returning one extra page.

```typescript
function getTotalPages(itemCount: number, pageSize: number): number {
  let pages = 0;
  for (let i = 0; i <= itemCount; i += pageSize) { // Should be <
    pages++;
  }
  return pages;
}
```

**Fix**:
```diff
- for (let i = 0; i <= itemCount; i += pageSize) {
+ for (let i = 0; i < itemCount; i += pageSize) {
```

Or better:
```diff
- let pages = 0;
- for (let i = 0; i <= itemCount; i += pageSize) {
-   pages++;
- }
- return pages;
+ return Math.ceil(itemCount / pageSize);
```

---

### Summary

- **1 Critical bug**: Race condition can cause financial data corruption
- **2 Major bugs**: Null reference and unhandled promise rejection
- **1 Minor bug**: Off-by-one error in pagination

---
Review saved to: .bug-review.md
