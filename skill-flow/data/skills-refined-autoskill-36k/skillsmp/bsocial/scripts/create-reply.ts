#!/usr/bin/env bun

import { PrivateKey, Transaction } from "@bsv/sdk";
import BSocial, { BSocialActionType, type BSocialPost } from "@bopen-io/templates/template/bsocial/BSocial.ts";
import { fundAndBroadcast } from "../lib/broadcast.js";

const HELP = `
create-reply - Reply to a BSocial post on the BSV blockchain

USAGE:
  bun run create-reply.ts <wif> <txid> "Reply content" [options]

OPTIONS:
  --tags <t1,t2>   Comma-separated tags
  --dry-run        Build tx but don't broadcast
  --json           Output JSON format
  -h, --help       Show this help

EXAMPLES:
  bun run create-reply.ts L1... abc123... "Great post!"
  bun run create-reply.ts L1... abc123... "Interesting" --tags discussion
`.trim();

interface Args {
  wif?: string;
  txid?: string;
  content?: string;
  tags?: string[];
  dryRun: boolean;
  json: boolean;
  help: boolean;
}

function parseArgs(args: string[]): Args {
  const result: Args = { dryRun: false, json: false, help: false };
  let i = 0;

  while (i < args.length) {
    const arg = args[i];

    if (arg === "-h" || arg === "--help") {
      result.help = true;
    } else if (arg === "--dry-run") {
      result.dryRun = true;
    } else if (arg === "--json") {
      result.json = true;
    } else if (arg === "--tags" && args[i + 1]) {
      result.tags = args[++i].split(",").map((t) => t.trim());
    } else if (!arg.startsWith("--") && !result.wif) {
      result.wif = arg;
    } else if (!arg.startsWith("--") && !result.txid) {
      result.txid = arg;
    } else if (!arg.startsWith("--") && !result.content) {
      result.content = arg;
    }
    i++;
  }

  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || !args.wif || !args.txid || !args.content) {
    console.log(HELP);
    process.exit(args.help ? 0 : 1);
  }

  if (!/^[a-fA-F0-9]{64}$/.test(args.txid)) {
    console.error("Error: Invalid txid format (must be 64 hex characters)");
    process.exit(1);
  }

  try {
    const privateKey = PrivateKey.fromWif(args.wif);

    const reply: BSocialPost = {
      app: "bsocial",
      type: BSocialActionType.POST,
      content: args.content,
      mediaType: "text/plain",
      encoding: "utf-8",
    };

    const lockingScript = await BSocial.createReply(reply, args.txid, args.tags, privateKey);

    const tx = new Transaction();
    tx.addOutput({
      satoshis: 0,
      lockingScript,
    });

    if (args.dryRun) {
      const result = {
        status: "dry-run",
        replyTo: args.txid,
        content: args.content,
        txSize: tx.toBinary().length,
      };
      if (args.json) {
        console.log(JSON.stringify(result, null, 2));
      } else {
        console.log(`Dry run - would reply to: ${args.txid}`);
        console.log(`Content: ${args.content}`);
        console.log(`TX size: ${result.txSize} bytes`);
      }
      process.exit(0);
    }

    const txid = await fundAndBroadcast(tx, privateKey);

    if (args.json) {
      console.log(JSON.stringify({ txid, replyTo: args.txid, content: args.content }, null, 2));
    } else {
      console.log(`Reply created: ${txid}`);
    }
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Error: ${message}`);
    process.exit(1);
  }
}

main();
