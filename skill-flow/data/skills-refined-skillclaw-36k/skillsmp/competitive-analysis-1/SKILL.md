---
name: competitive-analysis
description: Use when you need to research competitors and produce a structured comparison of features, positioning, or market landscape.
---

# Competitive Analysis

## Overview

A structured protocol for researching competitors that requires source attribution, separates observations from inferences, and produces actionable comparison matrices.

## When to Use

- User asks about competitors or "the market"
- User needs to understand competitive positioning
- User wants a feature comparison matrix
- User is preparing for strategy discussions or investor meetings

## Core Pattern

**Step 1: Gather Context**

Follow protocol in `.claude/rules/pm-core/context-gathering.md`:

1. **Detect available inputs** in outputs/ and inputs/:
   - `outputs/truth_base/truth-base.md` - Our product baseline
   - `outputs/roadmap/*.md` - Current strategic direction
   - `inputs/context/compass.md` - Mission and goals
   - Any existing competitive analyses in `outputs/insights/`

2. **Present options to user** via AskUserQuestion:
   - List each relevant file found with brief description
   - Ask: "Which competitors should I analyze?"
   - Ask: "What dimensions to compare?" (features, pricing, positioning, market)
   - Ask: "What's the purpose?" (roadmap, sales, investor deck)
   - Include option: "Point me to another document"
   - Include option: "Describe what you need"

3. **Read `.beads/insights.jsonl`** for relevant learnings from past competitive analyses

4. **Proceed with selected context and user-provided scope**

**If user skips/describes:** Use their description as context, mark claims as Assumption in Claims Ledger.

**Step 2: Research Protocol**

For each competitor, collect:

| Category | What to Find | Source Type |
|----------|--------------|-------------|
| Product | Features, capabilities | Website, docs, demos |
| Pricing | Plans, tiers, pricing model | Pricing page |
| Positioning | Tagline, value prop, target market | Homepage, about page |
| Traction | Funding, customers, reviews | News, G2/Capterra, Crunchbase |

**Rules:**
- Only use publicly available information
- Cite source URL for every claim
- Mark anything uncertain as "Unverified"
- Do NOT guess or infer pricing/features

**Step 3: Feature Comparison Matrix**

| Feature | Our Product | Competitor A | Competitor B |
|---------|-------------|--------------|--------------|
| [Feature 1] | ✓ | ✓ | ✗ |
| [Feature 2] | ✗ | ✓ | ✓ |

**Legend:** ✓ = Has feature, ✗ = Missing, ~ = Partial, ? = Unknown

**Step 4: Positioning Map**

```
           Enterprise
               │
    [Comp A]   │  [Comp B]
               │
  ─────────────┼─────────────
               │
    [Us]       │  [Comp C]
               │
             SMB
     Simple       Complex
```

**Step 5: Strategic Reasoning (Meta-Prompt)**

Before generating the main analysis, create a "Strategic Reasoning" section following `.claude/rules/pm-core/meta-prompt-reasoning.md`:

- **Problem & Goals:** What strategic question is this analysis answering? (e.g., "Should we position as enterprise vs SMB?")
- **Context & Constraints:** What evidence was available? What couldn't be verified?
- **Options Evaluated:** What positioning strategies or competitive responses were considered?
- **Selection Rationale:** If making positioning recommendations, why this approach beats alternatives

This is especially important when competitive analysis leads to positioning decisions.

**Step 6: Generate Output**

