---
name: simplicity-principles
description: Use when designing solutions, adding features, or refactoring by applying KISS, YAGNI, and Principle of Least Astonishment to write simple, predictable code.
---

# Simplicity Principles

Write code that is simple, necessary, and unsurprising.

## Three Core Principles

### 1. KISS - Keep It Simple, Stupid

### Simple solutions are better than clever ones

### What Simple Means

- Readable by developers of varying skill levels
- Fewer moving parts and abstractions
- Direct and obvious implementation
- Easy to debug and test
- Minimal cognitive load

### TypeScript Examples

```typescript
// COMPLEX - Over-abstraction
class UserDataManager {
  private dataSource: DataSource;
  private cache: Cache;
  private transformer: DataTransformer;

  async getUser(id: string): Promise<User> {
    const cached = await this.cache.get(id);
    if (cached) return this.transformer.transform(cached);

    const raw = await this.dataSource.fetch(id);
    await this.cache.set(id, raw);
    return this.transformer.transform(raw);
  }
}

// SIMPLE - Direct approach
async function getUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}
// Add cache/transform only when performance demands it
```

```typescript
// COMPLEX - Clever but confusing
const isValid = (x: number) => !!(x >= 0 && x <= 100);
const process = (items: number[]) =>
  items.filter(isValid).reduce((a, b) => a + b, 0);

// SIMPLE - Clear intent
function calculateTotal(scores: number[]): number {
  const validScores = scores.filter((score) => score >= 0 && score <= 100);
  return validScores.reduce((sum, score) => sum + score, 0);
}
```

### KISS Guidelines

- Prefer functions over classes (unless you need state)
- Prefer explicit over implicit
- Prefer boring over clever
- Prefer standard library over custom solutions
- Prefer clear names over short names
- Prefer straightforward logic over "elegant" one-liners

### When NOT to KISS

- Performance-critical code (after profiling proves need)
- Preventing code duplication (after third instance)
- Enforcing constraints (types, validations)

### 2. YAGNI - You Aren't Gonna Need It

### Don't implement features until you actually need them

### Signs You're Violating YAGNI

- "We might need this someday"
- "Let me add flexibility for future use cases"
- "I'll build a generic solution"
- "This could be configurable"

### TypeScript Examples (YAGNI)

```typescript
// YAGNI VIOLATION - Premature generalization
interface DataFetcher<T, P extends object = object> {
  fetch(params: P): Promise<T>;
  cache?(params: P): Promise<void>;
  invalidate?(key: string): Promise<void>;
  prefetch?(params: P[]): Promise<void>;
  // We don't use cache, invalidate, or prefetch yet!
}

// GOOD - Start simple
interface DataFetcher<T> {
  fetch(params: object): Promise<T>;
  // Add methods when we need caching
}
```

```typescript
// YAGNI VIOLATION - Configurable everything
interface ButtonProps {
  onClick: () => void;
  variant?: "primary" | "secondary" | "tertiary" | "ghost" | "outline";
  size?: "xs" | "sm" | "md" | "lg" | "xl";
  shape?: "rounded" | "square" | "pill";
  shadow?: "none" | "sm" | "md" | "lg";
  animation?: "fade" | "slide" | "bounce";
  // Design only uses 2 variants and 1 size!
}

// GOOD - Implement what designs require
interface ButtonProps {
  onClick: () => void;
  variant?: "primary" | "secondary"; // Only what we use
  // Add options when design requires them
}
```

### YAGNI Guidelines

- Implement features when you have a concrete use case, not a hypothetical one
- Delete unused code immediately (it's in git)
- Start with hardcoded values, extract constants when they vary
- Build for today's requirements, refactor for tomorrow's
- Question every "nice to have" and "might need"

### Exceptions to YAGNI

- Security features (implement defense in depth upfront)
- Data migrations (plan schema carefully)
- Public APIs (harder to change later)
- Accessibility (build in from start)

### 3. Principle of Least Astonishment (POLA)

### Code should behave the way users expect it to behave

### What Makes Code Astonishing

- Unexpected side effects
- Inconsistent naming
- Breaking conventions
- Hidden behavior
- Surprising return values

### TypeScript Examples (POLA)

```typescript
// ASTONISHING - Function mutates input
function processTask(gig: Task): Task {
  gig.status = "processed"; // Mutates input!
  gig.processedAt = new Date();
  return gig;
}

// EXPECTED - Pure function
function processTask(gig: Task): Task {
  return {
    ...gig,
    status: "processed",
    processedAt: new Date(),
  };
}
```

```typescript
// ASTONISHING - Inconsistent return types
async function getUser(id: string): Promise<User | null | undefined> {
  // Returns null sometimes, undefined other times, no pattern
}

// EXPECTED - Consistent return
async function getUser(id: string): Promise<User | null> {
  // Always null when not found
}
```

```typescript
// ASTONISHING - Breaking conventions
interface Props {
  onPress?: () => void; // React convention: onX
  clickHandler?: () => void; // Different convention in same interface!
  onTapGesture?: () => void; // Yet another name for same thing!
}

// EXPECTED - Consistent conventions
interface Props {
  onPress?: () => void;
  onLongPress?: () => void;
  onDoublePress?: () => void;
}
```

### POLA Guidelines

- Follow framework conventions (Phoenix, React, Relay)
- Use clear, descriptive names that match behavior
- Return what the function name promises
- Keep side effects explicit or avoid them
- Be consistent within the codebase
- Match platform conventions (iOS, Android, Web)
- Honor principle of least surprise in APIs

### Examples of Good POLA in YourApp

- Command handlers return `{:ok, result}` or `{:error, reason}` (consistent)
- React components with `onPress` not `onClick` (platform convention)
- Ecto changesets don't touch database (pure validation)
- GraphQL mutations clearly named: `createTask`, `updateTask`, `deleteTask`

## Application Checklist

### Before implementing

- [ ] Is this the simplest solution? (KISS)
- [ ] Do we actually need this now? (YAGNI)
- [ ] Will this behavior surprise users? (POLA)

### During implementation

- [ ] Prefer straightforward over clever
- [ ] Implement only what's required
- [ ] Follow established conventions
- [ ] Name things accurately
- [ ] Make side effects explicit

### During code review

- [ ] Is there a simpler approach?
- [ ] Are we building speculative features?
- [ ] Does the API behave as expected?
- [ ] Are conventions followed?

## Red Flags

### KISS Violations

- "Let me show you this clever trick..."
- More than 3 levels of abstraction
- Requires 10-minute explanation
- Uses advanced language features unnecessarily

### YAGNI Violations

- "We might need this later..."
- Unused parameters/options
- Configurable everything
- "Generic framework" for 2 use cases

### POLA Violations

- "Well, technically it does..."
- Inconsistent naming
- Hidden side effects
- Surprising error conditions

## Integration with Existing Skills

### Works with

- `solid-principles`: Simple implementations of SOLID patterns
- `boy-scout-rule`: Simplify when improving code
- `test-driven-development`: Simple code is easier to test
- `typescript-code-quality-enforcer`: Linting enforces consistency

## Remember

> "Simplicity is the ultimate sophistication." - Leonardo da Vinci

- Prefer boring, proven solutions over novel approaches
- Build incrementally based on actual requirements
- Follow conventions so code behaves as expected
- Delete speculative code immediately
- Simple != simplistic (handle errors, edge cases properly)

### When in doubt, choose the simpler path
