# TypeScript Utility Types Reference

Detailed type patterns and examples. For core principles and guidelines, see the main SKILL.md.

---

## Built-in Utility Types

```typescript
// Make all properties optional
type PartialShipment = Partial<Shipment>;

// Make all properties required
type RequiredShipment = Required<Shipment>;

// Pick specific properties
type ShipmentSummary = Pick<Shipment, 'id' | 'status' | 'carrier'>;

// Omit specific properties
type ShipmentWithoutId = Omit<Shipment, 'id'>;

// Make all properties readonly
type ReadonlyShipment = Readonly<Shipment>;

// Record type for dictionaries
type ShipmentMap = Record<string, Shipment>;

// Extract return type of a function
type ServiceReturn = ReturnType<typeof shipmentService.getShipment>;

// Extract parameter types
type ServiceParams = Parameters<typeof shipmentService.getShipment>;
```

---

## Custom Utility Types

```typescript
// Nullable type
type Nullable<T> = T | null;

// Optional type (null or undefined)
type Optional<T> = T | null | undefined;

// Deep partial (all nested properties optional)
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Make specific keys required
type RequireKeys<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Example: Shipment with required id and carrier
type ShipmentWithRequiredFields = RequireKeys<Partial<Shipment>, 'id' | 'carrier'>;
```

---

## Type Guards

### Basic type guards

```typescript
const isString = (value: unknown): value is string => {
  return typeof value === 'string';
};

const isNumber = (value: unknown): value is number => {
  return typeof value === 'number' && !isNaN(value);
};

const isArray = <T>(value: unknown): value is T[] => {
  return Array.isArray(value);
};
```

### Object type guards

```typescript
interface Shipment {
  id: string;
  status: string;
  carrier: string;
}

const isShipment = (value: unknown): value is Shipment => {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'status' in value &&
    'carrier' in value
  );
};

// Usage
const processData = (data: unknown) => {
  if (isShipment(data)) {
    // TypeScript knows data is Shipment here
    console.log(data.carrier);
  }
};
```

### Discriminated unions

```typescript
interface SuccessResponse {
  type: 'success';
  data: Shipment;
}

interface ErrorResponse {
  type: 'error';
  message: string;
}

type ApiResponse = SuccessResponse | ErrorResponse;

const handleResponse = (response: ApiResponse) => {
  if (response.type === 'success') {
    // TypeScript knows response.data exists
    return response.data;
  } else {
    // TypeScript knows response.message exists
    throw new Error(response.message);
  }
};
```

---

## Generic Functions

```typescript
// Generic identity
const identity = <T>(value: T): T => value;

// Generic with constraint
const getProperty = <T, K extends keyof T>(obj: T, key: K): T[K] => {
  return obj[key];
};

// Generic array filter
const filterByStatus = <T extends { status: string }>(
  items: T[],
  status: string
): T[] => {
  return items.filter(item => item.status === status);
};
```

---

## Callback Types

```typescript
// Define callback type
type OnSelectCallback = (item: ShipmentItem) => void;
type OnChangeCallback<T> = (value: T, oldValue: T) => void;

// Use in props
interface Props {
  onSelect?: OnSelectCallback;
  onChange?: OnChangeCallback<string>;
}
```

---

## Const Assertions

Use `as const` for literal types and readonly arrays:

```typescript
// Status literals
const STATUSES = ['pending', 'active', 'completed'] as const;
type Status = typeof STATUSES[number]; // 'pending' | 'active' | 'completed'

// Configuration object
const CONFIG = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
  retries: 3,
} as const;

// Column definitions
const COLUMNS = [
  { key: 'name', label: 'Name', sortable: true },
  { key: 'status', label: 'Status', sortable: false },
] as const;
```

---

## Service Typing Pattern

### Service class

```typescript
import type { Shipment, CreateShipmentRequest } from '@/generated/shipping';
import { ApiResponse } from '@/services/types';

class ShipmentService {
  async get(id: string): Promise<ApiResponse<Shipment>> {
    // Implementation
  }

  async create(data: CreateShipmentRequest): Promise<ApiResponse<Shipment>> {
    // Implementation
  }

  async list(params?: ListParams): Promise<ApiResponse<Shipment[]>> {
    // Implementation
  }
}
```

### API response handling

```typescript
import type { CoreProblemDetails } from '@/services/clients';

interface ApiResponse<T> {
  isSuccess: () => boolean;
  data?: T;
  problem?: CoreProblemDetails;
}

// Usage
const result = await shipmentService.get(id);
if (result.isSuccess() && result.data) {
  shipment.value = result.data;
} else {
  error.value = result.problem?.detail ?? 'Unknown error';
}
```

---

## Common Patterns

### Nullable state

```typescript
// Loading state with nullable data
const shipment = ref<Shipment | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

const loadShipment = async (id: string) => {
  loading.value = true;
  error.value = null;
  
  try {
    const result = await shipmentService.get(id);
    if (result.isSuccess()) {
      shipment.value = result.data ?? null;
    } else {
      error.value = result.problem?.detail ?? 'Failed to load';
    }
  } finally {
    loading.value = false;
  }
};
```

### Form state

```typescript
interface FormState {
  name: string;
  email: string;
  address?: Address;
}

const formState = reactive<FormState>({
  name: '',
  email: '',
});

const isValid = computed(() => {
  return formState.name.length > 0 && formState.email.includes('@');
});
```

### Event handlers

```typescript
// Type event handlers explicitly
const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  formState.name = target.value;
};

const handleSubmit = (event: SubmitEvent) => {
  event.preventDefault();
  // Submit logic
};
```
