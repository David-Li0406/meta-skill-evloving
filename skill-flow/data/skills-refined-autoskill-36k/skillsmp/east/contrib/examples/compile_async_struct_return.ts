/**
 * Example demonstrating a TypeScript error when using compileAsync with
 * a function that returns a specific StructType.
 *
 * Issue: StructType defaults to { [K in string]: any } which has an index signature,
 * but specific structs like { path: StringType; count: IntegerType } don't have one.
 * TypeScript sees them as incompatible.
 *
 * Error: CallableAsyncFunctionExpr<[StringType], StructType<{path: ..., count: ...}>>
 *        is not assignable to AsyncFunctionExpr<EastType[], EastType>
 */
import { East, IntegerType, StringType, StructType } from "../../src/index.js";

// Define platform functions
const fetch_data = East.asyncPlatform("fetch_data", [StringType], StringType);

// Define an async function with a specific struct return type
const getStatus = East.asyncFunction(
    [StringType],
    StructType({ path: StringType, count: IntegerType }),
    ($, url) => {
        const data = $.let(fetch_data(url));
        return { path: data, count: data.length() };
    }
);

// Platform implementation
const platform = [
    fetch_data.implement(async (url: string) => {
        const response = await fetch(url);
        return response.url;
    }),
];

// With the fix, this now compiles and infers the correct types
const compiled = East.compileAsync(getStatus, platform);

// Type check: compiled should be (url: string) => Promise<{ path: string; count: bigint }>
async function main() {
    const result = await compiled("https://example.com");
    // These should be properly typed:
    const path: string = result.path;
    const count: bigint = result.count;
    console.log("Path:", path);
    console.log("Count:", count);
}

main().catch(console.error);
