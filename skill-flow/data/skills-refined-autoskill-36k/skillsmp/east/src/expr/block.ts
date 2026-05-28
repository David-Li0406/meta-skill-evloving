/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { type AST, type IfElseAST, type Label, type TryCatchAST, type VariableAST } from "../ast.js";
import { get_location, printLocations, type Location } from "../location.js";
import { type EastType, FunctionType, isSubtype, NullType, printType, isTypeEqual, StringType, NeverType, VariantType, BooleanType, TypeUnion, IntegerType, StructType, ArrayType, type ValueTypeOf, AsyncFunctionType, type RefType, type SetType, type DictType, type RecursiveType, type RecursiveTypeMarker } from "../types.js";

import type { ExprType, SubtypeExprOrValue, TypeOf } from "./types.js";
import { AstSymbol, Expr, TypeSymbol } from "./expr.js";
import { NeverExpr } from "./never.js";
import { NullExpr } from "./null.js";
import { BooleanExpr } from "./boolean.js";
import { IntegerExpr } from "./integer.js";
import { FloatExpr } from "./float.js";
import { StringExpr } from "./string.js";
import { DateTimeExpr } from "./datetime.js";
import { BlobExpr } from "./blob.js";
import { ArrayExpr } from "./array.js";
import { SetExpr } from "./set.js";
import { DictExpr } from "./dict.js";
import { StructExpr } from "./struct.js";
import { VariantExpr } from "./variant.js";
import { RecursiveExpr } from "./recursive.js";
import { type CallableFunctionExpr, createFunctionExpr, FunctionExpr } from "./function.js";
import { valueOrExprToAst, valueOrExprToAstTyped } from "./ast.js";
import type { PlatformFunction } from "../platform.js";
import { toEastTypeValue, type EastTypeValue } from "../type_of_type.js";
import { isVariant } from "../containers/variant.js";
import { RefExpr } from "./ref.js";
import { AsyncFunctionExpr, createAsyncFunctionExpr, type CallableAsyncFunctionExpr } from "./asyncfunction.js";
import { PatchType, type PatchTypeOf } from "../patch/index.js";

/** A factory function to help build `Expr` from AST.
 * We inject this into each concrete `Expr` type so they can create new expressions recursively, without having circular dependencies between JavaScript modules.
 */
export function fromAst<T extends AST>(ast: T): Expr<T["type"]> {
  const type = ast.type.type;
  if (type === "Never") {
    return new NeverExpr(ast, fromAst);
  } else if (type === "Null") {
    return new NullExpr(ast, fromAst);
  } else if (type === "Boolean") {
    return new BooleanExpr(ast, fromAst);
  } else if (type === "Integer") {
    return new IntegerExpr(ast, fromAst);
  } else if (type === "Float") {
    return new FloatExpr(ast, fromAst);
  } else if (type === "String") {
    return new StringExpr(ast, fromAst);
  } else if (type === "DateTime") {
    return new DateTimeExpr(ast, fromAst);
  } else if (type === "Blob") {
    return new BlobExpr(ast, fromAst);
  } else if (type === "Ref") {
    return new RefExpr(ast.type.value, ast, fromAst);
  } else if (type === "Array") {
    return new ArrayExpr(ast.type.value, ast, fromAst);
  } else if (type === "Set") {
    return new SetExpr(ast.type.key, ast, fromAst);
  } else if (type === "Dict") {
    return new DictExpr(ast.type.key, ast.type.value, ast, fromAst);
  } else if (type === "Struct") {
    return new StructExpr(ast.type.fields, ast, fromAst);
  } else if (type === "Variant") {
    return new VariantExpr(ast.type.cases, ast, fromAst);
  } else if (type === "Recursive") {
    // Return RecursiveExpr to preserve the RecursiveType wrapper for TypeOf
    return new RecursiveExpr(ast.type.node, ast, fromAst);
  } else if (type === "Function") {
    return createFunctionExpr(ast.type.inputs, ast.type.output, ast, fromAst);
  } else if (type === "AsyncFunction") {
    return createAsyncFunctionExpr(ast.type.inputs, ast.type.output, ast, fromAst);
  } else {
    throw new Error(`fromAst not implemented for type ${printType(ast.type satisfies never)} at ${printLocations(ast.location)}`);
  }
}


/**
 * Compile a function expression into a JavaScript function.
 *
 * @param f the function expression to compile
 * @param platform the platform functions available during compilation
 * @returns the compiled function
 */
export function compile<I extends any[], O>(f: FunctionExpr<I, O>, platform: PlatformFunction[]): (...inputs: { [K in keyof I]: ValueTypeOf<I[K]> }) => ValueTypeOf<O>  {
  return f.toIR().compile(platform);
}

/**
 * Compile an async function expression into a JavaScript function.
 *
 * @param f the async function expression to compile
 * @param platform the platform functions available during compilation
 * @returns the compiled async function
 */
export function compileAsync<I extends any[], O>(f: AsyncFunctionExpr<I, O>, platform: PlatformFunction[]): (...inputs: { [K in keyof I]: ValueTypeOf<I[K]> }) => Promise<ValueTypeOf<O>>  {
  return f.toIR().compile(platform);
}

/**
 * Create an East expression from a JavaScript value
 */
export function from<T>(value: SubtypeExprOrValue<NoInfer<T>>, type: T): ExprType<T>
export function from<V>(value: V): ExprType<TypeOf<V>>
export function from(value: any, type?: EastType): Expr<any> {
  if (value instanceof Expr) {
    if (type) {
      const t = Expr.type(value);
      if (!isSubtype(t, type)) {
        throw new Error(`Expression expected to have type ${printType(type)} but got type ${printType(t)}`)
      }
    }
    return value;
  }

  // Handle function case specially since it requires BlockBuilder
  if (type && type.type === "Function") {
    if (typeof value !== "function") {
      throw new Error(`Expected function but got ${typeof value}`);
    }

    const { inputs, output } = type;
    const input_variables: VariableAST[] = inputs.map(i => ({
      ast_type: "Variable",
      type: i,
      location: get_location(),
      mutable: false,
    }));

    const $ = BlockBuilder(output);
    const input_exprs = input_variables.map(fromAst);
    const ret = value($, ...input_exprs);
    const statements = $.statements;
    
    if (ret !== undefined) {
      if (ret instanceof Expr) {
        // It is possible this expression is already the last statement.
        // Input of the form `$ => $.xxx()` or `$ => { ...; return $.xxx(); }` will cause this
        // So we filter out this case to avoid unintended repeated statements (and if users write an identical expression twice, they won't be `===`)
        if (statements.length === 0 || statements[statements.length - 1] !== ret[AstSymbol]) {
          statements.push(Expr.ast(ret));
        }
      } else {
        const retAst = valueOrExprToAstTyped(ret, output);
        statements.push(retAst);
      }
    }

    let body_ast: AST;
    if (isTypeEqual(output, NullType)) {
      if (statements.length === 0) {
        body_ast = { ast_type: "Value", type: NullType, location: get_location(), value: null };
      } else if (statements.length === 1 && isSubtype(statements[0]!.type, NullType)) {
        body_ast = statements[0]!;
      } else {
        if (!isSubtype(statements[statements.length - 1]!.type, NullType)) {
          statements.push({ ast_type: "Value", type: NullType, location: get_location(), value: null });
        }
        body_ast = {
          ast_type: "Block",
          type: statements[statements.length - 1]!.type,
          location: get_location(),
          statements: statements,
        }
      }
    } else {
      if (statements.length === 0) {
        throw new Error(`Function expected output of type ${printType(output)}, but no function body or statements were provided`)
      } else if (statements.length === 1) {
        if (!isSubtype(statements[0]!.type, output)) {
          throw new Error(`Function expected output of type ${printType(output)}, but function body has type ${printType(statements[0]!.type)}`)
        }
        body_ast = statements[0]!;
      } else {
        if (!isSubtype(statements[statements.length - 1]!.type, output)) {
          throw new Error(`Function expected output of type ${printType(output)}, but function body has type ${printType(statements[statements.length - 1]!.type)}`)
        }
        body_ast = {
          ast_type: "Block",
          type: statements[statements.length - 1]!.type,
          location: get_location(),
          statements: statements,
        }
      }
    }

    if (!isSubtype(body_ast.type, output)) {
      throw new Error(`Expected function definition to return type ${printType(output)}, got ${printType(body_ast.type)}`);
    }

    const ast: AST = {
      ast_type: "Function",
      type: FunctionType(inputs, output),
      location: get_location(),
      parameters: input_variables,
      body: body_ast,
    };

    return fromAst(ast);
  } else if (type && type.type === "AsyncFunction") {
    if (typeof value !== "function") {
      throw new Error(`Expected function but got ${typeof value}`);
    }

    const { inputs, output } = type;
    const input_variables: VariableAST[] = inputs.map(i => ({
      ast_type: "Variable",
      type: i,
      location: get_location(),
      mutable: false,
    }));

    const $ = BlockBuilder(output);
    const input_exprs = input_variables.map(fromAst);
    const ret = value($, ...input_exprs);
    const statements = $.statements;
    
    if (ret !== undefined) {
      if (ret instanceof Expr) {
        // It is possible this expression is already the last statement.
        // Input of the form `$ => $.xxx()` or `$ => { ...; return $.xxx(); }` will cause this
        // So we filter out this case to avoid unintended repeated statements (and if users write an identical expression twice, they won't be `===`)
        if (statements.length === 0 || statements[statements.length - 1] !== ret[AstSymbol]) {
          statements.push(Expr.ast(ret));
        }
      } else {
        const retAst = valueOrExprToAstTyped(ret, output);
        statements.push(retAst);
      }
    }

    let body_ast: AST;
    if (isTypeEqual(output, NullType)) {
      if (statements.length === 0) {
        body_ast = { ast_type: "Value", type: NullType, location: get_location(), value: null };
      } else if (statements.length === 1 && isSubtype(statements[0]!.type, NullType)) {
        body_ast = statements[0]!;
      } else {
        if (!isSubtype(statements[statements.length - 1]!.type, NullType)) {
          statements.push({ ast_type: "Value", type: NullType, location: get_location(), value: null });
        }
        body_ast = {
          ast_type: "Block",
          type: statements[statements.length - 1]!.type,
          location: get_location(),
          statements: statements,
        }
      }
    } else {
      if (statements.length === 0) {
        throw new Error(`Function expected output of type ${printType(output)}, but no function body or statements were provided`)
      } else if (statements.length === 1) {
        if (!isSubtype(statements[0]!.type, output)) {
          throw new Error(`Function expected output of type ${printType(output)}, but function body has type ${printType(statements[0]!.type)}`)
        }
        body_ast = statements[0]!;
      } else {
        if (!isSubtype(statements[statements.length - 1]!.type, output)) {
          throw new Error(`Function expected output of type ${printType(output)}, but function body has type ${printType(statements[statements.length - 1]!.type)}`)
        }
        body_ast = {
          ast_type: "Block",
          type: statements[statements.length - 1]!.type,
          location: get_location(),
          statements: statements,
        }
      }
    }

    if (!isSubtype(body_ast.type, output)) {
      throw new Error(`Expected function definition to return type ${printType(output)}, got ${printType(body_ast.type)}`);
    }

    const ast: AST = {
      ast_type: "AsyncFunction",
      type: FunctionType(inputs, output),
      location: get_location(),
      parameters: input_variables,
      body: body_ast,
    };

    return fromAst(ast);
  }

  const ast = type ? valueOrExprToAstTyped(value, type) : valueOrExprToAst(value);
  return fromAst(ast);
}


