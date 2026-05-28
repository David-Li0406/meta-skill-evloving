# Rule Catalog — Code Quality

A framework-agnostic frontend code quality guideline for consistent, maintainable, and scalable codebases.

---

## Naming Conventions

### PascalCase (大驼峰)

IsUrgent: True
Category: Naming Convention

#### Description

Use **PascalCase** for the following:

- Component names
- Enum names
- Type / Interface names

#### Examples

```ts
// ✅ Good
interface UserProfile {}
type ApiResponse<T> = {}
enum AuthRole {}

// ❌ Bad
interface userProfile {}
type apiResponse<T> = {}
```

---

### camelCase (小驼峰)

IsUrgent: True
Category: Naming Convention

#### Description

Use **camelCase** for the following:

- Variables
- Function names (except components)
- Method names
- Object properties
- Function parameters

#### Examples

```ts
// ✅ Good
const userName = 'John'
function fetchUserData() {}
const config = { maxRetries: 3 }

// ❌ Bad
const UserName = 'John'
const user_name = 'John'
function FetchUserData() {}
```

---

### SCREAMING_SNAKE_CASE (全大写下划线)

IsUrgent: True
Category: Naming Convention

#### Description

Use **SCREAMING_SNAKE_CASE** for the following:

- Global constants
- Environment variables
- Static readonly values

#### Examples

```ts
// ✅ Good
const MAX_RETRY_COUNT = 3
const API_BASE_URL = 'https://api.example.com'
const DEFAULT_TIMEOUT_MS = 5000

// ❌ Bad
const maxRetryCount = 3  // Should be SCREAMING_SNAKE_CASE for global constants
```

---

### File naming conventions

IsUrgent: True
Category: Naming Convention

#### Description

| File Type | Convention | Example |
|-----------|------------|---------|
| Component | `kebab-case` or `PascalCase` (project-specific) | `user-card.tsx` / `UserCard.tsx` |
| Utility / Helper | `kebab-case` | `date-utils.ts` |
| Hook / Composable | `camelCase` with prefix | `useAuth.ts` / `useUserData.ts` |
| Constant | `kebab-case` | `route-paths.ts` |
| Type / Interface | `kebab-case` | `user-types.ts` |
| Test file | Match source + `.test` / `.spec` | `user-service.test.ts` |

---

### Boolean naming

Category: Naming Convention

#### Description

Boolean variables and functions should use clear prefixes indicating their boolean nature.

| Prefix | Usage | Example |
|--------|-------|---------|
| `is` | State check | `isLoading`, `isVisible`, `isAuthenticated` |
| `has` | Possession check | `hasPermission`, `hasError`, `hasChildren` |
| `can` | Ability check | `canEdit`, `canDelete`, `canSubmit` |
| `should` | Recommendation | `shouldRefresh`, `shouldValidate` |

#### Examples

```ts
// ✅ Good
const isLoading = true
const hasPermission = checkPermission(user)
function canEditPost(user: User, post: Post): boolean {}

// ❌ Bad
const loading = true      // Unclear if boolean
const permission = true   // Ambiguous
function editPost() {}    // Doesn't indicate return type
```

---

### Method / Function naming

Category: Naming Convention

#### Description

