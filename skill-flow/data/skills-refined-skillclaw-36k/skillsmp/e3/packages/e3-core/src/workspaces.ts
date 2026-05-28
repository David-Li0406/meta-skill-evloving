/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Workspace operations for e3 repositories.
 *
 * Workspaces are mutable working copies of packages. They allow:
 * - Deploying a package to create a working environment
 * - Modifying data (inputs/outputs)
 * - Exporting changes back to a new package version
 *
 * State is stored in workspaces/<name>.beast2 as a single atomic file.
 * No state file means the workspace does not exist.
 */

import { createWriteStream } from 'fs';
import * as fs from 'fs/promises';
import yazl from 'yazl';
import { decodeBeast2For, encodeBeast2For, variant } from '@elaraai/east';
import { PackageObjectType, WorkspaceStateType } from '@elaraai/e3-types';
import type { PackageObject, WorkspaceState } from '@elaraai/e3-types';
import { packageResolve, packageRead } from './packages.js';
import {
  WorkspaceNotFoundError,
  WorkspaceNotDeployedError,
  WorkspaceExistsError,
  WorkspaceLockError,
} from './errors.js';
import type { StorageBackend, LockHandle } from './storage/interfaces.js';

/**
 * List workspace names.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @returns Array of workspace names
 */
export async function workspaceList(storage: StorageBackend, repo: string): Promise<string[]> {
  return storage.refs.workspaceList(repo);
}

/**
 * Write workspace state via storage backend.
 */
async function writeState(storage: StorageBackend, repo: string, name: string, state: WorkspaceState): Promise<void> {
  const encoder = encodeBeast2For(WorkspaceStateType);
  const data = encoder(state);
  await storage.refs.workspaceWrite(repo, name, data);
}

/**
 * Read workspace state.
 * Returns { exists: false } if workspace doesn't exist.
 * Returns { exists: true, deployed: false } if workspace exists but not deployed.
 * Returns { exists: true, deployed: true, state } if workspace is deployed.
 */
async function readState(
  storage: StorageBackend,
  repo: string,
  name: string
): Promise<
  | { exists: false }
  | { exists: true; deployed: false }
  | { exists: true; deployed: true; state: WorkspaceState }
> {
  const data = await storage.refs.workspaceRead(repo, name);

  if (data === null) {
    return { exists: false };
  }

  // Empty file means workspace exists but is not deployed
  if (data.length === 0) {
    return { exists: true, deployed: false };
  }

  const decoder = decodeBeast2For(WorkspaceStateType);
  return { exists: true, deployed: true, state: decoder(Buffer.from(data)) };
}

/**
 * Read workspace state, throwing if workspace doesn't exist or is not deployed.
 * @throws {WorkspaceNotFoundError} If workspace doesn't exist
 * @throws {WorkspaceNotDeployedError} If workspace exists but has no package deployed
 */
async function readStateOrThrow(storage: StorageBackend, repo: string, name: string): Promise<WorkspaceState> {
  const result = await readState(storage, repo, name);
  if (!result.exists) {
    throw new WorkspaceNotFoundError(name);
  }
  if (!result.deployed) {
    throw new WorkspaceNotDeployedError(name);
  }
  return result.state;
}


/**
 * Create an empty workspace.
 *
 * Creates an undeployed workspace (state file with null package info).
 * Use workspaceDeploy to deploy a package.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param name - Workspace name
 * @throws {WorkspaceExistsError} If workspace already exists
 */
export async function workspaceCreate(
  storage: StorageBackend,
  repo: string,
  name: string
): Promise<void> {
  // Check if workspace already exists
  const existing = await storage.refs.workspaceRead(repo, name);
  if (existing !== null) {
    throw new WorkspaceExistsError(name);
  }

  // Create empty state to mark workspace as existing but not deployed
  await storage.refs.workspaceWrite(repo, name, new Uint8Array(0));
}

/**
 * Options for workspace removal.
 */
export interface WorkspaceRemoveOptions {
  /**
   * External workspace lock to use. If provided, the caller is responsible
   * for releasing the lock after the operation. If not provided, workspaceRemove
   * will acquire and release a lock internally.
   */
  lock?: LockHandle;
}

/**
 * Remove a workspace.
 *
 * Objects remain until repoGc is run.
 *
 * Acquires a workspace lock to prevent removing a workspace while a dataflow
 * is running. Throws WorkspaceLockError if the workspace is currently locked.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param name - Workspace name
 * @param options - Optional settings including external lock
 * @throws {WorkspaceNotFoundError} If workspace doesn't exist
 * @throws {WorkspaceLockError} If workspace is locked by another process
 */
