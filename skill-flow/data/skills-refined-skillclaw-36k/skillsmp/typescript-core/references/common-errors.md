# Common TypeScript Errors & Solutions

Quick reference for resolving frequent TypeScript compilation errors.

## Type Assignment Errors

### Error: Type 'X' is not assignable to type 'Y'

**Cause**: Attempting to assign a value of one type to a variable/parameter expecting a different type.

**Solutions**:
1. Check if the types should actually match - fix the assignment
2. Use type assertion if you're certain: `value as TargetType`
3. Add type guards to narrow the type before assignment
4. Use union types if multiple types are valid: `X | Y`

**Example**:
```ts
// Error
const num: number = "123";

// Fix 1: Correct the value
const num: number = 123;

// Fix 2: Parse if needed
const num: number = parseInt("123");
```

### Error: Object is possibly 'null' or 'undefined'

**Cause**: Strict null checks are enabled (which they should be) and you're accessing a value that might be null/undefined.

**Solutions**:
1. Use optional chaining: `obj?.property`
2. Use nullish coalescing: `value ?? defaultValue`
3. Add explicit null check: `if (value !== null) { ... }`
4. Use non-null assertion if certain: `value!` (use sparingly)
5. Use `Maybe` from True Myth for better safety

**Example**:
```ts
// Error
function getUserName(user: User | null) {
  return user.name; // Error: Object is possibly 'null'
}

// Fix 1: Optional chaining
function getUserName(user: User | null) {
  return user?.name;
}

// Fix 2: Null check
function getUserName(user: User | null) {
  if (user === null) return undefined;
  return user.name;
}

// Fix 3: True Myth Maybe
function getUserName(user: User | null): Maybe<string> {
  return Maybe.of(user).map(u => u.name);
}
```

### Error: Property 'X' does not exist on type 'Y'

**Cause**: Attempting to access a property that isn't defined on the type.

**Solutions**:
1. Check if property name is spelled correctly
2. Ensure type definition includes the property
3. Use type guards to narrow union types
4. Use index signatures if accessing dynamic properties
5. Add the property to the interface/type definition

**Example**:
```ts
// Error
interface User {
  name: string;
}
const user: User = { name: "Alice" };
console.log(user.age); // Error: Property 'age' does not exist

// Fix 1: Add property to interface
interface User {
  name: string;
  age?: number; // Optional if not always present
}

// Fix 2: Use type assertion if dynamic
interface User {
  name: string;
  [key: string]: unknown; // Index signature
}
```

## Function & Parameter Errors

### Error: Argument of type 'X' is not assignable to parameter of type 'Y'

**Cause**: Passing wrong type to a function parameter.

**Solutions**:
1. Pass the correct type
2. Update function signature to accept the actual type
3. Transform the value before passing: `parseInt()`, `.toString()`, etc.
4. Use type guards to ensure correct type before calling

**Example**:
```ts
function greet(name: string) {
  console.log(`Hello, ${name}`);
}

// Error
greet(123);

// Fix 1: Pass correct type
greet("Alice");

// Fix 2: Transform the value
greet(String(123));

// Fix 3: Update function signature
function greet(name: string | number) {
  console.log(`Hello, ${name}`);
}
```

### Error: A function whose declared type is neither 'void' nor 'any' must return a value

**Cause**: Function declares a return type but some code paths don't return a value.

**Solutions**:
1. Ensure all code paths return appropriate value
2. Change return type to include `undefined` if some paths don't return
3. Add default return statement at end of function
4. Use `noImplicitReturns: true` is working correctly - fix the logic

**Example**:
```ts
// Error
function getDiscount(amount: number): number {
  if (amount > 100) {
    return 10;
  }
  // Missing return for other cases
}

// Fix 1: Add return for all paths
function getDiscount(amount: number): number {
  if (amount > 100) {
    return 10;
  }
  return 0;
}

// Fix 2: Update return type if undefined is valid
function getDiscount(amount: number): number | undefined {
  if (amount > 100) {
    return 10;
  }
}
```

## Array & Index Access Errors

### Error: Element implicitly has an 'any' type because expression of type 'X' can't be used to index type 'Y'

**Cause**: Trying to index an object/array with a type that TypeScript can't verify.

**Solutions**:
1. Use `as const` for literal types
2. Add index signature to type definition
3. Use `Record<K, V>` type for objects used as maps
4. Type assert the index if certain it's valid
5. Use type guards to narrow the index type

**Example**:
```ts
// Error
const config = {
  dev: "http://localhost",
  prod: "https://api.example.com"
};

function getUrl(env: string) {
  return config[env]; // Error: can't index with string
}

// Fix 1: Use specific type for parameter
type Env = "dev" | "prod";
function getUrl(env: Env) {
  return config[env];
}

// Fix 2: Add index signature
const config: Record<string, string> = {
  dev: "http://localhost",
  prod: "https://api.example.com"
};

// Fix 3: Type guard
function getUrl(env: string) {
  if (env === "dev" || env === "prod") {
    return config[env];
  }
  throw new Error(`Unknown env: ${env}`);
}
```

### Error: Object is possibly 'undefined' (array access)

