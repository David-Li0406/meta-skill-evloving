---
title: Early Return from Functions
impact: LOW-MEDIUM
impactDescription: avoids unnecessary computation
tags: js, early-return, optimization, control-flow
---

## Early Return from Functions

Return early when result is determined to skip unnecessary processing.

**Incorrect (processes all items even after finding answer):**

```typescript
function validateUsers(users: User[]) {
  let hasError = false
  let errorMessage = ''
  
  for (const user of users) {
    if (!user.email) {
      hasError = true
      errorMessage = 'Missing email'
    }
    if (!user.name) {
      hasError = true
      errorMessage = 'Missing name'
    }
  }
  
  return hasError ? { valid: false, error: errorMessage } : { valid: true }
}
```

**Correct (returns immediately on first error):**

```typescript
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) {
      return { valid: false, error: 'Missing email' }
    }
    if (!user.name) {
      return { valid: false, error: 'Missing name' }
    }
  }
  return { valid: true }
}
```
