#!/usr/bin/env bun
/**
 * parse-message.ts - Parse Stratum v1 JSON-RPC messages
 * Usage: bun run parse-message.ts <json-message> [--json]
 */

const args = process.argv.slice(2);

function showHelp(): void {
  console.log(`Usage: bun run parse-message.ts <json-message> [options]

Parse Stratum v1 JSON-RPC messages.

Options:
  --json                  Output as JSON
  --help, -h              Show this help message

Examples:
  bun run parse-message.ts '{"id":1,"method":"mining.subscribe","params":["Agent/1.0"]}'
  bun run parse-message.ts '{"id":1,"result":[[["mining.notify","ae6812eb"]],"08000002",4]}' --json

Supported Methods:
  mining.subscribe    - Subscribe to mining notifications
  mining.authorize    - Authorize worker
  mining.notify       - New job notification
  mining.submit       - Submit share
  mining.set_difficulty - Set target difficulty`);
}

if (args.includes("--help") || args.includes("-h")) {
  showHelp();
  process.exit(0);
}

const jsonOutput = args.includes("--json");
const messageArg = args.find((arg) => !arg.startsWith("-"));

if (!messageArg) {
  console.error("Error: No message provided");
  console.error("Usage: bun run parse-message.ts <json-message>");
  process.exit(1);
}

interface StratumMessage {
  id?: number | null;
  method?: string;
  params?: unknown[];
  result?: unknown;
  error?: unknown;
}

let message: StratumMessage;
try {
  message = JSON.parse(messageArg);
} catch {
  console.error("Error: Invalid JSON message");
  process.exit(1);
}

// Determine message type
let messageType: string;
if (message.method) {
  messageType = message.id !== null && message.id !== undefined ? "request" : "notification";
} else if (message.result !== undefined || message.error !== undefined) {
  messageType = "response";
} else {
  console.error("Error: Unrecognized message format");
  process.exit(1);
}

// Method descriptions
const methodDescriptions: Record<string, string> = {
  "mining.subscribe": "Subscribe to mining notifications",
  "mining.authorize": "Authorize worker credentials",
  "mining.notify": "New mining job notification",
  "mining.submit": "Submit a share",
  "mining.set_difficulty": "Set share difficulty target",
  "mining.set_extranonce": "Update extranonce values",
  "mining.configure": "Configure connection options",
};

const result = {
  type: messageType,
  id: message.id,
  method: message.method || null,
  methodDescription: message.method ? (methodDescriptions[message.method] || "Unknown method") : null,
  params: message.params || null,
  result: message.result !== undefined ? message.result : null,
  error: message.error || null,
};

if (jsonOutput) {
  console.log(JSON.stringify(result, null, 2));
} else {
  console.log(`Message Type: ${messageType}`);
  if (message.id !== undefined) {
    console.log(`ID: ${message.id}`);
  }
  if (message.method) {
    console.log(`Method: ${message.method}`);
    console.log(`Description: ${result.methodDescription}`);
  }
  if (message.params) {
    console.log(`Parameters: ${JSON.stringify(message.params)}`);
  }
  if (message.result !== undefined) {
    console.log(`Result: ${JSON.stringify(message.result)}`);
  }
  if (message.error) {
    console.log(`Error: ${JSON.stringify(message.error)}`);
  }
}
