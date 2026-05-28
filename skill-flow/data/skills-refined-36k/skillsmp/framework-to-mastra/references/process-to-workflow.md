# Process to Workflow Conversion

Converting framework process phases into Mastra workflows with proper data flow.

## Core Principle

Framework phases become workflow steps. Each phase's outputs become the next phase's inputs. Schema matching is critical.

## Mapping Framework Phases

Given a framework with phases:

```
Phase 0: Topic Analysis
  Input: topic
  Output: concepts, stakeholders, temporal, domains, controversies

Phase 1.5: Vocabulary Mapping
  Input: concepts (from Phase 0)
  Output: vocabulary_map

Phase 2: Query Construction
  Input: vocabulary_map, domains
  Output: queries

Synthesis:
  Input: all prior outputs
  Output: research_synthesis
```

Becomes workflow:

```typescript
import { createWorkflow, createStep } from "@mastra/core/workflows";
import { z } from "zod";

// Step 1: Topic Analysis (Phase 0)
const phase0Step = createStep({
  id: "phase-0-analysis",
  inputSchema: z.object({
    topic: z.string(),
    decisionContext: z.string().optional(),
  }),
  outputSchema: z.object({
    concepts: ConceptsSchema,
    stakeholders: StakeholdersSchema,
    temporal: TemporalSchema,
    domains: DomainsSchema,
    controversies: ControversiesSchema,
  }),
  execute: async ({ inputData, mastra }) => {
    const { topic, decisionContext } = inputData;

    const analyst = mastra?.getAgent("topic-analyst");
    const result = await analyst?.generate(
      `Analyze research topic: ${topic}\nContext: ${decisionContext || "general research"}`,
      { output: Phase0OutputSchema }
    );

    return result?.object;
  },
});

// Step 2: Vocabulary Mapping (Phase 1.5)
const phase15Step = createStep({
  id: "phase-1-5-vocabulary",
  // Input schema MUST match phase0Step output
  inputSchema: z.object({
    concepts: ConceptsSchema,
    stakeholders: StakeholdersSchema,
    temporal: TemporalSchema,
    domains: DomainsSchema,
    controversies: ControversiesSchema,
  }),
  outputSchema: z.object({
    vocabularyMap: VocabularyMapSchema,
    domains: DomainsSchema,  // Pass through for next step
  }),
  execute: async ({ inputData, mastra }) => {
    const { concepts, domains } = inputData;

    const mapper = mastra?.getAgent("vocabulary-mapper");
    const result = await mapper?.generate(
      `Build vocabulary map from concepts: ${JSON.stringify(concepts)}`,
      { output: VocabularyMapSchema }
    );

    return {
      vocabularyMap: result?.object,
      domains: inputData.domains,  // Pass through
    };
  },
});

// Step 3: Query Construction (Phase 2)
const phase2Step = createStep({
  id: "phase-2-queries",
  inputSchema: z.object({
    vocabularyMap: VocabularyMapSchema,
    domains: DomainsSchema,
  }),
  outputSchema: z.object({
    queries: z.array(QuerySchema),
    vocabularyMap: VocabularyMapSchema,  // Pass through
  }),
  execute: async ({ inputData, mastra }) => {
    const { vocabularyMap, domains } = inputData;

    const queryBuilder = mastra?.getAgent("query-builder");
    const result = await queryBuilder?.generate(
      `Generate research queries using vocabulary: ${JSON.stringify(vocabularyMap)}\n` +
      `Target domains: ${JSON.stringify(domains)}`,
      { output: z.object({ queries: z.array(QuerySchema) }) }
    );

    return {
      queries: result?.object.queries,
      vocabularyMap,
    };
  },
});

// Step 4: Synthesis
const synthesisStep = createStep({
  id: "synthesis",
  inputSchema: z.object({
    queries: z.array(QuerySchema),
    vocabularyMap: VocabularyMapSchema,
  }),
  outputSchema: ResearchSynthesisSchema,
  execute: async ({ inputData, getInitData, mastra }) => {
    const { queries, vocabularyMap } = inputData;
    const { topic } = getInitData();  // Access original workflow input

    const synthesizer = mastra?.getAgent("research-synthesizer");
    const result = await synthesizer?.generate(
      `Synthesize research plan for: ${topic}\n` +
      `Queries: ${JSON.stringify(queries)}\n` +
      `Vocabulary: ${JSON.stringify(vocabularyMap)}`,
      { output: ResearchSynthesisSchema }
    );

    return result?.object;
  },
});

// Assemble workflow
export const researchWorkflow = createWorkflow({
  id: "research-workflow",
  inputSchema: z.object({
    topic: z.string(),
    decisionContext: z.string().optional(),
  }),
  outputSchema: ResearchSynthesisSchema,
})
  .then(phase0Step)
  .then(phase15Step)
  .then(phase2Step)
  .then(synthesisStep)
  .commit();
```

## Handling Pass-Through Data

When later steps need data from earlier steps:

### Option 1: Pass Through in Schema

Include earlier data in each step's output:

```typescript
// Step 1 output includes data step 3 will need
outputSchema: z.object({
  vocabularyMap: VocabularyMapSchema,
  domains: DomainsSchema,  // Pass through for step 3
})
```

### Option 2: Use getStepResult

Access any prior step's output directly:

```typescript
execute: async ({ inputData, getStepResult }) => {
  // Get Phase 0 output directly
  const phase0 = getStepResult("phase-0-analysis");
  const domains = phase0.domains;

  // inputData is still the previous step's output
  const { vocabularyMap } = inputData;
}
```

### Option 3: Use getInitData

Access original workflow input:

