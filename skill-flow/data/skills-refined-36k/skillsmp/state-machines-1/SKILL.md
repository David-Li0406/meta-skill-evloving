---
name: state-machines
description: "WHAT: Type-safe state machines with discriminated unions and status property. WHEN: async operations, multi-step forms, authentication flows, loading/error states. KEYWORDS: state machine, discriminated union, status, idle, loading, success, error, Zustand, never, AsyncState."
---

# State Machines

## Core Principles

**Always use discriminated unions with a 'status' property.** State machines must be type-safe discriminated unions where each state has a unique 'status' value ('idle', 'loading', 'success', 'error'). The 'status' property enables TypeScript to narrow types and prevents accessing properties that don't exist in the current state.

**Always use helper functions for safe property extraction.** Never access state properties directly without checking 'status' first. Create helper functions (getIsLoading, getError, getLastSavedRecipe) that safely extract properties, returning null or false when the property doesn't exist in the current state.

**Always use plain Zustand stores without middleware.** State machines should be implemented as plain Zustand stores using create() without immer or other middleware. This ensures explicit state transitions and predictable updates. Use set() with function form for state updates.

**Always handle all state transitions explicitly.** State transitions must be explicit and intentional (idle → loading → success/error). Use switch statements with never type for exhaustive checking to ensure all states are handled. Each transition should be a distinct set() call.

**Why**: State machines eliminate impossible states, provide type safety, make state transitions explicit and testable, prevent race conditions, and enable predictable UI behavior through discriminated unions and helper functions.

## When to Use This Skill

Use these patterns when:

- Managing async operations with loading, success, and error states
- Implementing multi-step forms or wizards with explicit steps
- Handling feature flag states (enabled, disabled, loading, error)
- Managing authentication flows (logged out, logging in, logged in, error)
- Building UI that needs to prevent impossible state combinations
- Coordinating multiple async operations with dependencies
- Creating predictable state transitions for testing
- Preventing race conditions in async operations
- Building components with complex loading/error/success states
- Implementing retry logic with explicit state tracking

## Discriminated Unions

### Basic State Machine

Define type-safe state machines with discriminated unions using 'status' property.

```typescript
import { create } from 'zustand';

// State machine using discriminated unions
type SaveRecipeState =
  | { status: 'idle' }
  | { status: 'loading'; pendingSaveUrl: string }
  | { status: 'success'; lastSavedRecipe: ExternalRecipe }
  | { status: 'error'; error: Error };

type RecipeStore = {
  saveState: SaveRecipeState;
  startSave: (url: string) => void;
  completeSave: (recipe: ExternalRecipe) => void;
  failSave: (error: Error) => void;
  resetSave: () => void;
};

export const useRecipeStore = create<RecipeStore>((set) => ({
  saveState: { status: 'idle' },

  startSave: (url: string) =>
    set(() => ({
      saveState: { status: 'loading', pendingSaveUrl: url },
    })),

  completeSave: (recipe: ExternalRecipe) =>
    set(() => ({
      saveState: { status: 'success', lastSavedRecipe: recipe },
    })),

  failSave: (error: Error) =>
    set(() => ({
      saveState: { status: 'error', error },
    })),

  resetSave: () =>
    set(() => ({
      saveState: { status: 'idle' },
    })),
}));
```

**Why**: Discriminated unions make impossible states unrepresentable. TypeScript narrows types when checking 'status', preventing access to properties that don't exist in the current state. Each state can have its own unique properties (pendingSaveUrl only in loading, lastSavedRecipe only in success).

**Production Example**: `modules/social-recipe-bridge/stores/useAddRecipeLinkStore.ts:1`

### Generic AsyncState Pattern

Create reusable async state machine type for common operations.

