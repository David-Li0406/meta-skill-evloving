---
name: zustand-patterns
description: "WHAT: Zustand client state management for UI interactions and state machines. WHEN: UI state, form validation, filters, user preferences, complex UI flows. KEYWORDS: zustand, store, useShallow, immer, client state, selectors, actions, state machine, create."

tracked_repositories:
  - url: yourcompany/shared-mobile-modules
    type: internal
    paths:
      - /src/**/*Store.ts
      - /src/**/*store.ts
    last_synced: 2025-01-04T10:00:00Z
    sync_frequency: weekly

  - url: https://github.com/pmndrs/zustand
    type: external
    paths:
      - /docs/**/*.md
      - /readme.md
    last_synced: 2025-01-04T10:00:00Z
    sync_frequency: monthly
---

# Zustand State Management Patterns

## Core Principles

**Use Zustand for client state only.** Never store server data in Zustand stores. Use TanStack Query (REST) or Apollo Client (GraphQL) for server state.

**Why**: Separating client and server state prevents sync issues and enables optimistic updates with proper cache invalidation.

## When to Use This Skill

Use Zustand when you need to:

- Manage UI interaction state (modals, dropdowns, selected items)
- Handle form validation states
- Implement client-side filters and sorting
- Store user preferences before persistence
- Implement state machines for complex UI flows

**Don't use Zustand for**:
- API responses or cached server data
- Authentication tokens from backend
- Any data that should be refetchable from server

## File Organization

```
stores/
└── feature-name/
    ├── index.ts                # Export hooks only
    ├── feature-store.ts        # Store implementation
    ├── types.ts                # State/Actions interfaces
    ├── helpers.ts              # State extraction helpers (for state machines)
    └── feature-store.test.ts   # Tests
```

**Why**: Organized structure with clear separation makes stores easy to find, maintain, and test.

## Standard Store Pattern

### Step 1: Define Types

Always define separate interfaces for state and actions:

```typescript
// stores/cookbook-faq/types.ts
export interface CookbookFaqState {
  selectedCategory: string | null;
  isFilterOpen: boolean;
  searchQuery: string;
}

export interface CookbookFaqActions {
  setSelectedCategory: (category: string | null) => void;
  toggleFilter: () => void;
  updateSearchQuery: (query: string) => void;
  resetFilters: () => void;
}

export type CookbookFaqStore = CookbookFaqState & {
  actions: CookbookFaqActions;
};
```

**Why**: Separate types improve organization and make the store contract clear.

### Step 2: Implement Store

Use Immer middleware for safe nested updates and group actions:

```typescript
// stores/cookbook-faq/cookbook-faq-store.ts
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import type { CookbookFaqStore } from './types';

export const useCookbookFaqStore = create(
  immer<CookbookFaqStore>((set) => ({
    // Initial state
    selectedCategory: null,
    isFilterOpen: false,
    searchQuery: '',

    // Actions grouped
    actions: {
      setSelectedCategory: (category) =>
        set((state) => {
          state.selectedCategory = category;
        }),

      toggleFilter: () =>
        set((state) => {
          state.isFilterOpen = !state.isFilterOpen;
        }),

      updateSearchQuery: (query) =>
        set((state) => {
          state.searchQuery = query;
        }),

      resetFilters: () =>
        set((state) => {
          state.selectedCategory = null;
          state.isFilterOpen = false;
          state.searchQuery = '';
        }),
    },
  }))
);
```

**Why**: Immer middleware enables safe nested updates. Grouped actions prevent re-renders when accessing multiple actions.

### Step 3: Export Granular Selectors

Create focused selector hooks that only subscribe to specific state:

```typescript
// stores/cookbook-faq/index.ts
import { useCookbookFaqStore } from './cookbook-faq-store';

// Export granular selectors
export const useCookbookFaqSelectedCategory = () =>
  useCookbookFaqStore((state) => state.selectedCategory);

export const useCookbookFaqIsFilterOpen = () =>
  useCookbookFaqStore((state) => state.isFilterOpen);

export const useCookbookFaqSearchQuery = () =>
  useCookbookFaqStore((state) => state.searchQuery);

export const useCookbookFaqActions = () =>
  useCookbookFaqStore((state) => state.actions);

export type { CookbookFaqState, CookbookFaqActions } from './types';
```

