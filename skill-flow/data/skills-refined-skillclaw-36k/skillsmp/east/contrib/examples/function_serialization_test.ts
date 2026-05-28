/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under AGPL-3.0. See LICENSE file for details.
 *
 * Manual test for function serialization with platform functions.
 * Run with: npm run build && node dist/contrib/examples/function_serialization_test.js
 */
import { East, IntegerType, NullType, StringType, FunctionType, encodeBeast2For, decodeBeast2For, StructType } from "../../src/index.js";
import type { PlatformFunction } from "../../src/platform.js";

console.log("=== Function Serialization with Platform Functions ===\n");

{
    console.log("Test 1: Serialize and deserialize a function that uses a platform function");

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
    console.log(`  PASS: ${result === 21n}`);
    console.log();
}

{
    console.log("Test 2: Serialize and deserialize a struct containing a callback that uses a platform function");

    // Define a platform function for logging
    const trace = East.platform("trace", [StringType], NullType);

    let traceOutput: string[] = [];
    const tracePlatform: PlatformFunction[] = [
        trace.implement((msg: string) => { traceOutput.push(msg); }),
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
    traceOutput = [];  // Clear
    const result = decoded.processor(7n);
    console.log(`  Trace output: ${traceOutput.join(", ")}`);
    console.log(`  Result: ${result}`);
    console.log(`  Expected: 21 (and trace should show "7")`);
    console.log(`  PASS: ${result === 21n && traceOutput[0] === "7"}`);
    console.log();
}

{
    console.log("Test 3: Round-trip a function without platform functions");

    // Create a simple function with no platform dependencies
    const f = East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => {
        return a.add(b).multiply(2n);
    });

    const funcType = FunctionType([IntegerType, IntegerType], IntegerType);

    // Compile with empty platform
    const f_compiled = East.compile(f, []);

    // Serialize
    const encoder = encodeBeast2For(funcType);
    const encoded = encoder(f_compiled);
    console.log(`  Encoded function to ${encoded.length} bytes`);

    // Deserialize with empty platform
    const decoder = decodeBeast2For(funcType, { platform: [] });
    const f_decoded = decoder(encoded);

    // Test
    const result = f_decoded(3n, 4n);
    console.log(`  (3 + 4) * 2 = ${result}`);
    console.log(`  Expected: 14`);
    console.log(`  PASS: ${result === 14n}`);
    console.log();
}

console.log("=== All tests completed ===");
