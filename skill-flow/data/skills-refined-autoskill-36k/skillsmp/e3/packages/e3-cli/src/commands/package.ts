/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 package commands - Package management
 */

import { readFileSync, writeFileSync } from 'node:fs';
import {
  packageImport,
  packageExport,
  packageList,
  packageRemove,
  LocalStorage,
} from '@elaraai/e3-core';
import {
  packageImport as packageImportRemote,
  packageExport as packageExportRemote,
  packageList as packageListRemote,
  packageRemove as packageRemoveRemote,
} from '@elaraai/e3-api-client';
import { parseRepoLocation, parsePackageSpec, formatError, exitError } from '../utils.js';

export const packageCommand = {
  /**
   * Import a package from a .zip file.
   */
  async import(repoArg: string, zipPath: string): Promise<void> {
    try {
      const location = await parseRepoLocation(repoArg);

      if (location.type === 'local') {
        const storage = new LocalStorage();
        const result = await packageImport(storage, location.path, zipPath);

        console.log(`Imported ${result.name}@${result.version}`);
        console.log(`  Package hash: ${result.packageHash.slice(0, 12)}...`);
        console.log(`  Objects: ${result.objectCount}`);
      } else {
        // Remote import - read local zip and send to server
        const zipBytes = readFileSync(zipPath);
        const result = await packageImportRemote(location.baseUrl, location.repo, new Uint8Array(zipBytes), { token: location.token });

        console.log(`Imported ${result.name}@${result.version}`);
        console.log(`  Package hash: ${result.packageHash.slice(0, 12)}...`);
        console.log(`  Objects: ${result.objectCount}`);
      }
    } catch (err) {
      exitError(formatError(err));
    }
  },

  /**
   * Export a package to a .zip file.
   */
  async export(repoArg: string, pkgSpec: string, zipPath: string): Promise<void> {
    try {
      const location = await parseRepoLocation(repoArg);
      const { name, version } = parsePackageSpec(pkgSpec);

      if (location.type === 'local') {
        const storage = new LocalStorage();
        const result = await packageExport(storage, location.path, name, version, zipPath);

        console.log(`Exported ${name}@${version} to ${zipPath}`);
        console.log(`  Package hash: ${result.packageHash.slice(0, 12)}...`);
        console.log(`  Objects: ${result.objectCount}`);
      } else {
        // Remote export - fetch zip bytes and write locally
        const zipBytes = await packageExportRemote(location.baseUrl, location.repo, name, version, { token: location.token });
        writeFileSync(zipPath, zipBytes);

        console.log(`Exported ${name}@${version} to ${zipPath}`);
        console.log(`  Size: ${zipBytes.length} bytes`);
      }
    } catch (err) {
      exitError(formatError(err));
    }
  },

  /**
   * List installed packages.
   */
  async list(repoArg: string): Promise<void> {
    try {
      const location = await parseRepoLocation(repoArg);

      let packages: Array<{ name: string; version: string }>;

      if (location.type === 'local') {
        const storage = new LocalStorage();
        packages = await packageList(storage, location.path);
      } else {
        packages = await packageListRemote(location.baseUrl, location.repo, { token: location.token });
      }

      if (packages.length === 0) {
        console.log('No packages installed');
        return;
      }

      console.log('Packages:');
      for (const pkg of packages) {
        console.log(`  ${pkg.name}@${pkg.version}`);
      }
    } catch (err) {
      exitError(formatError(err));
    }
  },

  /**
   * Remove a package.
   */
  async remove(repoArg: string, pkgSpec: string): Promise<void> {
    try {
      const location = await parseRepoLocation(repoArg);
      const { name, version } = parsePackageSpec(pkgSpec);

      if (location.type === 'local') {
        const storage = new LocalStorage();
        await packageRemove(storage, location.path, name, version);
        console.log(`Removed ${name}@${version}`);
        console.log('Run `e3 gc` to reclaim disk space');
      } else {
        await packageRemoveRemote(location.baseUrl, location.repo, name, version, { token: location.token });
        console.log(`Removed ${name}@${version}`);
      }
    } catch (err) {
      exitError(formatError(err));
    }
  },
};
