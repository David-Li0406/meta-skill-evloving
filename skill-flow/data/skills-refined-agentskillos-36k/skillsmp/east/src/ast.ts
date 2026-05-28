/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { type BuiltinName } from "./builtins.js";
import type { EastType, NeverType, NullType } from "./types.js";
import type { Location } from "./location.js";

// This is the TypeScript-native, typed AST (abstract syntax tree) for East.
// At this stage variable resolution has not been completed and nodes may need to be compared by object identity to understand the code.
// The AST must be checked and transformed to IR before it can be serialized or compiled.

// TODO: all fields that are `AST` should be `any` to remove circular typing (type-erased to make TypeScript fast)

/** @internal */
export type ErrorAST = {
  ast_type: "Error",
  type: NeverType,
  location: Location[],
  message: AST,
}

/** @internal */
export type TryCatchAST = {
  ast_type: "TryCatch",
  type: EastType,
  location: Location[],
  try_body: AST,
  catch_body: AST,
  message: VariableAST,
  stack: VariableAST,
  finally_body?: AST,
}

/** @internal */
export type ValueAST = {
  ast_type: "Value",
  type: EastType,
  location: Location[],
  value: null | boolean | bigint | number | string | Date | Uint8Array,
};

/** @internal */
export type AsAST = {
  ast_type: "As",
  type: EastType,
  location: Location[],
  value: AST,
};

/** @internal */
export type VariableAST = {
  ast_type: "Variable",
  type: EastType,
  location: Location[],
  mutable: boolean,
};

/** @internal */
export type LetAST = {
  ast_type: "Let",
  type: EastType,
  location: Location[],
  variable: VariableAST,
  value: AST,
};

/** @internal */
export type AssignAST = {
  ast_type: "Assign",
  type: EastType,
  location: Location[],
  variable: VariableAST,
  value: AST,
};

/** @internal */
export type FunctionAST = {
  ast_type: "Function",
  type: EastType,
  location: Location[],
  parameters: VariableAST[],
  body: AST,
};

/** @internal */
export type AsyncFunctionAST = {
  ast_type: "AsyncFunction",
  type: EastType,
  location: Location[],
  parameters: VariableAST[],
  body: AST,
};


/** @internal */
export type CallAST = {
  ast_type: "Call",
  type: EastType,
  location: Location[],
  function: AST,
  arguments: AST[],
};

/** @internal */
export type CallAsyncAST = {
  ast_type: "CallAsync",
  type: EastType,
  location: Location[],
  function: AST,
  arguments: AST[],
};

/** @internal */
export type NewRefAST = {
  ast_type: "NewRef",
  type: EastType,
  location: Location[],
  value: AST,
};

/** @internal */
export type NewArrayAST = {
  ast_type: "NewArray",
  type: EastType,
  location: Location[],
  values: AST[],
};

/** @internal */
export type NewSetAST = {
  ast_type: "NewSet",
  type: EastType,
  location: Location[],
  values: AST[],
};

/** @internal */
export type NewDictAST = {
  ast_type: "NewDict",
  type: EastType,
  location: Location[],
  values: [AST, AST][],
};

/** @internal */
export type StructAST = {
  ast_type: "Struct",
  type: EastType,
  location: Location[],
  fields: Record<string, AST>,
};

/** @internal */
export type GetFieldAST = {
  ast_type: "GetField",
  type: EastType,
  location: Location[],
  field: string,
  struct: AST,
};

/** @internal */
export type VariantAST = {
  ast_type: "Variant",
  type: EastType,
  location: Location[],
  case: string,
  value: AST,
};

/** @internal */
export type BlockAST = {
  ast_type: "Block",
  type: EastType,
  location: Location[],
  statements: AST[],
}

/** @internal */
export type IfElseAST = {
  ast_type: "IfElse",
  type: EastType,
  location: Location[],
  ifs: {
    predicate: AST,
    body: AST,
  }[],
  else_body: AST,
};

/** @internal */
export type MatchAST = {
  ast_type: "Match",
  type: EastType,
  location: Location[],
  variant: AST,
  cases: Record<string, { variable: VariableAST, body: AST }>,
};

export type UnwrapRecursiveAST = {
  ast_type: "UnwrapRecursive",
  type: EastType,
  location: Location[],
  value: AST,
};

/** @internal */
export type WrapRecursiveAST = {
  ast_type: "WrapRecursive",
  type: EastType,
  location: Location[],
  value: AST,
};

/** @internal */
export type Label = {
  location: Location[],
}

/** @internal */
export type WhileAST = {
  ast_type: "While",
  type: NullType,
  location: Location[],
  predicate: AST,
  label: Label,
  body: AST,
};

/** @internal */
export type ForArrayAST = {
  ast_type: "ForArray",
  type: NullType,
  location: Location[],
  array: AST,
  label: Label,
  key: VariableAST,
  value: VariableAST,
  body: AST,
};

/** @internal */
export type ForSetAST = {
  ast_type: "ForSet",
  type: NullType,
  location: Location[],
  set: AST,
  label: Label,
  key: VariableAST,
  body: AST,
};

/** @internal */
export type ForDictAST = {
  ast_type: "ForDict",
  type: NullType,
  location: Location[],
  dict: AST,
  label: Label,
  key: VariableAST,
  value: VariableAST,
  body: AST,
};

/** @internal */
export type ReturnAST = {
  ast_type: "Return",
  type: NeverType,
  location: Location[],
  value: AST,
};

/** @internal */
export type ContinueAST = {
  ast_type: "Continue",
  type: NeverType,
  location: Location[],
  label: Label,
};

/** @internal */
export type BreakAST = {
  ast_type: "Break",
  type: NeverType,
  location: Location[],
  label: Label,
};

/**@internal */
export type BuiltinAST = {
  ast_type: "Builtin",
  type: EastType,
  location: Location[],
  builtin: BuiltinName,
  type_parameters: EastType[],
  arguments: AST[],
};

/** @internal */
export type PlatformAST = {
  ast_type: "Platform",
  type: EastType,
  location: Location[],
  name: string,
  type_parameters: EastType[],
  arguments: AST[],
  async: boolean,
  /** When true, compilation succeeds even if the platform function is not provided.
   * A runtime error will be thrown if the function is called without an implementation. */
  optional: boolean,
};

/** @internal */
export type AST = ErrorAST | TryCatchAST | ValueAST | AsAST | VariableAST | LetAST | AssignAST | FunctionAST | AsyncFunctionAST | CallAST | CallAsyncAST | NewRefAST | NewArrayAST | NewSetAST | NewDictAST | StructAST | GetFieldAST | VariantAST | BlockAST | IfElseAST | MatchAST | UnwrapRecursiveAST | WrapRecursiveAST | WhileAST | ForArrayAST | ForSetAST | ForDictAST | ReturnAST | ContinueAST | BreakAST | BuiltinAST | PlatformAST;
