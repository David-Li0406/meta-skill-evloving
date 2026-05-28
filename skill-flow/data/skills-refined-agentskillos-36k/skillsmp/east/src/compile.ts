/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { type BuiltinName } from "./builtins.js";
import { type IR, type LocationValue, printLocationValue } from "./ir.js";
import { compareFor, equalFor, greaterEqualFor, greaterFor, isFor, lessEqualFor, lessFor, notEqualFor } from "./comparison.js";
import { diffFor } from "./patch/diff.js";
import { applyFor } from "./patch/apply.js";
import { composeFor } from "./patch/compose.js";
import { invertFor } from "./patch/invert.js";
import { ConflictError } from "./patch/index.js";
import { printFor, parseFor } from "./serialization/east.js";
import { variant, type option } from "./containers/variant.js";
import { EastError, InternalError } from "./error.js";
import { SortedSet } from "./containers/sortedset.js";
import { SortedMap } from "./containers/sortedmap.js";
import { BufferWriter } from "./serialization/binary-utils.js";
import { decodeBeast2For, decodeBeastFor, encodeBeast2For, encodeBeastFor, fromJSONFor, toJSONFor, decodeCsvFor, encodeCsvFor } from "./serialization/index.js";
import { formatDateTime } from "./datetime_format/print.js";
import { parseDateTimeFormatted } from "./datetime_format/parse.js";
import type { DateTimeFormatToken } from "./datetime_format/types.js";
import { EastTypeValueType, isTypeValueEqual, type EastTypeValue, expandTypeValue, type DictTypeValue, type SetTypeValue, type ArrayTypeValue } from "./type_of_type.js";
import type { AnalyzedIR } from "./analyze.js";
import { ref } from "./containers/ref.js";
import type { PlatformFunction } from "./platform.js";

export { isTypeValueEqual };
export const printTypeValue = printFor(EastTypeValueType) as (type: EastTypeValue) => string;

/**
 * Symbol used to attach source IR to compiled functions.
 * This enables serialization of free functions (functions with no captures).
 */
export const EAST_IR_SYMBOL = Symbol.for("east.ir");

/**
 * Symbol used to attach capture values to compiled functions.
 * This enables serialization of closures (functions with captures).
 */
export const EAST_CAPTURES_SYMBOL = Symbol.for("east.captures");

// =============================================================================
// Context Value Types - for variables in execution context
// =============================================================================

/**
 * Context values are stored as variants to distinguish regular values from boxed mutable captures.
 * - variant("value", x): regular immutable or non-captured mutable variable
 * - variant("boxed", x): mutable captured variable (box enables shared mutation across closures)
 */
export type ContextValue<T = unknown> =
  | variant<"value", T>
  | variant<"boxed", T>;

/** Runtime context mapping variable names to their wrapped values */
export type RuntimeContext = Record<string, ContextValue>;

/** Determines if a variable requires boxing (mutable + captured) */
export function requiresBoxing(variable: { mutable: boolean; captured: boolean }): boolean {
  return variable.mutable && variable.captured;
}

/** Get a context value, throwing InternalError if missing */
function getContextValue(ctx: RuntimeContext, name: string): ContextValue {
  const value = ctx[name];
  if (value === undefined) {
    throw new InternalError(`Variable '${name}' not found in runtime context`);
  }
  return value;
}

// =============================================================================

/** @internal Track iteration locks to prevent concurrent modification */
const iterationLocks = new WeakMap<any, number>();

/** @internal Lock a collection for iteration (prevents size/keyset modifications) */
const lockForIteration = (obj: any) => {
  iterationLocks.set(obj, (iterationLocks.get(obj) || 0) + 1);
};

/** @internal Unlock a collection after iteration */
const unlockForIteration = (obj: any) => {
  const count = iterationLocks.get(obj) || 0;
  if (count > 1) {
    iterationLocks.set(obj, count - 1);
  } else {
    iterationLocks.delete(obj);
  }
};

/** @internal An exception throw for the purpose of early function return */
export class ReturnException {
  constructor(public value: any) {}
}

/** @internal An exception throw for the purpose of early loop continue */
class ContinueException {
  constructor(public label: string) {}
}

/** @internal An exception throw for the purpose of early loop break */
class BreakException {
  constructor(public label: string) {}
}

