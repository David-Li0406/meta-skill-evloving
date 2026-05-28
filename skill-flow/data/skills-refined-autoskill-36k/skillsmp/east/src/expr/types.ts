/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import type { variant } from "../containers/variant.js";
import type { ArrayType, BooleanType, FloatType, FunctionType, IntegerType, NeverType, NullType, StructType, StringType, VariantType, SubType, SetType, DictType, DateTimeType, BlobType, RecursiveType, RecursiveTypeMarker, RefType, AsyncFunctionType } from "../types.js";
import type { Expr } from "./expr.js";
import type { NeverExpr } from "./never.js";
import type { NullExpr } from "./null.js";
import type { BooleanExpr } from "./boolean.js";
import type { IntegerExpr } from "./integer.js";
import type { FloatExpr } from "./float.js";
import type { StringExpr } from "./string.js";
import type { DateTimeExpr } from "./datetime.js";
import type { BlobExpr } from "./blob.js";
import type { ArrayExpr } from "./array.js";
import type { SetExpr } from "./set.js";
import type { DictExpr } from "./dict.js";
import type { StructExpr } from "./struct.js";
import type { VariantExpr } from "./variant.js";
import type { RecursiveExpr } from "./recursive.js";
import type { CallableFunctionExpr } from "./function.js";
import type { BlockBuilder } from "./block.js";
import type { ref } from "../containers/ref.js";
import type { RefExpr } from "./ref.js";
import type { CallableAsyncFunctionExpr } from "./asyncfunction.js";

/**
 * Type mapping for values that can be passed to expression methods
 * Maps East types to their corresponding expression classes or JavaScript values
 */
export type SubtypeExprOrValue<T> =
  T extends never ? never :
  T extends NeverType ? Expr<NeverType> :
  T extends NullType ? Expr<NeverType> | Expr<NullType> | null :
  T extends BooleanType ? Expr<NeverType> | Expr<BooleanType> | boolean :
  T extends IntegerType ? Expr<NeverType> | Expr<IntegerType> | bigint :
  T extends FloatType ? Expr<NeverType> | Expr<FloatType> | number :
  T extends StringType ? Expr<NeverType> | Expr<StringType> | string :
  T extends DateTimeType ? Expr<NeverType> | Expr<DateTimeType> | Date :
  T extends BlobType ? Expr<NeverType> | Expr<BlobType> | Uint8Array :
  T extends RefType<infer U> ? Expr<NeverType> | Expr<RefType<U>> | ref<SubtypeExprOrValue<U>> :
  T extends ArrayType<infer V> ? Expr<NeverType> | Expr<ArrayType<V>> | SubtypeExprOrValue<V>[] :
  T extends SetType<infer K> ? Expr<NeverType> | Expr<SetType<K>> | Set<SubtypeExprOrValue<K>> :
  T extends DictType<infer K, infer V> ? Expr<NeverType> | Expr<DictType<K, V>> | Map<SubtypeExprOrValue<K>, SubtypeExprOrValue<V>> :
  T extends StructType<infer Fields> ? Expr<NeverType> | Expr<StructType<{ [K in keyof Fields]: SubType<Fields[K]> }>> | { [K in keyof Fields]: SubtypeExprOrValue<Fields[K]> } :
  // RecursiveType must be checked BEFORE VariantType to preserve the wrapper
  // Accept RecursiveExpr OR raw values matching the inner type (struct literals, variant values, etc.)
  // Note: SubtypeExprOrValue<U> (not ExpandOnce) - recursion breaks at RecursiveTypeMarker -> any
  T extends RecursiveType<infer U> ? RecursiveExpr<ExpandOnce<U, T>> | SubtypeExprOrValue<U> :
  T extends VariantType<infer Cases> ? Expr<NeverType> | Expr<VariantType<{ [K in keyof Cases]?: SubType<Cases[K]> }>> | { [K in keyof Cases]: variant<K, SubtypeExprOrValue<Cases[K]>> }[keyof Cases] :
  T extends RecursiveTypeMarker ? any : // recursive self-reference accepts anything
  T extends FunctionType<infer I, undefined> ? Expr<FunctionType<I, any>> | (($: BlockBuilder<NeverType>, ...input: { [K in keyof I]: ExprType<I[K]> }) => any) :
  T extends FunctionType<infer I, infer O> ? Expr<FunctionType<I, SubType<O>>> | (($: BlockBuilder<O>, ...input: { [K in keyof I]: ExprType<I[K]> }) => void | SubtypeExprOrValue<O>) :
  T extends AsyncFunctionType<infer I, undefined> ? Expr<AsyncFunctionType<I, any>> | (($: BlockBuilder<NeverType>, ...input: { [K in keyof I]: ExprType<I[K]> }) => any) :
  T extends AsyncFunctionType<infer I, infer O> ? Expr<AsyncFunctionType<I, SubType<O>>> | (($: BlockBuilder<O>, ...input: { [K in keyof I]: ExprType<I[K]> }) => void | SubtypeExprOrValue<O>) :
  Expr<NeverType> | Expr<T>;

