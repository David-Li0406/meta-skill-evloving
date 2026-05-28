---
name: deep-research
description: Multi-phase exploration agent for broad research and validation. Discovers subtopics, delegates parallel research, then synthesizes findings with source review.
---

# Deep Research Skill

A multi-phase exploration agent that broadly scans a topic, identifies key areas, delegates subtopic research to parallel agents, and synthesizes findings with comprehensive source validation.

## When to Use

- Exploring a new domain or technology you know little about
- Researching a complex topic with multiple facets
- Need validated findings with cross-referenced sources
- Want a comprehensive overview before making decisions

## Workflow Overview

```
Phase 1: DISCOVERY     → Broad scan, identify 5-8 subtopics
Phase 2: PLANNING      → Create structure, get user approval
Phase 3: RESEARCH      → Parallel agents research each subtopic
Phase 4: SYNTHESIS     → Unified overview + source validation (user-triggered)
```

---

## Phase 1: Discovery

**Goal:** Broadly explore the topic to identify key subtopics and questions.

### Step 1.1: Check Existing Knowledge

Search memory for prior research:
```javascript
memory({ mode: "search", query: "<topic>", tags: ["research"] })
```

Search Notion knowledge base:
```javascript
notion_search({ query: "<topic>" })
```

Note any relevant prior findings that provide context.

### Step 1.2: Broad Web Research

Conduct 2-3 web searches from different angles:

1. **Overview search:** `"<topic> overview guide"`
2. **Deep dive search:** `"<topic> best practices considerations"`
3. **Comparison search:** `"<topic> vs alternatives comparison"` (if applicable)

```javascript
google_ai_search_plus({ query: "<search query>" })
```

### Step 1.3: Identify Subtopics

Analyze all gathered information to extract:
- **5-8 key subtopics** that deserve deeper investigation
- **Key questions** that need answering
- **Potential controversies** or areas of disagreement
- **Knowledge gaps** - areas with limited information

For each subtopic, note:
- Why it's important to the overall topic
- What specific questions it should answer
- Initial source quality (official docs vs blogs)

### Step 1.4: Flag Uncertain Claims

During discovery, explicitly flag:
- Claims from single sources only
- Contradictions between sources
- Outdated information (note source dates)
- Marketing claims vs technical facts

---

## Phase 2: Planning

**Goal:** Create project structure and get user approval before deep research.

### Step 2.1: Detect/Create Project

Check for existing related projects:
```bash
ls research/
```

If topic fits existing project, suggest adding to it. Otherwise, propose a new project name (lowercase, hyphenated).

### Step 2.2: Create Folder Structure

```bash
mkdir -p research/<project-name>
```

### Step 2.3: Create Exploration Plan Document

Create `research/<project>/YYYY-MM-DD-exploration-plan.md`:

```markdown
---
topic: "<Topic> - Exploration Plan"
date: YYYY-MM-DD
project: <project-name>
sources_count: <number from discovery>
status: planning
tags: [exploration, <topic-tags>]
---

# <Topic> - Exploration Plan

## Discovery Summary

<2-3 paragraph summary of what was learned in broad discovery>

### Prior Knowledge Found
- Memory: <summary of relevant memory entries>
- Notion: <summary of relevant Notion pages>

### Initial Sources Consulted

| Source | Type | Key Insight |
|--------|------|-------------|
| [Source](url) | Official/Blog/etc | What we learned |

## Proposed Subtopics

### 1. <Subtopic Name>
**Why:** <Why this subtopic matters>
**Questions to answer:**
- Question 1
- Question 2

### 2. <Subtopic Name>
**Why:** <Why this subtopic matters>
**Questions to answer:**
- Question 1
- Question 2

[Continue for all 5-8 subtopics]

## Flagged Uncertainties

- [ ] <Claim> - Only found in single source
- [ ] <Topic> - Sources disagree on this
- [ ] <Info> - From 2021, may be outdated

## Recommended Research Order

1. <Subtopic> - Foundation for understanding others
2. <Subtopic> - High priority for user's likely goals
3. ...

## Next Steps

Awaiting user approval to proceed with subtopic research.
```

### Step 2.4: Present to User for Approval

Show the user:
1. Summary of discovery findings
2. List of proposed subtopics with rationale
3. Any flagged uncertainties
4. Ask for approval/modifications

**User can:**
- Approve all subtopics → Proceed to Phase 3
- Remove subtopics they don't need
- Add subtopics they want explored
- Reorder priority
- Ask for more discovery on specific areas

**Wait for explicit approval before proceeding to Phase 3.**

---

## Phase 3: Parallel Research

**Goal:** Research each approved subtopic using parallel Task agents.

### Step 3.1: Spawn Research Agents