/** Compile `IR` into a JavaScript function using a closure-compiler technique.
* This should execute faster than a simple tree-walking interpreter, but slower than hand-written Javascript.
*
* A "context" of the current variables in scope is given. For toplevel function IR, provide `{}`.
* A "platform" is provided with JavaScript functions to perform effects, like logging. If no effects are needed, simply provide `{}`.
*
* @internal
*/
export function compile_internal(ir: AnalyzedIR, ctx: Record<string, EastTypeValue>, platform: Record<string, (...args: any[]) => any>, asyncPlatformFns: Set<string>, platformDef: PlatformFunction[], fresh_ctx: boolean = true, compilingNodes: Set<IR> = new Set()): (ctx: RuntimeContext) => any {
  // The IR is checked prior to compilation, so we can assume it's valid here.
  // The compiler needs to take care that Promises are properly awaited, so most IR nodes need both sync and async implementations.
  // We assume unnecessary `async` functions degrade performance but unnecessary `await`s are not too bad, so while we could be more "specific" in our awaits we do not bother

  // TODO if function calls accepted the call Location, we could probably simplify the call site code generation

  if (ir.type === "Value") {
    const v = ir.value.value.value;
    return (_ctx: RuntimeContext) => v;
  } else if (ir.type === "Error") {
    const message_compiled = compile_internal(ir.value.message, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    const location = ir.value.location;
    if (ir.value.isAsync) {
      return async (ctx: RuntimeContext) => { throw new EastError(await message_compiled(ctx), { location: location }); };
    } else {
      return (ctx: RuntimeContext) => { throw new EastError(message_compiled(ctx), { location: location }); };
    }
  } else if (ir.type === "TryCatch") {
    const try_body = compile_internal(ir.value.try_body, Object.create(ctx), platform, asyncPlatformFns, platformDef, true, compilingNodes);

    const new_ctx = Object.create(ctx);
    const message_name = ir.value.message.value.name;
    const stack_name = ir.value.stack.value.name;
    new_ctx[message_name] = ir.value.message.value.type;
    new_ctx[stack_name] = ir.value.stack.value.type;
    const catch_body = compile_internal(ir.value.catch_body, new_ctx, platform, asyncPlatformFns, platformDef, true, compilingNodes);

    // Don't include finally unless necessary (Value nodes are effect free)
    const finally_body = ir.value.finally_body.type === "Value" ? undefined : compile_internal(ir.value.finally_body, Object.create(ctx), platform, asyncPlatformFns, platformDef, true, compilingNodes);

    if (ir.value.isAsync) {
      if (finally_body === undefined) {
        return async (ctx: RuntimeContext) => {
          try {
            return await try_body(Object.create(ctx))
          } catch (e) {
            if (e instanceof EastError) {
              const new_ctx: RuntimeContext = Object.create(ctx);
              new_ctx[message_name] = variant("value", e.message);
              new_ctx[stack_name] = variant("value", e.location);
              return await catch_body(new_ctx);
            } else {
              throw(e);
            }
          }
        }
      } else {
        return async (ctx: RuntimeContext) => {
          try {
            return await try_body(Object.create(ctx))
          } catch (e) {
            if (e instanceof EastError) {
              const new_ctx: RuntimeContext = Object.create(ctx);
              new_ctx[message_name] = variant("value", e.message);
              new_ctx[stack_name] = variant("value", e.location);
              return await catch_body(new_ctx);
            } else {
              throw(e);
            }
          } finally {
            await finally_body(Object.create(ctx));
          }
        }
      }
    } else {
      if (finally_body === undefined) {
        return (ctx: RuntimeContext) => {
          try {
            return try_body(Object.create(ctx))
          } catch (e) {
            if (e instanceof EastError) {
              const new_ctx: RuntimeContext = Object.create(ctx);
              new_ctx[message_name] = variant("value", e.message);
              new_ctx[stack_name] = variant("value", e.location);
              return catch_body(new_ctx);
            } else {
              throw(e);
            }
          }
        }
      } else {
        return (ctx: RuntimeContext) => {
          try {
            return try_body(Object.create(ctx))
          } catch (e) {
            if (e instanceof EastError) {
              const new_ctx: RuntimeContext = Object.create(ctx);
              new_ctx[message_name] = variant("value", e.message);
              new_ctx[stack_name] = variant("value", e.location);
              return catch_body(new_ctx);
            } else {
              throw(e);
            }
          } finally {
            finally_body(Object.create(ctx));
          }
        }
      }
    }
  } else if (ir.type === "Variable") {
    const name = ir.value.name;
    // All context values are variants - read via .value
    return (ctx: RuntimeContext) => getContextValue(ctx, name).value;
  } else if (ir.type === "Let") {
    const compiled_statement = compile_internal(ir.value.value, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    const name = ir.value.variable.value.name;
    ctx[name] = ir.value.variable.value.type;
    const boxed = requiresBoxing(ir.value.variable.value);
    if (ir.value.isAsync) {
      return async (ctx: RuntimeContext) => {
        ctx[name] = boxed
          ? variant("boxed", await compiled_statement(ctx))
          : variant("value", await compiled_statement(ctx));
        return null;
      };
    } else {
      return (ctx: RuntimeContext) => {
        ctx[name] = boxed
          ? variant("boxed", compiled_statement(ctx))
          : variant("value", compiled_statement(ctx));
        return null;
      };
    }
  } else if (ir.type === "Assign") {
    const name = ir.value.variable.value.name;
    const compiled_statement = compile_internal(ir.value.value, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    if (requiresBoxing(ir.value.variable.value)) {
      // Boxed variables: mutate in place via .value
      if (ir.value.isAsync) {
        return async (ctx: RuntimeContext) => {
          getContextValue(ctx, name).value = await compiled_statement(ctx);
          return null;
        };
      } else {
        return (ctx: RuntimeContext) => {
          getContextValue(ctx, name).value = compiled_statement(ctx);
          return null;
        };
      }
    } else {
      // Non-boxed variables: replace the variant
      if (ir.value.isAsync) {
        return async (ctx: RuntimeContext) => {
          const value = await compiled_statement(ctx);
          // We need to check in which prototype the variable lives
          while (!Object.hasOwn(ctx, name)) ctx = Object.getPrototypeOf(ctx);
          ctx[name] = variant("value", value);
          return null;
        };
      } else {
        return (ctx: RuntimeContext) => {
          const value = compiled_statement(ctx);
          // We need to check in which prototype the variable lives
          while (!Object.hasOwn(ctx, name)) ctx = Object.getPrototypeOf(ctx);
          ctx[name] = variant("value", value);
          return null;
        };
      }
    }
  } else if (ir.type === "As") {
    // in dynamically typed runtimes like Javascript, this is a no-op
    // (for statically typed runtimes this assists in unifying types in branches)
    return compile_internal(ir.value.value, ctx, platform, asyncPlatformFns, platformDef, fresh_ctx, compilingNodes);
  } else if (ir.type === "UnwrapRecursive") {
    // in dynamically typed runtimes like Javascript, this is a no-op
    // (for statically typed runtimes this assists in e.g. typing a reference or pointer)
    return compile_internal(ir.value.value, ctx, platform, asyncPlatformFns, platformDef, fresh_ctx, compilingNodes);
  } else if (ir.type === "WrapRecursive") {
    // in dynamically typed runtimes like Javascript, this is a no-op
    // (for statically typed runtimes this assists in e.g. typing a heap allocation)
    return compile_internal(ir.value.value, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
  } else if (ir.type === "Function") {
    // Compile-time type context for body compilation
    const typeCtx: Record<string, EastTypeValue> = {};
    for (const variable of ir.value.captures) {
      typeCtx[variable.value.name] = variable.value.type;
    }
    for (const parameter of ir.value.parameters) {
      typeCtx[parameter.value.name] = parameter.value.type;
    }

    const compiled_body = compile_internal(ir.value.body, typeCtx, platform, asyncPlatformFns, platformDef, true, compilingNodes);

    const capture_names = ir.value.captures.map(v => v.value.name);
    const parameter_names = ir.value.parameters.map(v => v.value.name);

    // Store original IR for potential serialization
    const originalIR = ir;

    return (ctx: RuntimeContext) => {
      // Runtime context for captured values
      const captureCtx: RuntimeContext = {};
      for (const name of capture_names) {
        captureCtx[name] = getContextValue(ctx, name);
      }

      const fn = (...args: any) => {
        const fnCtx: RuntimeContext = { ...captureCtx };
        parameter_names.forEach((name, i) => fnCtx[name] = variant("value", args[i]));
        return compiled_body(fnCtx);
      };

      // Attach IR to function for serialization support
      Object.defineProperty(fn, EAST_IR_SYMBOL, {
        value: originalIR,
        writable: false,
        enumerable: false,
        configurable: false
      });

      // Attach capture values for serialization support
      Object.defineProperty(fn, EAST_CAPTURES_SYMBOL, {
        value: captureCtx,
        writable: false,
        enumerable: false,
        configurable: false
      });

      return fn;
    }
  } else if (ir.type === "AsyncFunction") {
    // Compile-time type context for body compilation
    const typeCtx: Record<string, EastTypeValue> = {};
    for (const variable of ir.value.captures) {
      typeCtx[variable.value.name] = variable.value.type;
    }
    for (const parameter of ir.value.parameters) {
      typeCtx[parameter.value.name] = parameter.value.type;
    }

    const compiled_body = compile_internal(ir.value.body, typeCtx, platform, asyncPlatformFns, platformDef, true, compilingNodes);

    const capture_names = ir.value.captures.map(v => v.value.name);
    const parameter_names = ir.value.parameters.map(v => v.value.name);

    // Store original IR for potential serialization
    const originalIR = ir;

    return (ctx: RuntimeContext) => {
      // Runtime context for captured values
      const captureCtx: RuntimeContext = {};
      for (const name of capture_names) {
        captureCtx[name] = getContextValue(ctx, name);
      }

      const fn = (...args: any) => {
        const fnCtx: RuntimeContext = { ...captureCtx };
        parameter_names.forEach((name, i) => fnCtx[name] = variant("value", args[i]));
        return compiled_body(fnCtx); // Promise can pass through in tail position
      };

      // Attach IR to function for serialization support
      Object.defineProperty(fn, EAST_IR_SYMBOL, {
        value: originalIR,
        writable: false,
        enumerable: false,
        configurable: false
      });

      // Attach capture values for serialization support
      Object.defineProperty(fn, EAST_CAPTURES_SYMBOL, {
        value: captureCtx,
        writable: false,
        enumerable: false,
        configurable: false
      });

      return fn;
    }
  } else if (ir.type === "Call") {
    const compiled_f = compile_internal(ir.value.function, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    const compiled_args = ir.value.arguments.map(argument => compile_internal(argument, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes));
    const location = ir.value.location;

    if (ir.value.isAsync) {
      // need to await the arguments
      return async (ctx: RuntimeContext) => {
        try {
          const args: any[] = [];
          for (const compiled_arg of compiled_args) {
            args.push(await compiled_arg(ctx));
          }
          return compiled_f(ctx)(...args);
        } catch (e: unknown) {
          if (e instanceof ReturnException) {
            return e.value;
          } else if (e instanceof EastError) {
            e.location.push(...location); // The fact that we need to push the call location not the definition location means we need to handle this here
            throw(e);
          } else if (e instanceof ContinueException) {
            throw new Error(`continue failed to find label ${e.label} at ${printLocationValue(ir.value.location)}`)
          } else if (e instanceof BreakException) {
            throw new Error(`break failed to find label ${e.label} at ${printLocationValue(ir.value.location)}`)
          } else {
            throw(e);
          }
        }
      };
    } else {
      return (ctx: RuntimeContext) => {
        try {
          return compiled_f(ctx)(...compiled_args.map(arg => arg(ctx)));
        } catch (e: unknown) {
          if (e instanceof ReturnException) {
            return e.value;
          } else if (e instanceof EastError) {
            e.location.push(...location); // The fact that we need to push the call location not the definition location means we need to handle this here
            throw(e);
          } else if (e instanceof ContinueException) {
            throw new Error(`continue failed to find label ${e.label} at ${printLocationValue(ir.value.location)}`)
          } else if (e instanceof BreakException) {
            throw new Error(`break failed to find label ${e.label} at ${printLocationValue(ir.value.location)}`)
          } else {
            throw(e);
          }
        }
      }
    }
  } else if (ir.type === "CallAsync") {
    const compiled_f = compile_internal(ir.value.function, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    const compiled_args = ir.value.arguments.map(argument => compile_internal(argument, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes));
    const location = ir.value.location;

    return async (ctx: RuntimeContext) => {
      try {
        const args: any[] = [];
        for (const compiled_arg of compiled_args) {
          args.push(await compiled_arg(ctx));
        }
        return await compiled_f(ctx)(...args);
      } catch (e: unknown) {
        if (e instanceof ReturnException) {
          return e.value;
        } else if (e instanceof EastError) {
          e.location.push(...location); // The fact that we need to push the call location not the definition location means we need to handle this here
          throw(e);
        } else if (e instanceof ContinueException) {
          throw new Error(`continue failed to find label ${e.label} at ${printLocationValue(ir.value.location)}`)
        } else if (e instanceof BreakException) {
          throw new Error(`break failed to find label ${e.label} at ${printLocationValue(ir.value.location)}`)
        } else {
          throw(e);
        }
      }
    };
  } else if (ir.type === "IfElse") {
    const ifs: {
      predicate: (ctx: any) => boolean | Promise<boolean>,
      body: (ctx: any) => any
    }[] = [];
    let asyncPredicate = false;
    for (const { predicate, body } of ir.value.ifs) {
      if (predicate.value.isAsync) {
        asyncPredicate = true;
      }
      ifs.push({
        predicate: compile_internal(predicate, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes),
        body: compile_internal(body, Object.create(ctx), platform, asyncPlatformFns, platformDef, true, compilingNodes),
      });
    }
    const else_body = compile_internal(ir.value.else_body, Object.create(ctx), platform, asyncPlatformFns, platformDef, true, compilingNodes);

    if (ir.value.isAsync) {
      if (asyncPredicate) {
        return async (ctx: RuntimeContext) => {
          for (const { predicate, body } of ifs) {
            if (await predicate(ctx)) {
              return await body(Object.create(ctx));
            }
          }
          return await else_body(Object.create(ctx));
        };
      } else {
        return async (ctx: RuntimeContext) => {
          for (const { predicate, body } of ifs) {
            if (predicate(ctx) as boolean) {
              return await body(Object.create(ctx));
            }
          }
          return await else_body(Object.create(ctx));
        };
      }
    } else {
      return (ctx: RuntimeContext) => {
        for (const { predicate, body } of ifs) {
          if (predicate(ctx) as boolean) {
            return body(Object.create(ctx));
          }
        }
        return else_body(Object.create(ctx));
      };
    }
  } else if (ir.type === "Match") {
    const compiled_variant = compile_internal(ir.value.variant, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    const compiled_cases: Record<string, (ctx: RuntimeContext) => any> = {};
    const data_names: Record<string, string> = {};

    for (const { case: k, variable, body } of ir.value.cases) {
      const ctx2 = Object.create(ctx);
      const data_name = variable.value.name;
      data_names[k] = data_name;
      ctx2[data_name] = variable.value.type;
      compiled_cases[k] = compile_internal(body, ctx2, platform, asyncPlatformFns, platformDef, true, compilingNodes);
    }

    if (ir.value.isAsync) {
      if (ir.value.variant.value.isAsync) {
        return async (ctx: RuntimeContext) => {
          const v: variant = await compiled_variant(ctx);
          const ctx2: RuntimeContext = Object.create(ctx);
          ctx2[data_names[v.type]!] = variant("value", v.value);
          return await compiled_cases[v.type]!(ctx2);
        };
      } else {
        return async (ctx: RuntimeContext) => {
          const v: variant = compiled_variant(ctx);
          const ctx2: RuntimeContext = Object.create(ctx);
          ctx2[data_names[v.type]!] = variant("value", v.value);
          return await compiled_cases[v.type]!(ctx2);
        };
      }
    } else {
      return (ctx: RuntimeContext) => {
        const v: variant = compiled_variant(ctx);
        const ctx2: RuntimeContext = Object.create(ctx);
        ctx2[data_names[v.type]!] = variant("value", v.value);
        return compiled_cases[v.type]!(ctx2);
      };
    }
  } else if (ir.type === "While") {
    const compiled_predicate = compile_internal(ir.value.predicate, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    const ctx2 = Object.create(ctx);
    const compiled_body = compile_internal(ir.value.body, ctx2, platform, asyncPlatformFns, platformDef, true, compilingNodes);
    const label = ir.value.label.name;

    if (ir.value.isAsync) {
      return async (ctx: RuntimeContext) => {
        while (await compiled_predicate(ctx)) {
          try {
            const ctx2 = Object.create(ctx);
            await compiled_body(ctx2);
          } catch (e: unknown) {
            if (e instanceof ContinueException && e.label === label) {
              continue;
            } else if (e instanceof BreakException && e.label === label) {
              break;
            } else {
              throw e;
            }
          }
        }
        return null;
      };
    } else {
      return (ctx: RuntimeContext) => {
        while (compiled_predicate(ctx)) {
          try {
            const ctx2 = Object.create(ctx);
            compiled_body(ctx2);
          } catch (e: unknown) {
            if (e instanceof ContinueException && e.label === label) {
              continue;
            } else if (e instanceof BreakException && e.label === label) {
              break;
            } else {
              throw e;
            }
          }
        }
        return null;
      };
    }
  } else if (ir.type === "ForArray") {
    const value_type = (expandTypeValue(ir.value.array.value.type) as ArrayTypeValue).value;
    const compiled_array = compile_internal(ir.value.array, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    const ctx2 = Object.create(ctx);
    const key_name = ir.value.key.value.name;
    const value_name = ir.value.value.value.name;
    ctx2[key_name] = variant("Integer", null);
    ctx2[value_name] = value_type;
    const compiled_body = compile_internal(ir.value.body, ctx2, platform, asyncPlatformFns, platformDef, true, compilingNodes);
    const label = ir.value.label.name;

    if (ir.value.isAsync) {
      return async (ctx: RuntimeContext) => {
        const array = await compiled_array(ctx);
        lockForIteration(array);
        try {
          for (const [key, value] of array.entries()) {
            const ctx2: RuntimeContext = Object.create(ctx);
            ctx2[key_name] = variant("value", BigInt(key));
            ctx2[value_name] = variant("value", value);
            try {
              await compiled_body(ctx2);
            } catch (e: unknown) {
              if (e instanceof ContinueException && e.label === label) {
                continue;
              } else if (e instanceof BreakException && e.label === label) {
                break;
              } else {
                throw e;
              }
            }
          }
          return null;
        } finally {
          unlockForIteration(array);
        }
      };
    } else {
        return (ctx: RuntimeContext) => {
        const array = compiled_array(ctx);
        lockForIteration(array);
        try {
          for (const [key, value] of array.entries()) {
            const ctx2: RuntimeContext = Object.create(ctx);
            ctx2[key_name] = variant("value", BigInt(key));
            ctx2[value_name] = variant("value", value);
            try {
              compiled_body(ctx2);
            } catch (e: unknown) {
              if (e instanceof ContinueException && e.label === label) {
                continue;
              } else if (e instanceof BreakException && e.label === label) {
                break;
              } else {
                throw e;
              }
            }
          }
          return null;
        } finally {
          unlockForIteration(array);
        }
      };
    }
  } else if (ir.type === "ForSet") {
    const key_type = (expandTypeValue(ir.value.set.value.type) as SetTypeValue).value;
    const compiled_set = compile_internal(ir.value.set, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    const ctx2 = Object.create(ctx);
    const key_name = ir.value.key.value.name;
    ctx2[key_name] = key_type;
    const compiled_body = compile_internal(ir.value.body, ctx2, platform, asyncPlatformFns, platformDef, true, compilingNodes);
    const label = ir.value.label.name;

    if (ir.value.isAsync) {
      return async (ctx: RuntimeContext) => {
        const set = await compiled_set(ctx);
        lockForIteration(set);
        try {
          for (const key of set) {
            const ctx2: RuntimeContext = Object.create(ctx);
            ctx2[key_name] = variant("value", key);
            try {
              await compiled_body(ctx2);
            } catch (e: unknown) {
              if (e instanceof ContinueException && e.label === label) {
                continue;
              } else if (e instanceof BreakException && e.label === label) {
                break;
              } else {
                throw e;
              }
            }
          }
          return null;
        } finally {
          unlockForIteration(set);
        }
      };
    } else {
        return (ctx: RuntimeContext) => {
        const set = compiled_set(ctx);
        lockForIteration(set);
        try {
          for (const key of set) {
            const ctx2: RuntimeContext = Object.create(ctx);
            ctx2[key_name] = variant("value", key);
            try {
              compiled_body(ctx2);
            } catch (e: unknown) {
              if (e instanceof ContinueException && e.label === label) {
                continue;
              } else if (e instanceof BreakException && e.label === label) {
                break;
              } else {
                throw e;
              }
            }
          }
          return null;
        } finally {
          unlockForIteration(set);
        }
      };
    }
  } else if (ir.type === "ForDict") {
    const key_type = (expandTypeValue(ir.value.dict.value.type) as DictTypeValue).value.key;
    const value_type = (expandTypeValue(ir.value.dict.value.type) as DictTypeValue).value.value;
    const compiled_dict = compile_internal(ir.value.dict, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    const ctx2 = Object.create(ctx);
    const key_name = ir.value.key.value.name;
    const value_name = ir.value.value.value.name;
    ctx2[key_name] = key_type;
    ctx2[value_name] = value_type;
    const compiled_body = compile_internal(ir.value.body, ctx2, platform, asyncPlatformFns, platformDef, true, compilingNodes);
    const label = ir.value.label.name;

    if (ir.value.isAsync) {
      return async (ctx: RuntimeContext) => {
        const dict = await compiled_dict(ctx);
        lockForIteration(dict);
        try {
          for (const [key, value] of dict) {
            const ctx2: RuntimeContext = Object.create(ctx);
            ctx2[key_name] = variant("value", key);
            ctx2[value_name] = variant("value", value);
            try {
              await compiled_body(ctx2);
            } catch (e: unknown) {
              if (e instanceof ContinueException && e.label === label) {
                continue;
              } else if (e instanceof BreakException && e.label === label) {
                break;
              } else {
                throw e;
              }
            }
          }
          return null;
        } finally {
          unlockForIteration(dict);
        }
      };
    } else {
        return (ctx: RuntimeContext) => {
        const dict = compiled_dict(ctx);
        lockForIteration(dict);
        try {
          for (const [key, value] of dict) {
            const ctx2: RuntimeContext = Object.create(ctx);
            ctx2[key_name] = variant("value", key);
            ctx2[value_name] = variant("value", value);
            try {
              compiled_body(ctx2);
            } catch (e: unknown) {
              if (e instanceof ContinueException && e.label === label) {
                continue;
              } else if (e instanceof BreakException && e.label === label) {
                break;
              } else {
                throw e;
              }
            }
          }
          return null;
        } finally {
          unlockForIteration(dict);
        }
      };
    }
  } else if (ir.type === "Block") {
    // The pattern of creating a new context (e.g. a function) and then immediately invoking a block (e.g. as the function body) is very common.
    // Here we avoid creating a second context when possible, as an optimization.
    if (fresh_ctx) {
      const compiled_statements: ((ctx: RuntimeContext) => any)[] = [];
      for (const statement of ir.value.statements) {
        const compiled_statement = compile_internal(statement, ctx, platform, asyncPlatformFns, platformDef, true, compilingNodes);
        compiled_statements.push(compiled_statement);
      }
      if (ir.value.isAsync) {
        return async (ctx: RuntimeContext) => {
          let ret = null;
          for (const statement of compiled_statements) {
            ret = await statement(ctx);
          }
          return ret;
        };
      } else {
        return (ctx: RuntimeContext) => {
          let ret = null;
          for (const statement of compiled_statements) {
            ret = statement(ctx);
          }
          return ret;
        };
      }
    } else {
      const ctx2 = Object.create(ctx);
      const compiled_statements: ((ctx: RuntimeContext) => any)[] = [];
      for (const statement of ir.value.statements) {
        const compiled_statement = compile_internal(statement, ctx2, platform, asyncPlatformFns, platformDef, true, compilingNodes);
        compiled_statements.push(compiled_statement);
      }
      if (ir.value.isAsync) {
        return async (ctx: RuntimeContext) => {
          const ctx2 = Object.create(ctx);
          let ret = null;
          for (const statement of compiled_statements) {
            ret = await statement(ctx2);
          }
          return ret;
        };
      } else {
          return (ctx: RuntimeContext) => {
          const ctx2 = Object.create(ctx);
          let ret = null;
          for (const statement of compiled_statements) {
            ret = statement(ctx2);
          }
          return ret;
        }
      }
    }
  } else if (ir.type === "GetField") {
    const struct = compile_internal(ir.value.struct, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    const field = ir.value.field;
    if (ir.value.isAsync) {
      return async (ctx: RuntimeContext) => (await struct(ctx))[field];
    } else {
      return (ctx: RuntimeContext) => struct(ctx)[field];
    }
  } else if (ir.type === "Struct") {
    const fields = ir.value.fields.map(f => {
      return compile_internal(f.value, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    });
    const keys = ir.value.fields.map(f => f.name);
    if (ir.value.isAsync) {
      return async (ctx: RuntimeContext) => {
        const fs: [string, any][] = [];
        for (const [i, a] of fields.entries()) {
          fs.push([keys[i]!, await a(ctx)]);
        }
        return Object.fromEntries(fs);
      };
    } else {
      return (ctx: RuntimeContext) => Object.fromEntries(fields.map((a, i) => [keys[i]!, a(ctx)]));
    }
  } else if (ir.type === "Variant") {
    const k = ir.value.case;
    const v = compile_internal(ir.value.value, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    if (ir.value.isAsync) {
      return async (ctx: RuntimeContext) => variant(k, await v(ctx));
    } else {
      return (ctx: RuntimeContext) => variant(k, v(ctx));
    }
  } else if (ir.type === "NewRef") {
    const value = compile_internal(ir.value.value, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    if (ir.value.isAsync) {
      return async (ctx: RuntimeContext) => ref(await value(ctx));
    } else {
      return (ctx: RuntimeContext) => ref(value(ctx));
    }
  } else if (ir.type === "NewArray") {
    const values = ir.value.values.map(a => {
      return compile_internal(a, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes)
    });
    if (ir.value.isAsync) {
      return async (ctx: RuntimeContext) => {
        let vals: any[] = [];
        for (const a of values) {
          vals.push(await a(ctx));
        }
        return vals;
      }
    } else {
      return (ctx: RuntimeContext) => values.map(a => a(ctx));
    }
  } else if (ir.type === "NewSet") {
    const values = ir.value.values.map(a => {
      return compile_internal(a, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes)
    });
    const keyComparer = compareFor(ir.value.type.value);
    if (ir.value.isAsync) {
      return (ctx: RuntimeContext) => {
        const keys: any[] = [];
        for (const a of values) {
          keys.push(a(ctx));
        }
        return new SortedSet(keys, keyComparer);
      }
    } else {
      return (ctx: RuntimeContext) => new SortedSet(values.map(a => a(ctx)), keyComparer);
    }
  } else if (ir.type === "NewDict") {
    const values = ir.value.values.map(({key, value}) => {
      return [compile_internal(key, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes), compile_internal(value, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes)] as const;
    });
    const keyComparer = compareFor(ir.value.type.value.key);
    if (ir.value.isAsync) {
      return async (ctx: RuntimeContext) => {
        const entries: [any, any][] = [];
        for (const [k, v] of values) {
          entries.push([await k(ctx), await v(ctx)]);
        }
        return new SortedMap(entries, keyComparer);
      }
    } else {
      return (ctx: RuntimeContext) => new SortedMap(values.map(([k, v]) => [k(ctx), v(ctx)]), keyComparer);
    }
  } else if (ir.type === "Return") {
    const compiled_value = compile_internal(ir.value.value, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes);
    if (ir.value.isAsync) {
      return async (ctx: RuntimeContext) => {
        throw new ReturnException(await compiled_value(ctx));
      };
    } else {
      return (ctx: RuntimeContext): any => {
        throw new ReturnException(compiled_value(ctx));
      };
    }
  } else if (ir.type === "Continue") {
    const label = ir.value.label;
    return (_ctx: RuntimeContext): any => {
      throw new ContinueException(label.name);
    };
  } else if (ir.type === "Break") {
    const label = ir.value.label;
    return (_ctx: RuntimeContext): any => {
      throw new BreakException(label.name);
    };
  } else if (ir.type === "Builtin") {
    let argsAsync = false;
    const args = ir.value.arguments.map((a, _i) => {
      if (a.value.isAsync) {
        argsAsync = true;
      }

      return compile_internal(a, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes)
    });

    // Special optimization for regex builtins with literal pattern/flags
    if ((ir.value.builtin === "RegexContains" || ir.value.builtin === "RegexIndexOf" || ir.value.builtin === "RegexReplace") &&
    ir.value.arguments[1]?.type === "Value" &&
    ir.value.arguments[2]?.type === "Value") {
      if (ir.value.arguments[1].value.value.type !== "String") {
        throw new Error(`Regex builtin pattern argument must be String literal at ${printLocationValue(ir.value.arguments[1].value.location)}`);
      }
      if (ir.value.arguments[2].value.value.type !== "String") {
        throw new Error(`Regex builtin flags argument must be String literal at ${printLocationValue(ir.value.arguments[2].value.location)}`);
      }

      // Compile regex once at closure compilation time
      const pattern = ir.value.arguments[1].value.value.value as string;
      const flags = ir.value.arguments[2].value.value.value as string;
      const textArg = args[0]!; // Already compiled text argument

      if (ir.value.builtin === "RegexContains") {
        const compiledRegex = new RegExp(pattern, flags);
        return (ctx: RuntimeContext) => compiledRegex.test(textArg(ctx));
      } else if (ir.value.builtin === "RegexIndexOf") {
        const compiledRegex = new RegExp(pattern, flags);
        return (ctx: RuntimeContext) => {
          const text = textArg(ctx);
          const codeUnitIndex = text.search(compiledRegex);
          if (codeUnitIndex === -1) return -1n;

          // Convert code unit index to codepoint index
          let codepointIndex = 0;
          let codeUnitPos = 0;
          for (const char of text) {
            if (codeUnitPos === codeUnitIndex) {
              return BigInt(codepointIndex);
            }
            codeUnitPos += char.length;
            codepointIndex++;
          }
          return -1n;
        };
      } else { // RegexReplace
        // Precompile regex with global flag for replaceAll semantics
        const globalFlags = flags.includes('g') ? flags : flags + 'g';
        const compiledRegex = new RegExp(pattern, globalFlags);

        // Check if replacement is also constant for full optimization
        if (ir.value.arguments[3]?.type === "Value") {
          if (ir.value.arguments[3].value.value.type !== "String") {
            throw new Error(`RegexReplace builtin replacement argument must be String literal at ${printLocationValue(ir.value.arguments[3].value.location)}`);
          }

          // FULL OPTIMIZATION: Pattern, flags, and replacement are all constant
          const replacement = ir.value.arguments[3].value.value.value as string;

          // Validate replacement string: only allow $$, $1-$9, and $<
          // This is stricter than JavaScript's native behavior but provides clear, consistent semantics
          // and avoids backend-specific features like $&, $`, $'
          let i = 0;
          while (i < replacement.length) {
            const char = replacement[i]!;
            if (char === '$') {
              i += char.length;
              let char2 = replacement[i];
              if (char2 === undefined) {
                return (_ctx: RuntimeContext) => { throw new EastError(`invalid regex replacement string: unescaped $ at end of string`, { location: ir.value.arguments[3].value.location }) };
              } else if (char2 === '$') {
                i += 1;
              } else if (char2 >= '1' && char2 <= '9') {
                i += 1;
                char2 = replacement[i];
                while (char2 !== undefined && char2 >= '0' && char2 <= '9') {
                  i += 1;
                  char2 = replacement[i];
                }
              } else if (char2 === '<') {
                // Scan until closing >
                i += 1;
                const init_i = i;
                char2 = replacement[i];
                while (true) {
                  if (char2 === undefined) {
                    return (_ctx: RuntimeContext) => { throw new EastError(`invalid regex replacement string: unterminated group name in $<...>`, { location: ir.value.arguments[3].value.location }) };
                  }
                  if (char2 === '>') {
                    break;
                  }
                  if (!((char2 >= '0' && char2 <= '9') || (char2 >= 'a' && char2 <= 'z') || (char2 >= 'A' && char2 <= 'Z') || char2 === '_')) {
                    return (_ctx: RuntimeContext) => { throw new EastError(`invalid regex replacement string: invalid character ${JSON.stringify(char2)} in group name in $<...>`, { location: ir.value.arguments[3].value.location }) };
                  }
                  i += 1;
                  char2 = replacement[i];
                }
                if (i === init_i) {
                  return (_ctx: RuntimeContext) => { throw new EastError(`invalid regex replacement string: empty group name in $<>`, { location: ir.value.arguments[3].value.location }) };
                }
                i += 1; // for closing >
              } else {
                return (_ctx: RuntimeContext) => { throw new EastError(`invalid regex replacement string: unescaped $ at $${char2}`, { location: ir.value.arguments[3].value.location }) };
              }
            } else {
              i += char.length;
            }
          }

          return (ctx: RuntimeContext) => {
            const text = textArg(ctx);
            return text.replaceAll(compiledRegex, replacement);
          };
        } else {
          // PARTIAL OPTIMIZATION: Pattern and flags constant, replacement dynamic
          const replacementArg = args[3]!;
          return (ctx: RuntimeContext) => {
            const text = textArg(ctx);
            const replacement = replacementArg(ctx);

            // Validate replacement string: only allow $$, $1-$9, and $<
            // This is stricter than JavaScript's native behavior but provides clear, consistent semantics
            // and avoids backend-specific features like $&, $`, $'
            let i = 0;
            while (i < replacement.length) {
              const char = replacement[i]!;
              if (char === '$') {
                i += char.length;
                let char2 = replacement[i];
                if (char2 === undefined) {
                  throw new EastError(`invalid regex replacement string: unescaped $ at end of string`, { location: ir.value.arguments[3].value.location });
                } else if (char2 === '$') {
                  i += 1;
                } else if (char2 >= '1' && char2 <= '9') {
                  i += 1;
                  char2 = replacement[i];
                  while (char2 !== undefined && char2 >= '0' && char2 <= '9') {
                    i += 1;
                    char2 = replacement[i];
                  }
                } else if (char2 === '<') {
                  // Scan until closing >
                  i += 1;
                  const init_i = i;
                  char2 = replacement[i];
                  while (true) {
                    if (char2 === undefined) {
                      throw new EastError(`invalid regex replacement string: unterminated group name in $<...>`, { location: ir.value.arguments[3].value.location });
                    }
                    if (char2 === '>') {
                      break;
                    }
                    if (!((char2 >= '0' && char2 <= '9') || (char2 >= 'a' && char2 <= 'z') || (char2 >= 'A' && char2 <= 'Z') || char2 === '_')) {
                      throw new EastError(`invalid regex replacement string: invalid character ${JSON.stringify(char2)} in group name in $<...>`, { location: ir.value.arguments[3].value.location });
                    }
                    i += 1;
                    char2 = replacement[i];
                  }
                  if (i === init_i) {
                    throw new EastError(`invalid regex replacement string: empty group name in $<>`, { location: ir.value.arguments[3].value.location });
                  }
                  i += 1; // for closing >
                } else {
                  throw new EastError(`invalid regex replacement string: unescaped $ at $${char2}`, { location: ir.value.arguments[3].value.location });
                }
              } else {
                i += char.length;
              }
            }
            return text.replaceAll(compiledRegex, replacement);
          };
        }
      }
    }

    const evaluator = builtin_evaluators[ir.value.builtin](ir.value.location, platformDef, ...ir.value.type_parameters);
    if (argsAsync) {
      return async (ctx: RuntimeContext) => {
        const args_resolved: any[] = [];
        for (const a of args) {
          args_resolved.push(await a(ctx));
        }
        return evaluator(...args_resolved);
      }
    } else {
      return (ctx: RuntimeContext) => evaluator(...args.map(a => a(ctx)));
    }
  } else if (ir.type === "Platform") {
    let argsAsync = false;
    const args = ir.value.arguments.map(a => {
      if (a.value.isAsync) {
        argsAsync = true;
      }

      return compile_internal(a, ctx, platform, asyncPlatformFns, platformDef, false, compilingNodes)
    });

    // Look up platform function definition to check if generic
    const platformFn = platformDef.find(p => p.name === ir.value.name);

    const typeParams = ir.value.type_parameters ?? [];

    // Get evaluator - for generic functions, call factory with type params
    let evaluator: (...args: any[]) => any;
    if (typeParams.length > 0 && platformFn?.type_parameters && platformFn.type_parameters.length > 0) {
      // Generic platform function - fn is a factory that takes type params
      if (!platformFn.fn) {
        // Missing generic platform function - create stub that throws at runtime
        const name = ir.value.name;
        const location = ir.value.location;
        evaluator = () => {
          throw new EastError(`Platform function '${name}' is not available`, { location });
        };
      } else {
        evaluator = platformFn.fn(...typeParams);
      }
    } else {
      // Non-generic - use platform map for backwards compatibility
      const platformEvaluator = platform[ir.value.name];
      if (platformEvaluator === undefined) {
        // Missing platform function - create stub that throws at runtime
        const name = ir.value.name;
        const location = ir.value.location;
        evaluator = () => {
          throw new EastError(`Platform function '${name}' is not available`, { location });
        };
      } else {
        evaluator = platformEvaluator;
      }
    }

    if (argsAsync) {
      return async (ctx: RuntimeContext) => {
        const args_resolved: any[] = [];
        for (const a of args) {
          args_resolved.push(await a(ctx));
        }
        return evaluator(...args_resolved); // evaluator can return Promise unconditionally in tail position if the platform function is async
      }
    } else {
      return (ctx: RuntimeContext) => evaluator(...args.map(a => a(ctx))); // evaluator can return Promise unconditionally in tail position if the platform function is async
    }
  } else {
    throw new Error(`Unhandled IR type ${(ir satisfies never as IR).type} at ${printLocationValue((ir as IR).value.location)}`); // The `satisfies never` here ensures that this branch is unreachable if all IR types are handled
  }
}

/** Used to call a compiled function with the given arguments and handle errors within builtin functions */
function call_function(location: LocationValue[], compiled_f: (...args: any[]) => any, ...args: any[]): any {
  try {
    return compiled_f(...args);
  } catch (e: unknown) {
    if (e instanceof ReturnException) {
      return e.value;
    } else if (e instanceof EastError) {
      e.location.push(...location); // The fact that we need to push the call location not the definition location means we need to handle this here
      throw(e);
    } else if (e instanceof ContinueException) {
      throw new Error(`continue failed to find label ${e.label} at ${printLocationValue(location)}`)
    } else if (e instanceof BreakException) {
      throw new Error(`break failed to find label ${e.label} at ${printLocationValue(location)}`)
    } else {
      throw(e);
    }
  }
}


/** @internal */
const builtin_evaluators: Record<BuiltinName, (location: LocationValue[], platformDef: PlatformFunction[], ...arg_types: any[]) => (...args: any[]) => any> = {
  Is: (_location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue) => isFor(T),
  Equal: (_location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue) => equalFor(T),
  NotEqual: (_location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue) => notEqualFor(T),
  Less: (_location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue) => lessFor(T),
  LessEqual: (_location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue) => lessEqualFor(T),
  Greater: (_location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue) => greaterFor(T),
  GreaterEqual: (_location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue) => greaterEqualFor(T),
  Diff: (_location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue) => diffFor(T),
  ApplyPatch: (location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue) => {
    const apply = applyFor(T);
    return (base: any, patch: any) => {
      try {
        return apply(base, patch);
      } catch (e) {
        if (e instanceof ConflictError) {
          throw new EastError(e.message, { location });
        }
        throw e;
      }
    };
  },
  ComposePatch: (location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue) => {
    const compose = composeFor(T);
    return (first: any, second: any) => {
      try {
        return compose(first, second);
      } catch (e) {
        if (e instanceof ConflictError) {
          throw new EastError(e.message, { location });
        }
        throw e;
      }
    };
  },
  InvertPatch: (_location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue) => invertFor(T),
  BooleanNot: (_location: LocationValue[]) => (x: boolean) => !x,
  BooleanOr: (_location: LocationValue[]) => (x: boolean, y: boolean) => x || y,
  BooleanAnd: (_location: LocationValue[]) => (x: boolean, y: boolean) => x && y,
  BooleanXor: (_location: LocationValue[]) => (x: boolean, y: boolean) => x !== y,
  
  IntegerToFloat: (_location: LocationValue[]) => (x: bigint) => Number(x),
  IntegerNegate: (_location: LocationValue[]) => (x: bigint) => BigInt.asIntN(64, -x),
  IntegerAdd: (_location: LocationValue[]) => (x: bigint, y: bigint) => BigInt.asIntN(64, x + y),
  IntegerSubtract: (_location: LocationValue[]) => (x: bigint, y: bigint) => BigInt.asIntN(64, x - y),
  IntegerMultiply: (_location: LocationValue[]) => (x: bigint, y: bigint) => BigInt.asIntN(64, x * y),
  IntegerDivide: (_location: LocationValue[]) => (x: bigint, y: bigint) => x === 0n ? 0n : x / y,
  IntegerRemainder: (_location: LocationValue[]) => (x: bigint, y: bigint) => x === 0n ? 0n : x % y,
  IntegerPow: (_location: LocationValue[]) => (x: bigint, y: bigint) => y >= 0n ? BigInt.asIntN(64, x ** y) : 0n,
  IntegerAbs: (_location: LocationValue[]) => (x: bigint) => BigInt.asIntN(64, x < 0n ? -x : x),
  IntegerSign: (_location: LocationValue[]) => (x: bigint) => x > 0n ? 1n : x < 0n ? -1n : 0n,
  IntegerLog: (_location: LocationValue[]) => (value: bigint, base: bigint) => {
    if (value === 0n) return 0n;
    if (base <= 1n) return 0n; // Invalid base
    
    let abs_value = value < 0n ? -value : value;
    let result = 0n;
    
    while (abs_value >= base) {
      abs_value = abs_value / base;
      result = result + 1n;
    }
    
    return result;
  },
  
  FloatToInteger: (location: LocationValue[]) => (x: number) => {
    if (Number.isNaN(x)) throw new EastError("Cannot convert NaN to integer", { location });
    if (x >= 9223372036854775808) throw new EastError("Float too high to convert to integer", { location });
    if (x < -9223372036854775808) throw new EastError("Float too low to convert to integer", { location });
    if (!Number.isInteger(x)) { throw new EastError("Cannot convert non-integer float to integer", { location }); }
    return BigInt(x);
  },
  FloatNegate: (_location: LocationValue[]) => (x: bigint) => -x,
  FloatAdd: (_location: LocationValue[]) => (x: number, y: number) => x + y,
  FloatSubtract: (_location: LocationValue[]) => (x: number, y: number) => x - y,
  FloatMultiply: (_location: LocationValue[]) => (x: number, y: number) => x * y,
  FloatDivide: (_location: LocationValue[]) => (x: number, y: number) => x / y,
  FloatRemainder: (_location: LocationValue[]) => (x: number, y: number) => x % y,
  FloatPow: (_location: LocationValue[]) => (x: number, y: number) => x ** y,
  FloatAbs: (_location: LocationValue[]) => (x: number) => x < 0 ? -x : x,
  FloatSign: (_location: LocationValue[]) => (x: number) => x > 0 ? 1 : x < 0 ? -1 : 0, // What sign is NaN?
  FloatSqrt: (_location: LocationValue[]) => (value: number) => Math.sqrt(value),
  FloatLog: (_location: LocationValue[]) => (value: number) => Math.log(value),
  FloatExp: (_location: LocationValue[]) => (value: number) => Math.exp(value),
  FloatSin: (_location: LocationValue[]) => (value: number) => Math.sin(value),
  FloatCos: (_location: LocationValue[]) => (value: number) => Math.cos(value),
  FloatTan: (_location: LocationValue[]) => (value: number) => Math.tan(value),
  
  Print: (_location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue) => {
    return printFor(T);
  },
  Parse: (location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue) => {
    const p = parseFor(T);
    return (x: string) => {
      const result = p(x);
      if (result.success) {
        return result.value;
      } else {
        throw new EastError(`Failed to parse ${printTypeValue(T)} at ${result.position}: ${result.error}`, { location });
      }
    }
  },
  StringConcat: (_location: LocationValue[]) => (x: string, y: string) => x + y,
  StringRepeat: (_location: LocationValue[]) => (x: string, y: bigint) => y > 0n ? x.repeat(Number(y)) : "",
  StringLength: (_location: LocationValue[]) => (x: string) => {
    let len = 0;
    for (const _ of x) len++;
    return BigInt(len);
  },
  StringSubstring: (_location: LocationValue[]) => (x: string, from: bigint, to: bigint) => {
    // Convert bigint indices to numbers, handle forgiving semantics like JavaScript
    let fromNum = Number(from);
    let toNum = Number(to);
    
    // Handle negative indices and lengths (forgiving semantics)
    if (fromNum < 0) fromNum = 0;
    if (toNum < 0) toNum = 0;
    if (fromNum > toNum) {
      toNum = fromNum;
    }
    
    // Convert codepoint indices to code unit indices
    let codeUnitFrom = 0;
    let codeUnitTo = 0;
    let codepointIndex = 0;
    
    for (const char of x) {
      if (codepointIndex === fromNum) {
        codeUnitFrom = codeUnitTo;
      }
      if (codepointIndex === toNum) {
        break;
      }
      codeUnitTo += char.length;
      codepointIndex++;
    }
    
    // If 'from' is beyond string length, return empty string
    if (fromNum >= codepointIndex) return "";
    
    // If 'to' is beyond string length, use string end
    if (toNum > codepointIndex) {
      codeUnitTo = x.length;
    }
    
    return x.substring(codeUnitFrom, codeUnitTo);
  },
  StringUpperCase: (_location: LocationValue[]) => (x: string) => x.toUpperCase(),
  StringLowerCase: (_location: LocationValue[]) => (x: string) => x.toLowerCase(),
  StringSplit: (_location: LocationValue[]) => (x: string, delimiter: string) => {
    if (delimiter === "") {
      if (x === "") {
        // Split always returns at least one element
        return [""];
      } else {
        // Split into individual codepoints
        return [...x];
      }
    }
    return x.split(delimiter);
  },
  StringTrim: (_location: LocationValue[]) => (x: string) => x.trim(),
  StringTrimStart: (_location: LocationValue[]) => (x: string) => x.trimStart(),
  StringTrimEnd: (_location: LocationValue[]) => (x: string) => x.trimEnd(),
  StringStartsWith: (_location: LocationValue[]) => (x: string, prefix: string) => x.startsWith(prefix),
  StringEndsWith: (_location: LocationValue[]) => (x: string, suffix: string) => x.endsWith(suffix),
  StringContains: (_location: LocationValue[]) => (x: string, substring: string) => x.includes(substring),
  StringIndexOf: (_location: LocationValue[]) => (x: string, substring: string) => {
    const codeUnitIndex = x.indexOf(substring);
    if (codeUnitIndex === -1) return -1n;
    
    // Special case for empty substring - it's always found at position 0
    if (substring === "") return BigInt(codeUnitIndex);
    
    // Convert code unit index to codepoint index
    let codepointIndex = 0;
    let codeUnitPos = 0;
    for (const char of x) {
      if (codeUnitPos === codeUnitIndex) {
        return BigInt(codepointIndex);
      }
      codeUnitPos += char.length;
      codepointIndex++;
    }
    return -1n;
  },
  StringReplace: (_location: LocationValue[]) => (x: string, searchValue: string, replaceValue: string) => {
    // Replace all occurrences (like JavaScript's string.replaceAll with string)
    return x.replaceAll(searchValue, replaceValue);
  },
  RegexContains: (_location: LocationValue[]) => (text: string, pattern: string, flags: string) => {
    const regex = new RegExp(pattern, flags);
    return regex.test(text);
  },
  RegexIndexOf: (_location: LocationValue[]) => (text: string, pattern: string, flags: string) => {
    const regex = new RegExp(pattern, flags);
    const codeUnitIndex = text.search(regex);
    if (codeUnitIndex === -1) return -1n;

    // Convert code unit index to codepoint index
    let codepointIndex = 0;
    let codeUnitPos = 0;
    for (const char of text) {
      if (codeUnitPos === codeUnitIndex) {
        return BigInt(codepointIndex);
      }
      codeUnitPos += char.length;
      codepointIndex++;
    }
    return -1n;
  },
  RegexReplace: (location: LocationValue[]) => (text: string, pattern: string, flags: string, replacement: string) => {
    // Ensure global flag is set for replaceAll semantics
    const globalFlags = flags.includes('g') ? flags : flags + 'g';
    const regex = new RegExp(pattern, globalFlags);

    // Validate replacement string: only allow $$, $1-$9, and $<
    // This is stricter than JavaScript's native behavior but provides clear, consistent semantics
    // and avoids backend-specific features like $&, $`, $'
    let i = 0;
    while (i < replacement.length) {
      const char = replacement[i]!;
      if (char === '$') {
        i += char.length;
        let char2 = replacement[i];
        if (char2 === undefined) {
          throw new EastError(`invalid regex replacement string: unescaped $ at end of string`, { location });
        } else if (char2 === '$') {
          i += 1;
        } else if (char2 >= '1' && char2 <= '9') {
          i += 1;
          char2 = replacement[i];
          while (char2 !== undefined && char2 >= '0' && char2 <= '9') {
            i += 1;
            char2 = replacement[i];
          }
        } else if (char2 === '<') {
          // Scan until closing >
          i += 1;
          const init_i = i;
          char2 = replacement[i];
          while (true) {
            if (char2 === undefined) {
              throw new EastError(`invalid regex replacement string: unterminated group name in $<...>`, { location });
            }
            if (char2 === '>') {
              break;
            }
            if (!((char2 >= '0' && char2 <= '9') || (char2 >= 'a' && char2 <= 'z') || (char2 >= 'A' && char2 <= 'Z') || char2 === '_')) {
              throw new EastError(`invalid regex replacement string: invalid character ${JSON.stringify(char2)} in group name in $<...>`, { location });
            }
            i += 1;
            char2 = replacement[i];
          }
          if (i === init_i) {
            throw new EastError(`invalid regex replacement string: empty group name in $<>`, { location });
          }
          i += 1; // for closing >
        } else {
          throw new EastError(`invalid regex replacement string: unescaped $ at $${char2}`, { location });
        }
      } else {
        i += char.length;
      }
    }
    return text.replaceAll(regex, replacement);
  },
  StringEncodeUtf8: (_location: LocationValue[]) => {
    // do not add BOM for UTF-8
    const encoder = new TextEncoder();
    return (x: string) => {
      return encoder.encode(x);
    };
  },
  StringEncodeUtf16: (_location: LocationValue[]) => {
    // always use little-endian with BOM (most common in practice)
    return (x: string) => {
      const buffer = new BufferWriter();
      buffer.writeUint8(0xFF);
      buffer.writeUint8(0xFE);
      for (let i = 0; i < x.length; i++) {
        const codeUnit = x.charCodeAt(i);
        buffer.writeUint16LE(codeUnit);
      }
      return buffer.toUint8Array();
    };
  },
  StringParseJSON: (location: LocationValue[], _platformDef: PlatformFunction[], type: EastTypeValue) => {
    const fromJSON = fromJSONFor(type);
    return (x: string) => {
      let parsed: any;
      try {
        parsed = JSON.parse(x);
      } catch (e: unknown) {
        throw new EastError(`Failed to parse JSON: ${(e as Error).message}`, { location });
      }
      try {
        return fromJSON(parsed);
      } catch (e: unknown) {
        throw new EastError(`Failed to convert JSON to ${printTypeValue(type)}: ${(e as Error).message}`, { location });
      }
    }
  },
  StringPrintJSON: (_location: LocationValue[], _platformDef: PlatformFunction[], type: EastTypeValue) => {
    const toJSON = toJSONFor(type);
    return (x: any) => JSON.stringify(toJSON(x));
  },
  
  DateTimeGetYear: (_location: LocationValue[]) => (date: Date) => BigInt(date.getUTCFullYear()),
  DateTimeGetMonth: (_location: LocationValue[]) => (date: Date) => BigInt(date.getUTCMonth() + 1), // JavaScript months are 0-based, East uses 1-based
  DateTimeGetDayOfMonth: (_location: LocationValue[]) => (date: Date) => BigInt(date.getUTCDate()),
  DateTimeGetHour: (_location: LocationValue[]) => (date: Date) => BigInt(date.getUTCHours()),
  DateTimeGetMinute: (_location: LocationValue[]) => (date: Date) => BigInt(date.getUTCMinutes()),
  DateTimeGetSecond: (_location: LocationValue[]) => (date: Date) => BigInt(date.getUTCSeconds()),
  DateTimeGetDayOfWeek: (_location: LocationValue[]) => (date: Date) => {
    const jsDay = date.getUTCDay(); // JavaScript: 0=Sunday, 1=Monday, ..., 6=Saturday
    return BigInt(jsDay === 0 ? 7 : jsDay); // ISO 8601: 1=Monday, 2=Tuesday, ..., 7=Sunday
  },
  DateTimeGetMillisecond: (_location: LocationValue[]) => (date: Date) => BigInt(date.getUTCMilliseconds()),
  DateTimeAddMilliseconds: (_location: LocationValue[]) => (date: Date, milliseconds: bigint) => new Date(date.getTime() + Number(milliseconds)),
  DateTimeDurationMilliseconds: (_location: LocationValue[]) => (date1: Date, date2: Date) => BigInt(date1.getTime() - date2.getTime()),
  DateTimeToEpochMilliseconds: (_location: LocationValue[]) => (date: Date) => BigInt(date.getTime()),
  DateTimeFromEpochMilliseconds: (_location: LocationValue[]) => (milliseconds: bigint) => new Date(Number(milliseconds)),
  DateTimeFromComponents: (_location: LocationValue[]) => (year: bigint, month: bigint, day: bigint, hour: bigint, minute: bigint, second: bigint, millisecond: bigint) =>
    new Date(Date.UTC(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute), Number(second), Number(millisecond))),
  DateTimePrintFormat: (_location: LocationValue[]) => (date: Date, tokens: DateTimeFormatToken[]) => {
    return formatDateTime(date, tokens);
  },
  DateTimeParseFormat: (location: LocationValue[]) => (str: string, tokens: DateTimeFormatToken[]) => {
    const result = parseDateTimeFormatted(str, tokens);
    if (result.success) {
      return result.value;
    } else {
      throw new EastError(`Failed to parse datetime at position ${result.position}: ${result.error}`, { location });
    }
  },

  BlobSize: (_location: LocationValue[]) => (data: Uint8Array) => BigInt(data.length),
  BlobGetUint8: (location: LocationValue[]) => (data: Uint8Array, index: bigint) => {
    const i = Number(index);
    if (i < 0 || i >= data.length) {
      throw new EastError(`Blob index ${index} out of bounds`, { location });
    } else {
      return BigInt(data[i]!);
    }
  },
  BlobDecodeUtf8: (location: LocationValue[]) => {
    const decoder = new TextDecoder('utf-8', { fatal: true });
    return (data: Uint8Array) => {
      try {
        return decoder.decode(data);
      } catch {
        throw new EastError("Blob is not valid UTF-8", { location });
      }
    };
  },
  BlobDecodeUtf16: (location: LocationValue[]) => {
    const decoder_be = new TextDecoder('utf-16be', { fatal: true });
    const decoder_le = new TextDecoder('utf-16le', { fatal: true });
    return (data: Uint8Array) => {
      try {
        if (data.length >= 2) {
          // Check for BOM
          if (data[0] === 0xFE && data[1] === 0xFF) {
            // Big-endian BOM
            return decoder_be.decode(data.subarray(2));
          } else if (data[0] === 0xFF && data[1] === 0xFE) {
            // Little-endian BOM
            return decoder_le.decode(data.subarray(2));
          }
        }
        // No BOM, default to little-endian (not unicode spec compliant, but more common in practice)
        return decoder_le.decode(data);
      } catch {
        throw new EastError("Blob is not valid UTF-16", { location });
      }
    };
  },
  BlobEncodeBeast: (_location: LocationValue[], _platformDef: PlatformFunction[], type: EastTypeValue) => {
    const encodeBeast = encodeBeastFor(type);
    return (value: any) => {
      return encodeBeast(value);
    }
  },
  BlobDecodeBeast: (location: LocationValue[], _platformDef: PlatformFunction[], type: EastTypeValue) => {
    const decodeBeast = decodeBeastFor(type);
    return (data: Uint8Array) => {
      try {
        return decodeBeast(data);
      } catch (e: unknown) {
        throw new EastError(`Failed to decode Beast data: ${(e as Error).message}`, { location });
      }
    }
  },
  BlobEncodeBeast2: (_location: LocationValue[], _platformDef: PlatformFunction[], type: EastTypeValue) => {
    const encodeBeast2 = encodeBeast2For(type);
    return (value: any) => {
      return encodeBeast2(value);
    }
  },
  BlobDecodeBeast2: (location: LocationValue[], platformDef: PlatformFunction[], type: EastTypeValue) => {
    const decodeBeast2 = decodeBeast2For(type, { platform: platformDef });
    return (data: Uint8Array) => {
      try {
        return decodeBeast2(data);
      } catch (e: unknown) {
        throw new EastError(`Failed to decode Beast2 data: ${(e as Error).message}`, { location });
      }
    }
  },
  BlobDecodeCsv: (location: LocationValue[], _platformDef: PlatformFunction[], structType: EastTypeValue, _configType: EastTypeValue) => {
    return (data: Uint8Array, config: any) => {
      try {
        const decoder = decodeCsvFor(structType, config);
        return decoder(data);
      } catch (e: unknown) {
        throw new EastError(`Failed to decode CSV data: ${(e as Error).message}`, { location });
      }
    }
  },
  ArrayEncodeCsv: (location: LocationValue[], _platformDef: PlatformFunction[], structType: EastTypeValue, _configType: EastTypeValue) => {
    return (data: any[], config: any) => {
      try {
        const encoder = encodeCsvFor(structType, config);
        return encoder(data);
      } catch (e: unknown) {
        throw new EastError(`Failed to encode CSV data: ${(e as Error).message}`, { location });
      }
    }
  },

  RefGet: (_location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (ref: ref<any>) => {
    return ref.value;
  },
  RefUpdate: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (ref: ref<any>, value: any) => {
    if (Object.isFrozen(ref)) {
      throw new EastError("Cannot modify frozen Ref", { location });
    }
    ref.value = value;
    return null;
  },
  RefMerge: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (ref: ref<any>, value: any, merger: (existing: any, value: any) => any) => {
    if (Object.isFrozen(ref)) {
      throw new EastError("Cannot modify frozen Ref", { location });
    }
    const new_value = call_function(location, merger, ref.value, value);
    ref.value = new_value;
    return null;
  },
  
  ArrayGenerate: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (size: bigint, f: (i: bigint) => any) => {
    const result: any[] = [];
    for (let i = 0n; i < size; i += 1n) {
      const v = call_function(location, f, i);
      result.push(v);
    }
    return result;
  },
  ArrayRange: (_location: LocationValue[]) => (start: bigint, end: bigint, step: bigint) => {
    const result: any[] = [];
    if (step === 0n) {
      return result; // empty array
    } else if (step > 0n) {
      for (let i = start; i < end; i += step) {
        result.push(i);
      }
    } else { // step < 0
      for (let i = start; i > end; i += step) {
        result.push(i);
      }
    }
    return result;
  },
  ArrayLinspace: (_location: LocationValue[]) => (start: number, end: number, size: bigint) => {
    const result: any[] = [];
    if (size <= 0n) {
      return result; // empty array
    } else if (size === 1n) {
      return [start];
    } else {
      const step = (end - start) / Number(size - 1n);
      for (let i = 0n; i < size; i += 1n) {
        result.push(start + Number(i) * step);
      }
    }
    return result;
  },
  ArraySize: (_location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[]) => BigInt(array.length),
  ArrayHas: (_location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[], key: bigint) => {
    const i = Number(key);
    return i >= 0 && i < array.length;
  },
  ArrayGet: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[], key: bigint) => {
    const i = Number(key);
    if (i < 0 || i >= array.length) {
      throw new EastError(`Array index ${key} out of bounds`, { location });
    } else {
      return array[i];
    }
  },
  ArrayGetOrDefault: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[], key: bigint, defaultFn: (key: bigint) => any) => {
    const i = Number(key);
    if (i < 0 || i >= array.length) {
      return call_function(location, defaultFn, key);
    } else {
      return array[i];
    }
  },
  ArrayTryGet: (_location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[], key: bigint) => {
    const i = Number(key);
    if (i < 0 || i >= array.length) {
      return variant("none", null);
    } else {
      return variant("some", array[i]);
    }
  },
  ArrayUpdate: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[], key: bigint, value: any) => {
    if (Object.isFrozen(array)) {
      throw new EastError("Cannot modify frozen Array", { location });
    }
    const i = Number(key);
    if (i < 0 || i >= array.length) {
      throw new EastError(`Array index ${key} out of bounds`, { location });
    } else {
      array[i] = value;
      return null;
    }
  },
  ArrayMerge: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[], key: bigint, value: any, merger: (existing: any, value: any, key: bigint) => any) => {
    if (Object.isFrozen(array)) {
      throw new EastError("Cannot modify frozen Array", { location });
    }
    const i = Number(key);
    if (i < 0 || i >= array.length) {
      throw new EastError(`Array index ${key} out of bounds`, { location });
    } else {
      const new_value = call_function(location, merger, array[i], value, key);
      array[i] = new_value;
      return null;
    }
  },
  ArrayPushLast: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[], value: any) => {
    if (Object.isFrozen(array)) {
      throw new EastError("Cannot modify frozen Array", { location });
    }
    if ((iterationLocks.get(array) || 0) > 0) {
      throw new EastError("Cannot modify Array during iteration", { location });
    }
    array.push(value);
    return null;
  },
  ArrayPopLast: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[]) => {
    if (Object.isFrozen(array)) {
      throw new EastError("Cannot modify frozen Array", { location });
    }
    if ((iterationLocks.get(array) || 0) > 0) {
      throw new EastError("Cannot modify Array during iteration", { location });
    }
    if (array.length === 0) {
      throw new EastError("Cannot pop from empty Array", { location });
    } else {
      return array.pop();
    }
  },
  ArrayPushFirst: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[], value: any) => {
    if (Object.isFrozen(array)) {
      throw new EastError("Cannot modify frozen Array", { location });
    }
    if ((iterationLocks.get(array) || 0) > 0) {
      throw new EastError("Cannot modify Array during iteration", { location });
    }
    array.unshift(value);
    return null;
  },
  ArrayPopFirst: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[]) => {
    if (Object.isFrozen(array)) {
      throw new EastError("Cannot modify frozen Array", { location });
    }
    if ((iterationLocks.get(array) || 0) > 0) {
      throw new EastError("Cannot modify Array during iteration", { location });
    }
    if (array.length === 0) {
      throw new EastError("Cannot pop from empty Array", { location });
    } else {
      return array.shift();
    }
  },
  ArrayAppend: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[], other: any[]) => {
    if (Object.isFrozen(array)) {
      throw new EastError("Cannot modify frozen Array", { location });
    }
    if ((iterationLocks.get(array) || 0) > 0) {
      throw new EastError("Cannot modify Array during iteration", { location });
    }
    array.push(...other);
    return null;
  },
  ArrayPrepend: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[], other: any[]) => {
    if (Object.isFrozen(array)) {
      throw new EastError("Cannot modify frozen Array", { location });
    }
    if ((iterationLocks.get(array) || 0) > 0) {
      throw new EastError("Cannot modify Array during iteration", { location });
    }
    array.unshift(...other);
    return null;
  },
  ArrayMergeAll: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue, _T2: EastTypeValue) => (array: any[], other: any[], merger: (v1: any, v2: any, key: bigint) => any) => {
    if (Object.isFrozen(array)) {
      throw new EastError("Cannot modify frozen Array", { location });
    }
    lockForIteration(array);
    lockForIteration(other);
    try {
      for (let i = 0; i < other.length; i++) {
        const key = BigInt(i);
        if (i < array.length) {
          const new_value = call_function(location, merger, array[i], other[i], key);
          array[i] = new_value;
        } else {
          throw new EastError(`Array index ${key} out of bounds`, { location });
        }
      }
    } finally {
      unlockForIteration(other);
      unlockForIteration(array);
    }
    return null;
  },
  ArrayClear: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[]) => {
    if (Object.isFrozen(array)) {
      throw new EastError("Cannot modify frozen Array", { location });
    }
    if ((iterationLocks.get(array) || 0) > 0) {
      throw new EastError("Cannot modify Array during iteration", { location });
    }
    array.length = 0;
    return null;
  },
  ArraySortInPlace: (location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue, T2: EastTypeValue) => (array: any[], by: (a: any) => any) => {
    if (Object.isFrozen(array)) {
      throw new EastError("Cannot modify frozen Array", { location });
    }
    if ((iterationLocks.get(array) || 0) > 0) {
      throw new EastError("Cannot modify Array during iteration", { location });
    }
    lockForIteration(array);
    try {
      const cmp = compareFor(T2);
      array.sort((a, b) => {
        const projectedA = call_function(location, by, a);
        const projectedB = call_function(location, by, b);
        return cmp(projectedA, projectedB);
      });
    } finally {
      unlockForIteration(array);
    }
    return null;
  },
  ArrayReverseInPlace: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[]) => {
    if (Object.isFrozen(array)) {
      throw new EastError("Cannot modify frozen Array", { location });
    }
    if ((iterationLocks.get(array) || 0) > 0) {
      throw new EastError("Cannot modify Array during iteration", { location });
    }
    array.reverse();
    return null;
  },
  ArraySort: (location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue, T2: EastTypeValue) => (array: any[], by: (a: any) => any) => {
    const cmp = compareFor(T2);
    const newArray = [...array];
    newArray.sort((a, b) => {
      const projectedA = call_function(location, by, a);
      const projectedB = call_function(location, by, b);
      return cmp(projectedA, projectedB);
    });
    return newArray;
  },
  ArrayReverse: (_location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[]) => {
    const newArray = [...array];
    newArray.reverse();
    return newArray;
  },
  ArrayIsSorted: (location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue, T2: EastTypeValue) => {
    const cmp = compareFor(T2);
    return (array: any[], by: (a: any) => any) => {
      if (array.length < 2) return true;

      lockForIteration(array);
      try {
        let projectedPrev = call_function(location, by, array[0]!);

        for (let i = 1; i < array.length; i++) {
          const projectedCurr = call_function(location, by, array[i]);

          if (cmp(projectedPrev, projectedCurr) > 0) {
            return false;
          }

          projectedPrev = projectedCurr;
        }
      } finally {
        unlockForIteration(array);
      }
      return true;
    };
  },
  ArrayFindSortedFirst: (location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue, T2: EastTypeValue) => {
    const cmp = compareFor(T2);
    return (array: any[], key: any, by: (a: any) => any) => {
      let low = 0;
      let high = array.length;

      lockForIteration(array);
      try {
        while (low < high) {
          const mid = Math.floor((low + high) / 2);
          const projectedMid = call_function(location, by, array[mid]!);

          if (cmp(projectedMid, key) < 0) {
            low = mid + 1;
          } else {
            high = mid;
          }
        }
      } finally {
        unlockForIteration(array);
      }

      return BigInt(low);
    };
  },
  ArrayFindSortedLast: (location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue, T2: EastTypeValue) => {
    const cmp = compareFor(T2);
    return (array: any[], key: any, by: (a: any) => any) => {
      let low = 0;
      let high = array.length;

      lockForIteration(array);
      try {
        while (low < high) {
          const mid = Math.floor((low + high) / 2);
          const projectedMid = call_function(location, by, array[mid]!);

          if (cmp(projectedMid, key) <= 0) {
            low = mid + 1;
          } else {
            high = mid;
          }
        }
      } finally {
        unlockForIteration(array);
      }

      return BigInt(low);
    };
  },
  ArrayFindSortedRange: (location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue, T2: EastTypeValue) => {
    const cmp = compareFor(T2);
    return (array: any[], key: any, by: (a: any) => any) => {
      let lo = -1;
      let hi = array.length;
      
      lockForIteration(array);
      try {
        // Main search loop - find any equal element or determine the range doesn't exist
        while (lo < hi - 1) {
          const mid = Math.floor((lo + hi) / 2);
          const projectedMid = call_function(location, by, array[mid]!);

          const cmpResult = cmp(projectedMid, key);
          if (cmpResult < 0) {
            lo = mid;
          } else if (cmpResult > 0) {
            hi = mid;
          } else {
            // Found an equal element! Now find the first and last positions
            // within the constrained range

            // Find first position in range [max(lo, -1), mid]
            let firstLo = Math.max(lo, -1);
            let firstHi = mid + 1;

            while (firstLo < firstHi - 1) {
              const firstMid = Math.floor((firstLo + firstHi) / 2);
              const projectedFirst = call_function(location, by, array[firstMid]!);

              if (cmp(projectedFirst, key) < 0) {
                firstLo = firstMid;
              } else {
                firstHi = firstMid;
              }
            }

            // Find last position in range [mid, min(hi, array.length)]
            let lastLo = mid - 1;
            let lastHi = Math.min(hi, array.length);

            while (lastLo < lastHi - 1) {
              const lastMid = Math.floor((lastLo + lastHi) / 2);
              const projectedLast = call_function(location, by, array[lastMid]!);

              if (cmp(projectedLast, key) <= 0) {
                lastLo = lastMid;
              } else {
                lastHi = lastMid;
              }
            }

            return { start: BigInt(firstLo + 1), end: BigInt(lastLo + 1) };
          }
        }
      } finally {
        unlockForIteration(array);
      }

      // No equal element found - return empty range
      return { start: BigInt(lo + 1), end: BigInt(lo + 1) };
    };
  },
  ArrayFindFirst: (location: LocationValue[], _platformDef: PlatformFunction[], T: EastTypeValue, T2: EastTypeValue) => {
    const cmp = compareFor(T2);
    return (array: any[], value: any, by: (a: any) => any) => {
      lockForIteration(array);
      try {
        for (let i = 0; i < array.length; i++) {
          const projected = call_function(location, by, array[i]);
          if (cmp(projected, value) === 0) {
            return variant("some", BigInt(i));
          }
        }
        return variant("none", null);
      } finally {
        unlockForIteration(array);
      }
    };
  },
  ArrayConcat: (_location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (a1: any[], a2: any[]) => {
    return [...a1, ...a2];
  },
  ArraySlice: (_location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[], start: bigint, end: bigint) => {
    const startNum = Number(start);
    const endNum = Number(end);
    return array.slice(startNum, endNum);
  },
  ArrayGetKeys: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[], keys: bigint[], onMissing: (key: bigint) => any) => {
    return keys.map(k => {
      const i = Number(k);
      if (i < 0 || i >= array.length) {
        return call_function(location, onMissing, k);
      } else {
        return array[i];
      }
    });
  },
  ArrayForEach: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue, _T2: EastTypeValue) => (array: any[], f: (x: any, i: bigint) => any) => {
    lockForIteration(array);
    try {
      array.forEach((x, i) => {
        return call_function(location, f, x, BigInt(i));
      });
      return null;
    } finally {
      unlockForIteration(array);
    }
  },
  ArrayCopy: (_location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[]) => {
    return [...array];
  },
  ArrayMap: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue, _T2: EastTypeValue) => (array: any[], f: (x: any, i: bigint) => any) => {
    lockForIteration(array);
    try {
      return array.map((x, i) => {
        return call_function(location, f, x, BigInt(i));
      });
    } finally {
      unlockForIteration(array);
    }
  },
  ArrayFilter: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue, _T2: EastTypeValue) => (array: any[], f: (x: any, i: bigint) => any) => {
    lockForIteration(array);
    try {
      return array.filter((x, i) => {
        return call_function(location, f, x, BigInt(i));
      });
    } finally {
      unlockForIteration(array);
    }
  },
  ArrayFilterMap: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue, _T2: EastTypeValue) => (array: any[], f: (x: any, i: bigint) => any) => {
    lockForIteration(array);
    try {
      const result: any[] = [];
      for (let i = 0; i < array.length; i++) {
        const v: option<any> = call_function(location, f, array[i], BigInt(i));
        if (v.type === "some") {
          result.push(v.value);
        }
      }
      return result;
    } finally {
      unlockForIteration(array);
    }
  },
  ArrayFirstMap: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue, _T2: EastTypeValue) => (array: any[], f: (x: any, i: bigint) => any) => {
    lockForIteration(array);
    try {
      for (let i = 0; i < array.length; i++) {
        const v: option<any> = call_function(location, f, array[i], BigInt(i));
        if (v.type === "some") {
          return v;
        }
      }
      return variant("none", null);
    } finally {
      unlockForIteration(array);
    }
  },
  ArrayFold: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue, _T2: EastTypeValue) => (array: any[], init: any, f: (acc: any, x: any, i: bigint) => any) => {
    lockForIteration(array);
    try {
      return array.reduce((acc, x, i) => {
        return call_function(location, f, acc, x, BigInt(i));
      }, init);
    } finally {
      unlockForIteration(array);
    }
  },
  ArrayMapReduce: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue, _T2: EastTypeValue) => (array: any[], mapFn: (x: any, i: bigint) => any, reduceFn: (x: any, y:any) => any) => {
    if (array.length === 0) {
      throw new EastError("Cannot reduce empty array with no initial value", { location });
    }
    lockForIteration(array);
    try {
      let acc = call_function(location, mapFn, array[0], 0n);
      for (let i = 1; i < array.length; i++) {
        const mapped = call_function(location, mapFn, array[i], BigInt(i));
        acc = call_function(location, reduceFn, acc, mapped);
      }
      return acc;
    } finally {
      unlockForIteration(array);
    }
  },
  ArrayStringJoin: (_location: LocationValue[], _platformDef: PlatformFunction[]) => (x: string[], y:string) => x.join(y),
  ArrayToSet: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue, T2: EastTypeValue) => {
    const compare = compareFor(T2);
    return (array: any[], f: (x: any, i: bigint) => any) => {
      lockForIteration(array);
      try {
        const result = new SortedSet([], compare);
        for (let i = 0; i < array.length; i++) {
          const v = call_function(location, f, array[i], BigInt(i));
          result.add(v);
        }
        return result;
      } finally {
        unlockForIteration(array);
      }
    }
  },
  ArrayToDict: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue, K2: EastTypeValue, _T2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (array: any[], keyFn: (v: any, i: bigint) => any, valueFn: (v: any, i: bigint) => any, onConflict: (v1: any, v2: any, k: any) => null) => {
      const result = new SortedMap([], compare);
      lockForIteration(array);
      try {
        for (let i = 0; i < array.length; i++) {
          const v = array[i];
          const k = call_function(location, keyFn, v, BigInt(i));
          let val = call_function(location, valueFn, v, BigInt(i));
          const existing = result.get(k);
          if (existing === undefined) {
            result.set(k, val);
          } else {
            val = call_function(location, onConflict, existing, val, k);
            result.set(k, val);
          }
        }
        return result;
      } finally {
        unlockForIteration(array);
      }
    }
  },
  ArrayFlattenToArray: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue) => (array: any[], fn: (value: any) => any[]) => {
    return array.flatMap(v => {
      return call_function(location, fn, v);
    });
  },
  ArrayFlattenToSet: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue, K2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (array: any[], fn: (value: any) => any[]) => {
      const result = new SortedSet([], compare);
      lockForIteration(array);
      try {
        for (const v of array) {
          const subset = call_function(location, fn, v);
          for (const k of subset) {
            result.add(k);
          }
        }
        return result;
      } finally {
        unlockForIteration(array);
      }
    }
  },
  ArrayFlattenToDict: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue, K2: EastTypeValue, _T2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (array: any[], fn: (value: any) => any[], onConflict: (v1: any, v2: any, k: any) => null) => {
      const result = new SortedMap([], compare);
      lockForIteration(array);
      try {
        for (const v of array) {
          const subdict = call_function(location, fn, v);
          for (const [k, val] of subdict.entries()) {
            const existing = result.get(k);
            if (existing === undefined) {
              result.set(k, val);
            } else {
              const new_val = call_function(location, onConflict, existing, val, k);
              result.set(k, new_val);
            }
          }
        }
        return result;
      } finally {
        unlockForIteration(array);
      }
    }
  },
  ArrayGroupFold: (location: LocationValue[], _platformDef: PlatformFunction[], _T: EastTypeValue, K2: EastTypeValue, _V2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (array: any[], keyFn: (v: any, i: bigint) => any, init: (k: any) => any, folder: (acc: any, v: any, i: bigint) => any) => {
      const result = new SortedMap([], compare);
      lockForIteration(array);
      try {
        for (let i = 0; i < array.length; i++) {
          const v = array[i];
          const k = call_function(location, keyFn, v, BigInt(i));
          let existing = result.get(k);
          if (existing === undefined) {
            existing = call_function(location, init, k);
          }
          const new_val = call_function(location, folder, existing, v, BigInt(i));
          result.set(k, new_val);
        }
        return result;
      } finally {
        unlockForIteration(array);
      }
    }
  },

  SetGenerate: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue) => {
    const keyComparer = compareFor(K);
    return (size: bigint, keyFn: (i: bigint) => any, onConflict: (key: any) => null) => {
      const result = new SortedSet([], keyComparer);
      for (let i = 0n; i < size; i += 1n) {
        const k = call_function(location, keyFn, i);
        if (result.has(k)) {
          call_function(location, onConflict, k);
        } else {
          result.add(k);
        }
      }
      return result;
    }
  },
  SetSize: (_location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue) => (s: Set<any>) => BigInt(s.size),
  SetHas: (_location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue) => (s: Set<any>, key: any) => s.has(key),
  SetInsert: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue) => {
    const print = printFor(K);
    return (s: Set<any>, key: any) => {
      if (Object.isFrozen(s)) {
        throw new EastError("Cannot modify frozen Set", { location });
      }
      if ((iterationLocks.get(s) || 0) > 0) {
        throw new EastError("Cannot modify Set during iteration", { location });
      }
      const size_before = s.size;
      s.add(key);
      if (s.size === size_before) {
        throw new EastError(`Set already contains key ${print(key)}`, { location });
      }
      return null;
    }
  },
  SetTryInsert: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue) => (s: Set<any>, key: any) => {
    if (Object.isFrozen(s)) {
      throw new EastError("Cannot modify frozen Set", { location });
    }
    if ((iterationLocks.get(s) || 0) > 0) {
      throw new EastError("Cannot modify Set during iteration", { location });
    }
    const size_before = s.size;
    s.add(key);
    return s.size > size_before;
  },
  SetDelete: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue) => {
    const print = printFor(K);
    return (s: Set<any>, key: any) => {
      if (Object.isFrozen(s)) {
        throw new EastError("Cannot modify frozen Set", { location });
      }
      if ((iterationLocks.get(s) || 0) > 0) {
        throw new EastError("Cannot modify Set during iteration", { location });
      }
      if (!s.delete(key)) {
        throw new EastError(`Set does not contain key ${print(key)}`, { location });
      }
      return null;
    }
  },
  SetTryDelete: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue) => (s: Set<any>, key: any) => {
    if (Object.isFrozen(s)) {
      throw new EastError("Cannot modify frozen Set", { location });
    }
    if ((iterationLocks.get(s) || 0) > 0) {
      throw new EastError("Cannot modify Set during iteration", { location });
    }
    return s.delete(key);
  },
  SetClear: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue) => (s: Set<any>) => {
    if (Object.isFrozen(s)) {
      throw new EastError("Cannot modify frozen Set", { location });
    }
    if ((iterationLocks.get(s) || 0) > 0) {
      throw new EastError("Cannot modify Set during iteration", { location });
    }
    s.clear();
    return null
  },
  SetUnionInPlace: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue) => (s1: Set<any>, s2: Set<any>) => {
    if (Object.isFrozen(s1)) {
      throw new EastError("Cannot modify frozen Set", { location });
    }
    if ((iterationLocks.get(s1) || 0) > 0) {
      throw new EastError("Cannot modify Set during iteration", { location });
    }
    s2.forEach(v => s1.add(v));
    return null;
  },
  SetUnion: (_location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue) => (s1: Set<any>, s2: Set<any>) => s1.union(s2),
  SetIntersect: (_location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue) => (s1: Set<any>, s2: Set<any>) => s1.intersection(s2),
  SetDiff: (_location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue) => (s1: Set<any>, s2: Set<any>) => s1.difference(s2),
  SetSymDiff: (_location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue) => (s1: Set<any>, s2: Set<any>) => s1.symmetricDifference(s2),
  SetIsSubset: (_location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue) => (s1: Set<any>, s2: Set<any>) => s1.isSubsetOf(s2),
  SetIsDisjoint: (_location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue) => (s1: Set<any>, s2: Set<any>) => s1.isDisjointFrom(s2),
  SetCopy: (_location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue) => {
    const compare = compareFor(K);
    return (s: SortedSet<any>) => {
      return new SortedSet([...s], compare);
    }
  },
  SetForEach: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _T2: EastTypeValue) => (s: Set<any>, f: (x: any) => any) => {
    lockForIteration(s);
    try {
      s.forEach(x => {
        call_function(location, f, x);
      });
      return null;
    } finally {
      unlockForIteration(s);
    }
  },
  SetFilter: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue) => {
    const compare = compareFor(K);
    return (s: SortedSet<any>, f: (x: any) => any) => {
      const result = new SortedSet([], compare);
      lockForIteration(s);
      try {
        s.forEach(x => {
          const keep = call_function(location, f, x);
          if (keep) {
            result.add(x);
          }
        });
        return result;
      } finally {
        unlockForIteration(s);
      }
    }
  },
  SetFilterMap: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V2: EastTypeValue) => {
    const compare = compareFor(K);
    return (s: SortedSet<any>, f: (k: any) => option<any>) => {
      const result = new SortedMap([], compare);
      lockForIteration(s);
      try {
        s.forEach(k => {
          const v2: option<any> = call_function(location, f, k);
          if (v2.type === "some") {
            result.set(k, v2.value);
          }
        });
        return result;
      } finally {
        unlockForIteration(s);
      }
    }
  },
  SetFirstMap: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _T2: EastTypeValue) => (s: SortedSet<any>, f: (k: any) => any) => {
    lockForIteration(s);
    try {
      for (const k of s) {
        const v: option<any> = call_function(location, f, k);
        if (v.type === "some") {
          return v;
        }
      }
      return variant("none", null);
    } finally {
      unlockForIteration(s);
    }
  },
  SetMapReduce: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _T2: EastTypeValue) => (s: SortedSet<any>, mapFn: (k: any) => any, reduceFn: (x: any, y: any) => any) => {
    if (s.size === 0) {
      throw new EastError("Cannot reduce empty set with no initial value", { location });
    }
    lockForIteration(s);
    try {
      const iterator = s[Symbol.iterator]();
      const first = iterator.next().value;
      let acc = call_function(location, mapFn, first);
      for (const k of iterator) {
        const mapped = call_function(location, mapFn, k);
        acc = call_function(location, reduceFn, acc, mapped);
      }
      return acc;
    } finally {
      unlockForIteration(s);
    }
  },
  SetMap: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _T2: EastTypeValue) => {
    const compare = compareFor(K);
    return (s: SortedSet<any>, f: (x: any) => any) => {
      const result = new SortedMap([], compare);
      lockForIteration(s);
      try {
        s.forEach(x => {
          const v = call_function(location, f, x);
          result.set(x, v);
        });
        return result;
      } finally {
        unlockForIteration(s);
      }
    }
  },
  SetReduce: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _T2: EastTypeValue) => (s: Set<any>, f: (acc: any, x: any) => any, init: any) => {
    let acc = init;
    lockForIteration(s);
    try {
      for (const x of s) {
        acc = call_function(location, f, acc, x);
      }
      return acc;
    } finally {
      unlockForIteration(s);
    }
  },
  SetToArray: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _T2: EastTypeValue) => (s: Set<any>, valueFn: (key: any) => any) => {
    const ret = [];
    lockForIteration(s);
    try {
      for (const k of s) {
        const v = call_function(location, valueFn, k);
        ret.push(v);
      }
      return ret;
    } finally {
      unlockForIteration(s);
    }
  },
  SetToSet: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, K2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (s: SortedSet<any>, f: (x: any) => any) => {
      const result = new SortedSet([], compare);
      lockForIteration(s);
      try {
        for (const x of s) {
          const v = call_function(location, f, x);
          result.add(v);
        };
        return result;
      } finally {
        unlockForIteration(s);
      }
    }
  },
  SetToDict: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, K2: EastTypeValue, _V2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (s: Set<any>, keyFn: (key: any) => any, valueFn: (key: any) => any, onConflict: (v1: any, v2: any, k: any) => null) => {
      const result = new SortedMap([], compare);
      lockForIteration(s);
      try {
        for (const k of s) {
          const k2 = call_function(location, keyFn, k);
          let v2 = call_function(location, valueFn, k);
          const existing = result.get(k2);
          if (existing !== undefined) {
            v2 = call_function(location, onConflict, existing, v2, k2);
            result.set(k2, v2);
          } else {
            result.set(k2, v2);
          }
        }
        return result;
      } finally {
        unlockForIteration(s);
      }
    }
  },
  SetFlattenToArray: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _T2: EastTypeValue) => (s: Set<any>, fn: (value: any) => any[]) => {
    const ret = [];
    lockForIteration(s);
    try {
      for (const k of s) {
        const subarray = call_function(location, fn, k);
        ret.push(...subarray);
      }
      return ret;
    } finally {
      unlockForIteration(s);
    }
  },
  SetFlattenToSet: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, K2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (s: Set<any>, fn: (value: any) => any[]) => {
      const result = new SortedSet([], compare);
      lockForIteration(s);
      try {
        for (const k of s) {
          const subset = call_function(location, fn, k);
          for (const k2 of subset) {
            result.add(k2);
          }
        }
        return result;
      } finally {
        unlockForIteration(s);
      }
    }
  },
  SetFlattenToDict: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, K2: EastTypeValue, _V2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (s: Set<any>, fn: (value: any) => any[], onConflict: (v1: any, v2: any, k: any) => null) => {
      const result = new SortedMap([], compare);
      lockForIteration(s);
      try {
        for (const k of s) {
          const subdict = call_function(location, fn, k);
          for (const [k2, v2] of subdict.entries()) {
            const existing = result.get(k2);
            if (existing === undefined) {
              result.set(k2, v2);
            } else {
              const new_v2 = call_function(location, onConflict, existing, v2, k2);
              result.set(k2, new_v2);
            }
          }
        }
        return result;
      } finally {
        unlockForIteration(s);
      }
    }
  },
  SetGroupFold: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, K2: EastTypeValue, _T2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (s: Set<any>, keyFn: (k: any) => any, init: (k2: any) => any, folder: (acc: any, k: any) => any) => {
      const result = new SortedMap([], compare);
      lockForIteration(s);
      try {
        for (const k of s) {
          const k2 = call_function(location, keyFn, k);
          let existing = result.get(k2);
          if (existing === undefined) {
            existing = call_function(location, init, k2);
          }
          const new_val = call_function(location, folder, existing, k);
          result.set(k2, new_val);
        }
        return result;
      } finally {
        unlockForIteration(s);
      }
    }
  },

  DictGenerate: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue) => {
    const keyComparer = compareFor(K);
    return (size: bigint, keyFn: (i: bigint) => any, valueFn: (i: bigint) => any, onConflict: (v1: any, v2: any, key: any) => any) => {
      const result = new SortedMap([], keyComparer);
      for (let i = 0n; i < size; i += 1n) {
        const k = call_function(location, keyFn, i);
        const v = call_function(location, valueFn, i);
        const existing = result.get(k);
        if (existing !== undefined) {
          const v2 = call_function(location, onConflict, existing, v, k);
          result.set(k, v2);
        } else {
          result.set(k, v);
        }
      }
      return result;
    }
  },
  DictSize: (_location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue) => (d: Map<any, any>) => BigInt(d.size),
  DictHas: (_location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue) => (d: Map<any, any>, key: any) => d.has(key),
  DictGet: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue) => {
    const print = printFor(K);
    return (d: Map<any, any>, key: any) => {
      const result = d.get(key);
      if (result === undefined) {
        throw new EastError(`Dict does not contain key ${print(key)}`, { location });
      } else {
        return result;
      }
    }
  },
  DictGetOrDefault: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue) => (d: Map<any, any>, key: any, onMissingFn: (key: any) => any) => {
    const result = d.get(key);
    if (result === undefined) {
      return call_function(location, onMissingFn, key);
    } else {
      return result;
    }
  },
  DictTryGet: (_location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue) => (d: Map<any, any>, key: any) => {
    const result = d.get(key);
    if (result === undefined) {
      return variant("none", null);
    } else {
      return variant("some", result);
    }
  },
  DictInsert: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue) => {
    const print = printFor(K);
    return (d: Map<any, any>, key: any, value: any) => {
      if (Object.isFrozen(d)) {
        throw new EastError("Cannot modify frozen Dict", { location });
      }
      if ((iterationLocks.get(d) || 0) > 0) {
        throw new EastError("Cannot modify Dict during iteration", { location });
      }
      const existing = d.get(key);
      if (existing !== undefined) {
        throw new EastError(`Dict already contains key ${print(key)}`, { location });
      } else {
        d.set(key, value);
      }
      return null;
    }
  },
  DictGetOrInsert: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue) => (d: Map<any, any>, key: any, onMissing: (key: any) => any) => {
    if (Object.isFrozen(d)) {
      throw new EastError("Cannot modify frozen Dict", { location });
    }
    if ((iterationLocks.get(d) || 0) > 0) {
      throw new EastError("Cannot modify Dict during iteration", { location });
    }
    const existing = d.get(key);
    if (existing === undefined) {
      const newValue = call_function(location, onMissing, key);
      d.set(key, newValue);
      return newValue;
    } else {
      return existing;
    }
  },
  DictInsertOrUpdate: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue) => (d: Map<any, any>, key: any, value: any, onConflictFn: (existing: any, newValue: any, key: any) => any) => {
    if (Object.isFrozen(d)) {
      throw new EastError("Cannot modify frozen Dict", { location });
    }
    if ((iterationLocks.get(d) || 0) > 0) {
      throw new EastError("Cannot modify Dict during iteration", { location });
    }
    const existing = d.get(key);
    if (existing !== undefined) {
      const result = call_function(location, onConflictFn, existing, value, key);
      d.set(key, result);
    } else {
      d.set(key, value);
    }
    return null;
  },
  DictUpdate: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue) => {
    const print = printFor(K);
    return (d: Map<any, any>, key: any, value: any) => {
      if (Object.isFrozen(d)) {
        throw new EastError("Cannot modify frozen Dict", { location });
      }
      if (d.has(key)) {
        d.set(key, value);
        return null;
      } else {
        throw new EastError(`Dict does not contain key ${print(key)}`, { location });
      }
    }
  },
  DictSwap: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue) => {
    const print = printFor(K);
    return (d: Map<any, any>, key: any, value: any) => {
      if (Object.isFrozen(d)) {
        throw new EastError("Cannot modify frozen Dict", { location });
      }
      let existing = d.get(key);
      if (existing === undefined) {
        throw new EastError(`Dict does not contain key ${print(key)}`, { location });
      }
      d.set(key, value);
      return existing;
    };
  },
  DictMerge: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue) => (d: Map<any, any>, key: any, value: any, mergeFn: (existing: any, value: any, key: any) => any, initialFn: (key: any) => any) => {
    if (Object.isFrozen(d)) {
      throw new EastError("Cannot modify frozen Dict", { location });
    }
    if ((iterationLocks.get(d) || 0) > 0) {
      throw new EastError("Cannot modify Dict during iteration", { location });
    }
    let existing = d.get(key);
    if (existing === undefined) {
      existing = call_function(location, initialFn, key);
    }
    const new_value = call_function(location, mergeFn, existing, value, key);
    d.set(key, new_value);
    return null;
  },
  DictDelete: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue) => {
    const print = printFor(K);
    return (d: Map<any, any>, key: any) => {
      if (Object.isFrozen(d)) {
        throw new EastError("Cannot modify frozen Dict", { location });
      }
      if ((iterationLocks.get(d) || 0) > 0) {
        throw new EastError("Cannot modify Dict during iteration", { location });
      }
      const existed = d.delete(key);
      if (!existed) {
        throw new EastError(`Dict does not contain key ${print(key)}`, { location });
      }
      return null;
    }
  },
  DictTryDelete: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue) => (d: Map<any, any>, key: any) => {
    if (Object.isFrozen(d)) {
      throw new EastError("Cannot modify frozen Dict", { location });
    }
    if ((iterationLocks.get(d) || 0) > 0) {
      throw new EastError("Cannot modify Dict during iteration", { location });
    }
    return d.delete(key);
  },
  DictPop: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue) => {
    const print = printFor(K);
    return (d: Map<any, any>, key: any) => {
      if (Object.isFrozen(d)) {
        throw new EastError("Cannot modify frozen Dict", { location });
      }
      if ((iterationLocks.get(d) || 0) > 0) {
        throw new EastError("Cannot modify Dict during iteration", { location });
      }
      const existing = d.get(key);
      if (existing === undefined) {
        throw new EastError(`Dict does not contain key ${print(key)}`, { location });
      } else {
        d.delete(key);
        return existing;
      }
    };
  },
  DictClear: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue) => (d: Map<any, any>) => {
    if (Object.isFrozen(d)) {
      throw new EastError("Cannot modify frozen Dict", { location });
    }
    if ((iterationLocks.get(d) || 0) > 0) {
      throw new EastError("Cannot modify Dict during iteration", { location });
    }
    d.clear();
    return null;
  },
  DictUnionInPlace: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue) => (d1: Map<any, any>, d2: Map<any, any>, onConflict: (v1: any, v2: any, key: any) => any) => {
    if (Object.isFrozen(d1)) {
      throw new EastError("Cannot modify frozen Dict", { location });
    }
    if ((iterationLocks.get(d1) || 0) > 0) {
      throw new EastError("Cannot modify Dict during iteration", { location });
    }
    d2.forEach((v2, k) => {
      const v1 = d1.get(k);
      if (v1 === undefined) {
        d1.set(k, v2);
      } else {
        const new_value = call_function(location, onConflict, v1, v2, k);
        d1.set(k, new_value);
      }
    });
    return null;
  },
  DictMergeAll: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue) => (d1: SortedMap<any, any>, d2: SortedMap<any, any>, mergeFn: (v1: any, v2: any, key: any) => any, initialFn: (key: any) => any) => {
    if (Object.isFrozen(d1)) {
      throw new EastError("Cannot modify frozen Dict", { location });
    }
    if ((iterationLocks.get(d1) || 0) > 0) {
      throw new EastError("Cannot modify Dict during iteration", { location });
    }
    d2.forEach((v2, k) => {
      let v1 = d1.get(k);
      if (v1 === undefined) {
        v1 = call_function(location, initialFn, k);
      }
      const new_value = call_function(location, mergeFn, v1, v2, k);
      d1.set(k, new_value);
    });
    return null;
  },
  DictKeys: (_location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue) => {
    const compare = compareFor(K);
    return (d: Map<any, any>) => {
      return new SortedSet([...d.keys()], compare);
    }
  },
  DictGetKeys: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue) => {
    const compare = compareFor(K);
    return (d: SortedMap<any, any>, keys: SortedSet<any>, onMissing: (key: any) => any) => {
      const result = new SortedMap([], compare);
      for (const k of keys) {
        const v = d.get(k);
        if (v !== undefined) {
          result.set(k, v);
        } else {
          const new_v = call_function(location, onMissing, k);
          result.set(k, new_v);
        }
      }
      return result;
    }
  },
  DictForEach: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue, _T2) => (d: Map<any, any>, f: (k: any, v: any) => any) => {
    lockForIteration(d);
    try {
      d.forEach((v, k) => {
        call_function(location, f, v, k);
      });
      return null;
    } finally {
      unlockForIteration(d);
    }
  },
  DictCopy: (_location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue) => {
    const compare = compareFor(K);
    return (d: SortedMap<any, any>) => {
      return new SortedMap([...d], compare);
    }
  },
  DictMap: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue, _V2: EastTypeValue) => {
    const compare = compareFor(K);
    return (d: SortedMap<any, any>, f: (v: any, k: any) => any) => {
      const result = new SortedMap([], compare);
      lockForIteration(d);
      try {
        for (const [k, v] of d) {
          const v2 = call_function(location, f, v, k);
          result.set(k, v2);
        }
        return result;
      } finally {
        unlockForIteration(d);
      }
    }
  },
  DictFilter: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue) => {
    const compare = compareFor(K);
    return (d: SortedMap<any, any>, f: (v: any, k: any) => any) => {
      const result = new SortedMap([], compare);
      lockForIteration(d);
      try {
        for (const [k, v] of d) {
          const keep = call_function(location, f, v, k);
          if (keep) {
            result.set(k, v);
          }
        }
        return result;
      } finally {
        unlockForIteration(d);
      }
    }
  },
  DictFilterMap: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue, _V2: EastTypeValue) => {
    const compare = compareFor(K);
    return (d: SortedMap<any, any>, f: (v: any, k: any) => option<any>) => {
      const result = new SortedMap([], compare);
      lockForIteration(d);
      try {
        for (const [k, v] of d) {
          const v2: option<any> = call_function(location, f, v, k);
          if (v2.type === "some") {
            result.set(k, v2.value);
          }
        }
        return result;
      } finally {
        unlockForIteration(d);
      }
    }
  },
  DictFirstMap: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue, _T2: EastTypeValue) => (d: Map<any, any>, f: (v: any, k: any) => option<any>) => {
    lockForIteration(d);
    try {
      for (const [k, v] of d) {
        const result: option<any> = call_function(location, f, v, k);
        if (result.type === "some") {
          return result;
        }
      }
      return variant("none", null);
    } finally {
      unlockForIteration(d);
    }
  },
  DictMapReduce: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue, _T2: EastTypeValue) => (d: Map<any, any>, mapFn: (v: any, k: any) => any, reduceFn: (x: any, y: any) => any) => {
    if (d.size === 0) {
      throw new EastError("Cannot reduce empty dictionary with no initial value", { location });
    }
    lockForIteration(d);
    try {
      const iterator = d[Symbol.iterator]();
      const first = iterator.next().value!;
      let acc = call_function(location, mapFn, first[1], first[0]);
      for (const [k, v] of iterator) {
        const mapped = call_function(location, mapFn, v, k);
        acc = call_function(location, reduceFn, acc, mapped);
      }
      return acc;
    } finally {
      unlockForIteration(d);
    }
  },
  DictReduce: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue, _T2: EastTypeValue) => (d: Map<any, any>, f: (acc: any, v: any, k: any) => any, init: any) => {
    let acc = init;
    lockForIteration(d);
    try {
      for (const [k, v] of d) {
        acc = call_function(location, f, acc, v, k);
      }
      return acc;
    } finally {
      unlockForIteration(d);
    }
  },
  DictToArray: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue, _T2: EastTypeValue) => (d: Map<any, any>, valueFn: (v: any, k: any) => any) => {
    const ret = [];
    lockForIteration(d);
    try {
      for (const [k, v] of d) {
        const v2 = call_function(location, valueFn, v, k);
        ret.push(v2);
      }
      return ret;
    } finally {
      unlockForIteration(d);
    }
  },
  DictToSet: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue, K2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (d: SortedMap<any, any>, fn: (v: any, k: any) => any) => {
      const result = new SortedSet([], compare);
      lockForIteration(d);
      try {
        for (const [k, v] of d) {
          const k2 = call_function(location, fn, v, k);
          result.add(k2);
        }
        return result;
      } finally {
        unlockForIteration(d);
      }
    }
  },
  DictToDict: (location: LocationValue[], _platformDef: PlatformFunction[], K: EastTypeValue, _V: EastTypeValue, K2: EastTypeValue, _V2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (d: Map<any, any>, keyFn: (v: any, k: any) => any, valueFn: (v: any, k: any) => any, onConflict: (v1: any, v2: any, k: any) => any) => {
      const result = new SortedMap([], compare);
      lockForIteration(d);
      try {
        for (const [k, v] of d) {
          const k2 = call_function(location, keyFn, v, k);
          const v2 = call_function(location, valueFn, v, k);
          const existing = result.get(k2);
          if (existing !== undefined) {
            const v3 = call_function(location, onConflict, existing, v2, k2);
            result.set(k2, v3);
          } else {
            result.set(k2, v2);
          }
        }
        return result;
      } finally {
        unlockForIteration(d);
      }
    }
  },
  DictFlattenToArray: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue, _T2: EastTypeValue) => (d: Map<any, any>, fn: (key: any, value: any) => any[]) => {
    const ret = [];
    lockForIteration(d);
    try {
      for (const [k, v] of d.entries()) {
        const subarray = call_function(location, fn, v, k);
        for (const item of subarray) {
          ret.push(item);
        }
      }
      return ret;
    } finally {
      unlockForIteration(d);
    }
  },
  DictFlattenToSet: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue, K2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (d: Map<any, any>, fn: (key: any, value: any) => any[]) => {
      const result = new SortedSet([], compare);
      lockForIteration(d);
      try {
        for (const [k, v] of d.entries()) {
          const subset = call_function(location, fn, v, k);
          for (const k2 of subset) {
            result.add(k2);
          }
        }
        return result;
      } finally {
        unlockForIteration(d);
      }
    }
  },
  DictFlattenToDict: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue, K2: EastTypeValue, _V2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (d: Map<any, any>, fn: (key: any, value: any) => any[], onConflict: (v1: any, v2: any, k: any) => null) => {
      const result = new SortedMap([], compare);
      lockForIteration(d);
      try {
        for (const [k, v] of d.entries()) {
          const subdict = call_function(location, fn, v, k);
          for (const [k2, v2] of subdict.entries()) {
            const existing = result.get(k2);
            if (existing === undefined) {
              result.set(k2, v2);
            } else {
              const new_v2 = call_function(location, onConflict, existing, v2, k2);
              result.set(k2, new_v2);
            }
          }
        }
        return result;
      } finally {
        unlockForIteration(d);
      }
    }
  },
  DictGroupFold: (location: LocationValue[], _platformDef: PlatformFunction[], _K: EastTypeValue, _V: EastTypeValue, K2: EastTypeValue, _T2: EastTypeValue) => {
    const compare = compareFor(K2);
    return (d: Map<any, any>, keyFn: (v: any, k: any) => any, init: (k2: any) => any, folder: (acc: any, v: any, k: any) => any) => {
      const result = new SortedMap([], compare);
      lockForIteration(d);
      try {
        for (const [k, v] of d.entries()) {
          const k2 = call_function(location, keyFn, v, k);
          let existing = result.get(k2);
          if (existing === undefined) {
            existing = call_function(location, init, k2);
          }
          const new_val = call_function(location, folder, existing, v, k);
          result.set(k2, new_val);
        }
        return result;
      } finally {
        unlockForIteration(d);
      }
    }
  },
}

