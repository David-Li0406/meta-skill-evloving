/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { East, ArrayType, IntegerType, StringType, NullType, SetType, DictType, StructType, VariantType, variant, FloatType, BooleanType, DateTimeType, SortedSet, RefType, ref, RecursiveType } from "../src/index.js";
import type { ValueTypeOf } from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";
import { generateFuzzTestCases } from "../src/patch/fuzz.js";

// =============================================================================
// Primitive Type Tests
// =============================================================================

await describe("Patch - Primitives", (test) => {
    // Null
    test("Null: identical", $ => {
        const before = $.const(null, NullType);
        const after = $.const(null, NullType);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "unchanged"));
    });

    // Boolean
    test("Boolean: identical true", $ => {
        const before = $.const(true);
        const after = $.const(true);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "unchanged"));
    });

    test("Boolean: changed true to false", $ => {
        const before = $.const(true);
        const after = $.const(false);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "replace"));
        $(assert.equal(patch.unwrap("replace").before, true));
        $(assert.equal(patch.unwrap("replace").after, false));
    });

    test("Boolean: changed false to true", $ => {
        const before = $.const(false);
        const after = $.const(true);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "replace"));
        $(assert.equal(patch.unwrap("replace").before, false));
        $(assert.equal(patch.unwrap("replace").after, true));
    });

    // Integer
    test("Integer: identical", $ => {
        const before = $.const(42n);
        const after = $.const(42n);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "unchanged"));
    });

    test("Integer: changed", $ => {
        const before = $.const(0n);
        const after = $.const(100n);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "replace"));
        $(assert.equal(patch.unwrap("replace").before, 0n));
        $(assert.equal(patch.unwrap("replace").after, 100n));
    });

    // Float
    test("Float: identical", $ => {
        const before = $.const(3.14);
        const after = $.const(3.14);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "unchanged"));
    });

    test("Float: changed", $ => {
        const before = $.const(1.0);
        const after = $.const(2.0);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "replace"));
        $(assert.equal(patch.unwrap("replace").before, 1.0));
        $(assert.equal(patch.unwrap("replace").after, 2.0));
    });

    test("Float: NaN to NaN is unchanged", $ => {
        const before = $.const(NaN);
        const after = $.const(NaN);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "unchanged"));
    });

    test("Float: Infinity to -Infinity", $ => {
        const before = $.const(Infinity);
        const after = $.const(-Infinity);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "replace"));
        $(assert.equal(patch.unwrap("replace").before, Infinity));
        $(assert.equal(patch.unwrap("replace").after, -Infinity));
    });

    // String
    test("String: identical", $ => {
        const before = $.const("hello");
        const after = $.const("hello");
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "unchanged"));
    });

    test("String: changed", $ => {
        const before = $.const("hello");
        const after = $.const("world");
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "replace"));
        $(assert.equal(patch.unwrap("replace").before, "hello"));
        $(assert.equal(patch.unwrap("replace").after, "world"));
    });

    test("String: empty to non-empty", $ => {
        const before = $.const("");
        const after = $.const("x");
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "replace"));
        $(assert.equal(patch.unwrap("replace").before, ""));
        $(assert.equal(patch.unwrap("replace").after, "x"));
    });
});

// =============================================================================
// Apply/Invert Round-trip Tests
// =============================================================================

await describe("Patch - Round-trips", (test) => {
    test("Integer: apply unchanged preserves value", $ => {
        const value = $.const(42n);
        const patch = $.const(East.diff(value, value));
        const result = $.const(East.applyPatch(value, patch));
        $(assert.equal(result, 42n));
    });

    test("Integer: apply replace changes value", $ => {
        const before = $.const(42n);
        const after = $.const(100n);
        const patch = $.const(East.diff(before, after));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result, 100n));
    });

    test("Integer: invert swaps before/after", $ => {
        const before = $.const(42n);
        const after = $.const(100n);
        const patch = $.const(East.diff(before, after));
        const inverted = $.const(East.invertPatch(patch, IntegerType));
        $(assert.equal(inverted.getTag(), "replace"));
        $(assert.equal(inverted.unwrap("replace").before, 100n));
        $(assert.equal(inverted.unwrap("replace").after, 42n));
    });

    test("Integer: apply inverted restores original", $ => {
        const before = $.const(42n);
        const after = $.const(100n);
        const patch = $.const(East.diff(before, after));
        const inverted = $.const(East.invertPatch(patch, IntegerType));
        const restored = $.const(East.applyPatch(after, inverted));
        $(assert.equal(restored, 42n));
    });

    test("String: full round-trip", $ => {
        const before = $.const("hello");
        const after = $.const("world");
        const patch = $.const(East.diff(before, after));
        // Apply forward
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result, "world"));
        // Invert and apply backward
        const inverted = $.const(East.invertPatch(patch, StringType));
        const restored = $.const(East.applyPatch(after, inverted));
        $(assert.equal(restored, "hello"));
    });
});

// =============================================================================
// Array Tests
// =============================================================================

