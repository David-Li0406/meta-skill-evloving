/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Dataset platform function signatures for reading/writing e3 datasets.
 *
 * @remarks
 * This module contains only platform function definitions created with `East.platform()`.
 * All runtime implementations are in `@elaraai/east-ui-components`.
 *
 * @packageDocumentation
 */

import { East, StringType, NullType, BooleanType, ArrayType, IntegerType, VariantType } from "@elaraai/east";

/**
 * Path segment type for dataset paths.
 * Uses field variant for struct field access.
 */
export const DatasetPathSegmentType = VariantType({
    field: StringType,
});

/**
 * Dataset path type - array of path segments.
 */
export const DatasetPathType = ArrayType(DatasetPathSegmentType);

/**
 * Reads a typed value from an e3 dataset.
 *
 * @typeParam T - The East type of the dataset value
 * @param workspace - The workspace name
 * @param path - The dataset path as array of field segments
 * @returns The decoded dataset value
 *
 * @remarks
 * - Tracks the dataset path for reactive updates within `Reactive.Root`
 * - Returns cached value if available
 * - Throws if dataset not found or not yet loaded
 *
 * Implementation provided by `ReactiveDatasetPlatform` in `@elaraai/east-ui-components`.
 *
 * @example
 * ```ts
 * import { ReactiveDataset } from "@elaraai/east-ui";
 * import { variant, IntegerType } from "@elaraai/east";
 *
 * const value = ReactiveDataset.get(
 *     [IntegerType],
 *     "production",
 *     [variant("field", "inputs"), variant("field", "count")]
 * );
 * ```
 */
export const reactive_dataset_get = East.genericPlatform(
    "reactive_dataset_get",
    ["T"],
    [StringType, DatasetPathType],  // workspace, path
    "T",
    {
        optional: true
    }
);

/**
 * Writes a typed value to an e3 dataset.
 *
 * @typeParam T - The East type of the value
 * @param workspace - The workspace name
 * @param path - The dataset path as array of field segments
 * @param value - The value to write
 * @returns Null
 *
 * @remarks
 * - Encodes value as BEAST2 and sends to e3
 * - Invalidates cached data and triggers re-renders in reactive components
 * - Throws if write fails
 *
 * Implementation provided by `ReactiveDatasetPlatform` in `@elaraai/east-ui-components`.
 */
export const reactive_dataset_set = East.genericPlatform(
    "reactive_dataset_set",
    ["T"],
    [StringType, DatasetPathType, "T"],  // workspace, path, value
    NullType,
    {
        optional: true
    }
);

/**
 * Checks if a dataset exists and has a value.
 *
 * @param workspace - The workspace name
 * @param path - The dataset path as array of field segments
 * @returns Boolean indicating whether the dataset exists and is assigned
 *
 * @remarks
 * Implementation provided by `ReactiveDatasetPlatform` in `@elaraai/east-ui-components`.
 */
export const reactive_dataset_has = East.platform(
    "reactive_dataset_has",
    [StringType, DatasetPathType],  // workspace, path
    BooleanType,
    {
        optional: true
    }
);

/**
 * Lists field names at a dataset path.
 *
 * @param workspace - The workspace name
 * @param path - The parent path (empty array for root)
 * @returns Array of field names
 *
 * @remarks
 * Implementation provided by `ReactiveDatasetPlatform` in `@elaraai/east-ui-components`.
 */
export const reactive_dataset_list = East.platform(
    "reactive_dataset_list",
    [StringType, DatasetPathType],  // workspace, path
    ArrayType(StringType),
    {
        optional: true
    }
);

/**
 * Subscribes to dataset changes with polling.
 *
 * @param workspace - The workspace name
 * @param path - The dataset path as array of field segments
 * @param intervalMs - Polling interval in milliseconds
 * @returns Null (subscription is implicit)
 *
 * @remarks
 * - Enables automatic refetching at the specified interval
 * - Useful for datasets that may be updated by external processes (e.g., task outputs)
 * - Changes will trigger re-renders in reactive components that read the dataset
 *
 * Implementation provided by `ReactiveDatasetPlatform` in `@elaraai/east-ui-components`.
 */
export const reactive_dataset_subscribe = East.platform(
    "reactive_dataset_subscribe",
    [StringType, DatasetPathType, IntegerType],  // workspace, path, intervalMs
    NullType,
    {
        optional: true
    }
);