export async function workspaceRemove(
  storage: StorageBackend,
  repo: string,
  name: string,
  options: WorkspaceRemoveOptions = {}
): Promise<void> {
  // Acquire lock if not provided externally
  const externalLock = options.lock;
  let lock: LockHandle | null = externalLock ?? null;
  if (!lock) {
    lock = await storage.locks.acquire(repo, name, variant('removal', null));
    if (!lock) {
      const state = await storage.locks.getState(repo, name);
      throw new WorkspaceLockError(name, state ? {
        acquiredAt: state.acquiredAt.toISOString(),
        operation: state.operation.type,
      } : undefined);
    }
  }
  try {
    // Check if workspace exists
    const existing = await storage.refs.workspaceRead(repo, name);
    if (existing === null) {
      throw new WorkspaceNotFoundError(name);
    }

    await storage.refs.workspaceRemove(repo, name);
  } finally {
    // Only release the lock if we acquired it internally
    if (!externalLock) {
      await lock.release();
    }
  }
}

/**
 * Get the full state for a workspace.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param name - Workspace name
 * @returns Workspace state, or null if workspace doesn't exist or is not deployed
 */
export async function workspaceGetState(
  storage: StorageBackend,
  repo: string,
  name: string
): Promise<WorkspaceState | null> {
  const result = await readState(storage, repo, name);
  if (!result.exists || !result.deployed) {
    return null;
  }
  return result.state;
}

/**
 * Get the deployed package for a workspace.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param name - Workspace name
 * @returns Package name, version, and hash
 * @throws {WorkspaceNotFoundError} If workspace doesn't exist
 * @throws {WorkspaceNotDeployedError} If workspace exists but has no package deployed
 */
export async function workspaceGetPackage(
  storage: StorageBackend,
  repo: string,
  name: string
): Promise<{ name: string; version: string; hash: string }> {
  const state = await readStateOrThrow(storage, repo, name);
  return {
    name: state.packageName,
    version: state.packageVersion,
    hash: state.packageHash,
  };
}

/**
 * Get the root tree hash for a workspace.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param name - Workspace name
 * @returns Root tree object hash
 * @throws {WorkspaceNotFoundError} If workspace doesn't exist
 * @throws {WorkspaceNotDeployedError} If workspace exists but has no package deployed
 */
export async function workspaceGetRoot(
  storage: StorageBackend,
  repo: string,
  name: string
): Promise<string> {
  const state = await readStateOrThrow(storage, repo, name);
  return state.rootHash;
}

/**
 * Atomically update the root tree hash for a workspace.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param name - Workspace name
 * @param hash - New root tree object hash
 * @throws {WorkspaceNotFoundError} If workspace doesn't exist
 * @throws {WorkspaceNotDeployedError} If workspace exists but has no package deployed
 */
export async function workspaceSetRoot(
  storage: StorageBackend,
  repo: string,
  name: string,
  hash: string
): Promise<void> {
  const state = await readStateOrThrow(storage, repo, name);

  const newState: WorkspaceState = {
    ...state,
    rootHash: hash,
    rootUpdatedAt: new Date(),
  };

  await writeState(storage, repo, name, newState);
}

/**
 * Options for workspace deployment.
 */
export interface WorkspaceDeployOptions {
  /**
   * External workspace lock to use. If provided, the caller is responsible
   * for releasing the lock after the operation. If not provided, workspaceDeploy
   * will acquire and release a lock internally.
   */
  lock?: LockHandle;
}

/**
 * Deploy a package to a workspace.
 *
 * Creates the workspace if it doesn't exist. Writes state file atomically
 * containing deployment info and root hash.
 *
 * Acquires a workspace lock to prevent conflicts with running dataflows
 * or concurrent deploys. Throws WorkspaceLockError if the workspace is
 * currently locked by another process.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param name - Workspace name
 * @param pkgName - Package name
 * @param pkgVersion - Package version
 * @param options - Optional settings including external lock
 * @throws {WorkspaceLockError} If workspace is locked by another process
 */
export async function workspaceDeploy(
  storage: StorageBackend,
  repo: string,
  name: string,
  pkgName: string,
  pkgVersion: string,
  options: WorkspaceDeployOptions = {}
): Promise<void> {
  // Acquire lock if not provided externally
  const externalLock = options.lock;
  let lock: LockHandle | null = externalLock ?? null;
  if (!lock) {
    lock = await storage.locks.acquire(repo, name, variant('deployment', null));
    if (!lock) {
      const state = await storage.locks.getState(repo, name);
      throw new WorkspaceLockError(name, state ? {
        acquiredAt: state.acquiredAt.toISOString(),
        operation: state.operation.type,
      } : undefined);
    }
  }
  try {
    // Resolve package hash and read package object
    const packageHash = await packageResolve(storage, repo, pkgName, pkgVersion);
    const pkg = await packageRead(storage, repo, pkgName, pkgVersion);

    const now = new Date();
    const state: WorkspaceState = {
      packageName: pkgName,
      packageVersion: pkgVersion,
      packageHash,
      deployedAt: now,
      rootHash: pkg.data.value,
      rootUpdatedAt: now,
    };

    await writeState(storage, repo, name, state);
  } finally {
    // Only release the lock if we acquired it internally
    if (!externalLock) {
      await lock.release();
    }
  }
}