/** Define an East function.
 * 
 * The function may either be a free function or a closure.
 * A closure is a function defined within another function that "captures", or refers to, one or more variables from an outer function.
 * Functions without captures are called free functions and can be compiled and executed.
 */
export function func<const I extends EastType[], O extends EastType>(input_types: I, output_type: O, body: ($: BlockBuilder<O>, ...inputs: { [K in keyof I]: ExprType<I[K]> }) => SubtypeExprOrValue<O> | void): CallableFunctionExpr<I, O>
/** @internal */
export function func<const I extends EastType[], F extends ($: BlockBuilder<NeverType>, ...inputs: { [K in keyof I]: ExprType<I[K]> }) => any>(input_types: I, output_type: undefined, body: F): CallableFunctionExpr<I, TypeOf<ReturnType<F> extends void ? NeverType : ReturnType<F>>>
export function func(input_types: EastType[], output_type: EastType | undefined, body: ($: BlockBuilder<any>, ...inputs: Expr[]) => any): Expr<FunctionType<any[], any>> {
  const parameters: VariableAST[] = input_types.map(i => ({
    ast_type: "Variable",
    type: i,
    location: get_location(),
    mutable: false,
  }));
  const $ = BlockBuilder<any>(output_type ?? NeverType);
  let ret = body($, ...parameters.map(fromAst));
  const statements = $.statements;

  if (output_type === undefined) {
    if (ret === undefined) {
      throw new Error(`When output_type is not specified, function body must return a value`);
    }
    const ret_ast = ret instanceof Expr ? Expr.ast(ret) : valueOrExprToAst(ret);
    if (statements.length === 0 || statements[statements.length - 1] !== ret_ast) { // avoid duplicate statements
      statements.push(ret_ast)
    }
    const ret_type = ret_ast.type;
    
    let body_ast: AST;
    if (statements.length === 0) {
      body_ast = { ast_type: "Value", type: NullType, location: get_location(), value: null };
    } else if (statements.length === 1) {
      body_ast = statements[0]!;
    } else {
      body_ast = {
        ast_type: "Block",
        type: statements[statements.length - 1]!.type,
        location: get_location(),
        statements: statements,
      };
    }
    if (!isSubtype(body_ast.type, ret_type)) {
      throw new Error(`function expected to return a value of type ${printType(ret_type)}, got ${printType(body_ast.type)}`);
    }

    const ast = {
      ast_type: "Function" as const,
      type: FunctionType(input_types, ret_type),
      location: get_location(),
      parameters: parameters,
      body: body_ast,
    };

    return fromAst(ast);
  } else {
    if (ret !== undefined) {
      const ret_ast = valueOrExprToAstTyped(ret, output_type);
      if (statements.length === 0 || statements[statements.length - 1] !== ret_ast) { // avoid duplicate statements
        statements.push(ret_ast);
      }
    }

    let body_ast: AST;
    if (statements.length === 0) {
      body_ast = { ast_type: "Value", type: NullType, location: get_location(), value: null };
    } else if (statements.length === 1) {
      body_ast = statements[0]!;
    } else {
      body_ast = {
        ast_type: "Block",
        type: statements[statements.length - 1]!.type,
        location: get_location(),
        statements: statements,
      };
    }
    // This is an interesting one - do we have implicit returns? Do we need to track the absence of control flow?
    // if (!isSubtype(expr.type, output_type)) {
    //   throw new Error(`func expected to return a value of type ${printType(output_type)}, got ${printType(expr.type)}`);
    // }

    const ast = {
      ast_type: "Function" as const,
      type: FunctionType(input_types, output_type),
      location: get_location(),
      parameters: parameters,
      body: body_ast,
    };

    return fromAst(ast);
  }
}

/** Define an East function.
 * 
 * The function may either be a free function or a closure.
 * A closure is a function defined within another function that "captures", or refers to, one or more variables from an outer function.
 * Functions without captures are called free functions and can be compiled and executed.
 */
export function asyncFunction<const I extends EastType[], O extends EastType>(input_types: I, output_type: O, body: ($: BlockBuilder<O>, ...inputs: { [K in keyof I]: ExprType<I[K]> }) => SubtypeExprOrValue<O> | void): CallableAsyncFunctionExpr<I, O>
/** @internal */
export function asyncFunction<const I extends EastType[], F extends ($: BlockBuilder<NeverType>, ...inputs: { [K in keyof I]: ExprType<I[K]> }) => any>(input_types: I, output_type: undefined, body: F): CallableAsyncFunctionExpr<I, TypeOf<ReturnType<F> extends void ? NeverType : ReturnType<F>>>
export function asyncFunction(input_types: EastType[], output_type: EastType | undefined, body: ($: BlockBuilder<any>, ...inputs: Expr[]) => any): Expr<AsyncFunctionType<any[], any>> {
  const parameters: VariableAST[] = input_types.map(i => ({
    ast_type: "Variable",
    type: i,
    location: get_location(),
    mutable: false,
  }));
  const $ = BlockBuilder<any>(output_type ?? NeverType);
  let ret = body($, ...parameters.map(fromAst));
  const statements = $.statements;

  if (output_type === undefined) {
    if (ret === undefined) {
      throw new Error(`When output_type is not specified, function body must return a value`);
    }
    const ret_ast = ret instanceof Expr ? Expr.ast(ret) : valueOrExprToAst(ret);
    if (statements.length === 0 || statements[statements.length - 1] !== ret_ast) { // avoid duplicate statements
      statements.push(ret_ast)
    }
    const ret_type = ret_ast.type;
    
    let body_ast: AST;
    if (statements.length === 0) {
      body_ast = { ast_type: "Value", type: NullType, location: get_location(), value: null };
    } else if (statements.length === 1) {
      body_ast = statements[0]!;
    } else {
      body_ast = {
        ast_type: "Block",
        type: statements[statements.length - 1]!.type,
        location: get_location(),
        statements: statements,
      };
    }
    if (!isSubtype(body_ast.type, ret_type)) {
      throw new Error(`function expected to return a value of type ${printType(ret_type)}, got ${printType(body_ast.type)}`);
    }

    const ast = {
      ast_type: "AsyncFunction" as const,
      type: AsyncFunctionType(input_types, ret_type),
      location: get_location(),
      parameters: parameters,
      body: body_ast,
    };

    return fromAst(ast);
  } else {
    if (ret !== undefined) {
      const ret_ast = valueOrExprToAstTyped(ret, output_type);
      if (statements.length === 0 || statements[statements.length - 1] !== ret_ast) { // avoid duplicate statements
        statements.push(ret_ast);
      }
    }

    let body_ast: AST;
    if (statements.length === 0) {
      body_ast = { ast_type: "Value", type: NullType, location: get_location(), value: null };
    } else if (statements.length === 1) {
      body_ast = statements[0]!;
    } else {
      body_ast = {
        ast_type: "Block",
        type: statements[statements.length - 1]!.type,
        location: get_location(),
        statements: statements,
      };
    }
    // This is an interesting one - do we have implicit returns? Do we need to track the absence of control flow?
    // if (!isSubtype(expr.type, output_type)) {
    //   throw new Error(`func expected to return a value of type ${printType(output_type)}, got ${printType(expr.type)}`);
    // }

    const ast = {
      ast_type: "AsyncFunction" as const,
      type: AsyncFunctionType(input_types, output_type),
      location: get_location(),
      parameters: parameters,
      body: body_ast,
    };

    return fromAst(ast);
  }
}

/** Template string literal to create an East string dynamically from components
 * 
 * @example
 * ```ts
 * str`My name is ${name}`
 * ```
*/
export function str(strings: TemplateStringsArray, ...expressions: (Expr | string)[]): StringExpr {
  const location = get_location();

  // For simple strings, e.g: str`abc`
  if (strings.length === 1) {
    return fromAst({
      ast_type: "Value",
      type: StringType,
      location,
      value: strings[0]!,
    }) as StringExpr;
  }

  // In the below we optimize away components of `strings` that is empty, removing run-time overhead.
  // To do so correctly we need to handle when the first component is empty
  if (strings[0] === "") {
    let ret: AST;
    if (typeof expressions[0] === "string") {
      ret = {
        ast_type: "Value",
        type: StringType,
        location,
        value: expressions[0],
      };
    } else if (isTypeEqual(Expr.type(expressions[0]!), StringType)) {
      ret = Expr.ast(expressions[0]!);
    } else {
      ret = {
        ast_type: "Builtin",
        type: StringType,
        location,
        builtin: "Print",
        type_parameters: [Expr.type(expressions[0]!)],
        arguments: [Expr.ast(expressions[0]!)],
      }
    }

    if (strings[1]!.length > 0) {
      ret = {
        ast_type: "Builtin",
        type: StringType,
        location: ret.location,
        builtin: "StringConcat",
        type_parameters: [],
        arguments: [ret, {
          ast_type: "Value",
          location: ret.location,
          type: StringType,
          value: strings[1]!,
        }]
      };
    }

    for (let i = 2; i < strings.length; i++) {
      const expr = expressions[i - 1]!;
      if (typeof expr === "string") {
        ret = {
          ast_type: "Builtin",
          type: StringType,
          location: ret.location,
          builtin: "StringConcat",
          type_parameters: [],
          arguments: [ret, {
            ast_type: "Value",
            type: StringType,
            location,
            value: expr,
          }]
        };
      } else if (isTypeEqual(Expr.type(expr), StringType)) {
        ret = {
          ast_type: "Builtin",
          type: StringType,
          location: ret.location,
          builtin: "StringConcat",
          type_parameters: [],
          arguments: [ret, Expr.ast(expr)]
        };
      } else {
        ret = {
          ast_type: "Builtin",
          type: StringType,
          location: ret.location,
          builtin: "StringConcat",
          type_parameters: [],
          arguments: [ret, {
            ast_type: "Builtin",
            type: StringType,
            location: ret.location,
            builtin: "Print",
            type_parameters: [Expr.type(expr)],
            arguments: [Expr.ast(expr)],
          }]
        };
      }
  
      if (strings[i]!.length > 0) {
        ret = {
          ast_type: "Builtin",
          type: StringType,
          location: ret.location,
          builtin: "StringConcat",
          type_parameters: [],
          arguments: [ret, {
            ast_type: "Value",
            location: ret.location,
            type: StringType,
            value: strings[i]!,
          }]
        };
      }
    }

    return fromAst(ret) as StringExpr;
  } else {
    let ret: AST = {
      ast_type: "Value",
      type: StringType,
      location: get_location(),
      value: strings[0]!,
    };
  
    for (let i = 1; i < strings.length; i++) {
      const expr = expressions[i - 1]!;
      if (typeof expr === "string") {
        ret = {
          ast_type: "Builtin",
          type: StringType,
          location: ret.location,
          builtin: "StringConcat",
          type_parameters: [],
          arguments: [ret, {
            ast_type: "Value",
            type: StringType,
            location,
            value: expr,
          }]
        };
      } else if (isTypeEqual(Expr.type(expr), StringType)) {
        ret = {
          ast_type: "Builtin",
          type: StringType,
          location: ret.location,
          builtin: "StringConcat",
          type_parameters: [],
          arguments: [ret, Expr.ast(expr)]
        };
      } else {
        ret = {
          ast_type: "Builtin",
          type: StringType,
          location: ret.location,
          builtin: "StringConcat",
          type_parameters: [],
          arguments: [ret, {
            ast_type: "Builtin",
            type: StringType,
            location: ret.location,
            builtin: "Print",
            type_parameters: [Expr.type(expr)],
            arguments: [Expr.ast(expr)],
          }]
        };
      }
  
      if (strings[i]!.length > 0) {
        ret = {
          ast_type: "Builtin",
          type: StringType,
          location: ret.location,
          builtin: "StringConcat",
          type_parameters: [],
          arguments: [ret, {
            ast_type: "Value",
            location: ret.location,
            type: StringType,
            value: strings[i]!,
          }]
        };
      }
    }
  
    return fromAst(ret) as StringExpr;
  }
}