For each approved subtopic, spawn a Task agent:

```javascript
task({
  description: "Research <subtopic>",
  subagent_type: "general",
  prompt: `Research the subtopic "<subtopic>" in the context of "<parent topic>".

Context from discovery:
<relevant context and questions from exploration plan>

Use the /research skill workflow. Create the output document at:
research/<project>/YYYY-MM-DD-<subtopic-slug>.md

Focus on:
- Primary sources and official documentation first
- Cross-reference claims across multiple sources
- Flag uncertain or conflicting information with [UNCERTAIN] or [CONFLICTING]
- Note the date of sources - flag anything older than 2 years as potentially outdated
- Answer the specific questions identified in the exploration plan

Return a JSON summary:
{
  "subtopic": "<name>",
  "file_created": "<path>",
  "sources_count": <number>,
  "key_findings": ["finding 1", "finding 2", "finding 3"],
  "uncertainties": ["any flagged items"],
  "gaps": ["areas needing more research"]
}`
})
```

**Spawn all agents in parallel** (single message with multiple Task tool calls).

### Step 3.2: Track Progress

As agents complete, report to user:
- Which subtopics are complete
- Key findings from each
- Any issues encountered

### Step 3.3: Handle Completion

When all subtopic research completes:
1. Summarize what was researched
2. List all created documents
3. Inform user they can:
   - Request synthesis (Phase 4)
   - Add more subtopics for research
   - Review individual documents first

**Do NOT automatically proceed to synthesis.** Wait for user to request it.

---

## Phase 4: Synthesis (User-Triggered)

**Goal:** Create comprehensive overview and source validation when user requests.

**Trigger phrases:** "synthesize", "finish exploration", "create overview", "summarize findings"

### Step 4.1: Read All Research Documents

Read all subtopic documents in the project folder:
```bash
ls research/<project>/
```

For each document, extract:
- Key findings
- Sources used
- Uncertainties flagged
- Gaps identified

### Step 4.2: Cross-Reference Findings

Analyze across all subtopics:
- **Agreements:** Findings confirmed by multiple subtopics/sources
- **Contradictions:** Where sources or subtopics disagree
- **Patterns:** Recurring themes across subtopics
- **Gaps:** Areas not adequately covered

### Step 4.3: Update Project Index

Update `research/<project>/_index.md`:

```markdown
# <Project Name>

## Executive Summary

<3-5 paragraph comprehensive summary synthesizing all research>

## Key Insights

1. **<Insight 1>** - <explanation> [High confidence - multiple sources]
2. **<Insight 2>** - <explanation> [Medium confidence - limited sources]
3. **<Insight 3>** - <explanation> [Needs verification - sources conflict]

## Research Documents

| Date | Topic | Status | Key Contribution |
|------|-------|--------|------------------|
| YYYY-MM-DD | [Exploration Plan](./file.md) | complete | Initial discovery |
| YYYY-MM-DD | [Subtopic 1](./file.md) | complete | <what it covers> |
| YYYY-MM-DD | [Subtopic 2](./file.md) | complete | <what it covers> |
| YYYY-MM-DD | [Source Review](./file.md) | complete | Validation summary |

## Cross-Topic Findings

### Confirmed Findings
<Findings that appear across multiple subtopics with strong source support>

### Areas of Disagreement
<Where different sources or subtopics present conflicting information>

### Emerging Patterns
<Themes that emerged across the research>

## Open Questions

- [ ] <Question not fully answered>
- [ ] <Area needing future research>
- [ ] <Contradiction needing resolution>

## Recommendations

Based on this research:
1. <Actionable recommendation>
2. <Actionable recommendation>
3. <Actionable recommendation>
```

### Step 4.4: Create Source Review Document

Create `research/<project>/YYYY-MM-DD-source-review.md`:

