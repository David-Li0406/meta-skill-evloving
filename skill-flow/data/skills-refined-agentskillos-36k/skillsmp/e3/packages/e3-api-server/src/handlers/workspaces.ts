/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import * as fs from 'node:fs/promises';
import * as os from 'node:os';
import * as path from 'node:path';
import { BlobType, NullType, some, none, variant } from '@elaraai/east';
import { ArrayType } from '@elaraai/east';
import { WorkspaceStateType, parsePackageRef } from '@elaraai/e3-types';
import {
  workspaceList,
  workspaceCreate,
  workspaceRemove,
  workspaceGetState,
  workspaceDeploy,
  workspaceExport,
  workspaceStatus,
  packageGetLatestVersion,
} from '@elaraai/e3-core';
import type { StorageBackend } from '@elaraai/e3-core';
import { sendSuccess, sendError } from '../beast2.js';
import { errorToVariant } from '../errors.js';
import { WorkspaceInfoType, WorkspaceStatusResultType } from '../types.js';

/**
 * List all workspaces in the repository.
 */
export async function listWorkspaces(
  storage: StorageBackend,
  repoPath: string
): Promise<Response> {
  try {
    const workspaces = await workspaceList(storage, repoPath);
    const result = await Promise.all(
      workspaces.map(async (name) => {
        const state = await workspaceGetState(storage, repoPath, name);
        if (state) {
          return {
            name,
            deployed: true,
            packageName: some(state.packageName),
            packageVersion: some(state.packageVersion),
          };
        } else {
          return {
            name,
            deployed: false,
            packageName: none,
            packageVersion: none,
          };
        }
      })
    );
    return sendSuccess(ArrayType(WorkspaceInfoType), result);
  } catch (err) {
    return sendError(ArrayType(WorkspaceInfoType), errorToVariant(err));
  }
}

/**
 * Create a new workspace.
 */
export async function createWorkspace(
  storage: StorageBackend,
  repoPath: string,
  name: string
): Promise<Response> {
  try {
    await workspaceCreate(storage, repoPath, name);
    return sendSuccess(WorkspaceInfoType, {
      name,
      deployed: false,
      packageName: none,
      packageVersion: none,
    });
  } catch (err) {
    return sendError(WorkspaceInfoType, errorToVariant(err));
  }
}

/**
 * Get workspace state.
 */
export async function getWorkspace(
  storage: StorageBackend,
  repoPath: string,
  name: string
): Promise<Response> {
  try {
    const state = await workspaceGetState(storage, repoPath, name);
    if (!state) {
      return sendError(WorkspaceStateType, errorToVariant(new Error(`Workspace '${name}' is not deployed`)));
    }
    return sendSuccess(WorkspaceStateType, state);
  } catch (err) {
    return sendError(WorkspaceStateType, errorToVariant(err));
  }
}

/**
 * Get comprehensive workspace status.
 */
export async function getWorkspaceStatus(
  storage: StorageBackend,
  repoPath: string,
  name: string
): Promise<Response> {
  try {
    const status = await workspaceStatus(storage, repoPath, name);
    // Convert numbers to bigints for BEAST2 serialization
    const result = {
      workspace: status.workspace,
      lock: status.lock ? some({
        pid: BigInt(status.lock.pid ?? 0),
        acquiredAt: status.lock.acquiredAt,
        bootId: status.lock.bootId ? some(status.lock.bootId) : none,
        command: status.lock.command ? some(status.lock.command) : none,
      }) : none,
      datasets: status.datasets.map(d => ({
        path: d.path,
        status: convertDatasetStatus(d.status),
        hash: d.hash ? some(d.hash) : none,
        isTaskOutput: d.isTaskOutput,
        producedBy: d.producedBy ? some(d.producedBy) : none,
      })),
      tasks: status.tasks.map(t => ({
        name: t.name,
        hash: t.hash,
        status: convertTaskStatus(t.status),
        inputs: t.inputs,
        output: t.output,
        dependsOn: t.dependsOn,
      })),
      summary: {
        datasets: {
          total: BigInt(status.summary.datasets.total),
          unset: BigInt(status.summary.datasets.unset),
          stale: BigInt(status.summary.datasets.stale),
          upToDate: BigInt(status.summary.datasets.upToDate),
        },
        tasks: {
          total: BigInt(status.summary.tasks.total),
          upToDate: BigInt(status.summary.tasks.upToDate),
          ready: BigInt(status.summary.tasks.ready),
          waiting: BigInt(status.summary.tasks.waiting),
          inProgress: BigInt(status.summary.tasks.inProgress),
          failed: BigInt(status.summary.tasks.failed),
          error: BigInt(status.summary.tasks.error),
          staleRunning: BigInt(status.summary.tasks.staleRunning),
        },
      },
    };
    return sendSuccess(WorkspaceStatusResultType, result);
  } catch (err) {
    return sendError(WorkspaceStatusResultType, errorToVariant(err));
  }
}

