/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { East, type ExprType, variant, type CallableFunctionExpr } from "@elaraai/east";

import { UIComponentType } from "../component.js";

// ============================================================================
// Reactive Component Builder
// ============================================================================

/**
 * Creates a reactive component that re-renders independently when its dependencies change.
 *
 * @param body - Function body that returns UIComponentType. Must be a free function with no captures.
 * @returns A ReactiveComponent variant of UIComponentType
 *
 * @remarks
 * The body function MUST be a free function - no captures from parent East scope.
 * This is validated at IR creation time. Dependencies are automatically detected
 * at runtime by tracking which state keys are read during execution.
 *
 * **What IS allowed:**
 * - Platform functions (State.readTyped, State.writeTyped, etc.)
 * - Module-level constants and functions (not captures)
 * - Callbacks defined inside the body (East.function)
 *
 * **What is NOT allowed:**
 * - Parent East function scope variables ($.let, parameters, state reads)
 * - Any variable captured from enclosing East function scope
 *
 * @throws Error if the body captures variables from parent scope
 *
 * @example
 * ```ts
 * import { East, IntegerType } from "@elaraai/east";
 * import { Reactive, State, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const app = East.function([], UIComponentType, $ => {
 *     // This component re-renders only when "counter" changes
 *     return Reactive.Root($ => {
 *         const count = $.let(State.readTyped("counter", IntegerType)());
 *         const value = $.let(0n);
 *         $.match(count, {
 *             some: ($, v) => $.assign(value, v),
 *         });
 *         return Text.Root(East.str`Count: ${value}`);
 *     });
 * });
 * ```
 */
function createReactive(
    body: CallableFunctionExpr<[], typeof UIComponentType>,
): ExprType<typeof UIComponentType> {
    // Get the IR and validate no captures from parent scope
    // Return the ReactiveComponent variant
    return East.value(variant("ReactiveComponent", {
        render: body
    }), UIComponentType);
}

/**
 * Reactive component for selective re-rendering.
 *
 * @remarks
 * Use `Reactive.Root(body)` to create a reactive component that re-renders
 * independently when its state dependencies change. Dependencies are automatically
 * detected at runtime. The body function must be a free function with no captures
 * from parent East scope.
 */
export const Reactive = {
    /**
     * Creates a reactive component that re-renders independently.
     *
     * @param body - Function body returning UIComponentType. Must be a free function.
     * @returns A ReactiveComponent variant
     *
     * @see {@link createReactive} for full documentation and examples
     */
    Root: createReactive,
} as const;