**Why**: Granular selectors prevent unnecessary re-renders. Only components using specific state re-render when it changes.

### Step 4: Use in Components

```typescript
import {
  useCookbookFaqSelectedCategory,
  useCookbookFaqActions
} from '../../stores/cookbook-faq';

export const CookbookFaqScreen = () => {
  const selectedCategory = useCookbookFaqSelectedCategory();
  const { setSelectedCategory, resetFilters } = useCookbookFaqActions();

  return (
    <View>
      <CategoryFilter
        selectedCategory={selectedCategory}
        onCategorySelect={setSelectedCategory}
      />
      <Button onPress={resetFilters} title="Reset" />
    </View>
  );
};
```

**Why**: Component only subscribes to needed state, improving performance.

## Performance Optimization with useShallow

Use `useShallow` from `zustand/react/shallow` to prevent unnecessary re-renders when selecting multiple values:

```typescript
import { useShallow } from 'zustand/react/shallow';

// ✅ Select multiple primitives
export const useMealSelectionConfig = () =>
  useMealSelection(
    useShallow((state) => ({
      numberOfServings: state.selection?.config.numberOfServings,
      numberOfRecipes: state.selection?.config.numberOfRecipes,
      isSaving: state.isSaving,
    }))
  );

// ✅ Select with selector function
const pricesMapSelector = (state) => state.selection?.prices || {};
const prices = useMealSelection(useShallow(pricesMapSelector));

// ✅ Select single nested value
const numberOfServings =
  useMealSelection(useShallow((state) => state.selection?.config.numberOfServings)) ?? '2';
```

**Why**: `useShallow` performs shallow comparison on selected values, preventing re-renders when object references change but values remain the same. This is the recommended approach (100+ usages in production codebase).

### Two-Step Pattern for Arrays of Objects

Shallow comparison fails with arrays of objects. Use this two-step pattern:

```typescript
// Step 1: Get IDs only (primitives)
export const useActiveRecipeIds = () =>
  useRecipeStore(
    (state) => state.recipes
      .filter(recipe => recipe.isActive)
      .map(recipe => recipe.id),
    shallow
  );

// Step 2: Individual selectors
export const useRecipeById = (id: string) =>
  useRecipeStore(state => state.recipes.find(recipe => recipe.id === id));

// Usage
const ActiveRecipesList = () => {
  const activeIds = useActiveRecipeIds();
  return (
    <View>
      {activeIds.map(id => <ActiveRecipeCard key={id} recipeId={id} />)}
    </View>
  );
};

const ActiveRecipeCard = React.memo(({ recipeId }) => {
  const recipe = useRecipeById(recipeId);
  return <Card>{recipe?.name}</Card>;
});
```

**Why**: Primitives work with shallow comparison. Individual selectors minimize re-renders.

## State Machine Pattern with Discriminated Unions

For complex UI flows, use discriminated unions to represent state machines:

### Step 1: Define State Machine Types

```typescript
// stores/add-recipe-link/types.ts

type SaveRecipeState =
  | { status: 'idle' }
  | { status: 'loading'; pendingSaveUrl: string }
  | { status: 'success'; lastSavedRecipe: ExternalRecipe }
  | { status: 'error'; error: Error };

interface AddRecipeLinkState {
  isDrawerVisible: boolean;
  saveState: SaveRecipeState;
}

interface AddRecipeLinkActions {
  showDrawer: () => void;
  hideDrawer: () => void;
  startSaving: (url: string) => void;
  saveSuccess: (recipe: ExternalRecipe) => void;
  saveError: (error: Error) => void;
  resetSaveState: () => void;
}

export type AddRecipeLinkStore = AddRecipeLinkState & {
  actions: AddRecipeLinkActions;
};
```

**Why**: Discriminated unions ensure type-safe state transitions and prevent invalid state combinations.

