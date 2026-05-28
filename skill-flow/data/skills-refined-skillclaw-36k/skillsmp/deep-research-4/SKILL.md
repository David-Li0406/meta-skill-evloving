---
name: deep-research
description: Perform comprehensive research using the diffusion research loop with domain specialization. Supports general web research and specialized domains (geopolitical with GDELT). Auto-detects domain from query or accepts explicit --domain flag. Use when you need thorough, multi-perspective research with citations.
---

<objective>
Execute deep, comprehensive research on any topic using a multi-agent diffusion loop with domain-aware specialization:
1. Classify query and detect appropriate domain (general, geopolitical, etc.)
2. Break down the query into research dimensions using domain config
3. Spawn parallel worker agents appropriate for the domain
4. Synthesize findings into a coherent draft
5. Use domain-specific gap detection to identify missing coverage
6. Iterate until coverage is sufficient
7. Produce a final report with full citations in domain-appropriate format
</objective>

<essential_principles>
## The Diffusion Research Pattern

This skill implements **Self-Balancing Test-Time Diffusion** - starting with a noisy/speculative understanding and iteratively refining through parallel, isolated research workers.

### Key Design Principles

1. **Domain Awareness**: Different research domains require different tools, agents, and evaluation criteria. The skill auto-detects domain or accepts explicit specification.

2. **Worker Isolation**: Each research worker receives ONLY their assigned topic. They cannot see:
   - Other workers' findings
   - The current draft
   - The full research brief
   This prevents herd behavior and ensures diverse perspectives.

3. **Gap Detection Objectivity**: Use a separate gap-detector agent (not yourself) to evaluate coverage. This avoids the bias of judging your own work. Each domain has specialized gap detection dimensions.

4. **Conservative Iteration**: Continue researching if:
   - Coverage < 70% of core questions
   - Any critical question is unanswered
   Stop when diminishing returns are reached.

5. **Quality Over Quantity**: 3-5 well-sourced findings per worker beats 10 weakly-sourced ones.
</essential_principles>

<domains>
## Available Domains

### General (Default)
- **Triggers**: Any query not matching other domains
- **Prefix**: `core`
- **Agents**: `deep-research:core:research-worker`, `deep-research:core:gap-detector`
- **Tools**: WebSearch, WebFetch
- **Config**: `domains/general.md`

### Geopolitical
- **Triggers**: conflict, war, sanctions, bilateral relations, media coverage, GDELT, CAMEO
- **Prefix**: `geo`
- **Agents**: Specialized analysts (conflict, sanctions, actors, sentiment, trends)
- **Tools**: GDELT MCP tools (gdelt_events, gdelt_gkg, gdelt_actors, etc.) + WebSearch
- **Config**: `domains/geopolitical.md`

## Domain Detection

The skill automatically detects domain based on query keywords:

```
IF query contains (conflict, war, military, violence, escalation, sanctions,
   embargo, OFAC, bilateral, alliance, media coverage, sentiment, GDELT, CAMEO):
   → Use GEOPOLITICAL domain
ELSE:
   → Use GENERAL domain
```

Override with explicit flag: `/deep-research --domain=geopolitical "query here"`
</domains>

<algorithm>
## The Research Loop

```
PHASE 0: DOMAIN CLASSIFICATION & REFINEMENT (Interactive)
├── 0.1 Parse user query
├── 0.2 Detect domain (general | geopolitical | ...)
├── 0.3 Load domain config (agents, tools, gap dimensions, output format)
├── 0.4 Generate DRAFT research brief using domain expertise
├── 0.5 Present brief to user via AskUserQuestion
│   ├── "Is this domain correct?"
│   ├── "Are these dimensions correct?"
│   ├── "Any areas to add or remove?"
│   └── "What depth/focus do you need?"
├── 0.6 Refine brief based on feedback
└── 0.7 Confirm and proceed

PHASE 1: INITIALIZATION
├── 1.1 Finalize research brief from refinement
├── 1.2 Select domain-appropriate agents
└── 1.3 Generate initial speculative draft (noisy starting point)

PHASE 2: DIFFUSION LOOP (max 3 iterations)
├── 2.1 SPAWN WORKERS
│   ├── Identify 2-5 research topics from brief/gaps
│   ├── Launch domain-specific worker agents in PARALLEL
│   └── Collect findings (wait for all to complete)
│
├── 2.2 SYNTHESIZE
│   ├── Merge worker findings into current draft
│   ├── Resolve contradictions
│   └── Structure with citations
│
├── 2.3 GAP DETECTION
│   ├── Launch domain-specific gap-detector with: query, brief, draft
│   ├── Receive coverage score and gap topics
│   └── Decision: CONTINUE (spawn more workers) or COMPLETE
│
└── 2.4 ITERATE or EXIT

PHASE 3: FINAL REPORT
├── 3.1 Polish synthesis using domain output template
├── 3.2 Compile all sources with descriptions
└── 3.3 Add executive summary
```