```markdown
---
topic: Source Review - <Project>
date: YYYY-MM-DD
project: <project-name>
status: final
tags: [source-review, validation]
---

# Source Review: <Project>

## Overview

Total sources consulted: <number>
- Official documentation: <count>
- Peer-reviewed/academic: <count>
- Reputable publications: <count>
- Blog/community content: <count>
- Other: <count>

## Source Quality Ranking

| Rank | Source | Type | Reliability | Used In | Key Contribution |
|------|--------|------|-------------|---------|------------------|
| 1 | [Source](url) | Official docs | High | Subtopic 1, 3 | Primary reference |
| 2 | [Source](url) | Tech blog | Medium | Subtopic 2 | Practical examples |
| ... | ... | ... | ... | ... | ... |

### Reliability Criteria

| Rating | Meaning | Examples |
|--------|---------|----------|
| **High** | Official, peer-reviewed, or established authority | Official docs, RFC, academic papers |
| **Medium** | Reputable publication or known expert | Major tech blogs, conference talks |
| **Low** | Community content, unverified | Personal blogs, forum posts |
| **Uncertain** | Cannot verify authority | Anonymous, no credentials shown |

## Cross-Source Validation

### Well-Supported Findings

| Finding | Supported By | Confidence |
|---------|--------------|------------|
| <Finding 1> | Source A, B, C | High |
| <Finding 2> | Source D, E | High |

### Conflicting Information

| Topic | Claim A | Source | Claim B | Source | Assessment |
|-------|---------|--------|---------|--------|------------|
| <Topic> | <Claim> | [Src](url) | <Claim> | [Src](url) | <Which is likely correct and why> |

### Single-Source Claims

These findings come from only one source and should be verified:

| Claim | Source | Risk Level |
|-------|--------|------------|
| <Claim> | [Source](url) | Medium - reputable source |
| <Claim> | [Source](url) | High - unverified blog |

## Research Gaps

Areas where adequate information could not be found:

- [ ] **<Gap 1>** - <Why this matters, suggested next steps>
- [ ] **<Gap 2>** - <Why this matters, suggested next steps>

## Temporal Relevance

| Source | Published | Topic Area | Still Relevant? | Notes |
|--------|-----------|------------|-----------------|-------|
| [Source](url) | 2024 | <area> | Yes | Current best practices |
| [Source](url) | 2022 | <area> | Partially | Core concepts valid, details may have changed |
| [Source](url) | 2020 | <area> | Uncertain | Technology has evolved significantly |

### Outdated Information Warnings

- <Topic from 2021 source> - Recommend verifying with current documentation
- <Specific claim> - Based on older version, may not apply to current

## Methodology Notes

- Discovery phase: <N> broad searches conducted
- Subtopic research: <N> parallel research tasks
- Total unique sources: <N>
- Date range of sources: <oldest> to <newest>
```

### Step 4.5: Store Key Findings in Memory

Store synthesis results for future reference:

```javascript
memory({
  mode: "add",
  content: "Deep research on <topic>: <3-5 sentence summary of key findings, confidence levels, and any major gaps or uncertainties>",
  tags: ["research", "deep-research", "<project-name>"]
})
```

### Step 4.6: Report to User

Provide final summary:
1. Executive summary of findings
2. Confidence assessment (what's well-supported vs uncertain)
3. List of all created documents with paths
4. Key recommendations
5. Suggested next steps or follow-up research

---

## Error Handling

### Discovery Phase Failures

If web search fails:
- Try alternative search terms
- Check if Notion has relevant content
- Inform user and suggest narrowing topic

If no subtopics identified:
- Topic may be too narrow - suggest broadening
- Topic may be too new - note limited information available
- Offer to proceed with what was found

### Research Phase Failures

If a Task agent fails:
- Report which subtopic failed
- Offer to retry or skip
- Continue with other subtopics

If all agents fail:
- Check connectivity/API issues
- Offer manual research fallback

### Synthesis Phase Issues

If documents are missing:
- List what's available vs expected
- Offer partial synthesis
- Note gaps in overview

---

## Tool Reference

| Tool | Phase | Purpose |
|------|-------|---------|
| `memory({ mode: "search" })` | 1 | Check prior research |
| `notion_search()` | 1 | Search knowledge base |
| `google_ai_search_plus()` | 1, 3 | Web research |
| `task()` | 3 | Spawn parallel research agents |
| `memory({ mode: "add" })` | 4 | Store synthesis findings |

---

## Example Invocation

**User:** `/deep-research kubernetes deployment strategies`

**Agent Response (Phase 1-2):**

> I'll explore "kubernetes deployment strategies" broadly to identify key subtopics.
>
> **Discovery Summary:**
> Found prior research on Kubernetes in memory. Notion has 2 related pages. Web search identified these key areas...
>
> **Proposed Subtopics:**
> 1. Rolling Updates - Default strategy, zero-downtime basics
> 2. Blue-Green Deployments - Full environment switching
> 3. Canary Releases - Gradual rollout with monitoring
> 4. A/B Testing - Traffic splitting for experiments
> 5. GitOps Workflows - ArgoCD, Flux patterns
> 6. Rollback Strategies - Recovery from failed deployments
>
> **Flagged Uncertainties:**
> - Sources disagree on Blue-Green vs Canary for microservices
> - Limited recent info on GitOps with newer K8s versions
>
> Should I proceed with researching these subtopics? You can add, remove, or reorder them.

**User:** "Yes, proceed" or "Remove A/B testing, add service mesh deployments"

**Agent (Phase 3):** Spawns parallel agents, reports progress

**User:** "Synthesize the findings"

**Agent (Phase 4):** Creates overview and source review documents
