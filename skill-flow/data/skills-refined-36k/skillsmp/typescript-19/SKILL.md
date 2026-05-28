---
name: typescript
description: "TypeScript development process and type safety review. Use when writing TypeScript code, reviewing TypeScript PRs for type safety, configuring tsconfig.json or ESLint, debugging type errors, or migrating JavaScript to TypeScript. Also use when encountering `any` types, type assertions (`as Type`), runtime type checking, `@ts-ignore` comments, or when types feel 'too complex'. Essential for discriminated unions, generics, conditional types, and strict mode configuration."
---

# TypeScript Skill

## Overview

TypeScript's value comes from catching errors at compile time, not runtime. This skill guides systematic use of TypeScript's type system for safer, more maintainable code.

**Core principle:** If TypeScript can't verify it, neither can you. Use the type system to make invalid states unrepresentable.

## The Type-Safe Development Process

### Phase 1: Design Types First

**Before writing implementation:**

1. **Define Data Shapes**
   - What data flows through this code?
   - What are the possible states?
   - What states are INVALID and shouldn't exist?

2. **Use Discriminated Unions for States**
   ```typescript
   // Make invalid states unrepresentable
   type RequestState =
     | { status: 'idle' }
     | { status: 'loading' }
     | { status: 'success'; data: User }
     | { status: 'error'; error: Error };
   ```

3. **Define Function Signatures**
   - What goes in? What comes out?
   - What errors can occur?
   - See `references/advanced-types.md` for patterns

### Phase 2: Implement with Strict Mode

**Let the compiler guide you:**

1. **Enable All Strict Flags**
   ```json
   {
     "compilerOptions": {
       "strict": true,
       "noUncheckedIndexedAccess": true,
       "noImplicitReturns": true
     }
   }
   ```

2. **Fix Errors, Don't Silence Them**
   - Type error = bug waiting to happen
   - `// @ts-ignore` is almost never the answer
   - `any` defeats the purpose of TypeScript

3. **Use Type Narrowing**
   ```typescript
   // Let TypeScript narrow types for you
   if (result.status === 'success') {
     console.log(result.data);  // TypeScript knows data exists
   }
   ```

### Phase 3: Review for Type Safety

**Before approving:**

1. **Check for Type Escapes**
   - Any use of `any`?
   - Any type assertions (`as Type`)?
   - Any `// @ts-ignore` or `// @ts-expect-error`?

2. **Verify Null Handling**
   - Are null/undefined cases handled?
   - Does `strictNullChecks` catch issues?

3. **Test Type Inference**
   - Hover over variables - are types what you expect?
   - Are generics inferring correctly?

## Red Flags - STOP and Fix

### Type Safety Red Flags

```
- any type (find the real type)
- Type assertions: value as Type (use type guards)
- // @ts-ignore (fix the underlying issue)
- ! non-null assertion (handle the null case)
- Object or {} as type (be specific)
- Function type without parameters (define signature)
```

### Code Quality Red Flags

```
- Deeply nested generics (simplify with type aliases)
- Types duplicated across files (centralize in types/)
- Runtime type checking (let TypeScript do it)
- Optional chaining everywhere (fix the types)
- Type definitions longer than implementation (too complex)
```

### Configuration Red Flags

```
- strict: false (enable it)
- skipLibCheck: true without good reason
- any in function returns
- Missing return types on public functions
- No ESLint TypeScript rules
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "The type is too complex" | Simplify the design, not the types. |
| "I'll fix the types later" | Later never comes. Fix now. |
| "It works at runtime" | TypeScript catches bugs before runtime. |
| "any is fine here" | any disables TypeScript. Find the real type. |
| "The library has bad types" | Write better types or use unknown. |
| "Strict mode is too annoying" | Those "annoyances" are bugs. |

## Type Safety Checklist

Before approving TypeScript code:

- [ ] **No `any`**: All types are specific
- [ ] **No assertions**: Using type guards instead of `as`
- [ ] **Null handled**: Optional values properly checked
- [ ] **Strict mode**: All strict flags enabled
- [ ] **No ignores**: No `@ts-ignore` or `@ts-expect-error`
- [ ] **Interfaces defined**: Data shapes are explicit
- [ ] **Errors typed**: Error handling is type-safe

## Quick Type Patterns

### Prefer `unknown` over `any`

```typescript
// ❌ any bypasses all checking
function parse(json: string): any { ... }

// ✅ unknown requires narrowing
function parse(json: string): unknown { ... }
const data = parse(input);
if (isUser(data)) {
  console.log(data.name);  // Safe
}
```

### Use Type Guards

```typescript
// ❌ Type assertion (unsafe)
const user = response.data as User;

// ✅ Type guard (safe)
function isUser(data: unknown): data is User {
  return typeof data === 'object' && data !== null && 'id' in data;
}
if (isUser(response.data)) {
  const user = response.data;  // Typed correctly
}
```

### Use Discriminated Unions

```typescript
// ❌ Optional fields (any combination valid)
interface Result {
  data?: User;
  error?: Error;
  loading?: boolean;
}

// ✅ Discriminated union (only valid states)
type Result =
  | { status: 'loading' }
  | { status: 'success'; data: User }
  | { status: 'error'; error: Error };
```

## Quick Commands

```bash
# Type check without emitting
npx tsc --noEmit

# Type check with strict
npx tsc --noEmit --strict

# Find any types
grep -r ": any" src/

# ESLint with TypeScript
npx eslint . --ext .ts,.tsx
```

## References

Detailed patterns and examples in `references/`:
- `advanced-types.md` - Generics, conditional types, mapped types
- `typescript-config.md` - tsconfig.json best practices
- `migration-guide.md` - JavaScript to TypeScript migration
