/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import type { EastType, ValueTypeOf } from "../types.js";
import {
  BufferWriter,
  readInt64Twiddled,
  readFloat64Twiddled,
  readStringUtf8Null,
} from "./binary-utils.js";
import { isVariant, variant } from "../containers/variant.js";
import { EastTypeValueType, toEastTypeValue, type EastTypeValue } from "../type_of_type.js";
import { printFor } from "./east.js";
import { equalFor } from "../comparison.js";

const printTypeValue = printFor(EastTypeValueType) as (type: EastTypeValue) => string;
const isTypeValueEqual = equalFor(EastTypeValueType) as (t1: EastTypeValue, t2: EastTypeValue) => boolean;


// =============================================================================
// Beast v1 Type encoding/decoding (different from beast2!)
// =============================================================================
//
// NULLABLE TYPE HANDLING:
//
// Old East supported nullable types with a special flag (bit 7 set in type byte).
// New East removed nullable in favor of explicit Option/Variant types.
//
// DECODING: We auto-convert nullable types to Option<T> (Variant<{none: Null, some: T}>)
//   - This allows reading legacy .beast files seamlessly
//   - Tag mapping: tag 0 = none (null), tag 1 = some (has value)
//   - This matches the old nullable encoding for values (byte-for-byte identical)
//
// ENCODING: We currently do NOT auto-convert Option<T> back to nullable
//   - Pro: Simpler, more explicit, no magic behavior
//   - Con: Type schemas are larger (expanded Variant vs single nullable flag)
//   - Con: Old ELARACore cannot read files written by new East
//
// =============================================================================

// Beast v1 uses single-byte type tags (0-13) with nullable flag at bit 7
export const BEAST_TYPE_TO_BYTE = {
  Array: 0,
  Blob: 1,
  Boolean: 2,
  DateTime: 3,
  Dict: 4,
  Float: 5,
  Integer: 6,
  // Node: 7,  // Not implemented in this version
  Null: 8,
  Set: 9,
  String: 10,
  Struct: 11,
  // Tree: 12,  // Not implemented in this version
  Variant: 13,
} as const;

export const BEAST_BYTE_TO_TYPE = [
  "Array", "Blob", "Boolean", "DateTime", "Dict", "Float", "Integer",
  undefined, // 7 - Node (not implemented)
  "Null", "Set", "String", "Struct",
  undefined, // 12 - Tree (not implemented)
  "Variant",
] as const;

/**
 * Normalize a Beast-decoded type to standard East ordering.
 * Sorts variant cases alphabetically by name, matching East's canonical type representation.
 * Only used for type comparison in Beast decoding - the original ordering is preserved
 * for value decoding (to match byte layout).
 */
function _normalizeBeastType(type: EastTypeValue): EastTypeValue {
  const t = type.type;

  if (t === "Array") {
    return variant("Array", _normalizeBeastType(type.value));
  } else if (t === "Set") {
    return variant("Set", _normalizeBeastType(type.value));
  } else if (t === "Dict") {
    return variant("Dict", {
      key: _normalizeBeastType(type.value.key),
      value: _normalizeBeastType(type.value.value),
    });
  } else if (t === "Struct") {
    // Struct fields preserve declaration order (not sorted), only normalize field types
    return variant("Struct", type.value.map(f => ({
      name: f.name,
      type: _normalizeBeastType(f.type),
    })));
  } else if (t === "Variant") {
    // Sort cases by name and normalize their types
    const sortedCases = [...type.value].sort((a, b) => a.name < b.name ? -1 : a.name > b.name ? 1 : 0);
    return variant("Variant", sortedCases.map(c => ({
      name: c.name,
      type: _normalizeBeastType(c.type),
    })));
  }

  // Primitives pass through unchanged
  return type;
}

