---
title: Wrap Async Operations in Try-Catch
impact: HIGH
impactDescription: Prevents unhandled rejections and enables graceful error recovery
tags: async, errors, try-catch, exceptions
---

## Wrap Async Operations in Try-Catch

Async functions can throw at any await point. Without try-catch, errors become unhandled rejections that crash the application or fail silently.

**Incorrect (unhandled async errors):**

```javascript
async function loadUserData() {
  const user = await fetchUser(); // Can throw
  const posts = await fetchPosts(user.id); // Can throw
  return { user, posts };
}

// Caller doesn't handle errors
const data = await loadUserData();
renderDashboard(data);
```

**Correct (proper error handling):**

```javascript
async function loadUserData() {
  try {
    const user = await fetchUser();
    const posts = await fetchPosts(user.id);
    return { user, posts, error: null };
  } catch (error) {
    console.error('Failed to load user data:', error);
    return { user: null, posts: [], error };
  }
}

// Or throw with context
async function loadUserData() {
  try {
    const user = await fetchUser();
    const posts = await fetchPosts(user.id);
    return { user, posts };
  } catch (error) {
    throw new Error(`Failed to load user data: ${error.message}`, {
      cause: error
    });
  }
}

// Caller handles appropriately
try {
  const data = await loadUserData();
  renderDashboard(data);
} catch (error) {
  renderErrorState(error.message);
  reportError(error);
}
```

**For multiple independent operations:**

```javascript
async function loadDashboard() {
  const results = await Promise.allSettled([
    fetchUser(),
    fetchNotifications(),
    fetchRecommendations()
  ]);

  return {
    user: results[0].status === 'fulfilled' ? results[0].value : null,
    notifications: results[1].status === 'fulfilled' ? results[1].value : [],
    recommendations: results[2].status === 'fulfilled' ? results[2].value : []
  };
}
```