### Step 2: Implement State Machine Store

```typescript
// stores/add-recipe-link/add-recipe-link-store.ts
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

export const useAddRecipeLinkStore = create(
  immer<AddRecipeLinkStore>((set) => ({
    isDrawerVisible: false,
    saveState: { status: 'idle' },

    actions: {
      showDrawer: () =>
        set((state) => {
          state.isDrawerVisible = true;
        }),

      hideDrawer: () =>
        set((state) => {
          state.isDrawerVisible = false;
        }),

      startSaving: (url) =>
        set((state) => {
          state.saveState = { status: 'loading', pendingSaveUrl: url };
        }),

      saveSuccess: (recipe) =>
        set((state) => {
          state.saveState = { status: 'success', lastSavedRecipe: recipe };
        }),

      saveError: (error) =>
        set((state) => {
          state.saveState = { status: 'error', error };
        }),

      resetSaveState: () =>
        set((state) => {
          state.saveState = { status: 'idle' };
        }),
    },
  }))
);
```

### Step 3: Create Helper Functions

Create helpers to safely extract values from state machine states:

```typescript
// stores/add-recipe-link/helpers.ts

export const getIsLoading = (saveState: SaveRecipeState): boolean =>
  saveState.status === 'loading';

export const getIsError = (saveState: SaveRecipeState): boolean =>
  saveState.status === 'error';

export const getIsSuccess = (saveState: SaveRecipeState): boolean =>
  saveState.status === 'success';

export const getError = (saveState: SaveRecipeState): Error | null =>
  saveState.status === 'error' ? saveState.error : null;

export const getPendingSaveUrl = (saveState: SaveRecipeState): string | null =>
  saveState.status === 'loading' ? saveState.pendingSaveUrl : null;

export const getLastSavedRecipe = (saveState: SaveRecipeState): ExternalRecipe | null =>
  saveState.status === 'success' ? saveState.lastSavedRecipe : null;
```

**Why**: Helper functions prevent runtime errors from accessing properties that don't exist in certain states.

### Step 4: Integrate with API Mutations

Combine Zustand store with TanStack Query mutations:

```typescript
// stores/add-recipe-link/useAddRecipeLinkWithAPI.ts
import { useAddRecipeLinkStore } from './add-recipe-link-store';
import { useCreateExternalRecipe } from '@data-access/query/recipes';

export const useAddRecipeLinkWithAPI = ({ refetch }: { refetch: () => void }) => {
  const store = useAddRecipeLinkStore();
  const { showDrawer, hideDrawer, startSaving, saveSuccess, saveError, resetSaveState } =
    store.actions;

  const createRecipeMutation = useCreateExternalRecipe({
    onSuccess: (data) => {
      refetch(); // Refresh recipe list
      saveSuccess(data);
      setTimeout(() => {
        hideDrawer();
        resetSaveState();
      }, 2000); // Show success message briefly
    },
    onError: (error) => {
      saveError(error as Error);
    },
  });

  const saveRecipeLink = (url: string) => {
    startSaving(url);
    createRecipeMutation.mutate({ url });
  };

  return {
    ...store,
    saveRecipeLink,
  };
};
```

**Why**: Clean separation between UI state (Zustand) and API operations (TanStack Query).

### Step 5: Use in Components

```typescript
import { useAddRecipeLinkStore } from '../../stores/add-recipe-link';
import { useAddRecipeLinkWithAPI } from '../../stores/add-recipe-link/useAddRecipeLinkWithAPI';
import { getIsLoading, getIsError, getError, getIsSuccess } from '../../stores/add-recipe-link/helpers';

const AddRecipeDrawer = ({ refetch }) => {
  const { isDrawerVisible, saveState, actions } = useAddRecipeLinkStore();
  const { saveRecipeLink } = useAddRecipeLinkWithAPI({ refetch });
  const [url, setUrl] = useState('');

  const isLoading = getIsLoading(saveState);
  const isError = getIsError(saveState);
  const isSuccess = getIsSuccess(saveState);
  const error = getError(saveState);

  return (
    <Drawer visible={isDrawerVisible} onClose={actions.hideDrawer}>
      <InputField
        value={url}
        onChangeText={setUrl}
        disabled={isLoading}
      />

      {isError && <InlineMessage variant="error">{error?.message}</InlineMessage>}
      {isSuccess && <InlineMessage variant="success">Recipe saved!</InlineMessage>}

      <Button onPress={() => saveRecipeLink(url)} disabled={!url || isLoading} loading={isLoading}>
        Save Recipe
      </Button>
    </Drawer>
  );
};
```