export function encodeTypeToBeastBuffer(type: EastTypeValue, writer: BufferWriter): void {
  const t = type.type;

  // NOTE: We don't currently detect Variant<{notNull: T, null: Null}> and convert it
  // back to the old nullable encoding. This means type schemas are larger than necessary
  // but encoding is simpler and more explicit. See comments at top of file for trade-offs.

  if (t === "Recursive") {
    throw new Error("TODO");
  }

  const typeByte = BEAST_TYPE_TO_BYTE[t as keyof typeof BEAST_TYPE_TO_BYTE];
  if (typeByte === undefined) {
    throw new Error(`Unsupported type for Beast v1: ${t}`);
  }

  writer.writeUint8(typeByte);

  if (t === "Array") {
    encodeTypeToBeastBuffer(type.value, writer);
  } else if (t === "Set") {
    encodeTypeToBeastBuffer(type.value, writer);
  } else if (t === "Dict") {
    encodeTypeToBeastBuffer(type.value.key, writer);
    encodeTypeToBeastBuffer(type.value.value, writer);
  } else if (t === "Struct") {
    for (const { name: fieldName, type: fieldType} of type.value) {
      writer.writeUint8(1); // continuation byte
      writer.writeStringUtf8Null(fieldName);
      encodeTypeToBeastBuffer(fieldType, writer);
    }
    writer.writeUint8(0); // terminator
  } else if (t === "Variant") {
    for (const { name: caseName, type: caseType } of type.value) {
      writer.writeUint8(1); // continuation byte
      writer.writeStringUtf8Null(caseName);
      encodeTypeToBeastBuffer(caseType, writer);
    }
    writer.writeUint8(0); // terminator
  }
}

export function decodeTypeBeast(buffer: Uint8Array, offset: number): [EastTypeValue, number] {
  const typeByte = buffer[offset]!;
  offset += 1;

  // Check for nullable flag (bit 7)
  // In old East, nullable types were encoded with bit 7 set
  // We convert these to Variant types with cases "notNull" (tag 0) and "null" (tag 1)
  // which matches the old encoding where tag 0 = has value, tag 1 = null
  const nullable = typeByte >= 128;
  const actualTypeByte = nullable ? typeByte - 128 : typeByte;

  const t = BEAST_BYTE_TO_TYPE[actualTypeByte];
  if (!t) {
    throw new Error(`Invalid type byte 0x${typeByte.toString(16).padStart(2, '0')} at offset ${offset - 1}`);
  }

  // Decode the base type
  let baseType: EastTypeValue;

  if (t === "Null") {
    baseType = variant("Null", null);
  } else if (t === "Boolean") {
    baseType = variant("Boolean", null);
  } else if (t === "Integer") {
    baseType = variant("Integer", null);
  } else if (t === "Float") {
    baseType = variant("Float", null);
  } else if (t === "DateTime") {
    baseType = variant("DateTime", null);
  } else if (t === "String") {
    baseType = variant("String", null);
  } else if (t === "Blob") {
    baseType = variant("Blob", null);
  } else if (t === "Array") {
    const [elementType, newOffset] = decodeTypeBeast(buffer, offset);
    offset = newOffset;
    baseType = variant("Array", elementType);
  } else if (t === "Set") {
    const [keyType, newOffset] = decodeTypeBeast(buffer, offset);
    offset = newOffset;
    baseType = variant("Set", keyType);
  } else if (t === "Dict") {
    const [keyType, keyOffset] = decodeTypeBeast(buffer, offset);
    const [valueType, valueOffset] = decodeTypeBeast(buffer, keyOffset);
    offset = valueOffset;
    baseType = variant("Dict", { key: keyType, value: valueType });
  } else if (t === "Struct") {
    const fields: { name: string, type: EastTypeValue }[] = [];
    while (buffer[offset] === 1) {
      offset += 1;
      const [fieldName, nameOffset] = readStringUtf8Null(buffer, offset);
      const [fieldType, typeOffset] = decodeTypeBeast(buffer, nameOffset);
      fields.push({ name: fieldName, type: fieldType });
      offset = typeOffset;
    }
    if (buffer[offset] !== 0) {
      throw new Error(`Unexpected struct field separator ${buffer[offset]} at offset ${offset}`);
    }
    offset += 1;
    baseType = variant("Struct", fields);
  } else if (t === "Variant") {
    const cases: { name: string, type: EastTypeValue }[] = [];
    while (buffer[offset] === 1) {
      offset += 1;
      const [caseName, nameOffset] = readStringUtf8Null(buffer, offset);
      const [caseType, typeOffset] = decodeTypeBeast(buffer, nameOffset);
      cases.push({ name: caseName, type: caseType });
      offset = typeOffset;
    }
    if (buffer[offset] !== 0) {
      throw new Error(`Unexpected variant case separator ${buffer[offset]} at offset ${offset}`);
    }
    offset += 1;
    baseType = variant("Variant", cases);
  } else {
    throw new Error(`Unhandled type: ${t}`);
  }

  // If nullable, wrap in a Variant with "some" (tag 0) and "none" (tag 1)
  // Old nullable: tag 0 = has value, tag 1 = null
  // So we need: index 0 = some, index 1 = none (to match byte encoding)
  if (nullable) {
    return [variant("Variant", [ { name: "some", type: baseType }, { name: "none", type: variant("Null", null) } ]), offset];
  }

  return [baseType, offset];
}

