# API Type Definitions Guidelines

## Overview

API response types should be defined in the shared domain library, not in individual page domain libraries. This ensures consistency and reusability across the application.

## GET API Endpoint → Type Location

| Endpoint Pattern            | Type Location                                          | Example                               |
| --------------------------- | ------------------------------------------------------ | ------------------------------------- |
| `/status/xxx`               | `libs/mxsecurity/shared/domain/src/lib/models/api/status/` | `/status/gnssStatus`                  |
| `/setting/data/xxx/SRV_XXX` | `libs/mxsecurity/shared/domain/src/lib/models/api/srv/`    | `/setting/data/gnss/SRV_GNSS_GENERAL` |
| `/auth/xxx`                 | `libs/mxsecurity/shared/domain/src/lib/models/api/auth/`   | `/auth/login`                         |
| `/data/xxx`                 | `libs/mxsecurity/shared/domain/src/lib/models/api/data/`   | `/data/menuTree`                      |

## Directory Structure

```text
libs/mxsecurity/shared/domain/src/lib/models/api/
├── auth/          # /auth/* endpoints
│   ├── auth-login.def.ts
│   └── index.ts
├── data/          # /data/* endpoints
│   ├── menu-tree.def.ts
│   └── index.ts
├── srv/           # /setting/data/xxx/SRV_* endpoints
│   ├── srv-user-account.def.ts
│   ├── srv-pw-policy.def.ts
│   ├── srv-gnss-general.def.ts
│   └── index.ts
├── status/        # /status/* endpoints
│   ├── gnss-status.def.ts
│   └── index.ts
└── index.ts       # Re-exports all
```

## Rules

### 1. API Response Types → Shared Domain

API response types (types returned from REST calls) should be defined in:

```text
libs/mxsecurity/shared/domain/src/lib/models/api/
```

Example:

```typescript
// ✅ Correct: Use shared API types
import { SRV_USER_ACCOUNT } from '@one-ui/mxsecurity/shared/domain';

return this.#rest.get<SRV_USER_ACCOUNT>(this.#ENDPOINTS.USER_ACCOUNT);
```

```typescript
// ❌ Incorrect: Defining API types in page domain
// libs/mxsecurity/account-page/domain/src/lib/account-page.model.ts
export interface SrvUserAccount {
  SRV_USER_ACCOUNT_Table: SrvUserAccountEntry[];
}
```

### 2. Page-Specific Models → Page Domain

Page-specific models (view models, form models, table data models) should be defined in the page's domain library:

```text
libs/mxsecurity/{page-name}/domain/src/lib/{page-name}.model.ts
```

These include:

- Table data items (transformed for UI display)
- Form models
- Dialog data interfaces
- Component-specific computed models

Example:

```typescript
// libs/mxsecurity/account-page/domain/src/lib/account-page.model.ts

// ✅ Correct: Page-specific view model
export interface AccountTableDataItem {
  key: number;
  username: string;
  authority: string; // Translated display value
  authorityRaw: AuthorityType; // Original API value
  enable: string; // Translated display value
  enableRaw: number; // Original API value
  passwordExpire: string;
  loginOn: boolean;
  enableClass?: string;
}

// ✅ Correct: Dialog-specific data interface
export interface AccountSettingDialogData {
  row?: AccountTableDataItem;
  accountData?: AccountTableDataItem[];
  passwordPolicy: PasswordPolicy;
  adminNumber: number;
}
```

### 3. Missing API Types → Create in Shared Domain

If the API type doesn't exist in the shared domain, create it:

```bash
# Create new API type file
touch libs/mxsecurity/shared/domain/src/lib/models/api/srv/srv-new-endpoint.def.ts
```

Then export it from the shared domain index:

```typescript
// libs/mxsecurity/shared/domain/src/index.ts
export * from './lib/models/api/srv/srv-new-endpoint.def';
```

### 4. Interface Naming Convention

Interface names should reflect their **specific usage context**, not be generic placeholders.

```typescript
// ❌ Incorrect: Generic name used for specific operation
deleteAccount$(userName: string): Observable<AccountPageApiResponse> {
  const payload: AccountSetPayload = { ... };  // Generic name
  return this.#rest.post(...);
}

// ✅ Correct: Name reflects the specific operation
deleteAccount$(userName: string): Observable<AccountPageApiResponse> {
  const payload: DeleteAccountPayload = { ... };  // Specific name
  return this.#rest.post(...);
}
```

