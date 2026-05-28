---
title: Use Set for Unique Value Collections
impact: MEDIUM
impactDescription: O(1) lookups and automatic deduplication
tags: data-structures, set, unique, collections
---

## Use Set for Unique Value Collections

Arrays require O(n) includes() checks and manual deduplication. Set provides O(1) has() checks and automatic uniqueness.

**Incorrect (array for unique values):**

```javascript
// Slow O(n) lookup
const tags = ['javascript', 'react', 'node'];
if (tags.includes(newTag)) { // O(n) every time
  return;
}
tags.push(newTag);

// Manual deduplication
const unique = items.filter((item, index) =>
  items.indexOf(item) === index // O(n²)
);

// Checking membership in loop
items.forEach(item => {
  if (seen.includes(item)) return; // O(n) per iteration
  seen.push(item);
  process(item);
});
```

**Correct (use Set):**

```javascript
// O(1) lookup and automatic uniqueness
const tags = new Set(['javascript', 'react', 'node']);
tags.add(newTag); // Ignored if already exists
tags.has('react'); // O(1)

// Simple deduplication
const unique = [...new Set(items)]; // O(n)

// Efficient membership check in loop
const seen = new Set();
items.forEach(item => {
  if (seen.has(item)) return; // O(1)
  seen.add(item);
  process(item);
});

// Set operations
const setA = new Set([1, 2, 3]);
const setB = new Set([2, 3, 4]);

// Union
const union = new Set([...setA, ...setB]); // {1, 2, 3, 4}

// Intersection
const intersection = new Set([...setA].filter(x => setB.has(x))); // {2, 3}

// Difference
const difference = new Set([...setA].filter(x => !setB.has(x))); // {1}
```

**Converting between Array and Set:**

```javascript
const arr = [1, 2, 2, 3, 3, 3];
const set = new Set(arr);     // Set {1, 2, 3}
const unique = [...set];       // [1, 2, 3]
```

Reference: [MDN Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)
