# Platform Functions Refactor Design

## Executive Summary

This document proposes a refactoring of the platform functions across `@elaraai/east-ui` and `@elaraai/east-ui-components` to achieve cleaner separation between **definitions** and **implementations**.

**Key Principle**: `@elaraai/east-ui` should contain only:
1. Platform function **signatures** (created with `East.platform()`)
2. The `State` namespace that groups these signatures

All runtime implementations (store classes, `StateImpl`, typed helpers, tracking, singleton) belong in `@elaraai/east-ui-components`.

---

## Current Architecture Analysis

### What's in east-ui/platform/state.ts (332 lines)

| Code | Type | Should Be In |
|------|------|--------------|
| `state_read = East.platform(...)` | **Definition** | east-ui ✓ |
| `state_write = East.platform(...)` | **Definition** | east-ui ✓ |
| `state_has = East.platform(...)` | **Definition** | east-ui ✓ |
| `store = new UIStore()` | Implementation | east-ui-components |
| `StateImpl = [...]` | Implementation | east-ui-components |
| `state_read_typed()` | Implementation | east-ui-components |
| `state_write_typed()` | Implementation | east-ui-components |
| `state_init_typed()` | Implementation | east-ui-components |
| `enableTracking()` | Implementation | east-ui-components |
| `disableTracking()` | Implementation | east-ui-components |
| `isTracking()` | Implementation | east-ui-components |
| `trackKey()` | Implementation | east-ui-components |

### What's in east-ui/platform/store.ts (340 lines)

| Code | Type | Should Be In |
|------|------|--------------|
| `UIStoreInterface` | **Definition** | east-ui-components* |
| `UIStoreOptions` | **Definition** | east-ui-components* |
| `UIStore` class | Implementation | east-ui-components |
| `createUIStore()` | Implementation | east-ui-components |

*Note: Types can move to east-ui-components since there's no use case for implementing `UIStoreInterface` outside of that package.

### What's in east-ui/platform/index.ts (73 lines)

| Code | Type | Notes |
|------|------|-------|
| `State` namespace | **Definition** | Keep in east-ui, but remove implementation properties |

### Current State Namespace

```typescript
export const State = {
    read: state_read,           // ✓ Definition (platform function)
    write: state_write,         // ✓ Definition (platform function)
    has: state_has,             // ✓ Definition (platform function)
    Implementation: StateImpl,  // ✗ Implementation - move out
    store: store,               // ✗ Implementation - move out
    readTyped: state_read_typed,   // ✗ Implementation - move out
    writeTyped: state_write_typed, // ✗ Implementation - move out
    initTyped: state_init_typed,   // ✗ Implementation - move out
} as const;
```

---

## Proposed Architecture

### east-ui Package (Definitions Only)

**platform/state.ts** (~50 lines)

```typescript
/**
 * State management platform function signatures.
 *
 * @remarks
 * This module contains only platform function definitions created with `East.platform()`.
 * All runtime implementations are in `@elaraai/east-ui-components`.
 */

import { East, StringType, BlobType, NullType, BooleanType } from "@elaraai/east";
import { OptionType } from "@elaraai/east/internal";

/**
 * Reads a Beast2-encoded value from state storage.
 *
 * @param key - The state key to read from
 * @returns Option of Beast2-encoded blob (some if exists, none if not found)
 *
 * @remarks
 * Returns `none` if the key does not exist, `some(blob)` if it does.
 * Implementation provided by `StateImpl` in `@elaraai/east-ui-components`.
 */
export const state_read = East.platform("state_read", [StringType], OptionType(BlobType));

/**
 * Writes a Beast2-encoded value to state storage.
 *
 * @param key - The state key to write to
 * @param value - The value to write (some to set, none to delete)
 * @returns Null
 *
 * @remarks
 * Pass `none` to delete the key from state.
 * Implementation provided by `StateImpl` in `@elaraai/east-ui-components`.
 */
export const state_write = East.platform("state_write", [StringType, OptionType(BlobType)], NullType);

/**
 * Checks if a key exists in state storage.
 *
 * @param key - The state key to check
 * @returns Boolean indicating whether the key exists
 *
 * @remarks
 * Implementation provided by `StateImpl` in `@elaraai/east-ui-components`.
 */
export const state_has = East.platform("state_has", [StringType], BooleanType);
```

**platform/index.ts** (~40 lines)

