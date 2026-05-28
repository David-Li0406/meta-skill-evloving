/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import assert from "node:assert/strict";
import { describe, test } from "node:test";
import { variant } from '../containers/variant.js';
import { SortedMap } from '../containers/sortedmap.js';
import { SortedSet } from '../containers/sortedset.js';
import { diffFor } from './diff.js';
import { applyFor } from './apply.js';
import { composeFor } from './compose.js';
import { invertFor } from './invert.js';
import { PatchType } from './index.js';
import { ArrayType, BooleanType, DictType, FloatType, IntegerType, NullType, SetType, StringType, StructType, VariantType, isTypeEqual } from '../types.js';
import { equalFor } from '../comparison.js';
import { generateFuzzTestCases } from './fuzz.js';

describe('Patch system for EAST values', () => {
    describe('Primitives', () => {
        test('should diff identical integers as unchanged', () => {
            const diff = diffFor(IntegerType);
            const result = diff(42n, 42n);
            assert.deepEqual(result, variant('unchanged', null));
        });

        test('should diff different integers as replace', () => {
            const diff = diffFor(IntegerType);
            const result = diff(42n, 100n);
            assert.deepEqual(result, variant('replace', { before: 42n, after: 100n }));
        });

        test('should diff identical floats as unchanged', () => {
            const diff = diffFor(FloatType);
            const result = diff(3.14, 3.14);
            assert.deepEqual(result, variant('unchanged', null));
        });

        test('should diff different floats as replace', () => {
            const diff = diffFor(FloatType);
            const result = diff(3.14, 2.71);
            assert.deepEqual(result, variant('replace', { before: 3.14, after: 2.71 }));
        });

        test('should diff identical strings as unchanged', () => {
            const diff = diffFor(StringType);
            const result = diff("hello", "hello");
            assert.deepEqual(result, variant('unchanged', null));
        });

        test('should diff different strings as replace', () => {
            const diff = diffFor(StringType);
            const result = diff("hello", "world");
            assert.deepEqual(result, variant('replace', { before: "hello", after: "world" }));
        });

        test('should diff identical booleans as unchanged', () => {
            const diff = diffFor(BooleanType);
            const result = diff(true, true);
            assert.deepEqual(result, variant('unchanged', null));
        });

        test('should diff different booleans as replace', () => {
            const diff = diffFor(BooleanType);
            const result = diff(true, false);
            assert.deepEqual(result, variant('replace', { before: true, after: false }));
        });

        test('should apply unchanged patch to primitive', () => {
            const apply = applyFor(IntegerType);
            const patch = variant('unchanged', null);
            const result = apply(42n, patch);
            assert.equal(result, 42n);
        });

        test('should apply replace patch to primitive', () => {
            const apply = applyFor(IntegerType);
            const patch = variant('replace', { before: 42n, after: 100n });
            const result = apply(42n, patch);
            assert.equal(result, 100n);
        });

        test('should invert unchanged patch', () => {
            const invert = invertFor(IntegerType);
            const patch = variant('unchanged', null);
            const result = invert(patch);
            assert.deepEqual(result, variant('unchanged', null));
        });

        test('should invert replace patch', () => {
            const invert = invertFor(IntegerType);
            const patch = variant('replace', { before: 42n, after: 100n });
            const result = invert(patch);
            assert.deepEqual(result, variant('replace', { before: 100n, after: 42n }));
        });

        test('should compose unchanged patches', () => {
            const compose = composeFor(IntegerType);
            const first = variant('unchanged', null);
            const second = variant('unchanged', null);
            const result = compose(first, second);
            assert.deepEqual(result, variant('unchanged', null));
        });

        test('should compose replace then unchanged', () => {
            const compose = composeFor(IntegerType);
            const first = variant('replace', { before: 1n, after: 2n });
            const second = variant('unchanged', null);
            const result = compose(first, second);
            assert.deepEqual(result, variant('replace', { before: 1n, after: 2n }));
        });

        test('should compose unchanged then replace', () => {
            const compose = composeFor(IntegerType);
            const first = variant('unchanged', null);
            const second = variant('replace', { before: 1n, after: 2n });
            const result = compose(first, second);
            assert.deepEqual(result, variant('replace', { before: 1n, after: 2n }));
        });

        test('should compose two replace patches', () => {
            const compose = composeFor(IntegerType);
            const first = variant('replace', { before: 1n, after: 2n });
            const second = variant('replace', { before: 2n, after: 3n });
            const result = compose(first, second);
            assert.deepEqual(result, variant('replace', { before: 1n, after: 3n }));
        });
    });

    describe('Arrays', () => {
        const type = ArrayType(IntegerType);

        test('should diff identical arrays as unchanged', () => {
            const diff = diffFor(type);
            const result = diff([1n, 2n, 3n], [1n, 2n, 3n]);
            assert.deepEqual(result, variant('unchanged', null));
        });

        test('should diff different arrays with insert', () => {
            const diff = diffFor(type);
            const result = diff([1n, 3n], [1n, 2n, 3n]);
            assert.equal(result.type, 'patch');
            // Check patch has operations
            assert(Array.isArray(result.value));
        });

        test('should diff different arrays with delete', () => {
            const diff = diffFor(type);
            const result = diff([1n, 2n, 3n], [1n, 3n]);
            assert.equal(result.type, 'patch');
            assert(Array.isArray(result.value));
        });

        test('should diff different arrays with update', () => {
            const diff = diffFor(type);
            const result = diff([1n, 2n, 3n], [1n, 99n, 3n]);
            assert.equal(result.type, 'patch');
            assert(Array.isArray(result.value));
        });

        test('should apply unchanged patch to array', () => {
            const apply = applyFor(type);
            const patch = variant('unchanged', null);
            const result = apply([1n, 2n, 3n], patch);
            assert.deepEqual(result, [1n, 2n, 3n]);
        });

        test('should apply replace patch to array', () => {
            const apply = applyFor(type);
            const before = [1n, 2n, 3n];
            const after = [4n, 5n, 6n];
            const patch = variant('replace', { before, after });
            const result = apply(before, patch);
            assert.deepEqual(result, after);
        });

        test('should round-trip diff and apply for arrays', () => {
            const diff = diffFor(type);
            const apply = applyFor(type);
            const before = [1n, 2n, 3n];
            const after = [1n, 99n, 3n, 4n];
            const patch = diff(before, after);
            const result = apply(before, patch);
            assert.deepEqual(result, after);
        });

        test('should invert and round-trip simple array insert', () => {
            const diff = diffFor(type);
            const apply = applyFor(type);
            const invert = invertFor(type);
            const before = [1n, 2n];
            const after = [1n, 2n, 3n];
            const patch = diff(before, after);
            const inverted = invert(patch);
            const result = apply(after, inverted);
            assert.deepEqual(result, before);
        });

        test('should invert and round-trip simple array delete', () => {
            const diff = diffFor(type);
            const apply = applyFor(type);
            const invert = invertFor(type);
            const before = [1n, 2n, 3n];
            const after = [1n, 3n];
            const patch = diff(before, after);
            const inverted = invert(patch);
            const result = apply(after, inverted);
            assert.deepEqual(result, before);
        });
    });

    describe('Sets', () => {
        const type = SetType(IntegerType);
        const compare = (a: bigint, b: bigint) => a < b ? -1 : a > b ? 1 : 0;
        const createSet = (values: bigint[]) => new SortedSet(values, compare);

        test('should diff identical sets as unchanged', () => {
            const diff = diffFor(type);
            const result = diff(createSet([1n, 2n, 3n]), createSet([1n, 2n, 3n]));
            assert.deepEqual(result, variant('unchanged', null));
        });

        test('should diff different sets with insert', () => {
            const diff = diffFor(type);
            const result = diff(createSet([1n, 3n]), createSet([1n, 2n, 3n]));
            assert.equal(result.type, 'patch');
        });

        test('should diff different sets with delete', () => {
            const diff = diffFor(type);
            const result = diff(createSet([1n, 2n, 3n]), createSet([1n, 3n]));
            assert.equal(result.type, 'patch');
        });

        test('should round-trip diff and apply for sets', () => {
            const diff = diffFor(type);
            const apply = applyFor(type);
            const before = createSet([1n, 2n, 3n]);
            const after = createSet([1n, 3n, 4n]);
            const patch = diff(before, after);
            const result = apply(before, patch);
            assert.deepEqual([...result], [1n, 3n, 4n]);
        });
    });

    describe('Dicts', () => {
        const type = DictType(StringType, IntegerType);
        const compare = (a: string, b: string) => a < b ? -1 : a > b ? 1 : 0;
        const createDict = (entries: [string, bigint][]) => new SortedMap(entries, compare);

        test('should diff identical dicts as unchanged', () => {
            const diff = diffFor(type);
            const result = diff(
                createDict([["a", 1n], ["b", 2n]]),
                createDict([["a", 1n], ["b", 2n]])
            );
            assert.deepEqual(result, variant('unchanged', null));
        });

        test('should diff different dicts with insert', () => {
            const diff = diffFor(type);
            const result = diff(
                createDict([["a", 1n]]),
                createDict([["a", 1n], ["b", 2n]])
            );
            assert.equal(result.type, 'patch');
        });

        test('should diff different dicts with update', () => {
            const diff = diffFor(type);
            const result = diff(
                createDict([["a", 1n], ["b", 2n]]),
                createDict([["a", 1n], ["b", 99n]])
            );
            assert.equal(result.type, 'patch');
        });

        test('should round-trip diff and apply for dicts', () => {
            const diff = diffFor(type);
            const apply = applyFor(type);
            const before = createDict([["a", 1n], ["b", 2n]]);
            const after = createDict([["a", 10n], ["c", 3n]]);
            const patch = diff(before, after);
            const result = apply(before, patch);
            assert.deepEqual([...result.entries()], [["a", 10n], ["c", 3n]]);
        });
    });

    describe('Structs', () => {
        const type = StructType({ x: IntegerType, y: StringType });

        test('should diff identical structs as unchanged', () => {
            const diff = diffFor(type);
            const result = diff({ x: 1n, y: "hello" }, { x: 1n, y: "hello" });
            assert.deepEqual(result, variant('unchanged', null));
        });

        test('should diff different structs with replace', () => {
            const diff = diffFor(type);
            const result = diff({ x: 1n, y: "hello" }, { x: 2n, y: "world" });
            // For structs with changes, we get a patch
            assert.equal(result.type, 'patch');
        });

        test('should round-trip diff and apply for structs', () => {
            const diff = diffFor(type);
            const apply = applyFor(type);
            const before = { x: 1n, y: "hello" };
            const after = { x: 99n, y: "world" };
            const patch = diff(before, after);
            const result = apply(before, patch);
            assert.deepEqual(result, after);
        });
    });

    describe('Variants', () => {
        const type = VariantType({ num: IntegerType, str: StringType });

        test('should diff identical variants as unchanged', () => {
            const diff = diffFor(type);
            const result = diff(variant('num', 42n), variant('num', 42n));
            assert.deepEqual(result, variant('unchanged', null));
        });

        test('should diff same-tag variants with different data as patch', () => {
            const diff = diffFor(type);
            const result = diff(variant('num', 42n), variant('num', 100n));
            assert.equal(result.type, 'patch');
        });

        test('should diff different-tag variants as replace', () => {
            const diff = diffFor(type);
            const result = diff(variant('num', 42n), variant('str', "hello"));
            assert.equal(result.type, 'replace');
        });

        test('should round-trip diff and apply for variants', () => {
            const diff = diffFor(type);
            const apply = applyFor(type);
            const before = variant('num', 42n);
            const after = variant('num', 100n);
            const patch = diff(before, after);
            const result = apply(before, patch);
            assert.deepEqual(result, after);
        });
    });

    describe('PatchType constructor', () => {
        test('should create correct patch type for primitives', () => {
            const expected = VariantType({
                unchanged: NullType,
                replace: StructType({ before: IntegerType, after: IntegerType }),
            });
            assert.ok(isTypeEqual(PatchType(IntegerType), expected));
        });

        test('should create correct patch type for arrays', () => {
            const elementPatchType = VariantType({
                unchanged: NullType,
                replace: StructType({ before: IntegerType, after: IntegerType }),
            });
            const operationType = VariantType({
                delete: IntegerType,
                insert: IntegerType,
                update: elementPatchType,
            });
            const entryType = StructType({
                key: IntegerType,
                offset: IntegerType,
                operation: operationType,
            });
            const expected = VariantType({
                unchanged: NullType,
                replace: StructType({ before: ArrayType(IntegerType), after: ArrayType(IntegerType) }),
                patch: ArrayType(entryType),
            });
            assert.ok(isTypeEqual(PatchType(ArrayType(IntegerType)), expected));
        });

        test('should create correct patch type for sets', () => {
            const operationType = VariantType({
                delete: NullType,
                insert: NullType,
            });
            const expected = VariantType({
                unchanged: NullType,
                replace: StructType({ before: SetType(IntegerType), after: SetType(IntegerType) }),
                patch: DictType(IntegerType, operationType),
            });
            assert.ok(isTypeEqual(PatchType(SetType(IntegerType)), expected));
        });

        test('should create correct patch type for dicts', () => {
            const valuePatchType = VariantType({
                unchanged: NullType,
                replace: StructType({ before: IntegerType, after: IntegerType }),
            });
            const operationType = VariantType({
                delete: IntegerType,
                insert: IntegerType,
                update: valuePatchType,
            });
            const expected = VariantType({
                unchanged: NullType,
                replace: StructType({ before: DictType(StringType, IntegerType), after: DictType(StringType, IntegerType) }),
                patch: DictType(StringType, operationType),
            });
            assert.ok(isTypeEqual(PatchType(DictType(StringType, IntegerType)), expected));
        });

        test('should create correct patch type for structs', () => {
            const xPatchType = VariantType({
                unchanged: NullType,
                replace: StructType({ before: IntegerType, after: IntegerType }),
            });
            const yPatchType = VariantType({
                unchanged: NullType,
                replace: StructType({ before: StringType, after: StringType }),
            });
            const expected = VariantType({
                unchanged: NullType,
                replace: StructType({
                    before: StructType({ x: IntegerType, y: StringType }),
                    after: StructType({ x: IntegerType, y: StringType })
                }),
                patch: StructType({ x: xPatchType, y: yPatchType }),
            });
            assert.ok(isTypeEqual(PatchType(StructType({ x: IntegerType, y: StringType })), expected));
        });

        test('should create correct patch type for variants', () => {
            const numPatchType = VariantType({
                unchanged: NullType,
                replace: StructType({ before: IntegerType, after: IntegerType }),
            });
            const strPatchType = VariantType({
                unchanged: NullType,
                replace: StructType({ before: StringType, after: StringType }),
            });
            const expected = VariantType({
                unchanged: NullType,
                replace: StructType({
                    before: VariantType({ num: IntegerType, str: StringType }),
                    after: VariantType({ num: IntegerType, str: StringType })
                }),
                patch: VariantType({ num: numPatchType, str: strPatchType }),
            });
            assert.ok(isTypeEqual(PatchType(VariantType({ num: IntegerType, str: StringType })), expected));
        });
    });

    describe('Fuzz testing', () => {
        // Generate test cases upfront using shared fuzz configuration
        const fuzzTestCases = generateFuzzTestCases({ numTypes: 100, numSamples: 10 });

        for (const tc of fuzzTestCases) {
            describe(`Type: ${tc.typeName}`, () => {
                const diff = diffFor(tc.type);
                const apply = applyFor(tc.type);
                const invert = invertFor(tc.type);
                const compose = composeFor(tc.type);
                const equal = equalFor(tc.type);
                const patchEqual = equalFor(PatchType(tc.type));

                test('should round-trip diff and apply', () => {
                    for (const { before, after } of tc.pairs) {
                        // Diff identical values should give unchanged
                        const selfPatch = diff(before, before);
                        assert.strictEqual(selfPatch.type, 'unchanged', 'Diff of identical values should be unchanged');

                        // Apply unchanged patch should give same value
                        const appliedSelf = apply(before, selfPatch);
                        assert.ok(equal(appliedSelf, before), 'Applying unchanged patch should give same value');

                        // Diff and apply round trip
                        const patch = diff(before, after);
                        const result = apply(before, patch);
                        assert.ok(equal(result, after), 'Applying diff(a, b) to a should give b');
                    }
                });

                test('should round-trip diff, apply, invert', () => {
                    for (const { before, after } of tc.pairs) {
                        const patch = diff(before, after);
                        const result = apply(before, patch);
                        assert.ok(equal(result, after), 'Applying diff(a, b) to a should give b');

                        // Invert and apply should give back before
                        const invertedPatch = invert(patch);
                        const reversed = apply(after, invertedPatch);
                        assert.ok(equal(reversed, before), 'Applying inverted patch to b should give a');
                    }
                });

                test('should compose patches correctly', () => {
                    for (const { v1, v2, v3 } of tc.triplets) {
                        // Create patches a->b and b->c
                        const patchAB = diff(v1, v2);
                        const patchBC = diff(v2, v3);

                        // Compose them
                        const patchAC = compose(patchAB, patchBC);

                        // Apply composed patch should give same result as sequential application
                        const directResult = apply(apply(v1, patchAB), patchBC);
                        const composedResult = apply(v1, patchAC);

                        assert.ok(equal(composedResult, directResult), 'Composed patch result should match sequential application');
                        assert.ok(equal(composedResult, v3), 'Composed patch should transform a to c');
                    }
                });

                test('should double invert to identity', () => {
                    for (const { before, after } of tc.pairs) {
                        const patch = diff(before, after);

                        // Double invert should give original patch
                        const doubleInverted = invert(invert(patch));
                        assert.ok(patchEqual(doubleInverted, patch), 'Double inversion should give original patch');
                    }
                });
            });
        }
    });
});
