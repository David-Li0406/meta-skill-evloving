#!/usr/bin/env bun
/**
 * calculate-share.ts - Calculate share difficulty and validate against target
 * Usage: bun run calculate-share.ts --header <80-byte-hex> --target <difficulty>
 */

import { Hash } from "@bsv/sdk";

const args = process.argv.slice(2);

function showHelp(): void {
  console.log(`Usage: bun run calculate-share.ts [options]

Calculate share difficulty and validate against target.

Options:
  --header <hex>          80-byte block header as hex
  --target <difficulty>   Target difficulty (pool share difficulty)
  --version <hex>         Block version (4 bytes, big-endian)
  --prevhash <hex>        Previous block hash (32 bytes)
  --merkle <hex>          Merkle root (32 bytes)
  --time <hex>            Block time (4 bytes, big-endian)
  --bits <hex>            Difficulty bits (4 bytes)
  --nonce <hex>           Nonce (4 bytes, big-endian)
  --json                  Output as JSON
  --help, -h              Show this help message

Examples:
  # Using pre-built header
  bun run calculate-share.ts --header <80-byte-hex> --target 1

  # Build header from components
  bun run calculate-share.ts --version 20000000 --prevhash 00...00 --merkle ab...cd --time 5f5e5d5c --bits 1d00ffff --nonce 12345678 --target 1`);
}

if (args.includes("--help") || args.includes("-h")) {
  showHelp();
  process.exit(0);
}

// Parse arguments
let header: string | null = null;
let target = 1;
let version: string | null = null;
let prevhash: string | null = null;
let merkle: string | null = null;
let time: string | null = null;
let bits: string | null = null;
let nonce: string | null = null;
const jsonOutput = args.includes("--json");

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--header" && args[i + 1]) {
    header = args[i + 1];
    i++;
  } else if (args[i] === "--target" && args[i + 1]) {
    target = Number.parseFloat(args[i + 1]);
    i++;
  } else if (args[i] === "--version" && args[i + 1]) {
    version = args[i + 1];
    i++;
  } else if (args[i] === "--prevhash" && args[i + 1]) {
    prevhash = args[i + 1];
    i++;
  } else if (args[i] === "--merkle" && args[i + 1]) {
    merkle = args[i + 1];
    i++;
  } else if (args[i] === "--time" && args[i + 1]) {
    time = args[i + 1];
    i++;
  } else if (args[i] === "--bits" && args[i + 1]) {
    bits = args[i + 1];
    i++;
  } else if (args[i] === "--nonce" && args[i + 1]) {
    nonce = args[i + 1];
    i++;
  }
}

// Helper: reverse bytes in hex string
function reverseBytes(hex: string): string {
  const bytes = hex.match(/.{2}/g);
  if (!bytes) return hex;
  return bytes.reverse().join("");
}

// Build header from components if not provided directly
if (!header) {
  if (version && prevhash && merkle && time && bits && nonce) {
    // Version, time, bits, nonce are BE hex -> convert to LE bytes
    const versionLE = reverseBytes(version.padStart(8, "0"));
    const prevhashLE = reverseBytes(prevhash);
    const merkleLE = reverseBytes(merkle);
    const timeLE = reverseBytes(time.padStart(8, "0"));
    const bitsLE = reverseBytes(bits.padStart(8, "0"));
    const nonceLE = reverseBytes(nonce.padStart(8, "0"));

    header = versionLE + prevhashLE + merkleLE + timeLE + bitsLE + nonceLE;
  } else {
    console.error("Error: Either --header or all components (--version, --prevhash, --merkle, --time, --bits, --nonce) required");
    process.exit(1);
  }
}

// Validate header
if (!/^[0-9a-fA-F]{160}$/.test(header)) {
  console.error("Error: Header must be exactly 80 bytes (160 hex chars)");
  process.exit(1);
}

// Calculate block hash (SHA256d)
const headerBytes = Buffer.from(header, "hex");
const hash1 = Hash.sha256(Array.from(headerBytes));
const hash2 = Hash.sha256(hash1);
const hashBytes = Array.from(hash2).reverse();
const blockHash = Buffer.from(hashBytes).toString("hex");

// Calculate share difficulty from hash
// Difficulty = max_target / hash_as_target
// max_target = 0x00000000FFFF0000000000000000000000000000000000000000000000000000
const maxTarget = BigInt("0x00000000FFFF0000000000000000000000000000000000000000000000000000");
const hashBigInt = BigInt("0x" + blockHash);
const shareDifficulty = hashBigInt === 0n ? Number.MAX_VALUE : Number(maxTarget) / Number(hashBigInt);

const valid = shareDifficulty >= target;

const result = {
  blockHash,
  shareDifficulty: shareDifficulty.toFixed(6),
  targetDifficulty: target,
  valid,
  header: header.toLowerCase(),
};

if (jsonOutput) {
  console.log(JSON.stringify(result, null, 2));
} else {
  console.log(`Share Calculation`);
  console.log(`Block Hash: ${blockHash}`);
  console.log(`Share Difficulty: ${shareDifficulty.toFixed(6)}`);
  console.log(`Target Difficulty: ${target}`);
  console.log(`Valid: ${valid ? "YES" : "NO"}`);
}
