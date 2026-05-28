---
name: typescript
description: Use when writing or reviewing TypeScript code, or when the user mentions TypeScript, strict typing, type errors, or type safety.
---

# TypeScript: Strict Typing and Readability

Guidelines for writing maintainable, well-typed TypeScript code.

## Core Principles

1. **Avoid `any` and `unknown`** — Use precise, explicit types at all times
2. **Never silence type errors** — Don't use broad assertions like `as any` just to "make it work"
3. **Optimize for maintainability** — Prefer clear, easy-to-read code over clever type gymnastics
4. **Fail fast** — Validate inputs and fail immediately on invalid data rather than using placeholders

## Type Safety Rules

### Bad: Using `any` or `unknown`

```typescript
function processData(data: any) {
  return data.someProperty;
}

const result = apiCall() as any;
```

### Good: Using explicit types

```typescript
interface DataStructure {
  someProperty: string;
  otherProperty: number;
}

function processData(data: DataStructure): string {
  return data.someProperty;
}

interface ApiResponse {
  status: number;
  data: DataStructure;
}

const result: ApiResponse = await apiCall();
```

## When You Think You Need `any`/`unknown`

Investigate and fix the root cause instead:

| Problem | Solution |
|---------|----------|
| Upstream types missing/incorrect | Add or fix them |
| Invalid usage or design | Correct the code |
| Third-party types wrong | Augment types or contribute a fix |

**Last resort only**: Use `any`/`unknown` when avoiding them requires disproportionate, complex typings. Keep usage minimal and well-reasoned.

## Type Assertions

### Bad: Broad type assertions

```typescript
const value = (someFunction() as any).property;
const data = response as unknown as MyType;
```

### Good: Type guards and validation

```typescript
function isMyType(value: unknown): value is MyType {
  return (
    typeof value === 'object' &&
    value !== null &&
    'expectedProperty' in value
  );
}

const data = someFunction();
if (isMyType(data)) {
  // Now data is typed as MyType
  console.log(data.expectedProperty);
} else {
  throw new Error('Invalid data structure');
}
```

## Generic Types

### Bad: Untyped generics

```typescript
function transform(items: any[]) {
  return items.map(item => item.value);
}
```

### Good: Typed generics

```typescript
interface HasValue<T> {
  value: T;
}

function transform<T>(items: HasValue<T>[]): T[] {
  return items.map(item => item.value);
}
```

## Error Handling

### Bad: Catching without typing

```typescript
try {
  await someOperation();
} catch (error) {
  console.log(error.message); // error is any
}
```

### Good: Typed error handling

```typescript
try {
  await someOperation();
} catch (error) {
  if (error instanceof Error) {
    console.log(error.message);
  } else {
    console.log('Unknown error occurred');
  }
}
```

## When Blocked

If you're blocked from fixing the root cause of a type issue:

1. **Stop and document why** you can't fix it properly
2. **Ask for guidance** rather than using `as any`

## Verification

After making TypeScript changes, always:

1. Run `tsc --noEmit` to check for type errors
2. Fix any type errors before considering the work complete
3. Ensure all type assertions are justified and minimal