Function names should follow **Subject → Verb** pattern (not `handleXxx` or `onXxx` unless it's an event handler).

| Pattern | Usage | Example |
|---------|-------|---------|
| `verb + Noun` | General actions | `fetchUser()`, `validateForm()` |
| `subject + Verb` | Object-oriented style | `userCreate()`, `passwordChange()` |
| `get + Noun` | Synchronous getters | `getUserName()`, `getConfig()` |
| `fetch/load + Noun` | Async data fetching | `fetchUserList()`, `loadArticles()` |

#### Examples

```ts
// ✅ Good
function fetchUserProfile() {}
function validateEmail(email: string) {}
function passwordReset() {}

// ❌ Bad (avoid generic handle prefix)
function handleClick() {}     // Use specific: submitForm(), toggleMenu()
function handleData() {}      // Use specific: processData(), transformData()
```

---

## Type Safety

### Prohibit `any` type

IsUrgent: True
Category: Type Safety

#### Description

Never use `any` type. Always define proper `interface` or `type` based on actual data structure.

#### Examples

```ts
// ❌ Bad
function processData(data: any) {}
const response: any = await fetch(url)

// ✅ Good
interface UserData {
  id: number
  name: string
  email: string
}
function processData(data: UserData) {}
const response: ApiResponse<UserData> = await fetch(url)
```

---

### Use `unknown` over `any` when type is uncertain

Category: Type Safety

#### Description

When the type is genuinely unknown at compile time, use `unknown` instead of `any`. This forces explicit type checking before usage.

#### Examples

```ts
// ✅ Good
function parseJson(json: string): unknown {
  return JSON.parse(json)
}

const data = parseJson(input)
if (isUserData(data)) {
  // Now TypeScript knows data is UserData
  console.log(data.name)
}

// ❌ Bad
function parseJson(json: string): any {
  return JSON.parse(json)
}
```

---

### Use enum for related constants

IsUrgent: True
Category: Type Safety

#### Description

Use `enum` or `const object` for related constant values. Avoid hardcoding magic strings/numbers.

#### Examples

```ts
// ✅ Good - Enum
enum AuthRole {
  Admin = 'admin',
  Editor = 'editor',
  Viewer = 'viewer',
}
const role = AuthRole.Admin

// ✅ Good - Const object (when you need the values)
const HTTP_STATUS = {
  OK: 200,
  NOT_FOUND: 404,
  SERVER_ERROR: 500,
} as const

// ❌ Bad
const role = 'admin'
if (status === 404) {}
```

---

## Import & Export

### Import path conventions

IsUrgent: True
Category: Code Organization

#### Description

- Use **absolute paths** (`@/xxx`) for cross-module imports
- Use **relative paths** (`./`) only for same-directory imports
- Never use `../` for parent directory traversal

#### Examples

```ts
// ✅ Good
import { UserService } from '@/services/user-service'
import { formatDate } from '@/utils/date-utils'
import { helper } from './helper'

// ❌ Bad
import { UserService } from '../../services/user-service'
import { formatDate } from '../../../utils/date-utils'
```

---

### Import ordering

Category: Code Organization

#### Description

Organize imports in the following order, with blank lines between groups:

1. **External libraries** (node_modules)
2. **Internal absolute imports** (`@/...`)
3. **Relative imports** (`./...`)
4. **Type imports** (if separated)

#### Examples

```ts
// 1. External
import { useState, useEffect } from 'react'
import axios from 'axios'

// 2. Internal absolute
import { UserService } from '@/services/user-service'
import { API_BASE_URL } from '@/constants/config'

// 3. Relative
import { helper } from './helper'
import { LocalComponent } from './local-component'

// 4. Types (optional separate group)
import type { User } from '@/types/user'
```

---

## Code Organization

### Single responsibility

Category: Code Quality

#### Description

Each file, function, and class should have a single, well-defined responsibility.

- **Files**: One component/service/utility per file
- **Functions**: Do one thing and do it well
- **Max function length**: ~50 lines (consider splitting if longer)

---

### Dead code cleanup

Category: Code Quality

#### Description

Remove all dead code before committing. Check for:

- `console.log()` statements (use proper logging utilities instead)
- Commented-out code blocks
- Unused variables, functions, or imports
- Unreachable code after `return`, `throw`, or `break`
- Deprecated code that is no longer called

#### Examples

```ts
// ❌ Bad - Dead code
console.log('debugging...')           // Remove before commit
// const oldLogic = calculateOld()    // Commented-out code
import { unusedUtil } from '@/utils'  // Unused import
const unusedVar = 'test'              // Unused variable

function example() {
  return result
  doSomething()  // Unreachable code
}

// ✅ Good - Clean code
import { usedUtil } from '@/utils'

function example() {
  return result
}
```

> **Tip**: Use ESLint rules like `no-console`, `no-unused-vars`, and `no-unreachable` to automatically detect dead code.

---

### Avoid magic numbers/strings

IsUrgent: True
Category: Code Quality

#### Description

Extract magic values into named constants with meaningful names.

#### Examples

```ts
// ❌ Bad
if (retryCount > 3) {}
setTimeout(callback, 5000)
if (status === 'pending') {}

// ✅ Good
const MAX_RETRY_COUNT = 3
const DEBOUNCE_DELAY_MS = 5000
const OrderStatus = { PENDING: 'pending' } as const

if (retryCount > MAX_RETRY_COUNT) {}
setTimeout(callback, DEBOUNCE_DELAY_MS)
if (status === OrderStatus.PENDING) {}
```

---

### Comments policy

Category: Code Quality

#### Description

- Code should be self-documenting; avoid unnecessary comments
- Only add comments for complex logic, business rules, or non-obvious algorithms
- Use JSDoc for public APIs and exported functions
- Comments must be in **English** or **Japanese** (no Chinese comments)

#### Examples

```ts
// ❌ Bad - Obvious comment
// Loop through users
for (const user of users) {}

// ✅ Good - Explains WHY, not WHAT
// Retry with exponential backoff to handle rate limiting
for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
  await delay(Math.pow(2, attempt) * 1000)
}

// ✅ Good - JSDoc for public API
/**
 * Calculates the discount based on user tier and cart value.
 * @param tier - User membership tier
 * @param cartValue - Total cart value in cents
 * @returns Discount percentage (0-100)
 */
export function calculateDiscount(tier: UserTier, cartValue: number): number {}
```
