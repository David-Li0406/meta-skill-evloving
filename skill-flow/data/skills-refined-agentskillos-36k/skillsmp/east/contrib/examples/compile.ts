/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under AGPL-3.0. See LICENSE file for details.
 */
import { East, IntegerType } from "../../src/index.js";
import { IRType } from "../../src/ir.js";
import { toJSONFor } from "../../src/serialization/json.js";

// Create a simple function: (x: Integer) -> x + 1
const increment = East.function([IntegerType], IntegerType, ($, x) => {
    return x.add(1n);
});

const increment_ir_wrapper = increment.toIR();
const increment_ir = increment_ir_wrapper.ir;  // Extract raw IR from wrapper

// Serialize IR to JSON using East's serialization
const toJSON = toJSONFor(IRType);
const json = toJSON(increment_ir);

console.log("IR as JSON:");
console.log(JSON.stringify(json, null, 2));

// Save to file for Python tests
import { writeFileSync } from "fs";
writeFileSync("/tmp/increment_ir.json", JSON.stringify(json, null, 2));