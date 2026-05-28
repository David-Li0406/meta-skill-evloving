#!/usr/bin/env bun

import { queryBmap, buildPostsQuery, getPostsByBapId, type BmapPost } from "../lib/bmap-client.js";

const HELP = `
read-posts - Read BSocial posts from the blockchain

USAGE:
  bun run read-posts.ts <address> [options]

OPTIONS:
  --limit <n>    Maximum posts to return (default: 20)
  --json         Output JSON format
  -h, --help     Show this help

EXAMPLES:
  bun run read-posts.ts 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
  bun run read-posts.ts 1A1z... --limit 10 --json
`.trim();

interface Args {
  address?: string;
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
    } else if (arg === "--limit" && args[i + 1]) {
      result.limit = parseInt(args[++i], 10);
    } else if (!arg.startsWith("--") && !result.address) {
      result.address = arg;
    }
    i++;
  }

  return result;
}

function formatPost(post: BmapPost, index: number): string {
  const txid = post.tx.h;
  const time = post.blk?.t ? new Date(post.blk.t * 1000).toISOString() : "unconfirmed";
  const content = post.B?.[0]?.content || "";
  const author = post.AIP?.[0]?.address || "unknown";

  return `[${index + 1}] ${txid.substring(0, 8)}...
    Time: ${time}
    Author: ${author}
    Content: ${content.substring(0, 100)}${content.length > 100 ? "..." : ""}`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || !args.address) {
    console.log(HELP);
    process.exit(args.help ? 0 : 1);
  }

  try {
    const query = buildPostsQuery(args.address, args.limit);
    const posts = await queryBmap("post", query);

    if (args.json) {
      console.log(
        JSON.stringify(
          posts.map((p) => ({
            txid: p.tx.h,
            time: p.blk?.t,
            content: p.B?.[0]?.content,
            author: p.AIP?.[0]?.address,
          })),
          null,
          2
        )
      );
    } else {
      if (posts.length === 0) {
        console.log(`No posts found for ${args.address}`);
      } else {
        console.log(`Posts from ${args.address}:\n`);
        posts.forEach((post, i) => console.log(formatPost(post, i)));
      }
    }
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Error: ${message}`);
    process.exit(1);
  }
}

main();
