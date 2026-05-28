---
title: Use Promise.allSettled When Some Can Fail
impact: CRITICAL
impactDescription: Prevents single failure from losing all results
tags: promises, async, error-handling, allsettled
---

## Use Promise.allSettled When Some Can Fail

Promise.all rejects immediately when any promise fails, losing results from successful promises. Use Promise.allSettled to get all results regardless of individual failures.

**Incorrect (one failure loses all data):**

```javascript
async function loadUserData(userIds) {
  try {
    // If one user fails, we lose ALL users
    const users = await Promise.all(
      userIds.map(id => fetchUser(id))
    );
    return users;
  } catch (error) {
    return []; // Lost 99 successful fetches due to 1 failure
  }
}
```

**Correct (handle each result independently):**

```javascript
async function loadUserData(userIds) {
  const results = await Promise.allSettled(
    userIds.map(id => fetchUser(id))
  );

  const users = [];
  const errors = [];

  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      users.push(result.value);
    } else {
      errors.push({ userId: userIds[index], error: result.reason });
    }
  });

  if (errors.length > 0) {
    console.warn('Some users failed to load:', errors);
  }

  return users; // Returns successful fetches
}
```

Use Promise.all when all results are required. Use Promise.allSettled when partial results are acceptable.

Reference: [MDN Promise.allSettled](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled)
