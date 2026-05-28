# Diagnostic State to Tool Conversion

Converting framework diagnostic states into Mastra tools with structured output.

## Core Pattern

Each diagnostic state (or group of related states) becomes a tool that:
1. Accepts situation description as input
2. Assesses which state applies
3. Returns structured output with state, evidence, and recommendations

## Single State Assessment Tool

When states are distinct and each needs individual assessment:

```typescript
import { createTool } from "@mastra/core/tools";
import { z } from "zod";

// Schema for state assessment output
const StateAssessmentSchema = z.object({
  stateId: z.string(),
  stateName: z.string(),
  applies: z.boolean(),
  confidence: z.number().min(0).max(1),
  symptomsMatched: z.array(z.string()),
  symptomsMissed: z.array(z.string()),
  recommendedIntervention: z.string(),
  nextActions: z.array(z.string()),
});

// Tool for assessing a specific state
export const assessNoAnalysisState = createTool({
  id: "assess-no-analysis-r1",
  description: "Assess whether the research situation shows R1: No Analysis state. " +
    "Use when evaluating if topic analysis was skipped before searching.",
  inputSchema: z.object({
    situation: z.string().describe("Description of the current research situation"),
    priorActions: z.array(z.string()).optional().describe("What has been done so far"),
  }),
  outputSchema: StateAssessmentSchema,
  execute: async (inputData, context) => {
    const { situation, priorActions = [] } = inputData;
    const { mastra } = context;

    // State-specific assessment logic
    const symptoms = [
      "Jumping straight to searching without analyzing the topic",
      "No stakeholder identification",
      "No temporal scope defined",
      "No domain mapping done",
    ];

    // Check symptoms against situation
    const matched: string[] = [];
    const missed: string[] = [];

    // Simple keyword-based matching (in real implementation, use LLM)
    for (const symptom of symptoms) {
      if (situation.toLowerCase().includes("search") &&
          !situation.toLowerCase().includes("analyz")) {
        matched.push(symptoms[0]);
      }
      // ... more checks
    }

    const applies = matched.length >= 2;
    const confidence = matched.length / symptoms.length;

    return {
      stateId: "R1",
      stateName: "No Analysis",
      applies,
      confidence,
      symptomsMatched: matched,
      symptomsMissed: symptoms.filter(s => !matched.includes(s)),
      recommendedIntervention: applies
        ? "Run Phase 0 Analysis Template before generating queries"
        : "State does not apply",
      nextActions: applies
        ? ["Complete Phase 0 analysis template", "Map stakeholders", "Define temporal scope"]
        : [],
    };
  },
});
```

## Combined Assessment Tool

For most frameworks, a single tool that assesses all states is more practical:

```typescript
// Schema for all states
const DiagnosticStateEnum = z.enum([
  "R1", "R1.5", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"
]);

const CombinedAssessmentSchema = z.object({
  primaryState: DiagnosticStateEnum,
  primaryStateName: z.string(),
  confidence: z.number().min(0).max(1),
  allStatesAssessed: z.array(z.object({
    stateId: DiagnosticStateEnum,
    stateName: z.string(),
    score: z.number(),
    symptomsMatched: z.array(z.string()),
  })),
  recommendedIntervention: z.string(),
  nextActions: z.array(z.string()),
  isComplete: z.boolean(),
});

export const assessResearchState = createTool({
  id: "assess-research-state",
  description: "Assess current research state across all diagnostic states (R1-R10). " +
    "Returns primary state with highest match score and recommended intervention.",
  inputSchema: z.object({
    situation: z.string().describe("Description of current research situation"),
    topic: z.string().optional().describe("Research topic if known"),
    workDone: z.array(z.string()).optional().describe("Research activities completed"),
    vocabularyMap: z.boolean().optional().describe("Whether vocabulary map exists"),
  }),
  outputSchema: CombinedAssessmentSchema,
  execute: async (inputData, context) => {
    const { situation, topic, workDone = [], vocabularyMap = false } = inputData;
    const { mastra } = context;

    // Use LLM agent for nuanced assessment
    const assessor = mastra?.getAgent("research-diagnostician");
    if (!assessor) throw new Error("Diagnostician agent not found");

    const prompt = `Assess the following research situation against diagnostic states:

Situation: ${situation}
Topic: ${topic || "Not specified"}
Work done: ${workDone.join(", ") || "None specified"}
Has vocabulary map: ${vocabularyMap}

Rate each state R1-R10 on how well it matches (0-1 score).
Identify which symptoms match.
Recommend the intervention for the highest-scoring state.`;

    const result = await assessor.generate(prompt, {
      output: CombinedAssessmentSchema,
    });

    return result.object;
  },
});
```

## Agent-Powered Assessment

For complex diagnostic logic, use an agent as the assessor:

```typescript
// Diagnostician agent with framework knowledge in instructions
export const diagnosticianAgent = new Agent({
  name: "research-diagnostician",
  model: openai("gpt-4o-mini"),
  instructions: `You are a research methodology diagnostician.

You assess research situations against these diagnostic states:

