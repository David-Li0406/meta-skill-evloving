import { East, IntegerType, IRType, NullType, StringType, toJSONFor } from "../../src/index.js";
const { str } = East;

const log = East.platform("log", [StringType], NullType);
const fetch_status = East.asyncPlatform("fetch_status", [StringType], StringType);
const time_ns = East.platform("time_ns", [], IntegerType);

const fetchStatus = East.asyncFunction([StringType], NullType, ($, url) => {
    $(log(str`Fetching URL: ${url}`));
    const t1 = $.let(time_ns());
    const response = $.let(fetch_status(url));
    const t2 = $.let(time_ns());
    $(log(str`Response status: ${response} - fetched in ${t2.subtract(t1).multiply(1e-6)} ms`));
});

const platform = [
    log.implement(console.log),
    fetch_status.implement(async (url: string) => {
        const response = await fetch(url);
        return `${response.status} (${response.statusText})`;
    }),
    time_ns.implement(() => process.hrtime.bigint()),
];

const fetchStatusCompiled = East.compileAsync(fetchStatus, platform);
const increment_ir = fetchStatus.toIR().ir;  // Extract raw IR from wrapper

// Serialize IR to JSON using East's serialization
const toJSON = toJSONFor(IRType);
const json = toJSON(increment_ir);

console.log("IR as JSON:");
console.log(JSON.stringify(json, null, 2));

// Save to file for Python tests
import { writeFileSync } from "fs";
writeFileSync("/tmp/fetch_status_ir.json", JSON.stringify(json, null, 2));


await fetchStatusCompiled("https://www.google.com");
// Fetching URL: https://www.google.com
// Response status: 200 (OK)

console.log();
await fetchStatusCompiled("https://www.google.com");

console.log();
await fetchStatusCompiled("https://www.google.com");