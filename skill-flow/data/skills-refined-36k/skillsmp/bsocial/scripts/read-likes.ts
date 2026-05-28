#!/usr/bin/env bun

import { queryBmap, buildLikesQuery, type BmapPost } from "../lib/bmap-client.js";

const HELP = `
read-likes - Read BSocial likes from the blockchain

USAGE:
  bun run read-likes.ts [options]

OPTIONS:
  --address <addr>   Filter by liker's address
  --txid <txid>      Get likes for a specific post
  --limit <n>        Maximum likes to return (default: 20)
  --json             Output JSON format
  -h, --help         Show this help

EXAMPLES:
  bun run read-likes.ts --address 1A1z...
  bun run read-likes.ts --txid abc123...
`.trim();

interface Args {
  address?: string;
  txid?: string;
  limit: number;
  json: boolean;
  help: boolean;
}

function parseArgs(args: string[]): Args {
  const result: Args = { limit: 20, json: false, help: false };
  let i = 0;

  while (i < args.length) {
    const arg = args[i];

    if (arg === "-h" || arg === "--help") {
      result.help = true;
    } else if (arg === "--json") {
      result.json = true;
    } else if (arg === "--address" && args[i + 1]) {
      result.address = args[++i];
    } else if (arg === "--txid" && args[i + 1]) {
      result.txid = args[++i];
    } else if (arg === "--limit" && args[i + 1]) {
      result.limit = parseInt(args[++i], 10);
    }
    i++;
  }

  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || (!args.address && !args.txid)) {
    console.log(HELP);
    process.exit(args.help ? 0 : 1);
  }

  try {
    const query = buildLikesQuery({ address: args.address, txid: args.txid }, args.limit);
    const likes = await queryBmap("like", query);

    if (args.json) {
      console.log(
        JSON.stringify(
          likes.map((l) => ({
            txid: l.tx.h,
            time: l.blk?.t,
            likedTx: l.MAP?.[0]?.tx,
            liker: l.AIP?.[0]?.address,
          })),
          null,
          2
        )
      );
    } else {
      if (likes.length === 0) {
        console.log("No likes found");
      } else {
        console.log(`Found ${likes.length} likes:\n`);
        likes.forEach((like, i) => {
          const likedTx = like.MAP?.[0]?.tx || "unknown";
          const liker = like.AIP?.[0]?.address || "unknown";
          console.log(`[${i + 1}] ${liker.substring(0, 12)}... liked ${likedTx.substring(0, 12)}...`);
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
