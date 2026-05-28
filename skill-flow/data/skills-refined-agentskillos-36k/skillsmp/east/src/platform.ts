/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 *
 * @remarks
 */
import { type EastTypeValue } from "./type_of_type.js";

/** Represents a platform function in East */
export type PlatformFunction = {
    /** The name of the platform function */
    name: string,
    /** Input parameter types (as EastTypeValue for analysis) */
    inputs: EastTypeValue[],
    /** Output type (as EastTypeValue for analysis) */
    output: EastTypeValue,
    /** Whether the function is asynchronous (returns a Promise) */
    type: 'sync' | 'async',
    /** The function implementation */
    fn: (...args: any) => any;
    // Generic platform function fields (optional for non-generic functions)
    /** Type parameter names for generic functions (e.g., ["T", "U"]) */
    type_parameters?: string[];
    /** Computes input types from resolved type parameters */
    inputsFn?: (...typeParams: EastTypeValue[]) => EastTypeValue[];
    /** Computes output type from resolved type parameters */
    outputsFn?: (...typeParams: EastTypeValue[]) => EastTypeValue;
}
