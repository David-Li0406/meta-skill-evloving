# Type Strengthening (TypeScript)

Replaces loose types with proper, specific types without altering runtime logic.

## Find Loose Types

```bash
git diff main...HEAD -- <file> | grep -E '(: any|as any|: unknown|as unknown)'
```

## Patterns to Fix

### Replace `any` Types

**Function parameters:**
```typescript
// Before
function process(data: any) {
  return data.name;
}

// After
interface ProcessData { name: string; }
function process(data: ProcessData) {
  return data.name;
}
```

**Infer from usage** - examine how the value is used to determine the correct type.

### Remove Unnecessary Assertions

**Double casting:**
```typescript
// Before
const value = (input as unknown) as string;

// After - fix the source type or use conversion
const value = String(input);
```

**Assertions that match declared type:**
```typescript
// Before
const user: User = response.data as User;

// After (if response.data is already typed)
const user: User = response.data;
```

### Fix Overly Broad Unions

**Narrow string unions:**
```typescript
// Before
function setStatus(status: string) {}

// After
type Status = 'pending' | 'active' | 'completed' | 'failed';
function setStatus(status: Status) {}
```

### Add Missing Type Annotations

**Return types for public functions:**
```typescript
// Before
export function fetchUser(id: string) {
  return api.get(`/users/${id}`);
}

// After
export function fetchUser(id: string): Promise<User> {
  return api.get<User>(`/users/${id}`);
}
```

### Use Generic Constraints

```typescript
// Before
function getProperty<T>(obj: T, key: string): any {
  return obj[key];
}

// After
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

### Fix Event Handler Types

```typescript
// Before
const handleClick = (e: any) => { e.preventDefault(); };

// After
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  e.preventDefault();
};
```

## Finding the Right Type

1. **Check existing types in codebase:**
   ```bash
   grep -r "interface\|type " --include="*.ts" .
   ```

2. **Look at library type definitions:**
   ```bash
   cat node_modules/@types/react/index.d.ts | grep "interface.*Event"
   ```

3. **Use IDE** - hover over values to see inferred types

## Guidelines

- Only change types, not runtime behavior
- Prefer existing types from the project
- Don't over-constrain - types should be as specific as necessary, not more
- Document complex types with JSDoc
