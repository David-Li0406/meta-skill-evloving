/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { type EastType, type ValueTypeOf } from "../types.js";
import { isVariant, variant } from "../containers/variant.js";
import { BufferWriter, StreamBufferReader } from "./binary-utils.js";
import { encodeBeast2ValueToBufferFor, MAGIC_BYTES, type Beast2EncodeContext, type Beast2DecodeContext } from "./beast2.js";
import { EastTypeValueType, toEastTypeValue, type EastTypeValue } from "../type_of_type.js";
import { equalFor } from "../comparison.js";
import { printFor } from "./east.js";
import { ref } from "../containers/ref.js";

const printTypeValue = printFor(EastTypeValueType) as (type: EastTypeValue) => string;
const isTypeValueEqual = equalFor(EastTypeValueType) as (t1: EastTypeValue, t2: EastTypeValue) => boolean;

// Chunk size for streaming (64KB - good balance of memory vs throughput)
const CHUNK_SIZE = 64 * 1024;

/**
 * Type-level context for tracking which RecursiveType we're inside during streaming encoding.
 * Array of generator functions with late binding to break circular dependencies.
 */
type Beast2StreamEncodeTypeContext = ((value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => Generator<Uint8Array | void>)[];

/**
 * Type-level context for tracking which RecursiveType we're inside during streaming decoding.
 * Array of decoder functions with late binding to break circular dependencies.
 */
type Beast2StreamDecodeTypeContext = ((reader: StreamBufferReader, ctx?: Beast2DecodeContext) => Promise<any>)[];

/**
 * Determines if a type can be encoded synchronously without needing to yield.
 * Sync types are small and bounded - they can't cause excessive buffer growth.
 */
function isSyncType(type: EastTypeValue): boolean {
  switch (type.type) {
    case "Never":
    case "Null":
    case "Boolean":
    case "Integer":
    case "Float":
    case "DateTime":
      return true;

    case "String":
    case "Blob":
    case "Ref":
    case "Array":
    case "Set":
    case "Dict":
      // These can be large
      return false;

    case "Struct":
      // Sync only if all fields are sync
      return type.value.every(({ type }) => isSyncType(type));

    case "Variant":
      // Sync only if all cases are sync
      return type.value.every(({ type }) => isSyncType(type));

    case "Recursive":
      return false;

    case "Function":
      return true; // Will throw, but no need to yield

    case "AsyncFunction":
      return true; // Will throw, but no need to yield

    default:
      return false;
  }
}

/**
 * Create a generator function that encodes a value to a BufferWriter,
 * yielding chunks when the buffer reaches CHUNK_SIZE.
 *
 * The generator is closure-compiled: the type is analyzed once, and a
 * specialized generator function is returned with pre-allocated buffers
 * and no runtime type checking.
 *
 * @param type The type to encode
 * @returns A generator function: (value, writer) => Generator<Uint8Array | void>
 */
function encodeBeast2ValueToStreamFor(
  type: EastTypeValue,
  typeCtx?: Beast2StreamEncodeTypeContext
): (value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => Generator<Uint8Array | void>
function encodeBeast2ValueToStreamFor<T extends EastType>(
  type: T,
  typeCtx?: Beast2StreamEncodeTypeContext
): (value: ValueTypeOf<T>, writer: BufferWriter, ctx?: Beast2EncodeContext) => Generator<Uint8Array | void>
function encodeBeast2ValueToStreamFor(
  type: EastTypeValue | EastType,
  typeCtx: Beast2StreamEncodeTypeContext = []
): (value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => Generator<Uint8Array | void> {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

  // For fully sync types, use the sync encoder directly
  if (isSyncType(type as EastTypeValue)) {
    const syncEncoder = encodeBeast2ValueToBufferFor(type as EastTypeValue);
    return function* (value: ValueTypeOf<typeof type>, writer: BufferWriter, ctx?: Beast2EncodeContext) {
      syncEncoder(value, writer, ctx);
    };
  }

  // Async types - need generator logic
  if (type.type === "String") {
    return function* (value: string, writer: BufferWriter, _ctx?: Beast2EncodeContext) {
      writer.writeStringUtf8Varint(value);
      if (writer.size >= CHUNK_SIZE) {
        yield writer.pop();
      }
    };
  } else if (type.type === "Blob") {
    return function* (value: Uint8Array, writer: BufferWriter, _ctx?: Beast2EncodeContext) {
      // Write length prefix
      writer.writeVarint(value.length);

      // Check if we should chunk the blob
      if (value.length > CHUNK_SIZE) {
        // Large blob - flush buffer first, then send blob in chunks
        if (writer.size > 0) {
          yield writer.pop();
        }

        let offset = 0;
        while (offset < value.length) {
          const chunkSize = Math.min(CHUNK_SIZE, value.length - offset);
          const chunk = value.subarray(offset, offset + chunkSize);
          writer.writeBytes(chunk);
          yield writer.pop();
          offset += chunkSize;
        }
      } else {
        // Small blob - write it all
        writer.writeBytes(value);
        if (writer.size >= CHUNK_SIZE) {
          yield writer.pop();
        }
      }
    };
  } else if (type.type === "Ref") {
    // Branch on whether value type is sync
    if (isSyncType(type.value)) {
      const syncValueEncoder = encodeBeast2ValueToBufferFor(type.value);
      return function* (value: ref<any>, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) {
        // Check for backreference
        if (ctx.refs.has(value)) {
          const offset = ctx.refs.get(value)!;
          writer.writeVarint(writer.currentOffset - offset);
          return;
        }
        // Write inline marker and register
        writer.writeVarint(0);
        ctx.refs.set(value, writer.currentOffset);

        syncValueEncoder(value.value, writer, ctx);
      };
    } else {
      // Use late binding for async value type
      let valueGen: (value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => Generator<Uint8Array | void>;
      const ret = function* (value: ref<any>, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) {
        // Check for backreference
        if (ctx.refs.has(value)) {
          const offset = ctx.refs.get(value)!;
          writer.writeVarint(writer.currentOffset - offset);
          return;
        }
        // Write inline marker and register
        writer.writeVarint(0);
        ctx.refs.set(value, writer.currentOffset);

        yield* valueGen(value.value, writer, ctx);
      };
      typeCtx.push(ret);
      valueGen = encodeBeast2ValueToStreamFor(type.value, typeCtx);
      typeCtx.pop();

      return ret;
    }
  } else if (type.type === "Array") {
    // Branch on whether value type is sync
    if (isSyncType(type.value)) {
      const syncValueEncoder = encodeBeast2ValueToBufferFor(type.value);
      return function* (value: any[], writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) {
        // Check for backreference
        if (ctx.refs.has(value)) {
          const offset = ctx.refs.get(value)!;
          writer.writeVarint(writer.currentOffset - offset);
          return;
        }
        // Write inline marker and register
        writer.writeVarint(0);
        ctx.refs.set(value, writer.currentOffset);
        // Encode length
        writer.writeVarint(value.length);
        for (const item of value) {
          syncValueEncoder(item, writer, ctx);
          if (writer.size >= CHUNK_SIZE) {
            yield writer.pop();
          }
        }
      };
    } else {
      // Use late binding for async value type
      let valueGen: (value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => Generator<Uint8Array | void>;
      const ret = function* (value: any[], writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) {
        // Check for backreference
        if (ctx.refs.has(value)) {
          const offset = ctx.refs.get(value)!;
          writer.writeVarint(writer.currentOffset - offset);
          return;
        }
        // Write inline marker and register
        writer.writeVarint(0);
        ctx.refs.set(value, writer.currentOffset);
        // Encode length
        writer.writeVarint(value.length);
        for (const item of value) {
          yield* valueGen(item, writer, ctx);
          if (writer.size >= CHUNK_SIZE) {
            yield writer.pop();
          }
        }
      };
      typeCtx.push(ret);
      valueGen = encodeBeast2ValueToStreamFor(type.value, typeCtx);
      typeCtx.pop();
      return ret;
    }
  } else if (type.type === "Set") {
    // Keys are assumed small - always use sync
    const syncKeyEncoder = encodeBeast2ValueToBufferFor(type.value);
    return function* (value: Set<any>, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) {
      // Check for backreference
      if (ctx.refs.has(value)) {
        const offset = ctx.refs.get(value)!;
        writer.writeVarint(writer.currentOffset - offset);
        return;
      }
      // Write inline marker and register
      writer.writeVarint(0);
      ctx.refs.set(value, writer.currentOffset);
      // Encode length
      writer.writeVarint(value.size);
      for (const key of value) {
        syncKeyEncoder(key, writer, ctx);
        if (writer.size >= CHUNK_SIZE) {
          yield writer.pop();
        }
      }
    };
  } else if (type.type === "Dict") {
    // Keys are assumed small - always use sync. Check value type.
    const syncKeyEncoder = encodeBeast2ValueToBufferFor(type.value.key);
    if (isSyncType(type.value.value)) {
      const syncValueEncoder = encodeBeast2ValueToBufferFor(type.value.value);
      return function* (value: Map<any, any>, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) {
        // Check for backreference
        if (ctx.refs.has(value)) {
          const offset = ctx.refs.get(value)!;
          writer.writeVarint(writer.currentOffset - offset);
          return;
        }
        // Write inline marker and register
        writer.writeVarint(0);
        ctx.refs.set(value, writer.currentOffset);
        // Encode length
        writer.writeVarint(value.size);
        for (const [k, v] of value) {
          syncKeyEncoder(k, writer, ctx);
          syncValueEncoder(v, writer, ctx);
          if (writer.size >= CHUNK_SIZE) {
            yield writer.pop();
          }
        }
      };
    } else {
      // Use late binding for async value type
      let valueGen: (value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => Generator<Uint8Array | void>;
      const ret = function* (value: Map<any, any>, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) {
        // Check for backreference
        if (ctx.refs.has(value)) {
          const offset = ctx.refs.get(value)!;
          writer.writeVarint(writer.currentOffset - offset);
          return;
        }
        // Write inline marker and register
        writer.writeVarint(0);
        ctx.refs.set(value, writer.currentOffset);
        // Encode length
        writer.writeVarint(value.size);
        for (const [k, v] of value) {
          syncKeyEncoder(k, writer, ctx);
          yield* valueGen(v, writer, ctx);
          if (writer.size >= CHUNK_SIZE) {
            yield writer.pop();
          }
        }
      };
      typeCtx.push(ret);
      valueGen = encodeBeast2ValueToStreamFor(type.value.value, typeCtx);
      typeCtx.pop();
      return ret;
    }
  } else if (type.type === "Struct") {
    // Annotate each field with sync flag and appropriate encoder
    const fieldInfo: { name: string; isSync: boolean; encoder: (value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => void }[] = [];

    const ret = function* (value: Record<string, any>, writer: BufferWriter, _ctx?: Beast2EncodeContext) {
      // Struct is immutable - no backreference checking needed
      // Encode fields directly
      for (const {name, isSync, encoder} of fieldInfo) {
        if (isSync) {
          (encoder as (v: any, w: BufferWriter, ctx?: Beast2EncodeContext) => void)(value[name], writer);
        } else {
          yield* (encoder as (v: any, w: BufferWriter, ctx?: Beast2EncodeContext) => Generator<Uint8Array | void>)(value[name], writer);
        }
      }
    };

    typeCtx.push(ret);
    for (const { name, type: fieldType } of type.value) fieldInfo.push({
      name,
      isSync: isSyncType(fieldType),
      encoder: isSyncType(fieldType)
        ? encodeBeast2ValueToBufferFor(fieldType)
        : encodeBeast2ValueToStreamFor(fieldType, typeCtx),
    });
    typeCtx.pop();

    return ret;
  } else if (type.type === "Variant") {
    // Annotate each case with sync flag and appropriate encoder
    const caseInfo: Record<string, { tagIndex: number; isSync: boolean; encoder: (value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => void }> = {};

    const ret = function* (value: any, writer: BufferWriter, _ctx?: Beast2EncodeContext) {
      // Variant is immutable - no backreference checking needed
      // Encode tag and value directly
      const tag = value.type as string;
      const {tagIndex, isSync, encoder} = caseInfo[tag]!; // Assume valid input
      writer.writeVarint(tagIndex);
      if (isSync) {
        (encoder as (v: any, w: BufferWriter, ctx?: Beast2EncodeContext) => void)(value.value, writer);
      } else {
        yield* (encoder as (v: any, w: BufferWriter, ctx?: Beast2EncodeContext) => Generator<Uint8Array | void>)(value.value, writer);
      }
    };

    typeCtx.push(ret);
    let i = 0;
    for (const { name, type: caseType } of type.value) {
      caseInfo[name] = {
        tagIndex: i,
        isSync: isSyncType(caseType),
        encoder: isSyncType(caseType)
          ? encodeBeast2ValueToBufferFor(caseType)
          : encodeBeast2ValueToStreamFor(caseType, typeCtx),
      }
      i += 1;
    }
    typeCtx.pop();

    return ret;
  } else if (type.type === "Recursive") {
    // Type stack lookup: index from the end
    const targetEncoder = typeCtx[typeCtx.length - Number(type.value)];
    if (!targetEncoder) {
      throw new Error(`Recursive type depth ${type.value} exceeds type context stack size ${typeCtx.length}`);
    }
    return targetEncoder;
  } else {
    // Should never reach here - all types handled above
    throw new Error(`Unhandled type: ${type.type}`);
  }
}

const typeEncoder = encodeBeast2ValueToBufferFor(EastTypeValueType);

/**
 * Encode an East value to a ReadableStream in Beast v2 format with true backpressure.
 *
 * Uses pull-based control flow: the consumer pulls chunks via ReadableStream.pull(),
 * which drives the generator to produce the next chunk. This provides automatic
 * backpressure without any buffering or queueing.
 *
 * @param type The type of the value to encode
 * @returns A function that takes a value and returns a ReadableStream<Uint8Array>
 */
export function encodeBeast2ToStreamFor(type: EastTypeValue): (value: any) => ReadableStream<Uint8Array>
export function encodeBeast2ToStreamFor<T extends EastType>(type: T): (value: ValueTypeOf<T>) => ReadableStream<Uint8Array>
export function encodeBeast2ToStreamFor(type: EastTypeValue | EastType): (value: any) => ReadableStream<Uint8Array> {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

  const valueGen = encodeBeast2ValueToStreamFor(type as EastTypeValue);

  return (value: any) => {
    let writer: BufferWriter;
    let generator: Generator<Uint8Array | void>;
    let ctx: Beast2EncodeContext;

    return new ReadableStream<Uint8Array>({
      start(controller) {
        // Initialize writer and write header
        writer = new BufferWriter();
        writer.writeBytes(MAGIC_BYTES);

        // Write type schema
        typeEncoder(type, writer, { refs: new Map() });

        // Check if header exceeded chunk size (rare)
        if (writer.size >= CHUNK_SIZE) {
          controller.enqueue(writer.pop());
        }

        // Create context for value encoding
        ctx = { refs: new Map() };

        // Create value generator
        generator = valueGen(value, writer, ctx);
      },

      pull(controller) {
        while (true) {
          const { done, value: chunk } = generator.next();

          if (done) {
            // Flush any remaining data
            if (writer.size > 0) {
              controller.enqueue(writer.pop());
            }
            controller.close();
            return;
          }

          if (chunk !== undefined) {
            controller.enqueue(chunk);
            return; // Backpressure - wait for next pull()
          }

          // chunk is void from yield* delegation - keep looping
        }
      },
    });
  };
}

/**
 * Create a streaming decoder function for a given Beast v2 type.
 * Factory pattern: analyzes type once, returns async decoder.
 */
function decodeBeast2ValueFromStreamFor(type: EastTypeValue, typeCtx: Beast2StreamDecodeTypeContext = []): (reader: StreamBufferReader, ctx?: Beast2DecodeContext) => Promise<any> {
  if (type.type === "Never") {
    return (_reader: StreamBufferReader, _ctx?: Beast2DecodeContext) => { throw new Error(`Cannot decode Never type`); };
  } else if (type.type === "Null") {
    return (_reader: StreamBufferReader, _ctx?: Beast2DecodeContext) => null as unknown as Promise<null>;
  } else if (type.type === "Boolean") {
    return async (reader: StreamBufferReader, _ctx?: Beast2DecodeContext) => {
      const byte = await reader.readByte();
      return byte !== 0;
    };
  } else if (type.type === "Integer") {
    return (reader: StreamBufferReader, _ctx?: Beast2DecodeContext) => reader.readZigzag() as Promise<bigint>;
  } else if (type.type === "Float") {
    return (reader: StreamBufferReader, _ctx?: Beast2DecodeContext) => reader.readFloat64LE() as Promise<number>;
  } else if (type.type === "String") {
    return (reader: StreamBufferReader, _ctx?: Beast2DecodeContext) => reader.readStringUtf8Varint() as Promise<string>;
  } else if (type.type === "DateTime") {
    return (reader: StreamBufferReader, _ctx?: Beast2DecodeContext) => {
      const millis = reader.readZigzag();
      if (millis instanceof Promise) {
        return millis.then(m => new Date(Number(m)));
      }

      return new Date(Number(millis)) as unknown as Promise<Date>;
    };
  } else if (type.type === "Blob") {
    return async (reader: StreamBufferReader, _ctx?: Beast2DecodeContext) => {
      const length = await reader.readVarint();
      const blob = new Uint8Array(length);
      await reader.readBytes(blob);
      return blob;
    };
  } else if (type.type === "Ref") {
    // Use late binding for element decoder
    let elemDecoder: (reader: StreamBufferReader, ctx?: Beast2DecodeContext) => Promise<any>;
    const ret = async (reader: StreamBufferReader, ctx: Beast2DecodeContext = { refs: new Map() }) => {
      const startOffset = reader.position;
      const refOrZero = await reader.readVarint();

      // Check if this is a backreference
      if (refOrZero > 0) {
        const targetOffset = startOffset - refOrZero;
        if (!ctx.refs.has(targetOffset)) {
          throw new Error(`Undefined backreference at offset ${startOffset}, target ${targetOffset}`);
        }
        return ctx.refs.get(targetOffset);
      }

      // Inline ref
      const result: ref<any> = ref(undefined);
      ctx.refs.set(startOffset, result);

      result.value = await elemDecoder(reader, ctx); 
      return result;
    };

    typeCtx.push(ret);
    elemDecoder = decodeBeast2ValueFromStreamFor(type.value, typeCtx);
    typeCtx.pop();

    return ret;
  } else if (type.type === "Array") {
    // Use late binding for element decoder
    let elemDecoder: (reader: StreamBufferReader, ctx?: Beast2DecodeContext) => Promise<any>;
    const ret = async (reader: StreamBufferReader, ctx: Beast2DecodeContext = { refs: new Map() }) => {
      const startOffset = reader.position;
      const refOrZero = await reader.readVarint();

      // Check if this is a backreference
      if (refOrZero > 0) {
        const targetOffset = startOffset - refOrZero;
        if (!ctx.refs.has(targetOffset)) {
          throw new Error(`Undefined backreference at offset ${startOffset}, target ${targetOffset}`);
        }
        return ctx.refs.get(targetOffset);
      }

      // Inline array
      const result: any[] = [];
      ctx.refs.set(startOffset, result);

      const length = await reader.readVarint();
      for (let i = 0; i < length; i++) {
        result.push(await elemDecoder(reader, ctx));
      }
      return result;
    };
    typeCtx.push(ret);
    elemDecoder = decodeBeast2ValueFromStreamFor(type.value, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Set") {
    // Keys are standalone - no need for late binding
    const keyDecoder = decodeBeast2ValueFromStreamFor(type.value, []);
    return async (reader: StreamBufferReader, ctx: Beast2DecodeContext = { refs: new Map() }) => {
      const startOffset = reader.position;
      const refOrZero = await reader.readVarint();

      // Check if this is a backreference
      if (refOrZero > 0) {
        const targetOffset = startOffset - refOrZero;
        if (!ctx.refs.has(targetOffset)) {
          throw new Error(`Undefined backreference at offset ${startOffset}, target ${targetOffset}`);
        }
        return ctx.refs.get(targetOffset);
      }

      // Inline set
      const result = new Set<any>();
      ctx.refs.set(startOffset, result);

      const length = await reader.readVarint();
      for (let i = 0; i < length; i++) {
        result.add(await keyDecoder(reader));
      }
      return result;
    };
  } else if (type.type === "Dict") {
    // Keys are standalone, values use late binding
    const keyDecoder = decodeBeast2ValueFromStreamFor(type.value.key, []);
    let valueDecoder: (reader: StreamBufferReader, ctx?: Beast2DecodeContext) => Promise<any>;
    const ret = async (reader: StreamBufferReader, ctx: Beast2DecodeContext = { refs: new Map() }) => {
      const startOffset = reader.position;
      const refOrZero = await reader.readVarint();

      // Check if this is a backreference
      if (refOrZero > 0) {
        const targetOffset = startOffset - refOrZero;
        if (!ctx.refs.has(targetOffset)) {
          throw new Error(`Undefined backreference at offset ${startOffset}, target ${targetOffset}`);
        }
        return ctx.refs.get(targetOffset);
      }

      // Inline dict
      const result = new Map<any, any>();
      ctx.refs.set(startOffset, result);

      const length = await reader.readVarint();
      for (let i = 0; i < length; i++) {
        const key = await keyDecoder(reader);
        const value = await valueDecoder(reader, ctx);
        result.set(key, value);
      }
      return result;
    };
    typeCtx.push(ret);
    valueDecoder = decodeBeast2ValueFromStreamFor(type.value.value, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Struct") {
    // Struct is immutable - fields use typeCtx for recursive types
    let fieldDecoders: [string, (reader: StreamBufferReader, ctx?: Beast2DecodeContext) => Promise<any>][] = [];

    const ret = async (reader: StreamBufferReader, _ctx?: Beast2DecodeContext) => {
      // Struct is immutable - no backreference checking needed
      const result: Record<string, any> = {};
      for (const [key, decoder] of fieldDecoders) {
        result[key] = await decoder(reader);
      }
      return result;
    };

    typeCtx.push(ret);
    for (const { name, type: fieldType } of type.value) {
      fieldDecoders.push([name, decodeBeast2ValueFromStreamFor(fieldType, typeCtx)] as const)
    };
    typeCtx.pop();

    return ret;
  } else if (type.type === "Variant") {
    // Variant is immutable - cases use typeCtx for recursive types
    let caseDecoders: (readonly [string, (reader: StreamBufferReader, ctx?: Beast2DecodeContext) => Promise<any>])[] = [];

    const ret = async (reader: StreamBufferReader, _ctx?: Beast2DecodeContext) => {
      // Variant is immutable - no backreference checking needed
      const tagIndex = await reader.readVarint();
      if (tagIndex >= caseDecoders.length) {
        throw new Error(`Invalid variant tag ${tagIndex}`);
      }
      const [caseName, caseDecoder] = caseDecoders[tagIndex]!;
      const value = await caseDecoder(reader);
      return variant(caseName, value);
    };

    typeCtx.push(ret);
    for (const { name, type: caseType } of type.value) {
      caseDecoders.push([name, decodeBeast2ValueFromStreamFor(caseType, typeCtx)] as const);
    }
    typeCtx.pop();

    return ret;
  } else if (type.type === "Recursive") {
    // Type stack lookup: index from the end
    const targetDecoder = typeCtx[typeCtx.length - Number(type.value)];
    if (!targetDecoder) {
      throw new Error(`Recursive type depth ${type.value} exceeds type context stack size ${typeCtx.length}`);
    }
    return targetDecoder;
  } else if (type.type === "Function") {
    return (_reader: StreamBufferReader, _ctx?: Beast2DecodeContext) => { throw new Error(`Functions cannot be deserialized`); };
  } else if (type.type === "AsyncFunction") {
    return (_reader: StreamBufferReader, _ctx?: Beast2DecodeContext) => { throw new Error(`AsyncFunctions cannot be deserialized`); };
  } else {
    throw new Error(`Unhandled type ${(type satisfies never as EastTypeValue).type}`);
  }
}

/**
 * Internal helper to decode a value from a stream.
 * Uses the streaming decoder factory with context threading.
 */
async function decodeBeast2ValueFromStream(
  type: EastTypeValue,
  reader: StreamBufferReader
): Promise<any> {
  const decoder = decodeBeast2ValueFromStreamFor(type);
  const ctx: Beast2DecodeContext = { refs: new Map() };
  return await decoder(reader, ctx);
}

const streamingTypeDecode = decodeBeast2ValueFromStreamFor(EastTypeValueType);

/**
 * Decode a Beast v2 format stream to an East value.
 * Reads the type schema from the stream and returns both type and value.
 *
 * @param stream The input stream to decode
 * @returns Promise resolving to { type, value }
 */
export async function decodeBeast2FromStream(
  stream: ReadableStream<Uint8Array>
): Promise<{ type: EastTypeValue; value: any }> {
  const reader = new StreamBufferReader(stream);

  try {
    // Verify magic bytes
    for (let i = 0; i < MAGIC_BYTES.length; i++) {
      const byte = await reader.readByte();
      if (byte !== MAGIC_BYTES[i]) {
        throw new Error(
          `Invalid Beast v2 magic bytes at offset ${i}: expected 0x${MAGIC_BYTES[i]!.toString(16)}, got 0x${byte.toString(16)}`
        );
      }
    }

    // Decode type schema directly from stream
    const type = await streamingTypeDecode(reader, { refs: new Map() });

    // Decode value
    const value = await decodeBeast2ValueFromStream(type, reader);

    return { type, value };
  } finally {
    await reader.release();
  }
}

/**
 * Create a streaming decoder for a specific Beast v2 type.
 * Factory pattern: the type is verified once, returns async decoder.
 *
 * @param type The expected type to decode
 * @returns A function that takes a stream and returns a Promise of the decoded value
 */
export function decodeBeast2FromStreamFor<T extends EastTypeValue>(
  type: T
): (stream: ReadableStream<Uint8Array>) => Promise<ValueTypeOf<T>> {
  const valueDecoder = decodeBeast2ValueFromStreamFor(type);

  return async (stream: ReadableStream<Uint8Array>) => {
    const reader = new StreamBufferReader(stream);

    try {
      // Verify magic bytes
      for (let i = 0; i < MAGIC_BYTES.length; i++) {
        const byte = await reader.readByte();
        if (byte !== MAGIC_BYTES[i]) {
          throw new Error(
            `Invalid Beast v2 magic bytes at offset ${i}: expected 0x${MAGIC_BYTES[i]!.toString(16)}, got 0x${byte.toString(16)}`
          );
        }
      }

      // Decode type schema directly from stream
      const decodedType = await streamingTypeDecode(reader, { refs: new Map() });

      // Verify type matches expected type
      if (!isTypeValueEqual(decodedType, type)) {
        throw new Error(`Type mismatch: expected ${printTypeValue(type)}, got ${printTypeValue(decodedType)}`);
      }

      // Decode value with context
      const ctx: Beast2DecodeContext = { refs: new Map() };
      const value = await valueDecoder(reader, ctx);

      return value as ValueTypeOf<T>;
    } finally {
      await reader.release();
    }
  };
}
