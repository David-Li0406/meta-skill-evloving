/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import assert from "node:assert/strict";
import util from "node:util";
import { test as testNode, describe as describeNode } from "node:test";
import { writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { AsyncFunctionType, East, Expr, get_location, printLocations, IRType, NullType, StringType, toJSONFor, type SubtypeExprOrValue } from "../src/index.js";
import { valueOrExprToAstTyped } from "../src/expr/ast.js";
import type { TypeSymbol } from "../src/expr/expr.js";
import type { BlockBuilder } from "../src/expr/block.js";

const { str } = East;

// Force node test to show full stack traces for easier debugging
Error.stackTraceLimit = Infinity

// Force node to print full objects in console.log output
util.inspect.defaultOptions.depth = null

/**
 * Platform function that indicates a test assertion passed.
 *
 * This is used by East test code to signal successful assertions.
 * When running in Node.js, this does nothing. Other platforms may log or track passes.
 */
const testPass = East.platform("testPass", [], NullType);

/**
 * Platform function that indicates a test assertion failed.
 *
 * This is used by East test code to signal failed assertions.
 * When running in Node.js, this throws an assertion error.
 *
 * @param message - The error message describing the assertion failure
 */
const testFail = East.platform("testFail", [StringType], NullType);

/**
 * Platform function that defines a single test case.
 *
 * This is used by East test code to define individual tests.
 * When running in Node.js, this runs the test using Node's test runner.
 *
 * @param name - The name of the test
 * @param body - The test body function
 */
const test = East.asyncPlatform("test", [StringType, AsyncFunctionType([], NullType)], NullType);

/**
 * Platform function that defines a test suite.
 *
 * This is used by East test code to group related tests.
 * When running in Node.js, this runs the suite using Node's describe.
 *
 * @param name - The name of the test suite
 * @param body - A function that calls test() to define tests
 */
const describe = East.asyncPlatform("describe", [StringType, AsyncFunctionType([], NullType)], NullType);

/**
 * Creates a test platform that uses Node.js assertions.
 *
 * @returns A platform object with `testPass`, `testFail`, `test`, and `describe` functions
 */
function createTestPlatform() {
    return [
        testPass.implement(() => { }), // Assertion passed - do nothing (test continues)
        testFail.implement((message: string) => {
            // Assertion failed - throw to fail the test
            assert.fail(message);
        }),
        test.implement((name: string, body: () => Promise<null>) => testNode(name, async () => { await body(); })),
        describe.implement((name: string, body: () => Promise<null>) => describeNode(name, async () => { await body(); })),
    ];
}

const IRToJSON = toJSONFor(IRType);

/**
 * Defines and runs an East test suite using platform functions.
 *
 * This creates a single East function that calls `describe` and `test` platform functions.
 * The entire suite can be exported as IR and run on any East implementation that provides
 * the test platform (testPass, testFail, test, describe).
 *
 * When the `EXPORT_TEST_IR` environment variable is set to a directory path, the IR for
 * each test suite is exported to `<path>/<suite_name>.json`.
 *
 * @param suiteName - The name of the test suite
 * @param builder - A function that receives a `test` function for defining tests
 *
 * @example
 * ```ts
 * describeEast("Array tests", (test) => {
 *   test("addition", $ => {
 *     $(assertEast.equal(East.value(1n).add(1n), 2n));
 *   });
 *   test("subtraction", $ => {
 *     $(assertEast.equal(East.value(2n).subtract(1n), 1n));
 *   });
 * });
 * ```
 *
 * @example
 * ```bash
 * # Export test IR to a directory
 * EXPORT_TEST_IR=./test-ir npm test
 * ```
 */
export function describeEast(
    suiteName: string,
    builder: (test: (name: string, body: ($: BlockBuilder<NullType>) => void) => void) => void
) {
    const tests: Array<{ name: string, body: ($: BlockBuilder<NullType>) => void }> = [];

    // Collect all test names and bodies
    builder((name: string, body: ($: BlockBuilder<NullType>) => void) => {
        tests.push({ name, body });
    });

    // Create a single East function that uses describe/test platform functions
    const suiteFunction = East.asyncFunction([], NullType, $ => {
        $(describe.call($, suiteName, East.asyncFunction([], NullType, $ => {
            for (const { name, body } of tests) {
                $(test.call($, name, East.asyncFunction([], NullType, body)));
            }
        })));
    });

    // Auto-export test IR if EXPORT_TEST_IR environment variable is set to a path
    if (process.env.EXPORT_TEST_IR) {
        const outputDir = process.env.EXPORT_TEST_IR;

        try {
            mkdirSync(outputDir, { recursive: true });

            const ir = suiteFunction.toIR();
            const irJSON = IRToJSON(ir.ir);

            const filename = join(outputDir, `${suiteName.replace(/[^a-zA-Z0-9]/g, '_')}.json`);
            writeFileSync(filename, JSON.stringify(irJSON, null, 2));
            console.log(`✓ Exported test IR: ${filename}`);
        } catch (err) {
            console.error(`✗ Failed to export test IR for "${suiteName}":`, err);
        }
    }

    // Run the test suite using the Node.js platform implementation
    const platform = createTestPlatform();
    const compiled = suiteFunction.toIR().compile(platform);
    return compiled();
}

/**
 * East assertion functions that match Node.js assert API naming.
 *
 * These functions generate East expressions that perform runtime assertions
 * using platform functions, enabling testing of East code.
 */
export const assertEast = {
    /**
     * Asserts that two values are the same reference (meaning if one is mutated, the other reflects the change - and they are always equal).
     *
     * @typeParam E - The type of the actual expression
     * @param actual - The actual value to test
     * @param expected - The expected value to compare against
     * @returns An East expression that performs the equality check
     */
    is<E extends Expr>(actual: E, expected: SubtypeExprOrValue<NoInfer<E>[TypeSymbol]>) {
        const locations = get_location();
        const expected_expr = Expr.fromAst(valueOrExprToAstTyped(expected, Expr.type(actual)));
        return Expr.tryCatch(
            Expr.block($ => {
                const act = $.let(actual);
                const exp = $.let(expected_expr);
                return East.is(act as any, exp as any).ifElse(
                    _$ => testPass(),
                    _$ => testFail(str`Expected ${act} to be ${exp} (${East.value(printLocations(locations))})`)
                );
            }),
            (_$, message, stack) => testFail(East.String.printError(message, stack))
        );
    },

    /**
     * Asserts that two values are equal.
     *
     * @typeParam E - The type of the actual expression
     * @param actual - The actual value to test
     * @param expected - The expected value to compare against
     * @returns An East expression that performs the equality check
     */
    equal<E extends Expr>(actual: E, expected: SubtypeExprOrValue<NoInfer<E>[TypeSymbol]>) {
        const locations = get_location();
        const expected_expr = Expr.fromAst(valueOrExprToAstTyped(expected, Expr.type(actual)));
        return Expr.tryCatch(
            Expr.block($ => {
                const act = $.let(actual);
                const exp = $.let(expected_expr);
                return East.equal(act as any, exp as any).ifElse(
                    _$ => testPass(),
                    _$ => testFail(str`Expected ${act} to equal ${exp} (${East.value(printLocations(locations))})`)
                );
            }),
            (_$, message, stack) => testFail(East.String.printError(message, stack))
        );
    },

    /**
     * Asserts that two values are not equal.
     *
     * @typeParam E - The type of the actual expression
     * @param actual - The actual value to test
     * @param expected - The value that should not be equal
     * @returns An East expression that performs the inequality check
     */
    notEqual<E extends Expr>(actual: E, expected: SubtypeExprOrValue<NoInfer<E>[TypeSymbol]>) {
        const locations = get_location();
        const expected_expr = Expr.fromAst(valueOrExprToAstTyped(expected, Expr.type(actual)));
        return Expr.tryCatch(
            Expr.block($ => {
                const act = $.let(actual);
                const exp = $.let(expected_expr);
                return East.notEqual(act as any, exp as any).ifElse(
                    _$ => testPass(),
                    _$ => testFail(str`Expected ${act} to not equal ${exp} (${East.value(printLocations(locations))})`)
                );
            }),
            (_$, message, stack) => testFail(East.String.printError(message, stack))
        );
    },

    /**
     * Asserts that actual is less than expected.
     *
     * @typeParam E - The type of the actual expression
     * @param actual - The actual value to test
     * @param expected - The value that actual should be less than
     * @returns An East expression that performs the less-than check
     */
    less<E extends Expr>(actual: E, expected: SubtypeExprOrValue<NoInfer<E>[TypeSymbol]>) {
        const locations = get_location();
        const expected_expr = Expr.fromAst(valueOrExprToAstTyped(expected, Expr.type(actual)));
        return Expr.tryCatch(
            Expr.block($ => {
                const act = $.let(actual);
                const exp = $.let(expected_expr);
                return East.less(act as any, exp as any).ifElse(
                    _$ => testPass(),
                    _$ => testFail(str`Expected ${act} to be less than ${exp} (${printLocations(locations)})`)
                );
            }),
            (_$, message, stack) => testFail(East.String.printError(message, stack))
        );
    },

    /**
     * Asserts that actual is less than or equal to expected.
     *
     * @typeParam E - The type of the actual expression
     * @param actual - The actual value to test
     * @param expected - The value that actual should be less than or equal to
     * @returns An East expression that performs the less-than-or-equal check
     */
    lessEqual<E extends Expr>(actual: E, expected: SubtypeExprOrValue<NoInfer<E>[TypeSymbol]>) {
        const locations = get_location();
        const expected_expr = Expr.fromAst(valueOrExprToAstTyped(expected, Expr.type(actual)));
        return Expr.tryCatch(
            Expr.block($ => {
                const act = $.let(actual);
                const exp = $.let(expected_expr);
                return East.lessEqual(act as any, exp as any).ifElse(
                    _$ => testPass(),
                    _$ => testFail(str`Expected ${act} to be less than or equal to ${exp} (${printLocations(locations)})`)
                );
            }),
            (_$, message, stack) => testFail(East.String.printError(message, stack))
        );
    },

    /**
     * Asserts that actual is greater than expected.
     *
     * @typeParam E - The type of the actual expression
     * @param actual - The actual value to test
     * @param expected - The value that actual should be greater than
     * @returns An East expression that performs the greater-than check
     */
    greater<E extends Expr>(actual: E, expected: SubtypeExprOrValue<NoInfer<E>[TypeSymbol]>) {
        const locations = get_location();
        const expected_expr = Expr.fromAst(valueOrExprToAstTyped(expected, Expr.type(actual)));
        return Expr.tryCatch(
            Expr.block($ => {
                const act = $.let(actual);
                const exp = $.let(expected_expr);
                return East.greater(act as any, exp as any).ifElse(
                    _$ => testPass(),
                    _$ => testFail(str`Expected ${act} to be greater than ${exp} (${printLocations(locations)})`)
                );
            }),
            (_$, message, stack) => testFail(East.String.printError(message, stack))
        );
    },

    /**
     * Asserts that actual is greater than or equal to expected.
     *
     * @typeParam E - The type of the actual expression
     * @param actual - The actual value to test
     * @param expected - The value that actual should be greater than or equal to
     * @returns An East expression that performs the greater-than-or-equal check
     */
    greaterEqual<E extends Expr>(actual: E, expected: SubtypeExprOrValue<NoInfer<E>[TypeSymbol]>) {
        const locations = get_location();
        const expected_expr = Expr.fromAst(valueOrExprToAstTyped(expected, Expr.type(actual)));
        return Expr.tryCatch(
            Expr.block($ => {
                const act = $.let(actual);
                const exp = $.let(expected_expr);
                return East.greaterEqual(act as any, exp as any).ifElse(
                    _$ => testPass(),
                    _$ => testFail(str`Expected ${act} to be greater than or equal to ${exp} (${printLocations(locations)})`)
                );
            }),
            (_$, message, stack) => testFail(East.String.printError(message, stack))
        );
    },

    /**
     * Asserts that actual is between min and max (inclusive).
     *
     * @typeParam E - The type of the actual expression
     * @param actual - The actual value to test
     * @param min - The minimum value (inclusive)
     * @param max - The maximum value (inclusive)
     * @returns An East expression that performs the range check
     */
    between<E extends Expr>(actual: E, min: SubtypeExprOrValue<NoInfer<E>[TypeSymbol]>, max: SubtypeExprOrValue<NoInfer<E>[TypeSymbol]>) {
        const locations = get_location();
        const min_expr = Expr.fromAst(valueOrExprToAstTyped(min, Expr.type(actual)));
        const max_expr = Expr.fromAst(valueOrExprToAstTyped(max, Expr.type(actual)));
        return Expr.tryCatch(
            East.greaterEqual(actual, min_expr as any).ifElse(
                _$ => East.lessEqual(actual, max_expr as any).ifElse(
                    _$ => testPass(),
                    _$ => testFail(str`Expected ${actual} to be less than or equal to ${max_expr} (${printLocations(locations)})`)
                ),
                _$ => testFail(str`Expected ${actual} to be greater than or equal to ${min_expr}`)
            ),
            (_$, message, stack) => testFail(East.String.printError(message, stack))
        );
    },

    /**
     * Asserts that an expression throws an error.
     *
     * @param fn - The expression that should throw an error when evaluated
     * @param pattern - Optional regex pattern to match against the error message
     * @returns An East expression that verifies an error is thrown
     */
    throws(fn: Expr<any>, pattern?: RegExp) {
        const locations = get_location();
        return Expr.tryCatch(
            Expr.block($ => {
                const result = $.let(fn);
                $(testFail(str`Expected error, got ${result} (${East.value(printLocations(locations))})`));
                return null;
            }),
            ($, message, stack) => {
                if (pattern) {
                    // Validate error message matches the pattern
                    return message.contains(pattern).ifElse(
                        _$ => testPass(),
                        _$ => testFail(str`Expected error message to match ${East.value(pattern.source)}, but got: ${East.String.printError(message, stack)}`)
                    );
                } else {
                    // Just verify it threw
                    return testPass();
                }
            }
        );
    },
};
