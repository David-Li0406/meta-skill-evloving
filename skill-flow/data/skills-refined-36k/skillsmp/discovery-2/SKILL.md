---
name: discovery
description: Structured document analysis, interview preparation, and signal synthesis for new PM onboarding
---

# Discovery

## Overview

Discovery is the **first skill for new PMs** - it helps you make sense of inherited documents, prepare for stakeholder interviews, and synthesize signals into actionable insights. This skill bridges the gap between "I have documents" and "I understand what's happening."

**Why this matters:** PM OS is strong at synthesis and output generation (charters, PRDs), but that requires good inputs. Discovery ensures you gather quality signals *before* running downstream skills.

## When to Use

| Trigger | Mode | Command |
|---------|------|---------|
| Just inherited docs from predecessor | `--analyze-docs` | `/discover --analyze-docs` |
| Preparing for stakeholder interview | `--prep [role]` | `/discover --prep sales` |
| Have interview notes, need to synthesize | `--synthesize` | `/discover --synthesize` |
| Conversational exploration | (default) | "Help me understand these docs" |

## Modes

### Mode 1: Analyze Documents (`--analyze-docs`)

**Purpose:** Extract structured insights from inherited documents.

**Inputs:** Files in `inputs/` or `outputs/ingest/` (extracted text from PDFs, PPTs, etc.)

**Output:** `outputs/discovery/doc-analysis-YYYY-MM-DD.md`

### Mode 2: Interview Prep (`--prep [role]`)

**Purpose:** Generate role-specific interview questions based on what you know and don't know.

**Roles:** `sales`, `support`, `marketing`, `customer`, `engineering`, `leadership`

**Output:** `outputs/discovery/interview-guide-[role].md`

### Mode 3: Synthesize Signals (`--synthesize`)

**Purpose:** Combine all discovery signals into personas, themes, and validated insights.

**Inputs:** Previous discovery outputs, interview notes

**Output:** `outputs/discovery/signals-YYYY-MM-DD.md`

---

## Core Pattern

### Step 1: Gather Context

Before running any mode, understand what exists:

```
1. Check outputs/ingest/ for extracted documents
2. Check inputs/ for raw files
3. Check outputs/discovery/ for previous analyses
4. Note what's available vs. what's missing
```

### Step 2: Execute Mode

#### For `--analyze-docs`:

**Step 2a: Read all available documents**

Read files from `outputs/ingest/` and `inputs/`. For each document, extract:

| Column | What to Extract |
|--------|-----------------|
| **EXPLICIT** | Stated facts, decisions, priorities, metrics |
| **INFERRED** | Patterns, implied priorities, tensions, what's unsaid |
| **QUESTIONS** | What can't be answered from this doc? |
| **VALIDATE** | What needs stakeholder confirmation? |

**Step 2b: Cross-reference documents**

Look for:
- Contradictions between documents (roadmap vs. reality)
- Patterns across documents (same issue mentioned multiple times)
- Gaps (topics never mentioned but expected)
- Stale information (dates, metrics that may have changed)

**Step 2c: Generate output**

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: discovery
mode: analyze-docs
sources:
  - [list all analyzed files]
---

# Document Analysis

## Executive Summary
[3-5 bullet points of the most important findings]

## Document Insights

| Source | EXPLICIT (Stated) | INFERRED (Implied) | QUESTIONS |
|--------|-------------------|--------------------| ----------|
| [file] | [facts, decisions] | [patterns, tensions] | [unknowns] |

## Cross-Document Patterns

| Pattern | Sources | Confidence |
|---------|---------|------------|
| [pattern] | [which docs] | High/Medium/Low |

