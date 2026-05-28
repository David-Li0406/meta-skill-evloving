/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 set command - Set dataset value from file
 *
 * Usage:
 *   e3 set . ws.path.to.dataset ./data.beast2
 *   e3 set . ws.path.to.dataset ./data.east
 *   e3 set . ws.path.to.dataset ./data.json --type ".Integer"
 *   e3 set . ws.path.to.dataset ./data.csv --type ".Array .Struct [{name: \"name\", type: .String}, {name: \"value\", type: .Integer}]"
 *   e3 set https://server/repos/myrepo ws.path.to.dataset ./data.east
 */

import { readFile } from 'fs/promises';
import { extname } from 'path';
import { WorkspaceLockError, workspaceSetDataset, LocalStorage } from '@elaraai/e3-core';
import { datasetSet as datasetSetRemote } from '@elaraai/e3-api-client';
import {
  decodeBeast2,
  parseFor,
  fromJSONFor,
  decodeCsvFor,
  encodeBeast2For,
  EastTypeType,
  type EastTypeValue,
  type StructTypeValue,
  parseInferred,
  toEastTypeValue,
} from '@elaraai/east';
import { parseRepoLocation, parseDatasetPath, formatError, exitError } from '../utils.js';

/**
 * Parse a type specification in .east format.
 * Types are represented as EastTypeValue variants.
 *
 * Examples:
 *   ".Integer" -> variant("Integer", null)
 *   ".Array .Integer" -> variant("Array", variant("Integer", null))
 *   ".Struct [{name: \"x\", type: .Integer}]" -> variant("Struct", [{name: "x", type: variant("Integer", null)}])
 */
function parseTypeSpec(typeSpec: string): EastTypeValue {
  const parser = parseFor(EastTypeType);
  const result = parser(typeSpec);
  if (!result.success) {
    throw new Error(`Invalid type specification: ${result.error}`);
  }
  return result.value as EastTypeValue;
}

/**
 * Set dataset value from a file.
 */
export async function setCommand(
  repoArg: string,
  pathSpec: string,
  filePath: string,
  options: { type?: string } = {}
): Promise<void> {
  try {
    const location = await parseRepoLocation(repoArg);
    const { ws, path } = parseDatasetPath(pathSpec);

    if (path.length === 0) {
      exitError('Path must include at least one field (e.g., ws.field)');
    }

    // Parse type specification if provided
    let providedType: EastTypeValue | undefined;
    if (options.type) {
      providedType = parseTypeSpec(options.type);
    }

    // Read and decode the file based on extension
    const fileContent = await readFile(filePath);
    const ext = extname(filePath).toLowerCase();

    let value: unknown;
    let type: EastTypeValue;

    switch (ext) {
      case '.beast2': {
        // Beast2 is self-describing, type spec is optional (for override)
        const decoded = decodeBeast2(fileContent);
        value = decoded.value;
        type = providedType ?? decoded.type;
        break;
      }
      case '.east': {
        const content = fileContent.toString('utf-8');
        if (providedType) {
          // Parse with provided type for stricter validation
          const parser = parseFor(providedType);
          const result = parser(content);
          if (!result.success) {
            exitError(`Failed to parse .east file: ${result.error}`);
          }
          value = result.value;
          type = providedType;
        } else {
          // Use parseInferred for type inference from .east syntax
          const [parsedType, parsedValue] = parseInferred(content);
          // parseInferred returns EastType, but we need EastTypeValue
          // Use toEastTypeValue to convert
          value = parsedValue;
          type = toEastTypeValue(parsedType);
        }
        break;
      }
      case '.json': {
        if (!providedType) {
          exitError('JSON files require --type flag. Example: --type ".Integer"');
        }
        const content = fileContent.toString('utf-8');
        const jsonValue = JSON.parse(content);
        const fromJSON = fromJSONFor(providedType);
        value = fromJSON(jsonValue);
        type = providedType;
        break;
      }
      case '.csv': {
        if (!providedType) {
          exitError('CSV files require --type flag. Example: --type ".Array .Struct [{name: \\"name\\", type: .String}]"');
        }
        // CSV expects .Array .Struct [...] - check the variant type
        if (providedType.type !== 'Array') {
          exitError('CSV files require an Array type. Example: --type ".Array .Struct [...]"');
        }
        const elementType = providedType.value as EastTypeValue;
        if (elementType.type !== 'Struct') {
          exitError('CSV files require Array of Struct type. Example: --type ".Array .Struct [{name: \\"x\\", type: .Integer}]"');
        }
        const decoder = decodeCsvFor(elementType as StructTypeValue);
        value = decoder(fileContent);
        type = providedType;
        break;
      }
      default:
        exitError(`Unknown file extension: ${ext}. Supported: .beast2, .east, .json, .csv`);
    }

    if (location.type === 'local') {
      const storage = new LocalStorage();
      await workspaceSetDataset(storage, location.path, ws, path, value, type);
    } else {
      // Remote: encode value to BEAST2 and send
      const encoder = encodeBeast2For(type);
      const beast2Data = encoder(value);
      await datasetSetRemote(
        location.baseUrl,
        location.repo,
        ws,
        path,
        beast2Data,
        { token: location.token }
      );
    }

    console.log(`Set ${pathSpec} from ${filePath}`);
  } catch (err) {
    if (err instanceof WorkspaceLockError) {
      console.log('');
      console.log(`Workspace is locked by another process with PID: ${err.holder?.pid ?? 'unknown'}`);
      process.exit(1);
    }
    exitError(formatError(err));
  }
}
