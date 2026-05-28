---
name: eiffel-research
description: Pre-Phase research for new simple_* libraries. 7-step investigation process before design. Use when starting a new library idea. Produces research output for /eiffel.spec.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task, WebSearch, WebFetch
---

# /eiffel.research - Pre-Phase: Deep Research

**Purpose:** Systematically research a new library idea BEFORE design. Transforms a vague idea into validated requirements.

## When to Use

- **New simple_* library** - Before creating any new library
- **Major feature** - Before adding significant capability
- **Technology selection** - Choosing between approaches
- **Problem unclear** - When the problem space needs exploration

## Usage

```
/eiffel.research <project-path>
```

**Example:**
```
/eiffel.research d:\prod\simple_cache
```

## CRITICAL: Anti-Slop Rules

**This workflow requires ACTUAL:**
- Web searches with real URLs (WebSearch/WebFetch tools)
- Documentation written to actual files
- Sources cited with actual URLs

**FORBIDDEN:**
- Making up library names or features
- Citing documentation without actual URLs
- Claiming "research complete" without written deliverables

## Project Scoping

```
<project-path>/
├── .eiffel-workflow/
│   └── research/
│       ├── 01-SCOPE.md
│       ├── 02-LANDSCAPE.md
│       ├── 03-REQUIREMENTS.md
│       ├── 04-DECISIONS.md
│       ├── 05-INNOVATIONS.md
│       ├── 06-RISKS.md
│       ├── 07-RECOMMENDATION.md
│       └── REFERENCES.md
```

