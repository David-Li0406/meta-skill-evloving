---
name: context-pattern
description: Provides a React Context implementation pattern using useSyncExternalStore, with types, hooks, and examples. Be specific about capabilities and when to use the skill.
---

# React Context Pattern Guide

### When to use this skill ✅

- Create a reusable Context implementation that avoids unnecessary re-renders.
- Add a standardized pattern for `Context` + selector hooks across a repository.
- Provide examples, templates, or scripts for implementing `useSyncExternalStore`-based contexts.
- Share best practices for performance-sensitive state management and selector optimization.
- Teach the agent to apply this pattern during code reviews, refactors, or feature scaffolding.

## Overview

This guide provides comprehensive instructions for AI agents to generate professional, type-safe React Context implementations using the **Subscription Pattern with `useSyncExternalStore`**. This pattern avoids unnecessary re-renders and provides optimal performance for state management.

## Pattern Architecture

This Context Pattern uses the following key concepts:

1. **useRef for State Storage**: State is stored in `useRef` instead of `useState` to prevent re-renders
2. **Subscription Pattern**: Components subscribe to state changes manually
3. **useSyncExternalStore**: React 18+ hook for subscribing to external stores with automatic re-rendering
4. **Type Safety**: Full TypeScript support with explicit type definitions
5. **Separation of Concerns**: Separate files for types, context, hooks, and selectors

### Why This Pattern?

- Re-renders all consumers on any state change
- Only re-renders components that use changed values
- Uses `useState` causing cascading updates
- Uses `useRef` + subscriptions for granular control
- Performance issues with frequent updates
- Performance issues with frequent updates
- Optimal performance with `useSyncExternalStore`

---

## File Structure

```architecture
src/
└── context/
    └── FeatureName/
        ├── Context.tsx      # Context creation and Provider component
        ├── types.ts         # TypeScript type definitions
        ├── useContext.ts    # Custom hook to access context
        ├── useSelectors.ts  # Selector hooks using useSyncExternalStore
        └── index.ts         # Public exports
```

### Naming Conventions

- **Folder**: Use PascalCase feature name (e.g., `CreateTask`, `UserProfile`, `ShoppingCart`)
- **Files**: Use exact names: `Context.tsx`, `types.ts`, `useContext.ts`, `useSelectors.ts`
- **Exports**: Export from `index.ts` for clean imports

---

## Type Definitions

### File: `types.ts`

Define all TypeScript types for the context in a separate file.

```
// types.ts
import type { PropsWithChildren } from "react";

/**
 * Props for the Provider component
 * Uses React's PropsWithChildren for automatic children typing
 */
export type TProviderProps = PropsWithChildren;

/**
 * Callback type for subscribers
 * Called when state changes occur
 */
export type TSubscriberCallback = () => void;

/**
 * Context value type definition
 * Contains all getters, setters, and subscribe function
 */
export type TContext = {
  // Getters - return current state values
  getIsOpen: () => boolean;
  getLatestTask: () => TTask | undefined;

  // Setters - update state values
  setIsOpen: (value: boolean) => void;
  setLatestTask: (value:  TTask | undefined) => void;

  // Subscribe function - for useSyncExternalStore integration
  subscribe: (callback: TSubscriberCallback) => () => void;
};
```

### Type Definition Rules

1. **Always define `TProviderProps`** using `PropsWithChildren`
2. **Always define `TSubscriberCallback`** as `() => void`
3. **Always define `TContext`** with:
   - Getter functions: `get{StateName}:  () => StateType`
   - Setter functions: `set{StateName}: (value: StateType) => void`
   - Subscribe function: `subscribe: (callback: TSubscriberCallback) => () => void`

---

## Context Provider Implementation

### File: `Context.tsx`

