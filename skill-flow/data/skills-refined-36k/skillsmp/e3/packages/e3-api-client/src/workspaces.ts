/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { ArrayType, BlobType, NullType } from '@elaraai/east';
import { WorkspaceStateType, type WorkspaceState } from '@elaraai/e3-types';
import type { WorkspaceInfo, WorkspaceStatusResult } from './types.js';
import {
  WorkspaceInfoType,
  WorkspaceCreateRequestType,
  WorkspaceDeployRequestType,
  WorkspaceStatusResultType,
} from './types.js';
import { get, post, del, unwrap, type RequestOptions } from './http.js';

/**
 * List all workspaces in the repository.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param options - Request options including auth token
 * @returns Array of workspace info
 */
export async function workspaceList(url: string, repo: string, options: RequestOptions): Promise<WorkspaceInfo[]> {
  const response = await get(url, `/repos/${encodeURIComponent(repo)}/workspaces`, ArrayType(WorkspaceInfoType), options);
  return unwrap(response);
}

/**
 * Create a new empty workspace.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param name - Workspace name
 * @param options - Request options including auth token
 * @returns Created workspace info
 */
export async function workspaceCreate(url: string, repo: string, name: string, options: RequestOptions): Promise<WorkspaceInfo> {
  const response = await post(
    url,
    `/repos/${encodeURIComponent(repo)}/workspaces`,
    { name },
    WorkspaceCreateRequestType,
    WorkspaceInfoType,
    options
  );
  return unwrap(response);
}

/**
 * Get workspace state (deployed package info and current root hash).
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param name - Workspace name
 * @param options - Request options including auth token
 * @returns Workspace state
 */
export async function workspaceGet(url: string, repo: string, name: string, options: RequestOptions): Promise<WorkspaceState> {
  const response = await get(
    url,
    `/repos/${encodeURIComponent(repo)}/workspaces/${encodeURIComponent(name)}`,
    WorkspaceStateType,
    options
  );
  return unwrap(response);
}

/**
 * Get comprehensive workspace status including datasets, tasks, and lock info.
 *
 * Use this to poll for execution progress after calling dataflowStart().
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param name - Workspace name
 * @param options - Request options including auth token
 * @returns Workspace status with datasets, tasks, and summary
 */
export async function workspaceStatus(url: string, repo: string, name: string, options: RequestOptions): Promise<WorkspaceStatusResult> {
  const response = await get(
    url,
    `/repos/${encodeURIComponent(repo)}/workspaces/${encodeURIComponent(name)}/status`,
    WorkspaceStatusResultType,
    options
  );
  return unwrap(response);
}

/**
 * Remove a workspace.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param name - Workspace name
 * @param options - Request options including auth token
 */
export async function workspaceRemove(url: string, repo: string, name: string, options: RequestOptions): Promise<void> {
  const response = await del(
    url,
    `/repos/${encodeURIComponent(repo)}/workspaces/${encodeURIComponent(name)}`,
    NullType,
    options
  );
  unwrap(response);
}

/**
 * Deploy a package to a workspace.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param name - Workspace name
 * @param packageRef - Package reference (name or name@version)
 * @param options - Request options including auth token
 */
export async function workspaceDeploy(
  url: string,
  repo: string,
  name: string,
  packageRef: string,
  options: RequestOptions
): Promise<void> {
  const response = await post(
    url,
    `/repos/${encodeURIComponent(repo)}/workspaces/${encodeURIComponent(name)}/deploy`,
    { packageRef },
    WorkspaceDeployRequestType,
    NullType,
    options
  );
  unwrap(response);
}

/**
 * Export workspace as a package zip archive.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param name - Workspace name
 * @param options - Request options including auth token
 * @returns Zip archive as bytes
 */
export async function workspaceExport(url: string, repo: string, name: string, options: RequestOptions): Promise<Uint8Array> {
  const response = await get(
    url,
    `/repos/${encodeURIComponent(repo)}/workspaces/${encodeURIComponent(name)}/export`,
    BlobType,
    options
  );
  return unwrap(response);
}
