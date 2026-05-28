---
name: js-dev
description: |
  JavaScript ES6+ patterns, async/await, modules, and modern JS best practices.
  WHEN: Writing JavaScript code, using ES6+ features (destructuring, spread, arrow functions), async/await patterns, array methods, module imports/exports, .js files.
  WHEN NOT: TypeScript code (use ts-dev), Vue-specific patterns (use vuejs-dev), Node.js backend APIs (use python-backend equivalent for Node).
---

# JavaScript Development

Modern JavaScript (ES6+) patterns and best practices.

## Variables & Constants

```javascript
// const for values that won't be reassigned
const API_URL = 'https://api.example.com'
const config = { theme: 'dark' }  // object reference is constant

// let for values that will change
let count = 0
let isLoading = false

// Never use var (function-scoped, hoisted)
```

## Destructuring

```javascript
// Object destructuring
const { name, age, city = 'Unknown' } = user
const { data: userData, error } = response

// Array destructuring
const [first, second, ...rest] = items
const [x, , z] = coordinates  // skip elements

// Function parameters
function createUser({ name, email, role = 'user' }) {
  return { name, email, role }
}
```

## Spread & Rest

```javascript
// Spread: expand arrays/objects
const merged = { ...defaults, ...options }
const allItems = [...oldItems, newItem]
const copy = [...original]

// Rest: collect remaining
function log(message, ...args) {
  console.log(message, ...args)
}
```

## Arrow Functions

```javascript
// Concise syntax
const double = x => x * 2
const add = (a, b) => a + b
const getUser = () => ({ name: 'John' })  // return object

// When to use traditional function
// - Need 'this' binding
// - Need 'arguments' object
// - Object methods (sometimes)
```

## Array Methods

```javascript
const items = [1, 2, 3, 4, 5]

// Transform
const doubled = items.map(x => x * 2)

// Filter
const evens = items.filter(x => x % 2 === 0)

// Find
const found = items.find(x => x > 3)      // first match or undefined
const index = items.findIndex(x => x > 3) // index or -1

// Check
const hasEven = items.some(x => x % 2 === 0)  // at least one
const allPositive = items.every(x => x > 0)   // all match

// Reduce
const sum = items.reduce((acc, x) => acc + x, 0)

// Chain methods
const result = items
  .filter(x => x > 2)
  .map(x => x * 2)
  .reduce((acc, x) => acc + x, 0)
```

## Async/Await

```javascript
// Async function
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`)
    if (!response.ok) throw new Error('Failed to fetch')
    return await response.json()
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}

// Parallel execution
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
])

// With error handling per promise
const results = await Promise.allSettled([
  fetchUsers(),
  fetchPosts()
])
// results: [{ status: 'fulfilled', value }, { status: 'rejected', reason }]
```

## Promises

```javascript
// Create promise
const delay = ms => new Promise(resolve => setTimeout(resolve, ms))

// Chain
fetchData()
  .then(data => process(data))
  .then(result => save(result))
  .catch(error => handleError(error))
  .finally(() => cleanup())
```

## Modules

```javascript
// Named exports
export const API_URL = '...'
export function fetchData() { }
export class UserService { }

// Default export
export default function main() { }

// Import
import main, { API_URL, fetchData } from './module.js'
import * as utils from './utils.js'

// Dynamic import
const module = await import('./heavy-module.js')
```

## Optional Chaining & Nullish Coalescing

```javascript
// Optional chaining (?.)
const city = user?.address?.city
const firstItem = items?.[0]
const result = obj.method?.()

// Nullish coalescing (??) - only null/undefined
const value = input ?? 'default'

// vs OR (||) - all falsy values
const value = input || 'default'  // 0, '', false also trigger default
```

## Template Literals

```javascript
const name = 'World'
const greeting = `Hello, ${name}!`

// Multiline
const html = `
  <div class="card">
    <h1>${title}</h1>
    <p>${description}</p>
  </div>
`

// Tagged templates
const styled = css`color: ${color};`
```

## Classes

```javascript
class User {
  // Private field
  #password

  // Static property
  static count = 0

  constructor(name, email) {
    this.name = name
    this.email = email
    this.#password = ''
    User.count++
  }

  // Getter
  get displayName() {
    return `${this.name} <${this.email}>`
  }

  // Method
  async save() {
    return await api.saveUser(this)
  }

  // Static method
  static create(data) {
    return new User(data.name, data.email)
  }
}
```

## Error Handling

```javascript
// Custom errors
class ValidationError extends Error {
  constructor(message, field) {
    super(message)
    this.name = 'ValidationError'
    this.field = field
  }
}

// Try-catch
try {
  const data = JSON.parse(input)
} catch (error) {
  if (error instanceof SyntaxError) {
    console.error('Invalid JSON')
  } else {
    throw error
  }
}
```

## Common Patterns

### Debounce

```javascript
function debounce(fn, delay) {
  let timeoutId
  return (...args) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn(...args), delay)
  }
}
```

### Deep Clone

```javascript
const clone = structuredClone(original)
// or for simple objects
const clone = JSON.parse(JSON.stringify(original))
```

### Object Utilities

```javascript
// Check property exists
if ('name' in obj) { }
if (Object.hasOwn(obj, 'name')) { }

// Get entries/keys/values
Object.entries(obj)  // [[key, value], ...]
Object.keys(obj)     // [key, ...]
Object.values(obj)   // [value, ...]

// Create from entries
Object.fromEntries([['a', 1], ['b', 2]])  // { a: 1, b: 2 }
```

## Anti-Patterns to Avoid

1. **== instead of ===** → Always use strict equality
2. **Callback hell** → Use async/await or Promise chains
3. **Mutating function arguments** → Return new values
4. **for...in on arrays** → Use for...of or array methods
5. **Global variables** → Use modules and proper scoping
