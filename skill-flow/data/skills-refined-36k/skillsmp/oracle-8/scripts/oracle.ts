#!/usr/bin/env bun
/**
 * Oracle - Strategic Technical Advisor
 * Uses Codex TypeScript SDK with GPT-5.2 and streaming output
 */

import { Codex, type ThreadEvent, type ThreadItem } from "@openai/codex-sdk";
import { readFileSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

// Determine skill directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SKILL_DIR = process.env.CLAUDE_PLUGIN_ROOT
  ? join(process.env.CLAUDE_PLUGIN_ROOT, "skills/oracle")
  : dirname(__dirname);

// Read system prompt
const systemPrompt = readFileSync(
  join(SKILL_DIR, "system-prompt.txt"),
  "utf-8"
);

// Get user question from args
const userQuestion = process.argv.slice(2).join(" ");

if (!userQuestion) {
  console.error("Usage: oracle.ts <question>");
  console.error(
    'Example: oracle.ts "What is the best approach for implementing rate limiting?"'
  );
  process.exit(1);
}

// Initialize Codex
const codex = new Codex();

// Start a new thread with configuration
const thread = codex.startThread({
  model: "gpt-5.2",
  modelReasoningEffort: "xhigh",
  approvalPolicy: "never",
  sandboxMode: "read-only",
  skipGitRepoCheck: true,
  webSearchEnabled: true,
});

// Build prompt
const prompt = `${systemPrompt}\n\n---\nUser Question: ${userQuestion}`;

// Track final response from agent messages
let finalResponse = "";

/**
 * Get a display name for an item
 */
function getItemDisplay(item: ThreadItem): string {
  switch (item.type) {
    case "agent_message":
      return "thinking";
    case "reasoning":
      return "reasoning";
    case "command_execution":
      return `exec: ${item.command.slice(0, 40)}`;
    case "web_search":
      return `search: ${item.query.slice(0, 30)}`;
    case "mcp_tool_call":
      return `${item.server}/${item.tool}`;
    case "file_change":
      return `files: ${item.changes.length} changes`;
    case "todo_list":
      return `todo: ${item.items.length} items`;
    case "error":
      return `error: ${item.message}`;
    default:
      return (item as any).type || "unknown";
  }
}

try {
  // Stream events for progress visibility
  const { events } = await thread.runStreamed(prompt);

  for await (const event of events) {
    switch (event.type) {
      case "thread.started":
        console.error("🔮 Oracle started...");
        break;

      case "turn.started":
        console.error("🔄 Processing...");
        break;

      case "item.started":
        console.error(`  → ${getItemDisplay(event.item)}`);
        break;

      case "item.updated":
        // Update final response from agent messages
        if (event.item.type === "agent_message") {
          finalResponse = event.item.text;
        }
        break;

      case "item.completed":
        if (event.item.type === "agent_message") {
          finalResponse = event.item.text;
          console.error("  ✓ response ready");
        } else if (event.item.type === "web_search") {
          console.error(`  ✓ search: ${event.item.query.slice(0, 30)}`);
        } else if (event.item.type === "command_execution") {
          const status = event.item.exit_code === 0 ? "✓" : "✗";
          console.error(`  ${status} ${event.item.command.slice(0, 40)}`);
        } else {
          console.error(`  ✓ ${getItemDisplay(event.item)}`);
        }
        break;

      case "turn.completed":
        console.error("✨ Complete");
        break;

      case "turn.failed":
        console.error(`❌ Turn failed: ${event.error.message}`);
        process.exit(1);
        break;

      case "error":
        console.error(`❌ Error: ${event.message}`);
        process.exit(1);
        break;
    }
  }

  // Output final response
  if (finalResponse) {
    console.log(finalResponse);
  } else {
    console.error("No response received from oracle");
    process.exit(1);
  }
} catch (error) {
  console.error(`❌ Error: ${error instanceof Error ? error.message : error}`);
  process.exit(1);
}
