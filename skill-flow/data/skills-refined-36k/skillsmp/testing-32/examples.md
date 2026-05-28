# Testing Examples

## Component Test Template (Jest + Options API)

When generating tests for components using **Options API** with **Jest**:

```typescript
import { shallowMount } from '@vue/test-utils';
import { createStore } from 'vuex';
import ComponentName from './ComponentName.vue';

describe('ComponentName.vue', () => {
  // Mock store modules if component uses Vuex
  const mockStoreModule = {
    getters: {
      getSomeData: jest.fn().mockImplementation(() => 'mock data'),
    },
    actions: {
      fetchData: jest.fn(),
    },
    namespaced: true,
  };

  const createWrapper = (customOptions = {}) => {
    const store = createStore({
      modules: {
        moduleName: mockStoreModule,
      },
    });

    return shallowMount(ComponentName, {
      global: {
        plugins: [store],
      },
      ...customOptions,
    });
  };

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('component exists', () => {
    const wrapper = createWrapper();
    expect(wrapper.exists()).toBe(true);
  });

  describe('mounted lifecycle', () => {
    it('fetches data on mount', () => {
      createWrapper();
      expect(mockStoreModule.actions.fetchData).toHaveBeenCalled();
    });
  });

  describe('computed properties', () => {
    it('returns correct computed value', () => {
      const wrapper = createWrapper();
      expect(wrapper.vm.computedProperty).toBe('expected value');
    });
  });

  describe('methods', () => {
    it('handles button click correctly', async () => {
      const wrapper = createWrapper();
      await wrapper.find('button').trigger('click');
      expect(mockStoreModule.actions.fetchData).toHaveBeenCalled();
    });
  });
});
```

## Component Test Template (Jest + Composition API)

When generating tests for components using **Composition API** with **Jest**:

```typescript
import { shallowMount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import ComponentName from './ComponentName.vue';
import { useEntityStore } from '@/stores/entityStore';

describe('ComponentName.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  const createWrapper = (props = {}) => {
    return shallowMount(ComponentName, {
      global: {
        plugins: [createPinia()],
      },
      props,
    });
  };

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('component exists', () => {
    const wrapper = createWrapper();
    expect(wrapper.exists()).toBe(true);
  });

  describe('props', () => {
    it('receives and displays prop correctly', () => {
      const wrapper = createWrapper({ title: 'Test Title' });
      expect(wrapper.text()).toContain('Test Title');
    });
  });

  describe('emits', () => {
    it('emits event on button click', async () => {
      const wrapper = createWrapper();
      await wrapper.find('button').trigger('click');
      expect(wrapper.emitted('update')).toBeTruthy();
    });
  });

  describe('composables/stores', () => {
    it('calls store action', async () => {
      const wrapper = createWrapper();
      const store = useEntityStore();
      const fetchSpy = jest.spyOn(store, 'fetchItems');
      
      await wrapper.vm.loadData();
      expect(fetchSpy).toHaveBeenCalled();
    });
  });
});
```

## View Test Template

Views typically test:
- Lifecycle hooks (mounted, beforeUnmount)
- Navigation and routing
- Store interactions
- Event handlers
- Conditional rendering

```typescript
import { shallowMount } from '@vue/test-utils';
import { createStore } from 'vuex';
import ViewName from './ViewName.vue';

describe('ViewName.vue', () => {
  const createWrapper = () => {
    const store = createStore({
      modules: {
        // mock store modules
      },
    });

    return shallowMount(ViewName, {
      global: {
        plugins: [store],
        stubs: ['router-link'],
      },
    });
  };

  it('view exists', () => {
    const wrapper = createWrapper();
    expect(wrapper.exists()).toBe(true);
  });

  describe('mounted lifecycle', () => {
    it('sets up event listeners on mount', () => {
      const addEventListenerSpy = jest.spyOn(document, 'addEventListener');
      const wrapper = createWrapper();
      expect(addEventListenerSpy).toHaveBeenCalledWith(
        'click',
        expect.any(Function),
        true
      );
      wrapper.unmount();
    });
  });

  describe('navigation', () => {
    it('navigates to correct route on action', async () => {
      const wrapper = createWrapper();
      const pushMock = jest.fn();
      Object.defineProperty(wrapper.vm, '$router', {
        value: { push: pushMock },
      });
      
      await wrapper.vm.navigateToDetails('123');
      expect(pushMock).toHaveBeenCalledWith({
        name: 'Details',
        params: { id: '123' },
      });
    });
  });
});
```

## Store Test Template (Vuex)

```typescript
import store from '@/store';
import entityModule from './entityModule';

describe('entity store module', () => {
  beforeEach(() => {
    // Reset module state before each test
  });

  describe('mutations', () => {
    it('sets items correctly', () => {
      const state = { items: [] };
      const items = [{ id: 1, name: 'Item 1' }];
      entityModule.mutations.setItems(state, items);
      expect(state.items).toEqual(items);
    });
  });

  describe('actions', () => {
    it('fetches items and commits mutation', async () => {
      const commit = jest.fn();
      const mockItems = [{ id: 1, name: 'Item 1' }];
      
      // Mock API call
      jest.spyOn(entityService, 'getAll').mockResolvedValue(mockItems);
      
      await entityModule.actions.fetchItems({ commit });
      expect(commit).toHaveBeenCalledWith('setItems', mockItems);
    });
  });

  describe('getters', () => {
    it('returns filtered items', () => {
      const state = { items: [{ id: 1, active: true }, { id: 2, active: false }] };
      const result = entityModule.getters.activeItems(state);
      expect(result).toHaveLength(1);
    });
  });
});
```

