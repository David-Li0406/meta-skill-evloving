#!/usr/bin/env node

/**
 * Clear deployment configuration (appUrl) from config.yaml
 *
 * Usage:
 *   node clear-deployment-config.mjs [--config=<path>]
 *
 * Output: JSON format with result
 */

import { readFile, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { resolve } from "node:path";
import yaml from "yaml";

function parseArgs() {
  const args = process.argv.slice(2);
  let configPath = resolve(process.cwd(), "config.yaml");

  for (const arg of args) {
    if (arg.startsWith("--config=")) {
      configPath = arg.slice("--config=".length);
    }
  }

  return { configPath };
}

async function main() {
  const { configPath } = parseArgs();

  try {
    if (!existsSync(configPath)) {
      console.log(
        JSON.stringify({
          success: true,
          message: "Config file not found. No need to clear appUrl.",
          cleared: false,
        }),
      );
      return;
    }

    const configContent = await readFile(configPath, "utf-8");
    const doc = yaml.parseDocument(configContent);

    if (!doc.has("appUrl")) {
      console.log(
        JSON.stringify({
          success: true,
          message: "No appUrl found in config file. Nothing to clear.",
          cleared: false,
        }),
      );
      return;
    }

    doc.delete("appUrl");
    await writeFile(
      configPath,
      doc.toString({
        keepSourceTokens: true,
        indent: 2,
        lineWidth: 0,
        minContentWidth: 0,
      }),
      "utf-8",
    );

    console.log(
      JSON.stringify({
        success: true,
        message: "Cleared appUrl from config file.",
        cleared: true,
      }),
    );
  } catch (error) {
    console.log(
      JSON.stringify({
        success: false,
        error: `Failed to clear deployment config: ${error.message}`,
      }),
    );
    process.exit(1);
  }
}

main();
