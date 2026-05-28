---
name: framework-to-mastra
description: Convert operating-frameworks skills into deployed Mastra+Hono agents with APIs, workflows, and persistent memory. Use when deploying a framework as an API, creating agent versions of diagnostic skills, or building multi-agent systems from framework clusters.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
  domain: deployment
  cluster: agent-development
  type: generator
  mode: generative
---

# Framework-to-Mastra: Agent Conversion Skill

You convert operating-frameworks diagnostic skills and frameworks into production-deployed Mastra agents with Hono APIs.

## Core Principle

**Frameworks encode expertise; agents operationalize it.** A framework's diagnostic states become agent tools. Its processes become workflows. Its vocabulary becomes structured schemas. Its context network integration becomes agent memory.

## When to Use This Skill

**Use when:**
- Deploying a framework as an accessible API
- Creating an agent that embodies a diagnostic skill
- Building multi-agent systems from framework clusters
- Enabling non-technical users to access framework methodology
- Creating persistent, stateful framework interactions

**Do NOT use when:**
- Framework isn't mature enough (refine first using skill-builder)
- No API/deployment need (keep as Claude Code skill)

## Prerequisites

- **Node.js 22.13.0+** (required for Mastra v1 Beta)
- **Mastra v1 Beta packages**: `@mastra/core@beta`, `@mastra/hono@beta`
- **A mature framework** (score 19+ on 24-point evaluation)

## The Conversion States

### C1: No Framework Analysis
**Symptoms:** Jumping to code without understanding framework structure.
**Test:** Can you list diagnostic states, vocabulary terms, and process phases?
**Intervention:** Run framework analysis first. Extract structure systematically.

### C2: States Without Tools
**Symptoms:** Agent exists but can't diagnose. Framework states not exposed.
**Test:** Can the agent identify which diagnostic state applies to input?
**Intervention:** Convert each diagnostic state to a tool with structured output.

### C3: Tools Without Workflow
**Symptoms:** Tools exist but no orchestration. Multi-step processes are manual.
**Test:** Are framework phases connected as workflow steps?
**Intervention:** Map framework process to workflow with proper data flow.

### C4: No Structured Output
**Symptoms:** Agent returns prose instead of actionable structure.
**Test:** Can consumers programmatically parse agent responses?
**Intervention:** Add Zod output schemas matching framework vocabulary.

### C5: No Memory Integration
**Symptoms:** Agent forgets context between calls. No persistence.
**Test:** Does agent maintain conversation context? Access prior research?
**Intervention:** Configure memory threads, integrate RAG for knowledge persistence.

### C6: No API Design
**Symptoms:** Agent works but has no clean API interface.
**Test:** Can external systems easily call this agent?
**Intervention:** Design Hono routes, document endpoints, add OpenAPI spec.

### C7: Not Deployed
**Symptoms:** Everything works locally but isn't accessible.
**Test:** Can others access this agent via network?
**Intervention:** Containerize, deploy to cloud, configure hosting.

### C8: Conversion Complete
**Symptoms:** Framework is fully operationalized as deployed agent.
**Indicators:** API accessible, structured outputs, memory working, documented.

## Framework Analysis Process

Before any code, extract these from the framework:

### 1. Diagnostic States
Each state becomes a potential tool or structured output:

| State ID | Name | Symptoms | Test | Intervention |
|----------|------|----------|------|--------------|
| [from framework] | [state name] | [what user notices] | [how to assess] | [what to apply] |

### 2. Vocabulary to Schemas
Framework terms become typed structures:

```typescript
// From framework vocabulary
const VocabularyTermSchema = z.object({
  term: z.string(),
  definition: z.string(),
  depth: z.enum(["introductory", "working", "expert"]),
  domain: z.string(),
});
```

### 3. Processes to Workflows
Framework phases become workflow steps:

```
Phase 0: Analysis     → Step: analyze-input
Phase 1: Expansion    → Step: expand-queries
Phase 2: Synthesis    → Step: synthesize-findings
```