**Cause**: `noUncheckedIndexedAccess` is enabled (good!) and array/object access might return undefined.

**Solutions**:
1. Check for undefined: `if (arr[0] !== undefined) { ... }`
2. Use optional chaining: `arr[0]?.property`
3. Provide default: `arr[0] ?? defaultValue`
4. Use `.at()` method for clearer intent: `arr.at(0)`

**Example**:
```ts
// Error
function getFirst(arr: string[]) {
  return arr[0].toUpperCase(); // Error: possibly undefined
}

// Fix 1: Check for undefined
function getFirst(arr: string[]) {
  const first = arr[0];
  if (first === undefined) {
    throw new Error("Array is empty");
  }
  return first.toUpperCase();
}

// Fix 2: Use Maybe
function getFirst(arr: string[]): Maybe<string> {
  return Maybe.of(arr[0]).map(s => s.toUpperCase());
}

// Fix 3: Provide default
function getFirst(arr: string[]) {
  return (arr[0] ?? "").toUpperCase();
}
```

## Generic & Type Parameter Errors

### Error: Type 'X' does not satisfy the constraint 'Y'

**Cause**: Generic type parameter doesn't meet the required constraints.

**Solutions**:
1. Ensure the type passed meets the constraint
2. Update the constraint to match actual usage
3. Add properties/methods to the type to satisfy constraint

**Example**:
```ts
// Error
function getLength<T extends { length: number }>(item: T) {
  return item.length;
}

getLength(123); // Error: number doesn't have length

// Fix: Pass a type with length
getLength("hello");
getLength([1, 2, 3]);

// Or update constraint if needed
function getLength<T>(item: T): number {
  if (typeof item === "string" || Array.isArray(item)) {
    return item.length;
  }
  return 0;
}
```

## Module & Import Errors

### Error: Cannot find module 'X' or its corresponding type declarations

**Cause**: Module doesn't exist, isn't installed, or lacks type definitions.

**Solutions**:
1. Install the module: `pnpm add module-name`
2. Install types if available: `pnpm add -D @types/module-name`
3. Create a declaration file if no types exist: `module-name.d.ts`
4. Check module resolution settings in tsconfig.json

**Example**:
```ts
// Error
import express from 'express'; // Cannot find module

// Fix 1: Install the package
// pnpm add express

// Fix 2: Install types
// pnpm add -D @types/express

// Fix 3: Create declaration file if no types available
// In src/types/module-name.d.ts:
declare module 'module-name' {
  export function someFunction(): void;
}
```

## Class & Inheritance Errors

### Error: Property 'X' has no initializer and is not definitely assigned in the constructor

**Cause**: Class property isn't initialized (strict property initialization).

**Solutions**:
1. Initialize in declaration: `property: Type = defaultValue;`
2. Initialize in constructor
3. Mark as optional: `property?: Type;`
4. Use definite assignment assertion if certain it's assigned: `property!: Type;`

**Example**:
```ts
// Error
class User {
  name: string; // Error: no initializer
}

// Fix 1: Initialize in declaration
class User {
  name: string = "";
}

// Fix 2: Initialize in constructor
class User {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}

// Fix 3: Make optional
class User {
  name?: string;
}

// Fix 4: Use constructor parameter properties
class User {
  constructor(public name: string) {}
}
```

## Async & Promise Errors

### Error: 'await' expressions are only allowed within async functions

**Cause**: Using `await` in non-async function.

**Solutions**:
1. Mark function as `async`
2. Use `.then()` instead of `await` if can't make async
3. Wrap in async IIFE if in top-level code (or use top-level await in modules)

**Example**:
```ts
// Error
function fetchData() {
  const data = await fetch('/api'); // Error
}

// Fix: Mark as async
async function fetchData() {
  const data = await fetch('/api');
}
```

### Error: Floating promises (ESLint)

**Cause**: Promise not awaited or handled, potentially losing errors.

**Solutions**:
1. `await` the promise
2. Add `.catch()` handler
3. Use `void` prefix if intentionally not handling: `void myAsync();`
4. Return the promise if caller should handle

**Example**:
```ts
// Error (ESLint)
async function processAll(items: Item[]) {
  items.forEach(item => processItem(item)); // Floating promise
}

// Fix 1: Use for...of with await
async function processAll(items: Item[]) {
  for (const item of items) {
    await processItem(item);
  }
}

// Fix 2: Use Promise.all for parallel
async function processAll(items: Item[]) {
  await Promise.all(items.map(item => processItem(item)));
}

// Fix 3: If intentional (rare), use void
function processAll(items: Item[]) {
  items.forEach(item => void processItem(item));
}
```

## Quick Diagnostic Tips

1. **Read the full error message** - TS errors include file, line, and often suggestions
2. **Check the type inference** - Hover over variables in your IDE to see inferred types
3. **Use type annotations** - Add explicit types to help TS understand intent
4. **Enable all strict flags** - More errors upfront means fewer runtime issues
5. **Check tsconfig.json** - Ensure strict mode and all recommended flags are enabled
6. **Use Effect/Result types** - Prefer structured error handling over throwing exceptions
