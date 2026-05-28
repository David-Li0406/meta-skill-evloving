/**
 * Platform TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the platform module (State).
 *
 * Each example is compiled AND executed to verify correctness.
 * Since store is global, we verify state persists across function calls.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., State.read, State.write)
 */

import { East, IntegerType, NullType, some, none } from "@elaraai/east";
import { State, UIComponentType, Button, Text } from "../src/index.js";
import { encodeBeast2For, decodeBeast2For } from "@elaraai/east/internal";

// Helper to read current counter value from store
function getCounterValue(): bigint {
    const blob = State.store.read("counter");
    if (blob === undefined) return 0n;
    return decodeBeast2For(IntegerType)(blob) as bigint;
}

// Helper to assert counter value
function assertCounter(expected: bigint, message: string): void {
    const actual = getCounterValue();
    if (actual !== expected) {
        throw new Error(`${message}: expected ${expected}, got ${actual}`);
    }
    console.log(`  ✓ ${message}: ${actual}`);
}

// ============================================================================
// STATE
// ============================================================================

console.log("\n=== State Management Examples ===\n");

// File: src/platform/index.ts
// Export: State.write
console.log("Testing State.write...");
const stateWriteExample = East.function([], NullType, $ => {
    const blob = East.Blob.encodeBeast(East.value(42n), "v2");
    $(State.write("counter", some(blob)));
});
const writeCompiled = stateWriteExample.toIR().compile(State.Implementation);

// Write initial value
writeCompiled();
assertCounter(42n, "After first write");

// File: src/platform/index.ts
// Export: State.read
console.log("\nTesting State.read...");
const stateReadExample = East.function([], IntegerType, $ => {
    const count = $.let(0n);
    $.match($(State.read("counter")), {
        some: ($, v) => $.assign(count, v.decodeBeast(IntegerType, "v2")),
    });
    return count;
});
const readCompiled = stateReadExample.toIR().compile(State.Implementation);

// Read should return current value
const readResult = readCompiled();
if (readResult !== 42n) {
    throw new Error(`State.read returned ${readResult}, expected 42n`);
}
console.log(`  ✓ Read returned: ${readResult}`);

// File: src/platform/index.ts
// Export: State (namespace example) - increment counter
console.log("\nTesting State namespace (counter increment)...");
const incrementExample = East.function([], NullType, $ => {
    const count = $.let(0n);
    $.match($(State.read("counter")), {
        some: ($, v) => $.assign(count, v.decodeBeast(IntegerType, "v2")),
    });
    const newBlob = East.Blob.encodeBeast(count.add(1n), "v2");
    $(State.write("counter", some(newBlob)));
});
const incrementCompiled = incrementExample.toIR().compile(State.Implementation);

// Increment multiple times and verify
incrementCompiled();
assertCounter(43n, "After first increment");

incrementCompiled();
assertCounter(44n, "After second increment");

incrementCompiled();
assertCounter(45n, "After third increment");

// File: src/platform/index.ts
// Export: State with UIComponentType (full counter component)
console.log("\nTesting full counter component...");
const stateNamespaceExample = East.function([], UIComponentType, $ => {
    const count = $.let(0n);
    $.match($(State.read("counter")), {
        some: ($, v) => $.assign(count, v.decodeBeast(IntegerType, "v2")),
    });

    return Button.Root(East.str`Count: ${count}`, {
        onClick: East.function([], NullType, $ => {
            const count = $.let(0n);
            $.match($(State.read("counter")), {
                some: ($, v) => $.assign(count, v.decodeBeast(IntegerType, "v2")),
            });
            const newBlob = East.Blob.encodeBeast(count.add(1n), "v2");
            $(State.write("counter", some(newBlob)));
        })
    });
});
const counterCompiled = stateNamespaceExample.toIR().compile(State.Implementation);

// Render component (doesn't change state, just reads it)
const ui = counterCompiled();
assertCounter(45n, "After rendering component (no change)");
console.log(`  ✓ Component rendered successfully`);

// File: src/platform/index.ts
// Export: State.Implementation
console.log("\nTesting State.Implementation...");
const stateImplementationExample = East.function([], NullType, $ => {
    // Use State.read and State.write here
});
stateImplementationExample.toIR().compile(State.Implementation)();
console.log("  ✓ Empty function compiled and executed");

// Reset counter for clean state
console.log("\nResetting counter...");
const resetExample = East.function([], NullType, $ => {
    const blob = East.Blob.encodeBeast(East.value(0n), "v2");
    $(State.write("counter", some(blob)));
});
resetExample.toIR().compile(State.Implementation)();
assertCounter(0n, "After reset");

// Run increment 5 times to verify accumulation
console.log("\nRunning 5 increments...");
for (let i = 1n; i <= 5n; i++) {
    incrementCompiled();
    assertCounter(i, `After increment ${i}`);
}

// ============================================================================
// STATE.READTYPED
// ============================================================================

// File: src/platform/index.ts
// Export: State.readTyped
console.log("\nTesting State.readTyped...");
const stateReadTypedExample = East.function([], UIComponentType, $ => {
    // Read typed value - returns Option<Integer>
    const count = $(State.readTyped("counter", IntegerType)());

    // Unwrap with default if not set
    const value = $.let(0n);
    $.match(count, {
        some: ($, v) => $.assign(value, v),
    });
    return Text.Root(East.str`Count: ${value}`);
});
stateReadTypedExample.toIR().compile(State.Implementation)();
console.log("  ✓ State.readTyped example compiled and executed");

// ============================================================================
// STATE.WRITETYPED
// ============================================================================

// File: src/platform/index.ts
// Export: State.writeTyped
console.log("\nTesting State.writeTyped...");
const stateWriteTypedExample = East.function([], NullType, $ => {
    // Write a typed value
    $(State.writeTyped("counter", some(42n), IntegerType)());

    // Delete the key
    $(State.writeTyped("counter", none, IntegerType)());
});
stateWriteTypedExample.toIR().compile(State.Implementation)();
console.log("  ✓ State.writeTyped example compiled and executed");

// ============================================================================
// STATE.HAS
// ============================================================================

// File: src/platform/index.ts
// Export: State.has
console.log("\nTesting State.has...");
const stateHasExample = East.function([], NullType, $ => {
    $.if($(State.has("counter")), $ => {
        // Key exists, do something
    });
});
stateHasExample.toIR().compile(State.Implementation)();
console.log("  ✓ State.has example compiled and executed");

// ============================================================================
// STATE.INITTYPED
// ============================================================================

// File: src/platform/index.ts
// Export: State.initTyped
console.log("\nTesting State.initTyped...");
const stateInitTypedExample = East.function([], UIComponentType, $ => {
    // Initialize to 0 only if not already set (safe for re-renders)
    $(State.initTyped("counter", 0n, IntegerType)());

    // Read and display
    const count = $(State.readTyped("counter", IntegerType)());
    const value = $.let(0n);
    $.match(count, {
        some: ($, v) => $.assign(value, v),
    });
    return Text.Root(East.str`Count: ${value}`);
});
stateInitTypedExample.toIR().compile(State.Implementation)();
console.log("  ✓ State.initTyped example compiled and executed");

console.log("\n=== Platform TypeDoc examples compiled and executed successfully! ===\n");