## Execution Modes

**Interactive (default):** Main Claude orchestrates, can ask questions and steer mid-research.

**Background:** Spawn `deep-research:core:research-orchestrator` for autonomous research. Use when user wants to continue other work.
</algorithm>

<intake>
What would you like me to research?

Provide your research question or topic. I will:
1. Auto-detect the appropriate domain (or you can specify `--domain=geopolitical`)
2. Break it down into researchable dimensions
3. Deploy parallel research agents with domain expertise
4. Synthesize findings with citations
5. Iterate until comprehensive coverage

**General Research Examples:**
- "What are the latest developments in quantum computing for drug discovery?"
- "Compare the architectural approaches of major LLM providers"
- "How are companies implementing AI governance frameworks?"

**Geopolitical Research Examples** (auto-detected):
- "What is the current state of the Russia-Ukraine conflict?"
- "How effective have semiconductor sanctions on China been?"
- "Map the relationship network around the Gulf Cooperation Council"
- "How is Western vs BRICS media covering the Israel-Palestine situation?"
</intake>

<execution_guide>
## Phase 0: Domain Classification & Refinement

### Step 1: Detect Domain

Analyze the query for domain signals:

```markdown
## Domain Classification

**Your Query:** [User's original question]

**Detected Domain:** [general | geopolitical]

**Domain Signals Found:**
- [Signal 1]: [keyword or pattern that triggered detection]
- [Signal 2]: ...

**Domain Config Loaded:** domains/[domain].md
```

### Step 2: Generate Draft Brief (Domain-Aware)

**For General Domain:**
```markdown
## Draft Research Brief

**Query:** [User's original question]
**Domain:** General

**Proposed Dimensions:**
1. [Dimension 1] - [Why it matters]
2. [Dimension 2] - [Why it matters]
3. [Dimension 3] - [Why it matters]

**Key Questions I Plan to Answer:**
- [Question 1] (Core)
- [Question 2] (Core)
- [Question 3] (Supporting)
```

**For Geopolitical Domain:**
```markdown
## Draft Research Brief

**Query:** [User's original question]
**Domain:** Geopolitical
**Analysis Type:** [Conflict | Sanctions | Actors | Narrative | Multi-Dimensional]

**Geographic Scope:** [Countries/regions]
**Temporal Scope:** [Time period]
**Key Actors:** [Primary actors to track]

**Proposed Dimensions:**
1. [Dimension 1] - [Why it matters for this analysis]
2. [Dimension 2] - [Why it matters]
3. [Dimension 3] - [Why it matters]

**Key Questions I Plan to Answer:**
- [Question 1] (Core)
- [Question 2] (Core)
- [Question 3] (Supporting)

**Specialist Agents to Deploy:**
1. [Agent 1] for [Focus area]
2. [Agent 2] for [Focus area]
```

### Step 3: Validate with User

```
AskUserQuestion(
  questions: [
    {
      header: "Domain",
      question: "Is this the right research domain for your query?",
      options: [
        { label: "Yes, proceed", description: "Domain and approach look correct" },
        { label: "Switch to general", description: "Use general web research instead" },
        { label: "Switch to geopolitical", description: "Use GDELT + specialized agents" }
      ],
      multiSelect: false
    },
    {
      header: "Dimensions",
      question: "Are these research dimensions correct for your needs?",
      options: [
        { label: "Yes, proceed", description: "These dimensions cover what I need" },
        { label: "Add more", description: "I want to add additional dimensions" },
        { label: "Remove some", description: "Some dimensions aren't relevant" },
        { label: "Rethink entirely", description: "Let's approach this differently" }
      ],
      multiSelect: false
    },
    {
      header: "Depth",
      question: "What level of depth do you need?",
      options: [
        { label: "Quick overview", description: "Key facts, 1 iteration, ~2 min" },
        { label: "Standard (Recommended)", description: "Thorough coverage, 2-3 iterations, ~5 min" },
        { label: "Exhaustive", description: "Maximum depth, all angles, ~10 min" }
      ],
      multiSelect: false
    }
  ]
)
```