/** @internal */
export function applyTypeParameters(t: EastTypeValue | string, params: Map<string, EastTypeValue>): EastTypeValue {
  if (typeof(t) === "string") {
    let ret = params.get(t);
    if (ret === undefined) {
      throw new Error(`Unable to find type parameter ${JSON.stringify(t)}`);
    }
    return ret;
  } else if (t.type === "Null" || t.type === "Boolean" || t.type === "Integer" || t.type === "Float" || t.type === "String" || t.type === "DateTime" || t.type ==="Blob" || t.type === "Never") {
    return t;
  } else if (t.type === "Ref") {
    return variant("Ref", applyTypeParameters(t.value, params));
  } else if (t.type === "Array") {
    return variant("Array", applyTypeParameters(t.value, params));
  } else if (t.type === "Set") {
    return variant("Set", applyTypeParameters(t.value, params));
  } else if (t.type === "Dict") {
    return variant("Dict", { key: applyTypeParameters(t.value.key, params), value: applyTypeParameters(t.value.value, params) });
  } else if (t.type === "Struct") {
    return variant("Struct", t.value.map(({ name, type }) => ({ name, type: applyTypeParameters(type, params) })));
  } else if (t.type === "Variant") {
    return variant("Variant", t.value.map(({ name, type }) => ({ name, type: applyTypeParameters(type, params) })));
  } else if (t.type === "Recursive") {
    return t;
  } else if (t.type === "Function") {
    return variant("Function", { inputs: t.value.inputs.map(i => applyTypeParameters(i, params)), output: applyTypeParameters(t.value.output, params) } );
  } else if (t.type === "AsyncFunction") {
    return variant("AsyncFunction", { inputs: t.value.inputs.map(i => applyTypeParameters(i, params)), output: applyTypeParameters(t.value.output, params) } );
  } else {
    throw new Error(`Unhandled type ${((t satisfies never) as EastTypeValue).type}`)
  }
}