### 4. Context Integration to Memory
Framework persistence patterns map to:
- Vocabulary maps → Vector storage (RAG)
- Conversation context → Thread-based memory
- Prior research → Knowledge retrieval

## Mapping Table: Framework to Agent

| Framework Element | Mastra Equivalent | Implementation |
|-------------------|-------------------|----------------|
| Diagnostic States | Tools with structured output | One tool per state or combined assess-state tool |
| State Assessment | Tool that returns state ID + evidence | Include symptoms matched |
| Intervention Recommendations | Agent instructions + tool suggestions | Dynamic instructions |
| Process Phases | Workflow steps | Sequential with schema matching |
| Vocabulary | Zod schemas + type definitions | Shared types across tools |
| Anti-patterns | Validation logic in tools | Prevent known failure modes |
| Completion Criteria | Workflow output validation | Exit conditions |
| Context Integration | Memory + RAG | Thread + vector storage |
| Health Check Questions | Agent self-reflection tool | Metacognitive assessment |

## Conversion Process

### Step 1: Analyze Framework Structure

Read the framework SKILL.md and extract:
- All diagnostic states with symptoms, tests, interventions
- All vocabulary terms with definitions
- All process phases with inputs/outputs
- All integration points with other skills

Output: Framework analysis JSON (see `examples/research-agent/analysis.json`)

### Step 2: Design Agent Architecture

Decide on structure:
- **Single agent with multiple tools**: For simpler frameworks
- **Multiple specialized agents**: For complex framework clusters
- **Agent network**: For frameworks that coordinate multiple perspectives

### Step 3: Generate Zod Schemas

Create schemas for:
- Each diagnostic state output
- Framework vocabulary terms
- Workflow step inputs/outputs
- API request/response bodies

### Step 4: Implement Diagnostic Tools

For each diagnostic state or combined assessment:

```typescript
export const assessState = createTool({
  id: "assess-state",
  description: "Assess current state and recommend intervention",
  inputSchema: z.object({
    situation: z.string().describe("Description of current situation"),
  }),
  outputSchema: z.object({
    state: StateIdSchema,
    stateName: z.string(),
    symptomsMatched: z.array(z.string()),
    confidence: z.number(),
    recommendedIntervention: z.string(),
    nextActions: z.array(z.string()),
  }),
  execute: async (inputData, context) => {
    // Assessment logic using framework criteria
  },
});
```

### Step 5: Wire Workflow

Connect process phases as workflow steps:

```typescript
const frameworkWorkflow = createWorkflow({
  id: "framework-process",
  inputSchema: WorkflowInputSchema,
  outputSchema: WorkflowOutputSchema,
})
  .then(phase0Step)
  .then(phase1Step)
  .then(synthesisStep)
  .commit();
```

**Critical**: Ensure schema matching between steps. See `references/mastra-workflow-data-flow.md`.

### Step 6: Configure Memory

Set up persistence for framework context:

```typescript
// Thread per topic/session
const thread = `${userId}-${frameworkId}-${topicId}`;

// Vector storage for vocabulary maps
await mastra.vectors?.default.upsert({
  indexName: "vocabulary-maps",
  vectors: vocabularyVectors,
});
```

### Step 7: Design API

Create endpoints for framework operations:

```typescript
// Assessment endpoint
registerApiRoute("/diagnose", {
  method: "POST",
  handler: async (c) => {
    const { situation } = await c.req.json();
    const result = await assessTool.execute({ situation }, context);
    return c.json(result);
  },
});

// Workflow endpoint
registerApiRoute("/process", {
  method: "POST",
  handler: async (c) => {
    const input = await c.req.json();
    const run = frameworkWorkflow.createRun();
    const result = await run.start({ inputData: input });
    return c.json(result);
  },
});
```

### Step 8: Deploy

Containerize and deploy:

