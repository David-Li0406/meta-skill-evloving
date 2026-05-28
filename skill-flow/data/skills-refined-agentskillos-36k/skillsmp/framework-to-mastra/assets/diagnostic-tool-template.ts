/**
 * Diagnostic Tool Template (Mastra v1 Beta)
 *
 * Template for converting framework diagnostic states into assessment tools.
 *
 * Customization points marked with {{PLACEHOLDER}}:
 * - {{FRAMEWORK_NAME}}: kebab-case framework identifier
 * - {{STATE_ENUM}}: Zod enum of state IDs
 * - {{STATE_DETAILS}}: Lookup object with state details
 * - {{ASSESSMENT_LOGIC}}: Custom assessment logic
 */

import { createTool } from "@mastra/core/tools";
import { z } from "zod";

// State ID enum - replace with actual states
const StateIdSchema = z.enum([
  // {{STATE_ENUM}}
  "STATE_1",
  "STATE_2",
  "STATE_3",
  // ... add all states
]);

// State details lookup
const STATE_DETAILS: Record<
  z.infer<typeof StateIdSchema>,
  {
    name: string;
    symptoms: string[];
    test: string;
    intervention: string;
  }
> = {
  // {{STATE_DETAILS}}
  STATE_1: {
    name: "Example State",
    symptoms: ["Symptom 1", "Symptom 2"],
    test: "Can you...?",
    intervention: "Apply intervention X",
  },
  // ... add all states
};

// Assessment output schema
const AssessmentOutputSchema = z.object({
  primaryState: StateIdSchema,
  primaryStateName: z.string(),
  confidence: z.number().min(0).max(1),
  allStatesAssessed: z.array(
    z.object({
      stateId: StateIdSchema,
      stateName: z.string(),
      score: z.number().min(0).max(1),
      symptomsMatched: z.array(z.string()),
    })
  ),
  recommendedIntervention: z.string(),
  nextActions: z.array(z.string()),
  isComplete: z.boolean(),
});

/**
 * Assess current state against all diagnostic states.
 * Returns the primary (highest-scoring) state with intervention recommendation.
 */
export const assess{{FRAMEWORK_NAME}}State = createTool({
  id: "assess-{{FRAMEWORK_NAME}}-state",
  description:
    "Assess current situation against {{FRAMEWORK_NAME}} diagnostic states. " +
    "Returns primary state, confidence score, matched symptoms, and recommended intervention. " +
    "Use when evaluating where the user is in the {{FRAMEWORK_NAME}} process.",
  inputSchema: z.object({
    situation: z
      .string()
      .min(10)
      .describe("Description of the current situation"),
    workDone: z
      .array(z.string())
      .optional()
      .describe("Actions already taken"),
    priorState: StateIdSchema.optional().describe(
      "Previously assessed state, if known"
    ),
  }),
  outputSchema: AssessmentOutputSchema,
  execute: async (inputData, context) => {
    const { situation, workDone = [], priorState } = inputData;
    const { mastra, runtimeContext } = context;

    // Get diagnostician agent for nuanced assessment
    const diagnostician = mastra?.getAgent("{{FRAMEWORK_NAME}}-diagnostician");

    if (!diagnostician) {
      // Fallback: simple keyword-based assessment
      return simpleAssessment(situation, workDone);
    }

    // Build assessment prompt with framework knowledge
    const stateDescriptions = Object.entries(STATE_DETAILS)
      .map(
        ([id, details]) =>
          `${id}: ${details.name}\n  Symptoms: ${details.symptoms.join(", ")}\n  Test: ${details.test}`
      )
      .join("\n\n");

    const prompt = `Assess this situation against the diagnostic states:

Situation: ${situation}
Work done: ${workDone.join(", ") || "None specified"}
${priorState ? `Prior state: ${priorState}` : ""}

Diagnostic States:
${stateDescriptions}

For each state, score 0-1 how well symptoms match.
Identify specific symptoms that match.
Return the highest-scoring non-complete state as primary.
Provide specific next actions.`;

    const result = await diagnostician.generate(prompt, {
      output: AssessmentOutputSchema,
      runtimeContext,
    });

    return result.object;
  },
});

/**
 * Simple fallback assessment without LLM.
 * Uses keyword matching for basic state detection.
 */
function simpleAssessment(
  situation: string,
  workDone: string[]
): z.infer<typeof AssessmentOutputSchema> {
  const situationLower = situation.toLowerCase();
  const scores: Array<{
    stateId: z.infer<typeof StateIdSchema>;
    stateName: string;
    score: number;
    symptomsMatched: string[];
  }> = [];

  for (const [stateId, details] of Object.entries(STATE_DETAILS)) {
    const matched: string[] = [];
    let score = 0;

    for (const symptom of details.symptoms) {
      // Simple keyword check
      const keywords = symptom.toLowerCase().split(" ");
      const matchCount = keywords.filter((k) =>
        situationLower.includes(k)
      ).length;
      if (matchCount > keywords.length * 0.3) {
        matched.push(symptom);
        score += 1 / details.symptoms.length;
      }
    }

    scores.push({
      stateId: stateId as z.infer<typeof StateIdSchema>,
      stateName: details.name,
      score,
      symptomsMatched: matched,
    });
  }

  // Sort by score descending
  scores.sort((a, b) => b.score - a.score);

  const primary = scores[0];
  const stateDetails = STATE_DETAILS[primary.stateId];

  return {
    primaryState: primary.stateId,
    primaryStateName: primary.stateName,
    confidence: primary.score,
    allStatesAssessed: scores,
    recommendedIntervention: stateDetails.intervention,
    nextActions: [`Apply: ${stateDetails.intervention}`],
    isComplete: false, // Adjust based on "complete" state ID
  };
}

/*
// Usage:

const result = await assess{{FRAMEWORK_NAME}}State.execute(
  {
    situation: "I'm researching X but keep finding surface-level content",
    workDone: ["Searched Google", "Read Wikipedia"],
  },
  { mastra }
);

console.log(`State: ${result.primaryState} - ${result.primaryStateName}`);
console.log(`Confidence: ${result.confidence}`);
console.log(`Intervention: ${result.recommendedIntervention}`);
*/