Each API method should have a corresponding interface:

| API Method        | Interface Name         |
| ----------------- | ---------------------- |
| `createAccount$`  | `CreateAccountInput`   |
| `editAccount$`    | `EditAccountInput`     |
| `changePassword$` | `ChangePasswordInput`  |
| `deleteAccount$`  | `DeleteAccountPayload` |

### 5. API Endpoints - Inline Strings, No Constants

**DO NOT** define endpoint constants. Inline the endpoint strings directly in each method.

```typescript
// ❌ Incorrect: Defining endpoint constants
@Injectable()
export class MyPageApiService {
  readonly #ENDPOINTS = {
    STATUS_CSR: '/status/csr',
    AUTH_CSR_GEN: '/auth/csrGen'
  } as const;

  getCsrList$(): Observable<CsrApiEntry[]> {
    return this.#restService.get<CsrApiEntry[]>(this.#ENDPOINTS.STATUS_CSR);
  }

  createCsr$(payload: CreateCsrPayload): Observable<void> {
    return this.#restService.post<void>(this.#ENDPOINTS.AUTH_CSR_GEN, payload);
  }
}
```

```typescript
// ✅ Correct: Inline endpoint strings directly
@Injectable()
export class MyPageApiService {
  readonly #restService = inject(RestService);

  getCsrList$(): Observable<CsrApiEntry[]> {
    return this.#restService.get<CsrApiEntry[]>('/status/csr');
  }

  createCsr$(payload: CreateCsrPayload): Observable<void> {
    return this.#restService.post<void>('/auth/csrGen', payload);
  }
}
```

**Why inline?**

- Endpoints are only used once per method
- No benefit from abstraction
- Easier to read and understand
- Less code to maintain

### 6. Update Response Types - Use SettingDataResponse

The legacy system often used `void` for POST/update responses. **The new system requires proper typing.**

Use `SettingDataResponse<K, T>` for all update/POST operations:

```typescript
// libs/mxsecurity/shared/domain/src/lib/models/global/api.model.ts
export type SettingDataResponse<K extends string, T> = {
  [P in K]: T;
} & {
  success: string;
};
```

**API Service - Define Response Types:**

```typescript
// ❌ Incorrect: Using void (legacy pattern)
updateDot1xCfg$(cfg: Dot1xCfg): Observable<void> {
  return this.#rest.post<void>('/setting/data/?SRV=SRV_DOT1X_CFG', cfg);
}

// ✅ Correct: Use SettingDataResponse with proper types
updateDot1xCfg$(cfg: Dot1xCfg) {
  return this.#rest.post<UpdateDot1xCfgResponse>('/setting/data/?SRV=SRV_DOT1X_CFG', cfg);
}
```

**Model File - Define Response Type Aliases:**

```typescript
// libs/mxsecurity/{page}/domain/src/lib/{page}.model.ts

import type {
  SettingDataResponse,
  SRV_DOT1X_CFG,
  SRV_DOT1X_PORT,
  SRV_DOT1X_USER_DB
} from '@one-ui/mxsecurity/shared/domain';

// Define response type aliases for each update operation
export type UpdateDot1xCfgResponse = SettingDataResponse<'SRV_DOT1X_CFG', SRV_DOT1X_CFG>;
export type UpdateDot1xPortResponse = SettingDataResponse<'SRV_DOT1X_PORT', SRV_DOT1X_PORT>;
export type UpdateDot1xUserDbResponse = SettingDataResponse<'SRV_DOT1X_USER_DB', SRV_DOT1X_USER_DB>;
export type ReauthPortResponse = SettingDataResponse<'result', string>;
```

**Store - Use Response Types in mutationMethod:**

```typescript
// ❌ Incorrect: Using void or unknown
updateGeneralSettings: mutationMethod<GeneralFormValue, void>({ ... })
updateGeneralSettings: mutationMethod<GeneralFormValue, unknown>({ ... })

// ✅ Correct: Use the proper response type
updateGeneralSettings: mutationMethod<GeneralFormValue, UpdateDot1xCfgResponse>({
  store,
  observe: (formValue) => {
    const cfg = store.dot1xCfg();
    if (!cfg) throw new Error('Config not loaded');
    const updatedCfg = buildGeneralCfgUpdate(cfg, formValue);
    return api.updateDot1xCfg$(updatedCfg);
  }
})
```

