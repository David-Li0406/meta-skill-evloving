/**
 * @fileoverview Summary generation utilities for Climpt Agent
 * @module climpt-plugins/skills/delegate-climpt-agent/scripts/summary
 */

import { query } from "npm:@anthropic-ai/claude-agent-sdk";

/**
 * Read JSONL log and extract assistant messages
 */
export async function extractAssistantMessages(
  logPath: string,
): Promise<string[]> {
  const messages: string[] = [];
  const logContent = await Deno.readTextFile(logPath);

  for (const line of logContent.split("\n")) {
    if (!line.trim()) continue;

    try {
      const entry = JSON.parse(line);
      if (entry.level === "assistant") {
        messages.push(entry.message);
      }
    } catch {
      // Skip invalid JSON lines
    }
  }

  return messages;
}

/**
 * Generate summary of sub-agent execution using LLM
 */
export async function generateSummary(
  messages: string[],
  subAgentName: string,
): Promise<string> {
  const prompt =
    `Based on the following messages from a sub-agent task (${subAgentName}), provide a concise summary:

1. What was accomplished?
2. What are the key results or next steps?

Keep the summary brief and actionable.

Messages:
${messages.join("\n\n")}`;

  const queryResult = query({
    prompt,
    options: {
      model: "claude-sonnet-4-5-20250929",
      allowedTools: [], // No tools needed for summary
      systemPrompt:
        "You are a helpful assistant that summarizes task execution results concisely.",
    },
  });

  let summaryText = "";
  for await (const message of queryResult) {
    if (message.type === "assistant" && message.message.content) {
      for (const block of message.message.content) {
        if (block.type === "text") {
          summaryText += block.text;
        }
      }
    }
  }

  return summaryText;
}
