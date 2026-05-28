/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Internal exports for East
 * These are more internal APIs that may be useful for tools and integrations
 */

import { platform } from './expr/block.js';
import type { EastType } from './types.js';
export { TypeSymbol } from './expr/expr.js';

export * from './eastir.js';
export * from './platform.js';
export * from './expr/block.js';
export * from './expr/function.js';
export * from './error.js';
export * from './ir.js';
export { OutOfScopeException } from './ast_to_ir.js';
export * from './type_of_type.js';
export * from './types.js';
export * from './fuzz.js';
export { decodeBeast2For, encodeBeast2For, compileFunctionIR, compileAsyncFunctionIR, EAST_IR_SYMBOL } from './serialization/beast2.js';
// Patch system internals - value-level operations
export { diffFor } from './patch/diff.js';
export { applyFor } from './patch/apply.js';
export { invertFor } from './patch/invert.js';
export { composeFor } from './patch/compose.js';
export { type DiffContext, type ApplyContext, type ComposeContext, type InvertContext } from './patch/types.js';
export * from './datetime_format/types.js';
export * from './datetime_format/tokenize.js';
export * from './datetime_format/print.js';
export * from './datetime_format/parse.js';
// Profiling exports - for performance analysis
export { analyzeIR } from './analyze.js';
export { compile_internal } from './compile.js';

/**
 * Type helper for platform function definitions.
 * Use this to properly type platform function declarations.
 *
 * @typeParam Inputs - Tuple of input parameter types
 * @typeParam Output - Return type of the platform function
 *
 * @example
 * ```ts
 * import { East, StringType, NullType } from "@elaraai/east";
 * import type { PlatformFunctionDef } from "@elaraai/east/internal";
 *
 * export const console_log: PlatformFunctionDef<[typeof StringType], typeof NullType> =
 *     East.platform("console_log", [StringType], NullType);
 * ```
 */
export type PlatformFunctionDef<Inputs extends EastType[], Output extends EastType> =
    ReturnType<typeof platform<Inputs, Output>>;
