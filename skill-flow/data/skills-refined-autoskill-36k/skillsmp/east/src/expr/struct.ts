/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { get_location } from "../location.js";
import { StructType } from "../types.js";
import {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  AstSymbol,
  Expr,
  FactorySymbol,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  TypeSymbol,
  type ToExpr
} from "./expr.js";
import type { ExprType } from "./types.js";

/**
 * Expression representing struct (product type) values with named fields.
 *
 * StructExpr provides a natural JavaScript interface for working with East structs.
 * Fields are directly accessible as properties using dot notation, and structs can be
 * modified using spread syntax to create new structs with updated fields. Structs are
 * immutable in East - all modifications create new struct values.
 *
 * @typeParam Fields - Record type mapping field names to their East types
 *
 * @remarks
 * Structs use dynamic property generation to expose fields directly on the expression object.
 * This allows natural JavaScript syntax like `person.name` and `{ ...person, age: 30n }`.
 * All properties are enumerable to support spread operations.
 *
 * @example
 * ```ts
 * // Define and use struct types
 * const PersonType = StructType({ name: StringType, age: IntegerType });
 *
 * const greet = East.function([PersonType], StringType, ($, person) => {
 *   // Access fields with dot notation
 *   $.return(Expr.str`Hello, ${person.name}! You are ${person.age} years old.`);
 * });
 * const compiled = East.compile(greet.toIR(), []);
 * compiled({ name: "Alice", age: 30n });  // "Hello, Alice! You are 30 years old."
 * ```
 *
 * @example
 * ```ts
 * // Create modified structs with spread syntax
 * const birthday = East.function([PersonType], PersonType, ($, person) => {
 *   $.return({ ...person, age: person.age.add(1n) });
 * });
 * const compiled = East.compile(birthday.toIR(), []);
 * compiled({ name: "Bob", age: 25n });  // { name: "Bob", age: 26n }
 * ```
 */
const _StructExpr = class StructExpr<Fields extends Record<string, any>> extends Expr<StructType<Fields>> {
  constructor(field_types: Fields, ast: AST, factory: ToExpr) {
    super(ast.type as StructType<Fields>, ast, factory);
    
    // Generate all the "getfield" expressions dynamically
    for (const [key, type] of Object.entries(field_types)) {
      Object.defineProperty(this, key, {
        enumerable: true,
        get: () => this[FactorySymbol]({
          ast_type: "GetField",
          type,
          location: get_location(),
          field: key,
          struct: ast,
        }),
      });
    }
  }
}

export const StructExpr = _StructExpr;
export type StructExpr<Fields extends Record<string, any>> = Expr<StructType<Fields>> & { [Key in keyof Fields]: ExprType<Fields[Key]> };
