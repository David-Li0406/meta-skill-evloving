# State Machines - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating state machine patterns with discriminated unions.

## Example 1: Zustand Store with Discriminated Union

**File**: `modules/social-recipe-bridge/stores/useAddRecipeLinkStore.ts:1`

This example shows a complete Zustand store using discriminated unions for save recipe state machine.

```typescript
import { create } from 'zustand';

import { useCreateExternalRecipe } from '../../../data-access/query/external-recipes/hooks';
import type {
  ExternalRecipeListItem,
  CreateExternalRecipeRequest,
} from '../../../data-access/query/external-recipes/types';

// State machine using discriminated unions
type SaveRecipeState =
  | { status: 'idle' }
  | { status: 'loading'; pendingSaveUrl: string }
  | { status: 'success'; lastSavedRecipe: ExternalRecipeListItem }
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

// Helper functions to extract computed values from the state machine
export const getIsError = (saveState: SaveRecipeState): boolean =>
  saveState.status === 'error';

export const getError = (saveState: SaveRecipeState): Error | null =>
  saveState.status === 'error' ? saveState.error : null;

export const getLastSavedRecipe = (
  saveState: SaveRecipeState
): ExternalRecipeListItem | null =>
  saveState.status === 'success' ? saveState.lastSavedRecipe : null;

export const getPendingSaveUrl = (saveState: SaveRecipeState): string | null =>
  saveState.status === 'loading' ? saveState.pendingSaveUrl : null;

export const getIsLoading = (saveState: SaveRecipeState): boolean =>
  saveState.status === 'loading';
```

**Key patterns demonstrated:**
- Discriminated union SaveRecipeState with 4 states (idle, loading, success, error)
- Each state has unique 'status' property for type discrimination
- State-specific properties (pendingSaveUrl in loading, lastSavedRecipe in success, error in error)
- Plain Zustand store with create() (no middleware)
- Function form set(() => ({ ... })) for state updates
- Explicit state transitions (idle → loading, loading → success/error, any → idle)
- Helper functions for safe property extraction (getIsLoading, getError, getLastSavedRecipe, getPendingSaveUrl)
- Helper returns boolean/null when property doesn't exist in current state
- Optimistic UI (hide drawer when starting save)

## Example 2: Combining State Machine with API Mutation

**File**: `modules/social-recipe-bridge/stores/useAddRecipeLinkStore.ts:64`

This example shows custom hook pattern combining Zustand store with TanStack Query mutation.

```typescript
// Custom hook that combines the store with the API mutation
export const useAddRecipeLinkWithAPI = ({
  refetch,
}: {
  refetch: () => void;
}) => {
  const store = useAddRecipeLinkStore();
  const createRecipeMutation = useCreateExternalRecipe({
    onSuccess: (data) => {
      refetch();
      useAddRecipeLinkStore.setState({
        saveState: { status: 'success', lastSavedRecipe: data },
      });
    },
    onError: (error) => {
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

**Key patterns demonstrated:**
- Custom hook combines Zustand store with TanStack Query mutation
- onSuccess callback updates store with success state
- onError callback updates store with error state
- setState used for external updates (from mutation callbacks)
- Loading state set optimistically before API call (by onSaveRecipeLink)
- Success/error states set in callbacks after API response
- Refetch data on success to sync with server
- Spread store state/actions (...store) to expose them
- Separates state management (Zustand) from API logic (TanStack Query)
- Type casting (error as Error) for error handling

## Example 3: Using Helper Functions in Components

**File**: `modules/social-recipe-bridge/screens/social-recipe-bridge/SocialRecipeBridgeScreen.tsx:64`

This example shows usage of helper functions to safely extract state machine properties in components.

```typescript
import { useAddRecipeLinkWithAPI, useAddRecipeLinkStore } from '../../stores';
import { getIsLoading } from '../../stores/useAddRecipeLinkStore';

