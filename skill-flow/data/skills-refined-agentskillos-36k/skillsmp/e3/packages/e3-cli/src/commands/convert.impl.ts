/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 convert command - Transform data between .east, .json, and .beast2 formats
 */

import * as fs from 'fs/promises';
import {
  decodeBeast2,
  printFor,
  toJSONFor,
  parseFor,
  fromJSONFor,
  encodeBeast2For,
  parseInferred,
  printType,
} from '@elaraai/east';

/**
 * Output format type (type is output-only)
 */
export type ConvertFormat = 'east' | 'json' | 'beast2' | 'type';

/**
 * Input format type (no 'type' as input)
 */
export type InputFormat = 'east' | 'json' | 'beast2';

/**
 * Conversion result
 */
export interface ConvertResult {
  success: boolean;
  data?: string | Buffer;
  format?: ConvertFormat;
  error?: Error;
}

/**
 * Detect format from file extension
 */
function detectFormat(filePath: string): InputFormat {
  const ext = filePath.slice(filePath.lastIndexOf('.'));
  if (ext === '.east') return 'east';
  if (ext === '.json') return 'json';
  if (ext === '.beast2') return 'beast2';

  throw new Error(`Cannot detect format from extension: ${ext} (expected .east, .json, or .beast2)`);
}

/**
 * Core logic for converting between formats
 * Supports .beast2 (self-describing), .east (with parseInferred or --type), .json (with --type), and stdin
 */
export async function convertCore(
  inputPath: string | null,
  toFormat: ConvertFormat,
  outputPath?: string,
  typeSpec?: string,
  fromFormat?: InputFormat
): Promise<ConvertResult> {
  try {
    let type: any;
    let value: any;
    let detectedFormat: InputFormat;

    // Read input data
    let inputData: Buffer;
    if (inputPath === null) {
      // Read from stdin
      const chunks: Buffer[] = [];
      for await (const chunk of process.stdin) {
        chunks.push(chunk);
      }
      inputData = Buffer.concat(chunks);

      // Detect format if not explicitly specified
      if (fromFormat) {
        detectedFormat = fromFormat;
      } else {
        // Try to detect format from content
        if (inputData.length > 0 && inputData[0] === 0x42) {
          // Beast2 files typically start with 'B' (0x42) magic byte
          detectedFormat = 'beast2';
        } else {
          // Assume text format - default to .east unless explicitly JSON-like
          const content = inputData.toString('utf-8').trim();
          // Only treat as JSON if it looks like a JSON object with quotes around keys
          if (content.startsWith('{') && content.includes('"')) {
            detectedFormat = 'json';
          } else {
            // Default to .east (handles arrays, structs, primitives, etc.)
            detectedFormat = 'east';
          }
        }
      }
    } else {
      // Read from file
      inputData = await fs.readFile(inputPath);

      // Use explicit format if provided, otherwise detect from extension
      if (fromFormat) {
        detectedFormat = fromFormat;
      } else {
        detectedFormat = detectFormat(inputPath);
      }
    }

    // Parse type specification if provided (in .east format)
    let providedType: any | undefined;
    if (typeSpec) {
      const [parsedType, _] = parseInferred(typeSpec);
      providedType = parsedType;
    }

    // Decode input based on format
    if (detectedFormat === 'beast2') {
      // Beast2 is self-describing
      const decoded = decodeBeast2(inputData);
      type = decoded.type;
      value = decoded.value;
    } else if (detectedFormat === 'east') {
      // For .east, try parseInferred first, then use providedType
      const content = inputData.toString('utf-8');

      if (providedType) {
        // Use provided type
        const parser = parseFor(providedType);
        const result = parser(content);
        if (!result.success) {
          throw new Error(`Failed to parse .east with provided type: ${result.error}`);
        }
        type = providedType;
        value = result.value;
      } else {
        // Use parseInferred
        const [parsedType, parsedValue] = parseInferred(content);
        type = parsedType;
        value = parsedValue;
      }
    } else {
      // JSON format - requires type
      if (!providedType) {
        throw new Error('JSON format requires --type to be specified');
      }

      const content = inputData.toString('utf-8');
      const jsonValue = JSON.parse(content);
      const fromJSON = fromJSONFor(providedType);
      type = providedType;
      value = fromJSON(jsonValue);
    }

    // If already in target format and no output path, just return
    // (but not if outputting type, which is always computed)
    if (detectedFormat === toFormat && !outputPath && inputPath !== null) {
      return {
        success: true,
        data: inputData,
        format: toFormat,
      };
    }

    // Encode to target format
    let outputData: string | Buffer;

    if (toFormat === 'type') {
      // Output the type instead of the value (always in .east format)
      const typeString = printType(type);
      outputData = typeString;
    } else if (toFormat === 'east') {
      const printer = printFor(type);
      outputData = printer(value);
    } else if (toFormat === 'json') {
      const toJSON = toJSONFor(type);
      const jsonResult = toJSON(value);
      outputData = JSON.stringify(jsonResult, null, 2);
    } else {
      // beast2
      const encoder = encodeBeast2For(type);
      outputData = Buffer.from(encoder(value));
    }

    // Write to output file if specified
    if (outputPath) {
      if (outputData instanceof Buffer) {
        await fs.writeFile(outputPath, outputData);
      } else {
        await fs.writeFile(outputPath, outputData, 'utf-8');
      }
      return {
        success: true,
        format: toFormat,
      };
    }

    return {
      success: true,
      data: outputData,
      format: toFormat,
    };
  } catch (error: any) {
    return {
      success: false,
      error: error instanceof Error ? error : new Error(String(error)),
    };
  }
}

/**
 * CLI handler for the convert command
 */
export async function convertFile(
  inputPath: string | undefined,
  toFormat: ConvertFormat = 'east',
  outputPath?: string,
  typeSpec?: string,
  fromFormat?: InputFormat
): Promise<void> {
  // If no input path, use stdin
  const actualInputPath = inputPath === undefined || inputPath === '-' ? null : inputPath;

  const result = await convertCore(actualInputPath, toFormat, outputPath, typeSpec, fromFormat);

  if (!result.success) {
    console.error(`Error: Failed to convert: ${result.error?.message}`);
    process.exit(1);
  }

  // Output the data to stdout if no output file specified
  if (!outputPath && result.data) {
    if (result.data instanceof Buffer) {
      process.stdout.write(result.data);
    } else {
      console.log(result.data);
    }
  }
}