## The 7-Step Framework

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: SCOPE         (Define what we're researching)      │
│  STEP 2: LANDSCAPE     (What already exists?)               │
│  STEP 3: REQUIREMENTS  (What must it do?)                   │
│  STEP 4: DECISIONS     (What design choices?)               │
│  STEP 5: INNOVATIONS   (What's novel?)                      │
│  STEP 6: RISKS         (What could go wrong?)               │
│  STEP 7: RECOMMENDATION (What should we do?)                │
└─────────────────────────────────────────────────────────────┘
```

## Workflow

### Step 0: Get Initial Idea

Ask user for:
```
IDEA: {one-sentence description}
CONTEXT: {why we want this}
INITIAL THOUGHTS: {any preliminary ideas}
CONSTRAINTS: {known limitations}
```

### Step 1: SCOPE - Define Boundaries

Create `<project-path>/.eiffel-workflow/research/01-SCOPE.md`:

**Must answer:**
- What problem are we solving?
- Who has this problem?
- What does success look like?
- What's definitely NOT in scope?

**Template:**
```markdown
# SCOPE: {project_name}

## Problem Statement
In one sentence: {The problem is...}

What's wrong today: {current pain}
Who experiences this: {affected users}
Impact of not solving: {consequence}

## Target Users
| User Type | Needs | Pain Level |
|-----------|-------|------------|
| {type} | {needs} | HIGH/MED/LOW |

## Success Criteria
| Level | Criterion | Measure |
|-------|-----------|---------|
| MVP | {criterion} | {measure} |
| Full | {criterion} | {measure} |

## Scope Boundaries
### In Scope (MUST)
- {capability}

### In Scope (SHOULD)
- {capability}

### Out of Scope
- {excluded}: {reason}

### Deferred to Future
- {future item}: {why later}

## Constraints
| Type | Constraint |
|------|------------|
| Technical | {constraint} |
| Resource | {constraint} |

## Assumptions to Validate
| ID | Assumption | Risk if False |
|----|------------|---------------|
| A-1 | {assumption} | {risk} |

## Research Questions
- {question about the problem}
- {question about existing solutions}
- {question about feasibility}
```

### Step 2: LANDSCAPE - Survey Existing Solutions

Create `<project-path>/.eiffel-workflow/research/02-LANDSCAPE.md`:

**ACTUALLY search the web:**
```
WebSearch: "{problem domain} library"
WebSearch: "{technology} Eiffel"
WebSearch: "{comparable solution} comparison"
```

**Must research:**
- At least 3 alternative solutions
- Eiffel ecosystem (simple_*, ISE, Gobo)
- Other language solutions that could inform design

**Template:**
```markdown
# LANDSCAPE: {project_name}

## Existing Solutions

### {Solution 1}
| Aspect | Assessment |
|--------|------------|
| Type | LIBRARY/FRAMEWORK/SERVICE |
| Platform | {language/platform} |
| URL | {actual URL} |
| Maturity | MATURE/GROWING/EXPERIMENTAL |
| License | {license} |

**Strengths:**
- {strength}

**Weaknesses:**
- {weakness}

**Relevance:** {percent}%

### {Solution 2}
...

## Eiffel Ecosystem Check

### ISE Libraries
- {library}: {relevance}

### simple_* Libraries
- {simple_*}: {relevance}

### Gobo Libraries
- {library}: {relevance}

### Gap Analysis
Not available in Eiffel: {what's missing}

## Comparison Matrix
| Feature | Solution A | Solution B | Our Need |
|---------|------------|------------|----------|
| {feature} | ✓/✗ | ✓/✗ | MUST/SHOULD |

## Patterns Identified
| Pattern | Seen In | Adopt? |
|---------|---------|--------|
| {pattern} | {solutions} | YES/NO |

## Build vs Buy vs Adapt
| Option | Effort | Risk | Fit |
|--------|--------|------|-----|
| Build | HIGH/MED/LOW | HIGH/MED/LOW | {%} |
| Adopt | HIGH/MED/LOW | HIGH/MED/LOW | {%} |
| Adapt | HIGH/MED/LOW | HIGH/MED/LOW | {%} |

**Initial Recommendation:** {BUILD/ADOPT/ADAPT}
```

### Step 3: REQUIREMENTS - Define Needs

Create `<project-path>/.eiffel-workflow/research/03-REQUIREMENTS.md`:

**Template:**
```markdown
# REQUIREMENTS: {project_name}

## Functional Requirements
| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-001 | {requirement} | MUST | {how to verify} |
| FR-002 | {requirement} | SHOULD | {how to verify} |

## Non-Functional Requirements
| ID | Requirement | Category | Measure | Target |
|----|-------------|----------|---------|--------|
| NFR-001 | {requirement} | PERFORMANCE | {measure} | {target} |
| NFR-002 | {requirement} | SECURITY | {measure} | {target} |

## Constraints
| ID | Constraint | Type | Immutable? |
|----|------------|------|------------|
| C-001 | Must be SCOOP-compatible | TECHNICAL | YES |
| C-002 | Must prefer simple_* over ISE | ECOSYSTEM | YES |
```

### Step 4: DECISIONS - Make Choices

Create `<project-path>/.eiffel-workflow/research/04-DECISIONS.md`:

**Template:**
```markdown
# DECISIONS: {project_name}

## Decision Log

### D-001: {Decision Title}
**Question:** {what needed deciding}
**Options:**
1. {option 1}: {pros/cons}
2. {option 2}: {pros/cons}

**Decision:** {chosen option}
**Rationale:** {why}
**Implications:** {what this means for design}
**Reversible:** YES/NO

### D-002: {Decision Title}
...
```

### Step 5: INNOVATIONS - Identify Novel Approaches

Create `<project-path>/.eiffel-workflow/research/05-INNOVATIONS.md`:

**Template:**
```markdown
# INNOVATIONS: {project_name}

## What Makes This Different

### I-001: {Innovation Title}
**Problem Solved:** {what it addresses}
**Approach:** {how it works}
**Novelty:** {why this is new/different}
**Design Impact:** {what this means for structure}

## Differentiation from Existing Solutions
| Aspect | Existing | Our Approach | Benefit |
|--------|----------|--------------|---------|
| {aspect} | {how others do it} | {our way} | {why better} |
```

### Step 6: RISKS - Identify What Could Go Wrong

Create `<project-path>/.eiffel-workflow/research/06-RISKS.md`:

**Template:**
```markdown
# RISKS: {project_name}

## Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|------------|--------|------------|
| RISK-001 | {risk description} | HIGH/MED/LOW | HIGH/MED/LOW | {mitigation strategy} |

## Technical Risks
### RISK-001: {Risk Title}
**Description:** {what could go wrong}
**Likelihood:** HIGH/MEDIUM/LOW
**Impact:** HIGH/MEDIUM/LOW
**Indicators:** {how we'd know it's happening}
**Mitigation:** {how to prevent/handle}
**Contingency:** {fallback plan}

## Ecosystem Risks
{Risks related to dependencies, compatibility}

## Resource Risks
{Risks related to time, skills, effort}
```

### Step 7: RECOMMENDATION - Final Direction

Create `<project-path>/.eiffel-workflow/research/07-RECOMMENDATION.md`:

**Template:**
```markdown
# RECOMMENDATION: {project_name}

## Executive Summary
{2-3 sentence summary of recommendation}

## Recommendation
**Action:** BUILD / ADOPT / ADAPT / ABANDON
**Confidence:** HIGH / MEDIUM / LOW

## Rationale
{Why this recommendation}

## Proposed Approach
### Phase 1 (MVP)
- {feature}
- {feature}

### Phase 2 (Full)
- {feature}

## Key Features
1. {feature}: {brief description}
2. {feature}: {brief description}

## Success Criteria
- {measurable criterion}

## Dependencies
| Library | Purpose | simple_* Preferred |
|---------|---------|-------------------|
| {lib} | {why needed} | YES/NO |

## Next Steps
1. Run `/eiffel.spec` to transform this research into specification
2. Then `/eiffel.intent` to capture refined intent
3. Continue with Eiffel Spec Kit workflow

## Open Questions
{Any unresolved questions for spec phase}
```

### Step 8: Compile References

Create `<project-path>/.eiffel-workflow/research/REFERENCES.md`:

**Template:**
```markdown
# REFERENCES: {project_name}

## Documentation Consulted
- {URL}: {what we learned}

## Repositories Examined
- {URL}: {relevant code}

## Articles/Papers
- {URL}: {key insight}

## Discussions/Forums
- {URL}: {community perspective}
```

### Step 9: Save Evidence

Create `<project-path>/.eiffel-workflow/evidence/pre-phase-research.txt`:
```
# Pre-Phase Research Evidence
# Project: <project-path>
# Date: [timestamp]

Research completed: [yes/no]
Steps completed: 7/7
Recommendation: BUILD/ADOPT/ADAPT/ABANDON
Confidence: HIGH/MEDIUM/LOW

References cited: [count]
Alternatives researched: [count]
Risks identified: [count]

# Status: COMPLETE
```

## Completion

```
Pre-Phase RESEARCH COMPLETE: Research validated.
Project: <project-path>

Files:
  - .eiffel-workflow/research/01-SCOPE.md
  - .eiffel-workflow/research/02-LANDSCAPE.md
  - .eiffel-workflow/research/03-REQUIREMENTS.md
  - .eiffel-workflow/research/04-DECISIONS.md
  - .eiffel-workflow/research/05-INNOVATIONS.md
  - .eiffel-workflow/research/06-RISKS.md
  - .eiffel-workflow/research/07-RECOMMENDATION.md
  - .eiffel-workflow/research/REFERENCES.md

Recommendation: {BUILD/ADOPT/ADAPT}

Next: Run /eiffel.spec <project-path> to transform research into Eiffel specification.
```

## Context Management (RLM Pattern)

**DO:**
- Use WebSearch and WebFetch for actual research
- Use Task tool with Explore agent for ecosystem questions
- Write findings to actual files as you go

**DO NOT:**
- Make up library names or features
- Cite URLs without actually fetching them
- Skip steps or claim research without evidence

## Research Quality Criteria

| Step | Criterion |
|------|-----------|
| Scope | Problem clearly stated, boundaries defined |
| Landscape | At least 3 alternatives researched with real URLs |
| Requirements | Prioritized with acceptance criteria |
| Decisions | Options evaluated, rationale recorded |
| Innovations | Differentiation clearly stated |
| Risks | Identified with mitigations |
| Recommendation | Clear, evidence-based, actionable |

## Anti-Drift

- **Every claim needs evidence** - URLs, code samples, actual data
- **No imaginary libraries** - Only cite what actually exists
- **Research before recommend** - Don't skip to conclusions
- **simple_* first** - Check ecosystem before recommending ISE/Gobo
