/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Package operations for e3 repositories.
 *
 * Handles importing, exporting, and managing packages in the content-addressed
 * object store.
 */

import * as fs from 'fs/promises';
import { createWriteStream } from 'fs';
import yauzl from 'yauzl';
import yazl from 'yazl';
import { decodeBeast2For } from '@elaraai/east';
import { PackageObjectType } from '@elaraai/e3-types';
import type { PackageObject } from '@elaraai/e3-types';
import {
  PackageNotFoundError,
  PackageInvalidError,
} from './errors.js';
import type { StorageBackend } from './storage/interfaces.js';

/**
 * Result of importing a package
 */
export interface PackageImportResult {
  name: string;
  version: string;
  packageHash: string;
  objectCount: number;
}

/**
 * Import a package from a .zip file into the repository.
 *
 * Extracts objects to `objects/`, creates ref at `packages/<name>/<version>`.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param zipPath - Path to the .zip package file
 * @returns Import result with package name, version, and stats
 */
export async function packageImport(
  storage: StorageBackend,
  repo: string,
  zipPath: string
): Promise<PackageImportResult> {
  // Open the zip file
  const zipfile = await openZip(zipPath);

  let packageName: string | undefined;
  let packageVersion: string | undefined;
  let packageHash: string | undefined;
  let objectCount = 0;

  try {
    // Iterate through all entries
    for await (const entry of iterateZipEntries(zipfile)) {
      const { fileName, getData } = entry;

      // Skip directory entries
      if (fileName.endsWith('/')) {
        continue;
      }

      // Handle package ref: packages/<name>/<version>
      if (fileName.startsWith('packages/')) {
        const parts = fileName.split('/');
        if (parts.length === 3) {
          packageName = parts[1];
          packageVersion = parts[2];

          // Read the hash from the ref file
          const data = await getData();
          packageHash = data.toString('utf-8').trim();

          // Write the ref to the repository
          await storage.refs.packageWrite(repo, packageName, packageVersion, packageHash);
        }
        continue;
      }

      // Handle object: objects/<ab>/<cdef...>.beast2
      if (fileName.startsWith('objects/')) {
        const data = await getData();

        // Store the object (storage.objects.write will verify the hash matches)
        await storage.objects.write(repo, data);
        objectCount++;
        continue;
      }

      // Unknown entry type - ignore for forward compatibility
    }
  } finally {
    // Close the zip file
    zipfile.close();
  }

  if (!packageName || !packageVersion || !packageHash) {
    throw new PackageInvalidError('missing package ref');
  }

  return {
    name: packageName,
    version: packageVersion,
    packageHash,
    objectCount,
  };
}

/**
 * Remove a package ref from the repository.
 *
 * Objects remain until gc is run.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param name - Package name
 * @param version - Package version
 * @throws {PackageNotFoundError} If package doesn't exist
 */
export async function packageRemove(
  storage: StorageBackend,
  repo: string,
  name: string,
  version: string
): Promise<void> {
  // Check if package exists first (storage.refs.packageRemove is idempotent)
  const hash = await storage.refs.packageResolve(repo, name, version);
  if (hash === null) {
    throw new PackageNotFoundError(name, version);
  }

  await storage.refs.packageRemove(repo, name, version);
}

/**
 * List all installed packages.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @returns Array of (name, version) pairs
 */
export async function packageList(
  storage: StorageBackend,
  repo: string
): Promise<Array<{ name: string; version: string }>> {
  return storage.refs.packageList(repo);
}

/**
 * Get the latest version of a package.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param name - Package name
 * @returns Latest version string, or undefined if package not found
 */
export async function packageGetLatestVersion(
  storage: StorageBackend,
  repo: string,
  name: string
): Promise<string | undefined> {
  const packages = await packageList(storage, repo);
  const versions = packages
    .filter(p => p.name === name)
    .map(p => p.version)
    .sort();
  return versions[versions.length - 1];
}

/**
 * Resolve a package to its PackageObject hash.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param name - Package name
 * @param version - Package version
 * @returns PackageObject hash
 * @throws {PackageNotFoundError} If package doesn't exist
 */
export async function packageResolve(
  storage: StorageBackend,
  repo: string,
  name: string,
  version: string
): Promise<string> {
  const hash = await storage.refs.packageResolve(repo, name, version);
  if (hash === null) {
    throw new PackageNotFoundError(name, version);
  }
  return hash;
}

/**
 * Read and parse a PackageObject.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param name - Package name
 * @param version - Package version
 * @returns Parsed PackageObject
 * @throws {PackageNotFoundError} If package doesn't exist
 */
export async function packageRead(
  storage: StorageBackend,
  repo: string,
  name: string,
  version: string
): Promise<PackageObject> {
  const hash = await packageResolve(storage, repo, name, version);
  const data = await storage.objects.read(repo, hash);
  const decoder = decodeBeast2For(PackageObjectType);
  return decoder(Buffer.from(data));
}

/**
 * Result of exporting a package
 */
export interface PackageExportResult {
  packageHash: string;
  objectCount: number;
}

/**
 * Fixed mtime for deterministic zip output (Unix epoch)
 */