await describe("Patch - Arrays", (test) => {
    test("Array: identical empty is unchanged", $ => {
        const arr = $.const([], ArrayType(IntegerType));
        const patch = $.const(East.diff(arr, arr));
        $(assert.equal(patch.getTag(), "unchanged"));
    });

    test("Array: identical non-empty is unchanged", $ => {
        const arr = $.const([1n, 2n, 3n]);
        const patch = $.const(East.diff(arr, arr));
        $(assert.equal(patch.getTag(), "unchanged"));
    });

    test("Array: empty to single element - insert operation", $ => {
        const before = $.const([], ArrayType(IntegerType));
        const after = $.const([42n]);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        // Verify patch has one insert operation
        const ops = $.const(patch.unwrap("patch"));
        $(assert.equal(ops.length(), 1n));
        $(assert.equal(ops.get(0n).operation.getTag(), "insert"));
        $(assert.equal(ops.get(0n).operation.unwrap("insert"), 42n));
    });

    test("Array: single element to empty - delete operation", $ => {
        const before = $.const([42n]);
        const after = $.const([], ArrayType(IntegerType));
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const ops = $.const(patch.unwrap("patch"));
        $(assert.equal(ops.length(), 1n));
        $(assert.equal(ops.get(0n).operation.getTag(), "delete"));
        $(assert.equal(ops.get(0n).operation.unwrap("delete"), 42n));
    });

    test("Array: update single element", $ => {
        const before = $.const([1n, 2n, 3n]);
        const after = $.const([1n, 99n, 3n]);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        // Apply and verify
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.get(0n), 1n));
        $(assert.equal(result.get(1n), 99n));
        $(assert.equal(result.get(2n), 3n));
    });

    test("Array: insert at start", $ => {
        const before = $.const([2n, 3n]);
        const after = $.const([1n, 2n, 3n]);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 3n));
        $(assert.equal(result.get(0n), 1n));
        $(assert.equal(result.get(1n), 2n));
        $(assert.equal(result.get(2n), 3n));
    });

    test("Array: insert at end", $ => {
        const before = $.const([1n, 2n]);
        const after = $.const([1n, 2n, 3n]);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 3n));
        $(assert.equal(result.get(2n), 3n));
    });

    test("Array: delete from start", $ => {
        const before = $.const([1n, 2n, 3n]);
        const after = $.const([2n, 3n]);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 2n));
        $(assert.equal(result.get(0n), 2n));
        $(assert.equal(result.get(1n), 3n));
    });

    test("Array: delete from end", $ => {
        const before = $.const([1n, 2n, 3n]);
        const after = $.const([1n, 2n]);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 2n));
        $(assert.equal(result.get(0n), 1n));
        $(assert.equal(result.get(1n), 2n));
    });

    test("Array: delete from middle", $ => {
        const before = $.const([1n, 2n, 3n]);
        const after = $.const([1n, 3n]);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 2n));
        $(assert.equal(result.get(0n), 1n));
        $(assert.equal(result.get(1n), 3n));
    });

    test("Array: multiple deletes", $ => {
        const before = $.const([1n, 2n, 3n, 4n, 5n]);
        const after = $.const([1n, 3n, 5n]);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 3n));
        $(assert.equal(result.get(0n), 1n));
        $(assert.equal(result.get(1n), 3n));
        $(assert.equal(result.get(2n), 5n));
    });

    test("Array: multiple inserts", $ => {
        const before = $.const([1n, 3n, 5n]);
        const after = $.const([1n, 2n, 3n, 4n, 5n]);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 5n));
        $(assert.equal(result.get(0n), 1n));
        $(assert.equal(result.get(1n), 2n));
        $(assert.equal(result.get(2n), 3n));
        $(assert.equal(result.get(3n), 4n));
        $(assert.equal(result.get(4n), 5n));
    });

    test("Array: insert multiple at start", $ => {
        const before = $.const([3n]);
        const after = $.const([1n, 2n, 3n]);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 3n));
        $(assert.equal(result.get(0n), 1n));
        $(assert.equal(result.get(1n), 2n));
        $(assert.equal(result.get(2n), 3n));
    });

    test("Array: insert multiple at end", $ => {
        const before = $.const([1n]);
        const after = $.const([1n, 2n, 3n]);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 3n));
        $(assert.equal(result.get(0n), 1n));
        $(assert.equal(result.get(1n), 2n));
        $(assert.equal(result.get(2n), 3n));
    });

    test("Array: replace entire contents", $ => {
        const before = $.const([1n, 2n, 3n]);
        const after = $.const([4n, 5n, 6n]);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 3n));
        $(assert.equal(result.get(0n), 4n));
        $(assert.equal(result.get(1n), 5n));
        $(assert.equal(result.get(2n), 6n));
    });

    test("Array: shrink to empty", $ => {
        const before = $.const([1n, 2n, 3n]);
        const after = $.const([], ArrayType(IntegerType));
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 0n));
    });

    test("Array: grow from empty multiple elements", $ => {
        const before = $.const([], ArrayType(IntegerType));
        const after = $.const([1n, 2n, 3n]);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 3n));
        $(assert.equal(result.get(0n), 1n));
        $(assert.equal(result.get(1n), 2n));
        $(assert.equal(result.get(2n), 3n));
    });

    test("Array: invert insert becomes delete", $ => {
        const before = $.const([1n, 2n]);
        const after = $.const([1n, 2n, 3n]);
        const patch = $.const(East.diff(before, after));
        const inverted = $.const(East.invertPatch(patch, ArrayType(IntegerType)));
        // Apply inverted to get back original
        const restored = $.const(East.applyPatch(after, inverted));
        $(assert.equal(restored.length(), 2n));
        $(assert.equal(restored.get(0n), 1n));
        $(assert.equal(restored.get(1n), 2n));
    });

    test("Array: invert delete becomes insert", $ => {
        const before = $.const([1n, 2n, 3n]);
        const after = $.const([1n, 3n]);
        const patch = $.const(East.diff(before, after));
        const inverted = $.const(East.invertPatch(patch, ArrayType(IntegerType)));
        const restored = $.const(East.applyPatch(after, inverted));
        $(assert.equal(restored.length(), 3n));
        $(assert.equal(restored.get(0n), 1n));
        $(assert.equal(restored.get(1n), 2n));
        $(assert.equal(restored.get(2n), 3n));
    });

    test("Array: invert update preserves element", $ => {
        const before = $.const([1n, 2n, 3n]);
        const after = $.const([1n, 99n, 3n]);
        const patch = $.const(East.diff(before, after));
        const inverted = $.const(East.invertPatch(patch, ArrayType(IntegerType)));
        const restored = $.const(East.applyPatch(after, inverted));
        $(assert.equal(restored.length(), 3n));
        $(assert.equal(restored.get(0n), 1n));
        $(assert.equal(restored.get(1n), 2n));
        $(assert.equal(restored.get(2n), 3n));
    });

    test("Array: invert multiple inserts at start", $ => {
        const before = $.const([3n]);
        const after = $.const([1n, 2n, 3n]);
        const patch = $.const(East.diff(before, after));
        const inverted = $.const(East.invertPatch(patch, ArrayType(IntegerType)));
        const restored = $.const(East.applyPatch(after, inverted));
        $(assert.equal(restored.length(), 1n));
        $(assert.equal(restored.get(0n), 3n));
    });

    test("Array: invert multiple deletes", $ => {
        const before = $.const([1n, 2n, 3n, 4n, 5n]);
        const after = $.const([1n, 3n, 5n]);
        const patch = $.const(East.diff(before, after));
        const inverted = $.const(East.invertPatch(patch, ArrayType(IntegerType)));
        const restored = $.const(East.applyPatch(after, inverted));
        $(assert.equal(restored.length(), 5n));
        $(assert.equal(restored.get(0n), 1n));
        $(assert.equal(restored.get(1n), 2n));
        $(assert.equal(restored.get(2n), 3n));
        $(assert.equal(restored.get(3n), 4n));
        $(assert.equal(restored.get(4n), 5n));
    });

    test("Array: complex change round-trip", $ => {
        const before = $.const([1n, 2n, 3n, 4n]);
        const after = $.const([1n, 99n, 4n, 5n]);
        const patch = $.const(East.diff(before, after));
        // Apply forward
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.get(0n), 1n));
        $(assert.equal(result.get(1n), 99n));
        $(assert.equal(result.get(2n), 4n));
        $(assert.equal(result.get(3n), 5n));
        // Apply inverse
        const inverted = $.const(East.invertPatch(patch, ArrayType(IntegerType)));
        const restored = $.const(East.applyPatch(after, inverted));
        $(assert.equal(restored.get(0n), 1n));
        $(assert.equal(restored.get(1n), 2n));
        $(assert.equal(restored.get(2n), 3n));
        $(assert.equal(restored.get(3n), 4n));
    });

    test("Array: LCS preserves common subsequence", $ => {
        // LCS of [1, 2, 3, 4, 5] and [2, 4, 6] should preserve 2 and 4
        const before = $.const([1n, 2n, 3n, 4n, 5n]);
        const after = $.const([2n, 4n, 6n]);
        const patch = $.const(East.diff(before, after));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 3n));
        $(assert.equal(result.get(0n), 2n));
        $(assert.equal(result.get(1n), 4n));
        $(assert.equal(result.get(2n), 6n));
    });

    test("Array: reverse order round-trip", $ => {
        const before = $.const([1n, 2n, 3n]);
        const after = $.const([3n, 2n, 1n]);
        const patch = $.const(East.diff(before, after));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.get(0n), 3n));
        $(assert.equal(result.get(1n), 2n));
        $(assert.equal(result.get(2n), 1n));
        // Invert
        const inverted = $.const(East.invertPatch(patch, ArrayType(IntegerType)));
        const restored = $.const(East.applyPatch(after, inverted));
        $(assert.equal(restored.get(0n), 1n));
        $(assert.equal(restored.get(1n), 2n));
        $(assert.equal(restored.get(2n), 3n));
    });

    test("Array: string elements", $ => {
        const before = $.const(["a", "b", "c"]);
        const after = $.const(["a", "x", "c", "d"]);
        const patch = $.const(East.diff(before, after));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.length(), 4n));
        $(assert.equal(result.get(0n), "a"));
        $(assert.equal(result.get(1n), "x"));
        $(assert.equal(result.get(2n), "c"));
        $(assert.equal(result.get(3n), "d"));
    });
});

// =============================================================================
// Set Tests
// =============================================================================

