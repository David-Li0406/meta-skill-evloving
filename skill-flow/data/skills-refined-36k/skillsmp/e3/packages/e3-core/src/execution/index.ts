/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Execution abstraction layer for e3 dataflow.
 *
 * This module provides interfaces that separate orchestration from business
 * logic, enabling different execution strategies:
 * - LocalDataflowExecutor: In-process execution with AsyncMutex (CLI, local dev)
 * - StepFunctionsDataflowExecutor: AWS Step Functions orchestration (cloud)
 */

export {
  // Task execution
  type TaskExecuteOptions,
  type TaskResult,
  type TaskRunner,
  // Dataflow orchestration
  type ExecutionHandle,
  type DataflowStatus,
  type DataflowExecuteOptions,
  type DataflowExecuteResult,
  type DataflowExecutor,
  // Task graph
  type TaskGraph,
  // Business logic function types
  type DataflowGetGraphFn,
  type DataflowCheckCacheFn,
  type DataflowWriteOutputFn,
  type DataflowGetReadyTasksFn,
} from './interfaces.js';
