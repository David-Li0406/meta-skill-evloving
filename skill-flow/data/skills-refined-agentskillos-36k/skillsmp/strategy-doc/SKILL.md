---
name: strategy-doc
description: Develops product strategy documents using Cagan + Playing to Win frameworks with human-in-the-loop collaboration
---

# Strategy Doc Writer

Build rigorous product strategy documents through structured research, collaborative development, and critical review.

## When to Use

User wants to:
- Develop a product strategy
- Create a strategic planning document
- Think through a major product decision
- Document vision, positioning, or competitive strategy

## Frameworks

This skill combines three proven frameworks:

**Cagan** (Product Strategy)
- Vision: 2-5 year north star
- Principles: Decision guardrails
- Strategic bets: Sequenced problems to solve

**Playing to Win** (Competitive Strategy)
- Where to Play: Target customers, markets, channels
- How to Win: Competitive advantage, what makes us hard to copy
- Capabilities: What we must build/acquire

**Amazon FAQ**
- Anticipated objections
- "What if we're wrong about X?"

## Final Document Structure

```
1. Vision & Principles (Cagan)
2. Where to Play (P2W)
3. How to Win (P2W)
4. Strategic Bets (Cagan)
5. Capabilities Required (P2W)
6. FAQ (Amazon)
```

## Workflow

CRITICAL: Follow this workflow exactly. Each phase has a human gate. Save artifacts as you go.

### PHASE 0: SETUP

```
□ Create working directory: scratch/strategy-[topic]-[date]/
□ Initialize this checklist in the working directory
```

**Actions:**
1. Ask user: "What strategic question are we tackling?"
2. Create working directory with slugified topic name
3. Save initial checklist to `progress.md`

---

### PHASE 1: FRAME (fast)

```
□ Capture the strategic question in one sentence
□ User confirms we're pointed at the right problem
□ Save: 00-frame.md
```

**Actions:**
1. Restate the strategic question in one clear sentence
2. Ask user to confirm or refine
3. Save frame to working directory

**Human gate:** User confirms framing before proceeding

---

### PHASE 2: GATHER (critical step)

```
□ Fetch relevant Notion context
□ Research competitors and market landscape
□ Pull relevant metrics/data
□ Synthesize into research brief
□ Save: 01-research-brief.md
□ User reviews research, flags gaps or redirects scope
```

**Actions:**
1. Spawn agents IN PARALLEL using Task tool:
   - `notion-researcher`: Find existing strategy docs, past decisions, related context
   - `competitor-researcher`: Market landscape, competitor positioning, trends
   - Use `analyze` skill if user has relevant data questions
2. Synthesize agent outputs into a research brief
3. Save research brief to working directory
4. Present brief to user for review

**Human gate:** User reviews research, flags gaps, may redirect scope

**Agents to spawn:**
- `.claude/agents/notion-researcher.md`
- `.claude/agents/competitor-researcher.md`
- (Phase 6) `.claude/agents/notion-writer.md`

**Notion researcher output format for this skill:**
```markdown
## Existing Context: [Topic]

### Relevant Prior Decisions
- **[Decision]:** [Brief context and date]

### Active Constraints
- **[Constraint]:** [Why it matters]

### Relevant Prior Research
- **[Topic]:** [Key findings, source doc]

### Open Questions from Prior Work
- **[Question]:** [Context]

### Source Documents
| Document | Last Updated | Link |
|----------|--------------|------|
```

---

### PHASE 3: DEVELOP

```
□ Draft Vision statement options
□ Define Principles (decision guardrails)
□ Explore Where to Play options
□ Define How to Win for chosen arena
□ Sequence Strategic Bets
□ Identify Capabilities required
□ Save: 02-strategic-choices.md
□ User approves strategic choices
```

**Actions:**
Work through each element interactively:

1. **Vision**: Propose 2-3 vision statement options. Ask user to pick or refine.
2. **Principles**: Suggest 3-5 decision guardrails based on research. User confirms.
3. **Where to Play**: Present options for target customers/markets/channels. Discuss trade-offs.
4. **How to Win**: For chosen arena, articulate competitive advantage. Pressure-test: "What would have to be true?"
5. **Strategic Bets**: Sequence the problems to solve. Why this order?
6. **Capabilities**: What must we build or acquire to execute?

Save choices to working directory after user approval.

**Human gate:** User approves strategic choices before drafting

---

### PHASE 4: DRAFT

```
□ Write full document with FAQ
□ Save: 03-draft-v1.md
□ User reviews draft
```

**Actions:**
1. Spawn `strategy-writer` agent with:
   - Research brief (01-research-brief.md)
   - Strategic choices (02-strategic-choices.md)
   - Document structure and writing style guidelines
2. Save draft to working directory
3. Present draft to user

**Human gate:** User reviews draft, provides feedback

**Agent to spawn:**
- `.claude/agents/strategy-writer.md`

---

### PHASE 5: REVIEW

```
□ Strategy-reviewer critiques document
□ Save: 04-review-feedback.md
□ User incorporates feedback
□ Save: 03-draft-v2.md (iterate as needed)
```

**Actions:**
1. Spawn `strategy-reviewer` agent to critique the draft
2. Save review feedback to working directory
3. Present feedback to user
4. User decides which feedback to incorporate
5. Revise draft (spawn strategy-writer again if major changes)
6. Save revised draft with incremented version

**Human gate:** User satisfied with draft before publishing

**Agent to spawn:**
- `.claude/agents/strategy-reviewer.md`

---

### PHASE 6: PUBLISH

```
□ Confirm stakeholders and Notion location
□ User approves final
□ Convert to Notion format and publish
□ Save final: final.md
```

**Actions:**
1. Ask user: "Who are the stakeholders for this doc?"
2. Ask user: "Where in Notion should this live?" (get page ID or parent page)
3. Get explicit approval to publish
4. Spawn `notion-writer` agent to:
   - Verify formatting is Notion-compatible
   - Publish to specified Notion location
   - Return page URL
5. Save final version to working directory
6. Confirm publish succeeded with link

**Human gate:** Explicit approval before any Notion write

**Agent to spawn:**
- `.claude/agents/notion-writer.md`

---

## Critical Rules

1. **NEVER skip human gates.** Each phase requires user confirmation before proceeding.
2. **ALWAYS save artifacts.** Every phase produces a file in the working directory.
3. **Spawn agents in parallel** when possible (Phase 2 research agents).
4. **Read the working directory** if resuming a session to understand current state.
5. **Use the checklist** in progress.md to track what's done.

## Resuming a Session

If user returns to continue a strategy doc:
1. Ask which strategy doc they're working on (or check scratch/ for recent directories)
2. Read progress.md to see current phase
3. Read latest artifacts to restore context
4. Continue from where they left off
