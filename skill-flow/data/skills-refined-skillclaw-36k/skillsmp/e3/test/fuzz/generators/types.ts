/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Random East type generation for fuzz testing.
 *
 * Re-exports and extends the randomType from @elaraai/east/internal
 * with e3-specific preferences.
 */

import {
  type EastType,
  IntegerType,
  FloatType,
  StringType,
  BooleanType,
  ArrayType,
  StructType,
  OptionType,
} from '@elaraai/east';
import { randomType as eastRandomType } from '@elaraai/east/internal';
import { random } from '../helpers.js';

// Re-export the East randomType for direct use
export { eastRandomType as randomType };

export interface TypeGenConfig {
  maxDepth?: number;
  preferPrimitives?: boolean;
  includeBlob?: boolean;
  includeDateTime?: boolean;
}

/**
 * Generate a random East type biased towards types commonly used in e3 packages.
 *
 * Uses the East library's randomType internally but with e3-specific weighting:
 * - Higher weight on Integer, Float, String
 * - Struct types for complex data
 * - Arrays for collections
 */
export function randomE3Type(config: TypeGenConfig = {}): EastType {
  // 60% chance of using a "common" type pattern
  if (random.next() < 0.6) {
    return randomCommonType();
  }

  // 40% chance of using East's full randomType
  // Pass depth to control complexity
  return eastRandomType(config.maxDepth ?? 2, { includeRecursive: false, includeFunctions: false });
}

/**
 * Common type patterns used in e3 packages
 */
export const commonTypes = {
  // Simple scalars
  integer: IntegerType,
  float: FloatType,
  string: StringType,
  boolean: BooleanType,

  // Common collections
  integerArray: ArrayType(IntegerType),
  floatArray: ArrayType(FloatType),
  stringArray: ArrayType(StringType),

  // Common records
  point2d: StructType({ x: FloatType, y: FloatType }),
  point3d: StructType({ x: FloatType, y: FloatType, z: FloatType }),
  namedValue: StructType({ name: StringType, value: FloatType }),

  // Optional types
  optionalInteger: OptionType(IntegerType),
  optionalString: OptionType(StringType),
};

/**
 * Get a random "common" type that's frequently used in real packages
 */
export function randomCommonType(): EastType {
  const types = Object.values(commonTypes);
  return random.pick(types);
}

