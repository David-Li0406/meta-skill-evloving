/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { equalFor } from "../comparison.js";
import { EastTypeValueType, toEastTypeValue, type EastTypeValue } from "../type_of_type.js";
import type { EastType, ValueTypeOf } from "../types.js";
import { isVariant, variant } from "../containers/variant.js";
import {
  BufferWriter,
  readVarint,
  readZigzag,
  readFloat64LE,
  readStringUtf8Varint,
} from "./binary-utils.js";
import { printFor } from "./east.js";
import { ref } from "../containers/ref.js";
import { EAST_IR_SYMBOL, EAST_CAPTURES_SYMBOL, compile_internal, type RuntimeContext } from "../compile.js";
import { InternalError } from "../error.js";
import { IRType, type FunctionIR, type AsyncFunctionIR } from "../ir.js";
import type { PlatformFunction } from "../platform.js";
import { analyzeIR } from "../analyze.js";

const printTypeValue = printFor(EastTypeValueType) as (type: EastTypeValue) => string;
const isTypeValueEqual = equalFor(EastTypeValueType) as (t1: EastTypeValue, t2: EastTypeValue) => boolean;

// =============================================================================
// Context types for backreference tracking
// =============================================================================

/** Stack of encoders for recursive types */
export type Beast2EncodeTypeContext = ((value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => void)[];

/**
 * Value-level context for tracking mutable aliases during encoding.
 *
 * - refs: Map from mutable containers (Array/Set/Dict) to their byte offset (where inline content begins, after varint(0))
 */
export type Beast2EncodeContext = {
  refs: Map<any, number>;
};

/** Stack of decoders for recursive types */
export type Beast2DecodeTypeContext = ((buffer: Uint8Array, offset: number, ctx?: Beast2DecodeContext) => [any, number])[];

/**
 * Value-level context for tracking mutable aliases during decoding.
 *
 * - refs: Map from byte offset to deserialized mutable container (Array/Set/Dict)
 */
export type Beast2DecodeContext = {
  refs: Map<number, any>;
};

/**
 * Options for decoding, allowing function compilation.
 * When platform is provided, decoded functions will be compiled to callables with IR attached.
 * When not provided, raw FunctionIR/AsyncFunctionIR is returned.
 */
export type Beast2DecodeOptions = {
  platform?: PlatformFunction[];
};

// =============================================================================
// Value encoding/decoding factories (closure-compiler pattern)
// =============================================================================

export function encodeBeast2ValueToBufferFor(type: EastTypeValue, typeCtx: Beast2EncodeTypeContext = []): (value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => void {
  if (type.type === "Never") {
    return (_: unknown, _writer: BufferWriter, _ctx?: Beast2EncodeContext) => { throw new Error(`Attempted to encode value of type .Never`)};
  } else if (type.type === "Null") {
    return (_: null, _writer: BufferWriter, _ctx?: Beast2EncodeContext) => { /* null encodes as nothing */ };
  } else if (type.type === "Boolean") {
    return (x: boolean, writer: BufferWriter, _ctx?: Beast2EncodeContext) => writer.writeUint8(x ? 1 : 0);
  } else if (type.type === "Integer") {
    return (x: bigint, writer: BufferWriter, _ctx?: Beast2EncodeContext) => writer.writeZigzag(x);
  } else if (type.type === "Float") {
    return (x: number, writer: BufferWriter, _ctx?: Beast2EncodeContext) => writer.writeFloat64LE(x);
  } else if (type.type === "String") {
    return (x: string, writer: BufferWriter, _ctx?: Beast2EncodeContext) => writer.writeStringUtf8Varint(x);
  } else if (type.type === "DateTime") {
    return (x: Date, writer: BufferWriter, _ctx?: Beast2EncodeContext) => writer.writeZigzag(BigInt(x.valueOf()));
  } else if (type.type === "Blob") {
    return (x: Uint8Array, writer: BufferWriter, _ctx?: Beast2EncodeContext) => {
      writer.writeVarint(x.length);
      writer.writeBytes(x);
    };
  } else if (type.type === "Ref") {
    let valueEncoder: (value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => void;
    const ret = (x: ref<any>, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) => {
      // Check for backreference
      if (ctx.refs.has(x)) {
        const offset = ctx.refs.get(x)!;
        writer.writeVarint(writer.currentOffset - offset);
        return;
      }
      // Write inline marker and register
      writer.writeVarint(0);
      ctx.refs.set(x, writer.currentOffset);
      // Encode contents
      valueEncoder(x.value, writer, ctx);
    };
    typeCtx.push(ret);
    valueEncoder = encodeBeast2ValueToBufferFor(type.value, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Array") {
    let valueEncoder: (value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => void;
    const ret = (x: any[], writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) => {
      // Check for backreference
      if (ctx.refs.has(x)) {
        const offset = ctx.refs.get(x)!;
        writer.writeVarint(writer.currentOffset - offset);
        return;
      }
      // Write inline marker and register
      writer.writeVarint(0);
      ctx.refs.set(x, writer.currentOffset);
      // Encode contents
      writer.writeVarint(x.length);
      for (const item of x) {
        valueEncoder(item, writer, ctx);
      }
    };
    typeCtx.push(ret);
    valueEncoder = encodeBeast2ValueToBufferFor(type.value, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Set") {
    const keyEncoder = encodeBeast2ValueToBufferFor(type.value, typeCtx);
    return (x: Set<any>, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) => {
      // Check for backreference
      if (ctx.refs.has(x)) {
        const offset = ctx.refs.get(x)!;
        writer.writeVarint(writer.currentOffset - offset);
        return;
      }
      // Write inline marker and register
      writer.writeVarint(0);
      ctx.refs.set(x, writer.currentOffset);
      // Encode contents
      writer.writeVarint(x.size);
      for (const key of x) {
        keyEncoder(key, writer, ctx);
      }
    };
  } else if (type.type === "Dict") {
    const keyEncoder = encodeBeast2ValueToBufferFor(type.value.key, typeCtx);
    let valueEncoder: (value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => void;
    const ret = (x: Map<any, any>, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) => {
      // Check for backreference
      if (ctx.refs.has(x)) {
        const offset = ctx.refs.get(x)!;
        writer.writeVarint(writer.currentOffset - offset);
        return;
      }
      // Write inline marker and register
      writer.writeVarint(0);
      ctx.refs.set(x, writer.currentOffset);
      // Encode contents
      writer.writeVarint(x.size);
      for (const [k, v] of x) {
        keyEncoder(k, writer, ctx);
        valueEncoder(v, writer, ctx);
      }
    };
    typeCtx.push(ret);
    valueEncoder = encodeBeast2ValueToBufferFor(type.value.value, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Struct") {
    const fieldEncoders: [string, (value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => void][] = [];
    const ret = (x: Record<string, any>, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) => {
      // Encode fields
      for (const [k, encoder] of fieldEncoders) {
        encoder(x[k], writer, ctx);
      }
    };
    typeCtx.push(ret);
    for (const { name, type: fieldType } of type.value) {
      fieldEncoders.push([name, encodeBeast2ValueToBufferFor(fieldType, typeCtx)]);
    }
    typeCtx.pop();
    return ret;
  } else if (type.type === "Variant") {
    const caseEncoders: Record<string, (value: any, writer: BufferWriter, ctx?: Beast2EncodeContext) => void> = {};
    const caseTags = Object.fromEntries(type.value.map(({ name }, i) => [name, i]));
    const ret = (x: any, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) => {
      // Encode tag and value
      const tag = x.type as string;
      const tagIndex = caseTags[tag]!; // Assume valid input
      writer.writeVarint(tagIndex);
      caseEncoders[tag]!(x.value, writer, ctx);
    };
    typeCtx.push(ret);
    for (const { name, type: caseType } of type.value) {
      caseEncoders[name] = encodeBeast2ValueToBufferFor(caseType, typeCtx);
    }
    typeCtx.pop();
    return ret;
  } else if (type.type === "Recursive") {
    const ret = typeCtx[typeCtx.length - Number(type.value)];
    if (ret === undefined) {
      throw new Error(`Internal error: Recursive type context not found`);
    }
    return ret;
  } else if (type.type === "Function") {
    return (value: any, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) => {
      // Get IR from function
      const ir = value[EAST_IR_SYMBOL] as FunctionIR | undefined;

      if (!ir) {
        throw new Error(
          `Cannot serialize function: no IR attached. ` +
          `Functions must be compiled from East IR to be serializable.`
        );
      }

      // Serialize the IR
      irEncoder(ir, writer, ctx);

      // Serialize capture values
      const captures = value[EAST_CAPTURES_SYMBOL] as RuntimeContext | undefined;
      const captureCount = ir.value.captures.length;

      // Write number of captures
      writer.writeVarint(captureCount);

      // Serialize each capture value using its type from the IR
      for (const captureVar of ir.value.captures) {
        const name = captureVar.value.name;
        const captureType = captureVar.value.type;

        // Captured variables are stored as variants - extract the value
        if (!captures) {
          throw new InternalError(`Function has captures in IR but no EAST_CAPTURES_SYMBOL`);
        }
        const captureEntry = captures[name];
        if (!captureEntry) {
          throw new InternalError(`Capture '${name}' not found in function's capture context`);
        }
        const captureValue = captureEntry.value;

        // Get encoder for this capture's type and encode the value
        const captureEncoder = encodeBeast2ValueToBufferFor(captureType, typeCtx);
        captureEncoder(captureValue, writer, ctx);
      }
    };
  } else if (type.type === "AsyncFunction") {
    return (value: any, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) => {
      // Get IR from function
      const ir = value[EAST_IR_SYMBOL] as AsyncFunctionIR | undefined;

      if (!ir) {
        throw new Error(
          `Cannot serialize async function: no IR attached. ` +
          `Functions must be compiled from East IR to be serializable.`
        );
      }

      // Serialize the IR
      irEncoder(ir, writer, ctx);

      // Serialize capture values
      const captures = value[EAST_CAPTURES_SYMBOL] as RuntimeContext | undefined;
      const captureCount = ir.value.captures.length;

      // Write number of captures
      writer.writeVarint(captureCount);

      // Serialize each capture value using its type from the IR
      for (const captureVar of ir.value.captures) {
        const name = captureVar.value.name;
        const captureType = captureVar.value.type;

        // Captured variables are stored as variants - extract the value
        if (!captures) {
          throw new InternalError(`AsyncFunction has captures in IR but no EAST_CAPTURES_SYMBOL`);
        }
        const captureEntry = captures[name];
        if (!captureEntry) {
          throw new InternalError(`Capture '${name}' not found in async function's capture context`);
        }
        const captureValue = captureEntry.value;

        // Get encoder for this capture's type and encode the value
        const captureEncoder = encodeBeast2ValueToBufferFor(captureType, typeCtx);
        captureEncoder(captureValue, writer, ctx);
      }
    };
  } else {
    throw new Error(`Unhandled type ${(type satisfies never as EastTypeValue).type}`);
  }
}

export function decodeBeast2ValueFor(type: EastTypeValue | EastType, typeCtx: Beast2DecodeTypeContext = [], options?: Beast2DecodeOptions): (buffer: Uint8Array, offset: number, ctx?: Beast2DecodeContext) => [any, number] {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

  if (type.type === "Never") {
    return (_buffer: Uint8Array, _offset: number, _ctx?: Beast2DecodeContext) => { throw new Error(`Attempted to decode value of type .Never`)};
  } else if (type.type === "Null") {
    return (_buffer: Uint8Array, offset: number, _ctx?: Beast2DecodeContext) => [null, offset];
  } else if (type.type === "Boolean") {
    return (buffer: Uint8Array, offset: number, _ctx?: Beast2DecodeContext) => {
      if (offset >= buffer.length) {
        throw new Error(`Buffer underflow reading boolean at offset ${offset}`);
      }
      return [buffer[offset] !== 0, offset + 1];
    };
  } else if (type.type === "Integer") {
    return (buffer: Uint8Array, offset: number, _ctx?: Beast2DecodeContext) => readZigzag(buffer, offset);
  } else if (type.type === "Float") {
    return (buffer: Uint8Array, offset: number, _ctx?: Beast2DecodeContext) => {
      const view = new DataView(buffer.buffer, buffer.byteOffset, buffer.byteLength);
      const value = readFloat64LE(view, offset);
      return [value, offset + 8];
    };
  } else if (type.type === "String") {
    return (buffer: Uint8Array, offset: number, _ctx?: Beast2DecodeContext) => readStringUtf8Varint(buffer, offset);
  } else if (type.type === "DateTime") {
    return (buffer: Uint8Array, offset: number, _ctx?: Beast2DecodeContext) => {
      const [millis, newOffset] = readZigzag(buffer, offset);
      return [new Date(Number(millis)), newOffset];
    };
  } else if (type.type === "Blob") {
    return (buffer: Uint8Array, offset: number, _ctx?: Beast2DecodeContext) => {
      const [length, newOffset] = readVarint(buffer, offset);
      if (newOffset + length > buffer.length) {
        throw new Error(`Buffer underflow reading blob at offset ${offset}, length ${length}`);
      }
      const blob = buffer.slice(newOffset, newOffset + length);
      return [blob, newOffset + length];
    };
  } else if (type.type === "Ref") {
    let valueDecoder: (buffer: Uint8Array, offset: number, ctx?: Beast2DecodeContext) => [any, number];
    const ret = (buffer: Uint8Array, offset: number, ctx: Beast2DecodeContext = { refs: new Map() }): [any, number] => {
      const [refOrLength, newOffset] = readVarint(buffer, offset);
      // Check if this is a backreference
      if (refOrLength > 0) {
        const targetOffset = offset - refOrLength;
        if (!ctx.refs.has(targetOffset)) {
          throw new Error(`Undefined backreference at offset ${offset}, target ${targetOffset}`);
        }
        return [ctx.refs.get(targetOffset), newOffset];
      }
      // Inline ref
      const result: ref<any> = ref(undefined);
      ctx.refs.set(newOffset, result);
      const [value, nextOffset] = valueDecoder(buffer, newOffset, ctx);
      result.value = value;
      return [result, nextOffset];
    };
    typeCtx.push(ret);
    valueDecoder = decodeBeast2ValueFor(type.value, typeCtx, options);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Array") {
    let valueDecoder: (buffer: Uint8Array, offset: number, ctx?: Beast2DecodeContext) => [any, number];
    const ret = (buffer: Uint8Array, offset: number, ctx: Beast2DecodeContext = { refs: new Map() }): [any, number] => {
      const [refOrLength, newOffset] = readVarint(buffer, offset);
      // Check if this is a backreference
      if (refOrLength > 0) {
        const targetOffset = offset - refOrLength;
        if (!ctx.refs.has(targetOffset)) {
          throw new Error(`Undefined backreference at offset ${offset}, target ${targetOffset}`);
        }
        return [ctx.refs.get(targetOffset), newOffset];
      }
      // Inline array
      const result: any[] = [];
      ctx.refs.set(newOffset, result);
      const [length, lengthOffset] = readVarint(buffer, newOffset);
      let currentOffset = lengthOffset;
      for (let i = 0; i < length; i++) {
        const [value, nextOffset] = valueDecoder(buffer, currentOffset, ctx);
        result.push(value);
        currentOffset = nextOffset;
      }
      return [result, currentOffset];
    };
    typeCtx.push(ret);
    valueDecoder = decodeBeast2ValueFor(type.value, typeCtx, options);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Set") {
    const keyDecoder = decodeBeast2ValueFor(type.value, typeCtx, options);
    return (buffer: Uint8Array, offset: number, ctx: Beast2DecodeContext = { refs: new Map() }) => {
      const [refOrLength, newOffset] = readVarint(buffer, offset);
      // Check if this is a backreference
      if (refOrLength > 0) {
        const targetOffset = offset - refOrLength;
        if (!ctx.refs.has(targetOffset)) {
          throw new Error(`Undefined backreference at offset ${offset}, target ${targetOffset}`);
        }
        return [ctx.refs.get(targetOffset), newOffset];
      }
      // Inline set
      const result = new Set<any>();
      ctx.refs.set(newOffset, result);
      const [length, lengthOffset] = readVarint(buffer, newOffset);
      let currentOffset = lengthOffset;
      for (let i = 0; i < length; i++) {
        const [key, nextOffset] = keyDecoder(buffer, currentOffset, ctx);
        result.add(key);
        currentOffset = nextOffset;
      }
      return [result, currentOffset];
    };
  } else if (type.type === "Dict") {
    const keyDecoder = decodeBeast2ValueFor(type.value.key, typeCtx, options);
    let valueDecoder: (buffer: Uint8Array, offset: number, ctx?: Beast2DecodeContext) => [any, number];
    const ret = (buffer: Uint8Array, offset: number, ctx: Beast2DecodeContext = { refs: new Map() }): [any, number] => {
      const [refOrLength, newOffset] = readVarint(buffer, offset);
      // Check if this is a backreference
      if (refOrLength > 0) {
        const targetOffset = offset - refOrLength;
        if (!ctx.refs.has(targetOffset)) {
          throw new Error(`Undefined backreference at offset ${offset}, target ${targetOffset}`);
        }
        return [ctx.refs.get(targetOffset), newOffset];
      }
      // Inline dict
      const result = new Map<any, any>();
      ctx.refs.set(newOffset, result);
      const [length, lengthOffset] = readVarint(buffer, newOffset);
      let currentOffset = lengthOffset;
      for (let i = 0; i < length; i++) {
        const [key, keyOffset] = keyDecoder(buffer, currentOffset, ctx);
        const [value, valueOffset] = valueDecoder(buffer, keyOffset, ctx);
        result.set(key, value);
        currentOffset = valueOffset;
      }
      return [result, currentOffset];
    };
    typeCtx.push(ret);
    valueDecoder = decodeBeast2ValueFor(type.value.value, typeCtx, options);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Struct") {
    const fieldDecoders: [string, (buffer: Uint8Array, offset: number, ctx?: Beast2DecodeContext) => [any, number]][] = [];
    const ret = (buffer: Uint8Array, offset: number, ctx: Beast2DecodeContext = { refs: new Map() }): [any, number] => {
      // Decode struct fields
      const result: Record<string, any> = {};
      let currentOffset = offset;
      for (const [k, decoder] of fieldDecoders) {
        const [value, nextOffset] = decoder(buffer, currentOffset, ctx);
        result[k] = value;
        currentOffset = nextOffset;
      }
      return [result, currentOffset];
    };
    typeCtx.push(ret);
    for (const { name, type: fieldType } of type.value) {
      fieldDecoders.push([name, decodeBeast2ValueFor(fieldType, typeCtx, options)]);
    }
    typeCtx.pop();
    return ret;
  } else if (type.type === "Variant") {
    const caseDecoders: [string, (buffer: Uint8Array, offset: number, ctx?: Beast2DecodeContext) => [any, number]][] = [];
    const ret = (buffer: Uint8Array, offset: number, ctx: Beast2DecodeContext = { refs: new Map() }): [any, number] => {
      // Decode variant
      const [tagIndex, tagOffset] = readVarint(buffer, offset);
      if (tagIndex >= caseDecoders.length) {
        throw new Error(`Invalid variant tag ${tagIndex} at offset ${offset}`);
      }
      const [caseName, caseDecoder] = caseDecoders[tagIndex]!;
      const v = variant(caseName, undefined as any);
      const [value, finalOffset] = caseDecoder(buffer, tagOffset, ctx);
      (v as any).value = value;
      return [v, finalOffset];
    };
    typeCtx.push(ret);
    for (const { name, type: caseType } of type.value) {
      caseDecoders.push([name, decodeBeast2ValueFor(caseType, typeCtx, options)]);
    }
    typeCtx.pop();
    return ret;
  } else if (type.type === "Recursive") {
    const ret = typeCtx[typeCtx.length - Number(type.value)];
    if (ret === undefined) {
      throw new Error(`Internal error: Recursive type context not found`);
    }
    return ret;
  } else if (type.type === "Function") {
    // Convert platform to internal format
    const platform = options?.platform ?? [];
    const platformFns = Object.fromEntries(platform.map(fn => [fn.name, fn.fn]));
    const asyncPlatformFns = new Set(platform.filter(fn => fn.type === 'async').map(fn => fn.name));

    return (buffer: Uint8Array, offset: number, ctx: Beast2DecodeContext = { refs: new Map() }): [any, number] => {
      // Decode the IR
      const [ir, newOffset] = irDecoder(buffer, offset, ctx);
      let currentOffset = newOffset;

      // Validate it's a FunctionIR
      if (ir.type !== "Function") {
        throw new Error(
          `Expected Function IR, got ${ir.type} at offset ${offset}`
        );
      }

      // Decode capture count
      const [captureCount, offsetAfterCount] = readVarint(buffer, currentOffset);
      currentOffset = offsetAfterCount;

      if (captureCount !== ir.value.captures.length) {
        throw new Error(
          `Capture count mismatch: IR has ${ir.value.captures.length} captures, ` +
          `but serialized data has ${captureCount}`
        );
      }

      // Decode capture values
      const captureContext: RuntimeContext = {};
      for (const captureVar of ir.value.captures) {
        const name = captureVar.value.name;
        const captureType = captureVar.value.type;

        // Get decoder for this capture's type and decode the value
        const captureDecoder = decodeBeast2ValueFor(captureType, typeCtx, options);
        const [captureValue, nextOffset] = captureDecoder(buffer, currentOffset, ctx);
        currentOffset = nextOffset;

        // Wrap captures in appropriate variants
        captureContext[name] = captureVar.value.mutable
          ? variant("boxed", captureValue)
          : variant("value", captureValue);
      }

      // Build variable context from captures for analyzeIR
      const variableContext: Record<string, { type: EastTypeValue; mutable: boolean; definedBy: any; captured: boolean }> = {};
      for (const captureVar of ir.value.captures) {
        variableContext[captureVar.value.name] = {
          type: captureVar.value.type,
          mutable: captureVar.value.mutable,
          definedBy: captureVar,
          captured: true  // Already captured from outer scope
        };
      }

      // Build type context for compile_internal
      const typeContext: Record<string, EastTypeValue> = {};
      for (const captureVar of ir.value.captures) {
        typeContext[captureVar.value.name] = captureVar.value.type;
      }

      // Analyze and compile the function with capture context
      let fn: any;
      try {
        const analyzedIR = analyzeIR(ir, platform, variableContext);
        const compiled = compile_internal(analyzedIR, typeContext, platformFns, asyncPlatformFns, platform, true, new Set());
        fn = compiled(captureContext);
      } catch (e: unknown) {
        throw new Error(`Failed to compile decoded function: ${(e as Error).message}`);
      }

      return [fn, currentOffset];
    };
  } else if (type.type === "AsyncFunction") {
    // Convert platform to internal format
    const platform = options?.platform ?? [];
    const platformFns = Object.fromEntries(platform.map(fn => [fn.name, fn.fn]));
    const asyncPlatformFns = new Set(platform.filter(fn => fn.type === 'async').map(fn => fn.name));

    return (buffer: Uint8Array, offset: number, ctx: Beast2DecodeContext = { refs: new Map() }): [any, number] => {
      // Decode the IR
      const [ir, newOffset] = irDecoder(buffer, offset, ctx);
      let currentOffset = newOffset;

      // Validate it's an AsyncFunctionIR
      if (ir.type !== "AsyncFunction") {
        throw new Error(
          `Expected AsyncFunction IR, got ${ir.type} at offset ${offset}`
        );
      }

      // Decode capture count
      const [captureCount, offsetAfterCount] = readVarint(buffer, currentOffset);
      currentOffset = offsetAfterCount;

      if (captureCount !== ir.value.captures.length) {
        throw new Error(
          `Capture count mismatch: IR has ${ir.value.captures.length} captures, ` +
          `but serialized data has ${captureCount}`
        );
      }

      // Decode capture values
      const captureContext: RuntimeContext = {};
      for (const captureVar of ir.value.captures) {
        const name = captureVar.value.name;
        const captureType = captureVar.value.type;

        // Get decoder for this capture's type and decode the value
        const captureDecoder = decodeBeast2ValueFor(captureType, typeCtx, options);
        const [captureValue, nextOffset] = captureDecoder(buffer, currentOffset, ctx);
        currentOffset = nextOffset;

        // Wrap captures in appropriate variants
        captureContext[name] = captureVar.value.mutable
          ? variant("boxed", captureValue)
          : variant("value", captureValue);
      }

      // Build variable context from captures for analyzeIR
      const variableContext: Record<string, { type: EastTypeValue; mutable: boolean; definedBy: any; captured: boolean }> = {};
      for (const captureVar of ir.value.captures) {
        variableContext[captureVar.value.name] = {
          type: captureVar.value.type,
          mutable: captureVar.value.mutable,
          definedBy: captureVar,
          captured: true  // Already captured from outer scope
        };
      }

      // Build type context for compile_internal
      const typeContext: Record<string, EastTypeValue> = {};
      for (const captureVar of ir.value.captures) {
        typeContext[captureVar.value.name] = captureVar.value.type;
      }

      // Analyze and compile the function with capture context
      let fn: any;
      try {
        const analyzedIR = analyzeIR(ir, platform, variableContext);
        const compiled = compile_internal(analyzedIR, typeContext, platformFns, asyncPlatformFns, platform, true, new Set());
        fn = compiled(captureContext);
      } catch (e: unknown) {
        throw new Error(`Failed to compile decoded async function: ${(e as Error).message}`);
      }

      return [fn, currentOffset];
    };
  } else {
    throw new Error(`Unhandled type ${(type satisfies never as EastTypeValue).type}`);
  }
}

// =============================================================================
// High-level API (header-free encoding)
// =============================================================================

export function encodeBeast2ValueFor(type: EastTypeValue): (value: any) => Uint8Array
export function encodeBeast2ValueFor<T extends EastType>(type: T): (value: ValueTypeOf<T>) => Uint8Array
export function encodeBeast2ValueFor(type: EastTypeValue | EastType): (value: any) => Uint8Array {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

  const encoder = encodeBeast2ValueToBufferFor(type as EastTypeValue);
  return (value: any): Uint8Array => {
    const writer = new BufferWriter();
    const ctx: Beast2EncodeContext = { refs: new Map() };
    encoder(value, writer, ctx);
    return writer.toUint8Array();
  };
}

// =============================================================================
// Beast format (Minimal header with self-describing type)
// =============================================================================

// Magic bytes for Beast format
// 0x89       - Invalid UTF-8 marker (like PNG)
// 0x45 0x61 0x73 0x74 - "East" (human-readable in hex dumps)
// 0x0D 0x0A  - CRLF (detects line-ending corruption)
// 0x01       - Version byte (currently 1)
export const MAGIC_BYTES = new Uint8Array([0x89, 0x45, 0x61, 0x73, 0x74, 0x0D, 0x0A, 0x01]);
const typeEncoder = encodeBeast2ValueToBufferFor(EastTypeValueType);
const typeDecoder = decodeBeast2ValueFor(EastTypeValueType);

// IR encoder/decoder for function serialization
const IRTypeValue = toEastTypeValue(IRType);
const irEncoder = encodeBeast2ValueToBufferFor(IRTypeValue);
const irDecoder = decodeBeast2ValueFor(IRTypeValue);

export function encodeBeast2For(type: EastTypeValue): (value: any) => Uint8Array
export function encodeBeast2For<T extends EastType>(type: T): (value: ValueTypeOf<T>) => Uint8Array
export function encodeBeast2For(type: EastTypeValue | EastType): (value: any) => Uint8Array {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
      type = toEastTypeValue(type);
  }

  const valueEncoder = encodeBeast2ValueToBufferFor(type as EastTypeValue);

  return (value: any) => {
    const writer = new BufferWriter();

    // Write magic bytes (8 bytes)
    writer.writeBytes(MAGIC_BYTES);

    // Write type schema
    typeEncoder(type, writer, { refs: new Map() });

    // Write value
    const ctx: Beast2EncodeContext = { refs: new Map() };
    valueEncoder(value, writer, ctx);

    return writer.toUint8Array();
  };
}

export function decodeBeast2(data: Uint8Array): { type: EastTypeValue; value: any } {
  // Verify magic bytes
  if (data.length < MAGIC_BYTES.length) {
    throw new Error(`Data too short for Beast format: ${data.length} bytes`);
  }

  for (let i = 0; i < MAGIC_BYTES.length; i++) {
    if (data[i] !== MAGIC_BYTES[i]) {
      throw new Error(`Invalid Beast magic bytes at offset ${i}: expected 0x${MAGIC_BYTES[i]!.toString(16)}, got 0x${data[i]!.toString(16)}`);
    }
  }

  // Decode type schema
  let offset = MAGIC_BYTES.length;
  const [type, typeEndOffset] = typeDecoder(data, offset);
  if (type.type === "Set") console.log(type);

  // Decode value
  const valueDecoder = decodeBeast2ValueFor(type);
  const ctx: Beast2DecodeContext = { refs: new Map() };
  const [value, valueEndOffset] = valueDecoder(data, typeEndOffset, ctx);

  // Verify we consumed all data
  if (valueEndOffset !== data.length) {
    throw new Error(`Unexpected data after Beast value at offset ${valueEndOffset} (${data.length - valueEndOffset} bytes remaining)`);
  }

  return { type, value };
}

export function decodeBeast2For(type: EastTypeValue, options?: Beast2DecodeOptions): (data: Uint8Array) => any
export function decodeBeast2For<T extends EastType>(type: T, options?: Beast2DecodeOptions): (data: Uint8Array) => ValueTypeOf<T>
export function decodeBeast2For(type: EastTypeValue | EastType, options?: Beast2DecodeOptions): (data: Uint8Array) => any {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
      type = toEastTypeValue(type);
  }

  const valueDecoder = decodeBeast2ValueFor(type as EastTypeValue, [], options);

  return (data: Uint8Array) => {
    // Verify magic bytes
    if (data.length < MAGIC_BYTES.length) {
      throw new Error(`Data too short for Beast format: ${data.length} bytes`);
    }

    for (let i = 0; i < MAGIC_BYTES.length; i++) {
      if (data[i] !== MAGIC_BYTES[i]) {
        throw new Error(`Invalid Beast magic bytes at offset ${i}: expected 0x${MAGIC_BYTES[i]!.toString(16)}, got 0x${data[i]!.toString(16)}`);
      }
    }

    // Decode type schema
    let offset = MAGIC_BYTES.length;
    const [decodedType, typeEndOffset] = typeDecoder(data, offset);

    // Verify type matches expected type
    if (!isTypeValueEqual(decodedType, type as EastTypeValue)) {
      throw new Error(`Type mismatch: expected ${printTypeValue(type as EastTypeValue)}, got ${printTypeValue(decodedType)}`);
    }

    // Decode value
    const ctx: Beast2DecodeContext = { refs: new Map() };
    const [value, valueEndOffset] = valueDecoder(data, typeEndOffset, ctx);

    // Verify we consumed all data
    if (valueEndOffset !== data.length) {
      throw new Error(`Unexpected data after Beast value at offset ${valueEndOffset} (${data.length - valueEndOffset} bytes remaining)`);
    }

    return value;
  };
}

// =============================================================================
// Function serialization helpers
// =============================================================================

// Re-export for convenience
export { EAST_IR_SYMBOL, EAST_CAPTURES_SYMBOL } from "../compile.js";

import { EastIR, AsyncEastIR } from "../eastir.js";

/**
 * Compile a deserialized FunctionIR to an executable function.
 *
 * @param ir - The FunctionIR returned from BEAST2 deserialization
 * @param platform - Platform functions required for execution
 * @returns Compiled JavaScript function
 *
 * @example
 * ```ts
 * const funcType = FunctionType([IntegerType], IntegerType);
 * const data = encodeBeast2For(funcType)(myCompiledFunc);
 * const ir = decodeBeast2For(funcType)(data);
 * const recompiled = compileFunctionIR(ir, []);
 * const result = recompiled(42n);
 * ```
 */
export function compileFunctionIR<I extends any[], O>(
  ir: FunctionIR,
  platform: PlatformFunction[]
): (...args: I) => O {
  return new EastIR(ir).compile(platform) as (...args: I) => O;
}

/**
 * Compile a deserialized AsyncFunctionIR to an executable async function.
 *
 * @param ir - The AsyncFunctionIR returned from BEAST2 deserialization
 * @param platform - Platform functions required for execution
 * @returns Compiled JavaScript async function
 */
export function compileAsyncFunctionIR<I extends any[], O>(
  ir: AsyncFunctionIR,
  platform: PlatformFunction[]
): (...args: I) => Promise<O> {
  return new AsyncEastIR(ir).compile(platform) as (...args: I) => Promise<O>;
}
