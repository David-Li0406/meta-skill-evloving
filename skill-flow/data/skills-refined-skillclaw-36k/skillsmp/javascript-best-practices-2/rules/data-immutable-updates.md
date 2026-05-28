---
title: Use Spread Operator for Immutable Updates
impact: MEDIUM
impactDescription: Prevents mutation bugs and enables efficient change detection
tags: immutability, spread, state, updates
---

## Use Spread Operator for Immutable Updates

Mutating objects directly causes bugs in React state, breaks change detection, and makes debugging difficult. Create new objects for updates.

**Incorrect (direct mutation):**

```javascript
// Mutating object
const user = { name: 'Alice', age: 30 };
user.age = 31; // Mutation - reference unchanged

// Mutating array
const items = [1, 2, 3];
items.push(4); // Mutation - reference unchanged

// Mutating nested object
const state = { user: { name: 'Alice' } };
state.user.name = 'Bob'; // Deep mutation

// React won't detect these changes
setState(state); // No re-render!
```

**Correct (immutable updates):**

```javascript
// Object update
const user = { name: 'Alice', age: 30 };
const updatedUser = { ...user, age: 31 }; // New object

// Array operations
const items = [1, 2, 3];
const added = [...items, 4];           // Add
const removed = items.filter(x => x !== 2); // Remove
const updated = items.map(x => x === 2 ? 20 : x); // Update

// Nested update
const state = { user: { name: 'Alice', email: 'a@b.com' } };
const newState = {
  ...state,
  user: { ...state.user, name: 'Bob' }
};

// Array of objects
const users = [{ id: 1, name: 'Alice' }];
const updatedUsers = users.map(u =>
  u.id === 1 ? { ...u, name: 'Bob' } : u
);
```

**For deeply nested updates, consider Immer:**

```javascript
import { produce } from 'immer';

const newState = produce(state, draft => {
  draft.users[0].address.city = 'NYC';
  draft.users.push({ id: 2, name: 'Bob' });
});
```

Immutability enables React's efficient rendering, Redux time-travel debugging, and prevents subtle mutation bugs.

Reference: [Immer](https://immerjs.github.io/immer/)