/**
 * Create an East block expression.
 * The block may produce a value by returning an expressions.
 */
export function block<F extends ($: BlockBuilder<NeverType>) => any>(body: F): ReturnType<F> extends void ? NeverExpr : ExprType<TypeOf<ReturnType<F>>> {
  // Technically, a block not included in a statement will increment the var count and loop count
  const $ = BlockBuilder(NeverType);
  const ret = body($);
  const statements = $.statements;

  let ret_type: EastType = NullType;
  for (const stmt of statements) {
    ret_type = stmt.type;
  }

  if (ret === undefined) {
    // This ensures our TypeScript type inference and actual type inference concur
    if (!isTypeEqual(ret_type, NeverType)) {
      throw new Error(`block without return must have type ${printType(NeverType)}, got ${printType(ret_type)} - try returning the final expression or adding \`return null\``);
    }
 } else {
    const ret_ast = valueOrExprToAst(ret);
    if (statements.length === 0 || statements[statements.length - 1] !== ret_ast) { // avoid duplicate statements
      statements.push(ret_ast);
      ret_type = ret_ast.type;
    }
  }

  if (statements.length === 0) {
    return fromAst({
      ast_type: "Value",
      location: get_location(),
      type: ret_type,
      value: null,
    }) as any;
  } else if (statements.length === 1) {
    return fromAst(statements[0]!) as any;
  } else {
    return fromAst({
      ast_type: "Block",
      location: get_location(),
      type: ret_type,
      statements: statements,
    }) as any;
  }
}

/**
 * Create an East error expression
 */
export function error(message: SubtypeExprOrValue<StringType>, location: Location[] = get_location()): NeverExpr {
  const messageAst = message instanceof Expr ? Expr.ast(message as Expr<StringType>) : valueOrExprToAstTyped(message, StringType);
  return fromAst({
    ast_type: "Error",
    type: NeverType,
    message: messageAst,
    location,
  }) as NeverExpr;
}

/** Create a match expression */
export function matchExpr<Cases extends Record<string, any>, Handlers extends { [K in keyof Cases]: ($: BlockBuilder<NeverType>, data: ExprType<Cases[K]>) => any }>(variant: Expr<VariantType<Cases>>, handlers: Handlers): ExprType<TypeOf<{ [K in keyof Cases] : ReturnType<Handlers[K]> }[keyof Cases]>> {
  if (Expr.type(variant).type !== "Variant") {
    throw new Error(`match not defined over ${printType(Expr.type(variant))}`)
  }

  const cases_out: Record<string, { variable: VariableAST, body: AST }> = {};
  let out_type: EastType = NeverType;

  for (const [k, t] of Object.entries(Expr.type(variant).cases as Record<string, EastType>)) {
    const handler = handlers[k]!;

    const data_variable: VariableAST = {
      ast_type: "Variable",
      type: t,
      location: get_location(),
      mutable: false,
    };

    const ast = handler === undefined ? valueOrExprToAstTyped(null, NullType) : block($ => handler($, fromAst(data_variable) as any))[AstSymbol];

    out_type = TypeUnion(out_type, ast.type);

    cases_out[k] = { variable: data_variable, body: ast };
  }

  // TODO do we care if extra case branches exist? (we don't even call the function passed in!)

  return fromAst({
    ast_type: "Match",
    type: out_type,
    location: get_location(),
    variant: Expr.ast(variant),
    cases: cases_out,
  }) as any;
}

/**
 * Create an East try-catch expression
 */
export function tryCatch<T1, F extends ($: BlockBuilder<NeverType>, message: ExprType<StringType>, stack: ExprType<ArrayType<StructType<{ filename: StringType, line: IntegerType, column: IntegerType }>>>) => any>(try_body: Expr<T1>, catch_body: F): ExprType<TypeUnion<T1, TypeOf<ReturnType<F>>>> {
  const try_type = Expr.type(try_body) as EastType;

  // Create variables for the catch body
  const message_variable = {
    ast_type: "Variable" as const,
    type: StringType,
    location: get_location(),
    mutable: false,
  };

  const stack_variable = {
    ast_type: "Variable" as const,
    type: ArrayType(StructType({ filename: StringType, line: IntegerType, column: IntegerType })),
    location: get_location(),
    mutable: false,
  };

  if (typeof catch_body !== "function") {
    throw new Error(`tryCatch expected catch_body to be a function, got ${typeof catch_body}`);
  }
  const catch_body_expr = block($ => catch_body($, fromAst(message_variable) as any, fromAst(stack_variable) as any));
  const catch_body_ast = catch_body_expr[AstSymbol];
  const catch_type = catch_body_ast.type;

  const ret_type = TypeUnion(try_type, catch_type);

  return fromAst({
    ast_type: "TryCatch",
    type: ret_type,
    location: get_location(),
    try_body: Expr.ast(try_body),
    catch_body: catch_body_ast,
    message: message_variable,
    stack: stack_variable,
  }) as ExprType<TypeUnion<T1, TypeOf<ReturnType<F>>>>;
}

/** Test if the first value is equal to the second. */
export function equal<T>(left: Expr<T>, right: SubtypeExprOrValue<NoInfer<T>>): BooleanExpr {
  const rightAst = valueOrExprToAstTyped(right, Expr.type(left) as any);
  return fromAst({
    ast_type: "Builtin",
    type: BooleanType,
    location: get_location(),
    builtin: "Equal",
    type_parameters: [Expr.type(left) as EastType],
    arguments: [Expr.ast(left), rightAst],
  }) as BooleanExpr;
}

/** Test if the first value is not equal to the second. */
export function notEqual<T>(left: Expr<T>, right: SubtypeExprOrValue<NoInfer<T>>): BooleanExpr {
  const rightAst = valueOrExprToAstTyped(right, Expr.type(left) as any);
  return fromAst({
    ast_type: "Builtin",
    type: BooleanType,
    location: get_location(),
    builtin: "NotEqual",
    type_parameters: [Expr.type(left) as EastType],
    arguments: [Expr.ast(left), rightAst],
  }) as BooleanExpr;
}

/** Test if the first value is less than the second. */
export function less<T>(left: Expr<T>, right: SubtypeExprOrValue<NoInfer<T>>): BooleanExpr {
  const rightAst = valueOrExprToAstTyped(right, Expr.type(left) as any);
  return fromAst({
    ast_type: "Builtin",
    type: BooleanType,
    location: get_location(),
    builtin: "Less",
    type_parameters: [Expr.type(left) as EastType],
    arguments: [Expr.ast(left), rightAst],
  }) as BooleanExpr;
}

/** Test if the first value is less than or equal to the second. */
export function lessEqual<T>(left: Expr<T>, right: SubtypeExprOrValue<NoInfer<T>>): BooleanExpr {
  const rightAst = valueOrExprToAstTyped(right, Expr.type(left) as any);
  return fromAst({
    ast_type: "Builtin",
    type: BooleanType,
    location: get_location(),
    builtin: "LessEqual",
    type_parameters: [Expr.type(left) as EastType],
    arguments: [Expr.ast(left), rightAst],
  }) as BooleanExpr;
}

/** Test if the first value is greater than the second. */
export function greater<T>(left: Expr<T>, right: SubtypeExprOrValue<NoInfer<T>>): BooleanExpr {
  const rightAst = valueOrExprToAstTyped(right, Expr.type(left) as any);
  return fromAst({
    ast_type: "Builtin",
    type: BooleanType,
    location: get_location(),
    builtin: "Greater",
    type_parameters: [Expr.type(left) as EastType],
    arguments: [Expr.ast(left), rightAst],
  }) as BooleanExpr;
}

/** Test if the first value is greater than or equal to the second. */
export function greaterEqual<T>(left: Expr<T>, right: SubtypeExprOrValue<NoInfer<T>>): BooleanExpr {
  const rightAst = valueOrExprToAstTyped(right, Expr.type(left) as any);
  return fromAst({
    ast_type: "Builtin",
    type: BooleanType,
    location: get_location(),
    builtin: "GreaterEqual",
    type_parameters: [Expr.type(left) as EastType],
    arguments: [Expr.ast(left), rightAst],
  }) as BooleanExpr;
}

// ============================================================================
// Aliases for standalone comparison functions
// ============================================================================

/** Alias for {@link equal} */
export const equals = equal;
/** Alias for {@link equal} */
export const eq = equal;

/** Alias for {@link notEqual} */
export const notEquals = notEqual;
/** Alias for {@link notEqual} */
export const ne = notEqual;

/** Alias for {@link less} */
export const lessThan = less;
/** Alias for {@link less} */
export const lt = less;

/** Alias for {@link lessEqual} */
export const lessThanOrEqual = lessEqual;
/** Alias for {@link lessEqual} */
export const lte = lessEqual;
/** Alias for {@link lessEqual} */
export const le = lessEqual;

/** Alias for {@link greater} */
export const greaterThan = greater;
/** Alias for {@link greater} */
export const gt = greater;

/** Alias for {@link greaterEqual} */
export const greaterThanOrEqual = greaterEqual;
/** Alias for {@link greaterEqual} */
export const gte = greaterEqual;
/** Alias for {@link greaterEqual} */
export const ge = greaterEqual;

/** Test if the first value is the same object the second.
 * For mutable collections, such as arrays, this means that they are the same object in memory.
 * For immutable data types, such as integers and strings, this is equivalent to equality.
 */
export function is<T>(left: Expr<T>, right: SubtypeExprOrValue<NoInfer<T>>): BooleanExpr {
  const rightAst = valueOrExprToAstTyped(right, Expr.type(left) as any);
  return fromAst({
    ast_type: "Builtin",
    type: BooleanType,
    location: get_location(),
    builtin: "Is",
    type_parameters: [Expr.type(left) as EastType],
    arguments: [Expr.ast(left), rightAst],
  }) as BooleanExpr;
}

/** Print a value as a string. */
export function print(value: Expr): StringExpr {
  const valueAst = Expr.ast(value);
  return fromAst({
    ast_type: "Builtin",
    type: StringType,
    location: get_location(),
    builtin: "Print",
    type_parameters: [valueAst.type],
    arguments: [valueAst],
  }) as StringExpr;
}

// ============================================================================
// Patch Operations
// ============================================================================

/** Compute the difference between two values of the same type.
 * Returns a patch that, when applied to `before`, produces `after`.
 */
export function diff<T extends EastType>(before: Expr<T>, after: Expr<T>): ExprType<PatchTypeOf<T>> {
  const beforeAst = Expr.ast(before);
  const afterAst = Expr.ast(after);
  const valueType = beforeAst.type;
  const patchType = PatchType(valueType);
  return fromAst({
    ast_type: "Builtin",
    type: patchType,
    location: get_location(),
    builtin: "Diff",
    type_parameters: [valueType, patchType],
    arguments: [beforeAst, afterAst],
  }) as ExprType<PatchTypeOf<T>>;
}

/** Apply a patch to a value, producing the modified value.
 * @throws East runtime error if the patch conflicts with the value (e.g., deleting a non-existent key)
 */
export function applyPatch<T extends EastType>(value: Expr<T>, patch: Expr<PatchTypeOf<T>>): ExprType<T> {
  const valueAst = Expr.ast(value);
  const patchAst = Expr.ast(patch);
  const valueType = valueAst.type;
  const patchType = patchAst.type;
  return fromAst({
    ast_type: "Builtin",
    type: valueType,
    location: get_location(),
    builtin: "ApplyPatch",
    type_parameters: [valueType, patchType],
    arguments: [valueAst, patchAst],
  }) as ExprType<T>;
}