await describe("Patch - Sets", (test) => {
    test("Set: identical is unchanged", $ => {
        const s = $.const(new Set([1n, 2n, 3n]), SetType(IntegerType));
        const patch = $.const(East.diff(s, s));
        $(assert.equal(patch.getTag(), "unchanged"));
    });

    test("Set: insert element", $ => {
        const before = $.const(new Set([1n, 2n]), SetType(IntegerType));
        const after = $.const(new Set([1n, 2n, 3n]), SetType(IntegerType));
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        // Verify the patch contains insert for key 3n
        const ops = $.const(patch.unwrap("patch"));
        $(assert.equal(ops.has(3n), true));
        $(assert.equal(ops.get(3n).getTag(), "insert"));
    });

    test("Set: delete element", $ => {
        const before = $.const(new Set([1n, 2n, 3n]), SetType(IntegerType));
        const after = $.const(new Set([1n, 2n]), SetType(IntegerType));
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const ops = $.const(patch.unwrap("patch"));
        $(assert.equal(ops.has(3n), true));
        $(assert.equal(ops.get(3n).getTag(), "delete"));
    });

    test("Set: apply insert", $ => {
        const before = $.const(new Set([1n, 2n]), SetType(IntegerType));
        const after = $.const(new Set([1n, 2n, 3n]), SetType(IntegerType));
        const patch = $.const(East.diff(before, after));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.has(1n), true));
        $(assert.equal(result.has(2n), true));
        $(assert.equal(result.has(3n), true));
        $(assert.equal(result.size(), 3n));
    });

    test("Set: apply delete", $ => {
        const before = $.const(new Set([1n, 2n, 3n]), SetType(IntegerType));
        const after = $.const(new Set([1n, 3n]), SetType(IntegerType));
        const patch = $.const(East.diff(before, after));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.has(1n), true));
        $(assert.equal(result.has(2n), false));
        $(assert.equal(result.has(3n), true));
    });

    test("Set: round-trip with mixed changes", $ => {
        const before = $.const(new Set([1n, 2n, 3n]), SetType(IntegerType));
        const after = $.const(new Set([2n, 4n, 5n]), SetType(IntegerType));
        const patch = $.const(East.diff(before, after));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.has(1n), false));
        $(assert.equal(result.has(2n), true));
        $(assert.equal(result.has(3n), false));
        $(assert.equal(result.has(4n), true));
        $(assert.equal(result.has(5n), true));
        // Invert
        const inverted = $.const(East.invertPatch(patch, SetType(IntegerType)));
        const restored = $.const(East.applyPatch(after, inverted));
        $(assert.equal(restored.has(1n), true));
        $(assert.equal(restored.has(2n), true));
        $(assert.equal(restored.has(3n), true));
        $(assert.equal(restored.has(4n), false));
        $(assert.equal(restored.has(5n), false));
    });
});

// =============================================================================
// Dict Tests
// =============================================================================

await describe("Patch - Dicts", (test) => {
    test("Dict: identical is unchanged", $ => {
        const d = $.const(new Map([["a", 1n], ["b", 2n]]), DictType(StringType, IntegerType));
        const patch = $.const(East.diff(d, d));
        $(assert.equal(patch.getTag(), "unchanged"));
    });

    test("Dict: insert key", $ => {
        const before = $.const(new Map([["a", 1n]]), DictType(StringType, IntegerType));
        const after = $.const(new Map([["a", 1n], ["b", 2n]]), DictType(StringType, IntegerType));
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const ops = $.const(patch.unwrap("patch"));
        $(assert.equal(ops.has("b"), true));
        $(assert.equal(ops.get("b").getTag(), "insert"));
        $(assert.equal(ops.get("b").unwrap("insert"), 2n));
    });

    test("Dict: delete key", $ => {
        const before = $.const(new Map([["a", 1n], ["b", 2n]]), DictType(StringType, IntegerType));
        const after = $.const(new Map([["a", 1n]]), DictType(StringType, IntegerType));
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const ops = $.const(patch.unwrap("patch"));
        $(assert.equal(ops.has("b"), true));
        $(assert.equal(ops.get("b").getTag(), "delete"));
        $(assert.equal(ops.get("b").unwrap("delete"), 2n));
    });

    test("Dict: update value", $ => {
        const before = $.const(new Map([["a", 1n]]), DictType(StringType, IntegerType));
        const after = $.const(new Map([["a", 99n]]), DictType(StringType, IntegerType));
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const ops = $.const(patch.unwrap("patch"));
        $(assert.equal(ops.has("a"), true));
        $(assert.equal(ops.get("a").getTag(), "update"));
        // The update contains a nested patch
        const valuePatch = $.const(ops.get("a").unwrap("update"));
        $(assert.equal(valuePatch.getTag(), "replace"));
        $(assert.equal(valuePatch.unwrap("replace").before, 1n));
        $(assert.equal(valuePatch.unwrap("replace").after, 99n));
    });

    test("Dict: apply and verify", $ => {
        const before = $.const(new Map([["a", 1n], ["b", 2n]]), DictType(StringType, IntegerType));
        const after = $.const(new Map([["a", 10n], ["c", 3n]]), DictType(StringType, IntegerType));
        const patch = $.const(East.diff(before, after));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.get("a"), 10n));
        $(assert.equal(result.has("b"), false));
        $(assert.equal(result.get("c"), 3n));
    });

    test("Dict: round-trip", $ => {
        const before = $.const(new Map([["x", 1n], ["y", 2n]]), DictType(StringType, IntegerType));
        const after = $.const(new Map([["y", 99n], ["z", 3n]]), DictType(StringType, IntegerType));
        const patch = $.const(East.diff(before, after));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.has("x"), false));
        $(assert.equal(result.get("y"), 99n));
        $(assert.equal(result.get("z"), 3n));
        // Invert
        const inverted = $.const(East.invertPatch(patch, DictType(StringType, IntegerType)));
        const restored = $.const(East.applyPatch(after, inverted));
        $(assert.equal(restored.get("x"), 1n));
        $(assert.equal(restored.get("y"), 2n));
        $(assert.equal(restored.has("z"), false));
    });
});

// =============================================================================
// Struct Tests
// =============================================================================

await describe("Patch - Structs", (test) => {
    const PersonType = StructType({ name: StringType, age: IntegerType });

    test("Struct: identical is unchanged", $ => {
        const s = $.const({ name: "Alice", age: 30n }, PersonType);
        const patch = $.const(East.diff(s, s));
        $(assert.equal(patch.getTag(), "unchanged"));
    });

    test("Struct: single field change creates patch", $ => {
        const before = $.const({ name: "Alice", age: 30n }, PersonType);
        const after = $.const({ name: "Alice", age: 31n }, PersonType);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        // Check the field patches
        const fieldPatches = $.const(patch.unwrap("patch"));
        $(assert.equal(fieldPatches.name.getTag(), "unchanged"));
        $(assert.equal(fieldPatches.age.getTag(), "replace"));
        $(assert.equal(fieldPatches.age.unwrap("replace").before, 30n));
        $(assert.equal(fieldPatches.age.unwrap("replace").after, 31n));
    });

    test("Struct: all fields changed", $ => {
        const before = $.const({ name: "Alice", age: 30n }, PersonType);
        const after = $.const({ name: "Bob", age: 25n }, PersonType);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const fieldPatches = $.const(patch.unwrap("patch"));
        $(assert.equal(fieldPatches.name.getTag(), "replace"));
        $(assert.equal(fieldPatches.name.unwrap("replace").before, "Alice"));
        $(assert.equal(fieldPatches.name.unwrap("replace").after, "Bob"));
        $(assert.equal(fieldPatches.age.getTag(), "replace"));
        $(assert.equal(fieldPatches.age.unwrap("replace").before, 30n));
        $(assert.equal(fieldPatches.age.unwrap("replace").after, 25n));
    });

    test("Struct: apply patch", $ => {
        const before = $.const({ name: "Alice", age: 30n }, PersonType);
        const after = $.const({ name: "Bob", age: 25n }, PersonType);
        const patch = $.const(East.diff(before, after));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.name, "Bob"));
        $(assert.equal(result.age, 25n));
    });

    test("Struct: round-trip", $ => {
        const before = $.const({ name: "Alice", age: 30n }, PersonType);
        const after = $.const({ name: "Bob", age: 25n }, PersonType);
        const patch = $.const(East.diff(before, after));
        const inverted = $.const(East.invertPatch(patch, PersonType));
        const restored = $.const(East.applyPatch(after, inverted));
        $(assert.equal(restored.name, "Alice"));
        $(assert.equal(restored.age, 30n));
    });
});

// =============================================================================
// Variant Tests
// =============================================================================

