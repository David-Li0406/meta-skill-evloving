/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Fuzz testing configuration for patch operations.
 * Shared between unit tests (src/patch/patch.spec.ts) and compliance tests (test/patch.spec.ts).
 *
 * @module
 */

import type { EastType, ValueTypeOf, ArrayType as ArrayTypeT, StructType as StructTypeT } from "../types.js";
import {
    ArrayType,
    StructType,
    VariantType,
    DictType,
    SetType,
    RefType,
    FunctionType,
    IntegerType,
    StringType,
    FloatType,
    BooleanType,
    NullType,
    printType,
} from "../types.js";
import { randomType, randomValueFor, randomRecursiveType, randomFunctionType } from "../fuzz.js";

/**
 * A generated test case containing a random type and sample values for testing.
 */
export interface FuzzTestCase<T extends EastType = EastType> {
    /** The randomly generated East type */
    type: T;
    /** String representation of the type for test naming */
    typeName: string;
    /** Array type for before/after pairs (used by compliance tests) */
    pairsArrayType: ArrayTypeT<StructTypeT<{ before: T; after: T }>>;
    /** Array type for v1/v2/v3 triplets (used by compliance tests) */
    tripletsArrayType: ArrayTypeT<StructTypeT<{ v1: T; v2: T; v3: T }>>;
    /** Value pairs for diff/apply/invert tests */
    pairs: Array<{ before: ValueTypeOf<T>; after: ValueTypeOf<T> }>;
    /** Value triplets for compose tests */
    triplets: Array<{ v1: ValueTypeOf<T>; v2: ValueTypeOf<T>; v3: ValueTypeOf<T> }>;
}

/**
 * Options for generating fuzz test cases.
 */
export interface FuzzTestOptions {
    /** Number of random types to generate */
    numTypes?: number;
    /** Number of sample values per type */
    numSamples?: number;
    /** Include recursive types in generation */
    includeRecursive?: boolean;
    /** Include function types in generation */
    includeFunctions?: boolean;
    /** Maximum retries when generating values for a single type */
    maxValueRetries?: number;
    /** Multiplier for max attempts (numTypes * multiplier) */
    attemptsMultiplier?: number;
    /** Ensure diverse type coverage (at least one of each kind) */
    ensureDiversity?: boolean;
}

const DEFAULT_OPTIONS: Required<FuzzTestOptions> = {
    numTypes: 20,
    numSamples: 5,
    includeRecursive: true,
    includeFunctions: true,
    maxValueRetries: 20,
    attemptsMultiplier: 3,
    ensureDiversity: true,
};

/**
 * Specific type generators to ensure diversity in test coverage.
 * These guarantee we test important type patterns that random generation might miss.
 */
function getDiverseTypes(includeRecursive: boolean, includeFunctions: boolean): EastType[] {
    const types: EastType[] = [
        // Variants (often missed by random generation)
        VariantType({ none: NullType, some: IntegerType }),
        VariantType({ ok: StringType, err: StructType({ code: IntegerType, message: StringType }) }),

        // Nested variants
        VariantType({
            leaf: FloatType,
            branch: ArrayType(IntegerType),
        }),

        // Ref types
        RefType(IntegerType),
        RefType(StructType({ x: FloatType, y: FloatType })),

        // Nested collections
        ArrayType(VariantType({ a: IntegerType, b: StringType })),
        DictType(StringType, VariantType({ value: FloatType, missing: NullType })),

        // Struct with variant field
        StructType({
            id: IntegerType,
            status: VariantType({ active: NullType, inactive: StringType }),
        }),

        // Set with different key types
        SetType(IntegerType),

        // Deeply nested
        ArrayType(ArrayType(IntegerType)),
        DictType(StringType, DictType(StringType, IntegerType)),
    ];

    // Add recursive types if enabled
    if (includeRecursive) {
        // Add multiple recursive type patterns
        for (let i = 0; i < 3; i++) {
            types.push(randomRecursiveType());
        }
    }

    // Add function types if enabled
    if (includeFunctions) {
        types.push(
            // Simple function
            FunctionType([IntegerType], StringType),
            // Function with multiple args
            FunctionType([IntegerType, StringType], BooleanType),
            // Random function types
            randomFunctionType(),
            randomFunctionType(),
        );
    }

    return types;
}

/**
 * Generate fuzz test cases with random types and values.
 *
 * This function generates random East types and corresponding sample values
 * for testing patch operations. It handles recursive types gracefully by
 * retrying value generation when max recursion depth is exceeded.
 *
 * @param options Configuration options
 * @returns Array of test cases
 */
export function generateFuzzTestCases(options: FuzzTestOptions = {}): FuzzTestCase[] {
    const opts = { ...DEFAULT_OPTIONS, ...options };
    const testCases: FuzzTestCase[] = [];
    const seenTypes = new Set<string>();

    // Helper to try adding a type to test cases
    const tryAddType = (type: EastType): boolean => {
        const typeName = printType(type);

        // Skip duplicates
        if (seenTypes.has(typeName)) {
            return false;
        }

        try {
            const genValue = randomValueFor(type);

            // Helper to safely generate a value (retry on depth exceeded)
            const safeGenValue = (): any => {
                for (let retry = 0; retry < opts.maxValueRetries; retry++) {
                    try {
                        return genValue();
                    } catch (e) {
                        if ((e as Error).message?.includes("max recursion depth")) {
                            continue;
                        }
                        throw e;
                    }
                }
                throw new Error("max recursion depth");
            };

            // Generate value pairs
            const pairs: Array<{ before: any; after: any }> = [];
            for (let j = 0; j < opts.numSamples; j++) {
                pairs.push({ before: safeGenValue(), after: safeGenValue() });
            }

            // Generate triplets for compose tests
            const triplets: Array<{ v1: any; v2: any; v3: any }> = [];
            for (let j = 0; j < opts.numSamples; j++) {
                triplets.push({ v1: safeGenValue(), v2: safeGenValue(), v3: safeGenValue() });
            }

            // Create array types for East runtime iteration
            const pairsArrayType = ArrayType(StructType({ before: type, after: type }));
            const tripletsArrayType = ArrayType(StructType({ v1: type, v2: type, v3: type }));

            seenTypes.add(typeName);
            testCases.push({
                type,
                typeName,
                pairsArrayType,
                tripletsArrayType,
                pairs,
                triplets,
            });
            return true;
        } catch (e) {
            // Skip types that fail to generate values
            if ((e as Error).message?.includes("max recursion depth")) {
                return false;
            }
            throw e;
        }
    };

    // First, add diverse types to ensure coverage
    if (opts.ensureDiversity) {
        const diverseTypes = getDiverseTypes(opts.includeRecursive, opts.includeFunctions);
        for (const type of diverseTypes) {
            if (testCases.length >= opts.numTypes) break;
            tryAddType(type);
        }
    }

    // Fill remaining slots with random types
    let attempts = 0;
    const maxAttempts = opts.numTypes * opts.attemptsMultiplier;

    while (testCases.length < opts.numTypes && attempts < maxAttempts) {
        attempts++;

        // Generate a random type
        const type = randomType(0, {
            includeRecursive: opts.includeRecursive,
            includeFunctions: opts.includeFunctions,
        });

        tryAddType(type);
    }

    return testCases;
}
