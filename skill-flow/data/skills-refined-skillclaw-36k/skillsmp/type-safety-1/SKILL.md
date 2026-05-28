---
name: type-safety
description: TypeScript type system best practices. Detect unsafe type usage, enforce strict mode, and prevent runtime type errors.
priority: critical
rule_count: 10
sources:
  - "Effective TypeScript (Dan Vanderkam)"
  - "TypeScript Handbook (Official)"
  - "Programming TypeScript (Boris Cherny)"
---

# Type Safety - TypeScript Best Practices

Ensure type-safe code by avoiding `any`, using proper type guards, and enabling strict mode.

## When to Use

- Writing new TypeScript code
- Reviewing code for type safety issues
- Migrating JavaScript to TypeScript
- Debugging type-related runtime errors

**Trigger Phrases:**
- "Check for type safety issues"
- "Review TypeScript types"
- "Find unsafe type usage"
- "Is this type-safe?"

## Rules Overview

### Critical (3 rules)
These prevent runtime errors and type-related bugs:

1. **critical-any-escape-hatch** - Avoid `any`, use `unknown` or proper types
2. **critical-type-assertion-unsafe** - Prefer type guards over assertions (`as`)
3. **critical-null-undefined-confusion** - Distinguish `null` from `undefined` correctly

### High Priority (4 rules)
Improve type safety and catch errors at compile time:

4. **high-strict-mode-disabled** - Always enable `strict: true` in tsconfig
5. **high-implicit-any** - All function parameters must have explicit types
6. **high-type-narrowing** - Use discriminated unions instead of type assertions
7. **high-optional-chaining-abuse** - Don't use `?.` to hide type issues

### Medium Priority (3 rules)
Code quality and maintainability:

8. **medium-generic-constraints** - Constrain generic types properly
9. **medium-index-signatures** - Prefer mapped types over index signatures
10. **medium-type-vs-interface** - Use interfaces for object shapes, types for unions

---

## Rule Details

### 1. critical-any-escape-hatch

**Why it matters:** `any` disables type checking, defeating TypeScript's purpose.

**Detection:**
- Search for `: any` in type annotations
- Look for implicit `any` warnings
- Check for `as any` type assertions

**❌ Incorrect:**
```typescript
function processData(data: any) {
  return data.value.toUpperCase(); // No type safety!
}

// Runtime error if data.value is not a string
processData({ value: 123 });
```

**✅ Correct:**
```typescript
interface DataWithValue {
  value: string;
}

function processData(data: DataWithValue) {
  return data.value.toUpperCase(); // Type-safe!
}

// Or use unknown for truly dynamic data
function processUnknown(data: unknown) {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    const obj = data as { value: unknown };
    if (typeof obj.value === 'string') {
      return obj.value.toUpperCase();
    }
  }
  throw new Error('Invalid data structure');
}
```

**Impact:** HIGH - Prevents entire classes of runtime errors

**Reference:** Effective TypeScript, Item 38: Use the Narrowest Possible Scope for any Types

---

### 2. critical-type-assertion-unsafe

**Why it matters:** Type assertions (`as Type`) bypass type checking and can hide bugs.

**Detection:**
- Look for `as SomeType` in code
- Check for `!` non-null assertions
- Search for angle bracket assertions `<Type>`

**❌ Incorrect:**
```typescript
async function getUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();
  return data as User; // Unsafe! No runtime validation
}

// What if API returns different shape?
const user = await getUser('123');
console.log(user.email.toUpperCase()); // Runtime error if email is missing
```

**✅ Correct:**
```typescript
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'email' in obj &&
    typeof (obj as any).email === 'string'
  );
}

async function getUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();
  
  if (!isUser(data)) {
    throw new Error('Invalid user data from API');
  }
  
  return data; // Type-safe!
}
```

**Impact:** HIGH - Prevents runtime errors from API changes

**Reference:** Effective TypeScript, Item 9: Prefer Type Declarations to Type Assertions

---

### 3. critical-null-undefined-confusion

**Why it matters:** Mixing `null` and `undefined` leads to subtle bugs and unclear semantics.

**Detection:**
- Look for `value == null` (double equals)
- Check for inconsistent null/undefined handling
- Search for `|| undefined` or `|| null` patterns

**❌ Incorrect:**
```typescript
interface User {
  name: string;
  age: number | null | undefined; // What's the difference?
}

function greet(user: User) {
  // Unclear what null vs undefined means
  if (user.age == null) {
    return `Hello ${user.name}`;
  }
  return `Hello ${user.name}, age ${user.age}`;
}
```

**✅ Correct:**
```typescript
interface User {
  name: string;
  age?: number; // undefined = not provided, null = explicitly no value
}

function greet(user: User) {
  if (user.age === undefined) {
    return `Hello ${user.name}`;
  }
  return `Hello ${user.name}, age ${user.age}`;
}

// Or be explicit about semantics
interface UserWithAge {
  name: string;
  age: number | null; // null = user declined to provide age
}
```

**Impact:** MEDIUM-HIGH - Improves code clarity and prevents edge case bugs

**Reference:** Effective TypeScript, Item 37: Consider Brands for Nominal Typing

---

### 4. high-strict-mode-disabled

**Why it matters:** Strict mode catches many common bugs at compile time.

**Detection:**
- Check `tsconfig.json` for `"strict": false` or missing
- Look for disabled strict flags

**❌ Incorrect:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs"
    // Missing "strict": true
  }
}
```

**✅ Correct:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true
  }
}
```

**Impact:** HIGH - Enables all type safety features

**Reference:** TypeScript Handbook: Compiler Options

---

### 5. high-implicit-any

**Why it matters:** Implicit `any` silently disables type checking for parameters.

