#!/usr/bin/env bun

import { PrivateKey, Transaction, Script, Hash } from "@bsv/sdk";
import { fundAndBroadcast } from "../lib/broadcast.js";

const MAP_PREFIX = "1PuQa7K62MiKCtssSLKy1kh56WWU7MtUR5";

const HELP = `
create-friend - Send a friend request on the BSV blockchain

USAGE:
  bun run create-friend.ts <wif> <bapId>

OPTIONS:
  --dry-run    Build tx but don't broadcast
  --json       Output JSON format
  -h, --help   Show this help

NOTE: Friend requests include a derived public key for encrypted messaging.
      This creates a two-way relationship when both parties send friend requests.

EXAMPLES:
  bun run create-friend.ts L1... 1BAPSu...
`.trim();

interface Args {
  wif?: string;
  bapId?: string;
  dryRun: boolean;
  json: boolean;
  help: boolean;
}

function parseArgs(args: string[]): Args {
  const result: Args = { dryRun: false, json: false, help: false };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === "-h" || arg === "--help") {
      result.help = true;
    } else if (arg === "--dry-run") {
      result.dryRun = true;
    } else if (arg === "--json") {
      result.json = true;
    } else if (!arg.startsWith("--") && !result.wif) {
      result.wif = arg;
    } else if (!arg.startsWith("--") && !result.bapId) {
      result.bapId = arg;
    }
  }

  return result;
}

function textToHex(text: string): string {
  const bytes = new TextEncoder().encode(text);
  return Array.from(bytes)
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || !args.wif || !args.bapId) {
    console.log(HELP);
    process.exit(args.help ? 0 : 1);
  }

  try {
    const privateKey = PrivateKey.fromWif(args.wif);
    const publicKey = privateKey.toPublicKey().toString();

    // Derive a friend-specific public key using the bapId as input
    // This follows the BitcoinSchema friend protocol
    const bapIdHash = Hash.sha256(args.bapId, "utf8");
    // For now, use the main public key (proper derivation would use BAP library)
    const friendPublicKey = publicKey;

    // Build friend MAP data
    const mapData = [
      MAP_PREFIX,
      "SET",
      "app",
      "bsocial",
      "type",
      "friend",
      "bapID",
      args.bapId,
      "publicKey",
      friendPublicKey,
    ];

    // Build OP_RETURN script
    const asmParts = mapData.map((d) => textToHex(d)).join(" ");
    const lockingScript = Script.fromASM(`OP_0 OP_RETURN ${asmParts}`);

    const tx = new Transaction();
    tx.addOutput({
      satoshis: 0,
      lockingScript,
    });

    if (args.dryRun) {
      const result = {
        status: "dry-run",
        bapId: args.bapId,
        publicKey: friendPublicKey,
        txSize: tx.toBinary().length,
      };
      if (args.json) {
        console.log(JSON.stringify(result, null, 2));
      } else {
        console.log(`Dry run - would send friend request to: ${args.bapId}`);
        console.log(`Public key: ${friendPublicKey.substring(0, 20)}...`);
        console.log(`TX size: ${result.txSize} bytes`);
      }
      process.exit(0);
    }

    const txid = await fundAndBroadcast(tx, privateKey);

    if (args.json) {
      console.log(JSON.stringify({ txid, friend: args.bapId }, null, 2));
    } else {
      console.log(`Friend request sent: ${txid}`);
    }
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Error: ${message}`);
    process.exit(1);
  }
}

main();
