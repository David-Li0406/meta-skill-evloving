---
name: coding-standards
description: Use this skill when writing code in TypeScript, JavaScript, React, or Node.js to ensure consistent quality and adherence to best practices.
---

# Coding Standards & Best Practices

Universal coding standards applicable across all projects.

## Code Quality Principles

### 1. Readability First
- Code is read more than written.
- Use clear variable and function names.
- Prefer self-documenting code over comments.
- Maintain consistent formatting.

### 2. KISS (Keep It Simple, Stupid)
- Implement the simplest solution that works.
- Avoid over-engineering and premature optimization.
- Prioritize easy-to-understand code over clever code.

### 3. DRY (Don't Repeat Yourself)
- Extract common logic into functions.
- Create reusable components.
- Share utilities across modules to avoid copy-paste programming.

### 4. YAGNI (You Aren't Gonna Need It)
- Do not build features before they are needed.
- Avoid speculative generality.
- Add complexity only when required; start simple and refactor when necessary.

## TypeScript/JavaScript Standards

### Variable Naming

```typescript
// ✅ GOOD: Descriptive names
const marketSearchQuery = 'election';
const isUserAuthenticated = true;
const totalRevenue = 1000;

// ❌ BAD: Unclear names
const q = 'election';
const flag = true;
const x = 1000;
```

### Function Naming

```typescript
// ✅ GOOD: Verb-noun pattern
async function fetchMarketData(marketId: string) { }
function calculateSimilarity(a: number[], b: number[]) { }
function isValidEmail(email: string): boolean { }

// ❌ BAD: Unclear or noun-only
async function market(id: string) { }
function similarity(a, b) { }
function email(e) { }
```

### Immutability Pattern (CRITICAL)

```typescript
// ✅ ALWAYS use spread operator
const updatedUser = {
  ...user,
  name: 'New Name'
};

const updatedArray = [...items, newItem];

// ❌ NEVER mutate directly
user.name = 'New Name';  // BAD
items.push(newItem);     // BAD
```

### Error Handling

```typescript
// ✅ GOOD: Comprehensive error handling
async function fetchData(url: string) {
  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    throw new Error('Failed to fetch data');
  }
}

// ❌ BAD: No error handling
async function fetchData(url) {
  const response = await fetch(url);
  return response.json();
}
```

### Async/Await Best Practices

```typescript
// ✅ GOOD: Parallel execution when possible
const [users, markets, stats] = await Promise.all([
  fetchUsers(),
  fetchMarkets(),
  fetchStats()
]);

// ❌ BAD: Sequential when unnecessary
const users = await fetchUsers();
```