/** Compose two patches into a single patch.
 * The result is a patch that has the same effect as applying `first` then `second`.
 * @throws East runtime error if the patches are incompatible (second expects different intermediate state)
 */
export function composePatch<T extends EastType>(first: Expr<PatchTypeOf<T>>, second: Expr<PatchTypeOf<T>>, type: T): ExprType<PatchTypeOf<T>> {
  const firstAst = Expr.ast(first);
  const secondAst = Expr.ast(second);
  const valueType = type as EastType;
  const patchType = PatchType(valueType);
  return fromAst({
    ast_type: "Builtin",
    type: patchType,
    location: get_location(),
    builtin: "ComposePatch",
    type_parameters: [valueType, patchType],
    arguments: [firstAst, secondAst],
  }) as ExprType<PatchTypeOf<T>>;
}

/** Invert a patch, producing a patch that undoes the original.
 * Applying the inverted patch to the "after" value produces the "before" value.
 */
export function invertPatch<T extends EastType>(patch: Expr<PatchTypeOf<T>>, type: T): ExprType<PatchTypeOf<T>> {
  const patchAst = Expr.ast(patch);
  const valueType = type as EastType;
  const patchType = PatchType(valueType);
  return fromAst({
    ast_type: "Builtin",
    type: patchType,
    location: get_location(),
    builtin: "InvertPatch",
    type_parameters: [valueType, patchType],
    arguments: [patchAst],
  }) as ExprType<PatchTypeOf<T>>;
}

/** Callable helper type for synchronous platform functions. */
export type PlatformDefinition<Inputs extends EastType[], Output extends EastType> = ((...args: { [K in keyof Inputs]: SubtypeExprOrValue<Inputs[K]> }) => ExprType<Output>) & {
  implement: (fn: (...args: { [K in keyof Inputs]: ValueTypeOf<Inputs[K]> }) => Output extends NullType ? null | undefined | void : ValueTypeOf<Output>) => PlatformFunction,
}

/** Options for defining platform functions. */
export interface PlatformOptions {
  /**
   * When true, compilation succeeds even if the platform function is not provided.
   * A runtime error will be thrown if the function is called without an implementation.
   * This is useful for platform functions that may not be available in all environments.
   *
   * @default false
   */
  optional?: boolean;
}

/** Create a callable helper to invoke a synchronous platform function.
 *
 * Platform functions provide access to external capabilities (logging, I/O, database access, etc.)
 * that East code can call. They are defined by the platform when compiling and executing East IR.
 *
 * @param name - The name of the platform function
 * @param input_types - Array of input parameter types for the platform function
 * @param output_type - The return type of the platform function
 * @param options - Optional configuration for the platform function
 * @returns A callable function that creates Platform AST nodes when invoked
 *
 * @see {@link asyncPlatform} for defining asynchronous platform functions (that return `Promise`s)
 *
 * @example
 * ```ts
// Define a platform function helper for logging
const log = East.platform("log", [StringType], NullType);

// Use it in East code
const myFunction = East.function([], NullType, ($) => {
  $(log("Hello, world!"));
  $.return(null);
});

// Provide the implementation when compiling
const platform = [
  log.implement((message: string) => console.log(message)),
];
const compiled = myFunction.toIR().compile(platform);
compiled(); // Logs "Hello, world!" to the console
 * ```
 *
 * @example
 * ```ts
// Define an optional platform function that may not be available
const analytics = East.platform("analytics", [StringType], NullType, { optional: true });

// This compiles even without providing an analytics implementation
// If called at runtime without implementation, it throws an error
 * ```
 */
export function platform<const Inputs extends EastType[], Output extends EastType>(
  name: string,
  input_types: Inputs,
  output_type: Output,
  options: PlatformOptions = {},
): PlatformDefinition<Inputs, Output> {
  const isOptional = options.optional ?? false;

  const fn = (...args: any[]): any => {
    if (args.length !== input_types.length) {
      throw new Error(`Platform function ${name} expected ${input_types.length} arguments, got ${args.length}`);
    }

    const argAsts = args.map((arg, index) => {
      const expectedType = input_types[index]!;
      let ast = valueOrExprToAstTyped(arg, expectedType);

      if (ast.type.type === "Never") {
        throw new Error(`Platform function ${name} argument ${index} expected type ${printType(expectedType)}, got Never type`);
      }
      if (!isTypeEqual(ast.type, expectedType)) {
        if (!isSubtype(ast.type, expectedType)) {
          throw new Error(`Platform function ${name} argument ${index} expected type ${printType(expectedType)}, got ${printType(ast.type)}`);
        }
        // Insert implicit cast
        ast = {
          ast_type: "As",
          type: expectedType,
          location: get_location(),
          value: ast,
        }
      }

      return ast;
    });

    return fromAst({
      ast_type: "Platform",
      type: output_type,
      location: get_location(),
      name: name,
      type_parameters: [],
      arguments: argAsts,
      async: false,
      optional: isOptional,
    }) as ExprType<Output>;
  };

  fn.implement = (fnImpl: (...args: any[]) => any) => {
    // Convert types from EastType to EastTypeValue once at implementation time
    const inputsAsValues = input_types.map(t => toEastTypeValue(t));
    const outputAsValue = toEastTypeValue(output_type);

    if (output_type.type === "Null") {
      return {
        name,
        inputs: inputsAsValues,
        output: outputAsValue,
        type: 'sync' as const,
        fn: (...args: any[]) => { fnImpl(...args); return null; },
      };
    } else {
      return {
        name,
        inputs: inputsAsValues,
        output: outputAsValue,
        type: 'sync' as const,
        fn: fnImpl,
      };
    }
  }

  return fn;
}

/** Callable helper type for asynchronous platform functions. */
export type AsyncPlatformDefinition<Inputs extends EastType[], Output extends EastType> = ((...args: { [K in keyof Inputs]: SubtypeExprOrValue<Inputs[K]> }) => ExprType<Output>) & {
  implement: (fn: (...args: { [K in keyof Inputs]: ValueTypeOf<Inputs[K]> }) => Output extends NullType ? Promise<null | undefined | void> : Promise<ValueTypeOf<Output>>) => PlatformFunction,
}


/** Create a callable helper to invoke an asynchronous platform function.
 *
 * Platform functions provide access to external capabilities (logging, I/O, database access, etc.)
 * that East code can call. They are defined by the platform when compiling and executing East IR.
 *
 * @param name - The name of the asynchronous platform function
 * @param input_types - Array of input parameter types for the platform function
 * @param output_type - The return type of the platform function
 * @param options - Optional configuration for the platform function
 * @returns A callable function that creates Platform AST nodes when invoked
 *
 * @see {@link platform} for defining synchronous platform functions
 *
 * @example
 * ```ts
// Define a platform function for reading files as a string
const readFile = East.asyncPlatform("readFile", [StringType], StringType);

// Use it in East code
const myFunction = East.asyncFunction([], StringType, ($) => {
  $.return(readFile("data.txt"));
});

// Provide the (async) implementation when compiling
const platform = [
  readFile.implement((filename: string) => fs.promises.readFile(filename, 'utf-8')),
];
const compiled = myFunction.toIR().compile(platform);
compiled(); // Returns file contents
 * ```
 */
export function asyncPlatform<const Inputs extends EastType[], Output extends EastType>(
  name: string,
  input_types: Inputs,
  output_type: Output,
  options: PlatformOptions = {},
): AsyncPlatformDefinition<Inputs, Output> {
  const isOptional = options.optional ?? false;

  const fn = (...args: any[]): any => {
    if (args.length !== input_types.length) {
      throw new Error(`Platform function ${name} expected ${input_types.length} arguments, got ${args.length}`);
    }

    const argAsts = args.map((arg, index) => {
      const expectedType = input_types[index]!;
      let ast = valueOrExprToAstTyped(arg, expectedType);

      if (ast.type.type === "Never") {
        throw new Error(`Platform function ${name} argument ${index} expected type ${printType(expectedType)}, got Never type`);
      }
      if (!isTypeEqual(ast.type, expectedType)) {
        if (!isSubtype(ast.type, expectedType)) {
          throw new Error(`Platform function ${name} argument ${index} expected type ${printType(expectedType)}, got ${printType(ast.type)}`);
        }
        // Insert implicit cast
        ast = {
          ast_type: "As",
          type: expectedType,
          location: get_location(),
          value: ast,
        }
      }

      return ast;
    });

    return fromAst({
      ast_type: "Platform",
      type: output_type,
      location: get_location(),
      name: name,
      type_parameters: [],
      arguments: argAsts,
      async: true,
      optional: isOptional,
    }) as ExprType<Output>;
  };

  fn.implement = (fnImpl: (...args: any[]) => any) => {
    // Convert types from EastType to EastTypeValue once at implementation time
    const inputsAsValues = input_types.map(t => toEastTypeValue(t));
    const outputAsValue = toEastTypeValue(output_type);

    if (output_type.type === "Null") {
      return {
        name,
        inputs: inputsAsValues,
        output: outputAsValue,
        type: 'async' as const,
        fn: async (...args: any[]) => { await fnImpl(...args); return null; },
      };
    } else {
      return {
        name,
        inputs: inputsAsValues,
        output: outputAsValue,
        type: 'async' as const,
        fn: fnImpl,
      };
    }
  }

  return fn;
}


// =============================================================================
// Generic Platform Functions
// =============================================================================

// Helper to find index of a string in a tuple
type IndexOf<T extends readonly string[], S extends string, Acc extends unknown[] = []> =
  T extends readonly [infer First, ...infer Rest extends readonly string[]]
    ? First extends S
      ? Acc['length']
      : IndexOf<Rest, S, [...Acc, unknown]>
    : never;

// Helper type to zip parameter names with type arguments into a record
// E.g., ZipToRecord<["A", "B"], [IntegerType, StringType]> = { A: IntegerType, B: StringType }
type ZipToRecord<Names extends readonly string[], Types extends readonly unknown[]> = {
  [K in Names[number]]: Types[IndexOf<Names, K>]
};

// Type-level substitution: replaces string keys with actual types from TypeArgs
type ApplyTypeArgs<TypeArgs extends Record<string, EastType>, T> =
  T extends keyof TypeArgs ? TypeArgs[T] :
  T extends RefType<infer U> ? RefType<ApplyTypeArgs<TypeArgs, U>> :
  T extends ArrayType<infer U> ? ArrayType<ApplyTypeArgs<TypeArgs, U>> :
  T extends SetType<infer K> ? SetType<ApplyTypeArgs<TypeArgs, K>> :
  T extends DictType<infer K, infer V> ? DictType<ApplyTypeArgs<TypeArgs, K>, ApplyTypeArgs<TypeArgs, V>> :
  T extends StructType<infer Fields> ? StructType<{ [K in keyof Fields]: ApplyTypeArgs<TypeArgs, Fields[K]> }> :
  // RecursiveType must be checked BEFORE VariantType to preserve the wrapper
  T extends RecursiveType<infer U> ? RecursiveType<ApplyTypeArgs<TypeArgs, U>> :
  T extends VariantType<infer Cases> ? VariantType<{ [K in keyof Cases]: ApplyTypeArgs<TypeArgs, Cases[K]> }> :
  T extends RecursiveTypeMarker ? T : // Self-reference - leave alone
  T extends FunctionType<infer Ins, infer Out> ? FunctionType<
    { [K in keyof Ins]: ApplyTypeArgs<TypeArgs, Ins[K]> },
    ApplyTypeArgs<TypeArgs, Out>
  > :
  T;

