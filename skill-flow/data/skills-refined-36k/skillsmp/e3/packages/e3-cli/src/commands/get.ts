/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 get command - Get dataset value
 *
 * Usage:
 *   e3 get . ws.path.to.dataset
 *   e3 get . ws.path.to.dataset -f json
 *   e3 get https://server/repos/myrepo ws.path.to.dataset
 */

import { workspaceGetDatasetHash, datasetRead, LocalStorage } from '@elaraai/e3-core';
import { datasetGet as datasetGetRemote } from '@elaraai/e3-api-client';
import { printFor, toJSONFor, decodeBeast2, toEastTypeValue, isVariant, type EastTypeValue } from '@elaraai/east';
import { parseRepoLocation, parseDatasetPath, formatError, exitError } from '../utils.js';

/**
 * Get dataset value at a path.
 */
export async function getCommand(
  repoArg: string,
  pathSpec: string,
  options: { format?: string }
): Promise<void> {
  try {
    const location = await parseRepoLocation(repoArg);
    const { ws, path } = parseDatasetPath(pathSpec);

    if (path.length === 0) {
      exitError('Path must include at least one field (e.g., ws.field)');
    }

    const format = options.format ?? 'east';

    let type: EastTypeValue;
    let value: unknown;

    if (location.type === 'local') {
      const storage = new LocalStorage();

      // Get the hash first, then read with type info
      const { refType, hash } = await workspaceGetDatasetHash(storage, location.path, ws, path);

      if (refType === 'unassigned') {
        exitError('Dataset is unassigned (pending task output)');
      }

      if (refType === 'null' || hash === null) {
        console.log('null');
        return;
      }

      // Read the dataset to get both value and type
      const dataset = await datasetRead(storage, location.path, hash);
      // Convert EastType to EastTypeValue if necessary
      type = isVariant(dataset.type) ? dataset.type as EastTypeValue : toEastTypeValue(dataset.type);
      value = dataset.value;
    } else {
      // Remote: get raw BEAST2 bytes and decode
      const beast2Data = await datasetGetRemote(
        location.baseUrl,
        location.repo,
        ws,
        path,
        { token: location.token }
      );

      // Decode BEAST2 to get type and value
      const decoded = decodeBeast2(beast2Data);
      type = decoded.type;
      value = decoded.value;
    }

    switch (format) {
      case 'east': {
        const printer = printFor(type);
        console.log(printer(value));
        break;
      }
      case 'json': {
        const toJSON = toJSONFor(type);
        const jsonValue = toJSON(value);
        console.log(JSON.stringify(jsonValue, null, 2));
        break;
      }
      case 'beast2':
        exitError('beast2 output format not yet implemented for get command');
        break;
      default:
        exitError(`Unknown format: ${format}. Use: east, json, beast2`);
    }
  } catch (err) {
    exitError(formatError(err));
  }
}