export const SocialRecipeBridgeScreen = () => {
  const {
    data: infiniteData,
    isLoading,
    refetch,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useGetExternalRecipesInfinite({});

  // Flatten all pages into a single array of recipes
  const recipes = infiniteData?.pages.flatMap((page) => page.data) || [];
  const { isDrawerVisible, showDrawer, hideDrawer, saveRecipeLink, saveState } =
    useAddRecipeLinkWithAPI({ refetch });

  // Get recipe creation loading state using helper function
  const { saveState: storeSaveState } = useAddRecipeLinkStore();
  const isCreatingRecipe = getIsLoading(storeSaveState);

  // ... rest of component
};
```

**Key patterns demonstrated:**
- Import helper function (getIsLoading) from store file
- Access store state directly (useAddRecipeLinkStore())
- Use helper function for safe extraction (getIsLoading(storeSaveState))
- Helper returns boolean, no null checks needed in component
- Combine store hook (useAddRecipeLinkStore) with custom hook (useAddRecipeLinkWithAPI)
- Custom hook provides actions (saveRecipeLink) and state (saveState)
- Store hook provides direct state access for helper functions
- No direct property access (storeSaveState.pendingSaveUrl) - always use helpers

## Example 4: ProductListingResult Discriminated Union

**File**: `operations/product-listing/types.ts:1`

This example shows discriminated union type for product listing operation result.

```typescript
/**
 * Result type for the product listing operation
 * Represents different states of the operation (success, error, loading)
 *
 * This type uses a discriminated union pattern with a 'status' field
 */
export type ProductListingResult =
  | {
      status: 'success';
      data: ProductListingProduct[];
    }
  | {
      status: 'error';
      retry: () => void;
      error: Error;
    }
  | {
      status: 'loading';
    };
```

**Key patterns demonstrated:**
- Discriminated union ProductListingResult with 3 states (success, error, loading)
- 'status' property is discriminator (all states have it)
- success state includes data array
- error state includes error object and retry function
- loading state has no additional properties
- Retry function provided in error state for immediate retry capability
- Return type from operation hooks (not store state, but operation result)
- Type documentation explains discriminated union pattern

## Example 5: Operation Returning State Machine Result

**File**: `operations/product-listing/useProductListingOperation.ts:1`

This example shows operation pattern that returns discriminated union result based on query state.

```typescript
export const useProductListing = ({
  planId,
  selectedWeekId,
  selectedCategory,
  selectedSubcategory,
  selectedFilters,
  selectedSorting,
  initialData,
}: ProductListingOperationInput): ProductListingResult => {
  const { data, loading, error, retry } = useGetStoreProducts({
    planId,
    selectedWeekId,
    selectedFilters,
    selectedSorting,
    selectedCategory,
    selectedSubcategory,
    initialData,
  });

  if (loading) {
    return {
      status: 'loading',
    };
  }

  if (error || !data) {
    return {
      status: 'error',
      error: error || new Error('Unknown error'),
      retry: retry,
    };
  }

  return {
    status: 'success',
    data,
  };
};
```

**Key patterns demonstrated:**
- Operation hook returns discriminated union result (ProductListingResult)
- Conditional returns based on query state (loading, error, success)
- Early return pattern (loading first, then error, then success)
- Pass retry function from query to error state
- Default error when error is undefined but no data (new Error('Unknown error'))
- Type narrowing: TypeScript knows data exists in success return
- Operation transforms query state (loading, error, data) to state machine (status, data/error)
- No Zustand store - operation result is returned directly
- Caller decides how to handle each status (render different UI)

## Example 6: Testing Helper Functions

**File**: `modules/social-recipe-bridge/screens/add-recipe-link-drawer/AddRecipeLinkDrawer.test.tsx:36`

This example shows mocking helper functions in component tests.

```typescript
// Mock the store
jest.mock('../../stores', () => ({
  useAddRecipeLinkWithAPI: jest.fn(() => ({
    saveState: { status: 'idle' },
    clearError: jest.fn(),
  })),
  getIsError: jest.fn((saveState) => saveState.status === 'error'),
  getError: jest.fn((saveState) =>
    saveState.status === 'error' ? saveState.error : null
  ),
  getLastSavedRecipe: jest.fn((saveState) =>
    saveState.status === 'success' ? saveState.lastSavedRecipe : null
  ),
}));

describe('AddRecipeLinkDrawer', () => {
  const mockOnDismiss = jest.fn();
  const mockOnSave = jest.fn();
  const mockRefetch = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  const defaultProps = {
    visible: true,
    onDismiss: mockOnDismiss,
    onSave: mockOnSave,
    refetch: mockRefetch,
    entryPoint: 'empty_state' as const,
  };

  describe('Rendering', () => {
    it('renders the drawer when visible is true', () => {
      render(<AddRecipeLinkDrawer {...defaultProps} />);

      expect(screen.getByTestId('add-recipe-link-drawer')).toBeTruthy();
      expect(screen.getByTestId('drawer-title')).toBeTruthy();
      expect(screen.getByTestId('recipe-link-input')).toBeTruthy();
      expect(screen.getByTestId('save-button')).toBeTruthy();
    });

    it('does not render when visible is false', () => {
      render(<AddRecipeLinkDrawer {...defaultProps} visible={false} />);

      expect(screen.queryByTestId('add-recipe-link-drawer')).toBeFalsy();
    });
  });

  describe('User Interactions', () => {
    it('save button is disabled when input is empty', () => {
      render(<AddRecipeLinkDrawer {...defaultProps} />);

      const saveButton = screen.getByTestId('save-button');
      expect(saveButton.props.accessibilityState.disabled).toBe(true);
    });

    it('save button is enabled when valid URL is entered', async () => {
      render(<AddRecipeLinkDrawer {...defaultProps} />);

      const input = screen.getByTestId('recipe-link-input');
      fireEvent.changeText(input, 'https://example.com/recipe');

      await waitFor(() => {
        const saveButton = screen.getByTestId('save-button');
        expect(saveButton.props.accessibilityState.disabled).toBe(false);
      });
    });

    it('calls onSave with URL when save button is pressed with valid URL', async () => {
      render(<AddRecipeLinkDrawer {...defaultProps} />);

      const input = screen.getByTestId('recipe-link-input');
      const validUrl = 'https://example.com/recipe';

      fireEvent.changeText(input, validUrl);

      await waitFor(() => {
        const saveButton = screen.getByTestId('save-button');
        expect(saveButton.props.accessibilityState.disabled).toBe(false);
      });

      const saveButton = screen.getByTestId('save-button');
      fireEvent.press(saveButton);

      expect(mockOnSave).toHaveBeenCalledWith(validUrl);
    });
  });
});
```

**Key patterns demonstrated:**
- Mock entire store module with jest.mock
- Mock useAddRecipeLinkWithAPI to return specific saveState
- Mock helper functions (getIsError, getError, getLastSavedRecipe) with implementation
- Helper mock implementations match real logic (check status, return property or null)
- Mock returns idle state by default in tests
- clearError mocked as jest.fn() for action testing
- beforeEach clears all mocks to reset state between tests
- Component tests verify UI behavior, not state machine logic
- Test user interactions (input changes, button presses)
- waitFor for async state updates
- Use testID for querying elements
- Test both truthy (getByTestId) and falsy (queryByTestId) cases

## Summary

The YourCompany codebase consistently follows these state machine patterns:

1. **Discriminated Unions** - 'status' discriminator with idle/loading/success/error states
2. **State-Specific Properties** - pendingSaveUrl (loading), data (success), error (error)
3. **Plain Zustand Stores** - create() without middleware, explicit set() calls
4. **Function Form set()** - set(() => ({ ... })) for state updates
5. **Helper Functions** - getIsLoading, getError, getLastSavedRecipe for safe extraction
6. **Helper Returns** - Boolean/null when property doesn't exist, no exceptions
7. **Custom Hooks** - Combine Zustand store with TanStack Query/Apollo mutations
8. **setState for External Updates** - Use in mutation callbacks (onSuccess, onError)
9. **Optimistic UI** - Set loading state before API call
10. **Operation Pattern** - Return discriminated union from operations (useProductListing)
11. **Type Narrowing** - if (state.status === 'success') enables safe property access
12. **Mock Helper Functions** - Mock with real logic (check status, return property or null)
13. **Test Component Behavior** - Test UI, not state machine transitions
14. **Explicit Transitions** - idle → loading → success/error, any → idle

These patterns enable type-safe state management, eliminate impossible states, make state transitions explicit and testable, prevent race conditions, and provide predictable UI behavior through discriminated unions and helper functions.