## Testing Zustand Stores

### Testing Standard Stores

```typescript
import { renderHook, act } from '@testing-library/react';
import { useCookbookFaqSelectedCategory, useCookbookFaqActions } from '../index';

describe('CookbookFaq Store', () => {
  it('should update selected category', () => {
    const { result: actions } = renderHook(() => useCookbookFaqActions());
    const { result: category } = renderHook(() => useCookbookFaqSelectedCategory());

    expect(category.current).toBeNull();

    act(() => {
      actions.current.setSelectedCategory('appetizers');
    });

    expect(category.current).toBe('appetizers');
  });
});
```

### Testing State Machines

```typescript
import { renderHook, act } from '@testing-library/react';
import { useAddRecipeLinkStore } from './add-recipe-link-store';
import { getIsLoading, getIsError, getPendingSaveUrl } from './helpers';

describe('AddRecipeLink State Machine', () => {
  it('transitions from idle to loading', () => {
    const { result } = renderHook(() => useAddRecipeLinkStore());

    expect(result.current.saveState.status).toBe('idle');

    act(() => {
      result.current.actions.startSaving('https://example.com/recipe');
    });

    expect(getIsLoading(result.current.saveState)).toBe(true);
    expect(getPendingSaveUrl(result.current.saveState)).toBe('https://example.com/recipe');
  });

  it('transitions to error state on failure', () => {
    const { result } = renderHook(() => useAddRecipeLinkStore());
    const error = new Error('Network error');

    act(() => {
      result.current.actions.startSaving('https://example.com/recipe');
    });

    act(() => {
      result.current.actions.saveError(error);
    });

    expect(getIsError(result.current.saveState)).toBe(true);
    expect(getError(result.current.saveState)).toBe(error);
  });
});
```

## Common Mistakes to Avoid

❌ **Don't store server data in Zustand**:

```typescript
interface BadStore {
  user: User | null; // Use useUserQuery instead
  recipes: Recipe[]; // Use useRecipesQuery instead
}
```

❌ **Don't export the main store hook**:

```typescript
// Bad - allows bypassing granular selectors
export const useCookbookFaqStore = create<Store>(...);
```

❌ **Don't use shallow for arrays of objects**:

```typescript
// Bad - will cause unnecessary re-renders
export const useActiveRecipes = () =>
  useRecipeStore(
    (state) => ({
      activeRecipes: state.recipes.filter((r) => r.isActive), // New objects every time
    }),
    shallow // Won't work - objects have different references
  );
```

✅ **Do separate client and server state**:

```typescript
// Client state from Zustand
const selectedRecipeId = useRecipeListSelectedId();

// Server state from TanStack Query
const { data: recipes } = useRecipesQuery();

// Combine in component
<RecipeGrid recipes={recipes} selectedId={selectedRecipeId} />
```

## Quick Reference

**Standard Store Pattern:**
1. Define types (State, Actions, Store)
2. Implement with `create` + `immer` middleware
3. Group actions in `actions` object
4. Export granular selector hooks only

**Performance:**
- Use `useShallow` for selecting multiple primitives or derived state
- Use two-step pattern (IDs + individual selectors) for arrays of objects
- Keep selectors focused to minimize re-renders

**State Machines:**
1. Use discriminated unions for state
2. Create helper functions for safe state extraction
3. Integrate with TanStack Query mutations
4. Test state transitions

**Key Rule:** Zustand = client state, TanStack Query/Apollo = server state

For production examples, see [references/examples.md](references/examples.md).
For Zustand API reference, see [references/api-docs.md](references/api-docs.md).