```
// Context.tsx
import { createContext, useCallback, useRef } from "react";

import type { TContext, TProviderProps, TSubscriberCallback } from "./types";

/**
 * Create context with null as initial value
 * This allows type checking when context is not available
 */
export const Context = createContext<TContext | null>(null);

/**
 * Provider component that manages state and subscriptions
 */
export function Provider({ children }: TProviderProps) {
  // ============================================
  // STATE REFS - Store state without causing re-renders
  // ============================================

  const isOpen = useRef<boolean>(false);
  const latestTask = useRef<TTask | undefined>(undefined);

  // ============================================
  // SUBSCRIBERS SET - Track all subscribed callbacks
  // ============================================

  const subscribers = useRef<Set<TSubscriberCallback>>(new Set());

  // ============================================
  // GETTERS - Return current state values
  // ============================================

  const getIsOpen = useCallback((): boolean => {
    return isOpen.current;
  }, []);

  const getLatestTask = useCallback((): TTask | undefined => {
    return latestTask. current;
  }, []);

  // ============================================
  // SETTERS - Update state and notify subscribers
  // ============================================

  const setIsOpen = useCallback((value: boolean): void => {
    // Optimization: skip if value hasn't changed
    if (isOpen.current === value) {
      return;
    }

    isOpen.current = value;

    // Notify all subscribers about the change
    subscribers.current. forEach((callback) => callback());
  }, []);

  const setLatestTask = useCallback((value: TTask | undefined): void => {
    latestTask.current = value;
    subscribers.current.forEach((callback) => callback());
  }, []);

  // ============================================
  // SUBSCRIBE - Allow components to subscribe to changes
  // ============================================

  const subscribe = useCallback((callback: TSubscriberCallback) => {
    subscribers.current. add(callback);

    // Return unsubscribe function for cleanup
    return (): void => {
      subscribers. current.delete(callback);
    };
  }, []);

  // ============================================
  // RENDER PROVIDER
  // ============================================

  return (
    <Context. Provider
      value={{
        getIsOpen,
        setIsOpen,
        getLatestTask,
        setLatestTask,
        subscribe,
      }}
    >
      {children}
    </Context.Provider>
  );
}
```

### Provider Implementation Rules

1. **Create context with `null`**: `createContext<TContext | null>(null)`
2. **Use `useRef` for state**: Never use `useState` for stored values
3. **Use `useRef<Set<TSubscriberCallback>>` for subscribers**: Initialize with `new Set()`
4. **Wrap all functions in `useCallback`**: With empty dependency array `[]`
5. **Getters**: Simply return `ref.current`
6. **Setters**:
   - Optionally check if value changed (for optimization)
   - Update `ref.current`
   - Call all subscribers: `subscribers.current.forEach((callback) => callback())`
7. **Subscribe function**:
   - Add callback to Set
   - Return cleanup function that removes callback from Set

---

## Custom Hook Implementation

### File: `useContext.ts`

```
// useContext.ts
import { useContext } from "react";

import { Context } from "./Context";
import type { TContext } from "./types";

/**
 * Custom hook to access the context
 * Throws an error if used outside of Provider
 *
 * @returns TContext - The context value with all methods
 * @throws Error if context is not available
 */
export const useCreateTaskContext = (): TContext => {
  const context = useContext(Context);

  if (context === null) {
    throw new Error("CreateTask context is not available");
  }

  return context;
};
```

### Hook Implementation Rules

1. **Name the hook**: `use{FeatureName}Context` (e.g., `useCreateTaskContext`, `useUserProfileContext`)
2. **Import React's `useContext`** from "react"
3. **Import `Context`** from local "./Context"
4. **Import `TContext` type** from "./types"
5. **Check for null**: Always throw descriptive error if context is null
6. **Return typed context**: Function must return `TContext`

---

## Selectors Implementation

### File: `useSelectors.ts`

```
// useSelectors.ts
import { useSyncExternalStore } from "react";

import { useCreateTaskContext } from "./useContext";

// ============================================
// SELECTOR HOOKS - Subscribe to specific state slices
// ============================================

/**
 * Selector hook for isOpen state
 * Only re-renders when isOpen changes
 *
 * @returns boolean - Current isOpen value
 */
export const useCreateTaskModalOpenSelector = (): boolean => {
  const { getIsOpen, subscribe } = useCreateTaskContext();

  return useSyncExternalStore(subscribe, getIsOpen, getIsOpen);
};

/**
 * Selector hook for latestTask state
 * Only re-renders when latestTask changes
 *
 * @returns TTask | undefined - Current latestTask value
 */
export const useLatestCreatedTaskSelector = (): TTask | undefined => {
  const { getLatestTask, subscribe } = useCreateTaskContext();

  return useSyncExternalStore(subscribe, getLatestTask, getLatestTask);
};

// ============================================
// DISPATCH HOOKS - Return setter functions directly
// ============================================

/**
 * Dispatch hook for setIsOpen
 * Returns the setter function for external use
 *
 * @returns (value: boolean) => void
 */
export const useSetCreateTaskModalOpenDispatch = () => {
  return useCreateTaskContext().setIsOpen;
};

/**
 * Dispatch hook for setLatestTask
 * Returns the setter function for external use
 *
 * @returns (value: TTask | undefined) => void
 */
export const useSetLatestCreatedTaskDispatch = () => {
  return useCreateTaskContext().setLatestTask;
};
```