// =============================================================================
// Value encoding/decoding factories (closure-compiler pattern)
// =============================================================================

export function encodeBeastValueToBufferFor(type: EastTypeValue): (value: any, writer: BufferWriter) => void {
  if (type.type === "Never") {
    return (_: unknown, _writer: BufferWriter) => { throw new Error(`Cannot encode Never type`)};
  } else if (type.type === "Null") {
    return (_: null, _writer: BufferWriter) => { /* null encodes as nothing */ };
  } else if (type.type === "Boolean") {
    return (x: boolean, writer: BufferWriter) => writer.writeUint8(x ? 1 : 0);
  } else if (type.type === "Integer") {
    return (x: bigint, writer: BufferWriter) => writer.writeInt64Twiddled(x);
  } else if (type.type === "Float") {
    return (x: number, writer: BufferWriter) => writer.writeFloat64Twiddled(x);
  } else if (type.type === "String") {
    return (x: string, writer: BufferWriter) => writer.writeStringUtf8Null(x);
  } else if (type.type === "DateTime") {
    return (x: Date, writer: BufferWriter) => writer.writeInt64Twiddled(BigInt(x.valueOf()));
  } else if (type.type === "Blob") {
    // Preallocate length buffer (reused across calls)
    const lengthBytes = new Uint8Array(8);
    const lengthView = new DataView(lengthBytes.buffer);
    return (x: Uint8Array, writer: BufferWriter) => {
      // Old format: 8-byte big-endian length + raw bytes
      lengthView.setBigUint64(0, BigInt(x.length), false); // big-endian
      writer.writeBytes(lengthBytes);
      writer.writeBytes(x);
    };
  } else if (type.type === "Ref") {
    throw new Error(`Beast v1 format does not support ref types`);
  } else if (type.type === "Array") {
    const valueEncoder = encodeBeastValueToBufferFor(type.value);
    return (x: any[], writer: BufferWriter) => {
      // Old format: continuation bytes (0x01 before each element, 0x00 at end)
      for (const item of x) {
        writer.writeUint8(1); // continuation byte
        valueEncoder(item, writer);
      }
      writer.writeUint8(0); // end marker
    };
  } else if (type.type === "Set") {
    const keyEncoder = encodeBeastValueToBufferFor(type.value);
    return (x: Set<any>, writer: BufferWriter) => {
      // Old format: continuation bytes (0x01 before each element, 0x00 at end)
      for (const key of x) {
        writer.writeUint8(1); // continuation byte
        keyEncoder(key, writer);
      }
      writer.writeUint8(0); // end marker
    };
  } else if (type.type === "Dict") {
    const keyEncoder = encodeBeastValueToBufferFor(type.value.key);
    const valueEncoder = encodeBeastValueToBufferFor(type.value.value);
    return (x: Map<any, any>, writer: BufferWriter) => {
      // Old format: continuation bytes (0x01 before each entry, 0x00 at end)
      for (const [k, v] of x) {
        writer.writeUint8(1); // continuation byte
        keyEncoder(k, writer);
        valueEncoder(v, writer);
      }
      writer.writeUint8(0); // end marker
    };
  } else if (type.type === "Struct") {
    const fieldEncoders = type.value.map(({ name, type }) => [name, encodeBeastValueToBufferFor(type)] as const);
    return (x: Record<string, any>, writer: BufferWriter) => {
      for (const [k, encoder] of fieldEncoders) {
        encoder(x[k], writer);
      }
    };
  } else if (type.type === "Variant") {
    const caseEncoders = Object.fromEntries(type.value.map(({ name, type }) => [name, encodeBeastValueToBufferFor(type)])) as Record<string, (value: any, writer: BufferWriter) => void>;
    const caseTags = Object.fromEntries(type.value.map(({ name }, i) => [name, i]));
    return (x: any, writer: BufferWriter) => {
      const tag = x.type as string;
      const tagIndex = caseTags[tag]!; // Assume valid input
      writer.writeUint8(tagIndex);
      caseEncoders[tag]!(x.value, writer);
    };
  } else if (type.type === "Recursive") {
    throw new Error(`Beast v1 format does not support recursive types`);
  } else if (type.type === "Function") {
    throw new Error(`Functions cannot be serialized`);
  } else if (type.type === "AsyncFunction") {
    throw new Error(`AsyncFunctions cannot be serialized`);
  } else {
    throw new Error(`Unhandled type ${(type satisfies never as EastType).type}`);
  }
}

