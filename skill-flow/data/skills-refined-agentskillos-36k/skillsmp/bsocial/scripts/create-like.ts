#!/usr/bin/env bun

import { PrivateKey, Transaction } from "@bsv/sdk";
import BSocial, { BSocialActionType, type BSocialLike } from "@bopen-io/templates/template/bsocial/BSocial.ts";
import { fundAndBroadcast } from "../lib/broadcast.js";

const HELP = `
create-like - Like a BSocial post on the BSV blockchain

USAGE:
  bun run create-like.ts <wif> <txid>

OPTIONS:
  --dry-run    Build tx but don't broadcast
  --json       Output JSON format
  -h, --help   Show this help

EXAMPLES:
  bun run create-like.ts L1... abc123def456...
`.trim();

interface Args {
  wif?: string;
  txid?: string;
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
    } else if (!arg.startsWith("--") && !result.txid) {
      result.txid = arg;
    }
  }

  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || !args.wif || !args.txid) {
    console.log(HELP);
    process.exit(args.help ? 0 : 1);
  }

  if (!/^[a-fA-F0-9]{64}$/.test(args.txid)) {
    console.error("Error: Invalid txid format (must be 64 hex characters)");
    process.exit(1);
  }

  try {
    const privateKey = PrivateKey.fromWif(args.wif);

    const like: BSocialLike = {
      app: "bsocial",
      type: BSocialActionType.LIKE,
      txid: args.txid,
    };

    const lockingScript = await BSocial.createLike(like, privateKey);

    const tx = new Transaction();
    tx.addOutput({
      satoshis: 0,
      lockingScript,
    });

    if (args.dryRun) {
      const result = { status: "dry-run", txid: args.txid, txSize: tx.toBinary().length };
      if (args.json) {
        console.log(JSON.stringify(result, null, 2));
      } else {
        console.log(`Dry run - would like txid: ${args.txid}`);
        console.log(`TX size: ${result.txSize} bytes`);
      }
      process.exit(0);
    }

    const txid = await fundAndBroadcast(tx, privateKey);

    if (args.json) {
      console.log(JSON.stringify({ txid, liked: args.txid }, null, 2));
    } else {
      console.log(`Liked: ${txid}`);
    }
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Error: ${message}`);
    process.exit(1);
  }
}

main();
