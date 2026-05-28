/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { toEastTypeValue, type EastTypeValue } from "./type_of_type.js";
import type { EastType, ValueTypeOf } from "./types.js";
import { isVariant, match, variant } from "./containers/variant.js";
import { ref } from "./containers/ref.js";

/** Provide a default value for a given {@link EastType}, such as `0.0` for floats and `""` for strings.
 * 
 * @see {@link defaultValue} to create a typical default value, like `0.0` for floats.
*/
export function defaultValue(type: EastTypeValue): any
export function defaultValue<T extends EastType>(type: EastType): ValueTypeOf<T>
export function defaultValue(type: EastType | EastTypeValue): any {
  // convert EastTypeValue to EastType if needed
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

  return match(type as EastTypeValue, {
    Never: _ => { throw new Error(`Cannot create a default value of type .Never`) },
    Null: _ => null,
    Boolean: _ => false,
    Integer: _ => 0n,
    Float: _ => 0.0,
    String: _ => "",
    DateTime: _ => new Date(0),
    Blob: _ => new Uint8Array(),
    Ref: t => ref(defaultValue(t)),
    Array: _=> [],
    Set: _ => new Set(),
    Dict: _ => new Map(),
    Struct: field_types => {
      const obj: Record<string, any> = {};
      for (const { name, type } of field_types) {
        obj[name] = defaultValue(type);
      }
      return obj;
    },
    Variant: case_types => {
      const first_case = case_types[0];
      if (first_case === undefined) {
        throw new Error(`Cannot create a value of an empty variant`);
      }
      const { name, type } = first_case;
      return variant(name, defaultValue(type));
    },
    Recursive: _ => { throw new Error("Cannot create a default value of type .Recursive"); },
    Function: _ => { throw new Error(`Cannot create a default value of type .Function`) },
    AsyncFunction: _ => { throw new Error(`Cannot create a default value of type .AsyncFunction`) },
  });
}

/** Provide the minimal possible value for a given {@link EastType}, such as `-Infinity` for floats and `""` for strings.
 * 
 * @see {@link defaultValue} to create a typical default value, like `0.0` for floats.
 * 
 * Note that there is no maximal value for unbounded types - including strings, blobs, arrays, sets and dicts, so no `maximalValue` function is provided.
 */
export function minimalValue(type: EastTypeValue): any
export function minimalValue<T extends EastType>(type: T): ValueTypeOf<T>
export function minimalValue(type: EastType | EastTypeValue): any {
  // convert EastTypeValue to EastType if needed
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

  return match(type as EastTypeValue, {
    Never: _ => { throw new Error(`Cannot create a default value of type .Never`) },
    Null: _ => null,
    Boolean: _ => false,
    Integer: _ => 0n,
    Float: _ => 0.0,
    String: _ => "",
    DateTime: _ => new Date(0),
    Blob: _ => new Uint8Array(),
    Ref: t => ref(minimalValue(t)),
    Array: _=> [],
    Set: _ => new Set(),
    Dict: _ => new Map(),
    Struct: field_types => {
      const obj: Record<string, any> = {};
      for (const { name, type } of field_types) {
        obj[name] = defaultValue(type);
      }
      return obj;
    },
    Variant: case_types => {
      const first_case = case_types[0];
      if (first_case === undefined) {
        throw new Error(`Cannot create a value of an empty variant`);
      }
      const { name, type } = first_case;
      return variant(name, defaultValue(type));
    },
    Recursive: _ => { throw new Error("Cannot create a default value of type .Recursive"); },
    Function: _ => { throw new Error(`Cannot create a default value of type .Function`) },
    AsyncFunction: _ => { throw new Error(`Cannot create a default value of type .AsyncFunction`) },
  });
}
