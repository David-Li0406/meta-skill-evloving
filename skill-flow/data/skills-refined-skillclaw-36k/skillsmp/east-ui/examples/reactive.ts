/**
 * Reactive TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the reactive module (Reactive components).
 *
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., Reactive.Root)
 */

import { East, IntegerType, NullType, some } from "@elaraai/east";
import { Reactive, State, Text, Button, Stack, UIComponentType } from "../src/index.js";

// ============================================================================
// REACTIVE
// ============================================================================

// File: src/reactive/index.ts
// Export: createReactive (private function)
// A simple counter that reads and displays state
const reactiveExample = East.function([], UIComponentType, $ => {
    // This component re-renders only when "counter" changes
    return Reactive.Root($ => {
        const count = $.let(State.readTyped("counter", IntegerType)());
        const value = $.let(0n);
        $.match(count, {
            some: ($, v) => $.assign(value, v),
        });
        return Text.Root(East.str`Count: ${value}`);
    });
});
reactiveExample.toIR().compile(State.Implementation)();

// File: src/reactive/index.ts
// Export: Reactive.Root (interactive example with callback)
// A counter with a button that increments state via onClick callback
const reactiveInteractiveExample = East.function([], UIComponentType, $ => {
    // Initialize state
    $(State.initTyped("reactive_counter", 0n, IntegerType)());

    return Stack.VStack([
        // This re-renders only when "reactive_counter" changes
        Reactive.Root($ => {
            const count = $.let(State.readTyped("reactive_counter", IntegerType)());
            const value = $.let(0n);
            $.match(count, {
                some: ($, v) => $.assign(value, v),
            });
            return Text.Root(East.str`Count: ${value}`);
        }),

        // Button that increments counter via onClick
        Button.Root("Increment", {
            onClick: East.function([], NullType, $ => {
                const current = $.let(State.readTyped("reactive_counter", IntegerType)());
                const value = $.let(0n);
                $.match(current, {
                    some: ($, v) => $.assign(value, v),
                });
                $(State.writeTyped("reactive_counter", some(value.add(1n)), IntegerType)());
            })
        }),
    ], { gap: "3" });
});
reactiveInteractiveExample.toIR().compile(State.Implementation)();

console.log("Reactive TypeDoc examples compiled and executed successfully!");