await describe("Patch - Variants", (test) => {
    const ResultType = VariantType({ ok: IntegerType, error: StringType });

    test("Variant: identical is unchanged", $ => {
        const v = $.const(variant("ok", 42n), ResultType);
        const patch = $.const(East.diff(v, v));
        $(assert.equal(patch.getTag(), "unchanged"));
    });

    test("Variant: same case, data changed creates patch", $ => {
        const before = $.const(variant("ok", 1n), ResultType);
        const after = $.const(variant("ok", 99n), ResultType);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        // The patch contains a variant with the case's nested patch
        const casePatch = $.const(patch.unwrap("patch"));
        $(assert.equal(casePatch.getTag(), "ok"));
        const innerPatch = $.const(casePatch.unwrap("ok"));
        $(assert.equal(innerPatch.getTag(), "replace"));
        $(assert.equal(innerPatch.unwrap("replace").before, 1n));
        $(assert.equal(innerPatch.unwrap("replace").after, 99n));
    });

    test("Variant: different cases creates replace", $ => {
        const before = $.const(variant("ok", 42n), ResultType);
        const after = $.const(variant("error", "failed"), ResultType);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "replace"));
        $(assert.equal(patch.unwrap("replace").before.getTag(), "ok"));
        $(assert.equal(patch.unwrap("replace").before.unwrap("ok"), 42n));
        $(assert.equal(patch.unwrap("replace").after.getTag(), "error"));
        $(assert.equal(patch.unwrap("replace").after.unwrap("error"), "failed"));
    });

    test("Variant: apply same-case patch", $ => {
        const before = $.const(variant("ok", 1n), ResultType);
        const after = $.const(variant("ok", 99n), ResultType);
        const patch = $.const(East.diff(before, after));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.getTag(), "ok"));
        $(assert.equal(result.unwrap("ok"), 99n));
    });

    test("Variant: apply case-change replace", $ => {
        const before = $.const(variant("ok", 42n), ResultType);
        const after = $.const(variant("error", "failed"), ResultType);
        const patch = $.const(East.diff(before, after));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.getTag(), "error"));
        $(assert.equal(result.unwrap("error"), "failed"));
    });

    test("Variant: round-trip", $ => {
        const before = $.const(variant("ok", 1n), ResultType);
        const after = $.const(variant("ok", 99n), ResultType);
        const patch = $.const(East.diff(before, after));
        const inverted = $.const(East.invertPatch(patch, ResultType));
        const restored = $.const(East.applyPatch(after, inverted));
        $(assert.equal(restored.getTag(), "ok"));
        $(assert.equal(restored.unwrap("ok"), 1n));
    });
});

// =============================================================================
// Compose Tests
// =============================================================================

await describe("Patch - Compose", (test) => {
    test("Compose: unchanged + unchanged = unchanged", $ => {
        const v = $.const(42n);
        const p1 = $.const(East.diff(v, v));
        const p2 = $.const(East.diff(v, v));
        const composed = $.const(East.composePatch(p1, p2, IntegerType));
        $(assert.equal(composed.getTag(), "unchanged"));
    });

    test("Compose: replace + unchanged = original replace", $ => {
        const v1 = $.const(1n);
        const v2 = $.const(2n);
        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v2));
        const composed = $.const(East.composePatch(p1, p2, IntegerType));
        $(assert.equal(composed.getTag(), "replace"));
        $(assert.equal(composed.unwrap("replace").before, 1n));
        $(assert.equal(composed.unwrap("replace").after, 2n));
    });

    test("Compose: unchanged + replace = second replace", $ => {
        const v1 = $.const(1n);
        const v2 = $.const(2n);
        const p1 = $.const(East.diff(v1, v1));
        const p2 = $.const(East.diff(v1, v2));
        const composed = $.const(East.composePatch(p1, p2, IntegerType));
        $(assert.equal(composed.getTag(), "replace"));
        $(assert.equal(composed.unwrap("replace").before, 1n));
        $(assert.equal(composed.unwrap("replace").after, 2n));
    });

    test("Compose: replace + replace = combined replace", $ => {
        const v1 = $.const(1n);
        const v2 = $.const(2n);
        const v3 = $.const(3n);
        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));
        const composed = $.const(East.composePatch(p1, p2, IntegerType));
        $(assert.equal(composed.getTag(), "replace"));
        $(assert.equal(composed.unwrap("replace").before, 1n));
        $(assert.equal(composed.unwrap("replace").after, 3n));
    });

    test("Compose: verify transitivity", $ => {
        const a = $.const(1n);
        const b = $.const(2n);
        const c = $.const(3n);
        const ab = $.const(East.diff(a, b));
        const bc = $.const(East.diff(b, c));
        const composed = $.const(East.composePatch(ab, bc, IntegerType));
        const result = $.const(East.applyPatch(a, composed));
        $(assert.equal(result, 3n));
    });
});

// =============================================================================
// Algebraic Property Tests
// =============================================================================

await describe("Patch - Algebraic Properties", (test) => {
    test("Self-diff always returns unchanged", $ => {
        const arr = $.const([1n, 2n, 3n]);
        const patch = $.const(East.diff(arr, arr));
        $(assert.equal(patch.getTag(), "unchanged"));
    });

    test("Apply unchanged is identity", $ => {
        const x = $.const({ a: 1n, b: "hello" }, StructType({ a: IntegerType, b: StringType }));
        const patch = $.const(East.diff(x, x));
        const result = $.const(East.applyPatch(x, patch));
        $(assert.equal(result.a, 1n));
        $(assert.equal(result.b, "hello"));
    });

    test("Double invert equals original", $ => {
        const before = $.const(42n);
        const after = $.const(100n);
        const patch = $.const(East.diff(before, after));
        const inv1 = $.const(East.invertPatch(patch, IntegerType));
        const inv2 = $.const(East.invertPatch(inv1, IntegerType));
        // Both should produce same result when applied
        $(assert.equal(East.applyPatch(before, patch), East.applyPatch(before, inv2)));
    });

    test("Invert of unchanged is unchanged", $ => {
        const x = $.const(42n);
        const patch = $.const(East.diff(x, x));
        const inverted = $.const(East.invertPatch(patch, IntegerType));
        $(assert.equal(inverted.getTag(), "unchanged"));
    });

    test("Compose with unchanged is identity", $ => {
        const v1 = $.const(1n);
        const v2 = $.const(2n);
        const patch = $.const(East.diff(v1, v2));
        const unchanged = $.const(East.diff(v2, v2));
        const composed = $.const(East.composePatch(patch, unchanged, IntegerType));
        // Should equal original patch
        $(assert.equal(composed.getTag(), "replace"));
        $(assert.equal(composed.unwrap("replace").before, 1n));
        $(assert.equal(composed.unwrap("replace").after, 2n));
    });
});

// =============================================================================
// Nested Type Tests
// =============================================================================

await describe("Patch - Nested Types", (test) => {
    test("Array<Struct>: update nested field", $ => {
        const ItemType = StructType({ id: IntegerType, name: StringType });
        const before = $.const([{ id: 1n, name: "a" }, { id: 2n, name: "b" }], ArrayType(ItemType));
        const after = $.const([{ id: 1n, name: "a" }, { id: 2n, name: "updated" }], ArrayType(ItemType));
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.get(0n).name, "a"));
        $(assert.equal(result.get(1n).name, "updated"));
    });

    test("Dict<String, Array>: update nested array", $ => {
        const before = $.const(new Map([["x", [1n, 2n, 3n]]]), DictType(StringType, ArrayType(IntegerType)));
        const after = $.const(new Map([["x", [1n, 99n, 3n]]]), DictType(StringType, ArrayType(IntegerType)));
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.get("x").get(0n), 1n));
        $(assert.equal(result.get("x").get(1n), 99n));
        $(assert.equal(result.get("x").get(2n), 3n));
    });

    test("Struct with collection fields", $ => {
        const ContainerType = StructType({
            items: ArrayType(IntegerType),
            lookup: DictType(StringType, IntegerType)
        });
        const before = $.const({
            items: [1n, 2n],
            lookup: new Map([["a", 1n]])
        }, ContainerType);
        const after = $.const({
            items: [1n, 2n, 3n],
            lookup: new Map([["a", 99n]])
        }, ContainerType);
        const patch = $.const(East.diff(before, after));
        $(assert.equal(patch.getTag(), "patch"));
        const result = $.const(East.applyPatch(before, patch));
        $(assert.equal(result.items.length(), 3n));
        $(assert.equal(result.items.get(2n), 3n));
        $(assert.equal(result.lookup.get("a"), 99n));
    });
});

// =============================================================================
// E2E Tests for All Types - patch → patch → compose → invert → roundtrip
// =============================================================================

