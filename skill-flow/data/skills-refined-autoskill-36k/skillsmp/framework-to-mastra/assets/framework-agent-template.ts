/**
 * Framework Agent Template (Mastra v1 Beta)
 *
 * Template for converting an operating-framework skill into a Mastra agent.
 *
 * Customization points marked with {{PLACEHOLDER}}:
 * - {{FRAMEWORK_NAME}}: kebab-case framework identifier
 * - {{FRAMEWORK_TITLE}}: Human-readable framework name
 * - {{DIAGNOSTIC_STATES}}: Formatted list of diagnostic states
 * - {{TOOL_IMPORTS}}: Import statements for framework tools
 * - {{TOOLS_OBJECT}}: Object of available tools
 */

import { Agent } from "@mastra/core/agent";
import { openai } from "@ai-sdk/openai";

// {{TOOL_IMPORTS}}
// Example:
// import { assessStateTool } from "../tools/assess-state.js";
// import { runPhase0Tool } from "../tools/run-phase0.js";

export const {{FRAMEWORK_NAME}}Agent = new Agent({
  name: "{{FRAMEWORK_NAME}}-agent",

  // Dynamic instructions can access runtimeContext
  instructions: ({ runtimeContext }) => {
    const userId = runtimeContext?.get("user-id") || "unknown";
    const sessionTopic = runtimeContext?.get("topic") || "general";

    return `You are a {{FRAMEWORK_TITLE}} expert agent.

Your role is to:
1. Diagnose the current state of the user's situation
2. Recommend appropriate interventions based on framework methodology
3. Guide users through the framework's process phases
4. Track progress and maintain context across sessions

## Diagnostic States

You assess situations against these states:

{{DIAGNOSTIC_STATES}}

## Process

When helping users:
1. First assess which diagnostic state applies
2. Explain the assessment with evidence (which symptoms matched)
3. Recommend the appropriate intervention
4. Guide them through the intervention steps
5. Re-assess after intervention to confirm progress

## Guidelines

- Always explain your reasoning
- Provide concrete, actionable next steps
- Use the framework's vocabulary precisely
- Check for prior work before starting fresh
- Signal confidence levels explicitly

## Current Context

User: ${userId}
Topic: ${sessionTopic}

Start by understanding the user's current situation, then diagnose and guide.`;
  },

  // Model configuration
  model: openai("gpt-4o-mini"),

  // Alternative: model with fallbacks
  // model: [
  //   { model: "openai/gpt-4o", maxRetries: 3 },
  //   { model: "anthropic/claude-3-5-sonnet", maxRetries: 2 },
  // ],

  // Framework tools
  tools: {
    // {{TOOLS_OBJECT}}
    // Example:
    // assessStateTool,
    // runPhase0Tool,
    // buildVocabularyTool,
    // retrievePriorWorkTool,
  },
});

/*
// Usage example:

import { Mastra } from "@mastra/core/mastra";
import { RuntimeContext } from "@mastra/core";

const mastra = new Mastra({
  agents: { {{FRAMEWORK_NAME}}Agent },
});

// With runtime context
const runtimeContext = new RuntimeContext();
runtimeContext.set("user-id", "user-123");
runtimeContext.set("topic", "gentrification of workwear");

const response = await {{FRAMEWORK_NAME}}Agent.generate(
  "I'm researching this topic but keep finding surface-level content",
  {
    runtimeContext,
    memory: {
      thread: "research-user-123-gentrification-of-workwear",
      resource: "user-123",
    },
  }
);

console.log(response.text);
*/
