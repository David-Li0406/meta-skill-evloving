/**
 * Zod Schema Examples
 *
 * Common schema patterns for framework-to-agent conversion.
 * Use as reference when creating schemas from framework vocabulary.
 */

import { z } from "zod";

// ============================================================================
// Diagnostic State Schemas
// ============================================================================

/**
 * State ID enum pattern
 * Replace values with actual state IDs from framework
 */
export const StateIdSchema = z.enum([
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
  "R10",
]);

/**
 * State assessment result
 */
export const StateAssessmentSchema = z.object({
  stateId: StateIdSchema,
  stateName: z.string(),
  applies: z.boolean(),
  confidence: z.number().min(0).max(1),
  symptomsMatched: z.array(z.string()),
  symptomsMissed: z.array(z.string()),
  recommendedIntervention: z.string(),
  nextActions: z.array(z.string()),
});

/**
 * Multi-state assessment (for combined assessment tools)
 */
export const CombinedAssessmentSchema = z.object({
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

// ============================================================================
// Vocabulary Schemas
// ============================================================================

/**
 * Depth/expertise level
 */
export const DepthLevelSchema = z.enum(["introductory", "working", "expert"]);

/**
 * Single vocabulary term
 */
export const VocabularyTermSchema = z.object({
  term: z.string().describe("The vocabulary term"),
  definition: z.string().describe("Precise definition"),
  domain: z.string().describe("Field this term belongs to"),
  depth: DepthLevelSchema.describe("Expertise level required"),
  relatedTerms: z.array(z.string()).optional(),
});

/**
 * Cross-domain synonym mapping
 */
export const SynonymMappingSchema = z.object({
  concept: z.string().describe("The underlying concept"),
  termsByDomain: z
    .record(z.string())
    .describe("Domain -> term mapping, e.g., { 'psychology': 'confirmation bias', 'economics': 'motivated reasoning' }"),
});

/**
 * Full vocabulary map
 */
export const VocabularyMapSchema = z.object({
  topic: z.string(),
  coreTerms: z.array(VocabularyTermSchema),
  synonyms: z.array(SynonymMappingSchema),
  depthIndicators: z.object({
    introductory: z.array(z.string()),
    working: z.array(z.string()),
    expert: z.array(z.string()),
  }),
  lastUpdated: z.string().datetime().optional(),
});

// ============================================================================
// Process Phase Schemas
// ============================================================================

/**
 * Phase 0 analysis components (research framework example)
 */
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

/**
 * Combined Phase 0 output
 */
export const Phase0AnalysisSchema = z.object({
  topic: z.string(),
  concepts: CoreConceptsSchema,
  stakeholders: StakeholdersSchema,
  temporal: TemporalScopeSchema,
  domains: DomainsSchema,
  controversies: ControversiesSchema,
  analyzedAt: z.string().datetime(),
});

// ============================================================================
// Confidence and Source Schemas
// ============================================================================

/**
 * Confidence level
 */
export const ConfidenceLevelSchema = z.enum([
  "high",
  "medium",
  "low",
  "insufficient",
]);

/**
 * Confidence with justification
 */
export const ConfidenceWithDetailsSchema = z.object({
  level: ConfidenceLevelSchema,
  justification: z.string(),
  sourceCount: z.number(),
  consensusStatus: z.enum(["strong", "moderate", "weak", "contested"]),
});

/**
 * Source reference
 */
export const SourceReferenceSchema = z.object({
  title: z.string(),
  url: z.string().url().optional(),
  type: z.enum(["academic", "practitioner", "official", "encyclopedic", "primary"]),
  authority: z.number().min(0).max(1),
  accessedAt: z.string().datetime().optional(),
});

/**
 * Supported claim (claim with evidence)
 */
export const SupportedClaimSchema = z.object({
  claim: z.string(),
  confidence: ConfidenceLevelSchema,
  sources: z.array(SourceReferenceSchema),
  counterEvidence: z.array(z.string()).optional(),
});

// ============================================================================
// Synthesis Schemas
// ============================================================================

/**
 * Research synthesis output
 */
export const ResearchSynthesisSchema = z.object({
  topic: z.string(),
  summary: z.string().describe("Direct answer to the research question"),
  confidence: ConfidenceWithDetailsSchema,
  keyFindings: z.array(SupportedClaimSchema),
  vocabularyMap: VocabularyMapSchema.optional(),
  gaps: z.array(z.string()).describe("What remains unknown"),
  recommendations: z.array(z.string()),
  caveats: z.array(z.string()).describe("Limitations and assumptions"),
  synthesizedAt: z.string().datetime(),
});

// ============================================================================
// API Request/Response Schemas
// ============================================================================

/**
 * Diagnose request
 */
export const DiagnoseRequestSchema = z.object({
  situation: z.string().min(10).describe("Description of current situation"),
  topic: z.string().optional(),
  workDone: z.array(z.string()).optional().describe("Actions already taken"),
});

/**
 * Diagnose response
 */
export const DiagnoseResponseSchema = z.object({
  state: StateIdSchema,
  stateName: z.string(),
  confidence: z.number(),
  symptomsMatched: z.array(z.string()),
  intervention: z.string(),
  nextActions: z.array(z.string()),
  timestamp: z.string().datetime(),
});

/**
 * Workflow start request
 */
export const StartWorkflowRequestSchema = z.object({
  topic: z.string().min(3),
  depth: z.enum(["quick", "working", "expert"]).default("working"),
  timeBox: z.string().optional(),
  context: z.record(z.unknown()).optional(),
});

/**
 * Workflow status response
 */
export const WorkflowStatusResponseSchema = z.object({
  runId: z.string(),
  status: z.enum(["pending", "running", "completed", "failed"]),
  currentStep: z.string().optional(),
  completedSteps: z.array(z.string()),
  output: z.unknown().optional(),
  error: z.string().optional(),
  startedAt: z.string().datetime(),
  completedAt: z.string().datetime().optional(),
});

// ============================================================================
// Type Extraction
// ============================================================================

// Extract TypeScript types from schemas
export type StateId = z.infer<typeof StateIdSchema>;
export type StateAssessment = z.infer<typeof StateAssessmentSchema>;
export type CombinedAssessment = z.infer<typeof CombinedAssessmentSchema>;
export type DepthLevel = z.infer<typeof DepthLevelSchema>;
export type VocabularyTerm = z.infer<typeof VocabularyTermSchema>;
export type VocabularyMap = z.infer<typeof VocabularyMapSchema>;
export type Phase0Analysis = z.infer<typeof Phase0AnalysisSchema>;
export type ConfidenceLevel = z.infer<typeof ConfidenceLevelSchema>;
export type ConfidenceWithDetails = z.infer<typeof ConfidenceWithDetailsSchema>;
export type SourceReference = z.infer<typeof SourceReferenceSchema>;
export type SupportedClaim = z.infer<typeof SupportedClaimSchema>;
export type ResearchSynthesis = z.infer<typeof ResearchSynthesisSchema>;
export type DiagnoseRequest = z.infer<typeof DiagnoseRequestSchema>;
export type DiagnoseResponse = z.infer<typeof DiagnoseResponseSchema>;
export type StartWorkflowRequest = z.infer<typeof StartWorkflowRequestSchema>;
export type WorkflowStatusResponse = z.infer<typeof WorkflowStatusResponseSchema>;