**Using Response in Component (with skipSnackbar):**

When you need to show a custom message from the API response:

```typescript
// Use skipSnackbar: true and handle the response manually
this.#store.reauthPort(() => ({
  input: this.dialogData.row.portIndex,
  skipSnackbar: true,
  next: (response: ReauthPortResponse) => {
    this.#snackBar.open(response.result); // Show API result message
    this.#store.loadPageData();
    this.#dialogRef.close({ success: true });
  }
}));
```

**Response Type Pattern Summary:**

| API Response Key      | Response Type                             |
| --------------------- | ----------------------------------------- |
| Returns `SRV_*` data  | `SettingDataResponse<'SRV_XXX', SRV_XXX>` |
| Returns result string | `SettingDataResponse<'result', string>`   |

## Summary

| Type Category      | Location                                        | Example                             |
| ------------------ | ----------------------------------------------- | ----------------------------------- |
| API Response Types | `libs/mxsecurity/shared/domain/src/lib/models/api/` | `SRV_USER_ACCOUNT`, `SRV_PW_POLICY` |
| Page View Models   | `libs/mxsecurity/{page}/domain/src/lib/*.model.ts`  | `AccountTableDataItem`              |
| Page Form Models   | `libs/mxsecurity/{page}/domain/src/lib/*.model.ts`  | `AccountSettingDialogData`          |
| Page Constants     | `libs/mxsecurity/{page}/domain/src/lib/*.def.ts`    | `AuthorityType`, `AccountMode`      |

---

## Quick Reference

### Type Location Decision Tree

```
Is it a GET response type?
├── Yes → Define in shared domain (libs/mxsecurity/shared/domain/src/lib/models/api/)
│         ├── /status/* → api/status/
│         ├── /setting/data/*/SRV_* → api/srv/
│         ├── /auth/* → api/auth/
│         └── /data/* → api/data/
│
└── No (POST response) → Does it return SRV data?
    ├── Yes → Use SettingDataResponse in feature model.ts
    │         export type XxxResponse = SettingDataResponse<'SRV_XXX', SRV_XXX>;
    │
    └── No → Define custom response in feature model.ts
              export interface CustomActionResponse { result: string; }
```

### Naming Conventions

| Type            | Naming Pattern                     | Example                 |
| --------------- | ---------------------------------- | ----------------------- |
| SRV GET type    | `SRV_XXX_YYY` (uppercase)          | `SRV_GNSS_GENERAL`      |
| Status GET type | `XxxStatusResponse`                | `GnssStatusResponse`    |
| POST response   | `XxxResponse`                      | `GnssGeneralResponse`   |
| View model      | `XxxTableDataItem`, `XxxFormValue` | `GnssTableDataItem`     |
| Dialog data     | `XxxDialogData`                    | `GnssSettingDialogData` |
| Composite type  | `XxxPageData`                      | `GnssPageData`          |

### Import Paths

```typescript
// GET response types - from shared domain
import type { SRV_GNSS_GENERAL, GnssStatusResponse } from '@one-ui/mxsecurity/shared/domain';

// SettingDataResponse helper - from shared domain
import type { SettingDataResponse } from '@one-ui/mxsecurity/shared/domain';

// Feature-specific types - from feature domain
import type { GnssGeneralResponse, GnssTableDataItem } from './gnss-page.model';
```

### Feature model.ts Template

```typescript
// libs/mxsecurity/{page}/domain/src/lib/{page}.model.ts

import type { SettingDataResponse, SRV_XXX } from '@one-ui/mxsecurity/shared/domain';

// ========== POST Response Types (using SettingDataResponse) ==========
export type XxxResponse = SettingDataResponse<'SRV_XXX', SRV_XXX>;

// ========== View Models (for UI components) ==========
export interface XxxTableDataItem {
  index: number;
  name: string;
  status: string;
  statusRaw: number; // Original API value
}

// ========== Form Models ==========
export interface XxxFormValue {
  enabled: boolean;
  name: string;
}

// ========== Dialog Data ==========
export interface XxxDialogData {
  mode: 'create' | 'edit';
  initialData?: XxxTableDataItem;
}

// ========== Composite Types (for forkJoin) ==========
export interface XxxPageData {
  config: SRV_XXX;
  status: XxxStatusResponse;
}
```