/** Expand a given recursive type one level deeper */
export type ExpandOnce<T, NodeType> =
  T extends RefType<infer U> ? RefType<ExpandOnce<U, NodeType>> :
  T extends ArrayType<infer U> ? ArrayType<ExpandOnce<U, NodeType>> :
  T extends SetType<infer U> ? SetType<ExpandOnce<U, NodeType>> :
  T extends DictType<infer K, infer V> ? DictType<ExpandOnce<K, NodeType>, ExpandOnce<V, NodeType>> :
  T extends StructType<infer Fields> ? StructType<{ [K in keyof Fields]: ExpandOnce<Fields[K], NodeType> }> :
  // RecursiveType must be checked BEFORE VariantType to preserve the wrapper
  T extends RecursiveType<infer U> ? RecursiveType<U> :
  T extends VariantType<infer Cases> ? VariantType<{ [K in keyof Cases]: ExpandOnce<Cases[K], NodeType> }> :
  T extends RecursiveTypeMarker ? NodeType : // other recursive types get left as-is
  T;

/**
 * Type mapping from East types to their corresponding expression classes
 * This is the key type that provides concrete expression types to user code
 */
export type ExprType<T> =
  T extends never ? never :
  T extends NeverType ? NeverExpr :
  T extends NeverType | NullType ? NullExpr :
  T extends NeverType | BooleanType ? BooleanExpr :
  T extends NeverType | IntegerType ? IntegerExpr :
  T extends NeverType | FloatType ? FloatExpr :
  T extends NeverType | StringType ? StringExpr :
  T extends NeverType | DateTimeType ? DateTimeExpr :
  T extends NeverType | BlobType ? BlobExpr :
  T extends NeverType | RefType<infer U> ? RefExpr<U> :
  T extends NeverType | ArrayType<infer V> ? ArrayExpr<V> :
  T extends NeverType | SetType<infer K> ? SetExpr<K> :
  T extends NeverType | DictType<infer K, infer V> ? DictExpr<K, V> :
  T extends NeverType | StructType<infer Fields> ? StructExpr<Fields> :
  // RecursiveType must be checked BEFORE VariantType to preserve the wrapper
  // ExpandOnce replaces RecursiveTypeMarker with the full RecursiveType for proper nested access
  T extends NeverType | RecursiveType<infer U> ? RecursiveExpr<ExpandOnce<U, T>> :
  T extends NeverType | VariantType<infer Cases> ? VariantExpr<Cases> :
  T extends NeverType | RecursiveTypeMarker ? RecursiveExpr<any> : // shouldn't normally happen
  T extends NeverType | FunctionType<infer I, infer O> ? CallableFunctionExpr<I, O> :
  T extends NeverType | AsyncFunctionType<infer I, infer O> ? CallableAsyncFunctionExpr<I, O> :
  Expr<T>;

// Note the types below are written such that mixtures of values and expressions are accepted (e.g. Array<string | StringExpr> => StringType)
/**
 * Type mapping from JavaScript/Expression values to East types
 * Used for type inference in factory methods
 */
export type TypeOf<T> =
  T extends never ? never :
  T extends Expr<NeverType> ? NeverType :
  T extends null | Expr<NullType> ? NullType :
  T extends boolean | Expr<BooleanType> ? BooleanType :
  T extends bigint | Expr<IntegerType> ? IntegerType :
  T extends number | Expr<FloatType> ? FloatType :
  T extends string | Expr<StringType> ? StringType :
  T extends Date | Expr<DateTimeType> ? DateTimeType :
  T extends Uint8Array | Expr<BlobType> ? BlobType :
  T extends Expr<RefType<infer U>> ? RefType<U> :
  T extends ref<infer U> ? RefType<TypeOf<U>> :
  T extends Expr<ArrayType<infer U>> ? ArrayType<U> :
  T extends Array<infer U> ? ArrayType<TypeOf<U>> :
  T extends Expr<SetType<infer U>> ? SetType<U> :
  T extends Set<infer U> ? SetType<TypeOf<U>> :
  T extends Expr<DictType<infer K, infer V>> ? DictType<K, V> :
  T extends Map<infer K, infer V> ? DictType<TypeOf<K>, TypeOf<V>> :
  T extends Expr<FunctionType<infer I, infer O>> ? FunctionType<I, O> :
  // RecursiveType must be checked BEFORE VariantType to preserve the wrapper
  // Otherwise Expr<RecursiveType<VariantType<...>>> matches Expr<VariantType<...>> and strips the wrapper
  T extends Expr<RecursiveType<infer _U>> ? (T extends Expr<infer R> ? R : never) :
  T extends Expr<VariantType<infer Cases>> ? VariantType<Cases> :
  T extends variant<infer Case, infer U> ? Case extends string ? VariantType<{ [K in Case]: TypeOf<U> }> : never :
  // note the user might do some "interesting" spreads (replace a field, or add a new field - generally we don't support removing fields via spread)
  T extends Expr<StructType<infer Fields>> ? StructType<keyof Fields extends keyof T ? { [K in (string & keyof T)]: TypeOf<T[K]> } : { [K in keyof Fields]: K extends keyof T ? TypeOf<T[K]> : Fields[K] }> :
  T extends Expr<infer U> ? U :
  StructType<{ [K in (string & keyof T)]: TypeOf<T[K]> }>;
