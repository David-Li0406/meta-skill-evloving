# DDD Architecture

## Layer Decision Flow

```
QUESTION: Does component have HTTP calls or business logic?
  YES → domain/
  NO  ↓

QUESTION: Does component inject Store or manage dialogs?
  YES → features/
  NO  ↓

QUESTION: Does component ONLY have input()/output()?
  YES → ui/
  NO  ↓

QUESTION: Does component define routes/guards/resolvers?
  YES → shell/
```

## Layer Constraints

| Layer | CAN Inject | CANNOT |
|-------|------------|--------|
| **domain/** | HttpClient, MxRestService, other services | Import from features or ui |
| **features/** | Store, MatDialog, ViewContainerRef | Make HTTP calls directly |
| **ui/** | FormBuilder, TranslocoService | Store, HttpClient, MatDialog |
| **shell/** | Store (in resolvers only) | Business logic |

---

## 5-File Pattern (Domain Layer)

```
libs/{scope}/{feature}/domain/src/lib/
├── {feature}.api-model.ts  # Backend API types (OpenAPI schema)
├── {feature}.model.ts      # Frontend UI view models, constants
├── {feature}.api.ts        # HTTP calls (MxRestService)
├── {feature}.store.ts      # SignalStore
├── {feature}.helper.ts     # Pure utility functions (optional)
└── index.ts                # Public exports
```

| File | Contains | When to Modify |
|------|----------|----------------|
| `*.api-model.ts` | Types from backend API (OpenAPI) | When backend API changes |
| `*.model.ts` | UI view models, constants, type unions, enums | When UI requirements change |
| `*.api.ts` | HTTP calls using MxRestService | When endpoints change |
| `*.store.ts` | SignalStore with queryMethod/mutationMethod | When state logic changes |
| `*.helper.ts` | Pure functions for data transformation, serialization | When transformation logic needed |

> **Note**: Constants and enums can go in `*.model.ts` (no need for separate `*.def.ts`)

---

## api-model.ts (Backend Types)

Types that match the backend API response structure:

```typescript
/**
 * {Feature} API Models
 * Source: OpenAPI schema / Backend API
 */

// Entity types from backend
export interface User {
  userId?: string;
  username?: string;
  role?: { id: number; name: string };
}

// Request types
export interface UserCreate {
  username: string;
  password: string;
}

// Response wrappers
export interface UserResponse { data: User; }
export interface UsersResponse { data: User[]; }
```

---

## model.ts (Frontend Types)

UI view models, constants, type unions, and translation key mappings:

```typescript
/**
 * {Feature} UI Models
 * Frontend-defined types for UI layer
 */

// Constants - feature-specific defaults
export const FEATURE_DEFAULTS = {
  TABLE_MAX_SIZE: 10,
  PASSWORD_MIN_LENGTH: 4,
  PASSWORD_MAX_LENGTH: 64
} as const;

// Type union (preferred over enum)
export type UserRole = 'admin' | 'user' | 'supervisor';

// Type union with const object for runtime values
export const USER_STATUS = {
  Active: 'active',
  Inactive: 'inactive'
} as const;
export type UserStatus = typeof USER_STATUS[keyof typeof USER_STATUS];

// Translation key mappings for feature-specific values
export const ROLE_TRANSLATION_KEYS: Record<UserRole, string> = {
  admin: 'features.user_management.role.admin',
  user: 'features.user_management.role.user',
  supervisor: 'features.user_management.role.supervisor'
};

// View model for table display (flattened from API type)
export interface UserTableItem {
  key: number;
  username: string;
  roleName: string;      // Flattened: user.role.name
  roleRaw: UserRole;     // For filtering/sorting
}

