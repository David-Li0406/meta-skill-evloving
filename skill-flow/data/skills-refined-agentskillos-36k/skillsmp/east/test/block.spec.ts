/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import {
    East,
    ArrayType,
    IntegerType,
    NullType,
    BooleanType,
    FloatType,
    StringType,
    DateTimeType,
    BlobType,
    SetType,
    DictType,
    StructType,
    VariantType,
    variant,
} from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

await describe("Block", (test) => {
    test("const() with null", $ => {
        const x = $.const(null);
        $(assert.equal(x, null));
    });

    test("const() with null and type", $ => {
        const x = $.const(null, NullType);
        $(assert.equal(x, null));
    });

    test("const() with boolean", $ => {
        const x = $.const(true);
        $(assert.equal(x, true));
        const y = $.const(false);
        $(assert.equal(y, false));
    });

    test("const() with boolean and type", $ => {
        const x = $.const(true, BooleanType);
        $(assert.equal(x, true));
        const y = $.const(false, BooleanType);
        $(assert.equal(y, false));
    });

    test("const() with integer", $ => {
        const x = $.const(42n);
        $(assert.equal(x, 42n));
    });

    test("const() with integer and type", $ => {
        const x = $.const(42n, IntegerType);
        $(assert.equal(x, 42n));
    });

    test("const() with float", $ => {
        const x = $.const(3.14);
        $(assert.equal(x, 3.14));
    });

    test("const() with float and type", $ => {
        const x = $.const(3.14, FloatType);
        $(assert.equal(x, 3.14));
    });

    test("const() with string", $ => {
        const x = $.const("hello");
        $(assert.equal(x, "hello"));
    });

    test("const() with string and type", $ => {
        const x = $.const("hello", StringType);
        $(assert.equal(x, "hello"));
    });

    test("const() with datetime", $ => {
        const date = new Date("2025-01-01T00:00:00Z");
        const x = $.const(date);
        $(assert.equal(x, date));
    });

    test("const() with datetime and type", $ => {
        const date = new Date("2025-01-01T00:00:00Z");
        const x = $.const(date, DateTimeType);
        $(assert.equal(x, date));
    });

    test("const() with blob", $ => {
        const blob = new Uint8Array([1, 2, 3, 4]);
        const x = $.const(blob);
        $(assert.equal(x, blob));
    });

    test("const() with blob and type", $ => {
        const blob = new Uint8Array([1, 2, 3, 4]);
        const x = $.const(blob, BlobType);
        $(assert.equal(x, blob));
    });

    test("const() with array", $ => {
        const arr = [1n, 2n, 3n];
        const x = $.const(arr);
        $(assert.equal(x, arr));
    });

    test("const() with array and type", $ => {
        const arr = [1n, 2n, 3n];
        const x = $.const(arr, ArrayType(IntegerType));
        $(assert.equal(x, arr));
    });

    test("const() with set", $ => {
        const set = new Set([1n, 2n, 3n]);
        const x = $.const(set);
        $(assert.equal(x, set));
    });

    test("const() with set and type", $ => {
        const set = new Set([1n, 2n, 3n]);
        const x = $.const(set, SetType(IntegerType));
        $(assert.equal(x, set));
    });

    test("const() with dict", $ => {
        const dict = new Map([["a", 1n], ["b", 2n]]);
        const x = $.const(dict);
        $(assert.equal(x, dict));
    });

    test("const() with dict and type", $ => {
        const dict = new Map([["a", 1n], ["b", 2n]]);
        const x = $.const(dict, DictType(StringType, IntegerType));
        $(assert.equal(x, dict));
    });

    test("const() with struct", $ => {
        const struct = { x: 10n, y: 20n };
        const x = $.const(struct);
        $(assert.equal(x, struct));
    });

    test("const() with struct and type", $ => {
        const struct = { x: 10n, y: 20n };
        const x = $.const(struct, StructType({ x: IntegerType, y: IntegerType }));
        $(assert.equal(x, struct));
    });

    test("const() with variant", $ => {
        const v = variant("success", 42n);
        const x = $.const(v, VariantType({ success: IntegerType, failure: StringType }));
        $(assert.equal(x, v));
    });

    test("const() with expression", $ => {
        const x = $.const(East.value(42n));
        $(assert.equal(x, 42n));
    });

    test("let() with null", $ => {
        const x = $.let(null);
        $(assert.equal(x, null));
    });

    test("let() with null and type", $ => {
        const x = $.let(null, NullType);
        $(assert.equal(x, null));
    });

    test("let() with boolean", $ => {
        const x = $.let(true);
        $(assert.equal(x, true));
        const y = $.let(false);
        $(assert.equal(y, false));
    });

    test("let() with boolean and type", $ => {
        const x = $.let(true, BooleanType);
        $(assert.equal(x, true));
        const y = $.let(false, BooleanType);
        $(assert.equal(y, false));
    });

    test("let() with integer", $ => {
        const x = $.let(42n);
        $(assert.equal(x, 42n));
    });

    test("let() with integer and type", $ => {
        const x = $.let(42n, IntegerType);
        $(assert.equal(x, 42n));
    });

    test("let() with float", $ => {
        const x = $.let(3.14);
        $(assert.equal(x, 3.14));
    });

    test("let() with float and type", $ => {
        const x = $.let(3.14, FloatType);
        $(assert.equal(x, 3.14));
    });

    test("let() with string", $ => {
        const x = $.let("hello");
        $(assert.equal(x, "hello"));
    });

    test("let() with string and type", $ => {
        const x = $.let("hello", StringType);
        $(assert.equal(x, "hello"));
    });

    test("let() with datetime", $ => {
        const date = new Date("2025-01-01T00:00:00Z");
        const x = $.let(date);
        $(assert.equal(x, date));
    });

    test("let() with datetime and type", $ => {
        const date = new Date("2025-01-01T00:00:00Z");
        const x = $.let(date, DateTimeType);
        $(assert.equal(x, date));
    });

    test("let() with blob", $ => {
        const blob = new Uint8Array([1, 2, 3, 4]);
        const x = $.let(blob);
        $(assert.equal(x, blob));
    });

    test("let() with blob and type", $ => {
        const blob = new Uint8Array([1, 2, 3, 4]);
        const x = $.let(blob, BlobType);
        $(assert.equal(x, blob));
    });

    test("let() with array", $ => {
        const arr = [1n, 2n, 3n];
        const x = $.let(arr);
        $(assert.equal(x, arr));
    });

    test("let() with array and type", $ => {
        const arr = [1n, 2n, 3n];
        const x = $.let(arr, ArrayType(IntegerType));
        $(assert.equal(x, arr));
    });

    test("let() with set", $ => {
        const set = new Set([1n, 2n, 3n]);
        const x = $.let(set);
        $(assert.equal(x, set));
    });

    test("let() with set and type", $ => {
        const set = new Set([1n, 2n, 3n]);
        const x = $.let(set, SetType(IntegerType));
        $(assert.equal(x, set));
    });

    test("let() with dict", $ => {
        const dict = new Map([["a", 1n], ["b", 2n]]);
        const x = $.let(dict);
        $(assert.equal(x, dict));
    });

    test("let() with dict and type", $ => {
        const dict = new Map([["a", 1n], ["b", 2n]]);
        const x = $.let(dict, DictType(StringType, IntegerType));
        $(assert.equal(x, dict));
    });

    test("let() with struct", $ => {
        const struct = { x: 10n, y: 20n };
        const x = $.let(struct);
        $(assert.equal(x, struct));
    });

    test("let() with struct and type", $ => {
        const struct = { x: 10n, y: 20n };
        const x = $.let(struct, StructType({ x: IntegerType, y: IntegerType }));
        $(assert.equal(x, struct));
    });

    test("let() with variant", $ => {
        const v = variant("success", 42n);
        const x = $.let(v, VariantType({ success: IntegerType, failure: StringType }));
        $(assert.equal(x, v));
    });

    test("let() allows reassignment", $ => {
        const x = $.let(42n);
        $.assign(x, 43n);
        $(assert.equal(x, 43n));
    });

    test("assign() with null", $ => {
        const x = $.let(null);
        $.assign(x, null);
        $(assert.equal(x, null));
    });

    test("assign() with boolean", $ => {
        const x = $.let(true);
        $.assign(x, false);
        $(assert.equal(x, false));
        $.assign(x, true);
        $(assert.equal(x, true));
    });

    test("assign() with integer", $ => {
        const x = $.let(0n);
        $.assign(x, 5n);
        $(assert.equal(x, 5n));
        $.assign(x, 10n);
        $(assert.equal(x, 10n));
    });

    test("assign() with float", $ => {
        const x = $.let(0.0);
        $.assign(x, 3.14);
        $(assert.equal(x, 3.14));
        $.assign(x, 2.71);
        $(assert.equal(x, 2.71));
    });

    test("assign() with string", $ => {
        const x = $.let("hello");
        $.assign(x, "world");
        $(assert.equal(x, "world"));
        $.assign(x, "goodbye");
        $(assert.equal(x, "goodbye"));
    });

    test("assign() with datetime", $ => {
        const date1 = new Date("2025-01-01T00:00:00Z");
        const date2 = new Date("2025-12-31T23:59:59Z");
        const x = $.let(date1);
        $.assign(x, date2);
        $(assert.equal(x, date2));
    });

    test("assign() with blob", $ => {
        const blob1 = new Uint8Array([1, 2, 3]);
        const blob2 = new Uint8Array([4, 5, 6]);
        const x = $.let(blob1);
        $.assign(x, blob2);
        $(assert.equal(x, blob2));
    });

    test("assign() with array", $ => {
        const arr1 = [1n, 2n, 3n];
        const arr2 = [4n, 5n, 6n];
        const x = $.let(arr1);
        $.assign(x, arr2);
        $(assert.equal(x, arr2));
    });

    test("assign() with set", $ => {
        const set1 = new Set([1n, 2n, 3n]);
        const set2 = new Set([4n, 5n, 6n]);
        const x = $.let(set1);
        $.assign(x, set2);
        $(assert.equal(x, set2));
    });

    test("assign() with dict", $ => {
        const dict1 = new Map([["a", 1n], ["b", 2n]]);
        const dict2 = new Map([["c", 3n], ["d", 4n]]);
        const x = $.let(dict1);
        $.assign(x, dict2);
        $(assert.equal(x, dict2));
    });

    test("assign() with struct", $ => {
        const struct1 = { x: 10n, y: 20n };
        const struct2 = { x: 30n, y: 40n };
        const x = $.let(struct1);
        $.assign(x, struct2);
        $(assert.equal(x, struct2));
    });

    test("assign() with variant", $ => {
        const v1 = variant("success", 42n);
        const v2 = variant("failure", "error");
        const x = $.let(v1, VariantType({ success: IntegerType, failure: StringType }));
        $.assign(x, v2);
        $(assert.equal(x, v2));
    });

    test("assign() with expression", $ => {
        const x = $.let(5n);
        const y = $.let(10n);
        $.assign(x, x.add(y));
        $(assert.equal(x, 15n));
    });

    test("if() with true condition", $ => {
        const result = $.let(0n);
        $.if(true, $ => {
            $.assign(result, 42n);
        });
        $(assert.equal(result, 42n));
    });

    test("if() with false condition", $ => {
        const result = $.let(0n);
        $.if(false, $ => {
            $.assign(result, 42n);
        });
        $(assert.equal(result, 0n));
    });

    test("if().else()", $ => {
        const result = $.let(0n);
        $.if(false, $ => {
            $.assign(result, 42n);
        }).else($ => {
            $.assign(result, 99n);
        });
        $(assert.equal(result, 99n));
    });

    test("if().elseIf().else()", $ => {
        const result = $.let(0n);
        const x = $.const(5n);
        $.if(East.equal(x, 0n), $ => {
            $.assign(result, 1n);
        }).elseIf(East.equal(x, 5n), $ => {
            $.assign(result, 2n);
        }).else($ => {
            $.assign(result, 3n);
        });
        $(assert.equal(result, 2n));
    });

    test("while() loop", $ => {
        const i = $.let(0n);
        $.while(East.less(i, 5n), ($) => {
            $.assign(i, i.add(1n));
        });
        $(assert.equal(i, 5n));
    });

    test("while() with break", $ => {
        const i = $.let(0n);
        $.while(true, ($, label) => {
            $.assign(i, i.add(1n));
            $.if(East.equal(i, 3n), $ => {
                $.break(label);
            });
        });
        $(assert.equal(i, 3n));
    });

    test("while() with continue", $ => {
        const i = $.let(0n);
        const sum = $.let(0n);
        $.while(East.less(i, 5n), ($, label) => {
            $.assign(i, i.add(1n));
            $.if(East.equal(i, 3n), $ => {
                $.continue(label);
            });
            $.assign(sum, sum.add(i));
        });
        $(assert.equal(sum, 12n)); // 1 + 2 + 4 + 5 = 12
    });

    test("for() over array", $ => {
        const arr = $.const([1n, 2n, 3n]);
        const sum = $.let(0n);
        $.for(arr, ($, value, _key, _label) => {
            $.assign(sum, sum.add(value));
        });
        $(assert.equal(sum, 6n));
    });

    test("for() over array with index", $ => {
        const arr = $.const([10n, 20n, 30n]);
        const result = $.let([], ArrayType(IntegerType));
        $.for(arr, ($, _value, key) => {
            $(result.pushLast(key));
        });
        $(assert.equal(result, [0n, 1n, 2n]));
    });

    test("for() over set", $ => {
        const set = $.const(new Set([1n, 2n, 3n]));
        const sum = $.let(0n);
        $.for(set, ($, key) => {
            $.assign(sum, sum.add(key));
        });
        $(assert.equal(sum, 6n));
    });

    test("for() over dict", $ => {
        const dict = $.const(new Map([["a", 1n], ["b", 2n], ["c", 3n]]));
        const sum = $.let(0n);
        $.for(dict, ($, value) => {
            $.assign(sum, sum.add(value));
        });
        $(assert.equal(sum, 6n));
    });

    test("for() with break", $ => {
        const arr = $.const([1n, 2n, 3n, 4n, 5n]);
        const sum = $.let(0n);
        $.for(arr, ($, value, _key, label) => {
            $.if(East.equal(value, 3n), $ => {
                $.break(label);
            });
            $.assign(sum, sum.add(value));
        });
        $(assert.equal(sum, 3n)); // 1 + 2 = 3
    });

    test("for() with continue", $ => {
        const arr = $.const([1n, 2n, 3n, 4n, 5n]);
        const sum = $.let(0n);
        $.for(arr, ($, value, _key, label) => {
            $.if(East.equal(value, 3n), $ => {
                $.continue(label);
            });
            $.assign(sum, sum.add(value));
        });
        $(assert.equal(sum, 12n)); // 1 + 2 + 4 + 5 = 12
    });

    // =========================================================================
    // Nested loop break/continue tests - these test that break/continue with
    // labels work correctly when called from nested loops
    // =========================================================================

    test("break outer loop from inner loop", $ => {
        const outer = $.const([1n, 2n, 3n]);
        const inner = $.const([10n, 20n, 30n]);
        const sum = $.let(0n);

        $.for(outer, ($, o, _oi, outer_label) => {
            $.for(inner, ($, i) => {
                $.if(East.equal(o, 2n).bitAnd(East.equal(i, 20n)), $ => {
                    $.break(outer_label); // Break outer loop from inner
                });
                $.assign(sum, sum.add(i));
            });
            $.assign(sum, sum.add(o));
        });
        // o=1: inner adds 10+20+30=60, outer adds 1 -> 61
        // o=2: inner adds 10, then breaks outer
        $(assert.equal(sum, 71n));
    });

    test("continue outer loop from inner loop", $ => {
        const outer = $.const([1n, 2n, 3n]);
        const inner = $.const([10n, 20n, 30n]);
        const sum = $.let(0n);

        $.for(outer, ($, o, _oi, outer_label) => {
            $.for(inner, ($, i) => {
                $.if(East.equal(o, 2n).bitAnd(East.equal(i, 20n)), $ => {
                    $.continue(outer_label); // Continue outer loop from inner
                });
                $.assign(sum, sum.add(i));
            });
            $.assign(sum, sum.add(o));
        });
        // o=1: inner adds 10+20+30=60, outer adds 1 -> 61
        // o=2: inner adds 10, then continues outer (skips rest of inner and outer body)
        // o=3: inner adds 10+20+30=60, outer adds 3 -> 134
        $(assert.equal(sum, 134n));
    });

    test("continue outer loop from deeply nested scope", $ => {
        const arr = $.const([1n, 2n, 3n, 4n, 5n]);
        const sum = $.let(0n);

        $.for(arr, ($, value, _key, outer_label) => {
            // Nested $.if inside $.if
            $.if(East.greater(value, 0n), $ => {
                $.if(East.equal(value, 3n), $ => {
                    $.continue(outer_label); // Skip 3
                });
            });
            $.assign(sum, sum.add(value));
        });
        $(assert.equal(sum, 12n)); // 1 + 2 + 4 + 5 = 12
    });

    test("return() from function", $ => {
        const fn = East.function([IntegerType], IntegerType, ($, x) => {
            $.if(East.equal(x, 0n), $ => {
                $.return(1n);
            });
            return x.multiply(2n);
        });
        $(assert.equal(fn(0n), 1n));
        $(assert.equal(fn(5n), 10n));
    });

    test("try-catch with no error", $ => {
        const result = $.let(0n);
        $.try($ => {
            $.assign(result, 42n);
        }).catch(($, _message, _stack) => {
            $.assign(result, -1n);
        });
        $(assert.equal(result, 42n));
    });

    test("try-catch with error", $ => {
        const result = $.let(0n);
        const arr = $.const([1n, 2n, 3n]);
        $.try($ => {
            $(arr.get(10n));  // Out of bounds error
            $.assign(result, 42n);
        }).catch(($, _message, _stack) => {
            $.assign(result, -1n);
        });
        $(assert.equal(result, -1n));
    });

    test("try-catch returns correct type on success", $ => {
        const arr = $.const([1n, 2n, 3n]);
        const result = $.let(0n);
        $.try($ => {
            $.assign(result, arr.get(0n));
        }).catch(($, _message, _stack) => {
            $.assign(result, -1n);
        });
        $(assert.equal(result, 1n));
    });

    test("try-catch returns correct type on error", $ => {
        const arr = $.const([1n, 2n, 3n]);
        const result = $.let(0n);
        $.try($ => {
            $.assign(result, arr.get(10n));  // Out of bounds
        }).catch(($, _message, _stack) => {
            $.assign(result, -1n);
        });
        $(assert.equal(result, -1n));
    });

    test("try-finally executes finally on success", $ => {
        const result = $.let(0n);
        const finallyExecuted = $.let(false);
        $.try($ => {
            $.assign(result, 42n);
        }).finally($ => {
            $.assign(finallyExecuted, true);
        });
        $(assert.equal(result, 42n));
        $(assert.equal(finallyExecuted, true));
    });

    test("try-finally executes finally on error", $ => {
        const finallyExecuted = $.let(false);
        const arr = $.const([1n, 2n, 3n]);
        $.try($ => {
            $(arr.get(10n));  // Out of bounds error - will throw
        }).catch((_$, _message, _stack) => {
            // Catch the error so test doesn't fail
        }).finally($ => {
            $.assign(finallyExecuted, true);
        });
        $(assert.equal(finallyExecuted, true));
    });

    test("try-catch-finally all execute correctly", $ => {
        const result = $.let(0n);
        const finallyExecuted = $.let(false);
        $.try($ => {
            $.assign(result, 42n);
        }).catch(($, _message, _stack) => {
            $.assign(result, -1n);
        }).finally($ => {
            $.assign(finallyExecuted, true);
        });
        $(assert.equal(result, 42n));
        $(assert.equal(finallyExecuted, true));
    });

    test("try-catch-finally executes finally after catch", $ => {
        const result = $.let(0n);
        const finallyExecuted = $.let(false);
        const arr = $.const([1n, 2n, 3n]);
        $.try($ => {
            $(arr.get(10n));  // Out of bounds error
            $.assign(result, 42n);
        }).catch(($, _message, _stack) => {
            $.assign(result, -1n);
        }).finally($ => {
            $.assign(finallyExecuted, true);
        });
        $(assert.equal(result, -1n));
        $(assert.equal(finallyExecuted, true));
    });

    test("finally executes on early return from try", $ => {
        const finallyExecuted = $.let(false);
        const fn = East.function([IntegerType], IntegerType, ($, x) => {
            $.try($ => {
                $.if(East.equal(x, 0n), $ => {
                    $.return(1n);
                });
                $.return(x.multiply(2n));
            }).finally($ => {
                $.assign(finallyExecuted, true);
            });
            return 999n;  // Should not reach here
        });
        $(assert.equal(fn(0n), 1n));
        $(assert.equal(finallyExecuted, true));
    });

    test("finally executes on early return from catch", $ => {
        const finallyExecuted = $.let(false);
        const arr = $.const([1n, 2n, 3n]);
        const fn = East.function([], IntegerType, ($) => {
            $.try($ => {
                $(arr.get(10n));  // Out of bounds error
                $.return(42n);
            }).catch(($, _message, _stack) => {
                $.return(-1n);
            }).finally($ => {
                $.assign(finallyExecuted, true);
            });
            return 999n;  // Should not reach here
        });
        $(assert.equal(fn(), -1n));
        $(assert.equal(finallyExecuted, true));
    });

    test("finally can modify variables but not affect return value", $ => {
        const sideEffect = $.let(0n);
        const fn = East.function([], IntegerType, ($) => {
            $.try($ => {
                $.return(42n);
            }).finally($ => {
                $.assign(sideEffect, 100n);  // Side effect
            });
            return 999n;  // Should not reach here
        });
        const result = fn();
        $(assert.equal(result, 42n));  // Return value unaffected
        $(assert.equal(sideEffect, 100n));  // Side effect executed
    });

    test("finally block with multiple statements", $ => {
        const counter = $.let(0n);
        $.try($ => {
            $.assign(counter, 1n);
        }).finally($ => {
            $.assign(counter, counter.add(1n));
            $.assign(counter, counter.add(1n));
            $.assign(counter, counter.add(1n));
        });
        $(assert.equal(counter, 4n));
    });

    test("nested try-finally blocks", $ => {
        const outer = $.let(false);
        const inner = $.let(false);
        $.try($ => {
            $.try(_$ => {
                // Inner try
            }).finally($ => {
                $.assign(inner, true);
            });
        }).finally($ => {
            $.assign(outer, true);
        });
        $(assert.equal(inner, true));
        $(assert.equal(outer, true));
    });
});