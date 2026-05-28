/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 list command - List workspaces or tree contents
 *
 * Usage:
 *   e3 list .                    # List all workspaces
 *   e3 list . ws                 # List root tree of workspace
 *   e3 list . ws.inputs          # List fields under inputs
 */

import {
  workspaceList,
  workspaceListTree,
  workspaceGetState,
  LocalStorage,
} from '@elaraai/e3-core';
import {
  workspaceList as workspaceListRemote,
  datasetList as datasetListRemote,
  datasetListAt as datasetListAtRemote,
} from '@elaraai/e3-api-client';
import { parseRepoLocation, parseDatasetPath, formatError, exitError } from '../utils.js';

/**
 * List workspaces or tree contents at a path.
 */
export async function listCommand(repoArg: string, pathSpec?: string): Promise<void> {
  try {
    const location = await parseRepoLocation(repoArg);

    // If no path, list workspaces
    if (!pathSpec) {
      if (location.type === 'local') {
        const storage = new LocalStorage();
        const workspaces = await workspaceList(storage, location.path);

        if (workspaces.length === 0) {
          console.log('No workspaces');
          return;
        }

        for (const ws of workspaces) {
          const state = await workspaceGetState(storage, location.path, ws);
          if (state) {
            console.log(`${ws}  (${state.packageName}@${state.packageVersion})`);
          } else {
            console.log(`${ws}  (not deployed)`);
          }
        }
      } else {
        // Remote: list workspaces
        const workspaces = await workspaceListRemote(
          location.baseUrl,
          location.repo,
          { token: location.token }
        );

        if (workspaces.length === 0) {
          console.log('No workspaces');
          return;
        }

        for (const ws of workspaces) {
          if (ws.deployed && ws.packageName.type === 'some' && ws.packageVersion.type === 'some') {
            console.log(`${ws.name}  (${ws.packageName.value}@${ws.packageVersion.value})`);
          } else {
            console.log(`${ws.name}  (not deployed)`);
          }
        }
      }
      return;
    }

    // Parse path and list tree contents
    const { ws, path } = parseDatasetPath(pathSpec);
    let fields: string[];

    if (location.type === 'local') {
      const storage = new LocalStorage();
      fields = await workspaceListTree(storage, location.path, ws, path);
    } else {
      // Remote: list tree contents
      if (path.length === 0) {
        fields = await datasetListRemote(
          location.baseUrl,
          location.repo,
          ws,
          { token: location.token }
        );
      } else {
        fields = await datasetListAtRemote(
          location.baseUrl,
          location.repo,
          ws,
          path,
          { token: location.token }
        );
      }
    }

    if (fields.length === 0) {
      console.log('(empty)');
      return;
    }

    for (const field of fields) {
      console.log(field);
    }
  } catch (err) {
    exitError(formatError(err));
  }
}