R1: No Analysis - Jumping to searching without topic analysis
R1.5: No Vocabulary Map - Using outsider terminology, finding surface-level material
R2: Single-Perspective - All queries support one viewpoint
R3: Domain Blindness - Searching only in familiar field
R4: Recency Bias - Only recent sources, missing historical context
R5: Breadth Without Depth - Many tabs, no synthesis
R6: Completion Uncertainty - Unsure whether to continue or stop
R7: Research Complete - Can explain topic, identify uncertainties, take action
R8: No Persistence - Starting from scratch each session
R9: Scope Mismatch - Over/under-researching relative to stakes
R10: No Confidence Signaling - Hedging everywhere, reader can't tell what's certain

For each assessment:
1. Score each state 0-1 on how well symptoms match
2. Identify specific symptoms that match
3. Return the highest-scoring non-complete state as primary
4. Provide specific intervention recommendation
5. List concrete next actions

If R7 (Complete) scores highest, acknowledge completion.`,
});

// Tool that uses the agent
export const diagnoseState = createTool({
  id: "diagnose-research-state",
  description: "Use diagnostician agent to assess research state",
  inputSchema: z.object({
    situation: z.string(),
  }),
  outputSchema: CombinedAssessmentSchema,
  execute: async (inputData, context) => {
    const { situation } = inputData;
    const { mastra, runtimeContext } = context;

    const agent = mastra?.getAgent("research-diagnostician");
    const result = await agent?.generate(situation, {
      output: CombinedAssessmentSchema,
      runtimeContext,
    });

    return result?.object;
  },
});
```

## Intervention Tools

Each intervention recommendation can link to a specific tool:

```typescript
export const runPhase0Analysis = createTool({
  id: "run-phase0-analysis",
  description: "Execute Phase 0 topic analysis. Use when R1 state is identified.",
  inputSchema: z.object({
    topic: z.string().describe("Research topic to analyze"),
  }),
  outputSchema: Phase0AnalysisSchema,
  execute: async (inputData, context) => {
    const { topic } = inputData;
    const { mastra } = context;

    const analyst = mastra?.getAgent("topic-analyst");
    const result = await analyst?.generate(
      `Analyze topic for research: ${topic}

Apply Phase 0 Analysis Template:
1. Core Concepts - primary terms, variants, ambiguous terms
2. Stakeholders - primary actors, affected groups, opposing interests
3. Temporal Scope - origins, transitions, current state
4. Domains - primary field, adjacent fields
5. Controversies - active debates, competing frameworks`,
      { output: Phase0AnalysisSchema }
    );

    return result?.object;
  },
});

export const buildVocabularyMap = createTool({
  id: "build-vocabulary-map",
  description: "Build vocabulary map. Use when R1.5 state is identified.",
  inputSchema: z.object({
    topic: z.string(),
    initialTerms: z.array(z.string()).optional(),
    sources: z.array(z.string()).optional(),
  }),
  outputSchema: VocabularyMapSchema,
  execute: async (inputData, context) => {
    // Build vocabulary map from topic and initial terms
  },
});
```

## Chaining Assessment to Intervention

Common pattern: assess state, then run appropriate intervention:

```typescript
export const diagnoseAndIntervene = createTool({
  id: "diagnose-and-intervene",
  description: "Assess state and automatically run recommended intervention",
  inputSchema: z.object({
    situation: z.string(),
    topic: z.string(),
    autoIntervene: z.boolean().default(true),
  }),
  outputSchema: z.object({
    assessment: CombinedAssessmentSchema,
    interventionResult: z.any().optional(),
    interventionRan: z.boolean(),
  }),
  execute: async (inputData, context) => {
    const { situation, topic, autoIntervene } = inputData;
    const { mastra } = context;

    // Assess state
    const assessment = await diagnoseState.execute({ situation }, context);

    if (!autoIntervene || assessment.isComplete) {
      return { assessment, interventionRan: false };
    }

    // Run appropriate intervention
    let interventionResult;
    switch (assessment.primaryState) {
      case "R1":
        interventionResult = await runPhase0Analysis.execute({ topic }, context);
        break;
      case "R1.5":
        interventionResult = await buildVocabularyMap.execute({ topic }, context);
        break;
      // ... other states
    }

    return {
      assessment,
      interventionResult,
      interventionRan: true,
    };
  },
});
```

## Best Practices

### 1. Include Evidence
Always return which symptoms matched, not just the state ID:

```typescript
symptomsMatched: ["Found only surface-level content", "Using outsider terms"]
```

### 2. Confidence Scores
Provide confidence to help users evaluate:

```typescript
confidence: 0.85  // High confidence
confidence: 0.4   // Multiple states could apply
```

### 3. Actionable Next Steps
Don't just name the state - provide concrete actions:

```typescript
nextActions: [
  "Search for 'technically called' and 'also known as' in current sources",
  "Map terms by domain using vocabulary template",
  "Test searches with expert terms vs. current terms"
]
```

### 4. Handle Ambiguity
When multiple states apply, return all with scores:

```typescript
allStatesAssessed: [
  { stateId: "R1.5", score: 0.8, ... },
  { stateId: "R3", score: 0.6, ... },
  { stateId: "R4", score: 0.3, ... },
]
```
