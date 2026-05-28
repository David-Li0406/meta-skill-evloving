/**
 * @fileoverview CLI argument parsing for Climpt Agent
 * @module climpt-plugins/skills/delegate-climpt-agent/scripts/cli
 */

import type { CliArgs } from "./types.ts";

/**
 * Parse command line arguments
 */
export function parseArgs(args: string[]): CliArgs {
  const result: CliArgs = {
    agent: "climpt",
    options: [],
  };

  for (const arg of args) {
    if (arg.startsWith("--action=")) {
      result.action = arg.slice(9);
    } else if (arg.startsWith("--target=")) {
      result.target = arg.slice(9);
    } else if (arg.startsWith("--intent=")) {
      result.intent = arg.slice(9);
    } else if (arg.startsWith("--agent=")) {
      result.agent = arg.slice(8);
    } else if (arg.startsWith("--options=")) {
      result.options = arg.slice(10).split(",");
    }
  }

  return result;
}

/**
 * Validate CLI arguments and exit if invalid
 *
 * Requires both --action and --target parameters
 */
export function validateArgs(
  args: CliArgs,
): asserts args is CliArgs & { action: string; target: string } {
  if (!args.action || !args.target) {
    displayHelp();
    Deno.exit(1);
  }
}

/**
 * Display help message
 */
export function displayHelp(): void {
  // deno-lint-ignore no-console
  console.error(
    "Usage: climpt-agent.ts --action=... --target=... [--intent=...] [--agent=...] [--options=...]",
  );
  // deno-lint-ignore no-console
  console.error("");
  // deno-lint-ignore no-console
  console.error("Required Parameters:");
  // deno-lint-ignore no-console
  console.error(
    "  --action   Action-focused query (what to do, e.g., 'execute test')",
  );
  // deno-lint-ignore no-console
  console.error(
    "  --target   Target-focused query (what to act on, e.g., 'specific file')",
  );
  // deno-lint-ignore no-console
  console.error("");
  // deno-lint-ignore no-console
  console.error("Optional Parameters:");
  // deno-lint-ignore no-console
  console.error(
    "  --intent   Detailed description for option resolution (defaults to action+target)",
  );
  // deno-lint-ignore no-console
  console.error('  --agent    Agent name (default: "climpt")');
  // deno-lint-ignore no-console
  console.error("  --options  Comma-separated list of options");
  // deno-lint-ignore no-console
  console.error("");
  // deno-lint-ignore no-console
  console.error("Example:");
  // deno-lint-ignore no-console
  console.error(
    '  climpt-agent.ts --action="execute test" --target="specific file unit test"',
  );
}