/**
 * Result of exporting a workspace
 */
export interface WorkspaceExportResult {
  packageHash: string;
  objectCount: number;
  name: string;
  version: string;
}

/**
 * Fixed mtime for deterministic zip output (Unix epoch)
 */
const DETERMINISTIC_MTIME = new Date(0);

/**
 * Export a workspace as a package.
 *
 * 1. Read workspace state
 * 2. Read deployed package structure using stored packageHash
 * 3. Create new PackageObject with data.value set to current rootHash
 * 4. Collect all referenced objects
 * 5. Write to .zip
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param name - Workspace name
 * @param zipPath - Path to write the .zip file
 * @param outputName - Package name (default: deployed package name)
 * @param version - Package version (default: <pkgVersion>-<rootHash[0..8]>)
 * @returns Export result with package info
 * @throws {WorkspaceNotFoundError} If workspace doesn't exist
 * @throws {WorkspaceNotDeployedError} If workspace exists but has no package deployed
 */
export async function workspaceExport(
  storage: StorageBackend,
  repo: string,
  name: string,
  zipPath: string,
  outputName?: string,
  version?: string
): Promise<WorkspaceExportResult> {
  const partialPath = `${zipPath}.partial`;

  // Get workspace state
  const state = await readStateOrThrow(storage, repo, name);

  // Read the deployed package object using the stored hash
  const deployedPkgData = await storage.objects.read(repo, state.packageHash);
  const decoder = decodeBeast2For(PackageObjectType);
  const deployedPkgObject = decoder(Buffer.from(deployedPkgData));

  // Determine output name and version
  const finalName = outputName ?? state.packageName;
  const finalVersion = version ?? `${state.packageVersion}-${state.rootHash.slice(0, 8)}`;

  // Create new PackageObject with updated root
  const newPkgObject: PackageObject = {
    tasks: deployedPkgObject.tasks,
    data: {
      structure: deployedPkgObject.data.structure,
      value: state.rootHash,
    },
  };

  // Encode and store the new package object
  const encoder = encodeBeast2For(PackageObjectType);
  const pkgData = encoder(newPkgObject);
  const packageHash = await storage.objects.write(repo, pkgData);

  // Create zip file
  const zipfile = new yazl.ZipFile();

  // Track which objects we've added to avoid duplicates
  const addedObjects = new Set<string>();

  // Helper to add an object to the zip
  const addObject = async (hash: string): Promise<void> => {
    if (addedObjects.has(hash)) return;
    addedObjects.add(hash);

    const data = await storage.objects.read(repo, hash);
    const objPath = `objects/${hash.slice(0, 2)}/${hash.slice(2)}.beast2`;
    zipfile.addBuffer(Buffer.from(data), objPath, { mtime: DETERMINISTIC_MTIME });
  };

  // Helper to collect children from a tree object (same as packages.ts)
  const collectTreeChildren = async (treeData: Uint8Array): Promise<void> => {
    const dataStr = Buffer.from(treeData).toString('latin1');
    const hashPattern = /[a-f0-9]{64}/g;
    const matches = dataStr.matchAll(hashPattern);

    for (const match of matches) {
      const potentialHash = match[0];
      if (addedObjects.has(potentialHash)) continue;

      try {
        await addObject(potentialHash);
        const childData = await storage.objects.read(repo, potentialHash);
        await collectTreeChildren(childData);
      } catch {
        addedObjects.delete(potentialHash);
      }
    }
  };

  // Add the package object
  await addObject(packageHash);

  // Collect all task objects
  for (const taskHash of newPkgObject.tasks.values()) {
    await addObject(taskHash);
  }

  // Collect the root tree and all its children
  await addObject(state.rootHash);
  const rootTreeData = await storage.objects.read(repo, state.rootHash);
  await collectTreeChildren(rootTreeData);

  // Write the package ref
  const refPath = `packages/${finalName}/${finalVersion}`;
  zipfile.addBuffer(Buffer.from(packageHash + '\n'), refPath, { mtime: DETERMINISTIC_MTIME });

  // Finalize and write zip to disk
  await new Promise<void>((resolve, reject) => {
    const writeStream = createWriteStream(partialPath);
    zipfile.outputStream.pipe(writeStream);
    zipfile.outputStream.on('error', reject);
    writeStream.on('error', reject);
    writeStream.on('close', resolve);
    zipfile.end();
  });

  // Atomic rename to final path
  await fs.rename(partialPath, zipPath);

  return {
    packageHash,
    objectCount: addedObjects.size,
    name: finalName,
    version: finalVersion,
  };
}
