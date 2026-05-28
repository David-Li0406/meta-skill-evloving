---
name: api-integration
description: Integrating with generated API types and services in viya-app. Use when working with API endpoints, creating services, or handling API responses with proper typing.
license: MIT
metadata:
  author: shipitsmarter
  version: "1.0"
---

# API Integration Skill

Guidelines for integrating with APIs using generated TypeScript types.

---

## Overview

This project uses OpenAPI-generated TypeScript types for type-safe API calls:

1. **Generated types** in `src/generated/*.ts` - Auto-generated from OpenAPI specs
2. **Service layer** in `src/services/` - Wraps API calls with error handling
3. **Clients** in `src/services/clients.ts` - Configured API clients

---

## Generating API types

```bash
npm run generate-api
```

This regenerates types from the backend OpenAPI specs into `src/generated/`:
- `shipping.ts` - Shipment API
- `rates.ts` - Rates API
- `ftp.ts` - FTP integration API
- `hooks.ts` - Webhooks API
- `authorizing.ts` - Authorization API
- `auditor.ts` - Audit log API
- `printing.ts` - Printing API

**Always regenerate after backend API changes.**

---

## Using generated types

### Import types

```typescript
import type {
  ShipmentResponse,
  CreateShipmentRequest,
  AddressResponse,
} from '@/generated/shipping';
```

### Type API responses

```typescript
const shipment = ref<ShipmentResponse>();
const addresses = ref<AddressResponse[]>([]);
```

### Type function parameters

```typescript
const createShipment = async (request: CreateShipmentRequest): Promise<ShipmentResponse> => {
  const result = await shippingService.create(request);
  if (result.isSuccess()) {
    return result.data;
  }
  throw new Error(result.problem?.detail);
};
```

---

## Service layer pattern

### BaseService

All services extend `BaseService` which provides:
- Automatic loading state management
- Error handling with `CoreProblemDetails`
- Response wrapping with `DataOrProblem<T>`

```typescript
import { BaseService, DataOrProblem } from '@/services/base-service';

export class ShipmentService extends BaseService {
  async getById(id: string, ...args: Options<ShipmentResponse>): Promise<DataOrProblem<ShipmentResponse>> {
    return this.executeRequest(
      () => shippingClient.GET('/v4/shipments/{shipmentId}', {
        params: { path: { shipmentId: id } },
      }),
      ...args
    );
  }
}
```

### Using services in components

```typescript
// Service instance (in Constants section)
const shipmentService = new ShipmentService();

// Refs for state management
const loading = ref(false);
const problem = ref<CoreProblemDetails>();
const shipment = ref<ShipmentResponse>();

// Fetch with automatic state updates
const fetchShipment = async (id: string) => {
  await shipmentService.getById(id, loading, problem, shipment);
};

// Or handle manually
const fetchShipmentManual = async (id: string) => {
  const result = await shipmentService.getById(id);
  if (result.isSuccess()) {
    shipment.value = result.data;
  } else {
    toast.error(result.problem?.detail ?? 'Failed to load shipment');
  }
};
```

---

## DataOrProblem pattern

API responses are wrapped in `DataOrProblem<T>`:

```typescript
interface DataOrProblem<T> {
  data: T;
  problem: CoreProblemDetails | undefined;
  isSuccess(): boolean;
}
```

### Checking results

```typescript
const result = await service.getSomething();

if (result.isSuccess()) {
  // result.data is available and typed
  console.log(result.data);
} else {
  // result.problem contains error details
  console.error(result.problem?.detail);
}
```

### CoreProblemDetails

Error responses follow RFC 7807:

```typescript
interface CoreProblemDetails {
  type: string;
  title: string;
  detail: string;
  status: number;
  errors: Array<{ field: string; message: string }>;
}
```

---

## Common patterns

### Loading and error refs

Pass refs to automatically track loading state and errors:

```typescript
const loading = ref(false);
const problem = ref<CoreProblemDetails>();
const data = ref<MyType>();

// All three refs are updated automatically
await myService.getData(loading, problem, data);

// In template
<LoadingSpinner v-if="loading" />
<ErrorMessage v-else-if="problem" :problem="problem" />
<DataDisplay v-else :data="data" />
```

### Pagination

Many list endpoints return paginated data:

```typescript
import type { PaginatedResponse } from '@/generated/shipping';

const response = ref<PaginatedResponse<ShipmentResponse>>();

// Access pagination info
const totalItems = computed(() => response.value?.total ?? 0);
const items = computed(() => response.value?.items ?? []);
```

### Query parameters

```typescript
await service.getList({
  page: 1,
  pageSize: 50,
  sortBy: 'createdAt',
  sortDirection: 'desc',
  filter: 'status:active',
});
```

---

## Error handling

### In services

```typescript
try {
  const result = await request();
  return this.handledResponse(result);
} catch (error) {
  const problem: CoreProblemDetails = {
    type: 'about:blank',
    title: 'Network error',
    detail: (error as Error).message,
    status: 0,
    errors: [],
  };
  return DataOrProblem.fromProblem(problem, 'unknown');
}
```

### In components

```typescript
const result = await shipmentService.create(request);

if (!result.isSuccess()) {
  if (result.problem?.errors?.length) {
    // Validation errors - show field-level messages
    result.problem.errors.forEach(err => {
      formErrors.value[err.field] = err.message;
    });
  } else {
    // General error - show toast
    toast.error(result.problem?.detail ?? 'Something went wrong');
  }
  return;
}

// Success
toast.success('Shipment created');
router.push({ name: 'shipment-detail', params: { id: result.data.id } });
```

---

## API clients

Configured clients are exported from `src/services/clients.ts`:

```typescript
import { shippingClient, ratesClient, ftpClient } from '@/services/clients';

// Direct client usage (prefer service layer)
const response = await shippingClient.GET('/v4/shipments/{shipmentId}', {
  params: { path: { shipmentId: '123' } },
});
```

---

## Creating a new service

1. Create file: `src/services/my-feature-service.ts`

```typescript
import { BaseService, type Options } from '@/services/base-service';
import { myClient } from '@/services/clients';
import type { MyResponse, MyCreateRequest } from '@/generated/my-api';

export class MyFeatureService extends BaseService {
  async getById(id: string, ...args: Options<MyResponse>) {
    return this.executeRequest(
      () => myClient.GET('/v1/items/{id}', {
        params: { path: { id } },
      }),
      ...args
    );
  }

  async create(request: MyCreateRequest, ...args: Options<MyResponse>) {
    return this.executeRequest(
      () => myClient.POST('/v1/items', {
        body: request,
      }),
      ...args
    );
  }

  async update(id: string, request: MyCreateRequest, ...args: Options<MyResponse>) {
    return this.executeRequest(
      () => myClient.PUT('/v1/items/{id}', {
        params: { path: { id } },
        body: request,
      }),
      ...args
    );
  }

  async delete(id: string, ...args: EmptyResponseOptions) {
    return this.executeRequest(
      () => myClient.DELETE('/v1/items/{id}', {
        params: { path: { id } },
      }),
      ...args
    );
  }
}
```

2. Export from index: `src/services/index.ts`

---

## Checklist

- [ ] Types imported from `@/generated/*`
- [ ] Service extends `BaseService`
- [ ] Uses `executeRequest` for API calls
- [ ] Handles `DataOrProblem` responses correctly
- [ ] Loading and error states managed with refs
- [ ] Toast notifications for user feedback
- [ ] Field-level errors shown for validation failures

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **vue-component** | Component conventions when using services |
| **pr-review** | API pattern verification during code review |
