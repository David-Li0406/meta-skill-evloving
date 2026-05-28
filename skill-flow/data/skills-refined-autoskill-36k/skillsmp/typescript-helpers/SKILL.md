---
name: typescript-helpers
description: TypeScript patterns for types, interfaces, and type guards in viya-app. Use when defining types, working with generated API types, or creating type-safe utilities.
license: MIT
metadata:
  author: shipitsmarter
  version: "1.1"
---

# TypeScript Helpers Skill

Guidelines for TypeScript types, interfaces, and patterns in this project.

> **Detailed patterns**: See [reference/utility-types.md](reference/utility-types.md) for utility types, type guards, and common patterns.

---

## Core Principles

- **Strict typing required** - avoid `any`, prefer `unknown` with type guards
- **Use generated types** - import from `@/generated/*` for API responses
- **Type everything** - props, emits, functions, refs, and API responses

---

## Type vs Interface

### Use `interface` for:
- Object shapes that may be extended
- Props and emits definitions
- API response types (though prefer generated types)

```typescript
interface Props {
  title: string;
  items: Item[];
  readonly?: boolean;
}

interface Emits {
  (e: 'update', value: string): void;
  (e: 'close'): void;
}
```

### Use `type` for:
- Unions and intersections
- Mapped types
- Utility types
- Simple aliases

```typescript
type Status = 'pending' | 'active' | 'completed';
type ShipmentWithMeta = Shipment & { metadata: Record<string, unknown> };
type Nullable<T> = T | null;
```

---

## Generated API Types

API types are auto-generated from OpenAPI specs. **Always use these instead of defining your own:**

```typescript
// Import from generated modules
import type { 
  Shipment, 
  ShipmentStatus,
  CreateShipmentRequest 
} from '@/generated/shipping';

import type { Rate, RateRequest } from '@/generated/rates';
import type { Address, AddressType } from '@/generated/address';
```

### Regenerating types

```bash
npm run generate-api
```

This pulls the latest OpenAPI specs and regenerates all types in `src/generated/`.

---

## Component Typing

### Props

```typescript
interface Props {
  shipmentId: string;           // Required prop
  readonly?: boolean;            // Optional prop
  status?: 'pending' | 'active'; // Union type
  items: ShipmentItem[];         // Array type
}

const props = withDefaults(defineProps<Props>(), {
  readonly: false,
  status: 'pending',
});
```

### Emits

```typescript
interface Emits {
  (e: 'update:modelValue', value: string): void;
  (e: 'submit', data: FormData): void;
  (e: 'close'): void;
}

const emit = defineEmits<Emits>();
```

### Refs

```typescript
const loading = ref<boolean>(false);
const shipment = ref<Shipment | null>(null);
const items = ref<ShipmentItem[]>([]);
const formState = reactive<FormState>({ name: '', email: '' });
```

### Computed

```typescript
const filteredItems = computed<ShipmentItem[]>(() => {
  return items.value.filter(item => item.active);
});
```

---

## Function Typing

```typescript
// Arrow function with typed parameters and return
const formatPrice = (value: number): string => {
  return `$${value.toFixed(2)}`;
};

// Async function
const fetchShipment = async (id: string): Promise<Shipment> => {
  const response = await shipmentService.get(id);
  return response.data;
};

// Function with optional parameters
const greet = (name: string, greeting?: string): string => {
  return `${greeting ?? 'Hello'}, ${name}!`;
};
```

---

## What to Avoid

### Never use `any`

```typescript
// Bad
const processData = (data: any) => { ... };

// Good - use unknown with type guard
const processData = (data: unknown) => {
  if (isShipment(data)) {
    // Now TypeScript knows the type
  }
};
```

### Don't ignore TypeScript errors

```typescript
// Bad
// @ts-ignore
const value = obj.property;

// Good - fix the actual type issue
const value = (obj as ExpectedType).property;
// or use type guard
if ('property' in obj) {
  const value = obj.property;
}
```

### Don't use non-null assertion carelessly

```typescript
// Bad - can cause runtime errors
const name = user!.name;

// Good - handle null case
const name = user?.name ?? 'Unknown';
```

---

## Type Checklist

Before submitting:
- [ ] No `any` types - use `unknown` with type guards
- [ ] Using generated types from `@/generated/`
- [ ] Props and emits are fully typed
- [ ] Refs have explicit type annotations
- [ ] Functions have typed parameters and return types
- [ ] Type guards used for runtime type checking

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **api-integration** | Working with API services and types |
| **vue-component** | Using types in Vue components |
| **unit-testing** | Typing test mocks and fixtures |
