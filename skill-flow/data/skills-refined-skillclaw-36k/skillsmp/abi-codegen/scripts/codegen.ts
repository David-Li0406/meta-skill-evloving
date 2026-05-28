#!/usr/bin/env bun

/**
 * JSON ABI to TypeScript Converter
 *
 * Converts JSON ABI files to TypeScript files with const exports.
 *
 * Usage:
 *   bun codegen.ts <file-or-glob-pattern>
 *
 * Examples:
 *   bun codegen.ts src/evm/abi/lockup/v3.0/SablierLockup.json
 *   bun codegen.ts "src/evm/abi/lockup/v3.0/*.json"
 *   bun codegen.ts "src/evm/abi/**\/*.json"
 */

import { existsSync, mkdirSync } from "node:fs";
import { basename, dirname, relative } from "node:path";
import { $, Glob } from "bun";

const JSON_EXT_REGEX = /\.json$/;

type ConversionResult = {
  input: string;
  output: string;
  success: boolean;
  error?: string;
};

/**
 * Convert PascalCase filename to camelCase with "Abi" suffix
 * Example: "SablierLockup.json" -> "sablierLockupAbi"
 */
function generateExportName(filename: string): string {
  // Remove .json extension
  const nameWithoutExt = filename.replace(JSON_EXT_REGEX, "");

  // Convert PascalCase to camelCase
  const camelCase = nameWithoutExt.charAt(0).toLowerCase() + nameWithoutExt.slice(1);

  // Add "Abi" suffix
  return `${camelCase}Abi`;
}

/**
 * Determine output path based on input path
 * Input:  src/evm/abi/{protocol}/{version}/{ContractName}.json
 * Output: src/evm/releases/{protocol}/{version}/abi/{ContractName}.ts
 */
function getOutputPath(inputPath: string): string {
  // Parse the input path
  const parts = inputPath.split("/");
  const abiIndex = parts.indexOf("abi");

  if (abiIndex === -1) {
    throw new Error(`Invalid input path: ${inputPath} (missing 'abi' directory)`);
  }

  // Extract protocol and version
  // Example: ["src", "evm", "abi", "lockup", "v3.0", "SablierLockup.json"]
  //                              ^       ^        ^
  //                           abiIndex  +1       +2
  const protocol = parts[abiIndex + 1];
  const version = parts[abiIndex + 2];
  const filename = parts.at(-1);

  if (!protocol || !version || !filename) {
    throw new Error(
      `Invalid input path structure: ${inputPath} (expected src/evm/abi/{protocol}/{version}/{file}.json)`
    );
  }

  // Construct output path
  const tsFilename = filename.replace(JSON_EXT_REGEX, ".ts");
  return `src/evm/releases/${protocol}/${version}/abi/${tsFilename}`;
}

/**
 * Convert a single JSON ABI file to TypeScript
 */
async function convertFile(inputPath: string): Promise<ConversionResult> {
  try {
    const jsonContent = await globalThis.Bun.file(inputPath).text();
    const abi = JSON.parse(jsonContent);

    // Validate it's an array (ABIs are arrays)
    if (!Array.isArray(abi)) {
      throw new Error("ABI must be a JSON array");
    }

    // Generate export name
    const filename = basename(inputPath);
    const exportName = generateExportName(filename);

    // Generate TypeScript content
    const tsContent = `export const ${exportName} = ${JSON.stringify(abi, null, 2)} as const;\n`;

    // Determine output path
    const outputPath = getOutputPath(inputPath);

    // Create output directory if it doesn't exist
    const outputDir = dirname(outputPath);
    if (!existsSync(outputDir)) {
      mkdirSync(outputDir, { recursive: true });
    }

    await globalThis.Bun.write(outputPath, tsContent);

    return {
      input: inputPath,
      output: outputPath,
      success: true,
    };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : String(error),
      input: inputPath,
      output: "",
      success: false,
    };
  }
}

/**
 * Resolve glob pattern or file path to list of files
 */
async function resolveFiles(pattern: string): Promise<string[]> {
  // Check if it's a direct file path (no glob characters)
  if (!pattern.includes("*") && !pattern.includes("?")) {
    if (!existsSync(pattern)) {
      throw new Error(`File not found: ${pattern}`);
    }
    return [pattern];
  }

  // Use Bun's Glob to resolve pattern
  const glob = new Glob(pattern);
  const files: string[] = [];

  for await (const file of glob.scan(".")) {
    files.push(file);
  }

  if (files.length === 0) {
    throw new Error(`No files matched pattern: ${pattern}`);
  }

  return files;
}

/**
 * Run Biome formatter on generated files
 */
async function runBiomeFormat(files: string[]): Promise<void> {
  if (files.length === 0) {
    return;
  }

  console.log("\nRunning Biome formatter...");

  try {
    // Run biome-write via just
    await $`just biome-write ${files.join(" ")}`.quiet();
    console.log(`✓ Formatted ${files.length} file${files.length === 1 ? "" : "s"}`);
  } catch (error) {
    console.error("⚠ Warning: Biome formatting failed (non-fatal)");
    console.error(error);
  }
}

/**
 * Main execution
 */
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error("Usage: bun codegen.ts <file-or-glob-pattern>");
    console.error("\nExamples:");
    console.error("  bun codegen.ts src/evm/abi/lockup/v3.0/SablierLockup.json");
    console.error('  bun codegen.ts "src/evm/abi/lockup/v3.0/*.json"');
    console.error('  bun codegen.ts "src/evm/abi/**/*.json"');
    process.exit(1);
  }

  const pattern = args[0];
  console.log(`Resolving files: ${pattern}`);

  try {
    // Resolve files from pattern
    const files = await resolveFiles(pattern);
    console.log(`Found ${files.length} file${files.length === 1 ? "" : "s"}\n`);

    // Convert each file
    const results: ConversionResult[] = [];
    for (const file of files) {
      const result = await convertFile(file);
      results.push(result);

      if (result.success) {
        const relativeInput = relative(".", result.input);
        const relativeOutput = relative(".", result.output);
        console.log(`✓ ${basename(relativeInput)} → ${basename(relativeOutput)}`);
      } else {
        console.error(`✗ ${file}: ${result.error}`);
      }
    }

    // Collect successful outputs for formatting
    const successfulOutputs = results.filter((r) => r.success).map((r) => r.output);

    // Run Biome formatter
    if (successfulOutputs.length > 0) {
      await runBiomeFormat(successfulOutputs);
    }

    // Summary
    const successCount = results.filter((r) => r.success).length;
    const failCount = results.length - successCount;

    console.log(`\nDone! Converted ${successCount} ABI file${successCount === 1 ? "" : "s"}.`);

    if (failCount > 0) {
      console.error(`Failed to convert ${failCount} file${failCount === 1 ? "" : "s"}.`);
      process.exit(1);
    }
  } catch (error) {
    console.error("Error:", error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}

// Run main
main().catch((error) => {
  console.error("Fatal error:", error instanceof Error ? error.message : String(error));
  process.exit(1);
});
