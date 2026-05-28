---
title: Use Map for Dynamic Key Collections
impact: MEDIUM
impactDescription: Better performance and API for key-value collections
tags: data-structures, map, object, collections
---

## Use Map for Dynamic Key Collections

Plain objects have limitations: keys must be strings, prototype pollution risks, and no size property. Map provides a proper key-value data structure.

**Incorrect (object as map):**

```javascript
// Keys are coerced to strings
const cache = {};
cache[1] = 'one';
cache['1'] = 'string one';
console.log(Object.keys(cache)); // ['1'] - collision!

// Object keys
const userObj = { id: 1 };
cache[userObj] = 'user data';
console.log(cache['[object Object]']); // 'user data' - wrong key!

// Prototype pollution risk
const data = {};
data['__proto__'] = { malicious: true }; // Dangerous
```

**Correct (use Map):**

```javascript
// Any value as key, no coercion
const cache = new Map();
cache.set(1, 'one');
cache.set('1', 'string one');
console.log(cache.size); // 2 - no collision

// Object keys work correctly
const userObj = { id: 1 };
cache.set(userObj, 'user data');
console.log(cache.get(userObj)); // 'user data'

// No prototype pollution
cache.set('__proto__', { safe: true }); // Just a key

// Better API
cache.has(key);      // vs key in obj
cache.delete(key);   // vs delete obj[key]
cache.clear();       // vs obj = {}
cache.size;          // vs Object.keys(obj).length

// Iteration in insertion order
for (const [key, value] of cache) {
  console.log(key, value);
}
```

**When to use Object:**

```javascript
// Static structure known at compile time
const config = {
  apiUrl: '/api',
  timeout: 5000
};

// JSON serialization needed (Map doesn't serialize)
JSON.stringify({ key: 'value' }); // Works
JSON.stringify(new Map([['key', 'value']])); // "{}"
```

Reference: [MDN Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)
