#!/usr/bin/env -S deno run --allow-read --allow-write --allow-net --allow-env --allow-run --allow-sys
// deno-lint-ignore-file no-console no-await-in-loop

/**
 * @fileoverview Climpt Agent - Multi-stage workflow sub-agent builder
 * @module climpt-plugins/skills/delegate-climpt-agent/scripts/climpt-agent
 *
 * This script implements a multi-stage workflow:
 * 1. Receives a natural language query describing the task
 * 2. Searches the command registry using shared MCP utilities
 * 3. Gets command details (describe)
 * 4. Resolves options using LLM (NEW: based on option-handling design)
 * 5. Executes the command to get the instruction prompt
 * 6. Runs a sub-agent using Claude Agent SDK with the prompt
 */

import { join } from "@std/path";

// Local modules
import { parseArgs, validateArgs } from "./climpt-agent/cli.ts";
import {
  generateSubAgentName,
  getClimptPrompt,
} from "./climpt-agent/command.ts";
import { Logger } from "./climpt-agent/logger.ts";
import {
  extractStdinFromOptions,
  needsOptionResolution,
  resolveOptions,
  toCLIArgs,
} from "./climpt-agent/options-prompt.ts";
import { runSubAgent } from "./climpt-agent/sub-agent.ts";
import {
  extractAssistantMessages,
  generateSummary,
} from "./climpt-agent/summary.ts";
import type {
  ClimptCommand,
  CommandWithUV,
  PromptContext,
} from "./climpt-agent/types.ts";

// Plugin's shared library
import {
  describeCommand,
  loadMCPConfig,
  loadRegistryForAgent,
  searchWithRRF,
} from "../../../lib/mod.ts";

// =============================================================================
// Sandbox Detection
// =============================================================================

/**
 * Check if running in Claude Code sandbox mode by attempting network connection.
 * When stdin is piped, Claude Agent SDK requires network access which fails in sandbox.
 *
 * @throws Error with clear message if sandbox is detected with piped stdin
 */
async function checkSandboxWithPipedStdin(
  hasPipedStdin: boolean,
): Promise<void> {
  if (!hasPipedStdin) {
    return; // No stdin piped, skip check
  }

  try {
    // Attempt lightweight TCP connection to detect sandbox restrictions
    const conn = await Deno.connect({
      hostname: "api.anthropic.com",
      port: 443,
    });
    conn.close();
  } catch {
    // Any connection error to api.anthropic.com when stdin is piped
    // indicates sandbox restrictions - fail fast with clear guidance
    console.error("ERROR: Stdin is piped but running in sandbox mode.");
    console.error("");
    console.error(
      "Claude Agent SDK requires network access. Please invoke with:",
    );
    console.error("  dangerouslyDisableSandbox: true");
    console.error("");
    console.error("Example:");
    console.error(
      '  Bash({ command: "echo ... | deno run ...", dangerouslyDisableSandbox: true })',
    );
    Deno.exit(1);
  }
}

// =============================================================================
// Stdin Reading
// =============================================================================

/**
 * Read all content from stdin if piped (not interactive terminal)
 *
 * @returns stdin content or undefined if stdin is a terminal
 */
async function readStdinIfPiped(): Promise<string | undefined> {
  // If stdin is a terminal (interactive), don't read
  if (Deno.stdin.isTerminal()) {
    return undefined;
  }

  // Read all content from piped stdin using getReader() for TypeScript compatibility
  const chunks: Uint8Array[] = [];
  const reader = Deno.stdin.readable.getReader();
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
    }
  } finally {
    reader.releaseLock();
  }

  if (chunks.length === 0) {
    return undefined;
  }

  const totalLength = chunks.reduce((sum, chunk) => sum + chunk.length, 0);
  const combined = new Uint8Array(totalLength);
  let offset = 0;
  for (const chunk of chunks) {
    combined.set(chunk, offset);
    offset += chunk.length;
  }

  return new TextDecoder().decode(combined);
}

// =============================================================================
// Main Workflow
// =============================================================================

/**
 * Main entry point - Multi-stage workflow
 *
 * Uses shared MCP utilities from climpt package:
 * - searchCommands(): Find matching command using cosine similarity
 * - describeCommand(): Get command details
 *
 * New: Uses LLM to resolve options based on user intent
 */