**Detection:**
- Enable `noImplicitAny` in tsconfig
- Compiler will flag all implicit any

**❌ Incorrect:**
```typescript
function multiply(a, b) { // Implicit any!
  return a * b;
}

multiply('5', '10'); // Returns '510' string concatenation!
```

**✅ Correct:**
```typescript
function multiply(a: number, b: number): number {
  return a * b;
}

// multiply('5', '10'); // Compile error!
```

**Impact:** HIGH - Catches type errors at function boundaries

**Reference:** Effective TypeScript, Item 2: Know Which TypeScript Options You're Using

---

### 6. high-type-narrowing

**Why it matters:** Discriminated unions are safer than type assertions.

**Detection:**
- Look for `as` casts after type checks
- Check for manual type discrimination

**❌ Incorrect:**
```typescript
type Shape = Circle | Square;

function getArea(shape: Shape) {
  if ('radius' in shape) {
    return Math.PI * (shape as Circle).radius ** 2;
  }
  return (shape as Square).size ** 2;
}
```

**✅ Correct:**
```typescript
interface Circle {
  kind: 'circle'; // Discriminant
  radius: number;
}

interface Square {
  kind: 'square'; // Discriminant
  size: number;
}

type Shape = Circle | Square;

function getArea(shape: Shape): number {
  switch (shape.kind) {
    case 'circle':
      return Math.PI * shape.radius ** 2; // Type narrowed!
    case 'square':
      return shape.size ** 2;
  }
}
```

**Impact:** MEDIUM-HIGH - Improves type safety and readability

**Reference:** Effective TypeScript, Item 22: Understand Type Narrowing

---

### 7. high-optional-chaining-abuse

**Why it matters:** Optional chaining (`?.`) can hide missing data issues.

**Detection:**
- Look for excessive `?.` usage
- Check if required data is marked optional

**❌ Incorrect:**
```typescript
interface User {
  profile?: {
    email?: string;
  };
}

function sendEmail(user: User) {
  // Silently does nothing if email is missing!
  const email = user.profile?.email;
  if (email) {
    send(email);
  }
}
```

**✅ Correct:**
```typescript
interface User {
  profile: {
    email: string; // Required!
  };
}

function sendEmail(user: User) {
  // Guaranteed to have email
  send(user.profile.email);
}

// Or make it explicit
function sendEmailIfAvailable(user: User) {
  if (user.profile?.email) {
    send(user.profile.email);
  } else {
    throw new Error('User email is required');
  }
}
```

**Impact:** MEDIUM - Prevents silent failures

**Reference:** Programming TypeScript, Chapter 6: Advanced Types

---

### 8. medium-generic-constraints

**Why it matters:** Unconstrained generics can accept any type, defeating type safety.

**Detection:**
- Look for generic `<T>` without constraints
- Check if generic is used without type operations

**❌ Incorrect:**
```typescript
function getProperty<T>(obj: T, key: string) {
  return obj[key]; // Error: Element implicitly has 'any' type
}
```

**✅ Correct:**
```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key]; // Type-safe!
}

const user = { name: 'Alice', age: 30 };
const name = getProperty(user, 'name'); // string
// getProperty(user, 'invalid'); // Compile error
```

**Impact:** MEDIUM - Improves generic function safety

**Reference:** Effective TypeScript, Item 14: Use Type Operations and Generics

---

### 9. medium-index-signatures

**Why it matters:** Index signatures allow any string key, losing type safety.

**Detection:**
- Look for `[key: string]: any`
- Check for dynamic property access

**❌ Incorrect:**
```typescript
interface Config {
  [key: string]: string; // Too permissive
}

const config: Config = {
  apiUrl: 'https://api.example.com',
  timeout: '5000'
};

// Typo not caught!
console.log(config.apiUrll);
```

**✅ Correct:**
```typescript
type ConfigKeys = 'apiUrl' | 'timeout' | 'retries';
type Config = Record<ConfigKeys, string>;

const config: Config = {
  apiUrl: 'https://api.example.com',
  timeout: '5000',
  retries: '3'
};

// config.apiUrll; // Compile error!
```

**Impact:** MEDIUM - Catches typos and wrong keys

**Reference:** Effective TypeScript, Item 15: Use Index Signatures for Dynamic Data

---

### 10. medium-type-vs-interface

**Why it matters:** Choosing the right construct improves code clarity.

**Detection:**
- Check for `type` used for simple object shapes
- Look for `interface` used for unions

**❌ Incorrect:**
```typescript
// Using type for object shape (less extensible)
type User = {
  name: string;
  email: string;
};

// Using interface for union (not possible)
// interface Status = 'pending' | 'complete'; // Error!
```

**✅ Correct:**
```typescript
// Use interface for object shapes (can be extended)
interface User {
  name: string;
  email: string;
}

interface AdminUser extends User {
  role: 'admin';
}

// Use type for unions, intersections, mapped types
type Status = 'pending' | 'complete' | 'failed';
type Readonly<T> = { readonly [K in keyof T]: T[K] };
```

**Impact:** LOW-MEDIUM - Improves code organization

**Reference:** Effective TypeScript, Item 13: Know the Differences Between type and interface

---

## Usage Examples

**Check file for type safety issues:**
```
Review this TypeScript file for type safety problems
```

**Review API integration:**
```
Check this API code for unsafe type assertions
```

**Audit strict mode:**
```
Verify this project uses TypeScript strict mode
```

## Summary

Type safety is the foundation of TypeScript's value. These 10 rules ensure:
- ✅ No `any` escape hatches
- ✅ Type guards instead of assertions
- ✅ Strict mode enabled
- ✅ Proper generic constraints
- ✅ Clear null/undefined semantics

Following these rules prevents runtime type errors and improves code maintainability.
