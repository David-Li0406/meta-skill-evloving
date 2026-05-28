/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { get_location } from "../location.js";
import { FunctionType, NullType, RefType, type EastType } from "../types.js";
import { AstSymbol, Expr, FactorySymbol, TypeSymbol, type ToExpr } from "./expr.js";
import type { ExprType, SubtypeExprOrValue } from "./types.js";

/**
 * Expression representing reference cells (mutable containers) in East.
 *
 * RefExpr provides a reference cell type that can be shared across closures and modified.
 * Unlike variables declared with `$.let()`, references can be captured and modified from
 * within nested functions, making them useful for shared mutable state.
 *
 * @example
 * ```ts
 * // Creating and getting a reference value
 * const getRefValue = East.function([], IntegerType, ($) => {
 *   const counter = $.let(East.value(ref(42n)));
 *   $.return(counter.get());
 * });
 * const compiled = East.compile(getRefValue.toIR(), []);
 * compiled();  // 42n
 * ```
 *
 * @example
 * ```ts
 * // Updating a reference value
 * const updateRef = East.function([IntegerType], IntegerType, ($, newValue) => {
 *   const counter = $.let(East.value(ref(0n)));
 *   $(counter.update(newValue));
 *   $.return(counter.get());
 * });
 * const compiled = East.compile(updateRef.toIR(), []);
 * compiled(100n);  // 100n
 * ```
 */
export class RefExpr<T extends any> extends Expr<RefType<T>> {
  constructor(private value_type: T, ast: AST, createExpr: ToExpr) {
    super(RefType(value_type), ast, createExpr);
  }

  /**
   * Gets the current value stored in the reference cell.
   *
   * @returns An expression of the value type stored in the reference
   *
   * @example
   * ```ts
   * const getRefValue = East.function([], IntegerType, ($) => {
   *   const counter = $.let(East.value(ref(42n)));
   *   $.return(counter.get());
   * });
   * const compiled = East.compile(getRefValue.toIR(), []);
   * compiled();  // 42n
   * ```
   */
  get(): ExprType<T> {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this.value_type as EastType,
      location: get_location(),
      builtin: "RefGet",
      type_parameters: [this.value_type as EastType],
      arguments: [Expr.ast(this)],
    }) as ExprType<T>;
  }

  /**
   * Replaces the value in the reference cell with a new value.
   *
   * @param value - The new value to store in the reference cell
   * @returns A NullExpr (used for side effects)
   *
   * @example
   * ```ts
   * const updateRef = East.function([IntegerType], IntegerType, ($, newValue) => {
   *   const counter = $.let(East.value(ref(0n)));
   *   $(counter.update(newValue));
   *   $.return(counter.get());
   * });
   * const compiled = East.compile(updateRef.toIR(), []);
   * compiled(100n);  // 100n
   * ```
   *
   * @see {@link merge} for modifying the value based on its current value.
   */
  update(value: ExprType<T>): Expr<NullType> {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "RefUpdate",
      type_parameters: [this.value_type as EastType],
      arguments: [Expr.ast(this), Expr.ast(value)],
    }) as Expr<NullType>;
  }
  
  /**
   * Modifies the reference value by merging it with a new value using a function.
   *
   * This is useful for patterns where you want to update a reference based on its current value,
   * e.g. incrementing a number, appending to a string, updating fields in a struct, or pushing to an array.
   *
   * @param value - The new value to merge with the current value
   * @param updateFn - Function that takes (current, new) and returns the merged value
   * @returns A NullExpr (used for side effects)
   *
   * @example
   * ```ts
   * const incrementRef = East.function([IntegerType], IntegerType, ($, delta) => {
   *   const counter = $.let(East.value(ref(10n)));
   *   $(counter.merge(delta, ($, current, newVal) => current.add(newVal)));
   *   $.return(counter.get());
   * });
   * const compiled = East.compile(incrementRef.toIR(), []);
   * compiled(5n);  // 15n
   * ```
   *
   * @see {@link update} for simply replacing the value.
   */
  merge<T2>(value: Expr<T2>, updateFn: SubtypeExprOrValue<FunctionType<[T, NoInfer<T2>], T>>): ExprType<NullType> {
    const location = get_location();
    const value2Type = value[TypeSymbol];

    const updateFnExpr = Expr.from(updateFn as any, FunctionType([value2Type, this.value_type], this.value_type));

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location,
      builtin: "RefMerge",
      type_parameters: [this.value_type as EastType, value2Type as EastType],
      arguments: [this[AstSymbol], value[AstSymbol], updateFnExpr[AstSymbol]],
    }) as ExprType<NullType>;
  }
}