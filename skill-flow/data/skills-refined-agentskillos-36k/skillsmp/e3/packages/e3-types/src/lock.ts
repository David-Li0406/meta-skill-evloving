/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Lock state type definitions.
 *
 * A lock provides exclusive access to a workspace. The state tracks:
 * - What operation acquired the lock (dataflow, deployment, etc.)
 * - Who holds the lock (East text-encoded string)
 * - When it was acquired
 * - Optional expiry (for cloud TTL-based locks)
 *
 * Lock file location: workspaces/<name>.lock
 *
 * The holder field is an East text-encoded string, allowing different backends
 * to encode their own holder identification. Common patterns:
 * - Local: `.process (pid=1234, bootId="abc-123", startTime=98765, command="e3 start")`
 * - Cloud: `.lambda (requestId="req-123", functionName="e3-api")`
 */

import {
  VariantType,
  StructType,
  StringType,
  IntegerType,
  DateTimeType,
  OptionType,
  NullType,
  ValueTypeOf,
} from '@elaraai/east';

/**
 * Lock operation - what acquired the lock.
 */
export const LockOperationType = VariantType({
  /** Running a dataflow */
  dataflow: NullType,
  /** Deploying a package to the workspace */
  deployment: NullType,
  /** Removing the workspace */
  removal: NullType,
  /** Writing to a dataset */
  dataset_write: NullType,
});

export type LockOperation = ValueTypeOf<typeof LockOperationType>;

/**
 * Process holder schema - for local filesystem backends.
 * Used to encode/decode the holder string.
 */
export const ProcessHolderType = StructType({
  /** Process ID */
  pid: IntegerType,
  /** System boot ID (from /proc/sys/kernel/random/boot_id) */
  bootId: StringType,
  /** Process start time in jiffies since boot */
  startTime: IntegerType,
  /** Command that acquired the lock (for debugging) */
  command: StringType,
});

export type ProcessHolder = ValueTypeOf<typeof ProcessHolderType>;

/**
 * Lock state stored in workspaces/<name>.lock
 *
 * Represents an advisory lock on a workspace. The actual locking mechanism
 * is platform-specific (flock on Linux, DynamoDB conditional writes in cloud),
 * but the lock content follows this schema.
 *
 * The holder field is an East text-encoded string representing a variant value.
 * Use `printFor`/`parseInferred` from @elaraai/east to encode/decode.
 */
export const LockStateType = StructType({
  /** What operation acquired the lock */
  operation: LockOperationType,
  /** Who holds the lock - East text-encoded variant (e.g., `.process (...)`) */
  holder: StringType,
  /** When the lock was acquired */
  acquiredAt: DateTimeType,
  /** When the lock expires (for cloud TTL-based locks) */
  expiresAt: OptionType(DateTimeType),
});

export type LockState = ValueTypeOf<typeof LockStateType>;
