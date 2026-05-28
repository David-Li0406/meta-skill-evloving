#!/usr/bin/env bun

import { PrivateKey, Transaction } from "@bsv/sdk";
import BSocial, { BSocialActionType, BSocialContext, type BSocialMessage } from "@bopen-io/templates/template/bsocial/BSocial.ts";
import { fundAndBroadcast } from "../lib/broadcast.js";

const HELP = `
create-message - Send a BSocial message on the BSV blockchain

USAGE:
  bun run create-message.ts <wif> "Message content" [options]

OPTIONS:
  --channel <name>    Send to a channel
  --to <bapId>        Send to a specific user (private message)
  --dry-run           Build tx but don't broadcast
  --json              Output JSON format
  -h, --help          Show this help

EXAMPLES:
  bun run create-message.ts L1... "Hello everyone"
  bun run create-message.ts L1... "Channel message" --channel general
  bun run create-message.ts L1... "Private message" --to 1BAPSu...
`.trim();

interface Args {
  wif?: string;
  content?: string;
  channel?: string;
  to?: string;
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
    } else if (arg === "--channel" && args[i + 1]) {
      result.channel = args[++i];
    } else if (arg === "--to" && args[i + 1]) {
      result.to = args[++i];
    } else if (!arg.startsWith("--") && !result.wif) {
      result.wif = arg;
    } else if (!arg.startsWith("--") && !result.content) {
      result.content = arg;
    }
    i++;
  }

  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || !args.wif || !args.content) {
    console.log(HELP);
    process.exit(args.help ? 0 : 1);
  }

  try {
    const privateKey = PrivateKey.fromWif(args.wif);

    const message: BSocialMessage = {
      app: "bsocial",
      type: BSocialActionType.MESSAGE,
      content: args.content,
      mediaType: "text/plain",
      encoding: "utf-8",
    };

    // Set context based on target
    if (args.channel) {
      message.context = BSocialContext.CHANNEL;
      message.contextValue = args.channel;
    } else if (args.to) {
      message.context = BSocialContext.BAP_ID;
      message.contextValue = args.to;
    }

    const lockingScript = await BSocial.createMessage(message, privateKey);

    const tx = new Transaction();
    tx.addOutput({
      satoshis: 0,
      lockingScript,
    });

    if (args.dryRun) {
      const result = {
        status: "dry-run",
        content: args.content,
        channel: args.channel,
        to: args.to,
        txSize: tx.toBinary().length,
      };
      if (args.json) {
        console.log(JSON.stringify(result, null, 2));
      } else {
        console.log("Dry run - message not sent");
        console.log(`Content: ${args.content}`);
        if (args.channel) console.log(`Channel: ${args.channel}`);
        if (args.to) console.log(`To: ${args.to}`);
        console.log(`TX size: ${result.txSize} bytes`);
      }
      process.exit(0);
    }

    const txid = await fundAndBroadcast(tx, privateKey);

    if (args.json) {
      console.log(JSON.stringify({ txid, content: args.content }, null, 2));
    } else {
      console.log(`Message sent: ${txid}`);
    }
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Error: ${message}`);
    process.exit(1);
  }
}

main();