Write to `outputs/insights/competitive-analysis-YYYY-MM-DD.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: competitive-analysis
sources:
  - [URLs researched]
downstream:
  - outputs/roadmap/Qx-YYYY-charters.md
---

# Competitive Analysis: [Market/Category]

## Strategic Reasoning

### Problem & Goals
**Problem:** [What strategic question does this analysis answer?]
**Success Criteria:** [What makes this analysis useful for decisions?]

### Context & Constraints
**Available Evidence:**
- [What sources were accessible]
- [What was verifiable vs uncertain]

**Constraints:**
- [Limitations: only public info, couldn't verify X]

### Positioning Options Evaluated (if applicable)

| Option | Strengths | Weaknesses | Evidence |
|--------|-----------|------------|----------|
| [Strategy A] | [Pros] | [Cons] | [Competitive gaps found] |
| [Strategy B] | [Pros] | [Cons] | [Competitive threats] |

### Selection Rationale (if making recommendations)
**Recommended:** [Positioning/strategy recommendation if applicable]

**Why this beats alternatives:**
- [Reason 1 with competitive evidence]
- [Reason 2 with competitive evidence]

**What would change this:**
- [Market/competitive condition that would shift positioning]

---

## Executive Summary
[2-3 sentences on competitive landscape]

## Competitors Analyzed
| Competitor | Website | Positioning |
|------------|---------|-------------|
| [Name] | [URL] | [One-line positioning] |

## Feature Comparison
| Feature | Us | Comp A | Comp B | Source |
|---------|-----|--------|--------|--------|
| [Feature 1] | ✓ | ✓ | ✗ | [URLs] |

**Legend:** ✓ = Has, ✗ = Missing, ~ = Partial, ? = Unknown

## Pricing Comparison
| Competitor | Model | Entry Price | Enterprise | Source |
|------------|-------|-------------|------------|--------|
| [Name] | [SaaS/Usage] | [$X/mo] | [Contact] | [URL] |

## Positioning Map
[ASCII diagram or description]

## Opportunities
- **[Gap we can exploit]** — Evidence: [source]

## Threats
- **[Competitor strength]** — Evidence: [source]

## Recommendations
[Only if supported by evidence]

## Research Date
[YYYY-MM-DD] — Note: Competitive info changes; re-run periodically

## Sources
| Competitor | URLs Researched |
|------------|-----------------|
| [Name] | [URL1], [URL2] |

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [Has feature X] | Evidence | [URL] |
| [Pricing is $Y] | Evidence | [Pricing page URL] |
| [Targets enterprise] | Evidence/Inference | [About page or inference] |
```

**Step 7: Copy to History & Update Tracker**

- Run `pm-os mirror --quiet` to copy to `history/competitive-analysis/competitive-analysis-YYYY-MM-DD.md`
- Update `nexa/state.json` and append to `outputs/audit/auto-run-log.md`

**Step 8: Post-Skill Reflection (MANDATORY)**

Follow protocol in `.claude/rules/pm-core/post-skill-reflection.md`:

1. **Extract key learnings** (3-5 insights):
   - What competitive gaps were most surprising?
   - What positioning options were evaluated?
   - What evidence was hardest to verify?
   - How did meta-prompt reasoning clarify positioning choices?
   - Connections to past competitive analyses?

2. **Create learning entry:**
   - Write to `history/learnings/YYYY-MM-DD-competitive-analysis.md`
   - Use template from post-skill-reflection rule

3. **Create insight beads:**
   - For each significant, reusable insight
   - Append to `.beads/insights.jsonl`
   - Types: insight (competitive learning), pattern (market trends), question (needs validation)

4. **Request output rating:**
   ```
   Rate this competitive analysis (1-5, or 'skip'):
   1 - Needs major revision
   2 - Below expectations
   3 - Meets expectations
   4 - Exceeds expectations
   5 - Outstanding, exactly what I needed
   ```
   - If rated: Create output-rating bead
   - Capture any qualitative feedback

5. **Detect decisions:**
   - If positioning recommendations made = medium confidence decision
   - Ask: "This analysis includes positioning recommendations. Log as decision? [Yes/No]"
   - If yes: Write to `outputs/decisions/YYYY-MM-DD-competitive-positioning.md`

6. **Report completion:**
   ```
   ✅ Competitive analysis complete → outputs/insights/competitive-analysis-YYYY-MM-DD.md
      Mirrored to history/competitive-analysis/competitive-analysis-YYYY-MM-DD.md

   📝 Captured learnings: [N] insights, [N] beads → history/learnings/YYYY-MM-DD-competitive-analysis.md

   Rate this competitive analysis (1-5, or 'skip'): [prompt for rating]
   ```

## Quick Reference

| Output | Location |
|--------|----------|
| Feature matrix | outputs/insights/ |
| Full analysis | outputs/insights/ |
| History | history/competitive-analysis/ |

## Common Mistakes

- **Guessing features:** "They probably have X" → Only claim what's documented
- **Missing sources:** Making claims without URLs → Every claim needs a source
- **Stale data:** Using 2-year-old info → Note date of source, flag if old
- **Inferring strategy:** "They're clearly targeting enterprise" → Only state what's explicit
- **Competitive FUD:** "They're bad at X" → Stick to factual comparisons
- **No research date:** Analysis without timestamp → Always include when researched

## Verification Checklist

- [ ] All competitors have source URLs
- [ ] Feature claims cite specific pages
- [ ] Pricing info from official pricing page (or marked Unknown)
- [ ] Analysis saved to outputs/insights/
- [ ] Date of research noted prominently
- [ ] Unverified claims marked as such
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Has feature X] | Evidence | [URL to docs/page] |
| [Pricing is $Y] | Evidence | [Pricing page URL] |
| [Targets enterprise] | Evidence/Inference | [About page or "Inferred from..."] |
