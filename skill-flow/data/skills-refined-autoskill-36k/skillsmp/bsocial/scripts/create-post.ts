#!/usr/bin/env bun

import { PrivateKey, Transaction } from "@bsv/sdk";
import BSocial, { BSocialActionType, BSocialContext, type BSocialPost } from "@bopen-io/templates/template/bsocial/BSocial.ts";
import { fundAndBroadcast } from "../lib/broadcast.js";

const HELP = `
create-post - Create a BSocial post on the BSV blockchain

USAGE:
  bun run create-post.ts <wif> "Post content" [options]

OPTIONS:
  --channel <name>    Post to a specific channel
  --url <url>         Associate with a URL
  --tags <t1,t2>      Comma-separated tags
  --dry-run           Build tx but don't broadcast
  --json              Output JSON format
  -h, --help          Show this help

EXAMPLES:
  bun run create-post.ts L1... "Hello BSV!"
  bun run create-post.ts L1... "Check this out" --url https://example.com
  bun run create-post.ts L1... "Announcement" --channel announcements
  bun run create-post.ts L1... "Tagged post" --tags bsv,blockchain
`.trim();

interface Args {
  wif?: string;
  content?: string;
  channel?: string;
  url?: string;
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
    } else if (arg === "--channel" && args[i + 1]) {
      result.channel = args[++i];
    } else if (arg === "--url" && args[i + 1]) {
      result.url = args[++i];
    } else if (arg === "--tags" && args[i + 1]) {
      result.tags = args[++i].split(",").map((t) => t.trim());
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

    // Build post action
    const post: BSocialPost = {
      app: "bsocial",
      type: BSocialActionType.POST,
      content: args.content,
      mediaType: "text/plain",
      encoding: "utf-8",
    };

    // Add context if specified
    if (args.channel) {
      post.context = BSocialContext.CHANNEL;
      post.contextValue = args.channel;
    } else if (args.url) {
      post.context = "url" as BSocialContext;
      post.contextValue = args.url;
    }

    // Create locking script using BSocial template
    const lockingScript = await BSocial.createPost(post, args.tags, privateKey);

    // Build transaction with OP_RETURN output
    const tx = new Transaction();
    tx.addOutput({
      satoshis: 0,
      lockingScript,
    });

    if (args.dryRun) {
      const result = {
        status: "dry-run",
        txSize: tx.toBinary().length,
        content: args.content,
        channel: args.channel,
        url: args.url,
        tags: args.tags,
      };

      if (args.json) {
        console.log(JSON.stringify(result, null, 2));
      } else {
        console.log("Dry run - transaction not broadcast");
        console.log(`Content: ${args.content}`);
        console.log(`TX size: ${result.txSize} bytes`);
        if (args.channel) console.log(`Channel: ${args.channel}`);
        if (args.url) console.log(`URL: ${args.url}`);
        if (args.tags) console.log(`Tags: ${args.tags.join(", ")}`);
      }
      process.exit(0);
    }

    // Fund and broadcast
    const txid = await fundAndBroadcast(tx, privateKey);

    if (args.json) {
      console.log(JSON.stringify({ txid, content: args.content }, null, 2));
    } else {
      console.log(`Post created: ${txid}`);
    }
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Error: ${message}`);
    process.exit(1);
  }
}

main();
