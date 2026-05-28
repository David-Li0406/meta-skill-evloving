// deno-lint-ignore-file prefer-ascii no-await-in-loop
/**
 * @fileoverview Sub-agent execution for Climpt Agent
 * @module climpt-plugins/skills/delegate-climpt-agent/scripts/sub-agent
 */

import { query } from "npm:@anthropic-ai/claude-agent-sdk";
import type { Options, SDKMessage } from "npm:@anthropic-ai/claude-agent-sdk";

import type { Logger } from "./logger.ts";
import { resolvePluginPathsSafe } from "../../../../lib/plugin-resolver.ts";

/**
 * Run Claude Agent SDK with the obtained prompt
 *
 * Note: When running from Claude Code's sandbox, the parent sandbox restrictions
 * are inherited. The SDK's sandbox option only controls the child's command execution,
 * not the parent sandbox. To run this script from Claude Code, you must use:
 *   Bash tool with dangerouslyDisableSandbox: true
 */
export async function runSubAgent(
  agentName: string,
  prompt: string,
  cwd: string,
  logger: Logger,
): Promise<void> {
  // Resolve dynamic plugins from settings
  const dynamicPlugins = await resolvePluginPathsSafe(
    cwd,
    async (error: Error, message: string) => {
      await logger.writeError(`${message}: ${error.message}`);
    },
  );

  if (dynamicPlugins.length > 0) {
    await logger.write(
      `Dynamic plugins resolved: ${
        dynamicPlugins.map((p) => p.path).join(", ")
      }`,
    );
  }

  const options: Options = {
    // model: 省略 = 親エージェントから継承（意図的）
    cwd,
    settingSources: ["project"],
    allowedTools: [
      "Skill",
      "Read",
      "Write",
      "Edit",
      "Bash",
      "Glob",
      "Grep",
      "Task",
    ],
    systemPrompt: {
      type: "preset",
      preset: "claude_code",
    },
    plugins: dynamicPlugins.length > 0 ? dynamicPlugins : undefined,
  };

  await logger.write(`Starting sub-agent: ${agentName}`);

  const queryResult = query({
    prompt,
    options,
  });

  // Check if SDK JSON errors should be strictly handled
  // Set STRICT_SDK_JSON=1 to throw on JSON parse errors instead of ignoring
  const strictJsonMode = Deno.env.get("STRICT_SDK_JSON") === "1";

  try {
    for await (const message of queryResult) {
      try {
        await handleMessage(message, logger);
      } catch (error) {
        // SDK may emit malformed JSON during message handling
        if (error instanceof SyntaxError && error.message.includes("JSON")) {
          await logger.writeError(
            `SDK JSON parse warning in handler: ${error.message}`,
          );
          if (strictJsonMode) {
            throw error;
          }
          continue;
        }
        throw error;
      }
    }
  } catch (error) {
    // SDK may emit malformed JSON during streaming iteration (typically at stream end)
    if (error instanceof SyntaxError && error.message.includes("JSON")) {
      await logger.writeError(
        `SDK JSON parse error in stream (task may have completed): ${error.message}`,
      );
      if (strictJsonMode) {
        throw error;
      }
      return;
    }
    throw error;
  }
}

/**
 * Handle SDK message types
 *
 * SDKMessage types per SDK documentation:
 * - assistant: Model response with content blocks
 * - result: Task completion (success/error)
 * - system: Initialization info
 * - user: User message echo (ignored)
 * - stream_event: Partial streaming data (ignored)
 * - compact_boundary: Context compaction marker (ignored)
 *
 * @internal Exported for testing
 */
export async function handleMessage(
  message: SDKMessage,
  logger: Logger,
): Promise<void> {
  switch (message.type) {
    case "assistant":
      if (message.message.content) {
        for (const block of message.message.content) {
          if (block.type === "text") {
            await logger.writeAssistant(block.text);
          }
        }
      }
      break;

    case "result": {
      if (message.subtype === "success") {
        await logger.writeResult("success", message.total_cost_usd);
      } else {
        const errors = (message as { errors?: string[] }).errors ?? [];
        await logger.writeResult("error", undefined, { errors });
      }
      break;
    }

    case "system":
      if (message.subtype === "init") {
        const msg = message as {
          session_id: string;
          model: string;
          permissionMode?: string;
          mcp_servers?: Array<{ name: string; status: string }>;
          tools?: string[];
        };
        await logger.writeSystem(
          `Session: ${msg.session_id}, Model: ${msg.model}`,
          {
            permissionMode: msg.permissionMode,
            mcp_servers: msg.mcp_servers,
          },
        );
      }
      break;

    case "user":
      // User message echo - no action needed
      break;

    default:
      // Handle unknown/new message types gracefully
      break;
  }
}
