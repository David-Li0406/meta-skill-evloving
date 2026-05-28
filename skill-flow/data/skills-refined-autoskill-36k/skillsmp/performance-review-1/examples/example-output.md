# Performance Review Example Output

This is an example of the expected output format for a performance review.

---

## Performance Review

**Scope:** src/services/OrderService.ts, src/api/orders.ts
**Project Type:** Node.js/TypeScript

### Findings

| Severity | Count |
|----------|-------|
| Critical | 1 |
| Major | 2 |
| Minor | 1 |
| Suggestion | 1 |

### Critical Issues (Must Fix)

**1. N+1 Query Problem in Order Loading** `Critical` `Performance`
`src/services/OrderService.ts:45-52`

Each order triggers a separate database query for its items. With 100 orders, this makes 101 queries.

```typescript
// Current code (N+1 problem)
const orders = await Order.findAll();
for (const order of orders) {
  order.items = await OrderItem.findByOrderId(order.id);
}
```

**Fix**:
```diff
  const orders = await Order.findAll();
- for (const order of orders) {
-   order.items = await OrderItem.findByOrderId(order.id);
- }
+ const orderIds = orders.map(o => o.id);
+ const allItems = await OrderItem.findByOrderIds(orderIds);
+ const itemsByOrder = groupBy(allItems, 'orderId');
+ orders.forEach(o => o.items = itemsByOrder[o.id] || []);
```

---

### Major Issues (Should Fix)

**2. Sequential Awaits for Independent Data** `Major` `Performance`
`src/api/orders.ts:23-26`

Three independent API calls are awaited sequentially, taking 3x longer than necessary.

```typescript
const user = await getUser(userId);      // 200ms
const orders = await getOrders(userId);  // 300ms
const preferences = await getPrefs(userId); // 100ms
// Total: 600ms
```

**Fix**:
```diff
- const user = await getUser(userId);
- const orders = await getOrders(userId);
- const preferences = await getPrefs(userId);
+ const [user, orders, preferences] = await Promise.all([
+   getUser(userId),
+   getOrders(userId),
+   getPrefs(userId)
+ ]);
+ // Total: 300ms (parallel)
```

---

**3. Unbounded Query on Large Table** `Major` `Performance`
`src/services/OrderService.ts:78`

Query fetches all orders without pagination. This will cause memory issues as the table grows.

```typescript
const allOrders = await db.query('SELECT * FROM orders');
```

**Fix prompt** (copy to Claude Code):
> Add pagination to the orders query in src/services/OrderService.ts:78:
> 1. Add page and pageSize parameters to the function
> 2. Add LIMIT and OFFSET to the SQL query
> 3. Return a paginated result object with items, total, page, pageSize

---

### Minor Issues

**4. String Concatenation in Loop** `Minor` `Performance`
`src/utils/export.ts:34-38`

Building export string with += in a loop creates O(n²) string operations.

```typescript
let csv = '';
for (const row of rows) {
  csv += formatRow(row) + '\n';
}
```

**Fix**:
```diff
- let csv = '';
- for (const row of rows) {
-   csv += formatRow(row) + '\n';
- }
+ const csv = rows.map(row => formatRow(row)).join('\n');
```

---

### Suggestions

**5. Consider Caching User Preferences** `Suggestion` `Performance`
`src/api/orders.ts:26`

User preferences are loaded on every request but rarely change.

**Fix prompt** (copy to Claude Code):
> Add caching for user preferences in the orders API:
> 1. Create a simple in-memory cache with TTL (5 minutes suggested)
> 2. Check cache before calling getPrefs()
> 3. Invalidate cache when preferences are updated

---

### Summary

- **1 Critical issue**: N+1 queries causing database overload
- **2 Major issues**: Sequential operations and unbounded queries
- **1 Minor issue**: Inefficient string building
- **1 Suggestion**: Caching opportunity

---
Review saved to: .performance-review.md
