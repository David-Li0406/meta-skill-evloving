/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under AGPL-3.0. See LICENSE file for details.
 */
import { East, IntegerType, NullType, EastError, StringType, FunctionType, encodeBeast2For, decodeBeast2For, StructType } from "../../src/index.js";
import type { PlatformFunction } from "../../src/platform.js";

const log = East.platform("log", [StringType], NullType);

const platform = [
    log.implement(console.log),
];

{
    console.log(" * Can read input 1n and return output 2n:");

    const f = East.function([IntegerType], IntegerType, ($, input) => {
        return input.add(1n);
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled(1n);

    console.log(result);
    console.log();
}

{
    console.log(" * Early return:");

    const f = East.function([], IntegerType, $ => {
        const x = $.let(1n)
        $.return(x)
        // const y = $.let(x.add(1n));
        // return y;
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}

{
    console.log(" * Adding numbers from array individually:");

    const f = East.function([], IntegerType, $ => {
        const array = $.let([10n, 20n, 30n]);
        const x = $.let(array.get(0n));
        const y = $.let(array.get(1n));
        const z = $.let(array.get(2n));
        return x.add(y).add(z);
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}

{
    console.log(" * Adding numbers from array in a for loop:");

    const f = East.function([], IntegerType, $ => {
        const array = $.let([10n, 20n, 30n]);
        const ret = $.let(0n)
        $.for(array, ($, x) => $.assign(ret, ret.add(x)))
        return ret;
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}

{
    console.log(" * Adding numbers from set in a for loop:");

    const f = East.function([], IntegerType, $ => {
        const set = $.let(new Set([10n, 20n, 30n]));
        const ret = $.let(0n)
        $.for(set, ($, x) => $.assign(ret, ret.add(x)))
        return ret;
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}

{
    console.log(" * Adding numbers from dict in a for loop:");

    const f = East.function([], IntegerType, $ => {
        const dict = $.let(new Map([["a", 10n], ["b", 20n], ["c", 30n]]));
        const ret = $.let(0n)
        $.for(dict, ($, value, key) => $.assign(ret, ret.add(value)))
        return ret;
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}

{
    console.log(" * Read captured variables from a Function ");

    const f = East.function([], NullType, $ => {
        const array = $.const([10n, 20n, 30n]);
        $(array.forEach(($, x) => $(log(East.print(x)))));
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}

{
    console.log(" * Reassign captured variables from a Function ");

    const f = East.function([], IntegerType, $ => {
        const array = $.const([10n, 20n, 30n]);
        const ret = $.let(0n)
        $(array.forEach(($, x) => {
            // $(log(ret));
            // $(log(x));
            $.assign(ret, ret.add(x));
            return null
        }));
        return ret;
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}


{
    console.log(" * Platform effects (logging) in a for loop:");

    const f = East.function([], NullType, $ => {
        const array = $.let([10n, 20n, 30n]);
        $.for(array, ($, x) => {
            $(log(East.print(x)))
        })
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}


{
    console.log(" * Platform effects (logging) in a higher-order forEachValue:");

    const f = East.function([], NullType, $ => {
        const array = $.let([10n, 20n, 30n]);
        $(array.forEach(($, x) => $(log(East.print(x)))))
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}

{
    console.log(" * Early return inside if:");

    const f = East.function([], IntegerType, $ => {
        const x = $.let(true);
        $.if(x, $ => $.return(42n))
        return 0n;
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}

{
    console.log(" * Break from while:");

    const f = East.function([], IntegerType, $ => {
        $.while(true, ($, label) => $.break(label))
        return 42n;
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}

{
    console.log(" * Return from while:");

    const f = East.function([], IntegerType, $ => {
        $.while(true, $ => $.return(42n));
        $.return(0n);
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}

{
    console.log(" * Errors inside ifElse branches (error missed):");

    const f = East.function([], IntegerType, $ => {
        const x = $.let(true);
        const y = $.let(x.ifElse($ => 42n, $ => $.error("unexpected error")))
        return y;
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}

{
    console.log(" * Errors inside ifElse branches (error hit):");

    const f = East.function([], IntegerType, $ => {
        const x = $.let(false);
        const y = $.let(x.ifElse($ => 42n, $ => $.error("expected error")))
        return y;
    });

    const f_compiled = East.compile(f, platform);

    try {
        f_compiled();
    } catch (e: unknown) {
        if (e instanceof EastError) {
            console.log(e.message)
        } else {
            console.log(`Caught unexpected exception ${e}`)
        }
    }
    console.log();
}

{
    console.log(" * Out-of-bounds access:");

    const f = East.function([], IntegerType, $ => {
        const array = $.let([10n, 20n, 30n]);
        return array.get(4n);
    });

    const f_compiled = East.compile(f, platform);

    try {
        f_compiled();
    } catch (e: unknown) {
        if (e instanceof EastError) {
            console.log(e.message)
        } else {
            console.log(`Caught unexpected exception ${e}`)
        }
    }
    console.log();
}

{
    console.log(" * Construct and deconstruct structs:");

    const f = East.function([], IntegerType, $ => {
        const x = $.let({ a: 42n, b: true });

        const xa = $.let(x.a);

        const y = $.let(x.b.ifElse($ => x.a, $ => 0n))
        return y;
    });

    const f_compiled = East.compile(f, platform);

    const result = f_compiled();

    console.log(result);
    console.log();
}

{
    console.log(" * Produce an error and print a stack trace in JavaScript:");

    const f = East.function([], IntegerType, $ => {
        const array = $.let([10n, 20n, 30n]);
        
        const g = $.let(East.function([IntegerType], IntegerType, ($, i) => {
            $.return(array.get(i));
        }))

        return g(3n); // Oops, out-of-bounds access
    });

    const f_compiled = East.compile(f, platform);

    try {
        const result = f_compiled();
        console.log(result);
    } catch (e: unknown) {
        console.log(e);
    }

    console.log();
}

{
    console.log(" * Produce an error and print a stack trace in East:");

    const f = East.function([], NullType, $ => {
        const array = $.let([10n, 20n, 30n]);
        
        const g = $.let(East.function([IntegerType], IntegerType, ($, i) => {
            $.return(array.get(i));
        }))

        $.try($ => {
            $(g(3n)); // Oops, out-of-bounds access
        }).catch(($, message, stack) => {
            $(log(East.String.printError(message, stack)));
        });
    });

    const f_compiled = East.compile(f, platform);

    try {
        const result = f_compiled();
        console.log(result);
    } catch (e: unknown) {
        console.log(e);
    }

    console.log();
}

{
    console.log(" * Serialize and deserialize a function that uses a platform function:");

    // Define a platform function for doubling integers
    const double = East.platform("double", [IntegerType], IntegerType);

    const doublePlatform: PlatformFunction[] = [
        double.implement((x: bigint) => x * 2n),
    ];

    // Create a function that uses the platform function
    const f = East.function([IntegerType], IntegerType, ($, x) => {
        return double(x).add(1n);  // double(x) + 1
    });

    // Get the function type for serialization
    const funcType = FunctionType([IntegerType], IntegerType);

    // Compile the function (this attaches the IR)
    const f_compiled = East.compile(f, doublePlatform);

    // Serialize the function to Beast2
    const encoder = encodeBeast2For(funcType);
    const encoded = encoder(f_compiled);
    console.log(`  Encoded function to ${encoded.length} bytes`);

    // Deserialize the function back, passing the platform for compilation
    const decoder = decodeBeast2For(funcType, { platform: doublePlatform });
    const f_decoded = decoder(encoded);

    // Call the decoded function
    const result = f_decoded(10n);
    console.log(`  double(10) + 1 = ${result}`);
    console.log(`  Expected: 21`);
    console.log();
}

{
    console.log(" * Serialize and deserialize a struct containing a callback that uses a platform function:");

    // Define a platform function for logging
    const trace = East.platform("trace", [StringType], NullType);

    const tracePlatform: PlatformFunction[] = [
        trace.implement((msg: string) => console.log(`    [TRACE] ${msg}`)),
    ];

    // Create a callback function that uses the platform function
    const callback = East.function([IntegerType], IntegerType, ($, x) => {
        $(trace(East.print(x)));  // Log the input
        return x.multiply(3n);
    });

    // Define a struct type containing a callback
    const CallbackStructType = StructType({
        name: StringType,
        processor: FunctionType([IntegerType], IntegerType)
    });

    // Compile the callback
    const callback_compiled = East.compile(callback, tracePlatform);

    // Create a struct value with the callback
    const structValue = {
        name: "tripler",
        processor: callback_compiled
    };

    // Serialize the struct
    const encoder = encodeBeast2For(CallbackStructType);
    const encoded = encoder(structValue);
    console.log(`  Encoded struct with callback to ${encoded.length} bytes`);

    // Deserialize the struct, passing platform for function compilation
    const decoder = decodeBeast2For(CallbackStructType, { platform: tracePlatform });
    const decoded = decoder(encoded);

    // Call the deserialized callback
    console.log(`  Calling decoded processor callback with input 7:`);
    const result = decoded.processor(7n);
    console.log(`  Result: ${result}`);
    console.log(`  Expected: 21`);
    console.log();
}