await describe("Patch - E2E All Types", (test) => {
    // =========================================================================
    // Primitives
    // =========================================================================

    test("E2E: Integer patch-compose-invert roundtrip", $ => {
        // Start: 10 → 20 → 30, compose into single patch, invert, apply to 30 → back to 10
        const v1 = $.const(10n);
        const v2 = $.const(20n);
        const v3 = $.const(30n);

        // Create two patches
        const p1 = $.const(East.diff(v1, v2));  // 10 → 20
        const p2 = $.const(East.diff(v2, v3));  // 20 → 30

        // Verify intermediate results
        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1, 20n));
        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2, 30n));

        // Compose into single patch: 10 → 30
        const composed = $.const(East.composePatch(p1, p2, IntegerType));
        $(assert.equal(composed.getTag(), "replace"));

        // Verify composed patch works
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult, 30n));

        // Invert: 30 → 10
        const inverted = $.const(East.invertPatch(composed, IntegerType));

        // Apply inverted to v3 should give v1
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip, 10n));
    });

    test("E2E: Float patch-compose-invert roundtrip", $ => {
        const v1 = $.const(1.5);
        const v2 = $.const(2.5);
        const v3 = $.const(3.5);

        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));

        $(assert.equal(East.applyPatch(v1, p1), 2.5));
        $(assert.equal(East.applyPatch(v2, p2), 3.5));

        const composed = $.const(East.composePatch(p1, p2, FloatType));
        $(assert.equal(East.applyPatch(v1, composed), 3.5));

        const inverted = $.const(East.invertPatch(composed, FloatType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip, 1.5));
    });

    test("E2E: String patch-compose-invert roundtrip", $ => {
        const v1 = $.const("hello");
        const v2 = $.const("world");
        const v3 = $.const("goodbye");

        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));

        $(assert.equal(East.applyPatch(v1, p1), "world"));
        $(assert.equal(East.applyPatch(v2, p2), "goodbye"));

        const composed = $.const(East.composePatch(p1, p2, StringType));
        $(assert.equal(East.applyPatch(v1, composed), "goodbye"));

        const inverted = $.const(East.invertPatch(composed, StringType));
        $(assert.equal(East.applyPatch(v3, inverted), "hello"));
    });

    test("E2E: Boolean patch-compose-invert roundtrip", $ => {
        const v1 = $.const(true);
        const v2 = $.const(false);
        const v3 = $.const(true);

        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));

        $(assert.equal(East.applyPatch(v1, p1), false));
        $(assert.equal(East.applyPatch(v2, p2), true));

        const composed = $.const(East.composePatch(p1, p2, BooleanType));
        $(assert.equal(East.applyPatch(v1, composed), true));

        const inverted = $.const(East.invertPatch(composed, BooleanType));
        $(assert.equal(East.applyPatch(v3, inverted), true));
    });

    test("E2E: DateTime patch-compose-invert roundtrip", $ => {
        const d1 = new Date("2024-01-01T00:00:00Z");
        const d2 = new Date("2024-06-15T12:00:00Z");
        const d3 = new Date("2025-01-01T00:00:00Z");

        const v1 = $.const(d1);
        const v2 = $.const(d2);
        const v3 = $.const(d3);

        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));

        const composed = $.const(East.composePatch(p1, p2, DateTimeType));
        const result = $.const(East.applyPatch(v1, composed));
        $(assert.equal(result, d3));

        const inverted = $.const(East.invertPatch(composed, DateTimeType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip, d1));
    });

    // =========================================================================
    // Collections
    // =========================================================================

    test("E2E: Array patch-compose-invert roundtrip", $ => {
        // [1,2,3] → [1,2,3,4] → [1,3,4] → compose → invert → back to [1,2,3]
        const v1 = $.const([1n, 2n, 3n]);
        const v2 = $.const([1n, 2n, 3n, 4n]);
        const v3 = $.const([1n, 3n, 4n]);
        const arrType = ArrayType(IntegerType);

        // Create patches
        const p1 = $.const(East.diff(v1, v2));  // insert 4
        const p2 = $.const(East.diff(v2, v3));  // delete 2

        // Verify intermediate
        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.length(), 4n));
        $(assert.equal(applied1.get(3n), 4n));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.length(), 3n));
        $(assert.equal(applied2.get(0n), 1n));
        $(assert.equal(applied2.get(1n), 3n));
        $(assert.equal(applied2.get(2n), 4n));

        // Compose
        const composed = $.const(East.composePatch(p1, p2, arrType));

        // Verify composed gives same result
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.length(), 3n));
        $(assert.equal(directResult.get(1n), 3n));

        // Invert and apply to v3 should give v1
        const inverted = $.const(East.invertPatch(composed, arrType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.length(), 3n));
        $(assert.equal(roundtrip.get(0n), 1n));
        $(assert.equal(roundtrip.get(1n), 2n));
        $(assert.equal(roundtrip.get(2n), 3n));
    });

    test("E2E: Set patch-compose-invert roundtrip", $ => {
        const setType = SetType(IntegerType);
        const v1 = $.const(new SortedSet([1n, 2n, 3n]), setType);
        const v2 = $.const(new SortedSet([1n, 2n, 3n, 4n]), setType);
        const v3 = $.const(new SortedSet([1n, 3n, 4n]), setType);

        const p1 = $.const(East.diff(v1, v2));  // insert 4
        const p2 = $.const(East.diff(v2, v3));  // delete 2

        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.size(), 4n));
        $(assert.equal(applied1.has(4n), true));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.size(), 3n));
        $(assert.equal(applied2.has(2n), false));

        const composed = $.const(East.composePatch(p1, p2, setType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.size(), 3n));
        $(assert.equal(directResult.has(4n), true));
        $(assert.equal(directResult.has(2n), false));

        const inverted = $.const(East.invertPatch(composed, setType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.size(), 3n));
        $(assert.equal(roundtrip.has(1n), true));
        $(assert.equal(roundtrip.has(2n), true));
        $(assert.equal(roundtrip.has(3n), true));
        $(assert.equal(roundtrip.has(4n), false));
    });

    // =========================================================================
    // Complex Types (Struct, Variant)
    // =========================================================================

    test("E2E: Struct patch-compose-invert roundtrip", $ => {
        const PersonType = StructType({ name: StringType, age: IntegerType });
        const v1 = $.const({ name: "Alice", age: 25n }, PersonType);
        const v2 = $.const({ name: "Alice", age: 30n }, PersonType);
        const v3 = $.const({ name: "Bob", age: 30n }, PersonType);

        // Patches
        const p1 = $.const(East.diff(v1, v2));  // age: 25 → 30
        const p2 = $.const(East.diff(v2, v3));  // name: Alice → Bob

        // Verify intermediate
        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.name, "Alice"));
        $(assert.equal(applied1.age, 30n));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.name, "Bob"));
        $(assert.equal(applied2.age, 30n));

        // Compose and verify
        const composed = $.const(East.composePatch(p1, p2, PersonType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.name, "Bob"));
        $(assert.equal(directResult.age, 30n));

        // Invert and roundtrip
        const inverted = $.const(East.invertPatch(composed, PersonType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.name, "Alice"));
        $(assert.equal(roundtrip.age, 25n));
    });

    test("E2E: Variant patch-compose-invert roundtrip", $ => {
        const OptionType = VariantType({ some: IntegerType, none: NullType });
        const v1 = $.const(variant("some", 10n), OptionType);
        const v2 = $.const(variant("some", 20n), OptionType);
        const v3 = $.const(variant("none", null), OptionType);

        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));

        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.getTag(), "some"));
        $(assert.equal(applied1.unwrap("some"), 20n));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.getTag(), "none"));

        const composed = $.const(East.composePatch(p1, p2, OptionType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.getTag(), "none"));

        const inverted = $.const(East.invertPatch(composed, OptionType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.getTag(), "some"));
        $(assert.equal(roundtrip.unwrap("some"), 10n));
    });

    test("E2E: Dict patch-compose-invert roundtrip", $ => {
        const dictType = DictType(StringType, IntegerType);
        const v1 = $.const(new Map([["a", 1n], ["b", 2n]]), dictType);
        const v2 = $.const(new Map([["a", 1n], ["b", 2n], ["c", 3n]]), dictType);
        const v3 = $.const(new Map([["a", 10n], ["b", 2n], ["c", 3n]]), dictType);

        // Patches
        const p1 = $.const(East.diff(v1, v2));  // insert c
        const p2 = $.const(East.diff(v2, v3));  // update a

        // Verify intermediate
        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.size(), 3n));
        $(assert.equal(applied1.get("c"), 3n));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.get("a"), 10n));

        // Compose
        const composed = $.const(East.composePatch(p1, p2, dictType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.size(), 3n));
        $(assert.equal(directResult.get("a"), 10n));
        $(assert.equal(directResult.get("c"), 3n));

        // Invert and roundtrip
        const inverted = $.const(East.invertPatch(composed, dictType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.size(), 2n));
        $(assert.equal(roundtrip.get("a"), 1n));
        $(assert.equal(roundtrip.get("b"), 2n));
    });

    // =========================================================================
    // Nested Types
    // =========================================================================

    test("E2E: Nested struct patch-compose-invert roundtrip", $ => {
        const AddressType = StructType({ city: StringType, zip: IntegerType });
        const PersonType = StructType({ name: StringType, age: IntegerType, address: AddressType });

        const v1 = $.const({ name: "Alice", age: 25n, address: { city: "NYC", zip: 10001n } }, PersonType);
        const v2 = $.const({ name: "Alice", age: 26n, address: { city: "NYC", zip: 10001n } }, PersonType);
        const v3 = $.const({ name: "Alice", age: 26n, address: { city: "LA", zip: 90001n } }, PersonType);

        const p1 = $.const(East.diff(v1, v2));  // age: 25 → 26
        const p2 = $.const(East.diff(v2, v3));  // address: NYC → LA

        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.age, 26n));
        $(assert.equal(applied1.address.city, "NYC"));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.age, 26n));
        $(assert.equal(applied2.address.city, "LA"));

        const composed = $.const(East.composePatch(p1, p2, PersonType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.name, "Alice"));
        $(assert.equal(directResult.age, 26n));
        $(assert.equal(directResult.address.city, "LA"));
        $(assert.equal(directResult.address.zip, 90001n));

        const inverted = $.const(East.invertPatch(composed, PersonType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.name, "Alice"));
        $(assert.equal(roundtrip.age, 25n));
        $(assert.equal(roundtrip.address.city, "NYC"));
        $(assert.equal(roundtrip.address.zip, 10001n));
    });

    test("E2E: Dict<String, Struct> patch-compose-invert roundtrip", $ => {
        const PersonType = StructType({ name: StringType, score: IntegerType });
        const dictType = DictType(StringType, PersonType);

        const v1 = $.const(new Map([
            ["a", { name: "Alice", score: 100n }],
            ["b", { name: "Bob", score: 90n }]
        ]), dictType);
        const v2 = $.const(new Map([
            ["a", { name: "Alice", score: 110n }],
            ["b", { name: "Bob", score: 90n }],
            ["c", { name: "Charlie", score: 80n }]
        ]), dictType);
        const v3 = $.const(new Map([
            ["a", { name: "Alice", score: 110n }],
            ["c", { name: "Charlie", score: 85n }]
        ]), dictType);

        const p1 = $.const(East.diff(v1, v2));  // update a, insert c
        const p2 = $.const(East.diff(v2, v3));  // delete b, update c

        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.size(), 3n));
        $(assert.equal(applied1.get("a").score, 110n));
        $(assert.equal(applied1.get("c").name, "Charlie"));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.size(), 2n));
        $(assert.equal(applied2.get("c").score, 85n));

        const composed = $.const(East.composePatch(p1, p2, dictType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.size(), 2n));
        $(assert.equal(directResult.get("a").score, 110n));
        $(assert.equal(directResult.get("c").score, 85n));

        const inverted = $.const(East.invertPatch(composed, dictType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.size(), 2n));
        $(assert.equal(roundtrip.get("a").score, 100n));
        $(assert.equal(roundtrip.get("b").name, "Bob"));
    });

    test("E2E: Nested Array<Struct> patch-compose-invert roundtrip", $ => {
        const ItemType = StructType({ id: IntegerType, value: StringType });
        const arrType = ArrayType(ItemType);

        const v1 = $.const([
            { id: 1n, value: "one" },
            { id: 2n, value: "two" }
        ], arrType);
        const v2 = $.const([
            { id: 1n, value: "ONE" },  // updated
            { id: 2n, value: "two" }
        ], arrType);
        const v3 = $.const([
            { id: 1n, value: "ONE" },
            { id: 2n, value: "two" },
            { id: 3n, value: "three" }  // inserted
        ], arrType);

        // Patches
        const p1 = $.const(East.diff(v1, v2));  // update first item
        const p2 = $.const(East.diff(v2, v3));  // insert third item

        // Verify intermediate
        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.get(0n).value, "ONE"));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.length(), 3n));
        $(assert.equal(applied2.get(2n).value, "three"));

        // Compose
        const composed = $.const(East.composePatch(p1, p2, arrType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.length(), 3n));
        $(assert.equal(directResult.get(0n).value, "ONE"));
        $(assert.equal(directResult.get(2n).id, 3n));

        // Invert and roundtrip
        const inverted = $.const(East.invertPatch(composed, arrType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.length(), 2n));
        $(assert.equal(roundtrip.get(0n).value, "one"));
        $(assert.equal(roundtrip.get(1n).value, "two"));
    });

    // =========================================================================
    // Edge Cases
    // =========================================================================

    test("E2E: Array with multiple operations patch-compose-invert", $ => {
        const arr = ArrayType(IntegerType);
        const v1 = $.const([1n, 2n, 3n, 4n, 5n]);
        const v2 = $.const([1n, 3n, 5n, 6n]);  // delete 2, delete 4, insert 6
        const v3 = $.const([0n, 1n, 3n, 5n, 6n, 7n]);  // insert 0, insert 7

        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));

        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.length(), 4n));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.length(), 6n));
        $(assert.equal(applied2.get(0n), 0n));
        $(assert.equal(applied2.get(5n), 7n));

        const composed = $.const(East.composePatch(p1, p2, arr));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.length(), 6n));
        $(assert.equal(directResult.get(0n), 0n));
        $(assert.equal(directResult.get(5n), 7n));

        const inverted = $.const(East.invertPatch(composed, arr));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.length(), 5n));
        $(assert.equal(roundtrip.get(0n), 1n));
        $(assert.equal(roundtrip.get(1n), 2n));
        $(assert.equal(roundtrip.get(4n), 5n));
    });

    test("E2E: Multiple patches chained", $ => {
        // Chain 4 patches together
        const v1 = $.const(1n);
        const v2 = $.const(2n);
        const v3 = $.const(3n);
        const v4 = $.const(4n);
        const v5 = $.const(5n);

        const p12 = $.const(East.diff(v1, v2));
        const p23 = $.const(East.diff(v2, v3));
        const p34 = $.const(East.diff(v3, v4));
        const p45 = $.const(East.diff(v4, v5));

        // Compose all together
        const p13 = $.const(East.composePatch(p12, p23, IntegerType));
        const p35 = $.const(East.composePatch(p34, p45, IntegerType));
        const p15 = $.const(East.composePatch(p13, p35, IntegerType));

        $(assert.equal(East.applyPatch(v1, p15), 5n));

        const inverted = $.const(East.invertPatch(p15, IntegerType));
        $(assert.equal(East.applyPatch(v5, inverted), 1n));
    });

    test("E2E: Empty to non-empty array", $ => {
        const arr = ArrayType(StringType);
        const v1 = $.const([] as string[], arr);
        const v2 = $.const(["a", "b"]);
        const v3 = $.const(["a", "b", "c", "d"]);

        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));

        const composed = $.const(East.composePatch(p1, p2, arr));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.length(), 4n));
        $(assert.equal(directResult.get(0n), "a"));
        $(assert.equal(directResult.get(3n), "d"));

        const inverted = $.const(East.invertPatch(composed, arr));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.length(), 0n));
    });

    test("E2E: Non-empty to empty dict", $ => {
        const dictType = DictType(StringType, IntegerType);
        const v1 = $.const(new Map([["a", 1n], ["b", 2n], ["c", 3n]]), dictType);
        const v2 = $.const(new Map([["a", 1n], ["b", 2n]]), dictType);
        const v3 = $.const(new Map<string, bigint>([]), dictType);

        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));

        const composed = $.const(East.composePatch(p1, p2, dictType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.size(), 0n));

        const inverted = $.const(East.invertPatch(composed, dictType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.size(), 3n));
        $(assert.equal(roundtrip.get("a"), 1n));
        $(assert.equal(roundtrip.get("c"), 3n));
    });

    test("E2E: Set with string keys", $ => {
        const setType = SetType(StringType);
        const v1 = $.const(new SortedSet(["apple", "banana"]), setType);
        const v2 = $.const(new SortedSet(["apple", "banana", "cherry"]), setType);
        const v3 = $.const(new SortedSet(["banana", "cherry", "date"]), setType);

        const p1 = $.const(East.diff(v1, v2));  // insert cherry
        const p2 = $.const(East.diff(v2, v3));  // delete apple, insert date

        const composed = $.const(East.composePatch(p1, p2, setType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.size(), 3n));
        $(assert.equal(directResult.has("banana"), true));
        $(assert.equal(directResult.has("cherry"), true));
        $(assert.equal(directResult.has("date"), true));
        $(assert.equal(directResult.has("apple"), false));

        const inverted = $.const(East.invertPatch(composed, setType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.size(), 2n));
        $(assert.equal(roundtrip.has("apple"), true));
        $(assert.equal(roundtrip.has("banana"), true));
    });

    // =========================================================================
    // Special Types (Ref, Recursive)
    // =========================================================================

    test("E2E: Ref patch-compose-invert roundtrip", $ => {
        const refType = RefType(IntegerType);
        const v1 = $.const(ref(10n), refType);
        const v2 = $.const(ref(20n), refType);
        const v3 = $.const(ref(30n), refType);

        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));

        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.get(), 20n));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.get(), 30n));

        const composed = $.const(East.composePatch(p1, p2, refType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.get(), 30n));

        const inverted = $.const(East.invertPatch(composed, refType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.get(), 10n));
    });

    test("E2E: Recursive type patch-compose-invert roundtrip", $ => {
        // Tree type: { value: Integer, children: Array<Tree> }
        const TreeType = RecursiveType((self) => StructType({
            value: IntegerType,
            children: ArrayType(self)
        }));

        const v1 = $.const({ value: 1n, children: [{ value: 2n, children: [] }] }, TreeType);
        const v2 = $.const({ value: 1n, children: [{ value: 3n, children: [] }] }, TreeType);
        const v3 = $.const({ value: 10n, children: [{ value: 3n, children: [] }] }, TreeType);

        const p1 = $.const(East.diff(v1, v2));  // child value: 2 → 3
        const p2 = $.const(East.diff(v2, v3));  // root value: 1 → 10

        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.unwrap().value, 1n));
        $(assert.equal(applied1.unwrap().children.get(0n).unwrap().value, 3n));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.unwrap().value, 10n));
        $(assert.equal(applied2.unwrap().children.get(0n).unwrap().value, 3n));

        const composed = $.const(East.composePatch(p1, p2, TreeType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.unwrap().value, 10n));
        $(assert.equal(directResult.unwrap().children.get(0n).unwrap().value, 3n));

        const inverted = $.const(East.invertPatch(composed, TreeType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.unwrap().value, 1n));
        $(assert.equal(roundtrip.unwrap().children.get(0n).unwrap().value, 2n));
    });

    // =========================================================================
    // Nasty nested recursive types
    // =========================================================================

    test("E2E: Deeply nested Expr AST with recursive types", $ => {
        // Expression AST: num | add(left, right) | mul(left, right) | neg(expr) | call(name, args: Array<Expr>)
        const ExprType = RecursiveType((self) => VariantType({
            num: IntegerType,
            add: StructType({ left: self, right: self }),
            mul: StructType({ left: self, right: self }),
            neg: self,
            call: StructType({ name: StringType, args: ArrayType(self) })
        }));

        // Build: call("f", [add(1, mul(2, 3)), neg(4)])
        const v1 = $.const(variant("call", {
            name: "f",
            args: [
                variant("add", {
                    left: variant("num", 1n),
                    right: variant("mul", {
                        left: variant("num", 2n),
                        right: variant("num", 3n)
                    })
                }),
                variant("neg", variant("num", 4n))
            ]
        }), ExprType);

        // Change to: call("g", [add(1, mul(2, 99)), neg(5), num(6)])
        const v2 = $.const(variant("call", {
            name: "g",
            args: [
                variant("add", {
                    left: variant("num", 1n),
                    right: variant("mul", {
                        left: variant("num", 2n),
                        right: variant("num", 99n)  // 3 → 99
                    })
                }),
                variant("neg", variant("num", 5n)),  // 4 → 5
                variant("num", 6n)  // new arg
            ]
        }), ExprType);

        // Change to: call("h", [mul(10, 20)])
        const v3 = $.const(variant("call", {
            name: "h",
            args: [
                variant("mul", {
                    left: variant("num", 10n),
                    right: variant("num", 20n)
                })
            ]
        }), ExprType);

        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));

        // Apply forward
        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.unwrap().getTag(), "call"));
        $(assert.equal(applied1.unwrap().unwrap("call").name, "g"));
        $(assert.equal(applied1.unwrap().unwrap("call").args.length(), 3n));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.unwrap().unwrap("call").name, "h"));
        $(assert.equal(applied2.unwrap().unwrap("call").args.length(), 1n));

        // Compose and verify
        const composed = $.const(East.composePatch(p1, p2, ExprType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.unwrap().unwrap("call").name, "h"));
        $(assert.equal(directResult.unwrap().unwrap("call").args.get(0n).unwrap().getTag(), "mul"));

        // Invert and roundtrip
        const inverted = $.const(East.invertPatch(composed, ExprType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.unwrap().unwrap("call").name, "f"));
        $(assert.equal(roundtrip.unwrap().unwrap("call").args.length(), 2n));
        $(assert.equal(roundtrip.unwrap().unwrap("call").args.get(1n).unwrap().getTag(), "neg"));
    });

    test("E2E: JSON-like recursive type with Dict containing recursive values", $ => {
        // JSON: null | bool | num | str | array | object
        const JsonType = RecursiveType((self) => VariantType({
            null: NullType,
            bool: BooleanType,
            num: FloatType,
            str: StringType,
            array: ArrayType(self),
            object: DictType(StringType, self)
        }));

        // Build: { "users": [{ "name": "Alice", "age": 30 }, { "name": "Bob" }], "active": true }
        const v1 = $.const(variant("object", new Map<string, ValueTypeOf<typeof JsonType>>([
            ["users", variant("array", [
                variant("object", new Map<string, ValueTypeOf<typeof JsonType>>([
                    ["name", variant("str", "Alice")],
                    ["age", variant("num", 30)]
                ])),
                variant("object", new Map<string, ValueTypeOf<typeof JsonType>>([
                    ["name", variant("str", "Bob")]
                ]))
            ])],
            ["active", variant("bool", true)]
        ])), JsonType);

        // Change to: { "users": [{ "name": "Alice", "age": 31 }], "active": false, "count": 1 }
        const v2 = $.const(variant("object", new Map<string, ValueTypeOf<typeof JsonType>>([
            ["users", variant("array", [
                variant("object", new Map<string, ValueTypeOf<typeof JsonType>>([
                    ["name", variant("str", "Alice")],
                    ["age", variant("num", 31)]
                ]))
            ])],
            ["active", variant("bool", false)],
            ["count", variant("num", 1)]
        ])), JsonType);

        // Change to: { "data": null }
        const v3 = $.const(variant("object", new Map([
            ["data", variant("null", null)]
        ])), JsonType);

        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));

        // Apply forward
        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.unwrap().unwrap("object").get("active").unwrap().unwrap("bool"), false));
        $(assert.equal(applied1.unwrap().unwrap("object").get("count").unwrap().unwrap("num"), 1));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.unwrap().unwrap("object").has("data"), true));
        $(assert.equal(applied2.unwrap().unwrap("object").get("data").unwrap().getTag(), "null"));

        // Compose
        const composed = $.const(East.composePatch(p1, p2, JsonType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.unwrap().unwrap("object").size(), 1n));
        $(assert.equal(directResult.unwrap().unwrap("object").has("data"), true));

        // Invert and roundtrip
        const inverted = $.const(East.invertPatch(composed, JsonType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.unwrap().unwrap("object").has("users"), true));
        $(assert.equal(roundtrip.unwrap().unwrap("object").get("users").unwrap().unwrap("array").length(), 2n));
    });

    test("E2E: Recursive linked list with nested structs", $ => {
        // Node with metadata: { value: Struct, next: Option<Node> }
        const MetadataType = StructType({
            id: IntegerType,
            tags: ArrayType(StringType),
            scores: DictType(StringType, FloatType)
        });
        const ListType = RecursiveType((self) => StructType({
            value: MetadataType,
            next: VariantType({ none: NullType, some: self })
        }));

        // Build: [{ id: 1, tags: ["a"], scores: {"x": 1.0} }] → [{ id: 2, tags: ["b"], scores: {} }] → none
        const v1 = $.const({
            value: { id: 1n, tags: ["a"], scores: new Map([["x", 1.0]]) },
            next: variant("some", {
                value: { id: 2n, tags: ["b"], scores: new Map<string, number>() },
                next: variant("none", null)
            })
        }, ListType);

        // Change head and add element to middle
        const v2 = $.const({
            value: { id: 10n, tags: ["a", "updated"], scores: new Map([["x", 2.0], ["y", 3.0]]) },
            next: variant("some", {
                value: { id: 2n, tags: ["b", "c"], scores: new Map([["z", 9.9]]) },
                next: variant("some", {
                    value: { id: 3n, tags: [], scores: new Map<string, number>() },
                    next: variant("none", null)
                })
            })
        }, ListType);

        // Truncate to single element
        const v3 = $.const({
            value: { id: 100n, tags: [], scores: new Map<string, number>() },
            next: variant("none", null)
        }, ListType);

        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));

        // Apply forward
        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.unwrap().value.id, 10n));
        $(assert.equal(applied1.unwrap().value.tags.length(), 2n));
        $(assert.equal(applied1.unwrap().next.getTag(), "some"));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.unwrap().value.id, 100n));
        $(assert.equal(applied2.unwrap().next.getTag(), "none"));

        // Compose
        const composed = $.const(East.composePatch(p1, p2, ListType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.unwrap().value.id, 100n));
        $(assert.equal(directResult.unwrap().next.getTag(), "none"));

        // Invert and roundtrip
        const inverted = $.const(East.invertPatch(composed, ListType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.unwrap().value.id, 1n));
        $(assert.equal(roundtrip.unwrap().value.tags.get(0n), "a"));
        $(assert.equal(roundtrip.unwrap().next.getTag(), "some"));
        $(assert.equal(roundtrip.unwrap().next.unwrap("some").unwrap().value.id, 2n));
    });

    test("E2E: Mutually-referential-like structure via deep nesting", $ => {
        // Forest: Array of Trees where each Tree has children that can be any subtree
        // Tree = { label: String, metadata: Dict<String, Variant>, children: Array<Tree> }
        const TreeType = RecursiveType((self) => StructType({
            label: StringType,
            metadata: DictType(StringType, VariantType({
                text: StringType,
                number: IntegerType,
                flag: BooleanType,
                nested: ArrayType(self)  // Can nest trees in metadata!
            })),
            children: ArrayType(self)
        }));
        const ForestType = ArrayType(TreeType);

        // Type for metadata variant (nested case references any[] since recursive)
        type MetaVariant = variant<"text", string> | variant<"number", bigint> | variant<"flag", boolean> | variant<"nested", any[]>;
        const emptyMeta = (): Map<string, MetaVariant> => new Map();

        // Complex forest with metadata containing nested trees
        const v1 = $.const([
            {
                label: "root1",
                metadata: new Map<string, MetaVariant>([
                    ["info", variant("text", "hello")],
                    ["related", variant("nested", [
                        { label: "meta-child", metadata: emptyMeta(), children: [] }
                    ])]
                ]),
                children: [
                    { label: "child1", metadata: emptyMeta(), children: [] }
                ]
            },
            {
                label: "root2",
                metadata: new Map<string, MetaVariant>([["count", variant("number", 42n)]]),
                children: []
            }
        ], ForestType);

        // Modify deeply
        const v2 = $.const([
            {
                label: "root1-renamed",
                metadata: new Map<string, MetaVariant>([
                    ["info", variant("text", "world")],
                    ["related", variant("nested", [
                        { label: "meta-child-updated", metadata: emptyMeta(), children: [] },
                        { label: "new-meta-child", metadata: emptyMeta(), children: [] }
                    ])],
                    ["new-field", variant("flag", true)]
                ]),
                children: [
                    { label: "child1", metadata: emptyMeta(), children: [] },
                    { label: "child2", metadata: emptyMeta(), children: [] }
                ]
            }
        ], ForestType);

        // Simplify
        const v3 = $.const([
            { label: "simple", metadata: emptyMeta(), children: [] }
        ], ForestType);

        const p1 = $.const(East.diff(v1, v2));
        const p2 = $.const(East.diff(v2, v3));

        // Verify forward application
        const applied1 = $.const(East.applyPatch(v1, p1));
        $(assert.equal(applied1.length(), 1n));
        $(assert.equal(applied1.get(0n).unwrap().label, "root1-renamed"));

        const applied2 = $.const(East.applyPatch(applied1, p2));
        $(assert.equal(applied2.get(0n).unwrap().label, "simple"));

        // Compose and apply
        const composed = $.const(East.composePatch(p1, p2, ForestType));
        const directResult = $.const(East.applyPatch(v1, composed));
        $(assert.equal(directResult.length(), 1n));
        $(assert.equal(directResult.get(0n).unwrap().label, "simple"));

        // Invert and roundtrip
        const inverted = $.const(East.invertPatch(composed, ForestType));
        const roundtrip = $.const(East.applyPatch(v3, inverted));
        $(assert.equal(roundtrip.length(), 2n));
        $(assert.equal(roundtrip.get(0n).unwrap().label, "root1"));
        $(assert.equal(roundtrip.get(1n).unwrap().label, "root2"));
    });
});