// Dialog data
export interface UserDialogData {
  mode: 'create' | 'edit';
  item?: UserTableItem;
}
```

> **Important**: Put feature-specific constants, enums, and translation mappings in `*.model.ts`. Only use shared domain patterns for validators (e.g., `VAILD_REGEX_NOT_SPACE` from `@one-ui/shared/domain`).

---

## helper.ts (Pure Functions)

**Purpose**: Extract pure functions for data transformations and serialization to keep store files focused on state management.

**When to use `*.helper.ts`**:
- Transform API responses to table/UI data models
- Serialize form data to API payloads
- Complex data parsing or formatting
- Any pure function with no side effects

**Example - Data Transformation**:

```typescript
// user-management.helper.ts
import type { User } from './user-management.api-model';
import type { UserTableItem, ROLE_TRANSLATION_KEYS } from './user-management.model';

/**
 * Transform API user to table display item
 */
export function toTableItem(apiUser: User, index: number): UserTableItem {
  return {
    key: index,
    username: apiUser.username ?? '',
    roleName: getRoleTranslationKey(apiUser.role),
    roleRaw: apiUser.role ?? 'user'
  };
}

/**
 * Get translation key for role
 */
function getRoleTranslationKey(role: string): string {
  return ROLE_TRANSLATION_KEYS[role as UserRole] ?? ROLE_TRANSLATION_KEYS.user;
}

/**
 * Transform multiple users to table data
 */
export function transformToTableData(users: User[]): UserTableItem[] {
  return users.map((user, index) => toTableItem(user, index));
}
```

**Example - Serialization**:

```typescript
// config.helper.ts
import type { ConfigFormValue, ConfigPayload } from './config.model';

/**
 * Serialize form value to API payload format
 */
export function serializeConfigPayload(formValue: ConfigFormValue): ConfigPayload {
  return {
    entries: formValue.entries.map(entry => ({
      id: entry.id,
      name: entry.name.trim(),
      enabled: entry.enabled ? 1 : 0,  // Boolean to number
      raw: `${entry.interface}+${entry.port}+${entry.protocol}+`
    }))
  };
}
```

**Usage in Store**:

```typescript
// user-management.store.ts
import { transformToTableData } from './user-management.helper';

export const UserManagementStore = signalStore(
  withState({ users: [], tableData: [] }),
  withComputed((store) => ({
    // Use helper to transform data
    tableData: computed(() => transformToTableData(store.users()))
  })),
  withMethods((store, api = inject(UserManagementApiService)) => ({
    loadUsers: queryMethod<void, User[]>({
      store,
      observe: () => api.getUsers(),
      next: (users) => patchState(store, { users })
    })
  }))
);
```

**Benefits**:
- Keeps store files focused on state management only
- Makes pure functions testable in isolation
- Improves code reusability across components
- Clear separation between state logic and data transformation

---

## Import Pattern

⚠️ **No Re-export**: Import types directly from source. Do NOT re-export `api-model` types in `model.ts`.

```typescript
// In api.ts - import from api-model
import type { User, UserCreate, UserResponse } from './{feature}.api-model';

// In store.ts - import from both
import type { User, UserCreate } from './{feature}.api-model';
import type { UserTableItem } from './{feature}.model';

// In helper.ts - transform API to UI
import type { User } from './{feature}.api-model';
import type { UserTableItem, ROLE_TRANSLATION_KEYS } from './{feature}.model';

export function toTableItem(apiUser: User, index: number): UserTableItem {
  return {
    key: index,
    username: apiUser.username ?? '',
    roleName: ROLE_TRANSLATION_KEYS[apiUser.role] ?? '',
    roleRaw: apiUser.role
  };
}
```

---

## api.ts (HTTP Calls)

```typescript
import type { User, UserCreate, UsersResponse } from './{feature}.api-model';

