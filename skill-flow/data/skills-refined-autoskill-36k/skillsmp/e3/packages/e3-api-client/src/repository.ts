/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { StringType } from '@elaraai/east';
import type {
  RepositoryStatus,
  GcRequest,
  GcResult,
  GcStartResult,
  GcStatusResult,
  RepoDeleteStartResult,
  RepoDeleteStatusResult,
} from './types.js';
import {
  RepositoryStatusType,
  GcRequestType,
  GcStartResultType,
  GcStatusResultType,
  RepoDeleteStartResultType,
  RepoDeleteStatusResultType,
} from './types.js';
import { get, post, del, putEmpty, unwrap, type RequestOptions } from './http.js';

/**
 * Get repository status.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param options - Request options including auth token
 * @returns Repository status including object, package, and workspace counts
 */
export async function repoStatus(url: string, repo: string, options: RequestOptions): Promise<RepositoryStatus> {
  const response = await get(url, `/repos/${encodeURIComponent(repo)}/status`, RepositoryStatusType, options);
  return unwrap(response);
}

/**
 * Start garbage collection (async).
 *
 * Returns immediately with an executionId. Use repoGcStatus() to poll for completion.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param gcOptions - GC options (dryRun to preview without deleting)
 * @param options - Request options including auth token
 * @returns GC start result with executionId
 */
export async function repoGcStart(url: string, repo: string, gcOptions: GcRequest, options: RequestOptions): Promise<GcStartResult> {
  const response = await post(url, `/repos/${encodeURIComponent(repo)}/gc`, gcOptions, GcRequestType, GcStartResultType, options);
  return unwrap(response);
}

/**
 * Get garbage collection status.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param executionId - Execution ID from repoGcStart()
 * @param options - Request options including auth token
 * @returns GC status with stats when complete
 */
export async function repoGcStatus(url: string, repo: string, executionId: string, options: RequestOptions): Promise<GcStatusResult> {
  const response = await get(
    url,
    `/repos/${encodeURIComponent(repo)}/gc/${encodeURIComponent(executionId)}`,
    GcStatusResultType,
    options
  );
  return unwrap(response);
}

/**
 * Run garbage collection and wait for completion (convenience wrapper).
 *
 * Starts GC and polls until complete. Throws on error.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param gcOptions - GC options (dryRun to preview without deleting)
 * @param options - Request options including auth token
 * @param pollOptions - Polling options (interval in ms, default 500)
 * @returns GC result with counts and freed bytes
 */
export async function repoGc(
  url: string,
  repo: string,
  gcOptions: GcRequest,
  options: RequestOptions,
  pollOptions: { pollInterval?: number } = {}
): Promise<GcResult> {
  const pollInterval = pollOptions.pollInterval ?? 500;

  // Start GC
  const { executionId } = await repoGcStart(url, repo, gcOptions, options);

  // Poll until complete
  while (true) {
    const status = await repoGcStatus(url, repo, executionId, options);

    if (status.status.type === 'succeeded') {
      if (status.stats.type !== 'some') {
        throw new Error('GC succeeded but no stats returned');
      }
      return status.stats.value;
    }

    if (status.status.type === 'failed') {
      const errorMsg = status.error.type === 'some' ? status.error.value : 'Unknown error';
      throw new Error(`GC failed: ${errorMsg}`);
    }

    // Still running, wait and poll again
    await new Promise(resolve => setTimeout(resolve, pollInterval));
  }
}

/**
 * Create a new repository.
 *
 * @param url - Base URL of the e3 API server
 * @param name - Name for the new repository
 * @param options - Request options including auth token
 * @returns The created repository name
 */
export async function repoCreate(url: string, name: string, options: RequestOptions): Promise<string> {
  const response = await putEmpty(url, `/repos/${encodeURIComponent(name)}`, StringType, options);
  return unwrap(response);
}

/**
 * Start repository deletion (async).
 *
 * Returns immediately with an executionId. Use repoRemoveStatus() to poll for completion.
 *
 * @param url - Base URL of the e3 API server
 * @param name - Repository name to remove
 * @param options - Request options including auth token
 * @returns Delete start result with executionId
 */
export async function repoRemoveStart(url: string, name: string, options: RequestOptions): Promise<RepoDeleteStartResult> {
  const response = await del(url, `/repos/${encodeURIComponent(name)}`, RepoDeleteStartResultType, options);
  return unwrap(response);
}

/**
 * Get repository deletion status.
 *
 * @param url - Base URL of the e3 API server
 * @param name - Repository name being deleted
 * @param executionId - Execution ID from repoRemoveStart()
 * @param options - Request options including auth token
 * @returns Delete status
 */
export async function repoRemoveStatus(url: string, name: string, executionId: string, options: RequestOptions): Promise<RepoDeleteStatusResult> {
  const response = await get(
    url,
    `/repos/${encodeURIComponent(name)}/delete/${encodeURIComponent(executionId)}`,
    RepoDeleteStatusResultType,
    options
  );
  return unwrap(response);
}

/**
 * Remove a repository and wait for completion (convenience wrapper).
 *
 * Starts deletion and polls until complete. Throws on error.
 *
 * @param url - Base URL of the e3 API server
 * @param name - Repository name to remove
 * @param options - Request options including auth token
 * @param pollOptions - Polling options (interval in ms, default 500)
 */
export async function repoRemove(
  url: string,
  name: string,
  options: RequestOptions,
  pollOptions: { pollInterval?: number } = {}
): Promise<void> {
  const pollInterval = pollOptions.pollInterval ?? 500;

  // Start deletion
  const { executionId } = await repoRemoveStart(url, name, options);

  // Poll until complete
  while (true) {
    const status = await repoRemoveStatus(url, name, executionId, options);

    if (status.status.type === 'succeeded') {
      return;
    }

    if (status.status.type === 'failed') {
      const errorMsg = status.error.type === 'some' ? status.error.value : 'Unknown error';
      throw new Error(`Repo deletion failed: ${errorMsg}`);
    }

    // Still running, wait and poll again
    await new Promise(resolve => setTimeout(resolve, pollInterval));
  }
}
