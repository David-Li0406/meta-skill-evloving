/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import type { AST } from "../ast.js";
import { get_location } from "../location.js";
import { SortedMap } from "../containers/sortedmap.js";
import { SortedSet } from "../containers/sortedset.js";
import {
  ArrayType,
  BlobType,
  BooleanType,
  DateTimeType,
  DictType,
  type EastType,
  FloatType,
  IntegerType,
  isSubtype,
  NeverType,
  NullType,
  printType,
  RefType,
  SetType,
  StringType,
  StructType,
  TypeUnion,
  VariantType
} from "../types.js";
import { isVariant, variant } from "../containers/variant.js";
import { Expr, AstSymbol, TypeSymbol } from "./expr.js";
import { isRef } from "../containers/ref.js";

/**
 * Convert a value or expression directly to AST without creating intermediate expressions
 */
export function valueOrExprToAst(value: any): AST {
  if (value instanceof Expr) {
    return value[AstSymbol];
  } else if (value === null) {
    return { ast_type: "Value", type: NullType, value, location: get_location() };
  } else if (typeof value === "boolean") {
    return { ast_type: "Value", type: BooleanType, value, location: get_location() };
  } else if (typeof value === "bigint") {
    return { ast_type: "Value", type: IntegerType, value, location: get_location() };
  } else if (typeof value === "number") {
    return { ast_type: "Value", type: FloatType, value, location: get_location() };
  } else if (typeof value === "string") {
    return { ast_type: "Value", type: StringType, value, location: get_location() };
  } else if (value instanceof Date) {
    return { ast_type: "Value", type: DateTimeType, value, location: get_location() };
  } else if (value instanceof Uint8Array) {
    return { ast_type: "Value", type: BlobType, value, location: get_location() };
  } else if (typeof value === "function") {
    throw new Error(`Unable to convert function to AST without knowing it's type`);
  } else if (isRef(value)) {
    const val_ast = valueOrExprToAst(value.value);
    return {
      ast_type: "NewRef",
      type: RefType(val_ast.type),
      value: val_ast,
      location: get_location()
    };
  } else if (Array.isArray(value)) {
    const values = value.map(x => valueOrExprToAst(x));
    let value_type = values.length > 0 ? values[0]!.type : NeverType;
    for (const [i, ast] of values.entries()) {
      if (ast.type.type === "Never") {
        throw new Error(`Unable to convert array to Array expression: value at index ${i} has type .Never`);
      }
      value_type = TypeUnion(value_type, ast.type);
    }
    return { ast_type: "NewArray", type: ArrayType(value_type), values, location: get_location() };
  } else if (value instanceof Set || value instanceof SortedSet) {
    const values = [...value].map(x => valueOrExprToAst(x));
    let value_type = values.length > 0 ? values[0]!.type : NeverType;
    for (const [i, ast] of values.entries()) {
      if (ast.type.type === "Never") {
        throw new Error(`Unable to convert set to Set expression: key at index ${i} has type .Never`);
      }
      value_type = TypeUnion(value_type, ast.type);
    }
    return { ast_type: "NewSet", type: SetType(value_type), values, location: get_location() };
  } else if (value instanceof Map || value instanceof SortedMap) {
    const values: [AST, AST][] = [...value].map(([k, v]) => [valueOrExprToAst(k), valueOrExprToAst(v)]);
    let key_type = values.length > 0 ? values[0]![0].type : NeverType;
    let value_type = values.length > 0 ? values[0]![1].type : NeverType;
    for (const [i, [k, v]] of values.entries()) {
      if (k.type.type === "Never") {
        throw new Error(`Unable to convert dict to Dict expression: key at index ${i} has type .Never`);
      }
      key_type = TypeUnion(key_type, k.type);
      if (v.type.type === "Never") {
        throw new Error(`Unable to convert dict to Dict expression: value at index ${i} has type .Never`);
      }
      value_type = TypeUnion(value_type, v.type);
    }
    return { ast_type: "NewDict", type: DictType(key_type, value_type), values, location: get_location() };
  } else if (isVariant(value)) {
    const name = value.type;
    const val = value.value;
    const val_ast = valueOrExprToAst(val);
    if (val_ast.type.type === "Never") {
      throw new Error(`Unable to convert variant to Variant expression: case ${name} has type .Never`);
    }
    const case_types = { [name]: val_ast.type };
    return { ast_type: "Variant", type: VariantType(case_types), case: name, value: val_ast, location: get_location() };
  } else if (typeof value === "object" && Object.getPrototypeOf(value) === Object.getPrototypeOf({})) {
    const fields = Object.fromEntries(Object.entries(value).map(([k, v]) => [k, valueOrExprToAst(v)]));
    const field_types = Object.fromEntries(Object.entries(fields).map(([k, ast]) => {
      if (ast.type.type === "Never") {
        throw new Error(`Unable to convert object to Struct expression: field ${k} has type .Never`);
      }
      return [k, ast.type];
    }));
    return { ast_type: "Struct", type: StructType(field_types), fields, location: get_location() };
  } else {
    throw new Error(`Unable to convert value ${value} to AST`);
  }
}

