/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Execution status type definitions.
 *
 * An execution represents a single run of a task with specific inputs.
 * Executions are stored at: executions/<taskHash>/<inputsHash>/
 *
 * The status file tracks:
 * - For running: process identification for crash detection
 * - For success: output hash and timing
 * - For failed: exit code and timing
 * - For error: internal error message and timing
 */

import {
  VariantType,
  StructType,
  ArrayType,
  StringType,
  IntegerType,
  DateTimeType,
  ValueTypeOf,
} from '@elaraai/east';

/**
 * Execution status stored in executions/<taskHash>/<inputsHash>/status.beast2
 *
 * A variant type representing the four possible states of an execution:
 *
 * - `running`: Task has been launched but not yet completed
 * - `success`: Task ran and returned exit code 0
 * - `failed`: Task ran and returned non-zero exit code
 * - `error`: e3 execution engine had an internal error (runner not found, output missing, etc.)
 *
 * The `running` state includes process identification fields (pid, pidStartTime, bootId)
 * to enable detection of crashed executions. See design/e3-execution.md for details.
 */
export const ExecutionStatusType = VariantType({
  /** Task has been launched but not yet completed */
  running: StructType({
    /** Input dataset hashes */
    inputHashes: ArrayType(StringType),
    /** When execution started */
    startedAt: DateTimeType,
    /** Process ID of the runner */
    pid: IntegerType,
    /** Process start time in jiffies since boot (from /proc/<pid>/stat field 22) */
    pidStartTime: IntegerType,
    /** System boot ID (from /proc/sys/kernel/random/boot_id) */
    bootId: StringType,
  }),
  /** Task ran and returned exit code 0 */
  success: StructType({
    /** Input dataset hashes */
    inputHashes: ArrayType(StringType),
    /** Hash of the output dataset */
    outputHash: StringType,
    /** When execution started */
    startedAt: DateTimeType,
    /** When execution completed */
    completedAt: DateTimeType,
  }),
  /** Task ran and returned non-zero exit code */
  failed: StructType({
    /** Input dataset hashes */
    inputHashes: ArrayType(StringType),
    /** When execution started */
    startedAt: DateTimeType,
    /** When execution completed */
    completedAt: DateTimeType,
    /** Process exit code */
    exitCode: IntegerType,
  }),
  /** e3 execution engine had an internal error */
  error: StructType({
    /** Input dataset hashes */
    inputHashes: ArrayType(StringType),
    /** When execution started */
    startedAt: DateTimeType,
    /** When execution completed */
    completedAt: DateTimeType,
    /** Error message describing what went wrong */
    message: StringType,
  }),
});

export type ExecutionStatus = ValueTypeOf<typeof ExecutionStatusType>;
