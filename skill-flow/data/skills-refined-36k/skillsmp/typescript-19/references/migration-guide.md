# JavaScript to TypeScript Migration Guide

Migrate JavaScript projects to TypeScript incrementally.

## Migration Strategy

### Phase 1: Setup (Day 1)

```bash
# Install TypeScript
npm install -D typescript @types/node

# Initialize tsconfig
npx tsc --init

# Rename entry files
mv src/index.js src/index.ts
```

Start with loose settings:

```json
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": false,
    "strict": false,
    "noImplicitAny": false
  },
  "include": ["src/**/*"]
}
```

### Phase 2: Add Types Incrementally

1. **Rename .js to .ts file by file**
2. **Add explicit types to function parameters**
3. **Fix errors as they appear**

```typescript
// Before (JavaScript)
function getUser(id) {
  return database.find(u => u.id === id);
}

// After (TypeScript)
interface User {
  id: string;
  name: string;
  email: string;
}

function getUser(id: string): User | undefined {
  return database.find(u => u.id === id);
}
```

### Phase 3: Tighten Strict Mode

Enable flags one at a time:

```json
{
  "compilerOptions": {
    "noImplicitAny": true,      // First
    "strictNullChecks": true,    // Second
    "strictFunctionTypes": true, // Third
    "strict": true               // Finally
  }
}
```

## Common Migration Patterns

### Dynamic Object Access

```typescript
// JavaScript
const value = obj[key];

// TypeScript - add type guard
function hasKey<T extends object>(obj: T, key: PropertyKey): key is keyof T {
  return key in obj;
}

if (hasKey(obj, key)) {
  const value = obj[key];  // Typed correctly
}

// Or use Record
const obj: Record<string, string> = { a: '1', b: '2' };
```

### Event Handlers

```typescript
// JavaScript
element.addEventListener('click', (e) => {
  console.log(e.target.value);
});

// TypeScript
element.addEventListener('click', (e: MouseEvent) => {
  const target = e.target as HTMLInputElement;
  console.log(target.value);
});
```

### API Responses

```typescript
// JavaScript
const response = await fetch('/api/users');
const users = await response.json();

// TypeScript
interface User {
  id: number;
  name: string;
}

const response = await fetch('/api/users');
const users: User[] = await response.json();

// Better: runtime validation with Zod
import { z } from 'zod';

const UserSchema = z.object({
  id: z.number(),
  name: z.string(),
});

const users = z.array(UserSchema).parse(await response.json());
```

### Third-Party Libraries

```bash
# Check for types
npm install -D @types/library-name

# If no types exist, create declaration file
# src/types/library-name.d.ts
declare module 'library-name' {
  export function doSomething(input: string): number;
}
```

## Handling `any`

```typescript
// Start with any to unblock
function legacy(data: any): any {
  // TODO: Add types
}

// Migrate to unknown for safety
function safer(data: unknown): unknown {
  if (typeof data === 'string') {
    return data.toUpperCase();
  }
  throw new Error('Expected string');
}

// Final: proper types
function typed(data: InputType): OutputType {
  return transform(data);
}
```

## Migration Checklist

- [ ] TypeScript installed and configured
- [ ] Build pipeline updated (tsc before bundle)
- [ ] Entry files renamed to .ts
- [ ] Type definitions installed (@types/*)
- [ ] noImplicitAny enabled
- [ ] strictNullChecks enabled
- [ ] Full strict mode enabled
- [ ] No remaining `any` types
- [ ] All tests passing