// =============================================================================
// Fuzz Tests - Random Types
// =============================================================================

// Generate all test cases upfront using shared fuzz configuration
const fuzzTestCases = generateFuzzTestCases({ numTypes: 20, numSamples: 5 });

for (const tc of fuzzTestCases) {
    await describe(`Patch Fuzz - ${tc.typeName}`, (test) => {
        test("diff/apply round trip", $ => {
            // Use 'as any' to bypass TypeScript's static type checking for dynamic types
            const pairs = $.const(tc.pairs as any, tc.pairsArrayType as any);

            $.for(pairs as any, ($, pair: any) => {
                const before = $.let((pair as any).before);
                const after = $.let((pair as any).after);

                const patch = $.let(East.diff(before as any, after as any));
                const applied = $.let(East.applyPatch(before as any, patch as any));

                $(assert.equal(East.equal(applied as any, after as any), true));
            });
        });

        test("invert round trip", $ => {
            const pairs = $.const(tc.pairs as any, tc.pairsArrayType as any);

            $.for(pairs as any, ($, pair: any) => {
                const before = $.let((pair as any).before);
                const after = $.let((pair as any).after);

                const patch = $.let(East.diff(before as any, after as any));
                const inverted = $.let(East.invertPatch(patch as any, tc.type));
                const roundtrip = $.let(East.applyPatch(after as any, inverted as any));

                $(assert.equal(East.equal(roundtrip as any, before as any), true));
            });
        });

        test("compose round trip", $ => {
            const trips = $.const(tc.triplets as any, tc.tripletsArrayType as any);

            $.for(trips as any, ($, trip: any) => {
                const v1 = $.let((trip as any).v1);
                const v2 = $.let((trip as any).v2);
                const v3 = $.let((trip as any).v3);

                const p1 = $.let(East.diff(v1 as any, v2 as any));
                const p2 = $.let(East.diff(v2 as any, v3 as any));
                const composed = $.let(East.composePatch(p1 as any, p2 as any, tc.type));
                const direct = $.let(East.applyPatch(v1 as any, composed as any));

                $(assert.equal(East.equal(direct as any, v3 as any), true));

                // Verify sequential application matches
                const step1 = $.let(East.applyPatch(v1 as any, p1 as any));
                const step2 = $.let(East.applyPatch(step1 as any, p2 as any));
                $(assert.equal(East.equal(step2 as any, v3 as any), true));
            });
        });
    });
}