export function decodeBeastValueFor(type: EastTypeValue): (buffer: Uint8Array, offset: number) => [any, number]
export function decodeBeastValueFor<T extends EastType>(type: T): (buffer: Uint8Array, offset: number) => [ValueTypeOf<T>, number]
export function decodeBeastValueFor(type: EastTypeValue | EastType): (buffer: Uint8Array, offset: number) => [any, number] {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

  if (type.type === "Never") {
    return (_buffer: Uint8Array, _offset: number) => { throw new Error(`Cannot decode Never type`)};
  } else if (type.type === "Null") {
    return (_buffer: Uint8Array, offset: number) => [null, offset];
  } else if (type.type === "Boolean") {
    return (buffer: Uint8Array, offset: number) => {
      if (offset >= buffer.length) {
        throw new Error(`Buffer underflow reading boolean at offset ${offset}`);
      }
      return [buffer[offset] !== 0, offset + 1];
    };
  } else if (type.type === "Integer") {
    return (buffer: Uint8Array, offset: number) => {
      const view = new DataView(buffer.buffer, buffer.byteOffset, buffer.byteLength);
      return readInt64Twiddled(view, offset);
    };
  } else if (type.type === "Float") {
    return (buffer: Uint8Array, offset: number) => {
      const view = new DataView(buffer.buffer, buffer.byteOffset, buffer.byteLength);
      const value = readFloat64Twiddled(view, offset);
      return [value, offset + 8];
    };
  } else if (type.type === "String") {
    return (buffer: Uint8Array, offset: number) => readStringUtf8Null(buffer, offset);
  } else if (type.type === "DateTime") {
    return (buffer: Uint8Array, offset: number) => {
      const view = new DataView(buffer.buffer, buffer.byteOffset, buffer.byteLength);
      const [unixTime, newOffset] = readInt64Twiddled(view, offset);
      return [new Date(Number(unixTime)), newOffset];
    };
  } else if (type.type === "Blob") {
    return (buffer: Uint8Array, offset: number) => {
      if (offset + 8 > buffer.length) {
        throw new Error(`Buffer underflow reading blob length at offset ${offset}`);
      }
      const view = new DataView(buffer.buffer, buffer.byteOffset, buffer.byteLength);
      const length = Number(view.getBigUint64(offset, false)); // big-endian
      const newOffset = offset + 8;
      if (newOffset + length > buffer.length) {
        throw new Error(`Buffer underflow reading blob data at offset ${newOffset}, length ${length}`);
      }
      const blob = buffer.slice(newOffset, newOffset + length);
      return [blob, newOffset + length];
    };
  } else if (type.type === "Ref") {
    throw new Error("Beast v1 format does not support ref types");;
  } else if (type.type === "Array") {
    const valueDecoder = decodeBeastValueFor(type.value);
    return (buffer: Uint8Array, offset: number) => {
      const result: any[] = [];
      while (true) {
        if (offset >= buffer.length) {
          throw new Error(`Buffer underflow reading array continuation byte at offset ${offset}`);
        }
        const continuationByte = buffer[offset++];
        if (continuationByte === 0) {
          break; // end of array
        } else if (continuationByte === 1) {
          const [value, newOffset] = valueDecoder(buffer, offset);
          result.push(value);
          offset = newOffset;
        } else {
          throw new Error(`Invalid continuation byte ${continuationByte} at offset ${offset - 1}`);
        }
      }
      return [result, offset];
    };
  } else if (type.type === "Set") {
    const keyDecoder = decodeBeastValueFor(type.value);
    return (buffer: Uint8Array, offset: number) => {
      const result = new Set<any>();
      while (true) {
        if (offset >= buffer.length) {
          throw new Error(`Buffer underflow reading set continuation byte at offset ${offset}`);
        }
        const continuationByte = buffer[offset++];
        if (continuationByte === 0) {
          break; // end of set
        } else if (continuationByte === 1) {
          const [key, newOffset] = keyDecoder(buffer, offset);
          result.add(key);
          offset = newOffset;
        } else {
          throw new Error(`Invalid continuation byte ${continuationByte} at offset ${offset - 1}`);
        }
      }
      return [result, offset];
    };
  } else if (type.type === "Dict") {
    const keyDecoder = decodeBeastValueFor(type.value.key);
    const valueDecoder = decodeBeastValueFor(type.value.value);
    return (buffer: Uint8Array, offset: number) => {
      const result = new Map<any, any>();
      while (true) {
        if (offset >= buffer.length) {
          throw new Error(`Buffer underflow reading dict continuation byte at offset ${offset}`);
        }
        const continuationByte = buffer[offset++];
        if (continuationByte === 0) {
          break; // end of dict
        } else if (continuationByte === 1) {
          const [key, keyOffset] = keyDecoder(buffer, offset);
          const [value, valueOffset] = valueDecoder(buffer, keyOffset);
          result.set(key, value);
          offset = valueOffset;
        } else {
          throw new Error(`Invalid continuation byte ${continuationByte} at offset ${offset - 1}`);
        }
      }
      return [result, offset];
    };
  } else if (type.type === "Struct") {
    const fieldDecoders = type.value.map(({ name, type }) => [name, decodeBeastValueFor(type)] as const);
    return (buffer: Uint8Array, offset: number) => {
      const result: Record<string, any> = {};
      let currentOffset = offset;
      for (const [k, decoder] of fieldDecoders) {
        const [value, nextOffset] = decoder(buffer, currentOffset);
        result[k] = value;
        currentOffset = nextOffset;
      }
      return [result, currentOffset];
    };
  } else if (type.type === "Variant") {
    const caseDecoders = type.value.map(({ name, type }) => [name, decodeBeastValueFor(type)] as const);
    return (buffer: Uint8Array, offset: number) => {
      if (offset >= buffer.length) {
        throw new Error(`Buffer underflow reading variant tag at offset ${offset}`);
      }
      const tagIndex = buffer[offset++]!;
      if (tagIndex >= caseDecoders.length) {
        throw new Error(`Invalid variant tag ${tagIndex} at offset ${offset - 1}`);
      }
      const [caseName, caseDecoder] = caseDecoders[tagIndex]!;
      const [value, finalOffset] = caseDecoder(buffer, offset);
      return [variant(caseName, value), finalOffset];
    };
  } else if (type.type === "Recursive") {
    throw new Error("Beast v1 format does not support recursive types");;
  } else if (type.type === "Function") {
    throw new Error(`Functions cannot be deserialized`);
  } else if (type.type === "AsyncFunction") {
    throw new Error(`AsyncFunctions cannot be deserialized`);
  } else {
    throw new Error(`Unhandled type ${(type satisfies never as EastType).type}`);
  }
}

