# Vocabulary to Schema Conversion

Converting framework vocabulary terms into Zod schemas for structured agent output.

## Core Principle

Every term with semantic meaning in the framework becomes a typed schema. This enables:
- Validated agent outputs
- TypeScript type inference
- API contract definitions
- Cross-tool compatibility

## Basic Term to Schema

Framework vocabulary:
```
Vocabulary Map: Primary research deliverable mapping expert vs. outsider terms,
cross-domain synonyms, and depth indicators.
```

Becomes:
```typescript
import { z } from "zod";

export const VocabularyTermSchema = z.object({
  term: z.string().describe("The vocabulary term"),
  definition: z.string().describe("Precise definition"),
  domain: z.string().describe("Field this term belongs to"),
  depth: z.enum(["introductory", "working", "expert"]).describe("Expertise level"),
});

export const VocabularyMapSchema = z.object({
  topic: z.string().describe("Research topic"),
  coreTerms: z.array(VocabularyTermSchema).describe("Essential terms"),
  synonyms: z.array(z.object({
    concept: z.string(),
    termsByDomain: z.record(z.string()).describe("Domain -> term mapping"),
  })).describe("Cross-domain equivalent terms"),
  depthIndicators: z.object({
    introductory: z.array(z.string()).describe("Outsider/beginner terms"),
    working: z.array(z.string()).describe("Practitioner terms"),
    expert: z.array(z.string()).describe("Technical/academic terms"),
  }),
  lastUpdated: z.string().datetime().optional(),
});

// TypeScript type extraction
export type VocabularyTerm = z.infer<typeof VocabularyTermSchema>;
export type VocabularyMap = z.infer<typeof VocabularyMapSchema>;
```

## Enum Schemas for Constrained Values

Framework vocabulary with fixed values:
```
Depth Levels: introductory, working, expert
Confidence: high, medium, low, insufficient
```

Becomes:
```typescript
export const DepthLevelSchema = z.enum([
  "introductory",
  "working",
  "expert"
]).describe("Level of expertise required to use this term");

export const ConfidenceLevelSchema = z.enum([
  "high",
  "medium",
  "low",
  "insufficient"
]).describe("Confidence in research findings");

// With metadata
export const ConfidenceWithDetailsSchema = z.object({
  level: ConfidenceLevelSchema,
  justification: z.string(),
  sourceCount: z.number(),
  consensusStatus: z.enum(["strong", "moderate", "weak", "contested"]),
});
```

## Diagnostic State Schemas

Framework diagnostic states:
```
R1: No Analysis
R1.5: No Vocabulary Map
R2: Single-Perspective Search
...
```

Becomes:
```typescript
export const ResearchStateSchema = z.enum([
  "R1",
  "R1.5",
  "R2",
  "R3",
  "R4",
  "R5",
  "R6",
  "R7",
  "R8",
  "R9",
  "R10"
]).describe("Research diagnostic state identifier");

export const StateAssessmentSchema = z.object({
  state: ResearchStateSchema,
  name: z.string().describe("Human-readable state name"),
  applies: z.boolean(),
  confidence: z.number().min(0).max(1),
  symptomsMatched: z.array(z.string()),
  recommendedIntervention: z.string(),
});

// State details lookup (for instructions)
export const STATE_DETAILS: Record<string, { name: string; symptoms: string[]; intervention: string }> = {
  "R1": {
    name: "No Analysis",
    symptoms: ["Jumping straight to searching", "No stakeholder identification"],
    intervention: "Run Phase 0 Analysis Template",
  },
  // ...
};
```

## Process Phase Schemas

Framework process:
```
Phase 0: Topic Analysis
  Outputs: concepts, stakeholders, temporal, domains, controversies
```

Becomes:
```typescript
export const CoreConceptsSchema = z.object({
  primaryTerms: z.array(z.string()).describe("Key terms requiring definition"),
  variants: z.array(z.string()).describe("Synonyms, jargon, historical terms"),
  ambiguous: z.array(z.string()).describe("Terms with multiple meanings"),
});

export const StakeholdersSchema = z.object({
  primary: z.array(z.string()).describe("Directly involved actors"),
  affected: z.array(z.string()).describe("Groups bearing consequences"),
  opposing: z.array(z.string()).describe("Those with competing interests"),
});

export const TemporalScopeSchema = z.object({
  origins: z.string().describe("When this began"),
  transitions: z.array(z.string()).describe("Key change points"),
  current: z.string().describe("Present state"),
});

export const DomainsSchema = z.object({
  primary: z.string().describe("Main discipline"),
  adjacent: z.array(z.string()).describe("Related disciplines"),
});

export const ControversiesSchema = z.object({
  activeDebates: z.array(z.string()),
  competingFrameworks: z.array(z.string()),
});

// Combined Phase 0 output
export const Phase0AnalysisSchema = z.object({
  topic: z.string(),
  concepts: CoreConceptsSchema,
  stakeholders: StakeholdersSchema,
  temporal: TemporalScopeSchema,
  domains: DomainsSchema,
  controversies: ControversiesSchema,
  analyzedAt: z.string().datetime(),
});
```