## Store Test Template (Pinia)

```typescript
import { setActivePinia, createPinia } from 'pinia';
import { useEntityStore } from './entityStore';

describe('entity store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('initializes with default state', () => {
    const store = useEntityStore();
    expect(store.items).toEqual([]);
    expect(store.loading).toBe(false);
  });

  describe('actions', () => {
    it('fetches items successfully', async () => {
      const store = useEntityStore();
      const mockItems = [{ id: 1, name: 'Item 1' }];
      
      jest.spyOn(entityService, 'getAll').mockResolvedValue(mockItems);
      
      await store.fetchItems();
      expect(store.items).toEqual(mockItems);
      expect(store.loading).toBe(false);
    });
  });

  describe('getters', () => {
    it('returns correct item count', () => {
      const store = useEntityStore();
      store.items = [{ id: 1 }, { id: 2 }];
      expect(store.itemCount).toBe(2);
    });
  });
});
```

## Component Test Template (Vitest + Composition API)

When using **Vitest** instead of Jest, the syntax is very similar:

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { shallowMount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import ComponentName from './ComponentName.vue';
import { useEntityStore } from '@/stores/entityStore';

describe('ComponentName.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  const createWrapper = (props = {}) => {
    return shallowMount(ComponentName, {
      global: {
        plugins: [createPinia()],
      },
      props,
    });
  };

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('component exists', () => {
    const wrapper = createWrapper();
    expect(wrapper.exists()).toBe(true);
  });

  describe('props', () => {
    it('receives and displays prop correctly', () => {
      const wrapper = createWrapper({ title: 'Test Title' });
      expect(wrapper.text()).toContain('Test Title');
    });
  });

  describe('emits', () => {
    it('emits event on button click', async () => {
      const wrapper = createWrapper();
      await wrapper.find('button').trigger('click');
      expect(wrapper.emitted('update')).toBeTruthy();
    });
  });

  describe('composables/stores', () => {
    it('calls store action', async () => {
      const wrapper = createWrapper();
      const store = useEntityStore();
      const fetchSpy = vi.spyOn(store, 'fetchItems');
      
      await wrapper.vm.loadData();
      expect(fetchSpy).toHaveBeenCalled();
    });
  });
});
```

## Utility Test Template

```typescript
import { describe, it, expect } from 'vitest';
import { formatDate, validateEmail, debounce } from './utils';

describe('formatDate', () => {
  it('formats date correctly', () => {
    const date = new Date('2024-01-15');
    expect(formatDate(date)).toBe('01/15/2024');
  });

  it('handles invalid dates', () => {
    expect(formatDate(null)).toBe('');
  });
});

describe('validateEmail', () => {
  it('validates correct email format', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });

  it('rejects invalid email format', () => {
    expect(validateEmail('invalid-email')).toBe(false);
  });
});

describe('debounce', () => {
  it('debounces function calls', async () => {
    vi.useFakeTimers();
    const mockFn = vi.fn();
    const debouncedFn = debounce(mockFn, 300);
    
    debouncedFn();
    debouncedFn();
    debouncedFn();
    
    expect(mockFn).not.toHaveBeenCalled();
    
    vi.advanceTimersByTime(300);
    expect(mockFn).toHaveBeenCalledTimes(1);
    
    vi.useRealTimers();
  });
});
```

## Directive Test Template

```typescript
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import vClickOutside from './clickOutside';

describe('v-click-outside directive', () => {
  it('calls handler when clicking outside element', async () => {
    const handler = vi.fn();
    const wrapper = mount({
      template: '<div v-click-outside="handler"><button>Inside</button></div>',
      directives: { clickOutside: vClickOutside },
      setup() {
        return { handler };
      },
    });

    document.body.click();
    await wrapper.vm.$nextTick();

    expect(handler).toHaveBeenCalled();
  });

  it('does not call handler when clicking inside element', async () => {
    const handler = vi.fn();
    const wrapper = mount({
      template: '<div v-click-outside="handler"><button>Inside</button></div>',
      directives: { clickOutside: vClickOutside },
      setup() {
        return { handler };
      },
    });

    wrapper.find('button').trigger('click');
    await wrapper.vm.$nextTick();

    expect(handler).not.toHaveBeenCalled();
  });
});
```

*** Important Notes ***
- The above examples show the desired test structure and patterns
- When generating tests, adapt patterns to match the specific component/module being tested
- Use `jest.fn()` for Jest, `vi.fn()` for Vitest
- Use `jest.spyOn()` for Jest, `vi.spyOn()` for Vitest
- Always follow AAA pattern: Arrange, Act, Assert
- Group related tests using describe blocks
- Mock external dependencies (axios, router, store)
- Test user interactions, not implementation details