// Runtime type substitution function
function applyTypeArgs<T extends EastType | string>(
  typeArgs: Record<string, EastType>,
  t: T
): EastType {
  if (typeof t === 'string') {
    const ret = typeArgs[t];
    if (ret === undefined) {
      throw new Error(`Unexpected type argument ${t}`);
    }
    return ret;
  } else if (t.type === "Ref") {
    return { type: "Ref", value: applyTypeArgs(typeArgs, (t as any).value) } as EastType;
  } else if (t.type === "Array") {
    return { type: "Array", value: applyTypeArgs(typeArgs, (t as any).value) } as EastType;
  } else if (t.type === "Set") {
    return { type: "Set", key: applyTypeArgs(typeArgs, (t as any).key) } as EastType;
  } else if (t.type === "Dict") {
    return { type: "Dict", key: applyTypeArgs(typeArgs, (t as any).key), value: applyTypeArgs(typeArgs, (t as any).value) } as EastType;
  } else if (t.type === "Struct") {
    const newFields: Record<string, EastType> = {};
    for (const k in (t as any).fields) {
      newFields[k] = applyTypeArgs(typeArgs, (t as any).fields[k]);
    }
    return { type: "Struct", fields: newFields } as EastType;
  } else if (t.type === "Variant") {
    const newCases: Record<string, EastType> = {};
    for (const k in (t as any).cases) {
      newCases[k] = applyTypeArgs(typeArgs, (t as any).cases[k]);
    }
    return { type: "Variant", cases: newCases } as EastType;
  } else if (t.type === "Function") {
    const newInputs = (t as any).inputs.map((inputType: any) => applyTypeArgs(typeArgs, inputType));
    const newOutput = applyTypeArgs(typeArgs, (t as any).output);
    return { type: "Function", inputs: newInputs, output: newOutput } as EastType;
  } else if (t.type === "Recursive") {
    if ((t as any).node === undefined) {
      // RecursiveTypeMarker (self-reference) - leave alone
      return t as EastType;
    }
    return { type: "Recursive", node: applyTypeArgs(typeArgs, (t as any).node) } as EastType;
  } else {
    return t as EastType;
  }
}

// Callable type: type args as array, then value args
type GenericPlatformCallable<
  TParams extends readonly string[],
  Inputs extends readonly (EastType | string)[],
  Output extends EastType | string
> = <TypeArgs extends readonly EastType[] & { [K in keyof TParams]: EastType }>(
  type_args: TypeArgs,
  ...args: { [K in keyof Inputs]: SubtypeExprOrValue<ApplyTypeArgs<
    ZipToRecord<TParams, TypeArgs>,
    Inputs[K]
  >> }
) => ExprType<ApplyTypeArgs<ZipToRecord<TParams, TypeArgs>, Output>>;

/** Definition for a generic platform function with `.implement` method.
 *
 * The `implement` method receives a factory function where:
 * - Type parameters are `EastTypeValue` (the runtime representation of types)
 * - Value arguments are `unknown` (cast to specific types as needed based on the type parameters)
 *
 * Use helpers like `printFor(T)` to work with type-dependent behavior.
 */
export type GenericPlatformDefinition<
  TParams extends readonly string[],
  Inputs extends readonly (EastType | string)[],
  Output extends EastType | string
> = GenericPlatformCallable<TParams, Inputs, Output> & {
  implement: (factory: (...typeParams: { [K in keyof TParams]: EastTypeValue }) => (...args: unknown[]) => unknown) => PlatformFunction;
};

/** Create a callable helper to invoke a generic (polymorphic) platform function.
 *
 * Generic platform functions allow you to define platform functions with type parameters,
 * similar to how builtins work. The type parameters are passed at call time and flow
 * through to the implementation.
 *
 * @param name - The name of the platform function
 * @param typeParams - Array of type parameter names (e.g., `["T", "U"]`)
 * @param inputs - Array of input types, can contain string placeholders like `"T"`
 * @param output - Output type, can be a string placeholder like `"T"`
 * @returns A callable function that creates Platform AST nodes when invoked
 *
 * @example
 * ```ts
 * // Define a generic log function
 * const log = East.genericPlatform(
 *   "log",
 *   ["T"],
 *   ["T"],      // Input is type parameter T
 *   NullType
 * );
 *
 * // Use it in East code - type args as array, then value args
 * const myFunction = East.function([StringType], NullType, ($, s) => {
 *   $(log([StringType], s));
 * });
 *
 * // Implementation receives type params as a factory
 * const platform = [
 *   log.implement((T) => (value) => {
 *     console.log(printFor(T)(value));
 *     return null;
 *   }),
 * ];
 * ```
 *
 * @example
 * ```ts
 * // Define a generic map function with 2 type parameters
 * const map = East.genericPlatform(
 *   "map",
 *   ["T", "U"],
 *   ["T", FunctionType(["T"], "U")],  // String placeholders in nested types
 *   "U"
 * );
 *
 * // Call with type args array, then value arguments
 * map([StringType, IntegerType], myString, myMapperFn)
 * ```
 */
export function genericPlatform<
  const TParams extends readonly string[],
  const Inputs extends readonly (EastType | string)[],
  Output extends EastType | string
>(
  name: string,
  typeParams: TParams,
  inputs: Inputs,
  output: Output,
  options: PlatformOptions = {},
): GenericPlatformDefinition<TParams, Inputs, Output> {
  const numTypeParams = typeParams.length;
  const isOptional = options.optional ?? false;

  const fn = (type_args: EastType[], ...valueArgs: any[]): any => {
    // Validate type args array
    if (!Array.isArray(type_args)) {
      throw new Error(
        `Generic platform function '${name}' expects type arguments as an array, ` +
        `got ${typeof type_args}`
      );
    }

    // Validate type args count
    if (type_args.length !== numTypeParams) {
      throw new Error(
        `Generic platform function '${name}' expects ${numTypeParams} type parameters, ` +
        `got ${type_args.length}`
      );
    }

    // Validate type args are EastTypes
    for (let i = 0; i < numTypeParams; i++) {
      const typeArg = type_args[i];
      if (!typeArg || typeof typeArg !== 'object' || !('type' in typeArg)) {
        throw new Error(
          `Generic platform function '${name}' expects type parameter ${i + 1} ` +
          `(${typeParams[i]}) to be an EastType`
        );
      }
    }

    // Build type argument map
    const typeArgMap: Record<string, EastType> = {};
    typeParams.forEach((param, idx) => {
      typeArgMap[param] = type_args[idx]!;
    });

    // Apply type substitution to get concrete input/output types
    const inputTypes = inputs.map(t => applyTypeArgs(typeArgMap, t));
    const outputType = applyTypeArgs(typeArgMap, output);

    // Validate value args count
    if (valueArgs.length !== inputTypes.length) {
      throw new Error(
        `Generic platform function '${name}' expects ${inputTypes.length} ` +
        `value arguments, got ${valueArgs.length}`
      );
    }

    // Convert value args to AST with type validation and implicit casts
    const argAsts = valueArgs.map((arg, index) => {
      const expectedType = inputTypes[index]!;
      let ast = valueOrExprToAstTyped(arg, expectedType);

      if (ast.type.type === "Never") {
        throw new Error(`Generic platform function ${name} argument ${index + 1} expected type ${printType(expectedType)}, got Never type`);
      }
      if (!isTypeEqual(ast.type, expectedType)) {
        if (!isSubtype(ast.type, expectedType)) {
          throw new Error(`Generic platform function ${name} argument ${index + 1} expected type ${printType(expectedType)}, got ${printType(ast.type)}`);
        }
        // Insert implicit cast
        ast = {
          ast_type: "As",
          type: expectedType,
          location: get_location(),
          value: ast,
        }
      }

      return ast;
    });

    // Create PlatformAST with type_parameters
    return fromAst({
      ast_type: "Platform",
      type: outputType,
      location: get_location(),
      name: name,
      type_parameters: type_args,
      arguments: argAsts,
      async: false,
      optional: isOptional,
    });
  };

  fn.implement = (
    factory: (...typeParams: any[]) => (...args: any[]) => any
  ): PlatformFunction => {
    return {
      name,
      type_parameters: [...typeParams],
      inputs: [],  // Computed at call time via inputsFn
      output: toEastTypeValue(NullType),  // Placeholder
      inputsFn: (...tps: EastTypeValue[]) => {
        const typeArgMap: Record<string, EastTypeValue> = {};
        typeParams.forEach((param, idx) => {
          typeArgMap[param] = tps[idx]!;
        });
        return inputs.map(t => {
          if (typeof t === 'string') return typeArgMap[t]!;
          let result: EastType | EastTypeValue = applyTypeArgs(typeArgMap as any, t);
          if (!isVariant(result)) result = toEastTypeValue(result);
          return result as EastTypeValue;
        });
      },
      outputsFn: (...tps: EastTypeValue[]) => {
        const typeArgMap: Record<string, EastTypeValue> = {};
        typeParams.forEach((param, idx) => {
          typeArgMap[param] = tps[idx]!;
        });
        if (typeof output === 'string') return typeArgMap[output]!;
        let result: EastType | EastTypeValue = applyTypeArgs(typeArgMap as any, output);
        if (!isVariant(result)) result = toEastTypeValue(result);
        return result as EastTypeValue;
      },
      type: 'sync' as const,
      fn: factory,
    };
  };

  return fn as GenericPlatformDefinition<TParams, Inputs, Output>;
}

// Async callable type: type args as array, then value args
type AsyncGenericPlatformCallable<
  TParams extends readonly string[],
  Inputs extends readonly (EastType | string)[],
  Output extends EastType | string
> = <TypeArgs extends readonly EastType[] & { [K in keyof TParams]: EastType }>(
  type_args: TypeArgs,
  ...args: { [K in keyof Inputs]: SubtypeExprOrValue<ApplyTypeArgs<
    ZipToRecord<TParams, TypeArgs>,
    Inputs[K]
  >> }
) => ExprType<ApplyTypeArgs<ZipToRecord<TParams, TypeArgs>, Output>>;

/** Definition for an async generic platform function with `.implement` method.
 *
 * The `implement` method receives a factory function where:
 * - Type parameters are `EastTypeValue` (the runtime representation of types)
 * - Value arguments are `unknown` (cast to specific types as needed based on the type parameters)
 *
 * Use helpers like `printFor(T)` to work with type-dependent behavior.
 */
export type AsyncGenericPlatformDefinition<
  TParams extends readonly string[],
  Inputs extends readonly (EastType | string)[],
  Output extends EastType | string
> = AsyncGenericPlatformCallable<TParams, Inputs, Output> & {
  implement: (factory: (...typeParams: { [K in keyof TParams]: EastTypeValue }) => (...args: unknown[]) => Promise<unknown>) => PlatformFunction;
};

/** Create a callable helper to invoke an asynchronous generic (polymorphic) platform function.
 *
 * This is the async variant of `genericPlatform`. The implementation factory should return
 * an async function.
 *
 * @param name - The name of the platform function
 * @param typeParams - Array of type parameter names (e.g., `["T", "U"]`)
 * @param inputs - Array of input types, can contain string placeholders like `"T"`
 * @param output - Output type, can be a string placeholder like `"T"`
 * @returns A callable function that creates Platform AST nodes when invoked
 *
 * @see {@link genericPlatform} for synchronous generic platform functions
 *
 * @example
 * ```ts
 * // Define an async generic fetch function
 * const fetchAs = East.asyncGenericPlatform(
 *   "fetchAs",
 *   ["T"],
 *   [StringType],  // URL input
 *   "T"            // Returns parsed value of type T
 * );
 *
 * // Implementation receives type params and returns async function
 * const platform = [
 *   fetchAs.implement((T) => async (url) => {
 *     const response = await fetch(url);
 *     return parseFor(T)(await response.text());
 *   }),
 * ];
 * ```
 */