### Selector Implementation Rules

#### Selector Hooks (for reading state)

1. **Name pattern**: `use{FeatureName}{StateName}Selector`
2. **Use `useSyncExternalStore`**: Import from "react"
3. **Destructure `subscribe` and getter**: `const { get{State}, subscribe } = useContext()`
4. **Return**: `useSyncExternalStore(subscribe, getter, getter)`
   - First param: subscribe function
   - Second param: getSnapshot (client)
   - Third param: getServerSnapshot (SSR - use same getter)

#### Dispatch Hooks (for updating state)

1. **Name pattern**: `useSet{FeatureName}{StateName}Dispatch`
2. **Simply return the setter**: `return useContext().set{StateName}`
3. **No need for `useSyncExternalStore`**: Dispatchers don't subscribe to changes

---

## Best Practices

### 1. Always Use This File Structure

```
context/
└── FeatureName/
    ├── Context.tsx
    ├── types.ts
    ├── useContext.ts
    ├── useSelectors.ts
    └── index.ts
```

### 2. Export Pattern in index.ts

```
// index.ts
export { Provider } from "./Context";
export { useCreateTaskContext } from "./useContext";
export {
  useCreateTaskModalOpenSelector,
  useLatestCreatedTaskSelector,
  useSetCreateTaskModalOpenDispatch,
  useSetLatestCreatedTaskDispatch,
} from "./useSelectors";
export type { TContext, TProviderProps } from "./types";
```

### 3. Optimization Check in Setters

```
const setIsOpen = useCallback((value: boolean): void => {
  // Skip update if value hasn't changed
  if (isOpen.current === value) {
    return;
  }

  isOpen.current = value;
  subscribers.current.forEach((callback) => callback());
}, []);
```

### 4. Type Safety

- Always define explicit return types
- Use `TContext | null` for createContext
- Export types from `types.ts`

### 5. Naming Conventions

- **Context folder:** Use **PascalCase**. For example: `CreateTask` or `UserProfile`.
- **Provider:** Always name the file or component **Provider**.
- **Context hook:** Use the word "use", then the feature name, then "Context". Example: `useCreateTaskContext`.
- **Selector hook:** Use "use", then the feature, then the state name, and "Selector". Example: `useCreateTaskModalOpenSelector`
- **Dispatch hook:** Use "useSet", then the feature, then the state, and "Dispatch". Example: `useSetCreateTaskModalOpenDispatch`.
- **Context type:** Use the letter "T" and the word "Context". Example: **TContext**.
- **Subscriber callback:** Use "T", then "SubscriberCallback". Example: **TSubscriberCallback**.

---

## Complete Example

### Feature: ShoppingCart

#### types.ts

```
import type { PropsWithChildren } from "react";

export type TProviderProps = PropsWithChildren;

export type TSubscriberCallback = () => void;

export type TCartItem = {
  id: string;
  name: string;
  price: number;
  quantity: number;
};

export type TContext = {
  // Getters
  getItems: () => TCartItem[];
  getIsCartOpen: () => boolean;
  getTotalPrice: () => number;

  // Setters
  setItems: (value: TCartItem[]) => void;
  setIsCartOpen: (value: boolean) => void;

  // Subscribe
  subscribe: (callback: TSubscriberCallback) => () => void;
};
```

#### Context.tsx