### Step 4: Refine Based on Feedback

- If user switches domain → reload domain config, regenerate brief
- If user selects "Add more" → ask what to add
- If user selects "Remove some" → ask what to remove
- Adjust depth and focus based on selections
- Proceed to Phase 1 once confirmed

---

## Phase 1: Spawn Domain-Appropriate Workers

### General Domain Workers

```
Task(
  subagent_type: "deep-research:core:research-worker",
  prompt: "Research this topic: [TOPIC]

Context: This is part of a larger research effort on: [MAIN QUERY]

Focus on: [SPECIFIC ASPECTS TO COVER]

Return structured findings with citations.",
  description: "Research: [short topic]"
)
```

### Geopolitical Domain Workers

See `domains/geopolitical.md` for detailed agent prompts. Key patterns:

**Conflict Analysis:**
```
Task(
  subagent_type: "deep-research:geo:conflict-analyst",
  prompt: "Analyze conflict dynamics for: [TOPIC]

  Focus on: CAMEO events, Goldstein trends, actor relationships
  Use: gdelt_events, gdelt_actors, gdelt_gkg
  Return: Structured findings with GDELT citations",
  description: "Conflict analysis: [topic]"
)
```

**Sanctions Research:**
```
Task(
  subagent_type: "deep-research:geo:sanctions-researcher",
  prompt: "Research sanctions for: [TOPIC]

  Focus on: Active regimes, enforcement, evasion patterns
  Use: gdelt_gkg, gdelt_doc, gdelt_trends
  Return: Findings with quantitative data",
  description: "Sanctions research: [topic]"
)
```

**Actor Mapping:**
```
Task(
  subagent_type: "deep-research:geo:actor-mapper",
  prompt: "Map actor relationships for: [TOPIC]

  Focus on: Actor types, Goldstein patterns, alliance structures
  Use: gdelt_events, gdelt_actors
  Return: Network analysis with metrics",
  description: "Actor mapping: [topic]"
)
```

**Narrative Analysis:**
```
Task(
  subagent_type: "deep-research:geo:sentiment-tracker",
  prompt: "Analyze media sentiment for: [TOPIC]

  Focus on: Tone, regional differences, narrative themes
  Use: gdelt_gkg, gdelt_doc
  Return: Quantified sentiment analysis",
  description: "Sentiment analysis: [topic]"
)

Task(
  subagent_type: "deep-research:geo:trend-analyst",
  prompt: "Analyze coverage trends for: [TOPIC]

  Focus on: Volume timeline, inflection points, patterns
  Use: gdelt_trends, gdelt_events
  Return: Trend analysis with forecasting",
  description: "Trend analysis: [topic]"
)
```

**CRITICAL**: Spawn ALL workers in a SINGLE message with multiple Task tool calls. This enables true parallel execution.

---

## Phase 2: Synthesis and Gap Detection

### Synthesize Findings

After workers return, merge into a draft:

```markdown
## Research Draft (Iteration N)

### [Theme 1]

[Synthesized content from relevant worker findings]

Sources:
- [1] [URL]
- [2] [URL]

### [Theme 2]

[Synthesized content...]

### Current Gaps

[Note any obvious gaps before formal gap detection]
```

### Gap Detection (Domain-Specific)

**General Domain:**
```
Task(
  subagent_type: "deep-research:core:gap-detector",
  prompt: "Evaluate research coverage:

ORIGINAL QUERY:
[Query]

RESEARCH BRIEF:
[Brief]

CURRENT FINDINGS:
[Draft]

ITERATION: [N]

Assess coverage and identify gaps for follow-up.",
  description: "Detect research gaps"
)
```

**Geopolitical Domain:**
```
Task(
  subagent_type: "deep-research:geo:gap-detector-geo",
  prompt: "Evaluate geopolitical research coverage:

ORIGINAL QUERY:
[Query]

RESEARCH BRIEF:
[Brief]

CURRENT FINDINGS:
[Draft]

ITERATION: [N]

Assess coverage across:
- Core dimensions (3x weight): Temporal, Actor, Data Source
- Supporting dimensions (2x weight): Quantification, Geographic, Perspective
- Contextual dimensions (1x weight): Precedents, Expert Sources, Timeline

Provide weighted coverage score and specific gaps for follow-up.",
  description: "Evaluate geopolitical coverage"
)
```

### Iterate or Complete

If gap-detector returns CONTINUE:
- Extract the gap topics
- Spawn new workers for those specific gaps
- Repeat synthesis and gap detection

If gap-detector returns COMPLETE:
- Move to Phase 3