async function main(): Promise<void> {
  // Read stdin early (before any other async operations)
  const pipedStdinContent = await readStdinIfPiped();

  // Check sandbox restrictions when stdin is piped (fails fast with clear error)
  await checkSandboxWithPipedStdin(pipedStdinContent !== undefined);

  const args = parseArgs(Deno.args);
  validateArgs(args);

  // Initialize logger (JSONL format in tmp/logs/climpt-agents/)
  const cwd = Deno.cwd();
  const logDir = join(cwd, "tmp", "logs", "climpt-agents");
  const logger = new Logger();
  await logger.init(logDir);

  try {
    // Log parameters
    await logger.write(`Action: "${args.action}"`);
    await logger.write(`Target: "${args.target}"`);
    await logger.write(
      `Intent: "${args.intent || `${args.action} ${args.target}`}"`,
    );
    await logger.write(`Agent: ${args.agent}`);
    await logger.write(`CWD: ${cwd}`);
    await logger.write(
      `Piped stdin: ${
        pipedStdinContent ? `${pipedStdinContent.length} bytes` : "none"
      }`,
    );

    // Step 1: Load configuration and registry
    const mcpConfig = await loadMCPConfig();
    const commands = await loadRegistryForAgent(mcpConfig, args.agent);

    if (commands.length === 0) {
      await logger.writeError(`No commands found for agent '${args.agent}'`);
      console.log(`No commands found for agent '${args.agent}'`);
      Deno.exit(1);
    }

    await logger.write(`Found ${commands.length} commands in registry`);

    // Step 2: Search for matching commands using RRF
    const searchResults = searchWithRRF(commands, [args.action, args.target]);
    if (searchResults.length === 0) {
      await logger.writeError(
        `No matching commands found for action="${args.action}", target="${args.target}"`,
      );
      console.log(
        `No matching commands found for action="${args.action}", target="${args.target}"`,
      );
      Deno.exit(1);
    }
    const bestMatch = searchResults[0];

    await logger.write(
      `Best match: ${bestMatch.c1} ${bestMatch.c2} ${bestMatch.c3} (RRF score: ${
        bestMatch.score.toFixed(6)
      }, ranks: [${bestMatch.ranks.join(", ")}])`,
      { description: bestMatch.description },
    );

    if (searchResults.length > 1) {
      const otherCandidates = searchResults.slice(1).map((r) => ({
        command: `${r.c1} ${r.c2} ${r.c3}`,
        score: r.score,
        ranks: r.ranks,
      }));
      await logger.write("Other candidates", { candidates: otherCandidates });
    }

    // Step 3: Describe the command
    const matchedCommands = describeCommand(
      commands,
      bestMatch.c1,
      bestMatch.c2,
      bestMatch.c3,
    );

    if (matchedCommands.length === 0) {
      await logger.writeError("Command not found after describe");
      console.log("Command not found");
      Deno.exit(1);
    }

    const matchedCommand = matchedCommands[0] as CommandWithUV;

    if (matchedCommand.options) {
      await logger.write("Available options", {
        options: matchedCommand.options,
        uv: matchedCommand.uv,
      });
    }

    // Step 3.5: Resolve options using LLM (NEW)
    let resolvedCLIArgs: string[] = [];
    let llmGeneratedStdin: string | undefined;

    if (needsOptionResolution(matchedCommand)) {
      await logger.write("Command needs option resolution via LLM");

      const context: PromptContext = {
        workingDir: cwd,
        // files could be extracted from args or cwd in the future
      };

      // Use intent for option resolution, fallback to action+target
      const intent = args.intent || `${args.action} ${args.target}`;

      const resolvedOptions = await resolveOptions(
        matchedCommand,
        intent,
        context,
        logger,
      );

      // toCLIArgs excludes stdin (it must be piped, not passed as CLI arg)
      resolvedCLIArgs = toCLIArgs(resolvedOptions);
      llmGeneratedStdin = extractStdinFromOptions(resolvedOptions);

      await logger.write("Resolved CLI args", { args: resolvedCLIArgs });
      if (llmGeneratedStdin) {
        await logger.write("LLM generated stdin content", {
          length: llmGeneratedStdin.length,
        });
      }
    }

    // Step 4: Create command and execute
    // Determine stdin content:
    // 1. Priority: piped stdin (if command expects stdin and piped content exists)
    // 2. Fallback: LLM-generated stdin (if command expects stdin and no piped content)
    let stdinContent: string | undefined;
    if (matchedCommand.options?.stdin) {
      if (pipedStdinContent) {
        stdinContent = pipedStdinContent;
        await logger.write("Using piped stdin content");
      } else if (llmGeneratedStdin) {
        stdinContent = llmGeneratedStdin;
        await logger.write("Using LLM-generated stdin content");
      }
    }

    // CLI args from user override LLM-resolved args
    const cmd: ClimptCommand = {
      agent: args.agent,
      c1: bestMatch.c1,
      c2: bestMatch.c2,
      c3: bestMatch.c3,
      options: [...resolvedCLIArgs, ...args.options],
    };

    const subAgentName = generateSubAgentName(cmd);
    await logger.write(`Sub-agent name: ${subAgentName}`);

    await logger.write(
      `Fetching prompt: climpt --config=${cmd.c1} ${cmd.c2} ${cmd.c3}`,
      { options: cmd.options, hasStdin: !!stdinContent },
    );
    const prompt = await getClimptPrompt(cmd, stdinContent);

    // Log for Guimpt IDE usage statistics
    await logger.write("Climpt prompt executed", {
      type: "climpt_prompt_used",
      c1: cmd.c1,
      c2: cmd.c2,
      c3: cmd.c3,
      promptPath:
        `agent/${cmd.agent}/prompts/${cmd.c1}/${cmd.c2}/${cmd.c3}/f_default.md`,
    });

    await logger.writeSection("PROMPT", prompt);

    // Step 6: Run sub-agent
    await runSubAgent(subAgentName, prompt, cwd, logger);

    // Step 7: Generate and print summary
    const summary = logger.getSummary();

    if (summary.status === "success") {
      const assistantMessages = await extractAssistantMessages(
        logger.getLogPath(),
      );
      const summaryText = await generateSummary(
        assistantMessages,
        subAgentName,
      );

      console.log(`${subAgentName}`);
      console.log(summaryText);
    } else {
      console.log(`${subAgentName}: ${summary.status}`);
    }

    await logger.write(`Summary printed to stdout`);
  } finally {
    await logger.close();
  }
}

// Execute main
if (import.meta.main) {
  const logger = new Logger();
  main().catch(async (error) => {
    await logger.writeError(error.message, { stack: error.stack });
    console.log(`Error: ${error.message}`);
    console.log(`Log: ${logger.getLogPath()}`);
    await logger.close();
    Deno.exit(1);
  });
}
