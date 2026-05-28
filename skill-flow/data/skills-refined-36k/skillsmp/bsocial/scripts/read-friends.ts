#!/usr/bin/env bun

import { queryBmap, buildFriendsQuery, type BmapPost } from "../lib/bmap-client.js";

const HELP = `
read-friends - Read BSocial friend relationships from the blockchain

USAGE:
  bun run read-friends.ts <address> [options]

OPTIONS:
  --limit <n>    Maximum friends to return (default: 100)
  --json         Output JSON format
  -h, --help     Show this help

EXAMPLES:
  bun run read-friends.ts 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
  bun run read-friends.ts 1A1z... --json
`.trim();

interface Args {
  address?: string;
  limit: number;
  json: boolean;
  help: boolean;
}

function parseArgs(args: string[]): Args {
  const result: Args = { limit: 100, json: false, help: false };
  let i = 0;

  while (i < args.length) {
    const arg = args[i];

    if (arg === "-h" || arg === "--help") {
      result.help = true;
    } else if (arg === "--json") {
      result.json = true;
    } else if (arg === "--limit" && args[i + 1]) {
      result.limit = parseInt(args[++i], 10);
    } else if (!arg.startsWith("--") && !result.address) {
      result.address = arg;
    }
    i++;
  }

  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || !args.address) {
    console.log(HELP);
    process.exit(args.help ? 0 : 1);
  }

  try {
    const query = buildFriendsQuery(args.address, args.limit);
    const friends = await queryBmap("friend", query);

    if (args.json) {
      console.log(
        JSON.stringify(
          friends.map((f) => ({
            txid: f.tx.h,
            time: f.blk?.t,
            friend: f.MAP?.[0]?.bapID,
            publicKey: f.MAP?.[0]?.publicKey,
            from: f.AIP?.[0]?.address,
          })),
          null,
          2
        )
      );
    } else {
      if (friends.length === 0) {
        console.log(`No friend requests found for ${args.address}`);
      } else {
        console.log(`Friend requests from ${args.address}:\n`);
        friends.forEach((friend, i) => {
          const bapId = friend.MAP?.[0]?.bapID || "unknown";
          const time = friend.blk?.t ? new Date(friend.blk.t * 1000).toISOString() : "pending";
          console.log(`[${i + 1}] ${bapId} (${time})`);
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