**Maximum 3 iterations** to prevent infinite loops.

---

## Phase 3: Final Report

Use domain-specific output template from the domain config file.

**General Domain:** See `domains/general.md` for output format

**Geopolitical Domain:** See `domains/geopolitical.md` for output format (includes GDELT metrics, actor matrices, Goldstein analysis)

Save to: `research_output/[topic-slug]_[date].md`
</execution_guide>

<worker_management>
## Managing Research Workers

### Spawning Pattern

Always spawn workers in parallel using a single message with multiple Task calls:

```
[In a single response, include multiple Task tool invocations:]

Task 1: "Research: quantum computing applications"
Task 2: "Research: drug discovery AI methods"
Task 3: "Research: current clinical trials"
```

### General Worker Prompt Template

```
You are researching: [SPECIFIC TOPIC]

This is part of a larger investigation into: [MAIN QUERY]

Your focus areas:
- [Specific aspect 1]
- [Specific aspect 2]
- [Specific aspect 3]

Requirements:
- Use WebSearch for discovery, WebFetch for deep content
- Cite every factual claim with source URLs
- Return 3-7 key findings with confidence levels
- Note any contradictions or debates in the field
- Stop when you have sufficient coverage (5-7 searches max)

Do not research topics outside your assigned focus.
```

### Handling Worker Failures

If a worker returns an error or incomplete results:
- Note the gap in synthesis
- The gap detector will flag it for follow-up
- Do not block other workers
</worker_management>

<mid_research_steering>
## Mid-Research Steering

During the diffusion loop, watch for user messages that indicate steering:

| User Says | Action |
|-----------|--------|
| "Focus more on X" | Add X-related topics to next worker batch |
| "Skip Y" | Remove Y from remaining work, note as out-of-scope |
| "Go deeper on Z" | Spawn additional worker specifically for Z |
| "That's enough" | Skip remaining iterations, move to final report |
| "Add dimension W" | Update brief, spawn worker for W |
| "Switch to geopolitical" | Reload geopolitical domain config, adjust agents |

Use AskUserQuestion if steering intent is ambiguous:

```
AskUserQuestion(
  questions: [{
    header: "Clarify",
    question: "You mentioned focusing on X. Should I...",
    options: [
      { label: "Add worker for X", description: "Research X specifically in next round" },
      { label: "Prioritize X in synthesis", description: "Weight X findings more heavily" },
      { label: "Replace other dimensions", description: "Drop less relevant dimensions for X" }
    ],
    multiSelect: false
  }]
)
```
</mid_research_steering>

<output_specifications>
## Output File Location

Save reports to: `research_output/[topic-slug]_[date].md`

Example: `research_output/quantum-computing-healthcare_2024-01-15.md`

For geopolitical: `research_output/geo/[topic-slug]_[date].md`

## Required Sections (All Reports)

1. **Metadata Header**
   - Query
   - Domain used
   - Date
   - Iterations performed
   - Workers spawned

2. **Executive Summary** (bullet points, 100-200 words)

3. **Key Findings** (3-7 major findings with sources)

4. **Detailed Analysis** (cross-cutting themes, implications)

5. **Methodology Note** (brief explanation of research process)

6. **Complete Source List** (all URLs with descriptions)

Additional domain-specific sections are defined in each domain config.
</output_specifications>

<success_criteria>
## Research Completion Criteria

Research is complete when:
- All core questions from the brief are addressed
- Coverage score >= 70% (from gap detector)
- Key findings are well-sourced (2+ citations each)
- Contradictions are noted and explained
- Maximum 3 iterations reached

Research is NOT complete just because:
- The draft "reads well"
- You feel satisfied with the findings
- Workers stopped returning new information

Always use the domain-appropriate gap-detector agent for objective evaluation.
</success_criteria>

<quick_start>
## Quick Start

1. User provides research query
2. **Detect domain** (general or geopolitical)
3. Load domain config
4. Generate DRAFT research brief
5. **Use AskUserQuestion to validate domain, dimensions, depth**
6. Refine brief based on feedback
7. Spawn 2-4 domain-appropriate worker agents in parallel
8. Synthesize findings into draft
9. Spawn domain-specific gap-detector agent
10. If gaps found: spawn more workers for gap topics, repeat
11. If complete: generate final report using domain output template

**Time expectation:** 2-10 minutes depending on domain, depth, and iterations

**Skip refinement:** If user explicitly says "just do it" or "skip questions", proceed directly with your best judgment on the brief.
</quick_start>
