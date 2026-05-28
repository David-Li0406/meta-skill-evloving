---
name: coding-standards
description: TypeScript coding standards and best practices.  Use when implementing code, refactoring, writing tests, or reviewing code quality.
---

# Coding Standards

## Core Principles

- **Functional Domain Modeling** design
- Use functions - no `class`
- Algebraic Data Types for type design
- Early return pattern - avoid deep nesting
- Handle errors first
- **Imports**: Same directory → `./`. Cross-directory or global → `@/` aliases

## Type Safety

### Rules

- Never use `any` - define explicit types
- Avoid type assertions (`as`) when possible
- Resolve type errors immediately
- Prefer union types and discriminated unions

### Global Types

Only universal types (e.g., `Result<T, E>`) in `utils/types.ts`

## State Management

- **Derive, Don't Duplicate**: If state B can be computed from state A, compute B from A
- **Pure Functions First**: Extract pure logic into testable functions. Isolate side effects.
- **Tool Selection**: Use framework-appropriate stores (Zustand, Pinia, Nanostores, etc.)
- **Server-driven frameworks**: State lives on server, HTML represents state

## Composable Logic Design

_Applies to: React Hooks, Vue Composables, Svelte Runes, Solid Primitives, etc._

1. **Extract pure logic** - Separate business logic from framework code
2. **Isolate side effects** - Keep I/O separate from pure logic
3. **Accept state as arguments** - Make logic testable
4. **Return computed values** - Return derived state and operations

## Component Architecture Patterns

### Pattern 1: Direct Import

Components directly import stores/utilities/logic.

**Use when:**

- Simple, single-purpose components
- No reuse needs
- Small to medium complexity

**Trade-offs:** Simple, less boilerplate | Harder to test, lower reusability

### Pattern 2: Feature Layer + Presentational Components

Feature layer handles logic, components receive props.

**Use when:**

- Reusable across contexts
- Design systems/Storybook
- Complex business logic
- Clear server/client separation needed

**Trade-offs:** Testable, reusable, clear separation | More boilerplate, can be over-engineering

### Decision

Start with **Pattern 1**. Refactor to **Pattern 2** when needed for reuse, testing, or complexity.

## Error Handling

### Never use exceptions for control flow

### Use Result<T, E> Pattern for:

- Internal logic and domain functions
- Server Actions/route handlers returning success/error
- Hooks/Composables managing operations

### Use try-catch for:

- External operations (I/O, DB, fetch, file system)
- Always log: `console.error(error)` in catch blocks

### Result Pattern Examples

```typescript
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

// Domain function
function parseId(input: unknown): Result<string, "Invalid ID"> {
  return typeof input === "string" && input !== ""
    ? { ok: true, value: input }
    : { ok: false, error: "Invalid ID" };
}

// Server Action (example)
export async function createPost(
  formData: FormData,
): Promise<Result<Post, string>> {
  const title = formData.get("title");
  if (!title) return { ok: false, error: "Title required" };

  try {
    const post = await db.insert({ title });
    return { ok: true, value: post };
  } catch (error) {
    console.error("DB error:", error);
    return { ok: false, error: "Failed to create post" };
  }
}

// Hook/Composable (example)
function useCreatePost() {
  const [result, setResult] = useState<Result<Post, string> | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const create = async (formData: FormData) => {
    setIsLoading(true);
    const res = await createPost(formData);
    setResult(res);
    setIsLoading(false);
    return res;
  };

  return { create, result, isLoading };
}
```

## Comments

### Only for:

- Complex type hints
- Critical non-obvious logic

### Never for:

- Usage examples (use tests instead)
- Redundant descriptions

## Testing Policy

### Minimal Unit Tests Only

- No E2E tests
- Test business logic and critical functions only
- When connecting to API, tests for both normal and abnormal cases
- Skip UI components and trivial code
- Place `*.test.ts(x)` adjacent to source files
- Enable aliases using `vite-tsconfig-paths`

### What to Test

```typescript
// ✅ Test: Business logic
describe("calculateMetrics", () => {
  it("should calculate correctly with valid data", () => {});
  it("should handle edge cases", () => {});
});

// ✅ Test: API calls
describe("fetchUser", () => {
  it("should return user on success", async () => {});
  it("should return error on failure", async () => {});
});

// ❌ Don't test: UI components, trivial functions
```

### Commands

```bash
pnpm test              # Run all tests
pnpm test *.test.tsx   # Run specific test
```

---
