/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST, Label, VariableAST } from "./ast.js";
import { printLocationValue, type IR, type IRLabel, type LocationValue, type VariableIR } from "./ir.js";
import { printLocations, type Location } from "./location.js";
import { toEastTypeValue, type LiteralValue } from "./type_of_type.js";
import { ArrayType, DictType, type EastType, FunctionType, isSubtype, isTypeEqual, NeverType, NullType, printType, RefType, SetType, StructType, VariantType } from "./types.js";
import { variant } from "./containers/variant.js";
import { applyTypeParameters, Builtins } from "./builtins.js";


/** @internal An exception throw for the purpose of early loop continue */
export class OutOfScopeException extends Error {
  constructor(public definedLocation: Location[]) {
    super(`Variable defined at ${printLocations(definedLocation)} is out of scope here`);
  }
}

type Ctx = {
  local_ctx: Map<VariableAST, VariableIR>,
  parent_ctx: Map<VariableAST, VariableIR>,
  captures: Set<VariableIR>,
  loop_ctx: Map<Label, IRLabel>,
  recursiveASTs?: Set<any>,
  n_vars: number,
  n_loops: number,
  inputs: EastType[],
  output: EastType,
  async: boolean,
}

// TODO we should probably redo type checking exhaustively here?
function toLocationValues(locations: Location[]): LocationValue[] {
  return locations.map(loc => ({
    filename: loc.filename,
    line: BigInt(loc.line),
    column: BigInt(loc.column),
  }));
}


