/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { get_location } from "../../location.js";
import { BlobType } from "../../types.js";
import type { BlobExpr } from "../blob.js";
import { Expr } from "../expr.js";

/** Standard library for blobs */
export default {
  /**
   * Encodes a value to the binary East format (BEAST).
   *
   * @param value - The East value to encode
   * @param version - The BEAST format version to use: `'v1'` or `'v2'` (default: `'v1'`)
   * @returns A blob expression containing the encoded binary data
   *
   * @throws Error when an unsupported version string is provided
   *
   * @remarks
   * BEAST (Binary East) is a compact binary serialization format for East values.
   * Version 1 (v1) is the original format, while version 2 (v2) provides improved
   * encoding for certain types.
   *
   * @example
   * ```ts
   * // Encode an array to BEAST v1 format
   * const encodeArray = East.function([ArrayType(IntegerType)], BlobType, ($, arr) => {
   *   $.return(East.Blob.encodeBeast(arr));
   * });
   * const compiled = East.compile(encodeArray.toIR(), []);
   * const blob = compiled([1n, 2n, 3n]);  // Binary blob containing encoded array
   * ```
   *
   * @example
   * ```ts
   * // Encode using BEAST v2 format
   * const encodeV2 = East.function([IntegerType], BlobType, ($, num) => {
   *   $.return(East.Blob.encodeBeast(num, 'v2'));
   * });
   * const compiled = East.compile(encodeV2.toIR(), []);
   * const blob = compiled(42n);  // Binary blob with v2 encoding
   * ```
   */
  encodeBeast(value: Expr, version: 'v1' | 'v2' = 'v1'): BlobExpr {
    if (version === 'v1') {
      return Expr.fromAst({
        ast_type: "Builtin",
        type: BlobType,
        location: get_location(),
        builtin: "BlobEncodeBeast",
        type_parameters: [Expr.type(value)],
        arguments: [Expr.ast(value)],
      }) as BlobExpr;
    } else if (version === 'v2') {
      return Expr.fromAst({
        ast_type: "Builtin",
        type: BlobType,
        location: get_location(),
        builtin: "BlobEncodeBeast2",
        type_parameters: [Expr.type(value)],
        arguments: [Expr.ast(value)],
      }) as BlobExpr;
    } else {
      throw new Error(`Unsupported Beast version: ${version}`);
    }
  }
}