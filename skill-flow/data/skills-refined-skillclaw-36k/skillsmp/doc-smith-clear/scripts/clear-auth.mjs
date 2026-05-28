#!/usr/bin/env node

/**
 * Clear site authorization tokens
 *
 * Usage:
 *   node clear-auth.mjs --site=<hostname>  # Clear specific site
 *   node clear-auth.mjs --all              # Clear all sites
 *
 * Output: JSON format with result
 */

import { createStore } from "./utils/store/index.mjs";

function parseArgs() {
  const args = process.argv.slice(2);
  const result = { site: null, all: false };

  for (const arg of args) {
    if (arg === "--all") {
      result.all = true;
    } else if (arg.startsWith("--site=")) {
      result.site = arg.slice("--site=".length);
    }
  }

  return result;
}

async function main() {
  const args = parseArgs();

  if (!args.all && !args.site) {
    console.log(
      JSON.stringify({
        success: false,
        error: "Please specify --site=<hostname> or --all",
      }),
    );
    process.exit(1);
  }

  try {
    const store = await createStore();
    const listMap = await store.listMap();
    const sites = Object.keys(listMap);

    if (sites.length === 0) {
      console.log(
        JSON.stringify({
          success: true,
          message: "No site authorizations found to clear.",
          clearedSites: [],
        }),
      );
      return;
    }

    const clearedSites = [];

    if (args.all) {
      // Clear all sites
      await store.clear();
      clearedSites.push(...sites);
    } else if (args.site) {
      // Clear specific site
      if (!sites.includes(args.site)) {
        console.log(
          JSON.stringify({
            success: false,
            error: `Site '${args.site}' not found in authorized sites.`,
            availableSites: sites,
          }),
        );
        process.exit(1);
      }

      await store.deleteItem(args.site);
      clearedSites.push(args.site);
    }

    console.log(
      JSON.stringify({
        success: true,
        message: `Successfully cleared authorization for ${clearedSites.length} site(s).`,
        clearedSites,
      }),
    );
  } catch (error) {
    console.log(
      JSON.stringify({
        success: false,
        error: `Failed to clear authorizations: ${error.message}`,
      }),
    );
    process.exit(1);
  }
}

main();
