/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { type ValueTypeOf } from "./types.js";
import type { AsyncFunctionIR, FunctionIR } from "./ir.js";
import { compile_internal, ReturnException, EAST_IR_SYMBOL } from "./compile.js";
import type { PlatformFunction } from "./platform.js";
import { analyzeIR } from "./analyze.js";

/** A helper class wrapping East's "intermediate representation" (IR) for a free function.
 * The IR can be serialized and saved, or compiled so that the function can be executed.
 */
export class EastIR<Inputs extends any[], Output extends any> {
  constructor(public ir: FunctionIR) {
    if (ir.type !== "Function") {
      throw new Error(`Expected function expression, got a ${ir.type}`)
    }
    if (ir.value.captures.length !== 0) {
      throw new Error(`Expected free function, without captured variables`)
    }
  }

  /** Compile the function for execution in JavaScript using a closure-compiler technique.
   * Platform functions must be provided for the function to evaluate.
   *
   * @param platform - Array of platform function implementations
   */
  compile(platform: PlatformFunction[]): (...inputs: { [K in keyof Inputs]: ValueTypeOf<Inputs[K]> }) => ValueTypeOf<Output> {
    // Analyse the IR
    const analyzed_ir = analyzeIR(this.ir, platform);

    // compile the function (with no variables in environment)
    const platformFns = Object.fromEntries(platform.map(fn => [fn.name, fn.fn]));
    const asyncPlatformFns = new Set<string>();

    const compiled_expr = compile_internal(analyzed_ir, {}, platformFns, asyncPlatformFns, platform);

    // instantiate the function (with no environment)
    const instantiated_function = compiled_expr({});

    // Return sync wrapper
    const wrapper = (...inputs: any[]) => {
      try {
        return instantiated_function(...inputs)
      } catch (e: unknown) {
        if (e instanceof ReturnException) {
          return e.value;
        } else {
          throw e;
        }
      }
    };

    // Attach IR to wrapper for serialization support
    Object.defineProperty(wrapper, EAST_IR_SYMBOL, {
      value: this.ir,
      writable: false,
      enumerable: false,
      configurable: false
    });

    return wrapper;
  }
}

/** A helper class wrapping East's "intermediate representation" (IR) for a free async function.
 * The IR can be serialized and saved, or compiled so that the function can be executed.
 */
export class AsyncEastIR<Inputs extends any[], Output extends any> {
  constructor(public ir: AsyncFunctionIR) {
    if (ir.type !== "AsyncFunction") {
      throw new Error(`Expected async function expression, got a ${ir.type}`)
    }
    if (ir.value.captures.length !== 0) {
      throw new Error(`Expected free async function, without captured variables`)
    }
  }

  /** Compile the async function for execution in JavaScript using a closure-compiler technique.
   * Platform functions must be provided for the function to evaluate, which may return `Promise`s.
   * The compiled function itself returns a `Promise`.
   *
   * @param platform - Array of platform function implementations
   */
  compile(platform: PlatformFunction[]): (...inputs: { [K in keyof Inputs]: ValueTypeOf<Inputs[K]> }) => Promise<ValueTypeOf<Output>> {
    // Analyse the IR
    const analyzed_ir = analyzeIR(this.ir, platform);

    // compile the function (with no variables in environment)
    const platformFns = Object.fromEntries(platform.map(fn => [fn.name, fn.fn]));
    const asyncPlatformFns = new Set(
      platform.filter(fn => fn.type === 'async').map(fn => fn.name)
    );

    const compiled_expr = compile_internal(analyzed_ir, {}, platformFns, asyncPlatformFns, platform);

    // instantiate the function (with no environment)
    const instantiated_function = compiled_expr({});

    // Return async wrapper
    const wrapper = async (...inputs: any[]) => {
      try {
        return await instantiated_function(...inputs)
      } catch (e: unknown) {
        if (e instanceof ReturnException) {
          return e.value;
        } else {
          throw e;
        }
      }
    };

    // Attach IR to wrapper for serialization support
    Object.defineProperty(wrapper, EAST_IR_SYMBOL, {
      value: this.ir,
      writable: false,
      enumerable: false,
      configurable: false
    });

    return wrapper;
  }
}
