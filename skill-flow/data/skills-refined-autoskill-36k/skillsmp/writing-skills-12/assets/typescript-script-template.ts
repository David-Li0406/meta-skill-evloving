#!/usr/bin/env bun
import dedent from "ts-dedent";
import { parseArgs } from "util";
import { z } from "zod";

/** Prints the help message to the console. */
function printHelp() {
  console.log(dedent`
    Usage: script-name [options]

    Description of what the script does.

    Options:

      --url <url>        URL to process (required).
      --count <number>   Number of items to process (optional, default: 10).
      --help             Show this help message and exit.
  `);
}

// Parse the arguments
const { values } = parseArgs({
  args: process.argv.slice(2),
  options: {
    url: { type: "string" },
    count: { type: "string" },
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
  url: z.url(),
  count: z.coerce.number().int().positive().optional().default(10),
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

// @ts-expect-error - Template variable that will be used when script is implemented
const options = parseResult.data;

// TODO: Implement script
