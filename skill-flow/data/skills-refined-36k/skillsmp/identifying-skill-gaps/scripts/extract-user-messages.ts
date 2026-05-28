#!/usr/bin/env bun
import { glob } from "fs/promises";
import { readFile } from "fs/promises";
import { homedir } from "os";
import { join } from "path";
import dedent from "ts-dedent";
import { parseArgs } from "util";
import { z } from "zod";

interface UserMessage {
  type: string;
  timestamp: string;
  message: {
    role: string;
    content: string | Array<{ type: string; text: string }>;
  };
}

/** Prints the help message to the console. */
function printHelp() {
  console.log(dedent`
    Usage: extract-user-messages.ts --after <date>

    Extract user messages from all Claude Code conversation logs.

    Options:

      --after <date>  Only include messages after this date in YYYY-MM-DD format (required).
      --help          Show this help message and exit.

    Example:

      extract-user-messages.ts --after 2024-12-01
  `);
}

// Parse the arguments
const { values } = parseArgs({
  args: process.argv.slice(2),
  options: {
    after: { type: "string" },
    help: { type: "boolean" },
  },
  strict: true,
});

// Handle help flag
if (values.help) {
  printHelp();
  process.exit(0);
}

// Define the arguments schema
const argumentsSchema = z.object({
  after: z.iso.date(),
});

// Validate the arguments
const parseResult = argumentsSchema.safeParse(values);

if (!parseResult.success) {
  for (const issue of parseResult.error.issues) {
    console.error(`The --${issue.path.join(".")} parameter is not valid.`);
  }

  console.error();
  printHelp();
  process.exit(1);
}

const options = parseResult.data;

function extractTextContent(content: string | Array<{ type: string; text: string }>): string {
  if (typeof content === "string") {
    return content;
  }

  return content
    .filter((item) => item.type === "text")
    .map((item) => item.text)
    .join("\n");
}

function validUserMessage(text: string): boolean {
  // Filter out empty and very short messages
  if (text.trim().length < 5) {
    return false;
  }

  // Filter out XML tags and system messages
  if (
    /<\/?local-command-caveat>/.test(text) ||
    /<\/?command-name>/.test(text) ||
    /<\/?command-message>/.test(text) ||
    /<\/?command-args>/.test(text) ||
    /<\/?local-command-stdout>/.test(text)
  ) {
    return false;
  }

  // Filter out interrupt messages
  if (text.includes("[Request interrupted by user for tool use]")) {
    return false;
  }

  // Filter out session continuation messages
  if (text.includes("continued from a previous conversation that ran out of context")) {
    return false;
  }

  return true;
}

async function processLogFile(filePath: string, afterDate: string): Promise<void> {
  const content = await readFile(filePath, "utf-8");

  const messages = content
    .trim()
    .split("\n")
    .filter((line) => line.trim())
    .map((line) => JSON.parse(line) as UserMessage)
    .filter((event) => event.type === "user" && event.message.role === "user")
    .filter((message) => message.timestamp >= afterDate);

  for (const event of messages) {
    // Extract text content
    const text = extractTextContent(event.message.content);

    // Apply filters
    if (!validUserMessage(text)) continue;

    // Output the message
    console.log(`[${event.timestamp}]`);
    console.log(text);
    console.log("---\n");
  }
}

// Find all log files
const projectsDir = join(homedir(), ".claude", "projects");
const pattern = join(projectsDir, "*", "*.jsonl");
const files = glob(pattern);

// Process each log file
for await (const filePath of files) {
  await processLogFile(filePath, options.after);
}
