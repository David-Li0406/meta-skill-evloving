/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { get_location } from "../location.js";
import { RecursiveType } from "../types.js";
import { Expr, FactorySymbol, AstSymbol, type ToExpr } from "./expr.js";
import type { ExprType, SubtypeExprOrValue } from "./types.js";
import { valueOrExprToAstTyped } from "./ast.js";

/**
 * Expression representing recursive data types.
 *
 * RecursiveExpr wraps expressions of recursive types (like trees or linked lists) and provides
 * access to the underlying data through the `unwrap()` method. Use `unwrap()` to get the inner
 * expression, then use its methods (e.g., `match()` for variants).
 *
 * @typeParam T - The inner type that the recursive type wraps (after RecursiveTypeMarker expansion)
 *
 * @remarks
 * Recursive types are used to represent self-referential data structures. The RecursiveExpr
 * preserves the type identity so that `TypeOf<RecursiveExpr<T>>` returns `RecursiveType<T>`,
 * which is important for type inference when recursive values are used in collections or
 * passed to functions.
 *
 * @example
 * ```ts
 * // Define a linked list type
 * const LinkedListType = RecursiveType(self => VariantType({
 *   nil: NullType,
 *   cons: StructType({ head: IntegerType, tail: self })
 * }));
 *
 * // Create and work with linked lists
 * const sumList = East.function([LinkedListType], IntegerType, ($, list) => {
 *   $.return(list.unwrap().match({
 *     nil: ($) => 0n,
 *     cons: ($, node) => node.head.add(sumList(node.tail))
 *   }));
 * });
 * ```
 */
export class RecursiveExpr<T> extends Expr<RecursiveType<T>> {
  constructor(private nodeType: T, ast: AST, factory: ToExpr) {
    super(ast.type as RecursiveType<T>, ast, factory);
  }

  /**
   * Unwraps the recursive type to access the inner expression.
   *
   * @returns An expression of the inner type with full access to its methods
   *
   * @example
   * ```ts
   * const LinkedListType = RecursiveType(self => VariantType({
   *   nil: NullType,
   *   cons: StructType({ head: IntegerType, tail: self })
   * }));
   *
   * const getHead = East.function([LinkedListType], IntegerType, ($, list) => {
   *   // Unwrap to get VariantExpr, then use variant methods
   *   $.return(list.unwrap().unwrap("cons").head);
   * });
   * ```
   */
  unwrap(): ExprType<T> {
    const unwrapAst: AST = {
      ast_type: "UnwrapRecursive",
      type: this.nodeType as AST["type"],
      location: get_location(),
      value: this[AstSymbol],
    };
    return this[FactorySymbol](unwrapAst) as ExprType<T>;
  }

  /**
   * Wraps a value or expression in a recursive type.
   *
   * @param value - The value or expression to wrap
   * @param type - The recursive type to wrap it in
   * @returns A RecursiveExpr wrapping the value
   *
   * @example
   * ```ts
   * const LinkedListType = RecursiveType(self => VariantType({
   *   nil: NullType,
   *   cons: StructType({ head: IntegerType, tail: self })
   * }));
   *
   * // Wrap a variant value in the recursive type
   * const nil = RecursiveExpr.wrap(variant("nil", null), LinkedListType);
   * ```
   */
  static wrap<T>(
    value: SubtypeExprOrValue<T>,
    type: RecursiveType<T>,
    factory: ToExpr
  ): RecursiveExpr<T> {
    const valueAst = valueOrExprToAstTyped(value, type.node as AST["type"]);
    const wrapAst: AST = {
      ast_type: "WrapRecursive",
      type: type,
      location: get_location(),
      value: valueAst,
    };
    return factory(wrapAst) as RecursiveExpr<T>;
  }
}