```typescript
export { state_read, state_write, state_has } from "./state.js";

import { state_read, state_write, state_has } from "./state.js";

/**
 * State management platform functions for East UI.
 *
 * @remarks
 * Contains platform function signatures only. For implementations,
 * typed helpers, and store access, import from `@elaraai/east-ui-components`.
 *
 * @example
 * ```ts
 * import { East, NullType } from "@elaraai/east";
 * import { State } from "@elaraai/east-ui";
 * import { StateRuntime } from "@elaraai/east-ui-components";
 *
 * const fn = East.function([], NullType, $ => {
 *     $(State.read("key"));
 * });
 *
 * const compiled = fn.toIR().compile(StateRuntime.Implementation);
 * ```
 */
export const State = {
    /**
     * Reads a Beast2-encoded blob from state storage.
     * Returns `none` if key not found, `some(blob)` if found.
     */
    read: state_read,
    /**
     * Writes a Beast2-encoded blob to state storage.
     * Pass `none` as value to delete the key.
     */
    write: state_write,
    /**
     * Checks if a key exists in state storage.
     * Returns boolean indicating existence.
     */
    has: state_has,
} as const;
```

### east-ui-components Package (All Implementations)

**platform/store.ts** (~550 lines - consolidated)

```typescript
/**
 * Store implementations for East UI state management.
 */

// ============================================================================
// Store Interface (moved from east-ui)
// ============================================================================

export interface UIStoreInterface {
    read(key: string): Uint8Array | undefined;
    write(key: string, value: Uint8Array | undefined): void;
    has(key: string): boolean;
    subscribe(callback: () => void): () => void;
    subscribe(key: string, callback: () => void): () => void;
    batch<T>(fn: () => T): T;
    markActive(key: string): void;
    beginRender(): void;
    endRender(): void;
    getSnapshot(): number;
    getState(): Map<string, Uint8Array>;
    setScheduler(scheduler: ((notify: () => void) => void) | undefined): void;
    getKeyVersion(key: string): number;
    getActiveKeys?(): Set<string>;
    gc?(): string[];
}

export interface UIStoreOptions {
    gcIntervalMs?: number;
    enableGc?: boolean;
}

// ============================================================================
// In-Memory Store (moved from east-ui)
// ============================================================================

export class UIStore implements UIStoreInterface {
    // ... full implementation (340 lines)
}

export function createUIStore(
    initialState?: Record<string, Uint8Array>,
    options?: UIStoreOptions
): UIStore {
    return new UIStore(initialState, options);
}

// ============================================================================
// Persistent Store (existing)
// ============================================================================

export class PersistentUIStore implements UIStoreInterface {
    // ... existing implementation (200 lines)
}

export function createPersistentUIStore(...): PersistentUIStore {
    // ...
}
```

**platform/state-runtime.ts** (~350 lines - new file)