// =============================================================================
// High-level API
// =============================================================================

// Header-free encoding (raw value only)
export function encodeBeastValueFor(type: EastTypeValue): (value: any) => Uint8Array
export function encodeBeastValueFor<T extends EastType>(type: T): (value: ValueTypeOf<T>) => Uint8Array
export function encodeBeastValueFor(type: EastTypeValue | EastType): (value: any) => Uint8Array {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

  const encoder = encodeBeastValueToBufferFor(type as EastTypeValue);
  return (value: ValueTypeOf<typeof type>): Uint8Array => {
    const writer = new BufferWriter();
    encoder(value, writer);
    return writer.toUint8Array();
  };
}

export const MAGIC_BYTES = Uint8Array.from([69, 97, 115, 116, 0, 234, 87, 255]);
 
// Beast v1 format with header (magic bytes + type schema + value)
export function encodeBeastFor(type: EastTypeValue): (value: any) => Uint8Array
export function encodeBeastFor<T extends EastType>(type: T): (value: ValueTypeOf<T>) => Uint8Array
export function encodeBeastFor(type: EastTypeValue | EastType): (value: any) => Uint8Array{
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

  const valueEncoder = encodeBeastValueToBufferFor(type as EastTypeValue);

  return (value: any) => {
    const writer = new BufferWriter();

    // Write magic bytes (8 bytes)
    writer.writeBytes(MAGIC_BYTES);

    // Write type schema (using beast v1 type encoding)
    encodeTypeToBeastBuffer(type as EastTypeValue, writer);

    // Write value (using beast v1 encoding)
    valueEncoder(value, writer);

    return writer.toUint8Array();
  };
}

