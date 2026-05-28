/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { ArrayType, none, some, variant } from '@elaraai/east';
import type { ExecutionStatus } from '@elaraai/e3-types';
import {
  workspaceListTasks,
  workspaceGetTask,
  workspaceGetTaskHash,
  executionListForTask,
  executionGet,
} from '@elaraai/e3-core';
import type { StorageBackend } from '@elaraai/e3-core';
import { sendSuccess, sendError } from '../beast2.js';
import { errorToVariant } from '../errors.js';
import { TaskInfoType, TaskDetailsType, ExecutionListItemType, type ExecutionListItem } from '../types.js';

/**
 * List all tasks in a workspace.
 */
export async function listTasks(
  storage: StorageBackend,
  repoPath: string,
  workspace: string
): Promise<Response> {
  try {
    const taskNames = await workspaceListTasks(storage, repoPath, workspace);

    // Get hash for each task
    const result = await Promise.all(
      taskNames.map(async (name) => {
        const hash = await workspaceGetTaskHash(storage, repoPath, workspace, name);
        return { name, hash };
      })
    );

    return sendSuccess(ArrayType(TaskInfoType), result);
  } catch (err) {
    return sendError(ArrayType(TaskInfoType), errorToVariant(err));
  }
}

/**
 * Get task details.
 */
export async function getTask(
  storage: StorageBackend,
  repoPath: string,
  workspace: string,
  taskName: string
): Promise<Response> {
  try {
    const hash = await workspaceGetTaskHash(storage, repoPath, workspace, taskName);
    const task = await workspaceGetTask(storage, repoPath, workspace, taskName);

    return sendSuccess(TaskDetailsType, {
      name: taskName,
      hash,
      commandIr: task.commandIr,
      inputs: task.inputs,
      output: task.output,
    });
  } catch (err) {
    return sendError(TaskDetailsType, errorToVariant(err));
  }
}

/**
 * Convert ExecutionStatus to API ExecutionHistoryStatus variant.
 */
function statusToApiStatus(status: ExecutionStatus): ExecutionListItem['status'] {
  switch (status.type) {
    case 'running':
      return variant('running', null);
    case 'success':
      return variant('success', null);
    case 'failed':
      return variant('failed', null);
    case 'error':
      return variant('error', null);
  }
}

/**
 * Calculate duration in milliseconds between two dates.
 */
function calculateDuration(startedAt: Date, completedAt: Date): bigint {
  return BigInt(Math.round(completedAt.getTime() - startedAt.getTime()));
}

/**
 * List execution history for a task.
 */
export async function listExecutions(
  storage: StorageBackend,
  repoPath: string,
  workspace: string,
  taskName: string
): Promise<Response> {
  try {
    const taskHash = await workspaceGetTaskHash(storage, repoPath, workspace, taskName);
    const inputsHashes = await executionListForTask(storage, repoPath, taskHash);

    const result: ExecutionListItem[] = [];

    for (const inputsHash of inputsHashes) {
      const status = await executionGet(storage, repoPath, taskHash, inputsHash);
      if (!status) continue;

      // Build the complete item based on status type
      let item: ExecutionListItem;
      if (status.type === 'success') {
        item = {
          inputsHash,
          inputHashes: status.value.inputHashes,
          status: statusToApiStatus(status),
          startedAt: status.value.startedAt.toISOString(),
          completedAt: some(status.value.completedAt.toISOString()),
          duration: some(calculateDuration(status.value.startedAt, status.value.completedAt)),
          exitCode: none,
        };
      } else if (status.type === 'failed') {
        item = {
          inputsHash,
          inputHashes: status.value.inputHashes,
          status: statusToApiStatus(status),
          startedAt: status.value.startedAt.toISOString(),
          completedAt: some(status.value.completedAt.toISOString()),
          duration: some(calculateDuration(status.value.startedAt, status.value.completedAt)),
          exitCode: some(status.value.exitCode),
        };
      } else if (status.type === 'error') {
        item = {
          inputsHash,
          inputHashes: status.value.inputHashes,
          status: statusToApiStatus(status),
          startedAt: status.value.startedAt.toISOString(),
          completedAt: some(status.value.completedAt.toISOString()),
          duration: none,
          exitCode: none,
        };
      } else {
        // running status
        item = {
          inputsHash,
          inputHashes: status.value.inputHashes,
          status: statusToApiStatus(status),
          startedAt: status.value.startedAt.toISOString(),
          completedAt: none,
          duration: none,
          exitCode: none,
        };
      }

      result.push(item);
    }

    return sendSuccess(ArrayType(ExecutionListItemType), result);
  } catch (err) {
    return sendError(ArrayType(ExecutionListItemType), errorToVariant(err));
  }
}