/** Perform scope resolution and type checking on `AST`, produce `IR` ready for serialization, compilation or evaluation.
* 
* @internal */
export function ast_to_ir(ast: AST, ctx: Ctx = { local_ctx: new Map(), parent_ctx: new Map(), captures: new Set(), loop_ctx: new Map(), n_vars: 0, n_loops: 0, inputs: [], output: NeverType, async: false }): IR {
  try {
    if (ast.ast_type === "Variable") {
      if (ctx.local_ctx.has(ast)) {
        return ctx.local_ctx.get(ast)!;
      } else {
        if (ctx.parent_ctx.has(ast)) {
          const ir = ctx.parent_ctx.get(ast)!;
          ir.value.captured = true;
          ctx.captures.add(ir);
          return ir;
        } else {
          throw new OutOfScopeException(ast.location);
        }
      }
    } else if (ast.ast_type === "Let") {
      let value = ast_to_ir(ast.value, ctx);

      // Create a new variable
      const variable: VariableIR = variant("Variable", {
        type: toEastTypeValue(ast.variable.type),
        name: `_${ctx.n_vars}`,
        location: toLocationValues(ast.variable.location),
        mutable: ast.variable.mutable,
        captured: false,
      });

      // Insert As node if value type doesn't exactly match variable type
      // This ensures the IR has exact types everywhere
      if (!isTypeEqual(ast.value.type, ast.variable.type)) {
        // Validate subtype relationship before inserting As node
        // This catches type errors early at AST level
        if (!isSubtype(ast.value.type, ast.variable.type)) {
          throw new Error(
            `Cannot initialize variable of type ${printType(ast.variable.type)} ` +
            `with value of type ${printType(ast.value.type)} at ${printLocations(ast.location)}`
          );
        }

        value = variant("As", {
          type: toEastTypeValue(ast.variable.type),
          value,
          location: toLocationValues(ast.location),
        });
      }

      ctx.n_vars += 1;
      ctx.local_ctx.set(ast.variable, variable);

      return variant("Let", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        variable,
        value,
      });
    } else if (ast.ast_type === "Assign") {
      // Fetch the variable from context
      const variable = ast_to_ir(ast.variable, ctx) as VariableIR;

      if (!variable.value.mutable) {
        throw new Error(`Variable defined const at ${printLocationValue(variable.value.location)} is being reassigned at ${printLocations(ast.location)}`)
      }

      let value = ast_to_ir(ast.value, ctx);

      // Get the variable's type from the IR node
      const variableType = variable.value.type;

      // Insert As node if value type doesn't exactly match variable type
      // This ensures the IR has exact types everywhere
      if (!isTypeEqual(ast.value.type, ast.variable.type)) {
        // Validate subtype relationship before inserting As node
        if (!isSubtype(ast.value.type, ast.variable.type)) {
          throw new Error(
            `Cannot assign value of type ${printType(ast.value.type)} ` +
            `to variable of type ${printType(ast.variable.type)} at ${printLocations(ast.location)}`
          );
        }

        value = variant("As", {
          type: variableType,
          value,
          location: toLocationValues(ast.location),
        });
      }

      return variant("Assign", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        variable,
        value,
      });
    } else if (ast.ast_type === "Block") {
      const local_ctx = new Map([...ctx.local_ctx]);
      const ctx2: Ctx = { ...ctx, local_ctx };

      const statements = ast.statements.map(s => ast_to_ir(s, ctx2));
      ctx.n_vars = ctx2.n_vars;
      ctx.n_loops = ctx2.n_loops;

      return variant("Block", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        statements,
      });
    } else if (ast.ast_type === "Builtin") {
      // We need to apply the type parameters to the builtin, and cast the arguments as needed
      const builtin_name = ast.builtin;
      const builtin_def = Builtins[builtin_name];
      if (!builtin_def) {
        throw new Error(`Unknown builtin function '${builtin_name}' at ${printLocations(ast.location)}`);
      }
      if (builtin_def.type_parameters.length !== ast.type_parameters.length) {
        throw new Error(`Builtin function '${builtin_name}' expected ${builtin_def.type_parameters.length} type parameters, got ${ast.type_parameters.length} at ${printLocations(ast.location)}`);
      }
      const type_map = new Map(builtin_def.type_parameters.map((name, i) => [name, ast.type_parameters[i]!] as const));

      if (ast.arguments.length !== builtin_def.inputs.length) {
        throw new Error(`Builtin function '${builtin_name}' expected ${builtin_def.inputs.length} arguments, got ${ast.arguments.length} at ${printLocations(ast.location)}`);
      }

      return variant("Builtin", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        builtin: ast.builtin,
        type_parameters: ast.type_parameters.map(tp => toEastTypeValue(tp)),
        arguments: ast.arguments.map((arg, i) => {
          let arg_ir = ast_to_ir(arg, ctx);
          const expectedType = applyTypeParameters(builtin_def.inputs[i]!, type_map, [], []);

          // Now check type compatibility
          if (arg.type.type !== "Never" && !isTypeEqual(arg.type, expectedType)) {
            if (!isSubtype(arg.type, expectedType)) {
              throw new Error(
                `Builtin ${builtin_name} with type parameters [${ast.type_parameters.map(tp => printType(tp)).join(", ")}] argument ${i} of type ${printType(arg.type)} is not compatible with expected type ${printType(expectedType)} at ${printLocations(ast.location)}`
              );
            }
            arg_ir = variant("As", {
              type: toEastTypeValue(expectedType),
              value: arg_ir,
              location: toLocationValues(ast.location),
            });
          }

          return arg_ir;
        }),
      });
    } else if (ast.ast_type === "Platform") {
      if (ctx.async === false && ast.async === true) {
        throw new Error(`Async platform call not allowed outside async function at ${printLocations(ast.location)}`);
      }

      return variant("Platform", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        name: ast.name,
        type_parameters: ast.type_parameters.map(tp => toEastTypeValue(tp)),
        arguments: ast.arguments.map(ast => ast_to_ir(ast, ctx)), // type equality handled at Expr/AST level
        async: ast.async,
        optional: ast.optional,
      });
    } else if (ast.ast_type === "Struct") {
      return variant("Struct", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        fields: Object.entries(ast.fields).map(([name, fieldAst]) => {
          let value = ast_to_ir(fieldAst, ctx);
          const expectedType = (ast.type as StructType).fields[name];
          if (!expectedType) {
            throw new Error(`Struct type does not have field '${name}' at ${printLocations(ast.location)}`);
          }
          if (!isTypeEqual(fieldAst.type, expectedType)) {
            if (isSubtype(fieldAst.type, expectedType)) {
              value = variant("As", {
                type: toEastTypeValue(expectedType),
                value,
                location: toLocationValues(ast.location),
              })
            } else {
              throw new Error(
                `Cannot assign field '${name}' of type ${printType((ast.type as StructType).fields[name]!)} ` +
                `with value of type ${printType(fieldAst.type)} at ${printLocations(ast.location)}`
              );
            }
          }
          return { name, value };
        }),
      });
    } else if (ast.ast_type === "GetField") {
      return variant("GetField", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        struct: ast_to_ir(ast.struct, ctx),
        field: ast.field,
      });
    } else if (ast.ast_type === "Variant") {
      const expectedType = (ast.type as VariantType).cases[ast.case];
      let value = ast_to_ir(ast.value, ctx);
      if (!isTypeEqual(ast.value.type, expectedType)) {
        if (isSubtype(ast.value.type, expectedType)) {
          value = variant("As", {
            type: toEastTypeValue(expectedType),
            value,
            location: toLocationValues(ast.location),
          })
        } else {
          throw new Error(
            `Cannot assign case '${ast.case}' of type ${printType(expectedType)} ` +
            `with value of type ${printType(ast.value.type)} at ${printLocations(ast.location)}`
          );
        }
      }
      return variant("Variant", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        case: ast.case,
        value,
      });
    } else if (ast.ast_type === "Function") {
      const parameters: VariableIR[] = ast.parameters.map(parameter => {
        const param: VariableIR = variant("Variable", {
          type: toEastTypeValue(parameter.type),
          name: `_${ctx.n_vars}`,
          location: toLocationValues(parameter.location),
          mutable: parameter.mutable, // false...
          captured: false,
        });
        ctx.n_vars += 1;
        return param;
      });

      const local_ctx = new Map(parameters.map((parameter, i) => ([ast.parameters[i]!, parameter] as const)));
      const parent_ctx = new Map([...ctx.local_ctx, ...ctx.parent_ctx]);
      const captures = new Set<VariableIR>();
      const ctx2: Ctx = { local_ctx, parent_ctx, captures, loop_ctx: new Map(), n_vars: ctx.n_vars, n_loops: ctx.n_loops, inputs: (ast.type as FunctionType).inputs, output: (ast.type as FunctionType).output, async: false }

      const body = ast_to_ir(ast.body, ctx2);

      ctx.n_vars = ctx2.n_vars;
      ctx.n_loops = ctx2.n_loops;

      // Propagate captures: if this function captured something from ctx.parent_ctx,
      // then the enclosing function also needs to capture it
      for (const capturedVar of captures) {
        // Check if this variable came from our parent context (not defined locally in enclosing function)
        for (const [_astVar, ir] of ctx.parent_ctx) {
          if (ir === capturedVar) {
            // This capture came from an outer scope, so enclosing function must also capture it
            ctx.captures.add(capturedVar);
            break;
          }
        }
      }

      return variant("Function", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        parameters,
        captures: [...captures],
        body,
      });
    } else if (ast.ast_type === "AsyncFunction") {
      const parameters: VariableIR[] = ast.parameters.map(parameter => {
        const param: VariableIR = variant("Variable", {
          type: toEastTypeValue(parameter.type),
          name: `_${ctx.n_vars}`,
          location: toLocationValues(parameter.location),
          mutable: parameter.mutable, // false...
          captured: false,
        });
        ctx.n_vars += 1;
        return param;
      });

      const local_ctx = new Map(parameters.map((parameter, i) => ([ast.parameters[i]!, parameter] as const)));
      const parent_ctx = new Map([...ctx.local_ctx, ...ctx.parent_ctx]);
      const captures = new Set<VariableIR>();
      const ctx2: Ctx = { local_ctx, parent_ctx, captures, loop_ctx: new Map(), n_vars: ctx.n_vars, n_loops: ctx.n_loops, inputs: (ast.type as FunctionType).inputs, output: (ast.type as FunctionType).output, async: true }

      const body = ast_to_ir(ast.body, ctx2);

      ctx.n_vars = ctx2.n_vars;
      ctx.n_loops = ctx2.n_loops;

      // Propagate captures: if this function captured something from ctx.parent_ctx,
      // then the enclosing function also needs to capture it
      for (const capturedVar of captures) {
        // Check if this variable came from our parent context (not defined locally in enclosing function)
        for (const [_astVar, ir] of ctx.parent_ctx) {
          if (ir === capturedVar) {
            // This capture came from an outer scope, so enclosing function must also capture it
            ctx.captures.add(capturedVar);
            break;
          }
        }
      }

      return variant("AsyncFunction", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        parameters,
        captures: [...captures],
        body,
      });
    } else if (ast.ast_type === "Call") {
      // TODO - type equality could have been handled at Expr/AST level instead
      // TODO - what about widening the result with As?
      return variant("Call", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        function: ast_to_ir(ast.function, ctx),
        arguments: ast.arguments.map((argument, i) => {
          let arg = ast_to_ir(argument, ctx);
          const expectedType = (ast.function.type as FunctionType).inputs[i];

          if (!isTypeEqual(argument.type, expectedType)) {
            if (!isSubtype(argument.type, expectedType)) {
              throw new Error(
                `Argument ${i} of type ${printType(argument.type)} is not compatible with expected type ${printType(expectedType)} at ${printLocations(ast.location)}`
              );
            }
            arg = variant("As", {
              type: toEastTypeValue(expectedType),
              value: arg,
              location: toLocationValues(ast.location),
            });
          }

          return arg;
        }),
      });
    } else if (ast.ast_type === "CallAsync") {
      if (ctx.async === false) {
        throw new Error(`Async function call not allowed outside async function at ${printLocations(ast.location)}`);
      }

      // TODO - type equality could have been handled at Expr/AST level instead
      // TODO - what about widening the result with As?
      return variant("CallAsync", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        function: ast_to_ir(ast.function, ctx),
        arguments: ast.arguments.map((argument, i) => {
          let arg = ast_to_ir(argument, ctx);
          const expectedType = (ast.function.type as FunctionType).inputs[i];

          if (!isTypeEqual(argument.type, expectedType)) {
            if (!isSubtype(argument.type, expectedType)) {
              throw new Error(
                `Argument ${i} of type ${printType(argument.type)} is not compatible with expected type ${printType(expectedType)} at ${printLocations(ast.location)}`
              );
            }
            arg = variant("As", {
              type: toEastTypeValue(expectedType),
              value: arg,
              location: toLocationValues(ast.location),
            });
          }

          return arg;
        }),
      });
    } else if (ast.ast_type === "NewRef") {
      const valueType = (ast.type as RefType).value;
      let value = ast_to_ir(ast.value, ctx);
      if (!isTypeEqual(ast.value.type, valueType)) {
        if (!isSubtype(ast.value.type, valueType)) {
          throw new Error(
            `Ref value of type ${printType(ast.value.type)} is not compatible with expected type ${printType(valueType)} at ${printLocations(ast.location)}`
          );
        }
        value = variant("As", {
          type: toEastTypeValue(valueType),
          value,
          location: toLocationValues(ast.location),
        });
      }

      return variant("NewRef", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        value,
      });
    } else if (ast.ast_type === "NewArray") {
      const valueType = (ast.type as ArrayType).value;
      return variant("NewArray", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        values: ast.values.map((v, i) => {
          let value = ast_to_ir(v, ctx);
          if (!isTypeEqual(v.type, valueType)) {
            if (!isSubtype(v.type, valueType)) {
              throw new Error(
                `Array value at entry ${i} of type ${printType(v.type)} is not compatible with expected type ${printType(valueType)} at ${printLocations(ast.location)}`
              );
            }
            value = variant("As", {
              type: toEastTypeValue(valueType),
              value,
              location: toLocationValues(ast.location),
            });
          }

          return value;
        }),
      });
    } else if (ast.ast_type === "NewSet") {
      const keyType = (ast.type as SetType).key;
      return variant("NewSet", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        values: ast.values.map((k, i) => {
          let key = ast_to_ir(k, ctx);
          if (!isTypeEqual(k.type, keyType)) {
            if (!isSubtype(k.type, keyType)) {
              throw new Error(
                `Set key at entry ${i} of type ${printType(k.type)} is not compatible with expected type ${printType(keyType)} at ${printLocations(ast.location)}`
              );
            }
            key = variant("As", {
              type: toEastTypeValue(keyType),
              value: key,
              location: toLocationValues(ast.location),
            });
          }

          return key;
        }),
      });
    } else if (ast.ast_type === "NewDict") {
      const keyType = (ast.type as DictType).key;
      const valueType = (ast.type as DictType).value;
      return variant("NewDict", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        values: ast.values.map(([k, v], i) => {
          let key = ast_to_ir(k, ctx);
          if (!isTypeEqual(k.type, keyType)) {
            if (!isSubtype(k.type, keyType)) {
              throw new Error(
                `Dict key at entry ${i} of type ${printType(k.type)} is not compatible with expected type ${printType(keyType)} at ${printLocations(ast.location)}`
              );
            }
            key = variant("As", {
              type: toEastTypeValue(keyType),
              value: key,
              location: toLocationValues(ast.location),
            });
          }

          let value = ast_to_ir(v, ctx);
          if (!isTypeEqual(v.type, valueType)) {
            if (!isSubtype(v.type, valueType)) {
              throw new Error(
                `Dict value at entry ${i} of type ${printType(v.type)} is not compatible with expected type ${printType(valueType)} at ${printLocations(ast.location)}`
              );
            }
            value = variant("As", {
              type: toEastTypeValue(valueType),
              value,
              location: toLocationValues(ast.location),
            });
          };

          return { key, value };
        }),
      });
    } else if (ast.ast_type === "IfElse") {
      const ifs = ast.ifs.map(branch => {
        const predicate = ast_to_ir(branch.predicate, ctx);

        const ctx_branch: Ctx = {
          local_ctx: new Map([...ctx.local_ctx]),
          parent_ctx: ctx.parent_ctx,
          captures: ctx.captures,
          loop_ctx: ctx.loop_ctx,
          n_vars: ctx.n_vars,
          n_loops: ctx.n_loops,
          inputs: ctx.inputs,
          output: ctx.output,
          async: ctx.async,
        };
        let branch_body = ast_to_ir(branch.body, ctx_branch);
        ctx.n_vars = ctx_branch.n_vars;
        ctx.n_loops = ctx_branch.n_loops;

        if (branch.body.type.type !== "Never" && !isTypeEqual(branch.body.type, ast.type)) {
          if (!isSubtype(branch.body.type, ast.type)) {
            throw new Error(
              `If branch body of type ${printType(branch.body.type)} is not compatible with expected type ${printType(ast.type)} at ${printLocations(ast.location)}`
            );
          }

          branch_body = variant("As", {
            type: toEastTypeValue(ast.type),
            value: branch_body,
            location: toLocationValues(ast.location),
          });
        }

        return { predicate, body: branch_body };
      });

      const ctx_else: Ctx = {
        local_ctx: new Map([...ctx.local_ctx]),
        parent_ctx: ctx.parent_ctx,
        captures: ctx.captures,
        loop_ctx: ctx.loop_ctx,
        n_vars: ctx.n_vars,
        n_loops: ctx.n_loops,
        inputs: ctx.inputs,
        output: ctx.output,
        async: ctx.async,
      };
      let else_body = ast_to_ir(ast.else_body, ctx_else);
      ctx.n_vars = ctx_else.n_vars;
      ctx.n_loops = ctx_else.n_loops;

      if (ast.else_body.type.type !== "Never" && !isTypeEqual(ast.else_body.type, ast.type)) {
        if (!isSubtype(ast.else_body.type, ast.type)) {
          throw new Error(
            `Else branch body of type ${printType(ast.else_body.type)} is not compatible with expected type ${printType(ast.type)} at ${printLocations(ast.location)}`
          );
        }

        else_body = variant("As", {
          type: toEastTypeValue(ast.type),
          value: else_body,
          location: toLocationValues(ast.location),
        });
      }

      return variant("IfElse", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        ifs,
        else_body,
      });
    } else if (ast.ast_type === "Error") {
      return variant("Error", {
        type: variant("Never", null),
        location: toLocationValues(ast.location),
        message: ast_to_ir(ast.message, ctx),
      });
    } else if (ast.ast_type === "TryCatch") {
      const ctx_try: Ctx = {
        local_ctx: new Map([...ctx.local_ctx]),
        parent_ctx: ctx.parent_ctx,
        captures: ctx.captures,
        loop_ctx: ctx.loop_ctx,
        n_vars: ctx.n_vars,
        n_loops: ctx.n_loops,
        inputs: ctx.inputs,
        output: ctx.output,
        async: ctx.async,
      };
      const try_body = ast_to_ir(ast.try_body, ctx_try);
      ctx.n_vars = ctx_try.n_vars;
      ctx.n_loops = ctx_try.n_loops;

      // Create new variables for the catch message and stack
      const message: VariableIR = variant("Variable", {
        type: toEastTypeValue(ast.message.type),
        name: `_${ctx.n_vars}`,
        location: toLocationValues(ast.message.location),
        mutable: ast.message.mutable, // false...
        captured: false,
      });
      ctx.n_vars += 1;

      const stack: VariableIR = variant("Variable", {
        type: toEastTypeValue(ast.stack.type),
        name: `_${ctx.n_vars}`,
        location: toLocationValues(ast.stack.location),
        mutable: ast.stack.mutable, // false...
        captured: false,
      });
      ctx.n_vars += 1;
      const ctx_catch: Ctx = {
        local_ctx: new Map([...ctx.local_ctx, [ast.message, message], [ast.stack, stack]]),
        parent_ctx: ctx.parent_ctx,
        captures: ctx.captures,
        loop_ctx: ctx.loop_ctx,
        n_vars: ctx.n_vars,
        n_loops: ctx.n_loops,
        inputs: ctx.inputs,
        output: ctx.output,
        async: ctx.async,
      };
      const catch_body = ast_to_ir(ast.catch_body, ctx_catch);
      ctx.n_vars = ctx_catch.n_vars;
      ctx.n_loops = ctx_catch.n_loops;

      // Process finally block if present
      let finally_body: IR;
      if (ast.finally_body) {
        const ctx_finally: Ctx = {
          local_ctx: new Map([...ctx.local_ctx]),
          parent_ctx: ctx.parent_ctx,
          captures: ctx.captures,
          loop_ctx: ctx.loop_ctx,
          n_vars: ctx.n_vars,
          n_loops: ctx.n_loops,
          inputs: ctx.inputs,
          output: ctx.output,
          async: ctx.async,
        };
        finally_body = ast_to_ir(ast.finally_body, ctx_finally);
        ctx.n_vars = ctx_finally.n_vars;
        ctx.n_loops = ctx_finally.n_loops;
      } else {
        finally_body = variant("Value", {
          type: toEastTypeValue(NullType),
          location: toLocationValues(ast.location),
          value: variant("Null", null),
        });
      }

      return variant("TryCatch", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        try_body,
        catch_body,
        message,
        stack,
        finally_body,
      });
    } else if (ast.ast_type === "Value") {
      const type = toEastTypeValue(ast.type);
      let value: LiteralValue;
      if (ast.value === null) {
        value = variant("Null", null);
      } else if (typeof ast.value === "boolean") {
        value = variant("Boolean", ast.value);
      } else if (typeof ast.value === "bigint") {
        value = variant("Integer", ast.value);
      } else if (typeof ast.value === "number") {
        value = variant("Float", ast.value);
      } else if (typeof ast.value === "string") {
        value = variant("String", ast.value);
      } else if (ast.value instanceof Date) {
        value = variant("DateTime", new Date(ast.value));
      } else if (ast.value instanceof Uint8Array) {
        value = variant("Blob", new Uint8Array(ast.value));
      } else {
        throw new Error(`Unsupported literal value type: ${typeof ast.value} (expected ${printType(ast.type)})`);
      }

      if (type.type !== value.type) {
        throw new Error(`Literal value type mismatch at ${printLocations(ast.location)}: expected .${type.type} but got .${value.type}`);
      }

      return variant("Value", {
        type,
        location: toLocationValues(ast.location),
        value,
      });
    } else if (ast.ast_type === "As") {
      return variant("As", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        value: ast_to_ir(ast.value, ctx),
      });
    } else if (ast.ast_type === "While") {
      const predicate = ast_to_ir(ast.predicate, ctx);
      const label: IRLabel = {
        name: `_${ctx.n_loops}`,
        location: toLocationValues(ast.label.location),
      }
      ctx.n_loops += 1;

      const ctx2: Ctx = {
        local_ctx: new Map([...ctx.local_ctx]),
        parent_ctx: ctx.parent_ctx,
        captures: ctx.captures,
        loop_ctx: new Map([...ctx.loop_ctx, [ast.label, label]]),
        n_vars: ctx.n_vars,
        n_loops: ctx.n_loops,
        inputs: ctx.inputs,
        output: ctx.output,
        async: ctx.async,
      };
      const body = ast_to_ir(ast.body, ctx2);
      ctx.n_vars = ctx2.n_vars;
      ctx.n_loops = ctx2.n_loops;

      return variant("While", {
        type: variant("Null", null),
        location: toLocationValues(ast.location),
        label,
        predicate,
        body,
      });
    } else if (ast.ast_type === "ForArray") {
      const array = ast_to_ir(ast.array, ctx);
      const label: IRLabel = {
        name: `_${ctx.n_loops}`,
        location: toLocationValues(ast.label.location),
      }
      ctx.n_loops += 1;

      const value: VariableIR = variant("Variable", {
        type: toEastTypeValue(ast.value.type),
        name: `_${ctx.n_vars}`,
        location: toLocationValues(ast.value.location),
        mutable: ast.value.mutable, // false...
        captured: false,
      });
      ctx.n_vars += 1;

      const key: VariableIR = variant("Variable", {
        type: toEastTypeValue(ast.key.type),
        name: `_${ctx.n_vars}`,
        location: toLocationValues(ast.key.location),
        mutable: ast.key.mutable, // false...
        captured: false,
      });
      ctx.n_vars += 1;

      const ctx2: Ctx = {
        local_ctx: new Map([...ctx.local_ctx, [ast.value, value], [ast.key, key]]),
        parent_ctx: ctx.parent_ctx,
        captures: ctx.captures,
        loop_ctx: new Map([...ctx.loop_ctx, [ast.label, label]]),
        n_vars: ctx.n_vars,
        n_loops: ctx.n_loops,
        inputs: ctx.inputs,
        output: ctx.output,
        async: ctx.async,
      };
      const body = ast_to_ir(ast.body, ctx2);
      ctx.n_vars = ctx2.n_vars;
      ctx.n_loops = ctx2.n_loops;

      return variant("ForArray", {
        type: variant("Null", null),
        location: toLocationValues(ast.location),
        label,
        key,
        value,
        array,
        body,
      });
    } else if (ast.ast_type === "ForSet") {
      const set = ast_to_ir(ast.set, ctx);
      const label: IRLabel = {
        name: `_${ctx.n_loops}`,
        location: toLocationValues(ast.label.location),
      }
      ctx.n_loops += 1;

      const key: VariableIR = variant("Variable", {
        type: toEastTypeValue(ast.key.type),
        name: `_${ctx.n_vars}`,
        location: toLocationValues(ast.key.location),
        mutable: ast.key.mutable, // false...
        captured: false,
      });
      ctx.n_vars += 1;

      const ctx2: Ctx = {
        local_ctx: new Map([...ctx.local_ctx, [ast.key, key]]),
        parent_ctx: ctx.parent_ctx,
        captures: ctx.captures,
        loop_ctx: new Map([...ctx.loop_ctx, [ast.label, label]]),
        n_vars: ctx.n_vars,
        n_loops: ctx.n_loops,
        inputs: ctx.inputs,
        output: ctx.output,
        async: ctx.async,
      };
      const body = ast_to_ir(ast.body, ctx2);
      ctx.n_vars = ctx2.n_vars;
      ctx.n_loops = ctx2.n_loops;

      return variant("ForSet", {
        type: variant("Null", null),
        location: toLocationValues(ast.location),
        label,
        key,
        set,
        body,
      });
    } else if (ast.ast_type === "ForDict") {
      const dict = ast_to_ir(ast.dict, ctx);
      const label: IRLabel = {
        name: `_${ctx.n_loops}`,
        location: toLocationValues(ast.label.location),
      }
      ctx.n_loops += 1;

      const value: VariableIR = variant("Variable", {
        type: toEastTypeValue(ast.value.type),
        name: `_${ctx.n_vars}`,
        location: toLocationValues(ast.value.location),
        mutable: ast.value.mutable, // false...
        captured: false,
      });
      ctx.n_vars += 1;

      const key: VariableIR = variant("Variable", {
        type: toEastTypeValue(ast.key.type),
        name: `_${ctx.n_vars}`,
        location: toLocationValues(ast.key.location),
        mutable: ast.key.mutable, // false...
        captured: false,
      });
      ctx.n_vars += 1;

      const ctx2: Ctx = {
        local_ctx: new Map([...ctx.local_ctx, [ast.value, value], [ast.key, key]]),
        parent_ctx: ctx.parent_ctx,
        captures: ctx.captures,
        loop_ctx: new Map([...ctx.loop_ctx, [ast.label, label]]),
        n_vars: ctx.n_vars,
        n_loops: ctx.n_loops,
        inputs: ctx.inputs,
        output: ctx.output,
        async: ctx.async,
      };
      const body = ast_to_ir(ast.body, ctx2);
      ctx.n_vars = ctx2.n_vars;
      ctx.n_loops = ctx2.n_loops;

      return variant("ForDict", {
        type: variant("Null", null),
        location: toLocationValues(ast.location),
        label,
        key,
        value,
        dict,
        body,
      });
    } else if (ast.ast_type === "Match") {
      const variant_expr = ast_to_ir(ast.variant, ctx);

      const cases: { case: string, variable: VariableIR, body: IR }[] = [];
      for (const [k, v] of Object.entries(ast.cases)) {
        const variable: VariableIR = variant("Variable", {
          type: toEastTypeValue(v.variable.type),
          name: `_${ctx.n_vars}`,
          location: toLocationValues(v.variable.location),
          mutable: v.variable.mutable, // false...
          captured: false,
        });
        ctx.n_vars += 1;

        const ctx2: Ctx = {
          local_ctx: new Map([...ctx.local_ctx, [v.variable, variable]]),
          parent_ctx: ctx.parent_ctx,
          captures: ctx.captures,
          loop_ctx: ctx.loop_ctx,
          n_vars: ctx.n_vars,
          n_loops: ctx.n_loops,
          inputs: ctx.inputs,
          output: ctx.output,
          async: ctx.async,
        };
        let body = ast_to_ir(v.body, ctx2);
        ctx.n_vars = ctx2.n_vars;
        ctx.n_loops = ctx2.n_loops;

        if (v.body.type.type !== "Never" && !isTypeEqual(v.body.type, ast.type)) {
          if (!isSubtype(v.body.type, ast.type)) {
            throw new Error(
              `Match case '${k}' body of type ${printType(v.body.type)} is not compatible with expected type ${printType(ast.type)} at ${printLocations(ast.location)}`
            );
          }

          body = variant("As", {
            type: toEastTypeValue(ast.type),
            value: body,
            location: toLocationValues(ast.location),
          });
        }

        cases.push({ case: k, variable, body });
      }

      return variant("Match", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        variant: variant_expr,
        cases,
      });
    } else if (ast.ast_type === "UnwrapRecursive") {
      return variant("UnwrapRecursive", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        value: ast_to_ir(ast.value, ctx),
      });
    } else if (ast.ast_type === "WrapRecursive") {
      // Check if we're already converting this AST node -> circular reference
      if (!ctx.recursiveASTs) {
        ctx.recursiveASTs = new Set();
      }
      const existing = ctx.recursiveASTs.has(ast);
      if (existing) {
        throw new Error(`Circular reference detected when converting AST to IR at ${printLocations(ast.location)}`);
      }

      // Register before recursing (enables cycle detection)
      ctx.recursiveASTs.add(ast);

      // Create WrapRecursive IR node with placeholder
      const wrapIR: any = variant("WrapRecursive", {
        type: toEastTypeValue(ast.type),
        location: toLocationValues(ast.location),
        value: ast_to_ir(ast.value, ctx),
      });

      // The user may alias this AST value elsewhere in the tree, just not with a circular reference
      ctx.recursiveASTs.delete(ast);

      return wrapIR;
    } else if (ast.ast_type === "Break") {
      const label = ctx.loop_ctx.get(ast.label);
      if (label === undefined) {
        throw new Error(`Label defined at ${printLocations(ast.label.location)} is not in scope at break at ${printLocations(ast.location)}`)
      }

      return variant("Break", {
        type: variant("Never", null),
        location: toLocationValues(ast.location),
        label,
      });
    } else if (ast.ast_type === "Continue") {
      const label = ctx.loop_ctx.get(ast.label);
      if (label === undefined) {
        throw new Error(`Label defined at ${printLocations(ast.label.location)} is not in scope at continue at ${printLocations(ast.location)}`)
      }

      return variant("Continue", {
        type: variant("Never", null),
        location: toLocationValues(ast.location),
        label,
      });
    } else if (ast.ast_type === "Return") {
      if (!isSubtype(ast.value.type, ctx.output)) {
        throw new Error(`Attempted to return value of type ${printType(ast.value.type)} at ${printLocations(ast.location)}, but function expected return type of ${printType(ctx.output)}`)
      }

      return variant("Return", {
        type: variant("Never", null),
        location: toLocationValues(ast.location),
        value: ast_to_ir(ast.value, ctx),
      });
    } else {
      throw new Error(`Cannot check ${((ast satisfies never) as AST).type}`)
    }
  } catch (e: unknown) {
    if (e instanceof Error) {
      if (ast.ast_type === "Builtin") {
        e.message += `\n    at ${ast.ast_type} ${ast.builtin} node located at ${printLocations(ast.location)}`;
      } else if (ast.ast_type === "Platform") {
        e.message += `\n    at ${ast.ast_type} ${ast.name} node located at ${printLocations(ast.location)}`;
      } else{
        e.message += `\n    at ${ast.ast_type} node located at ${printLocations(ast.location)}`;
      }
    }
    throw e;
  }
}
