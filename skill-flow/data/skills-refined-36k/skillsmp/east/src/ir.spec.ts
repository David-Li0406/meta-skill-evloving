/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { describe, test } from "node:test";
import assert from "node:assert";
import { IRType } from "./ir.js";
import { fromJSONFor, toJSONFor } from "./serialization/json.js";
import { IntegerType, NullType, StringType } from "./types.js";
import { East } from "./expr/index.js";
import { str } from "./expr/block.js";

describe("IR deserialization", () => {
    test("should serialize and deserialize increment function IR", () => {
        // JSON generated from compile.ts for increment function: (x: Integer) -> x + 1

        const log = East.platform("log", [StringType], NullType);
        const fetch_status = East.platform("fetch_status", [StringType], StringType);
        const time_ns = East.platform("time_ns", [], IntegerType);

        const fetchStatus = East.function([StringType], NullType, ($, url) => {
            $(log(str`Fetching URL: ${url}`));
            const t1 = $.let(time_ns());
            const response = $.let(fetch_status(url));
            const t2 = $.let(time_ns());
            $(log(str`Response status: ${response} - fetched in ${t2.subtract(t1).multiply(1e-6)} ms`));
        });

        // Create encoder and decoder for IR type
        const toJSON = toJSONFor(IRType);
        const fromJSON = fromJSONFor(IRType);

        // Deserialize the JSON to IR
        const to = toJSON(fetchStatus.toIR().ir);
        const from = fromJSON(to);

        // Deep compare the deserialized IR with expected value
        assert.deepStrictEqual(from, fetchStatus.toIR().ir);
    });
});
