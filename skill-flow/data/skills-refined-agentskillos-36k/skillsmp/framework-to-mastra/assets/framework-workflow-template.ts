/**
 * Framework Workflow Template (Mastra v1 Beta)
 *
 * Template for converting framework process phases into Mastra workflows.
 *
 * CRITICAL: Schema matching between steps is the most error-prone area!
 * - Workflow inputSchema → Step 1 inputSchema: MUST match
 * - Step N outputSchema → Step N+1 inputSchema: MUST match
 * - Final step outputSchema → Workflow outputSchema: MUST match
 *
 * Customization points marked with {{PLACEHOLDER}}:
 * - {{WORKFLOW_NAME}}: kebab-case workflow identifier
 * - {{WORKFLOW_TITLE}}: Human-readable workflow name
 * - {{STEPS}}: Workflow step definitions
 */

import { createWorkflow, createStep } from "@mastra/core/workflows";
import { z } from "zod";

// ============================================================================
// Schema Definitions
// ============================================================================

// Workflow input schema
const WorkflowInputSchema = z.object({
  topic: z.string().describe("The subject for this workflow"),
  depth: z
    .enum(["quick", "working", "expert"])
    .default("working")
    .describe("Desired depth level"),
  context: z.record(z.unknown()).optional(),
});

// Phase 1 output schema (MUST match Phase 2 input)
const Phase1OutputSchema = z.object({
  topic: z.string(),
  phase1Result: z.unknown(), // Replace with specific schema
});

// Phase 2 output schema (MUST match Phase 3 input)
const Phase2OutputSchema = z.object({
  topic: z.string(),
  phase1Result: z.unknown(), // Passed through
  phase2Result: z.unknown(), // Replace with specific schema
});

// Final output schema (MUST match workflow outputSchema)
const FinalOutputSchema = z.object({
  topic: z.string(),
  summary: z.string(),
  results: z.unknown(),
  completedPhases: z.array(z.string()),
  processedAt: z.string().datetime(),
});

// ============================================================================
// Step Definitions
// ============================================================================

/**
 * Phase 1: [Phase Name]
 * Description of what this phase does.
 */
const phase1Step = createStep({
  id: "phase-1-name",
  // Input MUST match workflow inputSchema (for first step)
  inputSchema: WorkflowInputSchema,
  outputSchema: Phase1OutputSchema,
  execute: async ({ inputData, mastra, runtimeContext }) => {
    const { topic, depth, context } = inputData;

    // Get agent for this phase
    const agent = mastra?.getAgent("phase1-agent");

    // Execute phase logic
    const result = await agent?.generate(`Phase 1 for: ${topic}`, {
      runtimeContext,
    });

    // Return MUST match outputSchema
    return {
      topic,
      phase1Result: result?.text,
    };
  },
});

/**
 * Phase 2: [Phase Name]
 * Description of what this phase does.
 */
const phase2Step = createStep({
  id: "phase-2-name",
  // Input MUST match previous step's output
  inputSchema: Phase1OutputSchema,
  outputSchema: Phase2OutputSchema,
  execute: async ({ inputData, mastra, getInitData }) => {
    // inputData is phase1Step's output
    const { topic, phase1Result } = inputData;

    // Access original workflow input if needed
    const originalInput = getInitData();

    // Execute phase logic
    const agent = mastra?.getAgent("phase2-agent");
    const result = await agent?.generate(
      `Phase 2 based on: ${JSON.stringify(phase1Result)}`
    );

    // Pass through needed data for later steps
    return {
      topic,
      phase1Result, // Pass through
      phase2Result: result?.text,
    };
  },
});

/**
 * Synthesis: Combine results
 */
