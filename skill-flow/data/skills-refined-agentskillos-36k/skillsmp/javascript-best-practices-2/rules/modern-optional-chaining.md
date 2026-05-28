---
title: Use Optional Chaining for Safe Property Access
impact: LOW-MEDIUM
impactDescription: Cleaner code and prevents "cannot read property of undefined" errors
tags: optional-chaining, null-safety, modern, es2020
---

## Use Optional Chaining for Safe Property Access

Deeply nested property access throws errors when intermediate values are null or undefined. Optional chaining (?.) safely returns undefined instead.

**Incorrect (verbose null checks):**

```javascript
// Verbose and error-prone
let city;
if (user && user.address && user.address.city) {
  city = user.address.city;
}

// Logical AND has coercion issues
const name = user && user.profile && user.profile.name;
// Returns false for user.profile.name === ''

// Array/function access
const first = arr && arr[0];
const result = callback && callback();
```

**Correct (optional chaining):**

```javascript
// Clean nested access
const city = user?.address?.city;

// Array element access
const first = arr?.[0];
const dynamic = obj?.[dynamicKey];

// Method calls
const result = callback?.();
const length = obj?.method?.()?.length;

// Combining with nullish coalescing
const name = user?.profile?.name ?? 'Anonymous';
const count = data?.items?.length ?? 0;

// In conditions
if (user?.isAdmin) {
  showAdminPanel();
}

// With destructuring
const { city } = user?.address ?? {};
```

**When NOT to use:**

```javascript
// Don't hide programming errors
// If user should always exist, let it throw
function getUserId(user) {
  return user.id; // Throw if user is undefined (bug)
}

// Don't chain when you need to handle missing data
if (!user?.address) {
  showAddressForm(); // Handle missing address explicitly
}
```

Optional chaining is for optional data, not for hiding bugs. If a value should always exist, let it throw.

Reference: [MDN Optional Chaining](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining)