## Critical Gaps
[What's missing that a PM should know]

## Suggested Next Steps
1. [Interview recommendation based on gaps]
2. [Data to request]
3. [Questions to ask specific stakeholders]

## Claims Ledger

| Claim | Type | Source |
|-------|------|--------|
| [claim] | EXPLICIT/INFERRED/QUESTION | [file:line] |
```

#### For `--prep [role]`:

**Step 2a: Identify knowledge gaps**

Review existing discovery outputs and truth base. Note:
- What do we know well? (from documents)
- What do we need to validate? (INFERRED claims)
- What do we not know at all? (gaps)

**Step 2b: Generate role-specific questions**

Pull from the interview protocol rule (`.claude/rules/pm-workflows/interview-protocol.md`) and customize based on:
- Current knowledge gaps
- Specific topics from document analysis
- Role-specific concerns

**Step 2c: Generate output**

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: discovery
mode: prep
role: [sales|support|marketing|customer|engineering|leadership]
sources:
  - [discovery outputs, truth base]
---

# Interview Guide: [Role]

## Context from Documents
[What we already know relevant to this role]

## Questions

### Evidence Validation (confirm what we think we know)
1. [Question based on INFERRED claim]
2. [Question based on INFERRED claim]

### Gap Filling (learn what we don't know)
1. [Question based on identified gap]
2. [Question based on identified gap]

### Open Discovery (unexpected insights)
1. [Open-ended question for this role]
2. [Open-ended question for this role]

## Signals to Watch For
- [Pattern that would confirm hypothesis X]
- [Pattern that would invalidate hypothesis Y]

## Evidence to Validate

| Hypothesis | Ask About | Expected Signal |
|------------|-----------|-----------------|
| [hypothesis] | [specific question] | [what confirms/denies] |

## Post-Interview Actions
- [ ] Log notes in inputs/voc/
- [ ] Update discovery signals
- [ ] Flag any surprises for follow-up
```

#### For `--synthesize`:

**Step 2a: Gather all signals**

Read:
- `outputs/discovery/doc-analysis-*.md`
- `outputs/discovery/interview-guide-*.md`
- `inputs/voc/*.md` (interview notes)
- Previous signal syntheses

**Step 2b: Classify signals**

For each insight, classify:

| Type | Definition | Evidence Threshold |
|------|------------|-------------------|
| **EXPLICIT** | Directly stated by source | 1 source sufficient |
| **INFERRED** | Pattern across sources | 2+ sources |
| **IMPLICIT** | PM best practice gap | Professional judgment |

**Step 2c: Generate output**

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: discovery
mode: synthesize
sources:
  - [all inputs]
---

# Signal Synthesis

## Executive Summary
[3-5 bullet points of validated insights]

## Validated Signals (High Confidence)

| Signal | Type | Sources | Confidence |
|--------|------|---------|------------|
| [insight] | EXPLICIT | [3+ sources] | High |

## Emerging Patterns (Medium Confidence)

| Pattern | Type | Sources | Needs Validation |
|---------|------|---------|------------------|
| [pattern] | INFERRED | [2 sources] | [what would confirm] |

## Open Questions (Requires More Data)

| Question | Why It Matters | How to Answer |
|----------|---------------|---------------|
| [question] | [impact on decisions] | [who/what to ask] |

## Personas (if sufficient data)

### [Persona Name]
- **Role:** [title]
- **Key Pain:** [primary frustration]
- **Current Workaround:** [how they cope]
- **Ideal State:** [what they wish for]
- **Evidence:** [sources]

## Recommended Next Steps

| Action | Why | Priority |
|--------|-----|----------|
| [action] | [reasoning] | P0/P1/P2 |

## Claims Ledger

| Claim | Type | Source |
|-------|------|--------|
| [claim] | EXPLICIT/INFERRED/IMPLICIT | [source] |
```

### Step 3: Post-Execution

After generating any discovery output:

1. **Mirror to history:** Run `pm-os mirror --quiet`
2. **Update state:** Note discovery progress in `nexa/state.json`
3. **Recommend next:** Suggest next discovery step or downstream skill

---

## Conversational Mode

When invoked conversationally (without explicit mode), Nexa should:

1. **Ask clarifying questions:**
   - "What documents do you have?"
   - "Who are you meeting with?"
   - "What do you already know?"

2. **Suggest appropriate mode:**
   - "Sounds like you need document analysis. Want me to run `/discover --analyze-docs`?"
   - "I can prep you for that sales interview. Should I run `/discover --prep sales`?"

3. **Maintain context across turns:**
   - Remember what's been analyzed
   - Build on previous discovery work
   - Avoid re-reading files already processed

**Example Conversation:**

```
User: I just inherited a bunch of docs from my predecessor

Nexa: I can help you make sense of them. Let me check what's available...

[Reads outputs/ingest/ and inputs/]

I see 5 documents:
- Q3-roadmap.pptx (extracted to ingest/)
- jira-export.csv (in inputs/jira/)
- customer-feedback.pdf (extracted to ingest/)
- competitor-analysis.docx (extracted to ingest/)
- team-retro-notes.md (in inputs/)

Want me to analyze these for patterns, gaps, and questions to investigate?

User: Yes please

Nexa: [Runs --analyze-docs mode]
```

---

## Role-Specific Interview Frameworks

### Sales Interviews
**Goal:** Understand win/loss patterns, competitive landscape, customer objections

### Support Interviews
**Goal:** Understand pain points, workarounds, churn signals

### Marketing Interviews
**Goal:** Understand positioning, market perception, competitive messaging

### Customer Interviews
**Goal:** Understand actual usage, unmet needs, value perception

### Engineering Interviews
**Goal:** Understand technical constraints, debt, feasibility

### Leadership Interviews
**Goal:** Understand strategy, priorities, political landscape

See `.claude/rules/pm-workflows/interview-protocol.md` for detailed question templates.

---

## Signal Classification Framework

| Type | Definition | Example | Threshold |
|------|------------|---------|-----------|
| **EXPLICIT** | Directly stated in source | "Sync is slow" (in Jira ticket) | 1 source |
| **INFERRED** | Pattern across sources | Sales + Support both mention competitor X | 2+ sources |
| **IMPLICIT** | PM best practice gap | No success metrics for past features | Professional judgment |

See `.claude/rules/pm-workflows/signal-classification.md` for detailed rules.

---

## Integration with PM OS

### Feeds Into

| Downstream Skill | How Discovery Helps |
|-----------------|---------------------|
| `building-truth-base` | Provides validated facts to include |
| `synthesizing-voc` | Provides structured interview notes |
| `generating-quarterly-charters` | Provides evidence for strategic bets |

### Algorithm Phase

Discovery is an **OBSERVE** phase skill:
- No prerequisites (entry point for new PMs)
- Outputs feed THINK and PLAN phases
- Should run before other OBSERVE skills for context

---

## Verification Checklist

Before marking discovery output complete:

- [ ] All available documents analyzed
- [ ] EXPLICIT/INFERRED/IMPLICIT properly classified
- [ ] Questions are specific and actionable
- [ ] Sources cited for every claim
- [ ] Claims Ledger complete
- [ ] Next steps are concrete
- [ ] Output mirrored to history/

---

## Quick Reference

| Command | Purpose | Output |
|---------|---------|--------|
| `/discover --analyze-docs` | Analyze inherited documents | `doc-analysis-*.md` |
| `/discover --prep sales` | Prep for sales interview | `interview-guide-sales.md` |
| `/discover --prep support` | Prep for support interview | `interview-guide-support.md` |
| `/discover --prep marketing` | Prep for marketing interview | `interview-guide-marketing.md` |
| `/discover --prep customer` | Prep for customer interview | `interview-guide-customer.md` |
| `/discover --prep engineering` | Prep for engineering interview | `interview-guide-engineering.md` |
| `/discover --prep leadership` | Prep for leadership interview | `interview-guide-leadership.md` |
| `/discover --synthesize` | Combine all signals | `signals-*.md` |

---

## Common Workflows

### New PM Onboarding (Week 1)

```
Day 1-2: /discover --analyze-docs
Day 3: /discover --prep engineering
Day 4: /discover --prep sales
Day 5: /discover --prep support
Week 2: /discover --synthesize
Then: /truth-base (with discovery as input)
```

### Preparing for Quarterly Planning

```
1. /discover --analyze-docs (review last quarter's outputs)
2. /discover --prep leadership (understand priorities)
3. /discover --synthesize
4. /voc (if fresh customer data)
5. /charters
```
