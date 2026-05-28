# Coding Style Rules

Code organization and style conventions for consistency.

## Always Do

- **Use descriptive names** - Variables, functions, files should be self-documenting
- **Keep functions focused** - Single responsibility, one level of abstraction
- **Group related code** - Organize imports, keep related functions together
- **Use consistent formatting** - Let the formatter handle it (Biome/Prettier)
- **Add types** - TypeScript types for all function parameters and returns
- **Handle errors** - Every async operation needs error handling
- **Use early returns** - Reduce nesting with guard clauses
- **Prefer const** - Use const by default, let only when reassignment needed
- **Use async/await** - Prefer over .then() chains
- **Keep files small** - Under 300 lines, split if larger

## Never Do

- ❌ **Use magic numbers** - Define constants with meaningful names
- ❌ **Leave commented code** - Delete it, git has history
- ❌ **Use any** - Type properly or use unknown with type guards
- ❌ **Nest deeply** - Max 3 levels of nesting
- ❌ **Mix styles** - Pick one pattern and stick with it
- ❌ **Use abbreviations** - `getUserById` not `getUsrById`
- ❌ **Ignore errors** - No empty catch blocks
- ❌ **Use var** - Always const or let
- ❌ **Create god files** - No 1000+ line files

## Naming Conventions

### Variables and Functions
```typescript
// camelCase for variables and functions
const userName = 'alice';
function getUserById(id: string) { ... }

// SCREAMING_SNAKE_CASE for constants
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = '/api/v1';
```

### Types and Interfaces
```typescript
// PascalCase for types
interface UserProfile { ... }
type ApiResponse<T> = { ... }

// Prefix interfaces with 'I' only if needed for clarity
interface IUserRepository { ... } // Optional convention
```

### Files and Directories
```typescript
// kebab-case for files
user-service.ts
api-client.ts

// PascalCase for React components
UserProfile.tsx
ApiStatus.tsx

// index.ts for barrel exports
components/index.ts
```

## File Organization

### Import Order
```typescript
// 1. External packages
import { useState } from 'react';
import { z } from 'zod';

// 2. Internal modules (absolute imports)
import { api } from '@/lib/api';
import { Button } from '@/components/ui';

// 3. Relative imports
import { helper } from './utils';
import type { Props } from './types';
```

### File Structure
```typescript
// 1. Imports
import { ... } from '...';

// 2. Types
interface Props { ... }

// 3. Constants
const DEFAULT_VALUE = 10;

// 4. Helper functions (if small and file-specific)
function formatDate(date: Date) { ... }

// 5. Main export
export function Component(props: Props) { ... }

// 6. Sub-components (if needed)
function SubComponent() { ... }
```

## Examples

### Early Returns

**Good**:
```typescript
function processUser(user: User | null) {
  if (!user) return null;
  if (!user.isActive) return null;
  if (!user.hasPermission) return null;

  return doProcessing(user);
}
```

**Bad**:
```typescript
function processUser(user: User | null) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission) {
        return doProcessing(user);
      }
    }
  }
  return null;
}
```

### Error Handling

**Good**:
```typescript
async function fetchUser(id: string) {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    if (error instanceof NotFoundError) {
      return null;
    }
    throw new UserFetchError('Failed to fetch user', { cause: error });
  }
}
```

**Bad**:
```typescript
async function fetchUser(id: string) {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    // Silent failure - bad!
  }
}
```

### Constants vs Magic Numbers

**Good**:
```typescript
const MAX_FILE_SIZE_MB = 10;
const RETRY_DELAY_MS = 1000;
const MAX_RETRIES = 3;

if (file.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
  throw new Error(`File exceeds ${MAX_FILE_SIZE_MB}MB limit`);
}
```

**Bad**:
```typescript
if (file.size > 10485760) { // What is this number?
  throw new Error('File too large');
}
```

## Exceptions

1. **Performance-critical code** - May use abbreviations or unusual patterns if documented
2. **External API requirements** - Match external naming if integration requires it
3. **Legacy code** - Follow existing patterns when modifying legacy code
4. **Generated code** - Auto-generated code may not follow conventions