export function asyncGenericPlatform<
  const TParams extends readonly string[],
  const Inputs extends readonly (EastType | string)[],
  Output extends EastType | string
>(
  name: string,
  typeParams: TParams,
  inputs: Inputs,
  output: Output,
  options: PlatformOptions = {},
): AsyncGenericPlatformDefinition<TParams, Inputs, Output> {
  const numTypeParams = typeParams.length;
  const isOptional = options.optional ?? false;

  const fn = (type_args: EastType[], ...valueArgs: any[]): any => {
    // Validate type args array
    if (!Array.isArray(type_args)) {
      throw new Error(
        `Generic platform function '${name}' expects type arguments as an array, ` +
        `got ${typeof type_args}`
      );
    }

    // Validate type args count
    if (type_args.length !== numTypeParams) {
      throw new Error(
        `Generic platform function '${name}' expects ${numTypeParams} type parameters, ` +
        `got ${type_args.length}`
      );
    }

    // Validate type args are EastTypes
    for (let i = 0; i < numTypeParams; i++) {
      const typeArg = type_args[i];
      if (!typeArg || typeof typeArg !== 'object' || !('type' in typeArg)) {
        throw new Error(
          `Generic platform function '${name}' expects type parameter ${i + 1} ` +
          `(${typeParams[i]}) to be an EastType`
        );
      }
    }

    // Build type argument map
    const typeArgMap: Record<string, EastType> = {};
    typeParams.forEach((param, idx) => {
      typeArgMap[param] = type_args[idx]!;
    });

    // Apply type substitution to get concrete input/output types
    const inputTypes = inputs.map(t => applyTypeArgs(typeArgMap, t));
    const outputType = applyTypeArgs(typeArgMap, output);

    // Validate value args count
    if (valueArgs.length !== inputTypes.length) {
      throw new Error(
        `Generic platform function '${name}' expects ${inputTypes.length} ` +
        `value arguments, got ${valueArgs.length}`
      );
    }

    // Convert value args to AST with type validation and implicit casts
    const argAsts = valueArgs.map((arg, index) => {
      const expectedType = inputTypes[index]!;
      let ast = valueOrExprToAstTyped(arg, expectedType);

      if (ast.type.type === "Never") {
        throw new Error(`Generic platform function ${name} argument ${index + 1} expected type ${printType(expectedType)}, got Never type`);
      }
      if (!isTypeEqual(ast.type, expectedType)) {
        if (!isSubtype(ast.type, expectedType)) {
          throw new Error(`Generic platform function ${name} argument ${index + 1} expected type ${printType(expectedType)}, got ${printType(ast.type)}`);
        }
        // Insert implicit cast
        ast = {
          ast_type: "As",
          type: expectedType,
          location: get_location(),
          value: ast,
        }
      }

      return ast;
    });

    // Create PlatformAST with type_parameters and async: true
    return fromAst({
      ast_type: "Platform",
      type: outputType,
      location: get_location(),
      name: name,
      type_parameters: type_args,
      arguments: argAsts,
      async: true,
      optional: isOptional,
    });
  };

  fn.implement = (
    factory: (...typeParams: any[]) => (...args: any[]) => Promise<any>
  ): PlatformFunction => {
    return {
      name,
      type_parameters: [...typeParams],
      inputs: [],  // Computed at call time via inputsFn
      output: toEastTypeValue(NullType),  // Placeholder
      inputsFn: (...tps: EastTypeValue[]) => {
        const typeArgMap: Record<string, EastTypeValue> = {};
        typeParams.forEach((param, idx) => {
          typeArgMap[param] = tps[idx]!;
        });
        return inputs.map(t => {
          if (typeof t === 'string') return typeArgMap[t]!;
          let result: EastType | EastTypeValue = applyTypeArgs(typeArgMap as any, t);
          if (!isVariant(result)) result = toEastTypeValue(result);
          return result as EastTypeValue;
        });
      },
      outputsFn: (...tps: EastTypeValue[]) => {
        const typeArgMap: Record<string, EastTypeValue> = {};
        typeParams.forEach((param, idx) => {
          typeArgMap[param] = tps[idx]!;
        });
        if (typeof output === 'string') return typeArgMap[output]!;
        let result: EastType | EastTypeValue = applyTypeArgs(typeArgMap as any, output);
        if (!isVariant(result)) result = toEastTypeValue(result);
        return result as EastTypeValue;
      },
      type: 'async' as const,
      fn: factory,
    };
  };

  return fn as AsyncGenericPlatformDefinition<TParams, Inputs, Output>;
}


/** A helper for building blocks of code.
 * Methods like `let`, `if`, `for` etc are available on the builder.
 * You can also add expressions (having side effects) directly by calling the builder as a function.
 */
export type BlockBuilder<Ret> = ((expr: Expr) => void) & {
  /** @internal */
  statements: AST[],

  /** @internal */
  type(): EastType,

  /** Define a new variable with a given value, and optionally a type.
   * The variable may not be reassigned later (use `let` for that).
   * However the value itself may be mutable (e.g. an array), and internally modified.
  */
  const: (<T>(expr: SubtypeExprOrValue<NoInfer<T>>, type: T) => ExprType<T>) & (<V>(expr: V) => ExprType<TypeOf<V>>),
  /** Define a new variable with a given value, and optionally a type.
   * The value may be reassigned later with `assign`.
   */
  let: (<T>(expr: SubtypeExprOrValue<NoInfer<T>>, type: T) => ExprType<T>) & (<V>(expr: V) => ExprType<TypeOf<V>>),
  /** Reassign a variable defined with `let` to a new value. */
  assign: (<E extends Expr<any>>(variable: E, value: SubtypeExprOrValue<E[TypeSymbol]>) => ExprType<NullType>),
  /** Return a value immediately from the current function */
  return: (value: SubtypeExprOrValue<Ret>) => void,
  /** Break immediately from the indicated loop */
  break: (label: Label) => void,
  /** Continue immediately with the next iteration of the indicated loop */
  continue: (label: Label) => void,
  /** Perform logic if a condition is true */
  if: (predicate: BooleanExpr | boolean, true_branch: ($: BlockBuilder<Ret>) => void | Expr) => IfElseExpr<Ret>,
  /** Perform logic on different possible variants. For each variant tag, the associated data is unwrapped and provided to the branch. */
  match: <Cases extends Record<string, any>>(variant: Expr<VariantType<Cases>>, cases: { [K in keyof Cases]?: ($: BlockBuilder<Ret>, data: ExprType<Cases[K]>) => (void | Expr) }) => void,
  /** Loop while a condition is true */
  while: (predicate: BooleanExpr | boolean, body: ($: BlockBuilder<Ret>, label: Label) => (void | Expr)) => void,
  /** Loop over the values in a collection (array, set or dictionary) */
  for:
    & (<T>(array: ArrayExpr<T>, body: ($: BlockBuilder<Ret>, value: ExprType<T>, key: IntegerExpr, label: Label) => void) => void)
    & (<K>(array: SetExpr<K>, body: ($: BlockBuilder<Ret>, key: ExprType<K>, label: Label) => void) => void)
    & (<K, T>(array: DictExpr<K, T>, body: ($: BlockBuilder<Ret>, value: ExprType<T>, key: ExprType<K>, label: Label) => void) => void)
  /** Throw an error immediately with a given error message. */
  error: (message: StringExpr | string, location?: Location[]) => NeverExpr,
  /** Run some code and catch any errors that occur. */
  try: (try_block: ($: BlockBuilder<Ret>) => (void | Expr)) => TryCatchExpr<Ret>,
}

