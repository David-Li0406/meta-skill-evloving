# Types Pattern

## Entity Response Type

```typescript
// types/[entity].d.ts

export interface [Entity]Response {
  id: string;
  // Core fields
  name: string;
  description?: string | null;
  isActive: boolean;
  
  // Timestamps
  createdAt?: string | null;
  updatedAt?: string | null;
  
  // Relations (flattened for display)
  // Example: roles become string arrays
  roles?: Array<{ id: number; enName: string; arName?: string }>;
  enRoles?: string[];
  arRoles?: string[];
  rolesId?: number[];
}
```

## List Response Type

```typescript
export interface [Entity]ListResponse {
  // Data array
  items: [Entity]Response[];
  
  // Pagination
  total: number;
  
  // Stats for status panel
  activeCount: number;
  inactiveCount: number;
  
  // Optional filter options
  filterOptions?: Array<{ id: number; name: string; count: number }>;
}
```

## Actions Context Type

```typescript
export interface [Entity]ActionsContextType {
  onToggleStatus: (id: string, isActive: boolean) => Promise<ActionResult>;
  onUpdate: (id: string, data: UpdatePayload) => Promise<ActionResult>;
  onBulkUpdateStatus: (ids: string[], isActive: boolean) => Promise<ActionResult>;
  onRefresh: () => Promise<ActionResult>;
  updateItems: (items: [Entity]Response[]) => Promise<void>;
}

export interface ActionResult {
  success: boolean;
  message?: string;
  error?: string;
  data?: unknown;
}
```

## Request Types

```typescript
// Create request
export interface [Entity]CreateRequest {
  name: string;
  description?: string;
  isActive?: boolean;
  roleIds?: number[];
}

// Update request
export interface [Entity]UpdateRequest {
  name?: string;
  description?: string;
  roleIds?: number[];
}

// Status update
export interface StatusUpdateRequest {
  entityId: string;
  isActive: boolean;
}

// Bulk status update
export interface BulkStatusUpdateRequest {
  entityIds: string[];
  isActive: boolean;
}

// Bulk status response
export interface BulkStatusUpdateResponse {
  updatedItems: [Entity]Response[];
}
```

## Naming Conventions

| Backend (snake_case) | Frontend (camelCase) |
|---------------------|---------------------|
| `is_active` | `isActive` |
| `created_at` | `createdAt` |
| `role_ids` | `roleIds` |
| `en_name` | `enName` |
| `ar_name` | `arName` |

The API response transformation happens in the API route or fetch layer.
