#!/usr/bin/env node

/**
 * List all authorized sites
 * Output: JSON format with sites array
 */

import { createStore } from "./utils/store/index.mjs";

async function main() {
  try {
    const store = await createStore();
    const listMap = await store.listMap();
    const sites = Object.keys(listMap);

    console.log(JSON.stringify({ sites }, null, 2));
  } catch (error) {
    console.log(JSON.stringify({ sites: [], error: error.message }, null, 2));
  }
}

main();
