#!/usr/bin/env bun

import { PrivateKey, Transaction, Script, Utils } from "@bsv/sdk";
import { fundAndBroadcast } from "../lib/broadcast.js";

const MAP_PREFIX = "1PuQa7K62MiKCtssSLKy1kh56WWU7MtUR5";
const AIP_PREFIX = "15PciHG22SNLQJXMoSUaWVi7WSqc7hCfva";

const HELP = `
create-repost - Repost content on the BSV blockchain

USAGE:
  bun run create-repost.ts <wif> <txid> [options]

OPTIONS:
  --context <type>    New context (topic, url, channel)
  --value <value>     Context value
  --dry-run           Build tx but don't broadcast
  --json              Output JSON format
  -h, --help          Show this help

EXAMPLES:
  bun run create-repost.ts L1... abc123...
  bun run create-repost.ts L1... abc123... --context channel --value general
`.trim();

interface Args {
  wif?: string;
  txid?: string;
  context?: string;
  contextValue?: string;
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
    } else if (arg === "--context" && args[i + 1]) {
      result.context = args[++i];
    } else if (arg === "--value" && args[i + 1]) {
      result.contextValue = args[++i];
    } else if (!arg.startsWith("--") && !result.wif) {
      result.wif = arg;
    } else if (!arg.startsWith("--") && !result.txid) {
      result.txid = arg;
    }
    i++;
  }

  return result;
}

function textToHex(text: string): string {
  const bytes = new TextEncoder().encode(text);
  return Array.from(bytes)
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
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

    // Build repost MAP data
    const mapData = [
      MAP_PREFIX,
      "SET",
      "app",
      "bsocial",
      "type",
      "repost",
      "tx",
      args.txid,
    ];

    if (args.context && args.contextValue) {
      mapData.push("context", args.context, args.context, args.contextValue);
    }

    // Build OP_RETURN script
    const asmParts = mapData.map((d) => textToHex(d)).join(" ");
    const lockingScript = Script.fromASM(`OP_0 OP_RETURN ${asmParts}`);

    const tx = new Transaction();
    tx.addOutput({
      satoshis: 0,
      lockingScript,
    });

    if (args.dryRun) {
      const result = {
        status: "dry-run",
        reposting: args.txid,
        context: args.context,
        contextValue: args.contextValue,
        txSize: tx.toBinary().length,
      };
      if (args.json) {
        console.log(JSON.stringify(result, null, 2));
      } else {
        console.log(`Dry run - would repost: ${args.txid}`);
        console.log(`TX size: ${result.txSize} bytes`);
      }
      process.exit(0);
    }

    const txid = await fundAndBroadcast(tx, privateKey);

    if (args.json) {
      console.log(JSON.stringify({ txid, reposted: args.txid }, null, 2));
    } else {
      console.log(`Reposted: ${txid}`);
    }
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Error: ${message}`);
    process.exit(1);
  }
}

main();