const synthesisStep = createStep({
  id: "synthesis",
  inputSchema: Phase2OutputSchema,
  outputSchema: FinalOutputSchema,
  execute: async ({ inputData, mastra, getStepResult }) => {
    const { topic, phase1Result, phase2Result } = inputData;

    // Can also access any step by ID
    const phase1 = getStepResult("phase-1-name");

    // Synthesize results
    const agent = mastra?.getAgent("synthesizer");
    const synthesis = await agent?.generate(
      `Synthesize: Phase 1: ${phase1Result}, Phase 2: ${phase2Result}`
    );

    return {
      topic,
      summary: synthesis?.text || "",
      results: { phase1Result, phase2Result },
      completedPhases: ["phase-1-name", "phase-2-name", "synthesis"],
      processedAt: new Date().toISOString(),
    };
  },
});

// ============================================================================
// Workflow Assembly
// ============================================================================

export const {{WORKFLOW_NAME}}Workflow = createWorkflow({
  id: "{{WORKFLOW_NAME}}",
  inputSchema: WorkflowInputSchema,
  outputSchema: FinalOutputSchema,
  // Optional: retry configuration
  retryConfig: {
    attempts: 3,
    delay: 1000,
  },
})
  .then(phase1Step)
  .then(phase2Step)
  .then(synthesisStep)
  .commit();

// ============================================================================
// Parallel Execution Example
// ============================================================================

/*
const parallelStep1 = createStep({
  id: "parallel-1",
  inputSchema: z.object({ topic: z.string() }),
  outputSchema: z.object({ result1: z.string() }),
  execute: async ({ inputData }) => ({ result1: "Result 1" }),
});

const parallelStep2 = createStep({
  id: "parallel-2",
  inputSchema: z.object({ topic: z.string() }),
  outputSchema: z.object({ result2: z.string() }),
  execute: async ({ inputData }) => ({ result2: "Result 2" }),
});

// After parallel, input is keyed by step ID
const combineStep = createStep({
  id: "combine",
  inputSchema: z.object({
    "parallel-1": z.object({ result1: z.string() }),
    "parallel-2": z.object({ result2: z.string() }),
  }),
  outputSchema: z.object({ combined: z.string() }),
  execute: async ({ inputData }) => ({
    combined: `${inputData["parallel-1"].result1} + ${inputData["parallel-2"].result2}`,
  }),
});

const parallelWorkflow = createWorkflow({...})
  .parallel([parallelStep1, parallelStep2])
  .then(combineStep)
  .commit();
*/

// ============================================================================
// Conditional Branching Example
// ============================================================================

/*
const quickStep = createStep({
  id: "quick-path",
  outputSchema: z.object({ result: z.string(), path: z.literal("quick") }),
  execute: async () => ({ result: "Quick result", path: "quick" }),
});

const deepStep = createStep({
  id: "deep-path",
  outputSchema: z.object({ result: z.string(), path: z.literal("deep") }),
  execute: async () => ({ result: "Deep result", path: "deep" }),
});

// After branch, use .optional()
const afterBranchStep = createStep({
  id: "after-branch",
  inputSchema: z.object({
    "quick-path": z.object({ result: z.string(), path: z.string() }).optional(),
    "deep-path": z.object({ result: z.string(), path: z.string() }).optional(),
  }),
  outputSchema: z.object({ finalResult: z.string() }),
  execute: async ({ inputData }) => {
    const result = inputData["quick-path"]?.result || inputData["deep-path"]?.result;
    return { finalResult: result || "No result" };
  },
});

const branchingWorkflow = createWorkflow({...})
  .then(assessStep)
  .branch([
    [async ({ inputData }) => inputData.depth === "quick", quickStep],
    [async ({ inputData }) => inputData.depth !== "quick", deepStep],
  ])
  .then(afterBranchStep)
  .commit();
*/

// ============================================================================
// Usage
// ============================================================================

/*
import { Mastra } from "@mastra/core/mastra";

const mastra = new Mastra({
  workflows: { {{WORKFLOW_NAME}}Workflow },
  agents: { phase1Agent, phase2Agent, synthesizerAgent },
});

// Start workflow run
const run = {{WORKFLOW_NAME}}Workflow.createRun();
const result = await run.start({
  inputData: {
    topic: "gentrification of workwear",
    depth: "working",
  },
});

console.log(result.status);  // "success" | "failed"
console.log(result.output);  // FinalOutput type
*/