```typescript
// Generic async operation state machine
type AsyncState<T, E = Error> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: E };

// Usage with specific types
type ProductListingState = AsyncState<Product[], Error>;
type UserProfileState = AsyncState<UserProfile, ApiError>;
type CheckoutState = AsyncState<CheckoutResult, PaymentError>;

// Store with generic async state
type ProductStore = {
  listingState: ProductListingState;
  loadProducts: () => void;
  setProducts: (products: Product[]) => void;
  setError: (error: Error) => void;
};

export const useProductStore = create<ProductStore>((set) => ({
  listingState: { status: 'idle' },

  loadProducts: () =>
    set(() => ({
      listingState: { status: 'loading' },
    })),

  setProducts: (products: Product[]) =>
    set(() => ({
      listingState: { status: 'success', data: products },
    })),

  setError: (error: Error) =>
    set(() => ({
      listingState: { status: 'error', error },
    })),
}));
```

**Why**: Generic AsyncState<T, E> pattern provides reusable type for any async operation. Reduces boilerplate, ensures consistency across stores, and makes async operations predictable. Type parameters enable type safety for different data and error types.

### Multi-Step Form State Machine

Use discriminated unions for multi-step forms with explicit step tracking.

```typescript
type FormStep = 'personal' | 'address' | 'payment' | 'review';

type FormState =
  | { status: 'editing'; currentStep: FormStep; data: Partial<FormData> }
  | { status: 'submitting'; data: FormData }
  | { status: 'success'; submittedData: FormData }
  | { status: 'error'; error: Error; data: FormData };

type FormStore = {
  formState: FormState;
  setStep: (step: FormStep) => void;
  updateData: (data: Partial<FormData>) => void;
  submit: () => void;
  completeSubmission: () => void;
  failSubmission: (error: Error) => void;
};

export const useFormStore = create<FormStore>((set) => ({
  formState: { status: 'editing', currentStep: 'personal', data: {} },

  setStep: (step: FormStep) =>
    set((state) => {
      if (state.formState.status !== 'editing') return state;
      return {
        formState: { ...state.formState, currentStep: step },
      };
    }),

  updateData: (newData: Partial<FormData>) =>
    set((state) => {
      if (state.formState.status !== 'editing') return state;
      return {
        formState: {
          ...state.formState,
          data: { ...state.formState.data, ...newData },
        },
      };
    }),

  submit: () =>
    set((state) => {
      if (state.formState.status !== 'editing') return state;
      return {
        formState: { status: 'submitting', data: state.formState.data as FormData },
      };
    }),

  completeSubmission: () =>
    set((state) => {
      if (state.formState.status !== 'submitting') return state;
      return {
        formState: { status: 'success', submittedData: state.formState.data },
      };
    }),

  failSubmission: (error: Error) =>
    set((state) => {
      if (state.formState.status !== 'submitting') return state;
      return {
        formState: { status: 'error', error, data: state.formState.data },
      };
    }),
}));
```