```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Anti-Patterns

### The Monolithic Agent
**Problem:** Cramming entire framework into one agent's instructions.
**Symptoms:** Instructions exceed 2000 words, agent confused about scope.
**Fix:** Split diagnostic assessment, interventions, and processes into separate tools/workflows.

### The Schema Orphan
**Problem:** Framework vocabulary exists but no Zod schemas defined.
**Symptoms:** Agent returns inconsistent structures, consumers can't parse.
**Fix:** Every framework term with semantic meaning needs a typed schema.

### The State Black Box
**Problem:** Agent identifies states but doesn't explain reasoning.
**Symptoms:** Users don't trust assessment, can't verify correctness.
**Fix:** Include evidence in structured output: which symptoms matched, which didn't.

### The Memory Amnesiac
**Problem:** Agent doesn't persist vocabulary maps or prior findings.
**Symptoms:** Starting from scratch each session, repeating work.
**Fix:** Configure RAG storage for accumulated knowledge, conversation threads for context.

### The API Afterthought
**Problem:** Agent works but API is poorly designed.
**Symptoms:** Consumers struggle to integrate, endpoints are inconsistent.
**Fix:** Design API contracts before implementation. Consider consumer needs.

### The Workflow Spaghetti
**Problem:** Workflow steps don't match schemas, data flow is broken.
**Symptoms:** Runtime errors, steps receive undefined inputs.
**Fix:** Validate schema matching at design time. Use `.map()` for transformations.

## Available Scripts

### analyze-framework.ts
Extract structure from framework/skill document.

```bash
deno run --allow-read scripts/analyze-framework.ts path/to/SKILL.md
```

### scaffold-framework-agent.ts
Generate full project structure from framework analysis.

```bash
deno run --allow-all scripts/scaffold-framework-agent.ts \
  --framework research \
  --analysis ./analysis.json \
  --output ./agents/research-agent
```

### generate-diagnostic-tools.ts
Auto-generate tool files from diagnostic states.

```bash
deno run --allow-all scripts/generate-diagnostic-tools.ts \
  --states ./states.json \
  --output ./src/mastra/tools/
```

### generate-schemas.ts
Generate Zod schemas from vocabulary.

```bash
deno run --allow-all scripts/generate-schemas.ts \
  --vocabulary ./vocabulary.json \
  --output ./src/schemas/
```

### validate-conversion.ts
Check conversion completeness against checklist.

```bash
deno run --allow-read scripts/validate-conversion.ts ./agents/research-agent
```

## Example: Research Framework Conversion

See `examples/research-agent/` for complete worked example.

### Framework Analysis Summary

The research skill has:
- **10 diagnostic states** (R1-R10): No Analysis, No Vocabulary Map, Single-Perspective, Domain Blindness, Recency Bias, Breadth Without Depth, Completion Uncertainty, Research Complete, No Persistence, Scope Mismatch, No Confidence Signaling
- **Key vocabulary**: Phase 0 Analysis, Vocabulary Map, Core Terms, Depth Levels, Diminishing Returns, Single-Shot Research, Scope Calibration, Confidence Markers
- **Process phases**: Phase 0 (Analysis) → Phase 1.5 (Vocabulary) → Phase 2 (Query Construction) → Synthesis
- **Integration points**: context-networks (storage), fact-check (verification)

### Generated Agent Structure

```
research-agent/
├── src/mastra/
│   ├── agents/research-agent.ts    # Main agent with framework instructions
│   ├── tools/
│   │   ├── assess-state.ts         # Diagnose research state (R1-R10)
│   │   ├── run-phase0.ts           # Execute Phase 0 analysis
│   │   ├── build-vocabulary.ts     # Build vocabulary map
│   │   ├── expand-queries.ts       # Generate search queries
│   │   ├── retrieve-prior.ts       # Get prior research/vocabulary
│   │   └── synthesize.ts           # Create synthesis with confidence
│   ├── workflows/
│   │   ├── full-research.ts        # Complete research workflow
│   │   └── single-shot.ts          # Time-boxed research workflow
│   └── index.ts                    # Mastra instance
├── src/schemas/
│   ├── vocabulary.ts               # VocabularyMapSchema
│   ├── analysis.ts                 # Phase0AnalysisSchema
│   ├── synthesis.ts                # ResearchSynthesisSchema
│   └── states.ts                   # DiagnosticStateSchema
├── src/index.ts                    # Hono server
└── Dockerfile
```

### API Endpoints

```
POST /api/agents/research-agent/diagnose
Body: { "situation": "I'm researching X but keep finding surface-level content" }
Response: { "state": "R1.5", "stateName": "No Vocabulary Map", "intervention": "Build vocabulary map", ... }