export const BlockBuilder = <Ret>(return_type: Ret): BlockBuilder<Ret> => {
  const statements: AST[] = [];

  const $: BlockBuilder<Ret> = ((expr: Expr): void => {
    const ast = Expr.ast(expr)
    statements.push(ast);
  }) as any;

  $.statements = statements;

  $.type = () => {
    if (statements.length === 0) {
      return NullType;
    } else {
      return statements[statements.length - 1]!.type;
    }
  };

  $.const = ((value: any, type?: EastType): Expr<any> => {
    if (isTypeEqual($.type(), NeverType)) {
      throw new Error(`Unreachable statement detected at ${printLocations(get_location())}`);
    }

    let ast: AST;
    if (value instanceof Expr) {
      if (type && !isSubtype(Expr.type(value), type)) {
        throw new Error(`Expression expected to have type ${printType(type)} but got type ${printType(Expr.type(value))}`);
      }
      ast = Expr.ast(value);
    } else {
      ast = type ? valueOrExprToAstTyped(value, type) : valueOrExprToAst(value);
    }

    const variable: VariableAST = {
      ast_type: "Variable",
      type: type ?? ast.type,
      location: get_location(),
      mutable: false,
    };

    statements.push({
      ast_type: "Let",
      type: NullType,
      location: get_location(),
      variable,
      value: ast,
    });

    return fromAst(variable);
  }) as any;

  $.let = ((value: any, type?: EastType): Expr<any> => {
    if (isTypeEqual($.type(), NeverType)) {
      throw new Error(`Unreachable statement detected at ${printLocations(get_location())}`);
    }

    let ast: AST;
    if (value instanceof Expr) {
      if (type && !isSubtype(Expr.type(value), type)) {
        throw new Error(`Expression expected to have type ${printType(type)} but got type ${printType(Expr.type(value))}`);
      }
      ast = Expr.ast(value);
    } else {
      ast = type ? valueOrExprToAstTyped(value, type) : valueOrExprToAst(value);
    }

    const variable: VariableAST = {
      ast_type: "Variable",
      type: type ?? ast.type,
      location: get_location(),
      mutable: true,
    };

    statements.push({
      ast_type: "Let",
      type: NullType,
      location: get_location(),
      variable,
      value: ast,
    });

    return fromAst(variable);
  }) as any;

  $.assign = (<T>(variable: Expr<T>, value: SubtypeExprOrValue<NoInfer<T>>): NullExpr => {
    if (isTypeEqual($.type(), NeverType)) {
      throw new Error(`Unreachable statement detected at ${printLocations(get_location())}`);
    }

    let v: AST = Expr.ast(variable);

    // Handle RecursiveType variables which are auto-unwrapped by fromAst
    if (v.ast_type === "UnwrapRecursive") {
      v = v.value;
    }

    if (v.ast_type !== "Variable") {
      throw new Error("Can only assign to a variable");
    }

    if (!v.mutable) {
      throw new Error(`Cannot assign to variable defined at ${printLocations(v.location)} defined as const`);
    }

    const ast_value = value instanceof Expr ? Expr.ast(value) : valueOrExprToAstTyped(value, v.type);

    const ast: AST = {
      ast_type: "Assign",
      type: NullType,
      location: get_location(),
      variable: v,
      value: ast_value,
    }

    statements.push(ast);

    return fromAst(ast) as NullExpr;
  }) as any;

  // TODO if/when we introduce recursion, can we somehow get benefit from the typing?
  $.return = (expr: any): NeverExpr => {
    if (isTypeEqual($.type(), NeverType)) {
      throw new Error(`Unreachable statement detected at ${printLocations(get_location())}`);
    }

    const expAst = expr instanceof Expr ? Expr.ast(expr) : valueOrExprToAst(expr);

    if (!isSubtype(expAst.type, return_type as EastType)) {
      throw new Error(`Return expected to have type ${printType(return_type as EastType)}, got ${printType(expAst.type)}`);
    }

    // Deduplicate: if the expression is already the last statement (e.g., from $()),
    // don't push it again - just wrap it in the Return
    const exprAstRef = expr instanceof Expr ? Expr.ast(expr) : null;
    if (exprAstRef !== null && statements.length > 0 && statements[statements.length - 1] === exprAstRef) {
      statements.pop();
    }

    const ast = {
      ast_type: "Return" as const,
      type: NeverType,
      location: get_location(),
      value: expAst
    };
    statements.push(ast);

    return fromAst(ast) as NeverExpr;
  };

  $.break = (label: Label): NeverExpr => {
    if (isTypeEqual($.type(), NeverType)) {
      throw new Error(`Unreachable statement detected at ${printLocations(get_location())}`);
    }

    const ast = {
      ast_type: "Break" as const,
      type: NeverType,
      location: get_location(),
      label,
    };
    
    statements.push(ast);

    return fromAst(ast) as NeverExpr;
  };

  $.continue = (label: Label): NeverExpr => {
    if (isTypeEqual($.type(), NeverType)) {
      throw new Error(`Unreachable statement detected at ${printLocations(get_location())}`);
    }

    const ast = {
      ast_type: "Continue" as const,
      type: NeverType,
      location: get_location(),
      label,
    };
    statements.push(ast);

    return fromAst(ast) as NeverExpr;
  };

  $.if = (predicate: BooleanExpr | boolean, true_branch: ($: BlockBuilder<Ret>) => any): IfElseExpr<Ret> => {
    if (isTypeEqual($.type(), NeverType)) {
      throw new Error(`Unreachable statement detected at ${printLocations(get_location())}`);
    }

    const predicateAst = predicate instanceof Expr ? Expr.ast(predicate) : valueOrExprToAstTyped(predicate, BooleanType);
    if (predicateAst.type.type !== "Boolean") {
      throw new Error(`if predicate expected to have type Boolean, got ${printType(predicateAst.type)}`);
    }
    predicate = fromAst(predicateAst) as BooleanExpr;

    const $_true = BlockBuilder<Ret>(return_type);
    const ret_true = true_branch($_true);
    const true_stmts = $_true.statements;
    if (ret_true !== undefined) {
      const ret_ast = valueOrExprToAst(ret_true);
      if (true_stmts.length === 0 || true_stmts[true_stmts.length - 1] !== ret_ast) { // avoid duplicate statements
        true_stmts.push(ret_ast);
      }
    }

    let true_ast: AST;
    if (true_stmts.length === 0) {
      true_ast = { ast_type: "Value", type: NullType, location: get_location(), value: null };
    } else if (true_stmts.length === 1 && isSubtype(true_stmts[0]!.type, NullType)) {
      true_ast = true_stmts[0]!;
    } else {
      if (!isSubtype(true_stmts[true_stmts.length - 1]!.type, NullType)) {
        true_stmts.push({ ast_type: "Value", type: NullType, location: get_location(), value: null });
      }
      true_ast = {
        ast_type: "Block",
        type: true_stmts[true_stmts.length - 1]!.type,
        location: get_location(),
        statements: true_stmts,
      }
    }
    const if_else_ast: AST = {
      ast_type: "IfElse",
      type: NullType,
      location: get_location(),
      ifs: [{
        predicate: Expr.ast(predicate),
        body: true_ast,
      }],
      else_body: { ast_type: "Value", type: NullType, location: get_location(), value: null },
    };

    statements.push(if_else_ast);

    return new IfElseExpr(if_else_ast, return_type);
  };

  $.match = <Cases extends Record<string, any>>(variant: Expr<VariantType<Cases>>, cases: { [K in keyof Cases]?: ($: BlockBuilder<Ret>, data: ExprType<Cases[K]>) => any }): NullExpr => {
    if (isTypeEqual($.type(), NeverType)) {
      throw new Error(`Unreachable statement detected at ${printLocations(get_location())}`);
    }

    if (Expr.type(variant).type !== "Variant") {
      throw new Error(`match not defined over ${printType(Expr.type(variant))}`)
    }

    const cases_out: Record<string, { variable: VariableAST, body: AST }> = {};
    let out_type = NullType;

    for (const [k, t] of Object.entries(Expr.type(variant).cases as Record<string, EastType>)) {
      const f = cases[k];

      const data_variable: VariableAST = {
        ast_type: "Variable",
        type: t,
        location: get_location(),
        mutable: false,
      };


      if (f === undefined) {
        cases_out[k] = { variable: data_variable, body: { ast_type: "Value", type: NullType, location: get_location(), value: null } };
      } else {
        const data = fromAst(data_variable) as ExprType<Cases[string]>;

        const $ = BlockBuilder<Ret>(return_type);
        const ret = f($, data);
        const stmts = $.statements;
        if (ret !== undefined) {
          const ret_ast = valueOrExprToAst(ret);
          if (stmts.length === 0 || stmts[stmts.length - 1] !== ret_ast) { // avoid duplicate statements
            stmts.push(ret_ast);
          }
        }

        let expr: AST;
        if (stmts.length === 0) {
          expr = { ast_type: "Value", type: NullType, location: get_location(), value: null };
        } else if (stmts.length === 1 && isSubtype(stmts[0]!.type, NullType)) {
          expr = stmts[0]!;
        } else {
          if (!isSubtype(stmts[stmts.length - 1]!.type, NullType)) {
            stmts.push({ ast_type: "Value", type: NullType, location: get_location(), value: null });
          }
          expr = {
            ast_type: "Block",
            type: stmts[stmts.length - 1]!.type,
            location: get_location(),
            statements: stmts,
          }
        }

        cases_out[k] = { variable: data_variable, body: expr };
      }
    }

    // TODO do we care if extra case branches exist? (we don't even call the function passed in!)

    const ast = {
      ast_type: "Match" as const,
      type: out_type,
      location: get_location(),
      variant: Expr.ast(variant),
      cases: cases_out,
    }
    statements.push(ast);

    return fromAst(ast) as any;
  };

  $.while = (predicate: BooleanExpr | boolean, body: ($: BlockBuilder<Ret>, label: Label) => (void | Expr)): NullExpr => {
    if (isTypeEqual($.type(), NeverType)) {
      throw new Error(`Unreachable statement detected at ${printLocations(get_location())}`);
    }

    const predicateAst = predicate instanceof Expr ? Expr.ast(predicate) : valueOrExprToAstTyped(predicate, BooleanType);
    if (predicateAst.type.type !== "Boolean") {
      throw new Error(`while predicate expected to have type Boolean, got ${printType(predicateAst.type)}`);
    }

    const label = { location: get_location() };

    const $_body = BlockBuilder<Ret>(return_type);
    const ret = body($_body, label);
    const stmts = $_body.statements;
    if (ret !== undefined) {
      const ret_ast = valueOrExprToAst(ret);
      if (stmts.length === 0 || stmts[stmts.length - 1] !== ret_ast) { // avoid duplicate statements
        stmts.push(ret_ast);
      }
    }

    let expr: AST;
    if (stmts.length === 0) {
      expr = { ast_type: "Value", type: NullType, location: get_location(), value: null };
    } else if (stmts.length === 1 && isSubtype(stmts[0]!.type, NullType)) {
      expr = stmts[0]!;
    } else {
      if (!isSubtype(stmts[stmts.length - 1]!.type, NullType)) {
        stmts.push({ ast_type: "Value", type: NullType, location: get_location(), value: null });
      }
      expr = {
        ast_type: "Block",
        type: stmts[stmts.length - 1]!.type,
        location: get_location(),
        statements: stmts,
      }
    }

    // Note: we could try to look for unconditional loops with NeverType bodies and make the whole statement NeverType
    // However, this would have a false positive on a loop which breaks itself out of the loop, which would continue execution!
    // That is, `while (true) { break }` is valid and continues execution after the loop.

    const ast = {
      ast_type: "While" as const,
      type: NullType,
      location: get_location(),
      predicate: predicateAst,
      label,
      body: expr,
    };
    statements.push(ast);

    return fromAst(ast) as any;
  };

  $.for = ((collection: Expr<EastType>, body: ($: BlockBuilder<Ret>, value: any, key: any, label?: any) => void | Expr): NullExpr => {
    if (isTypeEqual($.type(), NeverType)) {
      throw new Error(`Unreachable statement detected at ${printLocations(get_location())}`);
    }

    if (collection instanceof ArrayExpr) {
      const value_variable: VariableAST = {
        ast_type: "Variable",
        type: Expr.type(collection).value as EastType,
        location: get_location(),
        mutable: false,
      };
      const value = fromAst(value_variable);

      const key_variable: VariableAST = {
        ast_type: "Variable",
        type: IntegerType,
        location: get_location(),
        mutable: false,
      };
      const key = fromAst(key_variable) as IntegerExpr;

      const label = { location: get_location() };

      const $ = BlockBuilder<Ret>(return_type);
      const ret = body($, value, key, label);
      const stmts = $.statements;
      if (ret !== undefined) {
        const ret_ast = valueOrExprToAst(ret);
        if (stmts.length === 0 || stmts[stmts.length - 1] !== ret_ast) { // avoid duplicate statements
          stmts.push(ret_ast);
        }
      }

      let expr: AST;
      if (stmts.length === 0) {
        expr = { ast_type: "Value", type: NullType, location: get_location(), value: null };
      } else if (stmts.length === 1 && isSubtype(stmts[0]!.type, NullType)) {
        expr = stmts[0]!;
      } else {
        if (!isSubtype(stmts[stmts.length - 1]!.type, NullType)) {
          stmts.push({ ast_type: "Value", type: NullType, location: get_location(), value: null });
        }
        expr = {
          ast_type: "Block",
          type: stmts[stmts.length - 1]!.type,
          location: get_location(),
          statements: stmts,
        }
      }

      const ast = {
        ast_type: "ForArray" as const,
        type: NullType,
        location: get_location(),
        label,
        array: Expr.ast(collection),
        key: key_variable,
        value: value_variable,
        body: expr,
      }

      statements.push(ast);

      return fromAst(ast) as any;
    } else if (collection instanceof SetExpr) {
      const key_variable: VariableAST = {
        ast_type: "Variable",
        type: Expr.type(collection).key as EastType,
        location: get_location(),
        mutable: false,
      };
      const key = fromAst(key_variable) as IntegerExpr;

      const label = { location: get_location() };

      const $ = BlockBuilder<Ret>(return_type);
      const ret = body($, key, label);
      const stmts = $.statements;
      if (ret !== undefined) {
        const ret_ast = valueOrExprToAst(ret);
        if (stmts.length === 0 || stmts[stmts.length - 1] !== ret_ast) { // avoid duplicate statements
          stmts.push(ret_ast);
        }
      }

      let expr: AST;
      if (stmts.length === 0) {
        expr = { ast_type: "Value", type: NullType, location: get_location(), value: null };
      } else if (stmts.length === 1 && isSubtype(stmts[0]!.type, NullType)) {
        expr = stmts[0]!;
      } else {
        if (!isSubtype(stmts[stmts.length - 1]!.type, NullType)) {
          stmts.push({ ast_type: "Value", type: NullType, location: get_location(), value: null });
        }
        expr = {
          ast_type: "Block",
          type: stmts[stmts.length - 1]!.type,
          location: get_location(),
          statements: stmts,
        }
      }

      const ast = {
        ast_type: "ForSet" as const,
        type: NullType,
        location: get_location(),
        label,
        set: Expr.ast(collection),
        key: key_variable,
        body: expr,
      }

      statements.push(ast);

      return fromAst(ast) as any;
    } else if (collection instanceof DictExpr) {
      const value_variable: VariableAST = {
        ast_type: "Variable",
        type: Expr.type(collection).value as EastType,
        location: get_location(),
        mutable: false,
      };
      const value = fromAst(value_variable);

      const key_variable: VariableAST = {
        ast_type: "Variable",
        type: Expr.type(collection).key as EastType,
        location: get_location(),
        mutable: false,
      };
      const key = fromAst(key_variable) as IntegerExpr;

      const label = { location: get_location() };

      const $ = BlockBuilder<Ret>(return_type);
      const ret = body($, value, key, label);
      const stmts = $.statements;
      if (ret !== undefined) {
        const ret_ast = valueOrExprToAst(ret);
        if (stmts.length === 0 || stmts[stmts.length - 1] !== ret_ast) { // avoid duplicate statements
          stmts.push(ret_ast);
        }
      }

      let expr: AST;
      if (stmts.length === 0) {
        expr = { ast_type: "Value", type: NullType, location: get_location(), value: null };
      } else if (stmts.length === 1 && isSubtype(stmts[0]!.type, NullType)) {
        expr = stmts[0]!;
      } else {
        if (!isSubtype(stmts[stmts.length - 1]!.type, NullType)) {
          stmts.push({ ast_type: "Value", type: NullType, location: get_location(), value: null });
        }
        expr = {
          ast_type: "Block",
          type: stmts[stmts.length - 1]!.type,
          location: get_location(),
          statements: stmts,
        }
      }

      const ast = {
        ast_type: "ForDict" as const,
        type: NullType,
        location: get_location(),
        label,
        dict: Expr.ast(collection),
        key: key_variable,
        value: value_variable,
        body: expr,
      }

      statements.push(ast);

      return fromAst(ast) as any;
    } else {
      throw new Error(`for not defined over ${printType(Expr.type(collection))} - you can only loop over arrays, sets and dictionaries`);
    }
  }) as any;

  $.error = (message: StringExpr | string, location?: Location[]): NeverExpr => {
    if (isTypeEqual($.type(), NeverType)) {
      throw new Error(`Unreachable statement detected at ${printLocations(get_location())}`);
    }

    if (location === undefined) {
      location = get_location();
    }

    const ast = {
      ast_type: "Error" as const,
      type: NeverType,
      message: message instanceof Expr ? Expr.ast(message) : valueOrExprToAstTyped(message, StringType),
      location,
    }

    statements.push(ast);

    return fromAst(ast);
  }

  $.try = (body: ($: BlockBuilder<Ret>) => void | Expr): TryCatchExpr<Ret> => {
    if (isTypeEqual($.type(), NeverType)) {
      throw new Error(`Unreachable statement detected at ${printLocations(get_location())}`);
    }

    const $try = BlockBuilder<Ret>(return_type);
    const ret = body($try);
    const try_stmts = $try.statements;
    if (ret !== undefined) {
      const ret_ast = valueOrExprToAst(ret);
      if (try_stmts.length === 0 || try_stmts[try_stmts.length - 1] !== ret_ast) { // avoid duplicate statements
        try_stmts.push(ret_ast);
      }
    }

    if (try_stmts.length === 0 || !isSubtype(try_stmts[try_stmts.length - 1]!.type, NullType)) {
      try_stmts.push({ ast_type: "Value", type: NullType, location: get_location(), value: null });
    }

    let try_expr: AST;
    if (try_stmts.length === 1) {
      try_expr = try_stmts[0]!;
    } else {
      try_expr = {
        ast_type: "Block",
        type: try_stmts[try_stmts.length - 1]!.type,
        location: get_location(),
        statements: try_stmts,
      }
    }

    // Now define the variables available in the catch block
    const message_variable: VariableAST = {
      ast_type: "Variable",
      type: StringType,
      location: get_location(),
      mutable: false,
    };

    const stack_variable: VariableAST = {
      ast_type: "Variable",
      type: ArrayType(StructType({ filename: StringType, line: IntegerType, column: IntegerType })),
      location: get_location(),
      mutable: false,
    };

    const try_catch_ast: TryCatchAST = {
      ast_type: "TryCatch",
      type: NullType,
      location: get_location(),
      try_body: try_expr,
      catch_body: { ast_type: "Value", type: NullType, location: get_location(), value: null }, // will be updated later
      message: message_variable,
      stack: stack_variable,
    };

    statements.push(try_catch_ast);

    return new TryCatchExpr<Ret>(try_catch_ast, message_variable, stack_variable, return_type);
  }

  return $;
}


