#!/usr/bin/env bun

import { PrivateKey, Transaction } from "@bsv/sdk";
import BSocial, { BSocialActionType, type BSocialFollow } from "@bopen-io/templates/template/bsocial/BSocial.ts";
import { fundAndBroadcast } from "../lib/broadcast.js";

const HELP = `
create-follow - Follow a user on the BSV blockchain

USAGE:
  bun run create-follow.ts <wif> <bapId>

OPTIONS:
  --dry-run    Build tx but don't broadcast
  --json       Output JSON format
  -h, --help   Show this help

EXAMPLES:
  bun run create-follow.ts L1... 1BAPSu...
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

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || !args.wif || !args.bapId) {
    console.log(HELP);
    process.exit(args.help ? 0 : 1);
  }

  try {
    const privateKey = PrivateKey.fromWif(args.wif);

    const follow: BSocialFollow = {
      app: "bsocial",
      type: BSocialActionType.FOLLOW,
      bapId: args.bapId,
    };

    const lockingScript = await BSocial.createFollow(follow, privateKey);

    const tx = new Transaction();
    tx.addOutput({
      satoshis: 0,
      lockingScript,
    });

    if (args.dryRun) {
      const result = { status: "dry-run", bapId: args.bapId, txSize: tx.toBinary().length };
      if (args.json) {
        console.log(JSON.stringify(result, null, 2));
      } else {
        console.log(`Dry run - would follow: ${args.bapId}`);
        console.log(`TX size: ${result.txSize} bytes`);
      }
      process.exit(0);
    }

    const txid = await fundAndBroadcast(tx, privateKey);

    if (args.json) {
      console.log(JSON.stringify({ txid, following: args.bapId }, null, 2));
    } else {
      console.log(`Following: ${txid}`);
    }
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Error: ${message}`);
    process.exit(1);
  }
}

main();
