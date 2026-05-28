---
name: unit-testing
description: Writing unit tests with vitest and vue-test-utils following project patterns. Use when creating tests for components, composables, utilities, or stores.
license: MIT
metadata:
  author: shipitsmarter
  version: "1.0"
---

# Unit Testing Skill

Guidelines for writing unit tests in this project using vitest and vue-test-utils.

---

## Test file structure

Tests go in `__tests__/` directories alongside the code they test:

```
src/
├── components/
│   └── feature-name/
│       ├── FeatureComponent.vue
│       └── __tests__/
│           └── FeatureComponent.spec.ts
├── utils/
│   ├── datetime.ts
│   └── __tests__/
│       └── datetime.spec.ts
├── store/
│   ├── my-store.ts
│   └── __tests__/
│       └── my-store.spec.ts
```

**Naming:** `*.spec.ts` (not `.test.ts`)

---

## Running tests

```bash
# Run all tests
npm test

# Single run (no watch)
npx vitest --run

# Run specific file
npx vitest src/path/to/file.spec.ts

# Run by pattern
npx vitest -t "test name pattern"

# Update snapshots
npm run test:update
```

---

## Test structure

```typescript
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

describe('FeatureName', () => {
  // Setup and teardown
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  // Group related tests
  describe('methodName', () => {
    it('should handle happy path', () => {
      // Arrange
      const input = 'test';
      
      // Act
      const result = methodName(input);
      
      // Assert
      expect(result).toBe('expected');
    });

    it('should handle edge case', () => {
      // ...
    });
  });
});
```

---

## Component testing

### Using the factory helper

The project provides a `factory` helper for mounting components:

```typescript
import { VueWrapper } from '@vue/test-utils';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import MyComponent from '@/components/feature/MyComponent.vue';
import { factory, resetWrapper } from '@/test-utils';

describe('MyComponent', () => {
  let wrapper: VueWrapper;

  beforeEach(() => {
    wrapper = factory(MyComponent, {
      props: {
        title: 'Test Title',
        items: [],
      },
      global: {
        stubs: {
          ChildComponent: true, // Stub child components
        },
      },
    });
  });

  afterEach(() => {
    resetWrapper(wrapper);
  });

  it('renders the component', () => {
    expect(wrapper.exists()).toBe(true);
  });

  it('displays the title', () => {
    expect(wrapper.text()).toContain('Test Title');
  });
});
```

### Testing with data-testid

Use `data-testid` attributes for reliable element selection:

```typescript
import { fromWrapper } from '@/test-utils';

it('triggers action on button click', async () => {
  const { findByTestId } = fromWrapper(wrapper);
  
  const button = findByTestId('submit-button');
  await button.trigger('click');
  
  expect(wrapper.emitted('submit')).toBeTruthy();
});
```

### Testing elements in document body (portals/teleports)

For components that render to `document.body` (dialogs, popovers):

```typescript
import { fromBody } from '@/test-utils';

it('opens dialog when triggered', async () => {
  await wrapper.get('[data-testid="open-dialog"]').trigger('click');
  
  const { findByTestId } = fromBody();
  const dialog = findByTestId('dialog-content');
  
  expect(dialog).toBeTruthy();
});
```

### Accessing component internals

Type the exposed properties for TypeScript support:

```typescript
interface ComponentExposed {
  isOpen: boolean;
  searchQuery: string;
  handleSelect: (option: Option) => void;
}

it('updates internal state', async () => {
  (wrapper.vm as unknown as ComponentExposed).searchQuery = 'test';
  await wrapper.vm.$nextTick();
  
  expect((wrapper.vm as unknown as ComponentExposed).isOpen).toBe(true);
});
```

---

## Mocking

### Mocking modules

```typescript
vi.mock('@/composables/useAccess', () => ({
  useAccess: vi.fn(() => ({
    can: vi.fn(() => true),
    canAll: vi.fn(() => true),
    canAny: vi.fn(() => true),
  })),
}));

vi.mock('@/utils/logger'); // Auto-mock all exports
```

### Mocking services

```typescript
vi.mock('@/services/shipment-service', () => ({
  ShipmentService: vi.fn().mockImplementation(() => ({
    getShipment: vi.fn().mockResolvedValue({ data: mockShipment }),
    updateShipment: vi.fn().mockResolvedValue({ isSuccess: () => true }),
  })),
}));
```

### Mocking timers

```typescript
beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date('2025-01-15T12:00:00Z'));
});

afterEach(() => {
  vi.useRealTimers();
});

it('handles time-based logic', () => {
  const result = formatRelativeTime(futureDate);
  expect(result).toBe('in 5 hours');
});
```

### Spying on functions

```typescript
it('calls handler when clicked', async () => {
  const handler = vi.fn();
  const wrapper = factory(MyComponent, {
    props: { onClick: handler },
  });

  await wrapper.get('button').trigger('click');
  
  expect(handler).toHaveBeenCalledOnce();
  expect(handler).toHaveBeenCalledWith(expect.any(Object));
});
```

---

## Mock data organization

**Static mock data must be in separate `.mock.ts` files:**

```
src/views/feature/__tests__/
├── FeatureComponent.spec.ts
└── __mocks__/
    └── feature-data-mock.ts
```

### Creating mock files

