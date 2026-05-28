/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import * as fs from 'node:fs/promises';
import * as os from 'node:os';
import * as path from 'node:path';
import { ArrayType, BlobType, NullType } from '@elaraai/east';
import {
  packageList,
  packageImport,
  packageExport,
  packageRemove,
  packageRead,
} from '@elaraai/e3-core';
import type { StorageBackend } from '@elaraai/e3-core';
import { PackageObjectType } from '@elaraai/e3-types';
import { sendSuccess, sendError } from '../beast2.js';
import { errorToVariant } from '../errors.js';
import { PackageListItemType, PackageImportResultType } from '../types.js';

/**
 * List all packages in the repository.
 */
export async function listPackages(
  storage: StorageBackend,
  repoPath: string
): Promise<Response> {
  try {
    const packages = await packageList(storage, repoPath);
    const result = packages.map((pkg) => ({
      name: pkg.name,
      version: pkg.version,
    }));
    return sendSuccess(ArrayType(PackageListItemType), result);
  } catch (err) {
    return sendError(ArrayType(PackageListItemType), errorToVariant(err));
  }
}

/**
 * Get package details.
 */
export async function getPackage(
  storage: StorageBackend,
  repoPath: string,
  name: string,
  version: string
): Promise<Response> {
  try {
    const pkg = await packageRead(storage, repoPath, name, version);
    return sendSuccess(PackageObjectType, pkg);
  } catch (err) {
    return sendError(PackageObjectType, errorToVariant(err));
  }
}

/**
 * Import a package from a zip archive.
 */
export async function importPackage(
  storage: StorageBackend,
  repoPath: string,
  archive: Uint8Array
): Promise<Response> {
  try {
    // Write to temp file
    const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'e3-import-'));
    const tempPath = path.join(tempDir, 'package.zip');
    try {
      await fs.writeFile(tempPath, archive);
      const result = await packageImport(storage, repoPath, tempPath);
      return sendSuccess(PackageImportResultType, {
        name: result.name,
        version: result.version,
        packageHash: result.packageHash,
        objectCount: BigInt(result.objectCount),
      });
    } finally {
      await fs.rm(tempDir, { recursive: true, force: true });
    }
  } catch (err) {
    return sendError(PackageImportResultType, errorToVariant(err));
  }
}

/**
 * Export a package as a zip archive.
 */
export async function exportPackage(
  storage: StorageBackend,
  repoPath: string,
  name: string,
  version: string
): Promise<Response> {
  try {
    // Export to temp file
    const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'e3-export-'));
    const tempPath = path.join(tempDir, 'package.zip');
    try {
      await packageExport(storage, repoPath, name, version, tempPath);
      const archive = await fs.readFile(tempPath);
      return sendSuccess(BlobType, new Uint8Array(archive));
    } finally {
      await fs.rm(tempDir, { recursive: true, force: true });
    }
  } catch (err) {
    return sendError(BlobType, errorToVariant(err));
  }
}

/**
 * Delete a package.
 */
export async function deletePackage(
  storage: StorageBackend,
  repoPath: string,
  name: string,
  version: string
): Promise<Response> {
  try {
    await packageRemove(storage, repoPath, name, version);
    return sendSuccess(NullType, null);
  } catch (err) {
    return sendError(NullType, errorToVariant(err));
  }
}