@Injectable({ providedIn: 'root' })
export class FeatureApiService {
  readonly #api = inject(MxRestService);
  readonly #ENDPOINTS = {
    USERS: '/api/users'
  } as const;

  getUsers$(): Observable<User[]> {
    return this.#api.get$<UsersResponse>(this.#ENDPOINTS.USERS)
      .pipe(map(res => res.data));
  }

  createUser$(data: UserCreate): Observable<User> {
    return this.#api.post$<User>(this.#ENDPOINTS.USERS, data);
  }
}
```

---

## Shared API Types (Centralized)

For API types used across multiple features:

```
libs/{scope}/shared/domain/src/lib/api/
├── user.api-model.ts
├── config.api-model.ts
├── device.api-model.ts
└── index.ts
```

```typescript
// Import shared API types
import type { User } from '@one-ui/{scope}/shared/domain';
```

---

## Full Directory Structure

```
libs/{scope}/{feature}/
├── domain/
│   ├── {feature}.api-model.ts  # Backend types
│   ├── {feature}.model.ts      # UI types
│   ├── {feature}.api.ts        # HTTP calls
│   ├── {feature}.store.ts      # SignalStore
│   ├── {feature}.helper.ts     # Pure functions
│   └── index.ts
├── features/
│   ├── {feature}-page.component.ts
│   └── {feature}-dialog/
│       ├── {feature}-dialog.component.ts
│       └── {feature}-dialog.component.html
├── ui/
│   ├── {feature}-table/
│   │   ├── {feature}-table.component.ts
│   │   └── {feature}-table.component.html
│   └── {feature}-form/
└── shell/
    └── {feature}.routes.ts
```

---

## Type vs Enum

Prefer TypeScript `type` union over `enum`:

```typescript
// ❌ Avoid enum (generates extra JavaScript)
enum Status {
  Active = 'active',
  Inactive = 'inactive'
}

// ✅ Prefer type union (better tree-shaking)
type Status = 'active' | 'inactive';

// ✅ With const object for runtime values
const STATUS = {
  Active: 'active',
  Inactive: 'inactive'
} as const;
type Status = typeof STATUS[keyof typeof STATUS];
```

---

## Layer Violations

### ❌ UI injects Store

```typescript
// UI component - WRONG
@Component({ selector: 'one-ui-user-table' })
export class UserTableComponent {
  readonly #store = inject(UserStore);  // ❌ NOT allowed in UI
}
```

### ✅ UI uses input/output

```typescript
// UI component - CORRECT
@Component({ selector: 'one-ui-user-table' })
export class UserTableComponent {
  users = input.required<User[]>();
  deleteUser = output<string>();
}
```

### ❌ Dialog in UI layer

```
❌ libs/{scope}/{feature}/ui/{feature}-dialog/
✅ libs/{scope}/{feature}/features/{feature}-dialog/
```

### ❌ Features makes HTTP calls

```typescript
// Features component - WRONG
export class FeaturePageComponent {
  readonly #http = inject(HttpClient);  // ❌ NOT allowed

  loadData() {
    this.#http.get('/api/users');  // ❌ HTTP in features
  }
}
```

### ✅ Features uses Store

```typescript
// Features component - CORRECT
export class FeaturePageComponent {
  readonly #store = inject(FeatureStore);

  constructor() {
    this.#store.loadUsers();  // ✅ Delegate to store
  }
}
```

---

## Legacy Path Mapping

```
LEGACY (f2e-networking)              → NEW (one-ui)
src/app/pages/{Page}/                → libs/{scope}/{feature}/features/
src/app/components/                  → libs/{scope}/{feature}/ui/
src/app/services/{name}.service.ts   → libs/{scope}/{feature}/domain/
src/app/models/{name}.model.ts       → libs/{scope}/{feature}/domain/{feature}.api-model.ts
                                       libs/{scope}/{feature}/domain/{feature}.model.ts
```

---

## Related References

- [checklist.md](./checklist.md) - DDD Architecture checklist
- [signal-store.md](../tools/signal-store.md) - Store pattern in domain
- [create-page.md](../guides/create-page.md) - Full page creation guide