## Integration Point Schemas

For skills that connect to others:
```typescript
// Reference to external skill
export const SkillReferenceSchema = z.object({
  skillId: z.string(),
  connectionType: z.enum(["storage", "verification", "transformation"]),
  state: z.string().optional(),
});

// Context network integration
export const ContextNetworkNodeSchema = z.object({
  path: z.string().describe("Path in context network"),
  nodeType: z.enum(["status", "decision", "glossary", "reference"]),
  content: z.unknown(),
});
```

## API Request/Response Schemas

For Hono endpoint definitions:
```typescript
// Assessment request
export const DiagnoseRequestSchema = z.object({
  situation: z.string().min(10).describe("Description of current situation"),
  topic: z.string().optional(),
  workDone: z.array(z.string()).optional(),
});

// Assessment response
export const DiagnoseResponseSchema = z.object({
  state: ResearchStateSchema,
  stateName: z.string(),
  confidence: z.number(),
  symptomsMatched: z.array(z.string()),
  intervention: z.string(),
  nextActions: z.array(z.string()),
  timestamp: z.string().datetime(),
});

// Workflow start request
export const StartResearchRequestSchema = z.object({
  topic: z.string().min(3),
  depth: z.enum(["quick", "working", "expert"]).default("working"),
  timeBox: z.string().optional(),
});

// Workflow status response
export const WorkflowStatusResponseSchema = z.object({
  runId: z.string(),
  status: z.enum(["pending", "running", "completed", "failed"]),
  currentStep: z.string().optional(),
  completedSteps: z.array(z.string()),
  output: z.unknown().optional(),
  error: z.string().optional(),
});
```

## Composing Schemas

Build complex schemas from simpler ones:
```typescript
// Base source reference
export const SourceReferenceSchema = z.object({
  title: z.string(),
  url: z.string().url().optional(),
  type: z.enum(["academic", "practitioner", "official", "encyclopedic"]),
  authority: z.number().min(0).max(1),
});

// Claim with source
export const SupportedClaimSchema = z.object({
  claim: z.string(),
  confidence: ConfidenceLevelSchema,
  sources: z.array(SourceReferenceSchema),
  counterEvidence: z.array(z.string()).optional(),
});

// Research synthesis (composed)
export const ResearchSynthesisSchema = z.object({
  topic: z.string(),
  summary: z.string(),
  confidence: ConfidenceWithDetailsSchema,
  keyFindings: z.array(SupportedClaimSchema),
  vocabularyMap: VocabularyMapSchema,
  gaps: z.array(z.string()),
  recommendations: z.array(z.string()),
  synthesizedAt: z.string().datetime(),
});
```

## Schema Organization

Organize schemas by purpose:
```
src/schemas/
├── index.ts           # Re-exports all schemas
├── states.ts          # Diagnostic state schemas
├── vocabulary.ts      # Vocabulary and term schemas
├── process.ts         # Process phase schemas
├── api.ts             # Request/response schemas
└── common.ts          # Shared/base schemas
```

Index file:
```typescript
// src/schemas/index.ts
export * from "./states.js";
export * from "./vocabulary.js";
export * from "./process.js";
export * from "./api.js";
export * from "./common.js";
```

## Best Practices

### 1. Use .describe() Liberally
Helps LLM understand what each field should contain:
```typescript
topic: z.string().describe("The research topic in plain language")
```

### 2. Add Constraints
Prevent invalid data:
```typescript
confidence: z.number().min(0).max(1)
email: z.string().email()
url: z.string().url().optional()
```

### 3. Export Types
Enable TypeScript inference:
```typescript
export type VocabularyMap = z.infer<typeof VocabularyMapSchema>;
```

### 4. Document Enums
Make enum values self-documenting:
```typescript
export const DepthLevel = {
  INTRODUCTORY: "introductory",  // Beginner/outsider terminology
  WORKING: "working",            // Practitioner terminology
  EXPERT: "expert",              // Technical/academic terminology
} as const;
```

### 5. Version Schemas
When schemas evolve:
```typescript
export const VocabularyMapV1Schema = z.object({ /* v1 */ });
export const VocabularyMapV2Schema = z.object({ /* v2 with new fields */ });
export const VocabularyMapSchema = VocabularyMapV2Schema;  // Current
```
