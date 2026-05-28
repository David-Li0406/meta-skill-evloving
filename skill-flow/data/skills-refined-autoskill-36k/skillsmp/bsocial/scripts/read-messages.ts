#!/usr/bin/env bun

import { queryBmap, buildMessagesQuery, type BmapPost } from "../lib/bmap-client.js";

const HELP = `
read-messages - Read BSocial messages from the blockchain

USAGE:
  bun run read-messages.ts [options]

OPTIONS:
  --channel <name>   Filter by channel
  --address <addr>   Filter by sender address
  --limit <n>        Maximum messages to return (default: 50)
  --json             Output JSON format
  -h, --help         Show this help

EXAMPLES:
  bun run read-messages.ts --channel general
  bun run read-messages.ts --address 1A1z...
`.trim();

interface Args {
  channel?: string;
  address?: string;
  limit: number;
  json: boolean;
  help: boolean;
}

function parseArgs(args: string[]): Args {
  const result: Args = { limit: 50, json: false, help: false };
  let i = 0;

  while (i < args.length) {
    const arg = args[i];

    if (arg === "-h" || arg === "--help") {
      result.help = true;
    } else if (arg === "--json") {
      result.json = true;
    } else if (arg === "--channel" && args[i + 1]) {
      result.channel = args[++i];
    } else if (arg === "--address" && args[i + 1]) {
      result.address = args[++i];
    } else if (arg === "--limit" && args[i + 1]) {
      result.limit = parseInt(args[++i], 10);
    }
    i++;
  }

  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || (!args.channel && !args.address)) {
    console.log(HELP);
    process.exit(args.help ? 0 : 1);
  }

  try {
    const query = buildMessagesQuery({ channel: args.channel, address: args.address }, args.limit);
    const messages = await queryBmap("message", query);

    if (args.json) {
      console.log(
        JSON.stringify(
          messages.map((m) => ({
            txid: m.tx.h,
            time: m.blk?.t,
            content: m.B?.[0]?.content,
            sender: m.AIP?.[0]?.address,
            channel: m.MAP?.[0]?.contextValue,
          })),
          null,
          2
        )
      );
    } else {
      if (messages.length === 0) {
        console.log("No messages found");
      } else {
        const label = args.channel ? `#${args.channel}` : args.address;
        console.log(`Messages from ${label}:\n`);
        messages.forEach((msg, i) => {
          const content = msg.B?.[0]?.content || "";
          const sender = msg.AIP?.[0]?.address || "unknown";
          const time = msg.blk?.t ? new Date(msg.blk.t * 1000).toLocaleTimeString() : "pending";
          console.log(`[${time}] ${sender.substring(0, 8)}...: ${content.substring(0, 80)}`);
        });
      }
    }
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Error: ${message}`);
    process.exit(1);
  }
}

main();
