#!/usr/bin/env bun
/**
 * build-coinbase.ts - Build coinbase transaction from Stratum components
 * Usage: bun run build-coinbase.ts --coinb1 <hex> --coinb2 <hex> --extranonce1 <hex> --extranonce2 <hex>
 */

import { Hash } from "@bsv/sdk";

const args = process.argv.slice(2);

function showHelp(): void {
  console.log(`Usage: bun run build-coinbase.ts [options]

Build coinbase transaction from Stratum components.

Options:
  --coinb1 <hex>          Coinbase part 1 (from mining.notify)
  --coinb2 <hex>          Coinbase part 2 (from mining.notify)
  --extranonce1 <hex>     Extranonce1 (from mining.subscribe)
  --extranonce2 <hex>     Extranonce2 (miner-selected)
  --json                  Output as JSON
  --help, -h              Show this help message

Example:
  bun run build-coinbase.ts \\
    --coinb1 01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff \\
    --coinb2 ffffffff0100f2052a0100000023210337 \\
    --extranonce1 08000002 \\
    --extranonce2 00000000`);
}

if (args.includes("--help") || args.includes("-h")) {
  showHelp();
  process.exit(0);
}

// Parse arguments
let coinb1: string | null = null;
let coinb2: string | null = null;
let extranonce1: string | null = null;
let extranonce2: string | null = null;
const jsonOutput = args.includes("--json");

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--coinb1" && args[i + 1]) {
    coinb1 = args[i + 1];
    i++;
  } else if (args[i] === "--coinb2" && args[i + 1]) {
    coinb2 = args[i + 1];
    i++;
  } else if (args[i] === "--extranonce1" && args[i + 1]) {
    extranonce1 = args[i + 1];
    i++;
  } else if (args[i] === "--extranonce2" && args[i + 1]) {
    extranonce2 = args[i + 1];
    i++;
  }
}

// Validate required params
if (!coinb1 || !coinb2 || !extranonce1 || !extranonce2) {
  console.error("Error: Missing required parameters");
  console.error("Required: --coinb1, --coinb2, --extranonce1, --extranonce2");
  process.exit(1);
}

// Validate hex format
const hexRegex = /^[0-9a-fA-F]*$/;
if (!hexRegex.test(coinb1) || !hexRegex.test(coinb2) || !hexRegex.test(extranonce1) || !hexRegex.test(extranonce2)) {
  console.error("Error: Invalid hex format");
  process.exit(1);
}

// Build coinbase: coinb1 + extranonce1 + extranonce2 + coinb2
const coinbaseHex = coinb1 + extranonce1 + extranonce2 + coinb2;
const coinbaseBytes = Buffer.from(coinbaseHex, "hex");

// Calculate txid (SHA256d, then reverse for display)
const hash1 = Hash.sha256(Array.from(coinbaseBytes));
const hash2 = Hash.sha256(hash1);
const txidBytes = Array.from(hash2).reverse();
const txid = Buffer.from(txidBytes).toString("hex");

const result = {
  coinbase: coinbaseHex,
  txid,
  components: {
    coinb1,
    extranonce1,
    extranonce2,
    coinb2,
  },
  length: coinbaseHex.length / 2,
};

if (jsonOutput) {
  console.log(JSON.stringify(result, null, 2));
} else {
  console.log(`Coinbase Transaction Built`);
  console.log(`Coinbase Hex: ${coinbaseHex}`);
  console.log(`TXID: ${txid}`);
  console.log(`Length: ${result.length} bytes`);
}