```typescript
/**
 * Runtime implementations for State platform functions.
 */

import { East, type EastType, type SubtypeExprOrValue, type CallableFunctionExpr, StringType, NullType, some, none } from "@elaraai/east";
import { type PlatformFunction, OptionType } from "@elaraai/east/internal";
import { state_read, state_write, state_has } from "@elaraai/east-ui";
import { UIStore, type UIStoreInterface } from "./store.js";

// ============================================================================
// Singleton Store
// ============================================================================

let _store: UIStoreInterface | null = null;

/**
 * Returns the singleton store instance used by State platform functions.
 *
 * @returns The current `UIStoreInterface` instance
 *
 * @remarks
 * Auto-creates a default `UIStore` if none has been initialized.
 * Call `initializeStore()` before this to use a custom store implementation.
 */
export function getStore(): UIStoreInterface {
    if (!_store) {
        // Auto-create default store for convenience
        _store = new UIStore();
    }
    return _store;
}

/**
 * Initializes or replaces the singleton store used by State platform functions.
 *
 * @param store - The store instance to use for all State operations
 *
 * @remarks
 * Call this before any State operations to use a custom store implementation
 * such as `PersistentUIStore` or a custom `UIStoreInterface` implementation.
 */
export function initializeStore(store: UIStoreInterface): void {
    _store = store;
}

// ============================================================================
// Reactive Dependency Tracking (internal)
// ============================================================================

let trackingContext: Set<string> | null = null;

/** @internal */
export function enableTracking(): Set<string> {
    trackingContext = new Set();
    return trackingContext;
}

/** @internal */
export function disableTracking(): string[] {
    const keys = trackingContext ? [...trackingContext] : [];
    trackingContext = null;
    return keys;
}

/** @internal */
export function isTracking(): boolean {
    return trackingContext !== null;
}

/** @internal */
export function trackKey(key: string): void {
    if (trackingContext) {
        trackingContext.add(key);
    }
}

// ============================================================================
// Platform Implementation
// ============================================================================

/**
 * Platform function implementations for State operations.
 *
 * @remarks
 * Pass this array to `ir.compile()` to enable `State.read`, `State.write`, and `State.has`
 * platform functions. The implementations use the singleton store from `getStore()`.
 *
 * @example
 * ```ts
 * import { State } from "@elaraai/east-ui";
 * import { StateImpl } from "@elaraai/east-ui-components";
 *
 * const fn = East.function([], BooleanType, $ => State.has("myKey"));
 * const compiled = fn.toIR().compile(StateImpl);
 * const exists = compiled(); // false (key doesn't exist yet)
 * ```
 */
export const StateImpl: PlatformFunction[] = [
    state_write.implement((key, value) => {
        if (value.type === 'none') {
            getStore().write(key, undefined);
        } else {
            getStore().write(key, value.value);
        }
    }),
    state_read.implement((key) => {
        trackKey(key);
        const ret = getStore().read(key);
        return ret === undefined ? none : some(ret);
    }),
    state_has.implement((key) => {
        return getStore().has(key);
    }),
];

// ============================================================================
// Typed Helpers
// ============================================================================

/**
 * Creates a typed state read function for a specific key and East type.
 *
 * @typeParam T - The East type of the stored value
 * @param key - The state key to read from
 * @param type - The East type for deserialization
 * @returns A callable East function that reads and deserializes the value
 *
 * @remarks
 * The returned function handles Beast2 deserialization automatically.
 * Returns `none` if key doesn't exist, `some(value)` if it does.
 */
export const state_read_typed = <T extends EastType>(
    key: SubtypeExprOrValue<StringType>,
    type: T
): CallableFunctionExpr<[], OptionType<T>> => {
    // ... implementation
};

/**
 * Creates a typed state write function for a specific key and East type.
 *
 * @typeParam T - The East type of the value to store
 * @param key - The state key to write to
 * @param value - The value to write (some to set, none to delete)
 * @param type - The East type for serialization
 * @returns A callable East function that serializes and writes the value
 *
 * @remarks
 * The returned function handles Beast2 serialization automatically.
 * Pass `none` to delete the key from state.
 */
export const state_write_typed = <T extends EastType>(
    key: SubtypeExprOrValue<StringType>,
    value: SubtypeExprOrValue<OptionType<T>>,
    type: T
): CallableFunctionExpr<[], NullType> => {
    // ... implementation
};

/**
 * Creates a typed state initialization function that only writes if key doesn't exist.
 *
 * @typeParam T - The East type of the default value
 * @param key - The state key to initialize
 * @param value - The default value to write if key doesn't exist
 * @param type - The East type for serialization
 * @returns A callable East function that conditionally initializes the value
 *
 * @remarks
 * Useful for setting default values on first access without overwriting existing data.
 * The returned function handles Beast2 serialization automatically.
 */
export const state_init_typed = <T extends EastType>(
    key: SubtypeExprOrValue<StringType>,
    value: SubtypeExprOrValue<T>,
    type: T
): CallableFunctionExpr<[], NullType> => {
    // ... implementation
};
```

**platform/index.ts** (~80 lines)

```typescript
// Re-export platform function signatures from east-ui
export { State, state_read, state_write, state_has } from "@elaraai/east-ui";

// Export store implementations
export {
    UIStore,
    createUIStore,
    PersistentUIStore,
    createPersistentUIStore,
    type UIStoreInterface,
    type UIStoreOptions,
} from "./store.js";

// Export state runtime
export {
    StateImpl,
    getStore,
    initializeStore,
    state_read_typed,
    state_write_typed,
    state_init_typed,
} from "./state-runtime.js";

// Internal exports (for hooks.tsx, not public API)
export { enableTracking, disableTracking, isTracking, trackKey } from "./state-runtime.js";

// Export React hooks
export { ... } from "./hooks.js";

import { StateImpl, getStore, initializeStore, state_read_typed, state_write_typed, state_init_typed } from "./state-runtime.js";

/**
 * Runtime implementations for State platform functions.
 *
 * @remarks
 * Provides platform implementations, store access, and typed helper functions.
 * Use `StateRuntime.Implementation` with `ir.compile()` to enable State operations.
 *
 * @example
 * ```ts
 * import { East, NullType } from "@elaraai/east";
 * import { State } from "@elaraai/east-ui";
 * import { StateRuntime } from "@elaraai/east-ui-components";
 *
 * const fn = East.function([], NullType, $ => {
 *     $(State.write("counter", some(serialize(42n))));
 * });
 *
 * const compiled = fn.toIR().compile(StateRuntime.Implementation);
 * compiled();
 * ```
 */
export const StateRuntime = {
    /**
     * Platform function implementations for State operations.
     * Pass to `ir.compile()` to enable `State.read`, `State.write`, and `State.has`.
     */
    Implementation: StateImpl,
    /**
     * Returns the singleton store instance.
     * Auto-creates a default `UIStore` if none has been initialized.
     */
    getStore,
    /**
     * Initializes or replaces the singleton store instance.
     * Call before any State operations to use a custom store implementation.
     */
    initializeStore,
    /**
     * Creates a typed state read function for a specific key and type.
     * Handles Beast2 serialization/deserialization automatically.
     */
    readTyped: state_read_typed,
    /**
     * Creates a typed state write function for a specific key and type.
     * Handles Beast2 serialization automatically.
     */
    writeTyped: state_write_typed,
    /**
     * Creates a typed state initialization function that only writes if key doesn't exist.
     * Useful for setting default values on first access.
     */
    initTyped: state_init_typed,
} as const;
```