export function decodeBeast(data: Uint8Array): { type: EastTypeValue; value: any } {
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
  const [type, typeEndOffset] = decodeTypeBeast(data, offset);

  // Decode value
  const valueDecoder = decodeBeastValueFor(type);
  const [value, valueEndOffset] = valueDecoder(data, typeEndOffset);

  // Verify we consumed all data
  if (valueEndOffset !== data.length) {
    throw new Error(`Unexpected data after Beast value at offset ${valueEndOffset} (${data.length - valueEndOffset} bytes remaining)`);
  }

  return { type, value };
}

export function decodeBeastFor(type: EastTypeValue): (data: Uint8Array) => any
export function decodeBeastFor<T extends EastType>(type: T): (data: Uint8Array) => ValueTypeOf<T>
export function decodeBeastFor(type: EastTypeValue | EastType): (data: Uint8Array) => any {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

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
    const [decodedType, typeEndOffset] = decodeTypeBeast(data, offset);

    // Normalize decoded type for comparison (sorts variant cases)
    // but keep original for value decoding (preserves byte-level tag ordering)
    const normalizedType = _normalizeBeastType(decodedType);

    // Verify type matches expected type
    if (!isTypeValueEqual(normalizedType, type as EastTypeValue)) {
      throw new Error(`Type mismatch: expected ${printTypeValue(type as EastTypeValue)}, got ${printTypeValue(normalizedType)}`);
    }

    // Decode value using original decoded_type (correct tag ordering)
    const valueDecoder = decodeBeastValueFor(decodedType);
    const [value, valueEndOffset] = valueDecoder(data, typeEndOffset);

    // Verify we consumed all data
    if (valueEndOffset !== data.length) {
      throw new Error(`Unexpected data after Beast value at offset ${valueEndOffset} (${data.length - valueEndOffset} bytes remaining)`);
    }

    return value;
  };
}