const DETERMINISTIC_MTIME = new Date(0);

/**
 * Export a package to a .zip file.
 *
 * Collects the package object and all transitively referenced objects.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier
 * @param name - Package name
 * @param version - Package version
 * @param zipPath - Path to write the .zip file
 * @returns Export result with package hash and object count
 */
export async function packageExport(
  storage: StorageBackend,
  repo: string,
  name: string,
  version: string,
  zipPath: string
): Promise<PackageExportResult> {
  const partialPath = `${zipPath}.partial`;

  // Resolve package to hash
  const packageHash = await packageResolve(storage, repo, name, version);

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

  // Helper to collect children from a tree object
  // Tree objects are encoded as structs with DataRef fields
  const collectTreeChildren = async (treeData: Uint8Array): Promise<void> => {
    // Decode as a generic structure and extract DataRefs
    // This is a bit tricky since trees have dynamic structure
    // For now, we'll use a heuristic: scan for hash patterns in the beast2 data
    // A more robust approach would be to track the structure during export

    const dataStr = Buffer.from(treeData).toString('latin1');

    // Look for hash patterns (64 hex chars) that might be object references
    // Use matchAll to avoid regex state issues
    const hashPattern = /[a-f0-9]{64}/g;
    const matches = dataStr.matchAll(hashPattern);

    for (const match of matches) {
      const potentialHash = match[0];

      // Skip if we've already added this object
      if (addedObjects.has(potentialHash)) {
        continue;
      }

      // Try to load this as an object - if it exists, it's a reference
      try {
        await addObject(potentialHash);
        // Recursively collect children from this object
        const childData = await storage.objects.read(repo, potentialHash);
        await collectTreeChildren(childData);
      } catch {
        // Object doesn't exist, not a valid reference - remove from set
        addedObjects.delete(potentialHash);
      }
    }
  };

  // Add the package object first
  await addObject(packageHash);

  // Load and parse the package object
  const packageData = await storage.objects.read(repo, packageHash);
  const decoder = decodeBeast2For(PackageObjectType);
  const packageObject: PackageObject = decoder(Buffer.from(packageData));

  // Collect all task objects
  for (const taskHash of packageObject.tasks.values()) {
    await addObject(taskHash);
    // Note: Task objects reference datasets by path, not by hash,
    // so we don't need to recursively collect from them
  }

  // Collect the root tree and all its children
  const rootTreeHash = packageObject.data.value;
  await addObject(rootTreeHash);
  const rootTreeData = await storage.objects.read(repo, rootTreeHash);
  await collectTreeChildren(rootTreeData);

  // Write the package ref
  const refPath = `packages/${name}/${version}`;
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
  };
}

// ============================================================================
// Zip file helpers using yauzl
// ============================================================================

interface ZipEntry {
  fileName: string;
  getData(): Promise<Buffer>;
}

/**
 * Open a zip file for reading
 */
function openZip(zipPath: string): Promise<yauzl.ZipFile> {
  return new Promise((resolve, reject) => {
    yauzl.open(zipPath, { lazyEntries: true }, (err, zipfile) => {
      if (err) return reject(err);
      if (!zipfile) return reject(new Error('No zipfile'));
      resolve(zipfile);
    });
  });
}

/**
 * Async iterator over zip entries
 */
async function* iterateZipEntries(
  zipfile: yauzl.ZipFile
): AsyncGenerator<ZipEntry> {
  // Create a queue for entries
  const entryQueue: Array<yauzl.Entry | null> = [];
  let resolveNext: (() => void) | null = null;
  let rejectNext: ((err: Error) => void) | null = null;

  zipfile.on('entry', (entry: yauzl.Entry) => {
    entryQueue.push(entry);
    if (resolveNext) {
      resolveNext();
      resolveNext = null;
    }
  });

  zipfile.on('end', () => {
    entryQueue.push(null); // Signal end
    if (resolveNext) {
      resolveNext();
      resolveNext = null;
    }
  });

  zipfile.on('error', (err: Error) => {
    if (rejectNext) {
      rejectNext(err);
      rejectNext = null;
    }
  });

  // Start reading
  zipfile.readEntry();

  while (true) {
    // Wait for an entry if queue is empty
    if (entryQueue.length === 0) {
      await new Promise<void>((resolve, reject) => {
        resolveNext = resolve;
        rejectNext = reject;
      });
    }

    const entry = entryQueue.shift();
    if (entry === null || entry === undefined) {
      return; // End of entries
    }

    // Create getData function for this entry
    const getData = (): Promise<Buffer> => {
      return new Promise((resolve, reject) => {
        zipfile.openReadStream(entry, (err, readStream) => {
          if (err) return reject(err);
          if (!readStream) return reject(new Error('No read stream'));

          const chunks: Buffer[] = [];
          readStream.on('data', (chunk: Buffer) => chunks.push(chunk));
          readStream.on('end', () => resolve(Buffer.concat(chunks)));
          readStream.on('error', reject);
        });
      });
    };

    yield { fileName: entry.fileName, getData };

    // Read next entry
    zipfile.readEntry();
  }
}
