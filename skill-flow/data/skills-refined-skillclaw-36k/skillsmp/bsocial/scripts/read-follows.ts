#!/usr/bin/env bun

import { queryBmap, buildFollowsQuery, type BmapPost } from "../lib/bmap-client.js";

const HELP = `
read-follows - Read BSocial follows from the blockchain

USAGE:
  bun run read-follows.ts <address> [options]

OPTIONS:
  --limit <n>    Maximum follows to return (default: 100)
  --json         Output JSON format
  -h, --help     Show this help

EXAMPLES:
  bun run read-follows.ts 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
  bun run read-follows.ts 1A1z... --json
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
    const query = buildFollowsQuery(args.address, args.limit);
    const follows = await queryBmap("follow", query);

    if (args.json) {
      console.log(
        JSON.stringify(
          follows.map((f) => ({
            txid: f.tx.h,
            time: f.blk?.t,
            following: f.MAP?.[0]?.bapId,
            follower: f.AIP?.[0]?.address,
          })),
          null,
          2
        )
      );
    } else {
      if (follows.length === 0) {
        console.log(`No follows found for ${args.address}`);
      } else {
        console.log(`${args.address} is following:\n`);
        follows.forEach((follow, i) => {
          const bapId = follow.MAP?.[0]?.bapId || "unknown";
          console.log(`[${i + 1}] ${bapId}`);
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