// Helper to convert dataset status to variant format
function convertDatasetStatus(status: { type: string }) {
  switch (status.type) {
    case 'unset': return variant('unset', null);
    case 'stale': return variant('stale', null);
    case 'up-to-date': return variant('up-to-date', null);
    default: return variant('unset', null);
  }
}

// Helper to convert task status to variant format
function convertTaskStatus(status: any) {
  switch (status.type) {
    case 'up-to-date':
      return variant('up-to-date', { cached: status.cached });
    case 'ready':
      return variant('ready', null);
    case 'waiting':
      return variant('waiting', { reason: status.reason });
    case 'in-progress':
      return variant('in-progress', {
        pid: status.pid != null ? some(BigInt(status.pid)) : none,
        startedAt: status.startedAt ? some(status.startedAt) : none,
      });
    case 'failed':
      return variant('failed', {
        exitCode: BigInt(status.exitCode),
        completedAt: status.completedAt ? some(status.completedAt) : none,
      });
    case 'error':
      return variant('error', {
        message: status.message,
        completedAt: status.completedAt ? some(status.completedAt) : none,
      });
    case 'stale-running':
      return variant('stale-running', {
        pid: status.pid != null ? some(BigInt(status.pid)) : none,
        startedAt: status.startedAt ? some(status.startedAt) : none,
      });
    default:
      return variant('ready', null);
  }
}

/**
 * Delete a workspace.
 */
export async function deleteWorkspace(
  storage: StorageBackend,
  repoPath: string,
  name: string
): Promise<Response> {
  try {
    await workspaceRemove(storage, repoPath, name);
    return sendSuccess(NullType, null);
  } catch (err) {
    return sendError(NullType, errorToVariant(err));
  }
}

/**
 * Deploy a package to a workspace.
 */
export async function deployWorkspace(
  storage: StorageBackend,
  repoPath: string,
  workspace: string,
  packageRef: string
): Promise<Response> {
  try {
    const { name: pkgName, version: maybeVersion } = parsePackageRef(packageRef);
    const pkgVersion = maybeVersion ?? await packageGetLatestVersion(storage, repoPath, pkgName);
    if (!pkgVersion) {
      return sendError(NullType, errorToVariant(new Error(`Package not found: ${pkgName}`)));
    }

    await workspaceDeploy(storage, repoPath, workspace, pkgName, pkgVersion);
    return sendSuccess(NullType, null);
  } catch (err) {
    return sendError(NullType, errorToVariant(err));
  }
}

/**
 * Export a workspace as a zip archive.
 */
export async function exportWorkspace(
  storage: StorageBackend,
  repoPath: string,
  workspace: string
): Promise<Response> {
  try {
    // Export to temp file
    const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'e3-ws-export-'));
    const tempPath = path.join(tempDir, 'workspace.zip');
    try {
      await workspaceExport(storage, repoPath, workspace, tempPath);
      const archive = await fs.readFile(tempPath);
      return sendSuccess(BlobType, new Uint8Array(archive));
    } finally {
      await fs.rm(tempDir, { recursive: true, force: true });
    }
  } catch (err) {
    return sendError(BlobType, errorToVariant(err));
  }
}