/** A helper class to perform if-elseif-else control flow. */
class IfElseExpr<Ret> extends NullExpr {
  /** @internal */
  constructor(ast: IfElseAST, private return_type: Ret) {
    super(ast, fromAst);
    // Note: the AST has been initialized to `value(null)` for the else body
    // The idea is that the if method bellow will fill them after the fact via mutation
  }

  /** Define the logic to follow when the condition is false. */
  else(body: ($: BlockBuilder<Ret>) => void | Expr): NullExpr {
    const $ = BlockBuilder<Ret>(this.return_type);
    const ret = body($);
    const stmts = $.statements;
    if (ret !== undefined) {
      const ret_ast = valueOrExprToAst(ret);
      if (stmts.length === 0 || stmts[stmts.length - 1] !== ret_ast) { // avoid duplicate statements
        stmts.push(ret_ast);
      }
    }

    if (stmts.length === 0 || !isSubtype(stmts[stmts.length - 1]!.type, NullType)) {
      stmts.push({ ast_type: "Value", type: NullType, location: get_location(), value: null });
    }

    (this[AstSymbol] as IfElseAST).else_body = stmts.length === 1 ? stmts[0]! : {
      ast_type: "Block",
      type: stmts[stmts.length - 1]!.type,
      location: get_location(),
      statements: stmts,
    };

    // propagate unreachable information
    let can_terminate = true;
    check: {
      for (const ifStmt of (this[AstSymbol] as IfElseAST).ifs) {
        if (isTypeEqual(ifStmt.predicate.type, NeverType)) {
          can_terminate = false;
          break check;
        } else if (!isTypeEqual(ifStmt.body.type, NeverType)) {
          break check;
        }
      }
      if (isTypeEqual((this[AstSymbol] as IfElseAST).else_body.type, NeverType)) {
        can_terminate = false;
      }
    }
    if (!can_terminate) {
      (this[AstSymbol] as IfElseAST).type = NeverType;
    }

    return fromAst(this[AstSymbol]) as NullExpr;
  }

  /** Check for another predicate, and execute logic if it is true */
  elseIf(predicate: BooleanExpr | boolean, body: ($: BlockBuilder<Ret>) => void | Expr): this {
    const predicateAst = predicate instanceof Expr ? Expr.ast(predicate) : valueOrExprToAstTyped(predicate, BooleanType);
    if (predicateAst.type.type !== "Boolean") {
      throw new Error(`elseIf predicate expected to have type Boolean, got ${printType(predicateAst.type)}`);
    }
    predicate = fromAst(predicateAst) as BooleanExpr;

    const $ = BlockBuilder<Ret>(this.return_type);
    const ret = body($);
    const stmts = $.statements;
    if (ret !== undefined) {
      const ret_ast = valueOrExprToAst(ret);
      if (stmts.length === 0 || stmts[stmts.length - 1] !== ret_ast) { // avoid duplicate statements
        stmts.push(ret_ast);
      }
    }

    if (stmts.length === 0 || !isSubtype(stmts[stmts.length - 1]!.type, NullType)) {
      stmts.push({ ast_type: "Value", type: NullType, location: get_location(), value: null });
    }

    (this[AstSymbol] as IfElseAST).ifs.push({
      predicate: Expr.ast(predicate),
      body: stmts.length === 1 ? stmts[0]! : {
        ast_type: "Block",
        type: stmts[stmts.length - 1]!.type,
        location: get_location(),
        statements: stmts,
      },
    })

    return this;
  }
}

/** A helper class to perform try-catch control flow. */
class TryCatchExpr<Ret> extends NullExpr {
  private catchCalled = false;

  /** @internal */
  constructor(ast: TryCatchAST, private message_variable: VariableAST, private stack_variable: VariableAST, private return_type: Ret) {
    super(ast, fromAst)
    // Note: the AST has been initialized to `value(null)` for the catch body
    // The idea is that the catch method bellow will fill it after the fact via mutation
  }

  /** Define the logic to follow when an error is caught. The error message and stack trace is provided. */
  catch(body: ($: BlockBuilder<Ret>, message: StringExpr, stack: ArrayExpr<StructType<{ filename: StringType, line: IntegerType, column: IntegerType }>>) => void | Expr): this {
    if (this.catchCalled) {
      throw new Error(`Cannot call .catch() more than once on the same try block at ${printLocations(get_location())}`);
    }
    this.catchCalled = true;
    const $ = BlockBuilder<Ret>(this.return_type);
    const ret = body($, fromAst(this.message_variable) as StringExpr, fromAst(this.stack_variable) as ArrayExpr<StructType<{ filename: StringType, line: IntegerType, column: IntegerType }>>);
    const stmts = $.statements;
    if (ret !== undefined) {
      const ret_ast = valueOrExprToAst(ret);
      if (stmts.length === 0 || stmts[stmts.length - 1] !== ret_ast) { // avoid duplicate statements
        stmts.push(ret_ast);
      }
    }

    if (stmts.length === 0 || !isSubtype(stmts[stmts.length - 1]!.type, NullType)) {
      stmts.push({ ast_type: "Value", type: NullType, location: get_location(), value: null });
    }

    (this[AstSymbol] as TryCatchAST).catch_body = stmts.length === 1 ? stmts[0]! : {
      ast_type: "Block",
      type: stmts[stmts.length - 1]!.type,
      location: get_location(),
      statements: stmts,
    };

    // Propagate unreachable information
    if (isTypeEqual((this[AstSymbol] as TryCatchAST).try_body.type, NeverType) && isTypeEqual((this[AstSymbol] as TryCatchAST).catch_body.type, NeverType)) {
      (this[AstSymbol] as TryCatchAST).type = NeverType;
    }

    return this;
  }

  /** Define cleanup logic that always executes, regardless of whether an error occurred. The finally block is for side effects only and does not affect the return type. */
  finally(body: ($: BlockBuilder<Ret>) => void | Expr): void {
    const $ = BlockBuilder<Ret>(this.return_type);
    const ret = body($);
    const stmts = $.statements;
    if (ret !== undefined) {
      const ret_ast = valueOrExprToAst(ret);
      if (stmts.length === 0 || stmts[stmts.length - 1] !== ret_ast) { // avoid duplicate statements
        stmts.push(ret_ast);
      }
    }

    if (stmts.length === 0 || !isSubtype(stmts[stmts.length - 1]!.type, NullType)) {
      stmts.push({ ast_type: "Value", type: NullType, location: get_location(), value: null });
    }

    (this[AstSymbol] as TryCatchAST).finally_body = stmts.length === 1 ? stmts[0]! : {
      ast_type: "Block",
      type: stmts[stmts.length - 1]!.type,
      location: get_location(),
      statements: stmts,
    };
  }
}

// Bind the static factory methods to the Expr class which were left undefined in expr.ts
Object.assign(Expr, {
  // Static factory methods - now simple functions
  fromAst,
  from,
  block,
  error,
  tryCatch,
  function: func,
  asyncFunction,
  print,
  str,
  equal,
  notEqual,
  less,
  lessEqual,
  greater,
  greaterEqual,
  is,
  match: matchExpr,
  // Comparison aliases
  equals,
  eq,
  notEquals,
  ne,
  lessThan,
  lt,
  lessThanOrEqual,
  lte,
  le,
  greaterThan,
  gt,
  greaterThanOrEqual,
  gte,
  ge,
  // Patch operations
  diff,
  applyPatch,
  composePatch,
  invertPatch,
});