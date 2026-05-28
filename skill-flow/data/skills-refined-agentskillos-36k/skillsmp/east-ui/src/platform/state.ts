/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * State management platform function signatures.
 *
 * @remarks
 * This module contains only platform function definitions created with `East.platform()`.
 * All runtime implementations are in `@elaraai/east-ui-components`.
 *
 * @packageDocumentation
 */

import { East, StringType, NullType, BooleanType } from "@elaraai/east";

/**
 * Reads a Beast2-encoded value from state storage.
 *
 * @param key - The state key to read from
 * @returns Option of Beast2-encoded blob (some if exists, none if not found)
 *
 * @remarks
 * Returns `none` if the key does not exist, `some(blob)` if it does.
 * Implementation provided by `StateImpl` in `@elaraai/east-ui-components`.
 */
export const state_read = East.genericPlatform(
    "state_read", 
    ["T"],
    [StringType], 
    "T",
    {
        optional: true
    }
);

/**
 * Writes a Beast2-encoded value to state storage.
 *
 * @param key - The state key to write to
 * @param value - The value to write (some to set, none to delete)
 * @returns Null
 *
 * @remarks
 * Pass `none` to delete the key from state.
 * Implementation provided by `StateImpl` in `@elaraai/east-ui-components`.
 */
export const state_write = East.genericPlatform(
    "state_write", 
    ["T"],
    [StringType, "T"], 
    NullType,
    {
        optional: true
    }
);

/**
 * Checks if a key exists in state storage.
 *
 * @param key - The state key to check
 * @returns Boolean indicating whether the key exists
 *
 * @remarks
 * Implementation provided by `StateImpl` in `@elaraai/east-ui-components`.
 */
export const state_has = East.platform(
    "state_has", 
    [StringType], 
    BooleanType,
    {
        optional: true
    }
);