```typescript
execute: async ({ inputData, getInitData }) => {
  const originalInput = getInitData();  // { topic, decisionContext }
}
```

### Option 4: Use State

For cross-cutting concerns:

```typescript
execute: async ({ inputData, state, setState }) => {
  // Store accumulated data in state
  setState({
    ...state,
    vocabularyTerms: [...state.vocabularyTerms, ...newTerms],
  });
}
```

## Parallel Phases

When phases can run independently:

```typescript
const collectSourcesStep = createStep({
  id: "collect-sources",
  inputSchema: QueryInputSchema,
  outputSchema: z.object({ sources: z.array(SourceSchema) }),
  execute: async ({ inputData }) => { /* ... */ },
});

const analyzeGapsStep = createStep({
  id: "analyze-gaps",
  inputSchema: QueryInputSchema,
  outputSchema: z.object({ gaps: z.array(z.string()) }),
  execute: async ({ inputData }) => { /* ... */ },
});

// Step after parallel receives keyed object
const synthesizeStep = createStep({
  id: "synthesize",
  inputSchema: z.object({
    "collect-sources": z.object({ sources: z.array(SourceSchema) }),
    "analyze-gaps": z.object({ gaps: z.array(z.string()) }),
  }),
  outputSchema: SynthesisSchema,
  execute: async ({ inputData }) => {
    const sources = inputData["collect-sources"].sources;
    const gaps = inputData["analyze-gaps"].gaps;
    // Combine and synthesize
  },
});

const workflow = createWorkflow({ ... })
  .then(prepStep)
  .parallel([collectSourcesStep, analyzeGapsStep])
  .then(synthesizeStep)
  .commit();
```

## Conditional Phases

When process branches based on conditions:

```typescript
const quickResearchStep = createStep({
  id: "quick-research",
  outputSchema: z.object({ result: z.string(), depth: z.literal("quick") }),
  execute: async () => ({ result: "Quick scan", depth: "quick" }),
});

const deepResearchStep = createStep({
  id: "deep-research",
  outputSchema: z.object({ result: z.string(), depth: z.literal("deep") }),
  execute: async () => ({ result: "Deep analysis", depth: "deep" }),
});

// Step after branch uses .optional()
const formatResultStep = createStep({
  id: "format-result",
  inputSchema: z.object({
    "quick-research": z.object({ result: z.string(), depth: z.string() }).optional(),
    "deep-research": z.object({ result: z.string(), depth: z.string() }).optional(),
  }),
  outputSchema: ResearchOutputSchema,
  execute: async ({ inputData }) => {
    const result = inputData["quick-research"] || inputData["deep-research"];
    return { output: result?.result, depth: result?.depth };
  },
});

const workflow = createWorkflow({ ... })
  .then(assessScopeStep)
  .branch([
    [async ({ inputData }) => inputData.timeBox === "quick", quickResearchStep],
    [async ({ inputData }) => inputData.timeBox !== "quick", deepResearchStep],
  ])
  .then(formatResultStep)
  .commit();
```

## Schema Transformation with .map()

When phase outputs don't directly match next phase's expected input:

```typescript
const workflow = createWorkflow({ ... })
  .then(phase0Step)  // outputs { concepts, stakeholders, ... }
  .map(async ({ inputData }) => {
    // Transform Phase 0 output to Phase 1.5 expected input
    return {
      coreTerms: inputData.concepts.primaryTerms,
      domainHints: inputData.domains.primary,
    };
  })
  .then(phase15Step)  // expects { coreTerms, domainHints }
  .commit();
```

## Single-Shot vs Full Workflow

Many frameworks have two modes. Create separate workflows:

```typescript
// Full research workflow (interactive, multi-step)
export const fullResearchWorkflow = createWorkflow({
  id: "full-research",
  inputSchema: z.object({
    topic: z.string(),
    depth: z.enum(["working", "expert"]),
  }),
  outputSchema: FullResearchOutputSchema,
})
  .then(phase0Step)
  .then(phase15Step)
  .then(phase2Step)
  .then(executionStep)
  .then(synthesisStep)
  .commit();

// Single-shot workflow (time-boxed, automated)
export const singleShotResearchWorkflow = createWorkflow({
  id: "single-shot-research",
  inputSchema: z.object({
    topic: z.string(),
    timeBox: z.enum(["minutes", "hours", "halfday"]),
    confidence: z.enum(["quick", "moderate", "high"]),
  }),
  outputSchema: SingleShotOutputSchema,
})
  .then(calibrateScopeStep)
  .then(quickAnalysisStep)
  .then(targetedSearchStep)
  .then(synthesizeWithConfidenceStep)
  .commit();
```

## Error Handling in Workflows

```typescript
const robustStep = createStep({
  id: "robust-step",
  execute: async ({ inputData, mastra }) => {
    try {
      const result = await doWork(inputData);
      return { success: true, data: result };
    } catch (error) {
      // Log error, return graceful degradation
      console.error("Step failed:", error);
      return {
        success: false,
        data: null,
        error: error.message,
      };
    }
  },
});

// Use retryConfig for transient failures
export const workflow = createWorkflow({
  id: "resilient-workflow",
  retryConfig: {
    attempts: 3,
    delay: 1000,
  },
  // ...
});
```

## Best Practices

1. **Schema Matching**: Always verify output schema matches next step's input
2. **Pass-Through**: Include data needed by later steps in intermediate outputs
3. **Clear IDs**: Use descriptive step IDs matching framework phase names
4. **Agent Per Phase**: Each phase can use a specialized agent
5. **Preserve Context**: Use getInitData() to access original request
6. **Handle Branches**: Use .optional() after branch steps
7. **Separate Workflows**: Create distinct workflows for different modes (full vs single-shot)