---

## API Changes

### Before (current)

```typescript
import { State } from "@elaraai/east-ui";

// Platform function signatures
State.read("key");
State.write("key", someBlob);
State.has("key");

// Implementation (shouldn't be here)
State.Implementation  // PlatformFunction[]
State.store           // UIStore singleton
State.readTyped(...)  // Typed helper
State.writeTyped(...) // Typed helper
State.initTyped(...)  // Typed helper
```

### After (proposed)

```typescript
// Signatures from east-ui
import { State } from "@elaraai/east-ui";

State.read("key");
State.write("key", someBlob);
State.has("key");

// Implementations from east-ui-components
import { StateRuntime } from "@elaraai/east-ui-components";

StateRuntime.Implementation  // PlatformFunction[]
StateRuntime.getStore()      // UIStore singleton
StateRuntime.readTyped(...)  // Typed helper
StateRuntime.writeTyped(...) // Typed helper
StateRuntime.initTyped(...)  // Typed helper
```

Or import directly:

```typescript
import { State } from "@elaraai/east-ui";
import { StateImpl, getStore, state_read_typed } from "@elaraai/east-ui-components";

const fn = East.function([], UIComponentType, $ => {
    $(State.read("key"));
});

const compiled = fn.toIR().compile(StateImpl);
```

---

## File Changes Summary

### east-ui Package

| File | Action | Before | After |
|------|--------|--------|-------|
| `platform/store.ts` | DELETE | 340 lines | 0 |
| `platform/state.ts` | REDUCE | 332 lines | ~50 lines |
| `platform/index.ts` | REDUCE | 73 lines | ~40 lines |
| **Total** | | **745 lines** | **~90 lines** |

**Net reduction: ~655 lines (88%)**

### east-ui-components Package

| File | Action | Before | After |
|------|--------|--------|-------|
| `platform/store.ts` | EXPAND | 219 lines | ~550 lines |
| `platform/state-runtime.ts` | CREATE | 0 | ~350 lines |
| `platform/hooks.tsx` | UPDATE | 387 lines | ~350 lines |
| `platform/index.ts` | UPDATE | 57 lines | ~80 lines |
| **Total** | | **663 lines** | **~1330 lines** |

---

## Implementation Checklist

### Phase 1: Prepare east-ui-components
- [ ] Create `platform/state-runtime.ts` with all implementation code
- [ ] Move `UIStore` class and `createUIStore` to `platform/store.ts`
- [ ] Move `UIStoreInterface` and `UIStoreOptions` to `platform/store.ts`
- [ ] Update `platform/hooks.tsx` to import from local files
- [ ] Update `platform/index.ts` exports

### Phase 2: Simplify east-ui
- [ ] Reduce `platform/state.ts` to signatures only
- [ ] Delete `platform/store.ts`
- [ ] Reduce `platform/index.ts` to re-export signatures only
- [ ] Update `src/index.ts` exports

### Phase 3: Fix Side Effect
- [ ] Remove `State.store.setScheduler()` from module scope in hooks.tsx
- [ ] Add scheduler configuration to `UIStoreProvider`

### Phase 4: Update Exports
- [ ] Add `StateRuntime` namespace to east-ui-components
- [ ] Update all re-exports
- [ ] Ensure backwards compatibility where possible

### Phase 5: Testing & Migration
- [ ] Update tests to use new import paths
- [ ] Update examples to use new patterns
- [ ] Update documentation

---

## Questions for Review

1. **Backwards compatibility**: Should east-ui-components re-export a `State` object that includes both signatures AND implementations for easier migration?

2. **Store auto-creation**: Should `getStore()` auto-create a default `UIStore` if none is initialized, or throw an error?

3. **Naming**: Is `StateRuntime` a good name, or should it be `StateImpl` / `StateStore` / something else?
