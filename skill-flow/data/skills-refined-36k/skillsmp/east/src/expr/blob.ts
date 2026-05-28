/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { get_location } from "../location.js";
import { ArrayType, IntegerType, StringType, type BlobType, type EastType, type StructType } from "../types.js";
import { valueOrExprToAstTyped } from "./ast.js";
import { AstSymbol, Expr, FactorySymbol, type ToExpr } from "./expr.js";
import type { IntegerExpr } from "./integer.js";
import type { StringExpr } from "./string.js";
import type { ExprType } from "./types.js";
import type { BooleanExpr } from "./boolean.js";
import { equal, notEqual } from "./block.js";
import { CsvParseConfigType, csvParseOptionsToValue, type CsvParseOptions } from "../serialization/csv.js";
import type { ArrayExpr } from "./array.js";

/**
 * Expression representing binary blob values and operations.
 *
 * BlobExpr provides methods for working with binary data including size queries,
 * byte access, text encoding/decoding (UTF-8, UTF-16), and BEAST binary format operations.
 * Blobs are immutable sequences of bytes.
 *
 * @example
 * ```ts
 * // Encoding and decoding text
 * const encodeText = East.function([StringType], BlobType, ($, text) => {
 *   $.return(text.encodeUtf8());
 * });
 *
 * const decodeText = East.function([BlobType], StringType, ($, blob) => {
 *   $.return(blob.decodeUtf8());
 * });
 *
 * // Working with blob bytes
 * const getByte = East.function([BlobType, IntegerType], IntegerType, ($, blob, offset) => {
 *   $.return(blob.getUint8(offset));
 * });
 * ```
 */
export class BlobExpr extends Expr<BlobType> {
  constructor(ast: AST, createExpr: ToExpr) {
    super(ast.type as BlobType, ast, createExpr);
  }
  
  /**
   * Returns the size of the blob in bytes.
   *
   * @returns An IntegerExpr representing the number of bytes
   *
   * @example
   * ```ts
   * const getSize = East.function([BlobType], IntegerType, ($, blob) => {
   *   $.return(blob.size());
   * });
   * const compiled = East.compile(getSize.toIR(), []);
   * const text = "hello";
   * const blob = new TextEncoder().encode(text);
   * compiled(blob);  // 5n (5 bytes for "hello")
   * ```
   */
  size(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "BlobSize",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }
  
