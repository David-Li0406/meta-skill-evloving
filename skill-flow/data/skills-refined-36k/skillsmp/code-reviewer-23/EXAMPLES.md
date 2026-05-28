# Code Review Examples

## Example 1: React Component Review

### Code Under Review

```javascript
function UserList({ users }) {
  const [filter, setFilter] = useState('');

  const filteredUsers = users.filter(u =>
    u.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <input onChange={e => setFilter(e.target.value)} />
      {filteredUsers.map(user => (
        <UserCard user={user} onClick={() => handleClick(user.id)} />
      ))}
    </div>
  );
}
```

### Review Output

## Code Review: UserList Component

### Summary
Functional component with filtering logic. Has performance issues due to missing memoization and key props.

### Critical Issues
1. **Missing key prop** (line 12): React list items need unique keys for reconciliation.
   ```javascript
   <UserCard key={user.id} user={user} ... />
   ```

### Recommendations
1. **Performance: Memoize filtered results** (line 4-6): Filter runs on every render. Use `useMemo`:
   ```javascript
   const filteredUsers = useMemo(() =>
     users.filter(u => u.name.toLowerCase().includes(filter.toLowerCase())),
     [users, filter]
   );
   ```

2. **Performance: Memoize click handler** (line 12): Creates new function each render. Use `useCallback`:
   ```javascript
   const handleUserClick = useCallback((id) => handleClick(id), []);
   // Then: onClick={() => handleUserClick(user.id)}
   ```

### Suggestions
1. **Accessibility**: Add label or aria-label to input
2. **UX**: Consider debouncing filter input for large lists

### Positive Highlights
- Clean, readable component structure
- Proper use of controlled input

---

## Example 2: API Service Review

### Code Under Review

```javascript
async function fetchUserData(userId) {
  const response = await fetch(`/api/users/${userId}`);
  const data = await response.json();
  return data;
}
```

### Review Output

## Code Review: fetchUserData Service

### Summary
Basic fetch wrapper lacking error handling and validation.

### Critical Issues
1. **Missing error handling**: Network errors and non-2xx responses will cause silent failures.
   ```javascript
   async function fetchUserData(userId) {
     const response = await fetch(`/api/users/${userId}`);
     if (!response.ok) {
       throw new Error(`Failed to fetch user: ${response.status}`);
     }
     return response.json();
   }
   ```

### Recommendations
1. **Input validation**: Validate userId before making request
   ```javascript
   if (!userId) throw new Error('userId is required');
   ```

2. **Type safety**: Consider adding JSDoc or TypeScript types for return value

### Suggestions
1. Consider using a shared fetch wrapper with consistent error handling
2. Add request timeout handling for slow networks

---

## Example 3: Architecture Review

### Code Under Review

```javascript
// OrderService.js
import { db } from './database';
import { sendEmail } from './emailService';
import { updateInventory } from './inventoryService';
import { processPayment } from './paymentService';
import { logAnalytics } from './analyticsService';

async function createOrder(orderData) {
  const payment = await processPayment(orderData.payment);
  const order = await db.orders.create({ ...orderData, paymentId: payment.id });
  await updateInventory(orderData.items);
  await sendEmail(orderData.email, 'Order Confirmation', order);
  logAnalytics('order_created', order);
  return order;
}
```

### Review Output

## Code Review: OrderService Architecture

### Summary
Order creation with tightly coupled dependencies. High risk of partial failures without proper handling.

### Critical Issues
1. **No transaction handling**: If `updateInventory` fails after payment, system is in inconsistent state. Consider:
   - Saga pattern for distributed transactions
   - Compensation logic for rollbacks
   - Event-driven architecture with eventual consistency

### Recommendations
1. **High coupling**: Service depends on 5 external services directly. Consider:
   - Event-driven: Publish `OrderCreated` event, let services subscribe
   - Dependency injection for testability

2. **Error handling**: Each step can fail independently. Add try/catch with appropriate rollback:
   ```javascript
   try {
     const payment = await processPayment(orderData.payment);
     try {
       const order = await db.orders.create({...});
       // Queue non-critical operations
       await Promise.allSettled([
         updateInventory(orderData.items),
         sendEmail(...),
       ]);
     } catch (e) {
       await refundPayment(payment.id);
       throw e;
     }
   } catch (e) {
     // Handle payment failure
   }
   ```

3. **Non-blocking operations**: Email and analytics shouldn't block order creation. Use message queue.

### Suggestions
1. Extract orchestration logic to a separate OrderOrchestrator
2. Add idempotency key for retry safety

### Positive Highlights
- Clear function name and single entry point
- Logical operation ordering (payment before inventory)