/**
 * Convert a value to AST with explicit type checking
 */
export function valueOrExprToAstTyped<T extends EastType>(value: any, type: T, visited?: Set<any>, location = get_location()): AST & { type: T } {
  if (value instanceof Expr) {
    const valueType = value[TypeSymbol];
    if (!isSubtype(valueType, type)) {
      throw new Error(`Expression expected to have type ${printType(type)} but got type ${printType(valueType)}`);
    }
    return value[AstSymbol] as AST & { type: T };
  }

  // For primitive values, validate type matches and create AST
  if (type.type === "Null") {
    if (value !== null) {
      throw new Error(`Expected null but got ${value}`);
    }
    return { ast_type: "Value", type, value, location };
  } else if (type.type === "Boolean") {
    if (typeof value !== "boolean") {
      console.log(value)
      throw new Error(`Expected boolean but got ${value === null ? "null" : typeof value}`);
    }
    return { ast_type: "Value", type, value, location };
  } else if (type.type === "Integer") {
    if (typeof value !== "bigint") {
      throw new Error(`Expected bigint but got ${value === null ? "null" : typeof value}`);
    }
    return { ast_type: "Value", type, value, location };
  } else if (type.type === "Float") {
    if (typeof value !== "number") {
      throw new Error(`Expected number but got ${value === null ? "null" : typeof value}`);
    }
    return { ast_type: "Value", type, value, location };
  } else if (type.type === "String") {
    if (typeof value !== "string") {
      throw new Error(`Expected string but got ${value === null ? "null" : typeof value}`);
    }
    return { ast_type: "Value", type, value, location };
  } else if (type.type === "DateTime") {
    if (!(value instanceof Date)) {
      throw new Error(`Expected Date but got ${value === null ? "null" : typeof value}`);
    }
    return { ast_type: "Value", type, value, location };
  } else if (type.type === "Blob") {
    if (!(value instanceof Uint8Array)) {
      throw new Error(`Expected Uint8Array but got ${value === null ? "null" : typeof value}`);
    }
    return { ast_type: "Value", type, value, location };
  } else if (type.type === "Ref") {
    if (!isRef(value)) {
      throw new Error(`Expected ref but got ${value === null ? "null" : typeof value}`);
    }

    const val_ast = valueOrExprToAstTyped(value.value, type.value, visited, location);
    if (!isSubtype(val_ast.type, type.value)) {
      throw new Error(`Ref value expected to have type ${printType(type.value)} but got type ${printType(val_ast.type)}`);
    }
    if (val_ast.type.type === "Never") {
      throw new Error(`Unable to convert value to Ref expression: value has type .Never`);
    }
    return {
      ast_type: "NewRef",
      type,
      value: val_ast,
      location
    };
  } else if (type.type === "Array") {
    if (!Array.isArray(value)) {
      throw new Error(`Expected array but got ${value === null ? "null" : typeof value}`);
    }
    const values = value.map((x, i) => {
      const ast = valueOrExprToAstTyped(x, type.value, visited, location);
      if (ast.type.type === "Never") {
        throw new Error(`Unable to convert array to Array expression: element at index ${i} has type .Never`);
      }
      return ast;
    });
    return { ast_type: "NewArray", type, values, location };
  } else if (type.type === "Set") {
    if (!(value instanceof Set || value instanceof SortedSet)) {
      throw new Error(`Expected set but got ${value === null ? "null" : typeof value}`);
    }
    const values = [...value].map((x, i) => {
      const ast = valueOrExprToAstTyped(x, type.key, visited, location);
      if (ast.type.type === "Never") {
        throw new Error(`Unable to convert set to Set expression: element at index ${i} has type .Never`);
      }
      return ast;
    });
    return { ast_type: "NewSet", type, values, location };
  } else if (type.type === "Dict") {
    if (!(value instanceof Map || value instanceof SortedMap)) {
      throw new Error(`Expected dict but got ${value === null ? "null" : typeof value}`);
    }
    const values: [AST, AST][] = [...value].map(([k, v], i) => {
      const key_ast = valueOrExprToAstTyped(k, type.key, visited, location);
      if (key_ast.type.type === "Never") {
        throw new Error(`Unable to convert dict to Dict expression: key at index ${i} has type .Never`);
      }

      const value_ast = valueOrExprToAstTyped(v, type.value, visited, location);
      if (value_ast.type.type === "Never") {
        throw new Error(`Unable to convert dict to Dict expression: value at index ${i} has type .Never`);
      }

      return [key_ast, value_ast];
    });
    return { ast_type: "NewDict", type, values, location };
  } else if (type.type === "Struct") {
    if (typeof value !== "object" || value === null) {
      throw new Error(`Expected object but got ${value === null ? "null" : typeof value}`);
    }
    const fields = Object.fromEntries(
      Object.entries(type.fields).map(([k, fieldType]) => {
        const ast = valueOrExprToAstTyped(value[k], fieldType, visited, location);
        if (ast.type.type === "Never") {
          throw new Error(`Unable to convert object to Struct expression: field ${k} has type .Never`);
        }
        return [k, ast];
      })
    );
    return { ast_type: "Struct", type, fields, location };
  } else if (type.type === "Variant") {
    if (!isVariant(value)) {
      throw new Error(`Expected variant but got ${value === null ? "null" : typeof value}`);
    }
    const name = (value as variant).type;
    const caseType = type.cases[name];
    if (!caseType) {
      throw new Error(`Variant case ${name} not found in type`);
    }

    const valueAst = valueOrExprToAstTyped((value as variant).value, caseType, visited, location);
    if (!isSubtype(valueAst.type, caseType)) {
      throw new Error(`Variant case ${name} expected to have type ${printType(caseType)} but got type ${printType(valueAst.type)}`);
    }
    if (valueAst.type.type === "Never") {
      throw new Error(`Unable to convert variant to Variant expression: case ${name} has type .Never`);
    }

    return { ast_type: "Variant", type, case: name, value: valueAst, location };
  } else if (type.type === "Recursive") {
    // Check if we're already processing this value -> circular reference (error)
    if (visited) {
      const existing = visited.has(value);
      if (existing) {
        throw new Error(`Circular reference detected when converting value to AST`);
      }
    } else {
      visited = new Set();
    }

    // Register before recursing (enables cycle detection)
    visited.add(value);

    // Process the value with the node type
    const node = valueOrExprToAstTyped(value, type.node, visited, location);

    visited.delete(value);

    // Wrap in WrapRecursive so fromAst returns a RecursiveExpr
    return { ast_type: "WrapRecursive", type, value: node, location };
  } else if (type.type === "Function") {
    if (typeof value !== "function") {
      throw new Error(`Expected function but got ${value === null ? "null" : typeof value}`);
    }

    return Expr.function(type.inputs, type.output, value)[AstSymbol] as any; // location?
  } else if (type.type === "AsyncFunction") {
    if (typeof value !== "function") {
      throw new Error(`Expected function but got ${value === null ? "null" : typeof value}`);
    }

    return Expr.asyncFunction(type.inputs, type.output, value)[AstSymbol] as any; // location?
  } else {
    throw new Error(`Type conversion not implemented for ${printType(type)}`);
  }
}