**Why**: Multi-step form state machine prevents invalid transitions (can't submit while already submitting). Guards (if checks) ensure actions only occur in valid states. Each state has relevant properties (currentStep only in editing, submittedData only in success).

## Helper Functions

### Safe Property Extraction

Create helper functions to safely extract properties from state machines.

```typescript
// State machine
type SaveRecipeState =
  | { status: 'idle' }
  | { status: 'loading'; pendingSaveUrl: string }
  | { status: 'success'; lastSavedRecipe: ExternalRecipe }
  | { status: 'error'; error: Error };

// Helper functions for safe extraction
export const getIsLoading = (saveState: SaveRecipeState): boolean =>
  saveState.status === 'loading';

export const getIsError = (saveState: SaveRecipeState): boolean =>
  saveState.status === 'error';

export const getError = (saveState: SaveRecipeState): Error | null =>
  saveState.status === 'error' ? saveState.error : null;

export const getLastSavedRecipe = (
  saveState: SaveRecipeState
): ExternalRecipe | null =>
  saveState.status === 'success' ? saveState.lastSavedRecipe : null;

export const getPendingSaveUrl = (saveState: SaveRecipeState): string | null =>
  saveState.status === 'loading' ? saveState.pendingSaveUrl : null;

// Usage in components
const MyComponent = () => {
  const { saveState } = useRecipeStore();

  // Safe extraction with helpers
  const isLoading = getIsLoading(saveState);
  const error = getError(saveState);
  const lastSaved = getLastSavedRecipe(saveState);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage error={error} />;
  }

  return <RecipeView recipe={lastSaved} />;
};
```

**Why**: Helper functions provide type-safe property extraction without accessing properties directly. Prevents runtime errors from accessing properties that don't exist in current state. Returns null or default values when property isn't available, making UI logic simpler.

**Production Example**: `modules/social-recipe-bridge/stores/useAddRecipeLinkStore.ts:46`

### Computed State Helpers

Create helpers that compute derived state from state machines.

```typescript
type AsyncState<T, E = Error> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: E };

// Computed state helpers
export const getIsIdle = <T, E>(state: AsyncState<T, E>): boolean =>
  state.status === 'idle';

export const getIsLoading = <T, E>(state: AsyncState<T, E>): boolean =>
  state.status === 'loading';

export const getIsSuccess = <T, E>(state: AsyncState<T, E>): boolean =>
  state.status === 'success';

export const getIsError = <T, E>(state: AsyncState<T, E>): boolean =>
  state.status === 'error';

export const getData = <T, E>(state: AsyncState<T, E>): T | null =>
  state.status === 'success' ? state.data : null;

export const getError = <T, E>(state: AsyncState<T, E>): E | null =>
  state.status === 'error' ? state.error : null;

// Computed flags for UI logic
export const getCanRetry = <T, E>(state: AsyncState<T, E>): boolean =>
  state.status === 'error' || state.status === 'idle';

export const getHasData = <T, E>(state: AsyncState<T, E>): boolean =>
  state.status === 'success';

// Usage
const MyComponent = () => {
  const { asyncState } = useDataStore();

  const canRetry = getCanRetry(asyncState);
  const hasData = getHasData(asyncState);
  const data = getData(asyncState);

  return (
    <View>
      {hasData && <DataView data={data} />}
      {canRetry && <Button onPress={retry}>Retry</Button>}
    </View>
  );
};
```

**Why**: Computed helpers encapsulate business logic (canRetry = error || idle). Generic helpers work with any AsyncState<T, E>. Reduces duplication across components and makes UI logic declarative.

## Zustand Integration

### Plain Store Pattern

Use plain Zustand stores without middleware for state machines.

```typescript
import { create } from 'zustand';

type SaveRecipeState =
  | { status: 'idle' }
  | { status: 'loading'; pendingSaveUrl: string }
  | { status: 'success'; lastSavedRecipe: ExternalRecipe }
  | { status: 'error'; error: Error };

type AddRecipeLinkState = {
  isDrawerVisible: boolean;
  saveState: SaveRecipeState;
  showDrawer: () => void;
  hideDrawer: () => void;
  onSaveRecipeLink: (url: string) => void;
  clearError: () => void;
  resetSaveState: () => void;
};

export const useAddRecipeLinkStore = create<AddRecipeLinkState>((set) => ({
  isDrawerVisible: false,
  saveState: { status: 'idle' },

  showDrawer: () => set(() => ({ isDrawerVisible: true })),
  hideDrawer: () => set(() => ({ isDrawerVisible: false })),

  clearError: () => set(() => ({ saveState: { status: 'idle' } })),

  resetSaveState: () => set(() => ({ saveState: { status: 'idle' } })),

  onSaveRecipeLink: (url: string) => {
    // Set loading state with the pending URL
    set(() => ({
      saveState: { status: 'loading', pendingSaveUrl: url },
      isDrawerVisible: false, // Optimistic UI
    }));
  },
}));
```

**Why**: Plain Zustand stores (no immer, no middleware) make state transitions explicit and predictable. Function form set(() => ({ ... })) ensures fresh state. Each state transition is a distinct set() call, making state changes traceable and testable.

**Production Example**: `modules/social-recipe-bridge/stores/useAddRecipeLinkStore.ts:1`

### Combining with API Mutations

Integrate state machines with TanStack Query or Apollo mutations using callbacks.

```typescript
import { create } from 'zustand';
import { useCreateExternalRecipe } from '@data-access/query/external-recipes';

type SaveRecipeState =
  | { status: 'idle' }
  | { status: 'loading'; pendingSaveUrl: string }
  | { status: 'success'; lastSavedRecipe: ExternalRecipe }
  | { status: 'error'; error: Error };

// Store definition
export const useAddRecipeLinkStore = create<AddRecipeLinkState>((set) => ({
  saveState: { status: 'idle' },
  onSaveRecipeLink: (url: string) => {
    set(() => ({
      saveState: { status: 'loading', pendingSaveUrl: url },
    }));
  },
}));

// Custom hook that combines store with API mutation
export const useAddRecipeLinkWithAPI = ({
  refetch,
}: {
  refetch: () => void;
}) => {
  const store = useAddRecipeLinkStore();
  const createRecipeMutation = useCreateExternalRecipe({
    onSuccess: (data) => {
      refetch();
      // Update store on success
      useAddRecipeLinkStore.setState({
        saveState: { status: 'success', lastSavedRecipe: data },
      });
    },
    onError: (error) => {
      // Update store on error
      useAddRecipeLinkStore.setState({
        saveState: { status: 'error', error: error as Error },
      });
    },
    onMutate: () => {
      // Loading state is already set by onSaveRecipeLink
    },
  });

  const saveRecipeLink = (url: string) => {
    // Update store state for optimistic UI
    store.onSaveRecipeLink(url);

    // Call the API
    const request: CreateExternalRecipeRequest = {
      url,
      title: undefined,
      thumbnail_url: undefined,
    };

    createRecipeMutation.mutate(request);
  };

  return {
    ...store,
    saveRecipeLink,
  };
};
```

**Why**: Custom hook pattern combines Zustand store with TanStack Query/Apollo mutation. onSuccess/onError callbacks update store state based on API response. Loading state set optimistically before API call, success/error states set in callbacks. Separates state management (Zustand) from API logic (TanStack Query).

**Production Example**: `modules/social-recipe-bridge/stores/useAddRecipeLinkStore.ts:64`

### External State Updates

Use setState for external updates to Zustand stores.

```typescript
// Update store from outside React components
const handleExternalEvent = (recipe: ExternalRecipe) => {
  useRecipeStore.setState({
    saveState: { status: 'success', lastSavedRecipe: recipe },
  });
};

// Update store from mutation callbacks
const mutation = useMutation({
  onSuccess: (data) => {
    useRecipeStore.setState({
      saveState: { status: 'success', lastSavedRecipe: data },
    });
  },
  onError: (error) => {
    useRecipeStore.setState({
      saveState: { status: 'error', error: error as Error },
    });
  },
});
```

**Why**: setState allows external updates outside React render cycle. Useful for mutation callbacks, event handlers, and non-React code. Maintains single source of truth in Zustand store.

## Type Narrowing

### Switch Statements with Exhaustive Checking

Use switch statements with never type to ensure all states are handled.

```typescript
type AsyncState<T, E = Error> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: E };

const renderAsyncState = <T, E>(state: AsyncState<T, E>) => {
  switch (state.status) {
    case 'idle':
      return <EmptyState />;
    case 'loading':
      return <LoadingSpinner />;
    case 'success':
      // TypeScript knows state.data exists here
      return <SuccessView data={state.data} />;
    case 'error':
      // TypeScript knows state.error exists here
      return <ErrorMessage error={state.error} />;
    default:
      // Exhaustive check - TypeScript error if new status added
      const _exhaustive: never = state;
      return _exhaustive;
  }
};
```

**Why**: Switch statements with never type provide exhaustive checking. TypeScript error if new status added but not handled. Type narrowing gives access to status-specific properties (data in success, error in error). Default case catches unhandled states at compile time.

### Conditional Type Narrowing

Use if statements for type narrowing in components.

```typescript
const MyComponent = () => {
  const { saveState } = useRecipeStore();

  // Type narrowing with if statements
  if (saveState.status === 'loading') {
    // TypeScript knows pendingSaveUrl exists
    return <LoadingView url={saveState.pendingSaveUrl} />;
  }

  if (saveState.status === 'error') {
    // TypeScript knows error exists
    return <ErrorView error={saveState.error} />;
  }

  if (saveState.status === 'success') {
    // TypeScript knows lastSavedRecipe exists
    return <SuccessView recipe={saveState.lastSavedRecipe} />;
  }

  // Default to idle state
  return <IdleView />;
};
```

**Why**: If statements provide type narrowing for discriminated unions. TypeScript narrows type based on status check, enabling safe property access. Early returns prevent nested conditionals and improve readability.

## Testing State Machines

### Test State Transitions

Test each state transition independently with explicit assertions.

```typescript
import { renderHook, act } from '@testing-library/react-native';
import { useRecipeStore } from './useRecipeStore';

describe('useRecipeStore', () => {
  beforeEach(() => {
    // Reset store before each test
    useRecipeStore.setState({ saveState: { status: 'idle' } });
  });

  it('transitions from idle to loading', () => {
    const { result } = renderHook(() => useRecipeStore());

    expect(result.current.saveState.status).toBe('idle');

    act(() => {
      result.current.startSave('https://example.com/recipe');
    });

    expect(result.current.saveState.status).toBe('loading');
    expect(result.current.saveState).toEqual({
      status: 'loading',
      pendingSaveUrl: 'https://example.com/recipe',
    });
  });

  it('transitions from loading to success', () => {
    const { result } = renderHook(() => useRecipeStore());
    const recipe = { id: '1', title: 'Test Recipe' };

    // Set initial loading state
    act(() => {
      result.current.startSave('https://example.com/recipe');
    });

    expect(result.current.saveState.status).toBe('loading');

    // Transition to success
    act(() => {
      result.current.completeSave(recipe);
    });

    expect(result.current.saveState.status).toBe('success');
    expect(result.current.saveState).toEqual({
      status: 'success',
      lastSavedRecipe: recipe,
    });
  });

  it('transitions from loading to error', () => {
    const { result } = renderHook(() => useRecipeStore());
    const error = new Error('Network error');

    act(() => {
      result.current.startSave('https://example.com/recipe');
    });

    expect(result.current.saveState.status).toBe('loading');

    act(() => {
      result.current.failSave(error);
    });

    expect(result.current.saveState.status).toBe('error');
    expect(result.current.saveState).toEqual({
      status: 'error',
      error,
    });
  });

  it('resets from any state to idle', () => {
    const { result } = renderHook(() => useRecipeStore());

    // Start in success state
    act(() => {
      result.current.completeSave({ id: '1', title: 'Recipe' });
    });

    expect(result.current.saveState.status).toBe('success');

    // Reset to idle
    act(() => {
      result.current.resetSave();
    });

    expect(result.current.saveState.status).toBe('idle');
  });
});
```

**Why**: Testing each transition verifies state machine correctness. beforeEach resets store to known state. act() wraps state updates. toEqual checks entire state object including status-specific properties.

### Test Helper Functions

Test helper functions return correct values for each state.

```typescript
import { getIsLoading, getError, getLastSavedRecipe } from './helpers';

describe('State machine helpers', () => {
  it('getIsLoading returns true only in loading state', () => {
    expect(getIsLoading({ status: 'idle' })).toBe(false);
    expect(getIsLoading({ status: 'loading', pendingSaveUrl: 'url' })).toBe(true);
    expect(getIsLoading({ status: 'success', lastSavedRecipe: {} })).toBe(false);
    expect(getIsLoading({ status: 'error', error: new Error() })).toBe(false);
  });

  it('getError returns error only in error state', () => {
    const error = new Error('Test error');

    expect(getError({ status: 'idle' })).toBe(null);
    expect(getError({ status: 'loading', pendingSaveUrl: 'url' })).toBe(null);
    expect(getError({ status: 'success', lastSavedRecipe: {} })).toBe(null);
    expect(getError({ status: 'error', error })).toBe(error);
  });

  it('getLastSavedRecipe returns recipe only in success state', () => {
    const recipe = { id: '1', title: 'Recipe' };

    expect(getLastSavedRecipe({ status: 'idle' })).toBe(null);
    expect(getLastSavedRecipe({ status: 'loading', pendingSaveUrl: 'url' })).toBe(null);
    expect(getLastSavedRecipe({ status: 'success', lastSavedRecipe: recipe })).toBe(recipe);
    expect(getLastSavedRecipe({ status: 'error', error: new Error() })).toBe(null);
  });
});
```

**Why**: Helper function tests verify safe extraction logic. Test all states for each helper (idle, loading, success, error). Ensures helpers return null/false for invalid states, preventing runtime errors in components.

### Mock Store in Component Tests

Mock Zustand store to test components with different state machine states.

```typescript
import { render, screen } from '@testing-library/react-native';
import { useRecipeStore } from './useRecipeStore';
import { RecipeComponent } from './RecipeComponent';

jest.mock('./useRecipeStore', () => ({
  useRecipeStore: jest.fn(),
}));

describe('<RecipeComponent />', () => {
  it('renders loading state', () => {
    (useRecipeStore as jest.Mock).mockReturnValue({
      saveState: { status: 'loading', pendingSaveUrl: 'https://example.com' },
    });

    render(<RecipeComponent />);

    expect(screen.getByTestId('loading-spinner')).toBeTruthy();
  });

  it('renders success state with recipe', () => {
    const recipe = { id: '1', title: 'Test Recipe' };
    (useRecipeStore as jest.Mock).mockReturnValue({
      saveState: { status: 'success', lastSavedRecipe: recipe },
    });

    render(<RecipeComponent />);

    expect(screen.getByText('Test Recipe')).toBeTruthy();
  });

  it('renders error state with error message', () => {
    const error = new Error('Failed to load');
    (useRecipeStore as jest.Mock).mockReturnValue({
      saveState: { status: 'error', error },
    });

    render(<RecipeComponent />);

    expect(screen.getByText('Failed to load')).toBeTruthy();
  });

  it('renders idle state', () => {
    (useRecipeStore as jest.Mock).mockReturnValue({
      saveState: { status: 'idle' },
    });

    render(<RecipeComponent />);

    expect(screen.getByTestId('empty-state')).toBeTruthy();
  });
});
```

**Why**: Mocking store enables testing components in all states without triggering real state transitions. mockReturnValue sets specific state for each test. Test each status separately to verify correct rendering for all states.

## Common Patterns

### AsyncState for API Operations

Use AsyncState<T, E> for any async operation with loading/success/error.

```typescript
type AsyncState<T, E = Error> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: E };

type ProductStore = {
  products: AsyncState<Product[]>;
  fetchProducts: () => void;
};

export const useProductStore = create<ProductStore>((set) => ({
  products: { status: 'idle' },

  fetchProducts: async () => {
    set({ products: { status: 'loading' } });
    try {
      const data = await api.getProducts();
      set({ products: { status: 'success', data } });
    } catch (error) {
      set({ products: { status: 'error', error: error as Error } });
    }
  },
}));
```

**Why**: AsyncState<T, E> pattern works for any async operation. Consistent structure across all API calls. Type parameters enable type-safe data and errors.

### FormState for Multi-Step Forms

Use FormState with step tracking for wizards and multi-step forms.

```typescript
type FormStep = 'personal' | 'address' | 'payment' | 'review';

type FormState =
  | { status: 'editing'; currentStep: FormStep; data: Partial<FormData> }
  | { status: 'submitting'; data: FormData }
  | { status: 'success'; submittedData: FormData }
  | { status: 'error'; error: Error; data: FormData };
```

**Why**: FormState prevents invalid transitions (can't edit while submitting). Tracks current step for multi-step navigation. Preserves data across error states for retry.

### FeatureState for Feature Flags

Use FeatureState for feature flags with loading and error states.

```typescript
type FeatureState =
  | { status: 'loading' }
  | { status: 'enabled'; config: FeatureConfig }
  | { status: 'disabled' }
  | { status: 'error'; error: Error };

type FeatureFlagStore = {
  featureState: FeatureState;
  checkFeature: () => void;
};
```

**Why**: FeatureState handles async feature flag loading. Distinguishes between disabled (intentional) and error (failure). Can include config for enabled features.

### AuthState for Authentication

Use AuthState for authentication flows with user data.

```typescript
type AuthState =
  | { status: 'unauthenticated' }
  | { status: 'authenticating'; provider: string }
  | { status: 'authenticated'; user: User; token: string }
  | { status: 'error'; error: Error };

type AuthStore = {
  authState: AuthState;
  login: (provider: string) => void;
  logout: () => void;
};
```

**Why**: AuthState tracks authentication flow explicitly. Includes provider during authentication, user and token when authenticated. Clear separation between unauthenticated and error states.

## Common Mistakes to Avoid

❌ **Don't access properties without checking status first**:

```typescript
// ❌ Wrong - unsafe property access
const MyComponent = () => {
  const { saveState } = useRecipeStore();

  // Runtime error if status isn't 'success'
  return <RecipeView recipe={saveState.lastSavedRecipe} />;
};
```

**Why**: Discriminated unions only guarantee properties exist for specific status values. Accessing lastSavedRecipe without checking status === 'success' causes TypeScript error or runtime crash.

✅ **Do check status before accessing properties**:

```typescript
// ✅ Correct - safe property access
const MyComponent = () => {
  const { saveState } = useRecipeStore();

  if (saveState.status === 'success') {
    // TypeScript knows lastSavedRecipe exists
    return <RecipeView recipe={saveState.lastSavedRecipe} />;
  }

  return <EmptyView />;
};

// ✅ Or use helper function
const MyComponent = () => {
  const { saveState } = useRecipeStore();
  const recipe = getLastSavedRecipe(saveState);

  if (recipe) {
    return <RecipeView recipe={recipe} />;
  }

  return <EmptyView />;
};
```

**Why**: Status check narrows type, making property access safe. Helper function provides null when property doesn't exist, simplifying UI logic.

❌ **Don't use immer or middleware with state machines**:

```typescript
// ❌ Wrong - immer mutates state
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

export const useRecipeStore = create<RecipeStore>()(
  immer((set) => ({
    saveState: { status: 'idle' },
    startSave: (url: string) =>
      set((state) => {
        state.saveState = { status: 'loading', pendingSaveUrl: url };
      }),
  }))
);
```

**Why**: Immer hides state transitions with mutations. Makes state updates implicit and harder to trace. State machines need explicit transitions for predictability.

✅ **Do use plain Zustand stores**:

```typescript
// ✅ Correct - explicit state transitions
import { create } from 'zustand';

export const useRecipeStore = create<RecipeStore>((set) => ({
  saveState: { status: 'idle' },
  startSave: (url: string) =>
    set(() => ({
      saveState: { status: 'loading', pendingSaveUrl: url },
    })),
}));
```

**Why**: Plain stores make state transitions explicit. Each set() call clearly shows what state changes. Function form set(() => ({ ... })) ensures fresh state.

❌ **Don't allow impossible state combinations**:

```typescript
// ❌ Wrong - multiple boolean flags
type RecipeState = {
  isLoading: boolean;
  isSuccess: boolean;
  isError: boolean;
  data: Recipe | null;
  error: Error | null;
};

// Can have impossible states:
// { isLoading: true, isSuccess: true } ❌
// { isError: true, data: { ... } } ❌
```

**Why**: Boolean flags allow impossible combinations (both loading and success, both error and data). Requires checking multiple booleans, prone to logic errors.

✅ **Do use discriminated unions**:

```typescript
// ✅ Correct - impossible states unrepresentable
type RecipeState =
  | { status: 'loading' }
  | { status: 'success'; data: Recipe }
  | { status: 'error'; error: Error };

// Impossible states can't exist:
// Can't be both loading and success
// Can't have data without success status
// Can't have error without error status
```

**Why**: Discriminated unions make impossible states unrepresentable. Single status check determines entire state. TypeScript enforces correctness at compile time.

❌ **Don't forget exhaustive checking**:

```typescript
// ❌ Wrong - missing error case
const renderState = (state: AsyncState<T>) => {
  switch (state.status) {
    case 'idle':
      return <EmptyState />;
    case 'loading':
      return <LoadingSpinner />;
    case 'success':
      return <SuccessView data={state.data} />;
    // Missing 'error' case - runtime bug
  }
};
```

**Why**: Missing cases cause runtime bugs when unhandled state occurs. No compile-time error without exhaustive check.

✅ **Do use never type for exhaustive checking**:

```typescript
// ✅ Correct - exhaustive checking with never
const renderState = (state: AsyncState<T>) => {
  switch (state.status) {
    case 'idle':
      return <EmptyState />;
    case 'loading':
      return <LoadingSpinner />;
    case 'success':
      return <SuccessView data={state.data} />;
    case 'error':
      return <ErrorView error={state.error} />;
    default:
      const _exhaustive: never = state;
      return _exhaustive;
  }
};
```

**Why**: Default case with never type causes TypeScript error if any case missing. Compile-time guarantee that all states are handled.

❌ **Don't mutate state directly**:

```typescript
// ❌ Wrong - direct mutation
const { saveState } = useRecipeStore();
saveState.status = 'loading'; // TypeScript error, and doesn't trigger re-render
```

**Why**: Discriminated unions are readonly. Direct mutation doesn't trigger Zustand re-renders. TypeScript prevents this with type errors.

✅ **Do use store actions for updates**:

```typescript
// ✅ Correct - use store actions
const { startSave } = useRecipeStore();
startSave('https://example.com/recipe');

// Or setState for external updates
useRecipeStore.setState({
  saveState: { status: 'loading', pendingSaveUrl: 'url' },
});
```

**Why**: Store actions (startSave) trigger Zustand updates and re-renders. setState updates store from outside components. Both methods ensure immutable updates.

## Quick Reference

**Basic discriminated union**:
```typescript
type AsyncState<T, E = Error> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: E };
```

**Plain Zustand store**:
```typescript
import { create } from 'zustand';

export const useStore = create<State>((set) => ({
  state: { status: 'idle' },
  action: () => set(() => ({ state: { status: 'loading' } })),
}));
```

**Helper functions**:
```typescript
export const getIsLoading = (state: State): boolean =>
  state.status === 'loading';

export const getData = (state: State): Data | null =>
  state.status === 'success' ? state.data : null;
```

**Combine with mutation**:
```typescript
const mutation = useMutation({
  onSuccess: (data) => {
    useStore.setState({ state: { status: 'success', data } });
  },
  onError: (error) => {
    useStore.setState({ state: { status: 'error', error } });
  },
});
```

**Type narrowing**:
```typescript
if (state.status === 'success') {
  // TypeScript knows state.data exists
  return <View data={state.data} />;
}
```

**Exhaustive checking**:
```typescript
switch (state.status) {
  case 'idle': return <Empty />;
  case 'loading': return <Loading />;
  case 'success': return <Success data={state.data} />;
  case 'error': return <Error error={state.error} />;
  default:
    const _exhaustive: never = state;
    return _exhaustive;
}
```

**Test state transitions**:
```typescript
it('transitions from idle to loading', () => {
  const { result } = renderHook(() => useStore());

  act(() => {
    result.current.startLoad();
  });

  expect(result.current.state.status).toBe('loading');
});
```

**Key Libraries:**
- zustand 5.0.3
- @tanstack/react-query 5.59.16
- @testing-library/react-native 12.9.0
- TypeScript 5.1.6

For production examples, see [references/examples.md](references/examples.md).