```typescript
// feature-data-mock.ts
import type { Shipment } from '@/generated/shipping';

export const mockShipment: Shipment = {
  id: 'ship-123',
  status: 'pending',
  carrier: 'DHL',
  // ... complete object matching generated type
};

export const mockShipmentList: Shipment[] = [
  mockShipment,
  { ...mockShipment, id: 'ship-456', status: 'delivered' },
];
```

### Using mocks in tests

```typescript
import { mockShipment, mockShipmentList } from './__mocks__/feature-data-mock';

describe('ShipmentList', () => {
  it('renders shipments', () => {
    const wrapper = factory(ShipmentList, {
      props: { shipments: mockShipmentList },
    });
    
    expect(wrapper.findAll('[data-testid="shipment-row"]')).toHaveLength(2);
  });
});
```

---

## Testing utilities

### Pure function tests

```typescript
import { formatPrice, calculateTotal } from '@/utils/pricing';

describe('pricing utilities', () => {
  describe('formatPrice', () => {
    it('formats positive numbers', () => {
      expect(formatPrice(1234.56)).toBe('$1,234.56');
    });

    it('handles zero', () => {
      expect(formatPrice(0)).toBe('$0.00');
    });

    it('handles negative numbers', () => {
      expect(formatPrice(-100)).toBe('-$100.00');
    });

    it('handles null/undefined', () => {
      expect(formatPrice(null)).toBe('');
      expect(formatPrice(undefined)).toBe('');
    });
  });
});
```

---

## Testing stores (Pinia)

```typescript
import { createPinia, Pinia } from 'pinia';
import { beforeEach, describe, expect, it } from 'vitest';

import { useMyStore } from '@/store/my-store';

describe('useMyStore', () => {
  let pinia: Pinia;

  beforeEach(() => {
    pinia = createPinia();
  });

  it('initializes with default state', () => {
    const store = useMyStore(pinia);
    expect(store.items).toEqual([]);
    expect(store.loading).toBe(false);
  });

  it('adds items correctly', () => {
    const store = useMyStore(pinia);
    store.addItem({ id: '1', name: 'Test' });
    
    expect(store.items).toHaveLength(1);
    expect(store.items[0].name).toBe('Test');
  });

  it('computes derived state', () => {
    const store = useMyStore(pinia);
    store.items = [{ id: '1', active: true }, { id: '2', active: false }];
    
    expect(store.activeItems).toHaveLength(1);
  });
});
```

---

## Testing composables

```typescript
import { ref } from 'vue';
import { describe, expect, it } from 'vitest';

import { useDebounce } from '@/composables/useDebounce';

describe('useDebounce', () => {
  it('returns debounced value after delay', async () => {
    vi.useFakeTimers();
    
    const source = ref('initial');
    const debounced = useDebounce(source, 300);
    
    expect(debounced.value).toBe('initial');
    
    source.value = 'updated';
    expect(debounced.value).toBe('initial'); // Still old value
    
    vi.advanceTimersByTime(300);
    expect(debounced.value).toBe('updated'); // Now updated
    
    vi.useRealTimers();
  });
});
```

---

## Common patterns

### Testing async operations

```typescript
it('loads data on mount', async () => {
  const wrapper = factory(DataComponent);
  
  // Wait for async operations
  await wrapper.vm.$nextTick();
  await vi.waitFor(() => {
    expect(wrapper.find('[data-testid="data-loaded"]').exists()).toBe(true);
  });
});
```

### Testing emitted events

```typescript
it('emits update event with new value', async () => {
  const wrapper = factory(InputComponent, {
    props: { modelValue: '' },
  });

  await wrapper.find('input').setValue('new value');
  
  expect(wrapper.emitted('update:modelValue')).toBeTruthy();
  expect(wrapper.emitted('update:modelValue')![0]).toEqual(['new value']);
});
```

### Testing v-model

```typescript
it('supports v-model', async () => {
  const wrapper = factory(ToggleComponent, {
    props: {
      'modelValue': false,
      'onUpdate:modelValue': (e: boolean) => wrapper.setProps({ modelValue: e }),
    },
  });

  await wrapper.find('button').trigger('click');
  
  expect(wrapper.props('modelValue')).toBe(true);
});
```

---

## Browser API mocks

### ResizeObserver

```typescript
global.ResizeObserver = class {
  observe() {}
  unobserve() {}
  disconnect() {}
};
```

### getBoundingClientRect

```typescript
HTMLElement.prototype.getBoundingClientRect = () => ({
  width: 100,
  height: 40,
  top: 0,
  left: 0,
  bottom: 40,
  right: 100,
  x: 0,
  y: 0,
  toJSON: () => {},
});
```

### scrollIntoView

```typescript
window.HTMLElement.prototype.scrollIntoView = vi.fn();
```

---

## Test checklist

Before submitting:
- [ ] Tests are in `__tests__/` directory with `.spec.ts` extension
- [ ] Mock data is in separate `*-mock.ts` files
- [ ] Using `factory` helper for component mounting
- [ ] Cleanup in `afterEach` (resetWrapper, vi.useRealTimers)
- [ ] Testing both happy paths and edge cases
- [ ] No `any` types - use proper typing or `unknown`
- [ ] Mocks use generated types from `@/generated/`

---

## Related skills

| Skill | When to Use |
|-------|-------------|
| **vue-component** | Understanding component patterns to test |
| **playwright-test** | E2E tests instead of unit tests |
| **api-integration** | Testing service integration |
