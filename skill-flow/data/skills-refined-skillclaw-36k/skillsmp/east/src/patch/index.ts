/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Patch system for computing and applying differences between East values.
 *
 * Provides four core operations:
 * - `diffFor(type)` - Compute the difference between two values
 * - `applyFor(type)` - Apply a patch to a value
 * - `composeFor(type)` - Combine two sequential patches
 * - `invertFor(type)` - Invert a patch
 *
 * @module
 */

// Re-export types for public API
export {
  type PatchTypeOf,
  ConflictError,
} from "./types.js";

// Re-export PatchType constructor
export { PatchType } from "./type_of_patch.js";
