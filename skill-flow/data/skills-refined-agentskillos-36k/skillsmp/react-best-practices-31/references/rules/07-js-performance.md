# JavaScript Performance

**Impact: LOW-MEDIUM** | Micro-optimizations for hot paths can add up to meaningful improvements.

---

## 1. Use Set/Map for O(1) Lookups

Convert arrays to Set/Map for repeated membership checks.

```typescript
// BAD: O(n) per check
items.filter(item => allowedIds.includes(item.id))

// GOOD: O(1) per check
const allowed = new Set(allowedIds)
items.filter(item => allowed.has(item.id))
```

---

## 2. Build Index Maps for Repeated Lookups

Multiple `.find()` calls should use Map. **1M ops → 2K ops** for 1000×1000.

```typescript
// BAD: O(n) per lookup
orders.map(o => ({ ...o, user: users.find(u => u.id === o.userId) }))

// GOOD: O(1) per lookup
const userById = new Map(users.map(u => [u.id, u]))
orders.map(o => ({ ...o, user: userById.get(o.userId) }))
```

---

## 3. Early Length Check for Array Comparisons

Check lengths before expensive operations.

```typescript
function hasChanges(current: string[], original: string[]) {
  if (current.length !== original.length) return true
  // ... expensive comparison
}
```

---

## 4. Use toSorted() Instead of sort()

`.sort()` mutates array - causes React bugs. Use `.toSorted()` for immutability.

```typescript
// BAD: mutates original
const sorted = users.sort((a, b) => a.name.localeCompare(b.name))

// GOOD: creates new array
const sorted = users.toSorted((a, b) => a.name.localeCompare(b.name))

// Fallback: [...items].sort()
```

---

## 5. Use Loop for Min/Max Instead of Sort

Finding min/max requires single pass, not sorting. **O(n) vs O(n log n)**.

```typescript
// BAD
const latest = [...projects].sort((a, b) => b.updatedAt - a.updatedAt)[0]

// GOOD
let latest = projects[0]
for (const p of projects) {
  if (p.updatedAt > latest.updatedAt) latest = p
}
```

---

## 6. Combine Multiple Array Iterations

Multiple `.filter()` calls = multiple iterations.

```typescript
// BAD: 3 iterations
const admins = users.filter(u => u.isAdmin)
const testers = users.filter(u => u.isTester)

// GOOD: 1 iteration
const admins: User[] = [], testers: User[] = []
for (const u of users) {
  if (u.isAdmin) admins.push(u)
  if (u.isTester) testers.push(u)
}
```

---

## 7. Early Return from Functions

Return immediately when result is determined.

```typescript
// BAD: processes all items after finding answer
function validateUsers(users: User[]) {
  let error = ''
  for (const u of users) {
    if (!u.email) error = 'Email required'
  }
  return error ? { valid: false, error } : { valid: true }
}

// GOOD: returns on first error
function validateUsers(users: User[]) {
  for (const u of users) {
    if (!u.email) return { valid: false, error: 'Email required' }
  }
  return { valid: true }
}
```

---

## 8. Cache Repeated Function Calls

Use module-level Map for expensive computations.

```typescript
const cache = new Map<string, string>()

function getCachedSlug(text: string): string {
  if (!cache.has(text)) cache.set(text, slugify(text))
  return cache.get(text)!
}
```

---

## 9. Cache Storage API Calls

localStorage/sessionStorage are synchronous and expensive.

```typescript
const storageCache = new Map<string, string | null>()

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) storageCache.set(key, localStorage.getItem(key))
  return storageCache.get(key)
}
```

---

## 10. Cache Property Access in Loops

```typescript
// BAD: 3 lookups × N iterations
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value)
}

// GOOD: 1 lookup total
const value = obj.config.settings.value
const len = arr.length
for (let i = 0; i < len; i++) process(value)
```

---

## 11. Hoist RegExp Creation

Don't create RegExp inside render.

```tsx
// BAD: new RegExp every render
const regex = new RegExp(`(${query})`, 'gi')

// GOOD: memoize
const regex = useMemo(() => new RegExp(`(${query})`, 'gi'), [query])
```

---

## 12. Batch DOM CSS Changes

Group CSS changes via classes to minimize reflows.

```typescript
// BAD: multiple reflows
el.style.width = '100px'
el.style.height = '200px'

// GOOD: single reflow
el.classList.add('highlighted-box')
// or
el.style.cssText = 'width: 100px; height: 200px;'
```