  /**
   * Gets the byte value at the specified offset.
   *
   * @param offset - The zero-based byte offset to read from
   * @returns An IntegerExpr representing the unsigned 8-bit integer (0-255) at that offset
   *
   * @throws East runtime error if the offset is out of bounds (< 0 or >= blob size)
   *
   * @example
   * ```ts
   * const getByte = East.function([BlobType, IntegerType], IntegerType, ($, blob, offset) => {
   *   $.return(blob.getUint8(offset));
   * });
   * const compiled = East.compile(getByte.toIR(), []);
   * const blob = new Uint8Array([72, 101, 108, 108, 111]); // "Hello"
   * compiled(blob, 0n);  // 72n (ASCII 'H')
   * compiled(blob, 1n);  // 101n (ASCII 'e')
   * // compiled(blob, 10n) would throw error (out of bounds)
   * ```
   */
  getUint8(offset: IntegerExpr | bigint): IntegerExpr {
    const offsetAst = valueOrExprToAstTyped(offset, IntegerType);
    
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "BlobGetUint8",
      type_parameters: [],
      arguments: [this[AstSymbol], offsetAst],
    }) as any;
  }

  /**
   * Decodes the blob as UTF-8 text, returning a string.
   *
   * @returns A StringExpr containing the decoded text
   *
   * @throws East runtime error if the blob contains invalid UTF-8 sequences
   *
   * @remarks UTF-8 is a superset of ASCII. No byte-order mark (BOM) is expected.
   *
   * @example
   * ```ts
   * const decode = East.function([BlobType], StringType, ($, blob) => {
   *   $.return(blob.decodeUtf8());
   * });
   * const compiled = East.compile(decode.toIR(), []);
   * const blob = new TextEncoder().encode("hello");
   * compiled(blob);  // "hello"
   *
   * const emojiBlob = new TextEncoder().encode("😀");
   * compiled(emojiBlob);  // "😀"
   * ```
   */
  decodeUtf8(): StringExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: StringType,
      location: get_location(),
      builtin: "BlobDecodeUtf8",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as StringExpr;
  }

  /**
   * Decodes the blob as UTF-16 text, returning a string.
   *
   * @returns A StringExpr containing the decoded text
   *
   * @throws East runtime error if the blob contains invalid UTF-16 sequences
   *
   * @remarks UTF-16 is common on Windows. If no byte-order mark (BOM) is present, assumes little-endian.
   *
   * @example
   * ```ts
   * const decode = East.function([BlobType], StringType, ($, blob) => {
   *   $.return(blob.decodeUtf16());
   * });
   * const compiled = East.compile(decode.toIR(), []);
   * // Assume blob contains UTF-16 LE encoded "hello" with BOM
   * const blob = new Uint8Array([0xFF, 0xFE, 0x68, 0x00, 0x65, 0x00, 0x6C, 0x00, 0x6C, 0x00, 0x6F, 0x00]);
   * compiled(blob);  // "hello"
   * ```
   */
  decodeUtf16(): StringExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: StringType,
      location: get_location(),
      builtin: "BlobDecodeUtf16",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as StringExpr;
  }

  /**
   * Decodes a value from East's binary format (BEAST).
   *
   * @param type - The expected East type of the decoded value
   * @param version - The BEAST format version ('v1' or 'v2', default 'v1')
   * @returns An expression of the specified type containing the decoded value
   *
   * @throws East runtime error if the blob does not contain a valid BEAST encoding of the specified type
   *
   * @example
   * ```ts
   * const decode = East.function([BlobType], ArrayType(IntegerType), ($, blob) => {
   *   $.return(blob.decodeBeast(ArrayType(IntegerType), 'v2'));
   * });
   * const compiled = East.compile(decode.toIR(), []);
   * // Assume blob contains BEAST v2 encoding of [1n, 2n, 3n]
   * const encodedBlob = // ... BEAST encoded data ... ;
   * compiled(encodedBlob);  // [1n, 2n, 3n]
   * ```
   */
  decodeBeast<T extends EastType>(type: T, version: 'v1' | 'v2' = 'v1'): ExprType<T> {
    if (version === 'v1') {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type,
        location: get_location(),
        builtin: "BlobDecodeBeast",
        type_parameters: [type],
        arguments: [this[AstSymbol]],
      }) as ExprType<T>;
    } else if (version === 'v2') {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type,
        location: get_location(),
        builtin: "BlobDecodeBeast2",
        type_parameters: [type],
        arguments: [this[AstSymbol]],
      }) as ExprType<T>;
    } else {
      throw new Error(`Unsupported Beast version: ${version}`);
    }
  }

  /**
   * Decodes the blob as CSV data into an array of structs.
   *
   * @param structType - The struct type for each row
   * @param options - CSV parsing options
   * @returns An ArrayExpr containing the decoded structs
   *
   * @throws East runtime error if the CSV is malformed or doesn't match the struct type
   *
   * @example
   * ```ts
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   *
   * const parseCsv = East.function([BlobType], ArrayType(PersonType), ($, blob) => {
   *   $.return(blob.decodeCsv(PersonType, { delimiter: ',' }));
   * });
   * const compiled = East.compile(parseCsv.toIR(), []);
   * const csv = new TextEncoder().encode("name,age\nAlice,30\nBob,25");
   * compiled(csv);  // [{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }]
   * ```
   */
  decodeCsv<T extends StructType>(structType: T, options?: CsvParseOptions): ArrayExpr<T> {
    // Convert options to East config value
    const configValue = csvParseOptionsToValue(options);
    const configAst = valueOrExprToAstTyped(configValue, CsvParseConfigType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: ArrayType(structType),
      location: get_location(),
      builtin: "BlobDecodeCsv",
      type_parameters: [structType, CsvParseConfigType],
      arguments: [this[AstSymbol], configAst],
    }) as ArrayExpr<T>;
  }

  /**
   * Checks if this blob equals another blob (byte-by-byte comparison).
   *
   * @param other - The blob to compare against
   * @returns A BooleanExpr that is true if the blobs are identical
   *
   * @example
   * ```ts
   * const isEqual = East.function([BlobType, BlobType], BooleanType, ($, a, b) => {
   *   $.return(a.equals(b));
   * });
   * const compiled = East.compile(isEqual.toIR(), []);
   * const blob1 = new Uint8Array([1, 2, 3]);
   * const blob2 = new Uint8Array([1, 2, 3]);
   * const blob3 = new Uint8Array([1, 2, 4]);
   * compiled(blob1, blob2);  // true
   * compiled(blob1, blob3);  // false
   * ```
   */
  equals(other: BlobExpr | Uint8Array): BooleanExpr {
    return equal(this, other);
  }

  /**
   * Checks if this blob does not equal another blob.
   *
   * @param other - The blob to compare against
   * @returns A BooleanExpr that is true if the blobs are different
   *
   * @example
   * ```ts
   * const isNotEqual = East.function([BlobType, BlobType], BooleanType, ($, a, b) => {
   *   $.return(a.notEquals(b));
   * });
   * const compiled = East.compile(isNotEqual.toIR(), []);
   * const blob1 = new Uint8Array([1, 2, 3]);
   * const blob2 = new Uint8Array([1, 2, 4]);
   * compiled(blob1, blob2);  // true
   * compiled(blob1, blob1);  // false
   * ```
   */
  notEquals(other: BlobExpr | Uint8Array): BooleanExpr {
    return notEqual(this, other);
  }

  // ============================================================================
  // Aliases for comparison operations
  // ============================================================================

  /** Alias for {@link equals} */
  eq = this.equals;
  /** Alias for {@link equals} */
  equal = this.equals;

  /** Alias for {@link notEquals} */
  ne = this.notEquals;
  /** Alias for {@link notEquals} */
  notEqual = this.notEquals;
}
