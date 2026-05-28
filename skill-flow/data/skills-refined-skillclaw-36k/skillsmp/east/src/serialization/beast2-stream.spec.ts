/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { describe, test } from "node:test";
import assert from "node:assert/strict";
import { encodeBeast2For } from "./beast2.js";
import { encodeBeast2ToStreamFor, decodeBeast2FromStream } from "./beast2-stream.js";
import { fuzzerTest } from "../fuzz.js";
import { equalFor } from "../comparison.js";
import type { EastType } from "../types.js";
import { toEastTypeValue } from "../type_of_type.js";
import { isTypeValueEqual } from "../compile.js";

async function streamToUint8Array(stream: ReadableStream<Uint8Array>): Promise<Uint8Array> {
  const reader = stream.getReader();
  const chunks: Uint8Array[] = [];
  let totalLength = 0;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    totalLength += value.length;
  }

  const result = new Uint8Array(totalLength);
  let offset = 0;
  for (const chunk of chunks) {
    result.set(chunk, offset);
    offset += chunk.length;
  }

  return result;
}

/**
 * Helper to convert a Uint8Array to a ReadableStream.
 * Chunks the data into random-sized pieces to stress test the stream handling.
 */
function uint8ArrayToStream(data: Uint8Array): ReadableStream<Uint8Array> {
  return new ReadableStream({
    start(controller) {
      // Chunk data into pieces of random size between 1 and 32 bytes to stress test the stream handling
      let offset = 0;
      while (offset < data.length) {
        const chunkSize = Math.min(data.length - offset, Math.floor(Math.random() * 32) + 1);
        const chunk = data.subarray(offset, offset + chunkSize);
        controller.enqueue(chunk);
        offset += chunkSize;
      }
      // Signal end of stream
      controller.close();
    },
  });
}

describe("Beast v2 streaming", () => {
  test("should match sync encoding for random types", { timeout: 60_000 }, async () => {
    const result = await fuzzerTest(
      (type: EastType) => {
        const syncEncoder = encodeBeast2For(type);
        const streamEncoder = encodeBeast2ToStreamFor(type);
        return async (value: any) => {
          const syncEncoded = syncEncoder(value);
          const stream = streamEncoder(value);
          const streamEncoded = await streamToUint8Array(stream);

          // Verify byte-for-byte identical
          assert.strictEqual(streamEncoded.length, syncEncoded.length, "Encoded lengths should match");
          for (let i = 0; i < syncEncoded.length; i++) {
            if (syncEncoded[i] !== streamEncoded[i]) {
              throw new Error(`Encoded bytes differ at offset ${i}: sync=${syncEncoded[i]}, stream=${streamEncoded[i]}`);
            }
          }
        };
      },
      50,
      10,
      { includeRecursive: false } // TODO: recursive value generation needs work
    );
    assert.strictEqual(result, true, "Fuzzer test should pass");
  });

  test("should decode sync-encoded data", { timeout: 60_000 }, async () => {
    const result = await fuzzerTest(
      (type: EastType) => {
        const syncEncoder = encodeBeast2For(type);
        const equal = equalFor(type);

        return async (value: any) => {
          // Encode with sync encoder
          const syncEncoded = syncEncoder(value);

          // Convert to stream with random chunking and decode
          const stream = uint8ArrayToStream(syncEncoded);
          const { type: decodeType, value: decodedValue } = await decodeBeast2FromStream(stream);

          // Check type equality
          if (!isTypeValueEqual(decodeType, toEastTypeValue(type))) {
            throw new Error(`Decoding sync-encoded data failed: types not equal`);
          }

          // Check value equality
          if (!equal(decodedValue, value)) {
            throw new Error(`Decoding sync-encoded data failed: values not equal`);
          }
        };
      },
      100, // 100 random types
      50,  // 50 samples per type
      { includeRecursive: false } // TODO: recursive value generation needs work
    );

    assert.strictEqual(result, true, "Fuzz test failed");
  });
});

