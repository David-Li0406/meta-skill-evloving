/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Random value generation for East types.
 *
 * Uses the randomValueFor and equalFor from @elaraai/east/internal
 */

import type { EastType, ValueTypeOf } from '@elaraai/east';
import { equalFor, printFor } from '@elaraai/east';
import { randomValueFor as eastRandomValueFor } from '@elaraai/east/internal';

// Re-export the East utilities
export { eastRandomValueFor as randomValueFor, equalFor, printFor };

export interface ValueGenConfig {
  /** Max size for collections */
  maxCollectionSize?: number;
  /** Max string length */
  maxStringLength?: number;
}

/**
 * Generate a random value for a given East type.
 * Wrapper around East's randomValueFor that returns a value directly.
 */
export function randomValue<T extends EastType>(
  type: T,
  _config: ValueGenConfig = {}
): ValueTypeOf<T> {
  const generator = eastRandomValueFor(type);
  return generator();
}

/**
 * Generate a new random value that's different from the original.
 * Useful for testing input mutation scenarios.
 */
export function mutateValue<T extends EastType>(
  type: T,
  original: ValueTypeOf<T>,
  config: ValueGenConfig = {}
): ValueTypeOf<T> {
  const isEqual = equalFor(type);

  // Try up to 10 times to generate a different value
  for (let i = 0; i < 10; i++) {
    const newValue = randomValue(type, config);
    if (!isEqual(newValue, original)) {
      return newValue;
    }
  }
  // Fall back to just returning a new value (might be same for simple types like Boolean)
  return randomValue(type, config);
}

/**
 * Check if two values are equal according to their type.
 */
export function valuesEqual<T extends EastType>(
  type: T,
  a: ValueTypeOf<T>,
  b: ValueTypeOf<T>
): boolean {
  const isEqual = equalFor(type);
  return isEqual(a, b);
}

/**
 * Format a value as a string for debugging/logging.
 */
export function formatValue<T extends EastType>(
  type: T,
  value: ValueTypeOf<T>
): string {
  const print = printFor(type);
  return print(value);
}
