/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Analysis and validation of IR for JavaScript backend compilation.
 *
 * This module provides backend-specific enrichment of universal IR,
 * computing metadata needed for efficient JavaScript closure compilation.
 * Different backends (Julia, Python, etc.) would have their own analysis modules.
 */

import type { AsyncFunctionIR, FunctionIR, IR } from "./ir.js";
import { printLocationValue } from "./ir.js";
import type { EastTypeValue, StructTypeValue } from "./type_of_type.js";
import { isTypeValueEqual, isSubtypeValue, expandTypeValue, toEastTypeValue } from "./type_of_type.js";
import { printTypeValue } from "./compile.js";
import { variant } from "./containers/variant.js";
import { ArrayType, IntegerType, StringType, StructType } from "./types.js";
import { Builtins } from "./builtins.js";

/**
 * Platform definition for JavaScript backend.
 *
 * Maps platform function names to their implementations and async metadata.
 * Different JavaScript execution environments may provide different platforms
 * with the same functions but different async characteristics.
 *
 * Types are stored as EastTypeValue (IR representation) rather than EastType
 * (front-end representation) to avoid repeated conversion during analysis.
 *
 * @example
 * ```ts
 * const log = East.platform("log", [StringType], NullType);
 * const readFile = East.asyncPlatform("readFile", [StringType], StringType);
 *
 * const platform = [
 *   log.implement(console.log),
 *   readFile.implement(fs.promises.readFile),
 * ];
 * ```
 */
export type PlatformDefinition = {
  name: string,
  inputs: EastTypeValue[],
  output: EastTypeValue,
  type: 'sync' | 'async',
  // Generic platform function fields (optional for non-generic functions)
  type_parameters?: string[];
  inputsFn?: (...typeParams: EastTypeValue[]) => EastTypeValue[];
  outputsFn?: (...typeParams: EastTypeValue[]) => EastTypeValue;
};

export type AnalyzedIR<T extends IR = IR> = T & { value: { isAsync: boolean } };


/**
 * Variable metadata tracked during analysis.
 *
 * Tracks type information and other properties needed for optimization
 * and code generation.
 */
export interface VariableMetadata {
  /** The East type of this variable */
  type: EastTypeValue;

  /** Whether this variable can be mutated (let vs const) */
  mutable: boolean;

  /** The IR node that defined this variable (VariableIR from Let or Function parameter) */
  definedBy: IR;

  /** Whether this variable is captured by a nested function (mutated during analysis) */
  captured: boolean;

  // Future additions for variable analysis:
  //
  // /** Whether this variable needs boxing (mutable + captured) */
  // boxed?: boolean;
  //
  // /** Number of reads (for optimization) */
  // readCount?: number;
  //
  // /** Number of writes (for optimization) */
  // writeCount?: number;
}

/**
 * Variable context mapping names to their metadata.
 *
 * Used during analysis to track variable types and properties.
 */
export type VariableContext = Record<string, VariableMetadata>;

/**
 * Analyze IR tree and produce enriched IR for JavaScript backend.
 *
 * This function:
 * - Validates the IR (type checking, variable scope, etc.)
 * - Computes which nodes require async compilation
 * - Returns enriched IR with metadata populated (isAsync, etc.)
 *
 * @param ir - The IR tree to analyze
 * @param platformDef - Platform function definitions with async metadata
 * @param ctx - Variable context mapping variable names to their metadata
 * @returns Enriched IR with metadata fields populated
 * @throws {Error} If IR is invalid (type errors, undefined variables, etc.)
 *
 * @example
 * ```ts
 * const ir = // ... parsed East program
 * const platform = [
 *   log.implement(console.log),
 *   fetch.implement(fetch)  // async platform uses .implement() too
 * ];
 *
 * const enrichedIR = analyzeIR(ir, platform, {});
 * const compiled = compile_internal(enrichedIR, {}, platform);
 * ```
 */