POST /api/agents/research-agent/start-research
Body: { "topic": "gentrification of workwear", "timeBox": "2h", "depth": "working" }
Response: { "workflowRunId": "...", "status": "started" }

GET /api/workflows/full-research/{runId}/status
Response: { "status": "running", "currentStep": "vocabulary-mapping", ... }

POST /api/agents/research-agent/synthesize
Body: { "topic": "...", "findings": [...], "confidenceLevel": "medium" }
Response: { "synthesis": {...}, "confidenceLevel": "medium", "caveats": [...] }
```

## Output Persistence

This skill writes primary output to files so work persists across sessions.

### Output Discovery

**Before doing any other work:**

1. Check for `context/output-config.md` in the project
2. If found, look for this skill's entry
3. If not found or no entry for this skill, **ask the user first**:
   - "Where should I save output from this framework-to-mastra session?"
   - Suggest: `agents/` or a sensible location for agent code
4. Store the user's preference:
   - In `context/output-config.md` if context network exists
   - In `.framework-to-mastra-output.md` at project root otherwise

### Primary Output

For this skill, persist:
- **Framework analysis** - extracted states, vocabulary, processes
- **Generated agent code** - full project structure
- **Schema definitions** - Zod schemas for framework vocabulary
- **Conversion checklist** - validation of completeness

### Conversation vs. File

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| Analysis JSON | Discussion of framework structure |
| Generated code files | Iteration on design |
| Schema definitions | Real-time feedback |
| Validation reports | Deployment decisions |

### File Naming

Pattern: `{framework-name}-agent/` (directory structure)
Example: `agents/research-agent/`

## What You Do NOT Do

- You do not convert immature frameworks (refine first using skill-builder)
- You do not skip framework analysis
- You do not hard-code what should be configurable
- You do not deploy without testing
- You do not ignore schema matching in workflows
- You guide the conversion; the user decides what to deploy

## Integration Points

| Skill | Connection |
|-------|------------|
| **skill-builder** | Use to refine framework before conversion |
| **context-networks** | Agent memory maps to context network structure |
| **research** | Primary worked example for conversion |
| **story-sense** | Complex diagnostic example with multiple states |

## Additional Resources

### Reference Files
- **`references/framework-analysis.md`** - How to analyze a framework for conversion
- **`references/diagnostic-to-tool.md`** - Converting diagnostic states to tools
- **`references/process-to-workflow.md`** - Converting processes to workflows
- **`references/vocabulary-to-schema.md`** - Framework vocabulary to Zod schemas
- **`references/context-to-memory.md`** - Context networks to agent memory
- **`references/api-design-patterns.md`** - API design for framework agents
- **`references/deployment-patterns.md`** - Hosting and containerization
- **`references/mastra-core-patterns.md`** - Mastra v1 Beta fundamentals
- **`references/mastra-workflow-data-flow.md`** - Critical workflow patterns
- **`references/mastra-server-patterns.md`** - Hono server setup
- **`references/mastra-memory-patterns.md`** - RAG and conversation memory

### Asset Templates
- **`assets/framework-agent-template.ts`** - Agent template
- **`assets/diagnostic-tool-template.ts`** - Diagnostic tool template
- **`assets/intervention-tool-template.ts`** - Intervention tool template
- **`assets/framework-workflow-template.ts`** - Workflow template
- **`assets/context-memory-template.ts`** - Memory/RAG setup
- **`assets/framework-server-template.ts`** - Hono server template
- **`assets/zod-schema-examples.ts`** - Common schema patterns

## Mastra Version Note

**Target version**: Mastra v1 Beta (stable release expected January 2026)

Patterns in this skill are for v1 Beta. Stable (0.24.x) patterns differ significantly - especially tool signatures and workflow data access.
