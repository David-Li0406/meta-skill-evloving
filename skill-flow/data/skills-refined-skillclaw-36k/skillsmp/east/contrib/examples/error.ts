/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under AGPL-3.0. See LICENSE file for details.
 *
 * Example demonstrating error handling and stack traces with the new location capture system.
 */
import { East, IntegerType, NullType, EastError, StringType, ArrayType } from "../../src/index.js";

const log = East.platform("log", [StringType], NullType);

const platform = [
    log.implement(console.log),
];

// Helper to run and catch errors
function runAndCatch(name: string, fn: () => void) {
    console.log(`\n=== ${name} ===`);
    try {
        fn();
        console.log("No error thrown");
    } catch (e) {
        if (e instanceof EastError) {
            console.log("EastError caught:");
            console.log("  Message:", e.eastMessage);
            console.log("  Stack locations:");
            for (const loc of e.location) {
                console.log(`    ${loc.filename}:${loc.line}:${loc.column}`);
            }
            console.log("  toString():", e.toString());
        } else {
            console.log("Other error:", e);
        }
    }
}

// Test 1: Simple direct error
runAndCatch("Direct $.error() call", () => {
    const f = East.function([], NullType, $ => {
        $.error("This is a direct error");
    });
    const compiled = East.compile(f, platform);
    compiled();
});

// Test 2: Error inside nested function call
runAndCatch("Error in nested function", () => {
    const inner = East.function([], NullType, $ => {
        $.error("Error from inner function");
    });

    const outer = East.function([], NullType, $ => {
        $(inner());
    });

    const compiled = East.compile(outer, platform);
    compiled();
});

// Test 3: Error in deeply nested calls
runAndCatch("Deeply nested error", () => {
    const level3 = East.function([], NullType, $ => {
        $.error("Error at level 3");
    });

    const level2 = East.function([], NullType, $ => {
        $(level3());
    });

    const level1 = East.function([], NullType, $ => {
        $(level2());
    });

    const compiled = East.compile(level1, platform);
    compiled();
});

// Test 4: Error with Expr.error
runAndCatch("Expr.error() static method", () => {
    const f = East.function([], NullType, $ => {
        $.return($.error("Static error method"));
    });
    const compiled = East.compile(f, platform);
    compiled();
});

// Test 5: Error in conditional branch
runAndCatch("Error in if branch", () => {
    const f = East.function([IntegerType], NullType, ($, x) => {
        $.if(x.equal(0n), $ => {
            $.error("Cannot be zero!");
        });
    });
    const compiled = East.compile(f, platform);
    compiled(0n);
});

// Test 6: Error in loop
runAndCatch("Error in forEach loop", () => {
    const f = East.function([ArrayType(IntegerType)], NullType, ($, arr) => {
        $(arr.forEach(($, val) => {
            $.if(val.less(0n), $ => {
                $.error("Negative values not allowed");
            });
        }));
    });
    const compiled = East.compile(f, platform);
    compiled([1n, 2n, -3n, 4n]);
});

// Test 7: Try-catch demonstration - catches error and logs stack
runAndCatch("Try-catch captures stack", () => {
    const inner = East.function([], NullType, $ => {
        $.error("Inner error to be caught");
    });

    const f = East.function([], StringType, $ => {
        $.try($ => {
            $(inner());
        }).catch(($, message, stack) => {
            // Log the stack info
            $(log(East.String.printError(message, stack)));
        }).finally(() => {});
        $.return("done");
    });
    const compiled = East.compile(f, platform);
    const result = compiled();
    console.log("Function returned:", result);
});

console.log("\n=== Done ===");