export function analyzeIR<T extends IR>(
  ir: T,
  platformDef: PlatformDefinition[],
  ctx: VariableContext = {},
): AnalyzedIR<T> {
  // Working data for tracking during analysis
  const analysis = new Map<IR, { captured?: boolean }>();

  // Pre-populate analysis Map with definedBy nodes from external context.
  // This is needed when analyzing deserialized functions with captures - the external
  // context contains variable metadata with definedBy references that need to be in
  // the analysis Map so nested functions can properly mark them as captured.
  for (const varName of Object.keys(ctx)) {
    const varMeta = ctx[varName];
    if (varMeta?.definedBy && !analysis.has(varMeta.definedBy)) {
      analysis.set(varMeta.definedBy, { captured: varMeta.captured });
    }
  }

  // Build a lookup map for platform functions
  const platformMap = new Map<string, PlatformDefinition>();
  for (const p of platformDef) {
    if (platformMap.has(p.name)) {
      throw new Error(`Duplicate platform function definition for '${p.name}'`);
    }

    platformMap.set(p.name, p);
  }

  // Track circular references
  const visiting = new Set<IR>();

  function visit(node: IR, ctx: VariableContext, expectedReturnType?: EastTypeValue): AnalyzedIR {
    // Detect circular IR (we don't cache because we're building new nodes)
    if (visiting.has(node)) {
      throw new Error(`Circular IR reference detected at ${printLocationValue(node.value.location)}`);
    }

    visiting.add(node);
    try {
      const result = visitNode(node, ctx, expectedReturnType);
      return result;
    } finally {
      visiting.delete(node);
    }
  }

  function visitNode(node: IR, ctx: VariableContext, expectedReturnType?: EastTypeValue): AnalyzedIR {
    let isAsync: boolean = false;

    if (node.type === "Value") {
      // Validate that the type matches the value
      if (node.value.type.type !== node.value.value.type) {
        throw new Error(
          `Value node expected value of type .${node.value.type.type} ` +
          `but got .${node.value.value.type} at ${printLocationValue(node.value.location)}`
        );
      }

      // Value is always sync (literal constant)
      return {
        ...node,
        value: {
          ...node.value,
          isAsync: false,
        }
      } as AnalyzedIR;
    }

    else if (node.type === "Variable") {
      const name = node.value.name;
      const varMeta = ctx[name];

      // Validate variable is in scope
      if (varMeta === undefined) {
        throw new Error(
          `Variable ${name} not in scope at ${printLocationValue(node.value.location)}`
        );
      }

      // Validate type matches
      if (!isTypeValueEqual(varMeta.type, node.value.type)) {
        throw new Error(
          `Variable ${name} has type ${printTypeValue(varMeta.type)} ` +
          `but expected ${printTypeValue(node.value.type)} at ${printLocationValue(node.value.location)}`
        );
      }

      // Validate mutability matches
      if (varMeta.mutable !== node.value.mutable) {
        throw new Error(
          `Variable ${name} mutability mismatch: ` +
          `context has ${varMeta.mutable ? 'mutable' : 'const'} ` +
          `but IR expects ${node.value.mutable ? 'mutable' : 'const'} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Detect capture: if variable is not in current scope but in parent, mark as captured
      if (!Object.hasOwn(ctx, name)) {
        // Variable is from a parent scope - walk up to find and mark it
        let parentCtx = Object.getPrototypeOf(ctx) as VariableContext | null;
        while (parentCtx) {
          if (Object.hasOwn(parentCtx, name)) {
            // Found the defining scope - mark as captured in working memory
            const varMeta = parentCtx[name]!;
            varMeta.captured = true;

            // Also mark the defining VariableIR's analysis as captured
            const defVarAnalysis = analysis.get(varMeta.definedBy);
            if (!defVarAnalysis) {
              throw new Error(
                `Internal error: VariableIR node for ${name} not analyzed. ` +
                `This should never happen - all VariableIR nodes should be analyzed when encountered.`
              );
            }
            defVarAnalysis.captured = true;
            break;
          }
          parentCtx = Object.getPrototypeOf(parentCtx) as VariableContext | null;
        }
      }

      // Reading a variable is always synchronous
      return {
        ...node,
        value: {
          ...node.value,
          isAsync: false,
        }
      } as AnalyzedIR;
    }

    else if (node.type === "Let") {
      // Visit the value expression first
      const valueInfo = visit(node.value.value, ctx, expectedReturnType);

      // Validate value type exactly matches variable type
      // (Subtyping should be handled by explicit As nodes)
      if (node.value.variable.value.type.type !== "Never" && !isTypeValueEqual(valueInfo.value.type, node.value.variable.value.type)) {
        throw new Error(
          `Let statement requires exact type match. ` +
          `Variable ${node.value.variable.value.name} ` +
          `has type ${printTypeValue(node.value.variable.value.type)} ` +
          `but value has type ${printTypeValue(valueInfo.value.type)}. ` +
          `Insert an As node if subtyping is intended. ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Analyze the VariableIR node itself (so it has an entry in the analysis map)
      analysis.set(node.value.variable, {
        captured: false
      });

      // Add variable to context for subsequent statements
      const varName = node.value.variable.value.name;
      ctx[varName] = {
        type: node.value.variable.value.type,
        mutable: node.value.variable.value.mutable,
        definedBy: node.value.variable,  // Store reference to the VariableIR
        captured: false   // Initially not captured
      };

      // Return analyzed Let node with analyzed value
      return {
        ...node,
        value: {
          ...node.value,
          value: valueInfo,
          isAsync: valueInfo.value.isAsync,
        }
      } as AnalyzedIR;
    }

    else if (node.type === "Assign") {
      const varName = node.value.variable.value.name;
      const varMeta = ctx[varName];

      // Validate variable exists in scope
      if (varMeta === undefined) {
        throw new Error(
          `Cannot assign to variable ${varName} which is not in scope ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Validate variable is mutable in IR
      if (!node.value.variable.value.mutable) {
        throw new Error(
          `Cannot reassign const variable ${varName} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Validate variable is mutable in context (matches IR)
      if (!varMeta.mutable) {
        throw new Error(
          `Cannot reassign variable ${varName} - context says it's const ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Visit the value expression
      const valueInfo = visit(node.value.value, ctx, expectedReturnType);

      // Validate value type exactly matches variable type
      // (Subtyping should be handled by explicit As nodes)
      if (valueInfo.value.type.type !== "Never" && !isTypeValueEqual(valueInfo.value.type, varMeta.type)) {
        throw new Error(
          `Assign statement requires exact type match. ` +
          `Variable ${varName} has type ${printTypeValue(varMeta.type)} ` +
          `but value has type ${printTypeValue(valueInfo.value.type)}. ` +
          `Insert an As node if subtyping is intended. ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      isAsync = valueInfo.value.isAsync;  // Async if the value expression is async
    }

    else if (node.type === "Block") {
      // Create a new scope inheriting from parent (the classic trick!)
      const innerCtx = Object.create(ctx) as VariableContext;

      let lastType: EastTypeValue = variant("Null", null);

      // Visit each statement in sequence
      const analyzedStatements: AnalyzedIR[] = [];
      for (const statement of node.value.statements) {
        // Note: We don't validate unreachable code here because the IR generator
        // may produce statements after diverging control flow (e.g., return statements
        // from if/else branches). The type system ensures correctness anyway.

        const stmtInfo = visit(statement, innerCtx, expectedReturnType);
        analyzedStatements.push(stmtInfo);
        lastType = stmtInfo.value.type;
        if (stmtInfo.value.isAsync) {
          isAsync = true;
        }
      }

      // Validate block evaluates to expected type
      if (!isTypeValueEqual(lastType, node.value.type)) {
        throw new Error(
          `Block evaluates to type ${printTypeValue(lastType)} ` +
          `but expected ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Return analyzed Block with analyzed statements
      return {
        ...node,
        value: {
          ...node.value,
          statements: analyzedStatements as IR[],
          isAsync,
        }
      } as AnalyzedIR;
    }

    else if (node.type === "As") {
      // Visit the child value
      const valueInfo = visit(node.value.value, ctx, expectedReturnType);

      // Validate subtyping: child type must be subtype of target type
      if (!isSubtypeValue(valueInfo.value.type, node.value.type)) {
        throw new Error(
          `Cannot cast value of type ${printTypeValue(valueInfo.value.type)} ` +
          `to type ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // More thorough checks for "unnecessary" As IR nodes:

      // Cannot cast Never to a value
      if (valueInfo.value.type.type === "Never") {
        throw new Error(
          `Cannot cast .Never to type ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      if (isTypeValueEqual(valueInfo.value.type, node.value.type)) {
        throw new Error(
          `Unnecessary As node: value is already of type ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      isAsync = valueInfo.value.isAsync;  // Propagate async from child
    }

    else if (node.type === "Platform") {
      // Look up platform function
      const platformFn = platformMap.get(node.value.name);
      if (!platformFn) {
        // Allow missing platforms only if this specific platform function is marked as optional in the IR
        if (!node.value.optional) {
          throw new Error(
            `Platform function '${node.value.name}' not found ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }

        // allowMissingPlatform is true - analyze arguments without type validation
        // and let compile inject a runtime error stub
        const analyzedArgs: AnalyzedIR[] = [];
        for (const arg of node.value.arguments) {
          const argAnalyzed = visit(arg, ctx, expectedReturnType);
          analyzedArgs.push(argAnalyzed);
          if (argAnalyzed.value.isAsync) {
            isAsync = true;
          }
        }

        // Return analyzed Platform node with analyzed arguments (no type validation)
        return {
          ...node,
          value: {
            ...node.value,
            arguments: analyzedArgs as IR[],
            isAsync,
          }
        } as AnalyzedIR;
      }

      // Handle generic platform functions
      const typeParams = node.value.type_parameters ?? [];
      const expectedTypeParamCount = platformFn.type_parameters?.length ?? 0;

      if (typeParams.length !== expectedTypeParamCount) {
        throw new Error(
          `Platform function '${node.value.name}' expects ${expectedTypeParamCount} ` +
          `type parameters, got ${typeParams.length} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Compute concrete input/output types by substituting type parameters
      let inputTypes: EastTypeValue[];
      let outputType: EastTypeValue;

      if (expectedTypeParamCount > 0 && platformFn.inputsFn && platformFn.outputsFn) {
        // Generic platform function - use callbacks to compute types
        inputTypes = platformFn.inputsFn(...typeParams);
        outputType = platformFn.outputsFn(...typeParams);
      } else {
        // Non-generic - use stored concrete types
        inputTypes = platformFn.inputs;
        outputType = platformFn.output;
      }

      // Validate argument count (now using computed inputTypes)
      if (node.value.arguments.length !== inputTypes.length) {
        throw new Error(
          `Platform function '${node.value.name}' expects ${inputTypes.length} arguments ` +
          `but got ${node.value.arguments.length} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Visit all arguments, check if any are async, and validate types
      const analyzedArgs: AnalyzedIR[] = [];
      for (let i = 0; i < node.value.arguments.length; i++) {
        const arg = node.value.arguments[i]!;
        const argAnalyzed = visit(arg, ctx, expectedReturnType);
        analyzedArgs.push(argAnalyzed);

        if (argAnalyzed.value.isAsync) {
          isAsync = true;
        }

        // Validate argument type exactly matches expected (using computed inputTypes)
        // (Subtyping should be handled by explicit As nodes)
        const expectedType = inputTypes[i]!;
        if (argAnalyzed.value.type.type !== "Never" && !isTypeValueEqual(argAnalyzed.value.type, expectedType)) {
          throw new Error(
            `Platform function '${node.value.name}' argument ${i + 1} ` +
            `requires exact type match. ` +
            `Expected type ${printTypeValue(expectedType)} ` +
            `but got ${printTypeValue(argAnalyzed.value.type)}. ` +
            `Insert an As node if subtyping is intended. ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }
      }

      // Platform function itself might be async
      if (platformFn.type === 'async') {
        isAsync = true;
      }

      // Validate return type matches (using computed outputType)
      if (!isTypeValueEqual(node.value.type, outputType)) {
        throw new Error(
          `Platform function '${node.value.name}' return type ` +
          `expected to be ${printTypeValue(outputType)} ` +
          `but IR has ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Return analyzed Platform node with analyzed arguments
      return {
        ...node,
        value: {
          ...node.value,
          arguments: analyzedArgs as IR[],
          isAsync,
        }
      } as AnalyzedIR;
    }

    else if (node.type === "Function") {
      // Validate it has a Function type
      if (node.value.type.type !== "Function") {
        throw new Error(
          `Expected Function type, got ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Create new context for function body
      const fnCtx: VariableContext = {};

      // Add captured variables to context
      for (const captureVar of node.value.captures) {
        const outerVar = ctx[captureVar.value.name];
        if (outerVar === undefined) {
          throw new Error(
            `Captured variable ${captureVar.value.name} not in scope ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }
        if (!isTypeValueEqual(outerVar.type, captureVar.value.type)) {
          throw new Error(
            `Captured variable ${captureVar.value.name} has type ${printTypeValue(outerVar.type)} ` +
            `but expected ${printTypeValue(captureVar.value.type)} ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }
        if (outerVar.mutable !== captureVar.value.mutable) {
          throw new Error(
            `Captured variable ${captureVar.value.name} mutability mismatch: ` +
            `context has ${outerVar.mutable ? 'mutable' : 'const'} ` +
            `but IR expects ${captureVar.value.mutable ? 'mutable' : 'const'} ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }

        // Mark the outer variable as captured (it's being closed over by this function)
        const wasAlreadyCaptured = outerVar.captured;
        outerVar.captured = true;
        const defVarAnalysis = analysis.get(outerVar.definedBy);
        if (defVarAnalysis) {
          defVarAnalysis.captured = true;
        } else if (!wasAlreadyCaptured) {
          // Only error if this wasn't already marked as captured (from a synthetic/external context)
          throw new Error(
            `Internal error: VariableIR node for captured variable ${captureVar.value.name} not analyzed. ` +
            `This should never happen - all VariableIR nodes should be analyzed when encountered.`
          );
        }

        fnCtx[captureVar.value.name] = {
          type: captureVar.value.type,
          mutable: captureVar.value.mutable,
          definedBy: outerVar.definedBy,
          captured: false  // In the function's context, they're not "captured" yet
        };
      }

      // Add parameters to context
      for (const param of node.value.parameters) {
        // Analyze the parameter VariableIR node
        analysis.set(param, {
          captured: false
        });

        fnCtx[param.value.name] = {
          type: param.value.type,
          mutable: param.value.mutable,
          definedBy: param,  // Parameter VariableIR defines itself
          captured: false
        };
      }

      // Visit function body, passing expected return type for Return statement validation
      const expectedOutput = node.value.type.value.output;
      const bodyInfo = visit(node.value.body, fnCtx, expectedOutput);

      // Validate body return type
      // - If Never: OK (there was an explicit Return statement that was already validated)
      // - Otherwise: must exactly match expected output type
      if (bodyInfo.value.type.type !== "Never" && !isTypeValueEqual(bodyInfo.value.type, expectedOutput)) {
        throw new Error(
          `Function body returns type ${printTypeValue(bodyInfo.value.type)} ` +
          `but function signature expects ${printTypeValue(expectedOutput)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Creating a function is sync (it just captures variables at this stage)
      return {
        ...node,
        value: {
          ...node.value,
          body: bodyInfo,  // Use analyzed body
          isAsync: false,
        }
      } as AnalyzedIR<FunctionIR>;
    }

    else if (node.type === "AsyncFunction") {
      // Validate it has a Function type
      if (node.value.type.type !== "AsyncFunction") {
        throw new Error(
          `Expected AsyncFunction type, got ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Create new context for function body
      const fnCtx: VariableContext = {};

      // Add captured variables to context
      for (const captureVar of node.value.captures) {
        const outerVar = ctx[captureVar.value.name];
        if (outerVar === undefined) {
          throw new Error(
            `Captured variable ${captureVar.value.name} not in scope ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }
        if (!isTypeValueEqual(outerVar.type, captureVar.value.type)) {
          throw new Error(
            `Captured variable ${captureVar.value.name} has type ${printTypeValue(outerVar.type)} ` +
            `but expected ${printTypeValue(captureVar.value.type)} ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }
        if (outerVar.mutable !== captureVar.value.mutable) {
          throw new Error(
            `Captured variable ${captureVar.value.name} mutability mismatch: ` +
            `context has ${outerVar.mutable ? 'mutable' : 'const'} ` +
            `but IR expects ${captureVar.value.mutable ? 'mutable' : 'const'} ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }

        // Mark the outer variable as captured (it's being closed over by this function)
        const wasAlreadyCaptured = outerVar.captured;
        outerVar.captured = true;
        const defVarAnalysis = analysis.get(outerVar.definedBy);
        if (defVarAnalysis) {
          defVarAnalysis.captured = true;
        } else if (!wasAlreadyCaptured) {
          // Only error if this wasn't already marked as captured (from a synthetic/external context)
          throw new Error(
            `Internal error: VariableIR node for captured variable ${captureVar.value.name} not analyzed. ` +
            `This should never happen - all VariableIR nodes should be analyzed when encountered.`
          );
        }

        fnCtx[captureVar.value.name] = {
          type: captureVar.value.type,
          mutable: captureVar.value.mutable,
          definedBy: outerVar.definedBy,
          captured: false  // In the function's context, they're not "captured" yet
        };
      }

      // Add parameters to context
      for (const param of node.value.parameters) {
        // Analyze the parameter VariableIR node
        analysis.set(param, {
          captured: false
        });

        fnCtx[param.value.name] = {
          type: param.value.type,
          mutable: param.value.mutable,
          definedBy: param,  // Parameter VariableIR defines itself
          captured: false
        };
      }

      // Visit function body, passing expected return type for Return statement validation
      const expectedOutput = node.value.type.value.output;
      const bodyInfo = visit(node.value.body, fnCtx, expectedOutput);

      // Validate body return type
      // - If Never: OK (there was an explicit Return statement that was already validated)
      // - Otherwise: must exactly match expected output type
      if (bodyInfo.value.type.type !== "Never" && !isTypeValueEqual(bodyInfo.value.type, expectedOutput)) {
        throw new Error(
          `AsyncFunction body returns type ${printTypeValue(bodyInfo.value.type)} ` +
          `but function signature expects ${printTypeValue(expectedOutput)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Creating a function is sync (it just captures variables at this stage)
      return {
        ...node,
        value: {
          ...node.value,
          body: bodyInfo,  // Use analyzed body
          isAsync: false,
        }
      } as AnalyzedIR<AsyncFunctionIR>;
    }

    else if (node.type === "Call") {
      // Visit function expression
      const fnInfo = visit(node.value.function, ctx, expectedReturnType);

      // Validate it's a function type
      if (fnInfo.value.type.type !== "Function") {
        throw new Error(
          `Call expects Function type, got ${printTypeValue(fnInfo.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Validate argument count
      if (fnInfo.value.type.value.inputs.length !== node.value.arguments.length) {
        throw new Error(
          `Function expects ${fnInfo.value.type.value.inputs.length} arguments, ` +
          `got ${node.value.arguments.length} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Analyze all arguments
      const analyzedArgs: AnalyzedIR[] = [];
      for (let i = 0; i < node.value.arguments.length; i++) {
        const arg = node.value.arguments[i]!;
        const argInfo = visit(arg, ctx, expectedReturnType);
        analyzedArgs.push(argInfo);

        if (argInfo.value.isAsync) {
          isAsync = true;
        }

        // Validate argument type exactly matches expected
        const expectedType = fnInfo.value.type.value.inputs[i]!;
        if (argInfo.value.type.type !== "Never" && !isTypeValueEqual(argInfo.value.type, expectedType)) {
          throw new Error(
            `Function call argument ${i + 1} requires exact type match. ` +
            `Expected type ${printTypeValue(expectedType)} ` +
            `but got ${printTypeValue(argInfo.value.type)}. ` +
            `Insert an As node if subtyping is intended. ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }
      }

      // Validate return type matches
      if (!isTypeValueEqual(node.value.type, fnInfo.value.type.value.output)) {
        throw new Error(
          `Function call return type expected to be ${printTypeValue(fnInfo.value.type.value.output)} ` +
          `but IR has ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Return analyzed Call with analyzed function and arguments
      return {
        ...node,
        value: {
          ...node.value,
          function: fnInfo,
          arguments: analyzedArgs as IR[],
          isAsync,
        }
      } as AnalyzedIR;
    }

    else if (node.type === "CallAsync") {
      // CallAsync is similar to Call but always async - equivalent to `await fn(...)`
      isAsync = true;

      // Visit function expression
      const fnInfo = visit(node.value.function, ctx, expectedReturnType);

      // Validate it's an async function type
      if (fnInfo.value.type.type !== "AsyncFunction") {
        throw new Error(
          `CallAsync expects AsyncFunction type, got ${printTypeValue(fnInfo.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Validate argument count
      if (fnInfo.value.type.value.inputs.length !== node.value.arguments.length) {
        throw new Error(
          `Function expects ${fnInfo.value.type.value.inputs.length} arguments, ` +
          `got ${node.value.arguments.length} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Analyze all arguments
      const analyzedArgs: AnalyzedIR[] = [];
      for (let i = 0; i < node.value.arguments.length; i++) {
        const arg = node.value.arguments[i]!;
        const argInfo = visit(arg, ctx, expectedReturnType);
        analyzedArgs.push(argInfo);

        // Validate argument type exactly matches expected
        const expectedType = fnInfo.value.type.value.inputs[i]!;
        if (argInfo.value.type.type !== "Never" && !isTypeValueEqual(argInfo.value.type, expectedType)) {
          throw new Error(
            `Function call argument ${i + 1} requires exact type match. ` +
            `Expected type ${printTypeValue(expectedType)} ` +
            `but got ${printTypeValue(argInfo.value.type)}. ` +
            `Insert an As node if subtyping is intended. ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }
      }

      // Validate return type matches
      if (!isTypeValueEqual(node.value.type, fnInfo.value.type.value.output)) {
        throw new Error(
          `Function call return type expected to be ${printTypeValue(fnInfo.value.type.value.output)} ` +
          `but IR has ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Return analyzed Call with analyzed function and arguments
      return {
        ...node,
        value: {
          ...node.value,
          function: fnInfo,
          arguments: analyzedArgs as IR[],
          isAsync,
        }
      } as AnalyzedIR;
    }

    else if (node.type === "Builtin") {
      // builtins are currently all synchronous (and accept synchronous-only functions as arguments)
      isAsync = false;

      // Look up builtin function
      const builtinName = node.value.builtin;
      const builtin = Builtins[builtinName];
      if (!builtin) {
        throw new Error(
          `Unknown builtin function '${builtinName}' ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      if (node.value.arguments.length !== builtin.inputs.length) {
        throw new Error(
          `Builtin function '${builtinName}' expects ${builtin.inputs.length} arguments, ` +
          `but got ${node.value.arguments.length} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Visit all arguments
      const analyzedArgs: AnalyzedIR[] = [];
      for (const arg of node.value.arguments) {
        const argInfo = visit(arg, ctx, expectedReturnType);
        analyzedArgs.push(argInfo);
        if (argInfo.value.isAsync) {
          isAsync = true;
        }
      }

      // Return analyzed Builtin with analyzed arguments
      return {
        ...node,
        value: {
          ...node.value,
          arguments: analyzedArgs as IR[],
          isAsync,
        }
      } as AnalyzedIR;
    }

    else if (node.type === "Return") {
      // Validate we're inside a function
      if (!expectedReturnType) {
        throw new Error(
          `Return statement outside of function at ${printLocationValue(node.value.location)}`
        );
      }

      // Analyze the return value expression
      const valueInfo = visit(node.value.value, ctx, expectedReturnType);

      // Validate return value type exactly matches expected return type
      if (valueInfo.value.type.type !== "Never" && !isTypeValueEqual(valueInfo.value.type, expectedReturnType)) {
        throw new Error(
          `Return statement returns type ${printTypeValue(valueInfo.value.type)} ` +
          `but function signature expects ${printTypeValue(expectedReturnType)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Return analyzed Return node with analyzed value
      return {
        ...node,
        value: {
          ...node.value,
          value: valueInfo,
          isAsync: valueInfo.value.isAsync,
        }
      } as AnalyzedIR;
    }

    else if (node.type === "NewRef") {
      // Validate type is Ref
      if (node.value.type.type !== "Ref") {
        throw new Error(
          `NewRef node must have Ref type, got ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      const elementType = node.value.type.value;
      
      const valueInfo = visit(node.value.value, ctx, expectedReturnType);
      isAsync = valueInfo.value.isAsync;

      // Validate element type exactly matches
      if (valueInfo.value.type.type !== "Never" && !isTypeValueEqual(valueInfo.value.type, elementType)) {
        throw new Error(
          `Ref value has type ${printTypeValue(valueInfo.value.type)} ` +
          `but Ref expects ${printTypeValue(elementType)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }
    }

    else if (node.type === "NewArray") {
      // Validate type is Array
      if (node.value.type.type !== "Array") {
        throw new Error(
          `NewArray node must have Array type, got ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      const elementType = node.value.type.value;
      isAsync = false;

      // Visit all element values and validate types
      for (let i = 0; i < node.value.values.length; i++) {
        const valueExpr = node.value.values[i]!;
        const valueInfo = visit(valueExpr, ctx, expectedReturnType);

        if (valueInfo.value.isAsync) {
          isAsync = true;
        }

        // Validate element type exactly matches
        if (valueInfo.value.type.type !== "Never" && !isTypeValueEqual(valueInfo.value.type, elementType)) {
          throw new Error(
            `Array element ${i} has type ${printTypeValue(valueInfo.value.type)} ` +
            `but array expects ${printTypeValue(elementType)} ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }
      }
    }

    else if (node.type === "NewSet") {
      // Validate type is Set
      if (node.value.type.type !== "Set") {
        throw new Error(
          `NewSet node must have Set type, got ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      const keyType = node.value.type.value;
      isAsync = false;

      // Visit all element values and validate types
      for (let i = 0; i < node.value.values.length; i++) {
        const keyExpr = node.value.values[i]!;
        const keyInfo = visit(keyExpr, ctx, expectedReturnType);

        if (keyInfo.value.isAsync) {
          isAsync = true;
        }

        // Validate element type exactly matches
        if (keyInfo.value.type.type !== "Never" && !isTypeValueEqual(keyInfo.value.type, keyType)) {
          throw new Error(
            `Set element ${i} has type ${printTypeValue(keyInfo.value.type)} ` +
            `but set expects ${printTypeValue(keyType)} ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }
      }
    }

    else if (node.type === "NewDict") {
      // Validate type is Dict
      if (node.value.type.type !== "Dict") {
        throw new Error(
          `NewDict node must have Dict type, got ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      const keyType = node.value.type.value.key;
      const valueType = node.value.type.value.value;
      isAsync = false;

      // Visit all key-value pairs and validate types
      for (let i = 0; i < node.value.values.length; i++) {
        const pair = node.value.values[i]!;

        const keyInfo = visit(pair.key, ctx, expectedReturnType);
        if (keyInfo.value.isAsync) {
          isAsync = true;
        }

        const valInfo = visit(pair.value, ctx, expectedReturnType);
        if (valInfo.value.isAsync) {
          isAsync = true;
        }

        // Validate key type exactly matches
        if (keyInfo.value.type.type !== "Never" && !isTypeValueEqual(keyInfo.value.type, keyType)) {
          throw new Error(
            `Dict key ${i} has type ${printTypeValue(keyInfo.value.type)} ` +
            `but dict expects ${printTypeValue(keyType)} ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }

        // Validate value type exactly matches
        if (valInfo.value.type.type !== "Never" && !isTypeValueEqual(valInfo.value.type, valueType)) {
          throw new Error(
            `Dict value ${i} has type ${printTypeValue(valInfo.value.type)} ` +
            `but dict expects ${printTypeValue(valueType)} ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }
      }
    }

    else if (node.type === "ForArray") {
      // Visit the array expression
      const arrayInfo = visit(node.value.array, ctx, expectedReturnType);

      // Validate it's an Array type (not Never)
      if (arrayInfo.value.type.type !== "Array") {
        throw new Error(
          `ForArray expects Array type, got ${printTypeValue(arrayInfo.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      const elementType = arrayInfo.value.type.value;

      // Validate key variable is Integer type
      if (node.value.key.value.type.type !== "Integer") {
        throw new Error(
          `ForArray key must be Integer type, got ${printTypeValue(node.value.key.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Validate value variable matches array element type
      if (!isTypeValueEqual(node.value.value.value.type, elementType)) {
        throw new Error(
          `ForArray value variable has type ${printTypeValue(node.value.value.value.type)} ` +
          `but array elements have type ${printTypeValue(elementType)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Analyze the key and value VariableIR nodes
      analysis.set(node.value.key, {
        captured: false
      });

      analysis.set(node.value.value, {
        captured: false
      });

      // Create new scope for loop body with key and value variables
      const loopCtx = Object.create(ctx) as VariableContext;
      loopCtx[node.value.key.value.name] = {
        type: node.value.key.value.type,
        mutable: node.value.key.value.mutable,
        definedBy: node.value.key,
        captured: false
      };
      loopCtx[node.value.value.value.name] = {
        type: node.value.value.value.type,
        mutable: node.value.value.value.mutable,
        definedBy: node.value.value,
        captured: false
      };

      // Visit loop body
      const bodyInfo = visit(node.value.body, loopCtx, expectedReturnType);

      // Return analyzed ForArray with analyzed array and body
      return {
        ...node,
        value: {
          ...node.value,
          array: arrayInfo as IR,
          body: bodyInfo as IR,
          isAsync: arrayInfo.value.isAsync || bodyInfo.value.isAsync,
        }
      } as AnalyzedIR;
    }

    else if (node.type === "ForSet") {
      // Visit the set expression
      const setInfo = visit(node.value.set, ctx, expectedReturnType);

      // Validate it's a Set type (not Never)
      if (setInfo.value.type.type !== "Set") {
        throw new Error(
          `ForSet expects Set type, got ${printTypeValue(setInfo.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      const elementType = setInfo.value.type.value;

      // Validate key variable matches set element type
      if (!isTypeValueEqual(node.value.key.value.type, elementType)) {
        throw new Error(
          `ForSet key variable has type ${printTypeValue(node.value.key.value.type)} ` +
          `but set elements have type ${printTypeValue(elementType)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Analyze the key VariableIR node
      analysis.set(node.value.key, {
        captured: false
      });

      // Create new scope for loop body with key variable
      const loopCtx = Object.create(ctx) as VariableContext;
      loopCtx[node.value.key.value.name] = {
        type: node.value.key.value.type,
        mutable: node.value.key.value.mutable,
        definedBy: node.value.key,
        captured: false
      };

      // Visit loop body
      const bodyInfo = visit(node.value.body, loopCtx, expectedReturnType);

      isAsync = setInfo.value.isAsync || bodyInfo.value.isAsync;
    }

    else if (node.type === "ForDict") {
      // Visit the dict expression
      const dictInfo = visit(node.value.dict, ctx, expectedReturnType);

      // Validate it's a Dict type (not Never)
      if (dictInfo.value.type.type !== "Dict") {
        throw new Error(
          `ForDict expects Dict type, got ${printTypeValue(dictInfo.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      const keyType = dictInfo.value.type.value.key;
      const valueType = dictInfo.value.type.value.value;

      // Validate key variable matches dict key type
      if (!isTypeValueEqual(node.value.key.value.type, keyType)) {
        throw new Error(
          `ForDict key variable has type ${printTypeValue(node.value.key.value.type)} ` +
          `but dict keys have type ${printTypeValue(keyType)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Validate value variable matches dict value type
      if (!isTypeValueEqual(node.value.value.value.type, valueType)) {
        throw new Error(
          `ForDict value variable has type ${printTypeValue(node.value.value.value.type)} ` +
          `but dict values have type ${printTypeValue(valueType)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Analyze the key and value VariableIR nodes
      analysis.set(node.value.key, {
        captured: false
      });

      analysis.set(node.value.value, {
        captured: false
      });

      // Create new scope for loop body with key and value variables
      const loopCtx = Object.create(ctx) as VariableContext;
      loopCtx[node.value.key.value.name] = {
        type: node.value.key.value.type,
        mutable: node.value.key.value.mutable,
        definedBy: node.value.key,
        captured: false
      };
      loopCtx[node.value.value.value.name] = {
        type: node.value.value.value.type,
        mutable: node.value.value.value.mutable,
        definedBy: node.value.value,
        captured: false
      };

      // Visit loop body
      const bodyInfo = visit(node.value.body, loopCtx, expectedReturnType);

      isAsync = dictInfo.value.isAsync || bodyInfo.value.isAsync;
    }

    else if (node.type === "IfElse") {
      isAsync = false;
      let allBranchesNever = true;

      // Visit all if/else-if branches
      const analyzedIfs: { predicate: AnalyzedIR, body: AnalyzedIR }[] = [];
      for (let i = 0; i < node.value.ifs.length; i++) {
        const branch = node.value.ifs[i]!;

        // Visit and validate predicate is Boolean
        const predicateInfo = visit(branch.predicate, ctx, expectedReturnType);
        if (predicateInfo.value.isAsync) {
          isAsync = true;
        }

        if (predicateInfo.value.type.type !== "Boolean") {
          throw new Error(
            `IfElse predicate ${i} must be Boolean type, got ${printTypeValue(predicateInfo.value.type)} ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }

        // Visit branch body and validate type
        const bodyInfo = visit(branch.body, ctx, expectedReturnType);
        if (bodyInfo.value.isAsync) {
          isAsync = true;
        }

        // Track if this branch returns normally
        if (bodyInfo.value.type.type !== "Never") {
          allBranchesNever = false;
        }

        // Branch body must be IfElse result type (or Never)
        if (bodyInfo.value.type.type !== "Never" && !isTypeValueEqual(bodyInfo.value.type, node.value.type)) {
          throw new Error(
            `IfElse branch ${i} returns type ${printTypeValue(bodyInfo.value.type)} ` +
            `but IfElse expects ${printTypeValue(node.value.type)} ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }

        analyzedIfs.push({ predicate: predicateInfo, body: bodyInfo });
      }

      // Visit else body and validate type
      const elseInfo = visit(node.value.else_body, ctx, expectedReturnType);
      if (elseInfo.value.isAsync) {
        isAsync = true;
      }

      // Track if else branch returns normally
      if (elseInfo.value.type.type !== "Never") {
        allBranchesNever = false;
      }

      // Branch body must be IfElse result type (or Never)
      if (elseInfo.value.type.type !== "Never" && !isTypeValueEqual(elseInfo.value.type, node.value.type)) {
        throw new Error(
          `IfElse else branch returns type ${printTypeValue(elseInfo.value.type)} ` +
          `but IfElse expects ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // If all branches diverge, IfElse must be Never
      if (allBranchesNever && node.value.type.type !== "Never") {
        throw new Error(
          `IfElse has all branches returning Never, so it must have type Never, ` +
          `but has type ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // If IfElse is Never, all branches must be Never
      if (node.value.type.type === "Never" && !allBranchesNever) {
        throw new Error(
          `IfElse has type Never but not all branches diverge ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Return analyzed IfElse with analyzed branches
      return {
        ...node,
        value: {
          ...node.value,
          ifs: analyzedIfs.map(({ predicate, body }) => ({ predicate: predicate as IR, body: body as IR })),
          else_body: elseInfo as IR,
          isAsync,
        }
      } as AnalyzedIR;
    }

    else if (node.type === "While") {
      // Visit and validate predicate is Boolean or Never
      const predicateInfo = visit(node.value.predicate, ctx, expectedReturnType);

      if (predicateInfo.value.type.type !== "Boolean") {
        throw new Error(
          `While predicate must be Boolean type, got ${printTypeValue(predicateInfo.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Visit loop body
      const bodyInfo = visit(node.value.body, ctx, expectedReturnType);

      // While returns Null, is async if predicate or body is async
      return {
        ...node,
        value: {
          ...node.value,
          predicate: predicateInfo as IR,
          body: bodyInfo as IR,
          isAsync: predicateInfo.value.isAsync || bodyInfo.value.isAsync,
        }
      } as AnalyzedIR;
    }

    else if (node.type === "Continue") {
      // Continue always has type Never (diverges control flow)
      isAsync = false;  // Continue is not async
    }

    else if (node.type === "Break") {
      // Break always has type Never (diverges control flow)
      isAsync = false;  // Break is not async
    }

    else if (node.type === "Error") {
      // Visit and validate message is String type
      const messageInfo = visit(node.value.message, ctx, expectedReturnType);

      if (messageInfo.value.type.type !== "String") {
        throw new Error(
          `Error message must be String type, got ${printTypeValue(messageInfo.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Error always has type Never (throws exception, diverges control flow)
      isAsync = messageInfo.value.isAsync;  // Error is async if message is async
    }

    else if (node.type === "TryCatch") {
      // Visit try body
      const tryInfo = visit(node.value.try_body, ctx, expectedReturnType);

      // Validate message variable is String type
      if (node.value.message.value.type.type !== "String") {
        throw new Error(
          `TryCatch message variable must be String type, got ${printTypeValue(node.value.message.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Validate stack variable is correct type
      const stackType = toEastTypeValue(ArrayType(StructType({ filename: StringType, line: IntegerType, column: IntegerType })));
      if (!isTypeValueEqual(node.value.stack.value.type, stackType)) {
        throw new Error(
          `TryCatch stack variable must be ${printTypeValue(stackType)} type, got ${printTypeValue(node.value.stack.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Analyze the message and stack VariableIR nodes
      analysis.set(node.value.message, {
        captured: false
      });

      analysis.set(node.value.stack, {
        captured: false
      });

      // Create new scope for catch body with message and stack variables
      const catchCtx = Object.create(ctx) as VariableContext;
      catchCtx[node.value.message.value.name] = {
        type: node.value.message.value.type,
        mutable: node.value.message.value.mutable,
        definedBy: node.value.message,
        captured: false
      };
      catchCtx[node.value.stack.value.name] = {
        type: node.value.stack.value.type,
        mutable: node.value.stack.value.mutable,
        definedBy: node.value.stack,
        captured: false
      };

      // Visit catch body
      const catchInfo = visit(node.value.catch_body, catchCtx, expectedReturnType);

      // Both bodies must be TryCatch result type (or Never)
      if (tryInfo.value.type.type !== "Never" && !isTypeValueEqual(tryInfo.value.type, node.value.type)) {
        throw new Error(
          `TryCatch try body returns type ${printTypeValue(tryInfo.value.type)} ` +
          `but TryCatch expects ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      if (catchInfo.value.type.type !== "Never" && !isTypeValueEqual(catchInfo.value.type, node.value.type)) {
        throw new Error(
          `TryCatch catch body returns type ${printTypeValue(catchInfo.value.type)} ` +
          `but TryCatch expects ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // If both bodies diverge, TryCatch must be Never
      const bothNever = tryInfo.value.type.type === "Never" && catchInfo.value.type.type === "Never";
      if (bothNever && node.value.type.type !== "Never") {
        throw new Error(
          `TryCatch has both try and catch bodies returning Never, so it must have type Never, ` +
          `but has type ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Visit finally body
      const finallyInfo = visit(node.value.finally_body, ctx, expectedReturnType);

      isAsync = tryInfo.value.isAsync || catchInfo.value.isAsync || finallyInfo.value.isAsync;

      // Return analyzed TryCatch with analyzed bodies
      return {
        ...node,
        value: {
          ...node.value,
          try_body: tryInfo as IR,
          catch_body: catchInfo as IR,
          finally_body: finallyInfo as IR,
          isAsync,
        }
      } as AnalyzedIR;
    }

    else if (node.type === "Struct") {
      // Validate type is Struct
      if (node.value.type.type !== "Struct") {
        throw new Error(
          `Struct node must have Struct type, got ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      const structType = expandTypeValue(node.value.type) as StructTypeValue;
      isAsync = false;

      if (structType.value.length !== node.value.fields.length) {
        throw new Error(
          `Struct type has ${structType.value.length} fields but struct value has ` +
          `${node.value.fields.length} fields ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Visit all field values and validate types
      for (const [i, field] of node.value.fields.entries()) {
        const fieldInfo = visit(field.value, ctx, expectedReturnType);

        if (fieldInfo.value.isAsync) {
          isAsync = true;
        }

        // Find corresponding field in struct type (in fixed order)
        const typeField = structType.value[i]!;
        if (typeField.name !== field.name) {
          throw new Error(
            `Struct has field ${typeField.name} at position ${i}, but value does not ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }

        // Validate field type exactly matches
        if (!isTypeValueEqual(fieldInfo.value.type, typeField.type)) {
          throw new Error(
            `Struct field ${field.name} has type ${printTypeValue(fieldInfo.value.type)} ` +
            `but struct type expects ${printTypeValue(typeField.type)} ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }
      }

    }

    else if (node.type === "GetField") {
      // Visit the struct expression
      const structInfo = visit(node.value.struct, ctx, expectedReturnType);

      // Validate it's a Struct type
      if (structInfo.value.type.type !== "Struct") {
        throw new Error(
          `GetField expects Struct type, got ${printTypeValue(structInfo.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Find the field in struct type
      const structType = expandTypeValue(structInfo.value.type) as StructTypeValue;
      const field = structType.value.find(f => f.name === node.value.field);

      if (!field) {
        throw new Error(
          `Struct does not have field ${node.value.field} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Validate return type matches field type
      if (!isTypeValueEqual(node.value.type, field.type)) {
        throw new Error(
          `GetField result type ${printTypeValue(node.value.type)} ` +
          `does not match field type ${printTypeValue(field.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      isAsync = structInfo.value.isAsync;
    }

    else if (node.type === "Variant") {
      // Visit the value expression
      const valueInfo = visit(node.value.value, ctx, expectedReturnType);

      // Validate type is Variant
      if (node.value.type.type !== "Variant") {
        throw new Error(
          `Variant node must have Variant type, got ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Expand recursive types to get well-formed variant type
      const variantType = expandTypeValue(node.value.type);
      if (variantType.type !== "Variant") {
        throw new Error(
          `Expanded Variant type is not Variant, got ${printTypeValue(variantType)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Find the case in variant type
      const caseType = variantType.value.find((c) => c.name === node.value.case);
      if (!caseType) {
        throw new Error(
          `Variant type does not have case ${node.value.case} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Validate value type exactly matches case type
      if (!isTypeValueEqual(valueInfo.value.type, caseType.type)) {
        throw new Error(
          `Variant case ${node.value.case} value has type ${printTypeValue(valueInfo.value.type)} ` +
          `but variant type expects ${printTypeValue(caseType.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      isAsync = valueInfo.value.isAsync;
    }

    else if (node.type === "Match") {
      // Visit the variant expression
      const variantInfo = visit(node.value.variant, ctx, expectedReturnType);

      // Validate it's a Variant type
      if (variantInfo.value.type.type !== "Variant") {
        throw new Error(
          `Match expects Variant type, got ${printTypeValue(variantInfo.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Expand recursive types to get well-formed variant type
      const variantType = expandTypeValue(variantInfo.value.type);
      if (variantType.type !== "Variant") {
        throw new Error(
          `Expanded Match variant type is not Variant, got ${printTypeValue(variantType)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // Validate case count matches
      if (variantType.value.length !== node.value.cases.length) {
        throw new Error(
          `Match has ${node.value.cases.length} cases but variant type has ` +
          `${variantType.value.length} cases ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      isAsync = variantInfo.value.isAsync;
      let allCasesNever = true;

      // Visit all match cases
      for (const matchCase of node.value.cases) {
        // Find corresponding case in variant type
        const typeCase = variantType.value.find((c) => c.name === matchCase.case);
        if (!typeCase) {
          throw new Error(
            `Match has case ${matchCase.case} but variant type does not ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }

        // Validate variable type matches case type
        if (!isTypeValueEqual(matchCase.variable.value.type, typeCase.type)) {
          throw new Error(
            `Match case ${matchCase.case} variable has type ${printTypeValue(matchCase.variable.value.type)} ` +
            `but variant case has type ${printTypeValue(typeCase.type)} ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }

        // Analyze the variable VariableIR node
        analysis.set(matchCase.variable, {
        captured: false
        });

        // Create new scope for case body with variable
        const caseCtx = Object.create(ctx) as VariableContext;
        caseCtx[matchCase.variable.value.name] = {
          type: matchCase.variable.value.type,
          mutable: matchCase.variable.value.mutable,
          definedBy: matchCase.variable,
          captured: false
        };

        // Visit case body
        const bodyInfo = visit(matchCase.body, caseCtx, expectedReturnType);
        if (bodyInfo.value.isAsync) {
          isAsync = true;
        }

        // Track if this case returns normally
        if (bodyInfo.value.type.type !== "Never") {
          allCasesNever = false;
        }

        // Case body must be Match result type (or Never)
        if (bodyInfo.value.type.type !== "Never" && !isTypeValueEqual(bodyInfo.value.type, node.value.type)) {
          throw new Error(
            `Match case ${matchCase.case} returns type ${printTypeValue(bodyInfo.value.type)} ` +
            `but Match expects ${printTypeValue(node.value.type)} ` +
            `at ${printLocationValue(node.value.location)}`
          );
        }
      }

      // If all cases diverge, Match must be Never
      if (allCasesNever && node.value.type.type !== "Never") {
        throw new Error(
          `Match has all cases returning Never, so it must have type Never, ` +
          `but has type ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      // isAsync already set from loop above
    }

    else if (node.type === "UnwrapRecursive") {
      // Visit the value expression
      const valueInfo = visit(node.value.value, ctx, expectedReturnType);

      // Validate result type matches expanded type
      if (valueInfo.value.type.type !== "Never" && !isTypeValueEqual(node.value.type, valueInfo.value.type)) {
        throw new Error(
          `UnwrapRecursive result type ${printTypeValue(node.value.type)} ` +
          `does not match recursive type ${printTypeValue(valueInfo.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      isAsync = valueInfo.value.isAsync;
    }

    else if (node.type === "WrapRecursive") {
      // Visit the value expression
      const valueInfo = visit(node.value.value, ctx, expectedReturnType);

      // Validate value type matches expanded recursive type
      if (valueInfo.value.type.type !== "Never" && !isTypeValueEqual(valueInfo.value.type, node.value.type)) {
        throw new Error(
          `WrapRecursive value has type ${printTypeValue(valueInfo.value.type)} ` +
          `but expects ${printTypeValue(node.value.type)} ` +
          `at ${printLocationValue(node.value.location)}`
        );
      }

      isAsync = valueInfo.value.isAsync;
    }

    else {
      throw new Error(`Unhandled IR type: ${(node satisfies never as IR).type} at ${printLocationValue((node as IR).value?.location || { file: "unknown", line: 0, column: 0 })}`);
    }

    return {
      ...node,
      value: {
        ...node.value as any,
        isAsync,
      }
    }
  }

  return visit(ir, ctx) as AnalyzedIR<T>;
}
