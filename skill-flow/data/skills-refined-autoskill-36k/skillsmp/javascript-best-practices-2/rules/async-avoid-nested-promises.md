---
title: Flatten Promise Chains with Async/Await
impact: CRITICAL
impactDescription: Improves readability and error handling
tags: promises, async, await, refactoring
---

## Flatten Promise Chains with Async/Await

Nested .then() callbacks create "callback hell" that's hard to read and maintain. Async/await provides linear, synchronous-looking code.

**Incorrect (nested promise hell):**

```javascript
function getUserPosts(userId) {
  return fetchUser(userId)
    .then(user => {
      return fetchPosts(user.id)
        .then(posts => {
          return fetchComments(posts[0].id)
            .then(comments => {
              return { user, posts, comments };
            });
        });
    })
    .catch(error => console.error(error));
}
```

**Correct (flat async/await):**

```javascript
async function getUserPosts(userId) {
  try {
    const user = await fetchUser(userId);
    const posts = await fetchPosts(user.id);
    const comments = await fetchComments(posts[0].id);

    return { user, posts, comments };
  } catch (error) {
    console.error('Failed to load user posts:', error);
    throw error;
  }
}
```

**With parallel operations where possible:**

```javascript
async function getUserPosts(userId) {
  const user = await fetchUser(userId);

  // Posts and recent activity can load in parallel
  const [posts, activity] = await Promise.all([
    fetchPosts(user.id),
    fetchActivity(user.id)
  ]);

  return { user, posts, activity };
}
```

Async/await is syntactic sugar over promises - use it for cleaner code while maintaining promise semantics.
