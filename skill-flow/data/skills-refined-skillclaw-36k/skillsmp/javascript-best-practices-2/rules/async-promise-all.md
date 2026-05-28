---
title: Use Promise.all for Parallel Operations
impact: CRITICAL
impactDescription: 2-10x improvement by parallelizing independent async operations
tags: promises, async, parallel, performance
---

## Use Promise.all for Parallel Operations

Sequential awaits add latency for each operation. When operations are independent, run them in parallel with Promise.all().

**Incorrect (sequential - 3 round trips):**

```javascript
async function loadDashboard(userId) {
  const user = await fetchUser(userId);       // 200ms
  const posts = await fetchPosts(userId);     // 200ms
  const notifications = await fetchNotifications(userId); // 200ms
  // Total: 600ms

  return { user, posts, notifications };
}
```

**Correct (parallel - 1 round trip):**

```javascript
async function loadDashboard(userId) {
  const [user, posts, notifications] = await Promise.all([
    fetchUser(userId),
    fetchPosts(userId),
    fetchNotifications(userId)
  ]);
  // Total: 200ms (longest request)

  return { user, posts, notifications };
}
```

**Note:** Promise.all rejects immediately if any promise rejects. Use Promise.allSettled if you need all results regardless of failures.

Reference: [MDN Promise.all](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all)