```
import { createContext, useCallback, useRef } from "react";

import type { TContext, TProviderProps, TSubscriberCallback, TCartItem } from "./types";

export const Context = createContext<TContext | null>(null);

export function Provider({ children }: TProviderProps) {
  // State refs
  const items = useRef<TCartItem[]>([]);
  const isCartOpen = useRef<boolean>(false);

  // Subscribers
  const subscribers = useRef<Set<TSubscriberCallback>>(new Set());

  // Getters
  const getItems = useCallback((): TCartItem[] => {
    return items.current;
  }, []);

  const getIsCartOpen = useCallback((): boolean => {
    return isCartOpen. current;
  }, []);

  const getTotalPrice = useCallback((): number => {
    return items.current.reduce(
      (total, item) => total + item.price * item. quantity,
      0
    );
  }, []);

  // Setters
  const setItems = useCallback((value: TCartItem[]): void => {
    items. current = value;
    subscribers.current.forEach((callback) => callback());
  }, []);

  const setIsCartOpen = useCallback((value: boolean): void => {
    if (isCartOpen.current === value) {
      return;
    }

    isCartOpen.current = value;
    subscribers.current.forEach((callback) => callback());
  }, []);

  // Subscribe
  const subscribe = useCallback((callback: TSubscriberCallback) => {
    subscribers.current.add(callback);

    return (): void => {
      subscribers.current.delete(callback);
    };
  }, []);

  return (
    <Context.Provider
      value={{
        getItems,
        getIsCartOpen,
        getTotalPrice,
        setItems,
        setIsCartOpen,
        subscribe,
      }}
    >
      {children}
    </Context.Provider>
  );
}
```

#### useContext.ts

```
import { useContext } from "react";

import { Context } from "./Context";
import type { TContext } from "./types";

export const useShoppingCartContext = (): TContext => {
  const context = useContext(Context);

  if (context === null) {
    throw new Error("ShoppingCart context is not available");
  }

  return context;
};
```

#### useSelectors.ts

```
import { useSyncExternalStore } from "react";

import { useShoppingCartContext } from "./useContext";
import type { TCartItem } from "./types";

// Selectors
export const useCartItemsSelector = (): TCartItem[] => {
  const { getItems, subscribe } = useShoppingCartContext();
  return useSyncExternalStore(subscribe, getItems, getItems);
};

export const useCartOpenSelector = (): boolean => {
  const { getIsCartOpen, subscribe } = useShoppingCartContext();
  return useSyncExternalStore(subscribe, getIsCartOpen, getIsCartOpen);
};

export const useCartTotalPriceSelector = (): number => {
  const { getTotalPrice, subscribe } = useShoppingCartContext();
  return useSyncExternalStore(subscribe, getTotalPrice, getTotalPrice);
};

// Dispatchers
export const useSetCartItemsDispatch = () => {
  return useShoppingCartContext().setItems;
};

export const useSetCartOpenDispatch = () => {
  return useShoppingCartContext().setIsCartOpen;
};
```

#### index.ts

```
export { Provider as ShoppingCartProvider } from "./Context";
export { useShoppingCartContext } from "./useContext";
export {
  useCartItemsSelector,
  useCartOpenSelector,
  useCartTotalPriceSelector,
  useSetCartItemsDispatch,
  useSetCartOpenDispatch,
} from "./useSelectors";
export type { TContext, TCartItem } from "./types";
```

---

## AI Agent Checklist

When generating Context Pattern, ensure you:

- **Create all 4 files:** `Context.tsx`, `types.ts`, `useContext.ts`, `useSelectors.ts`
- Use `useRef` for state storage (NOT `useState`)
- Use `useRef<Set<TSubscriberCallback>>` for subscribers
- Wrap all functions in `useCallback` with empty dependency array
- **Create getter for each state:** `get{StateName}`
- **Create setter for each state:** `set{StateName}`
- **Setters must notify all subscribers:** `subscribers.current.forEach((callback) => callback())`
- Subscribe function must return unsubscribe cleanup function
- Custom hook throws error when context is null
- Selectors use `useSyncExternalStore(subscribe, getter, getter)`
- Dispatchers return setter functions directly
- Follow naming conventions for all hooks and types
- Export everything from `index.ts`
- Add TypeScript types for all functions and variables

---

## useSyncExternalStore API Reference

```
const state = useSyncExternalStore(
  subscribe,      // (callback) => unsubscribe function
  getSnapshot,    // () => current state (client)
  getServerSnapshot // () => current state (server/SSR) - optional
);
```

### Parameters

- **subscribe**: This is a function to watch the store. When the data changes, it calls a "callback". It also returns a function to stop watching.
- **getSnapshot:** This is a function to get the current data from the store. Use this to see the state right now.
- **getServerSnapshot:** This is an optional function for SSR (Server-Side Rendering). Usually, you can use the same function as getSnapshot.
