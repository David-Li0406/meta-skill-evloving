/**
 * @fileoverview Command execution utilities for Climpt Agent
 * @module climpt-plugins/skills/delegate-climpt-agent/scripts/command
 */

import type { ClimptCommand } from "./types.ts";

/**
 * Generate sub-agent name following C3L naming convention
 *
 * Format: <agent>-<c1>-<c2>-<c3>
 * Example: climpt-git-group-commit-unstaged-changes
 */
export function generateSubAgentName(cmd: ClimptCommand): string {
  return `${cmd.agent}-${cmd.c1}-${cmd.c2}-${cmd.c3}`;
}

/**
 * Execute Climpt command via CLI and get the instruction prompt
 *
 * @param cmd - Command parameters
 * @param stdinContent - Optional stdin content to pass to the command
 * @returns The instruction prompt from Climpt
 */
export async function getClimptPrompt(
  cmd: ClimptCommand,
  stdinContent?: string,
): Promise<string> {
  const configParam = cmd.agent === "climpt"
    ? cmd.c1
    : `${cmd.agent}-${cmd.c1}`;

  const commandArgs = [
    "run",
    "--allow-read",
    "--allow-write",
    "--allow-env",
    "--allow-run",
    "--allow-net",
    "--no-config",
    "jsr:@aidevtool/climpt",
    `--config=${configParam}`,
    cmd.c2,
    cmd.c3,
  ];

  if (cmd.options?.length) {
    commandArgs.push(...cmd.options);
  }

  if (stdinContent) {
    // stdin content provided: use spawn + write + close pattern
    const process = new Deno.Command("deno", {
      args: commandArgs,
      stdout: "piped",
      stderr: "piped",
      stdin: "piped",
    });

    const child = process.spawn();

    // Write stdin content and close to send EOF
    const writer = child.stdin.getWriter();
    await writer.write(new TextEncoder().encode(stdinContent));
    await writer.close();

    const { stdout, stderr, code } = await child.output();

    if (code !== 0) {
      const errorText = new TextDecoder().decode(stderr);
      throw new Error(`Climpt execution failed: ${errorText}`);
    }

    return new TextDecoder().decode(stdout);
  } else {
    // No stdin content: use simple output() which defaults stdin to "null"
    const process = new Deno.Command("deno", {
      args: commandArgs,
      stdout: "piped",
      stderr: "piped",
    });

    const { stdout, stderr, code } = await process.output();

    if (code !== 0) {
      const errorText = new TextDecoder().decode(stderr);
      throw new Error(`Climpt execution failed: ${errorText}`);
    }

    return new TextDecoder().decode(stdout);
  }
}
