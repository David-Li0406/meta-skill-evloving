---
name: "typescript"
paths: "**/*.ts"
alwaysApply: true
description: Contains rules that MUST ALWAYS be applied to EVERY TypeScript file. Covers method definitions, constants, imports, and type safety. CRITICAL INSTRUCTION You MUST ALWAYS use this skill before editing/writing any file matching "**/*.ts".
---

# TypeScript Coding Rules

## Type Safety (CRITICAL)

**This is the most important section. Type safety is non-negotiable.**

### Never use `any`

The `any` type completely bypasses TypeScript's type system. You MUST NOT use it under any circumstances.

### Avoid `unknown` without narrowing

When you receive `unknown`, you MUST narrow it before use:

```ts
// ❌ BAD: Using unknown without narrowing
function handle(input: unknown) {
  return input.toString(); // Error or unsafe
}

// ✅ GOOD: Narrow with type guards
function handle(input: unknown): string {
  if (typeof input === "string") {
    return input;
  }
  if (typeof input === "number") {
    return String(input);
  }
  throw new Error("Unsupported type");
}
```

### Never use non-null assertions (`!`)

The `!` operator is **FORBIDDEN**. Always use proper type guards or optional chaining.

```ts
// ❌ WRONG
const name = user!.name;

// ✅ CORRECT
if (!user) {
  throw new Error("User is required");
}
const name = user.name;
```

## Method Definition

Always use object as method parameter to have named keys:

```ts
// ❌ BAD
function createUser(name: string, age: number, email: string) {}

// ✅ GOOD
function createUser({
  name,
  age,
  email,
}: {
  name: string;
  age: number;
  email: string;
}) {}
```

## Number Constants

Always use constants for magic numbers:

```ts
// ❌ BAD
bcrypt.hash(password, 10);

// ✅ GOOD
const SALT_ROUNDS = 10;
bcrypt.hash(password, SALT_ROUNDS);
```

## Node Stdlib Imports

Always use the `node:` prefix for stdlib imports:

```ts
// ❌ BAD
import assert from "assert";
import fs from "fs/promises";

// ✅ GOOD
import assert from "node:assert";
import fs from "node:fs/promises";
```

## Type Imports

If you import only a type, use the `type` modifier:

```ts
// ✅ GOOD
import type { UserRole } from "./users";

// or
import { User, type UserRole } from "./users";
```

## Exhaustive Type Checking

Always use exhaustive type checking for union types in switch statements:

```ts
type Status = "pending" | "approved" | "rejected";

function handleStatus(status: Status): string {
  switch (status) {
    case "pending":
      return "Processing...";
    case "approved":
      return "Approved!";
    case "rejected":
      return "Rejected.";
    default:
      // Ensure all cases are handled
      status satisfies never;
      throw new Error(`Unhandled status: ${status}`);
  }
}
```

This pattern ensures that if a new value is added to the union type, TypeScript will show a compile-time error until all cases are handled.
