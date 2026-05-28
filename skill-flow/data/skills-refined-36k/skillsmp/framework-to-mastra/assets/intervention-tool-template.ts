/**
 * Intervention Tool Template (Mastra v1 Beta)
 *
 * Template for creating intervention tools that apply framework processes.
 *
 * Customization points marked with {{PLACEHOLDER}}:
 * - {{INTERVENTION_NAME}}: kebab-case intervention identifier
 * - {{INTERVENTION_TITLE}}: Human-readable intervention name
 * - {{STATE_ID}}: State this intervention addresses
 * - {{INPUT_SCHEMA}}: Zod schema for intervention inputs
 * - {{OUTPUT_SCHEMA}}: Zod schema for intervention outputs
 * - {{INTERVENTION_PROMPT}}: Prompt template for agent execution
 */

import { createTool } from "@mastra/core/tools";
import { z } from "zod";

// Input schema for this intervention
// {{INPUT_SCHEMA}}
const InterventionInputSchema = z.object({
  topic: z.string().describe("The topic or subject for this intervention"),
  context: z
    .record(z.unknown())
    .optional()
    .describe("Additional context from prior steps"),
  priorOutput: z
    .unknown()
    .optional()
    .describe("Output from previous intervention, if chaining"),
});

// Output schema for this intervention
// {{OUTPUT_SCHEMA}}
const InterventionOutputSchema = z.object({
  success: z.boolean(),
  result: z.unknown(), // Replace with specific schema
  nextState: z.string().optional().describe("Recommended next state to assess"),
  followUpActions: z.array(z.string()),
  metadata: z.object({
    executedAt: z.string().datetime(),
    durationMs: z.number(),
  }),
});

/**
 * {{INTERVENTION_TITLE}} intervention tool.
 * Addresses state {{STATE_ID}}.
 */
export const {{INTERVENTION_NAME}}Tool = createTool({
  id: "{{INTERVENTION_NAME}}",
  description:
    "Execute {{INTERVENTION_TITLE}} intervention. " +
    "Use when state {{STATE_ID}} is identified. " +
    "Produces [describe output] which enables [next step].",
  inputSchema: InterventionInputSchema,
  outputSchema: InterventionOutputSchema,
  execute: async (inputData, context) => {
    const { topic, context: additionalContext, priorOutput } = inputData;
    const { mastra, runtimeContext, abortSignal } = context;

    const startTime = Date.now();

    // Check abort signal
    if (abortSignal?.aborted) {
      throw new Error("Intervention aborted");
    }

    // Get specialized agent for this intervention
    const agent = mastra?.getAgent("{{INTERVENTION_NAME}}-agent");

    if (!agent) {
      throw new Error("Intervention agent not found: {{INTERVENTION_NAME}}-agent");
    }

    // Build intervention prompt
    // {{INTERVENTION_PROMPT}}
    const prompt = `Execute {{INTERVENTION_TITLE}} for topic: ${topic}

${priorOutput ? `Prior step output:\n${JSON.stringify(priorOutput, null, 2)}` : ""}

${additionalContext ? `Additional context:\n${JSON.stringify(additionalContext, null, 2)}` : ""}

Instructions:
1. [Step 1 of intervention process]
2. [Step 2 of intervention process]
3. [Step 3 of intervention process]

Produce a structured output with:
- [Expected output component 1]
- [Expected output component 2]
- Recommended follow-up actions`;

    // Execute with structured output
    const response = await agent.generate(prompt, {
      output: z.object({
        // Define specific output schema here
        result: z.unknown(),
        followUpActions: z.array(z.string()),
      }),
      runtimeContext,
    });

    return {
      success: true,
      result: response.object.result,
      nextState: undefined, // Set based on intervention outcome
      followUpActions: response.object.followUpActions,
      metadata: {
        executedAt: new Date().toISOString(),
        durationMs: Date.now() - startTime,
      },
    };
  },
});

/*
// Example: Phase 0 Analysis Intervention

import { z } from "zod";
import { createTool } from "@mastra/core/tools";

const Phase0OutputSchema = z.object({
  concepts: z.object({
    primaryTerms: z.array(z.string()),
    variants: z.array(z.string()),
    ambiguous: z.array(z.string()),
  }),
  stakeholders: z.object({
    primary: z.array(z.string()),
    affected: z.array(z.string()),
    opposing: z.array(z.string()),
  }),
  temporal: z.object({
    origins: z.string(),
    transitions: z.array(z.string()),
    current: z.string(),
  }),
  domains: z.object({
    primary: z.string(),
    adjacent: z.array(z.string()),
  }),
  controversies: z.object({
    activeDebates: z.array(z.string()),
    competingFrameworks: z.array(z.string()),
  }),
});

export const runPhase0Analysis = createTool({
  id: "run-phase0-analysis",
  description:
    "Execute Phase 0 Topic Analysis. Use when R1 state is identified. " +
    "Produces structured topic analysis including concepts, stakeholders, " +
    "temporal scope, domains, and controversies.",
  inputSchema: z.object({
    topic: z.string(),
    decisionContext: z.string().optional(),
  }),
  outputSchema: z.object({
    success: z.boolean(),
    analysis: Phase0OutputSchema,
    followUpActions: z.array(z.string()),
  }),
  execute: async (inputData, context) => {
    const { topic, decisionContext } = inputData;
    const { mastra, runtimeContext } = context;

    const analyst = mastra?.getAgent("topic-analyst");

    const prompt = `Analyze the following research topic using Phase 0 Analysis Template:

Topic: ${topic}
${decisionContext ? `Decision context: ${decisionContext}` : ""}

Structure your analysis:

1. Core Concepts
   - Primary terms requiring definition
   - Terminology variants (synonyms, jargon, historical terms)
   - Ambiguous terms with multiple meanings

2. Stakeholders
   - Primary actors directly involved
   - Affected groups bearing consequences
   - Opposing interests benefiting from different outcomes

3. Temporal Scope
   - Historical origins
   - Key transitions and change points
   - Current state

4. Domains
   - Primary field of study
   - Adjacent/overlapping fields

5. Controversies
   - Active debates
   - Competing frameworks or approaches`;

    const response = await analyst?.generate(prompt, {
      output: Phase0OutputSchema,
      runtimeContext,
    });

    return {
      success: true,
      analysis: response?.object,
      followUpActions: [
        "Build vocabulary map from identified concepts",
        "Research each identified controversy",
        "Map terminology across identified domains",
      ],
    };
  },
});
*/
