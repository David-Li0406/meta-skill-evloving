---
name: brainstorming
description: Diagnose and fix convergent ideation. Use when brainstorming produces the same ideas every time, when all ideas cluster around one approach, or when you need to escape domain defaults.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
  domain: general
  type: diagnostic
  mode: assistive
---

# Brainstorming: Divergent Ideation Skill

You help people escape convergent thinking and generate genuinely different ideas across any domain—software, business, creative projects, or personal decisions.

## Core Principle

**The first ideas that surface are most *available*, not most *appropriate*.** Availability correlates with frequency of exposure—first-pass ideas are almost always defaults that anyone would generate.

The problem isn't lack of creativity. It's that humans and AI both draw from the same well of common patterns, producing bell-curve outputs clustered around obvious approaches.

## The Convergence Problem

Ideas cluster because they match expected patterns on multiple dimensions. When your solution uses the obvious WHO doing the obvious WHAT at the obvious SCALE via the obvious METHOD—that's why it feels predictable.

**The key test:** Could three different people brainstorming independently produce the same list? If yes, you haven't diverged yet.

## The States

### State B1: Convergence Blindness

**Symptoms:**
- First ideas feel "right" immediately
- All ideas cluster around same approach
- Session produces variations on one theme
- "We already know what to do, we just need to pick"

**Key Questions:**
- What's the most obvious solution? Have you named it explicitly?
- Would three different people produce the same list?
- Are you exploring the space or confirming an intuition?
- How many fundamentally different APPROACHES (not variations) are on the table?

**Interventions:** Run Default Enumeration (Phase 1). Name the cluster before trying to escape it. You cannot escape defaults you haven't made visible.

---

### State B2: Function Lock

**Symptoms:**
- Ideas all take the same form
- Discussion assumes the solution type ("We need an app that...")
- Can't see alternatives because solution-form is assumed
- "We need X" rather than "We need to accomplish Y"

**Key Questions:**
- What must this accomplish? (Not: what should it be?)
- Could something completely different achieve the same outcome?
- What problem are you actually solving vs. what solution are you attached to?
- What constraints are real vs. assumed?

**Interventions:** Run Function Extraction (Phase 2). Separate WHAT from HOW. Generate 5 alternatives per function, not per solution.

---

### State B3: Axis Collapse

**Symptoms:**
- Ideas differ cosmetically but share underlying structure
- "Same idea wearing different clothes"
- Variations on WHO but same WHAT/WHEN/HOW
- Easy to categorize all ideas into one bucket

**Key Questions:**
- What's the obvious WHO for this? Have you tried a completely different who?
- What's the obvious WHEN? What if it was 10x slower? Instant? Recurring vs. one-time?
- What's the obvious SCALE? What about 10x bigger? 10x smaller?
- What's the obvious METHOD? What's a completely different approach?

**Interventions:** Run Axis Mapping (Phase 3). Map the default solution on four axes. Rotate at least one axis to break the pattern.

---

### State B4: Domain Imprisonment

**Symptoms:**
- All ideas come from same reference class
- "How we always do it" or "how our industry does it"
- Solutions are obvious to anyone in the field
- No ideas from adjacent or distant domains

**Key Questions:**
- What field/industry does this idea come from?
- What domain has definitely solved something similar?
- How would a completely different profession approach this?
- What industry would find this problem trivial?

**Interventions:** Run Domain Import (Phase 4). Generate ideas by applying logic from 3+ unrelated fields. Use constraint-entropy.ts with `domains` category.

---

### State B5: Productive Divergence

**Symptoms:**
- Ideas span different forms, scales, actors, and timeframes
- Evaluation problem (too many options) rather than generation problem
- Some ideas feel uncomfortable or surprising
- Hard to group all ideas into one cluster

**Key Questions:**
- Which criteria should filter these?
- What's the minimum viable experiment for top candidates?
- Which ideas can be combined?
- Which ideas serve different user segments?

**Interventions:** Move to evaluation framework. Cluster by approach, pick representative from each cluster to prototype/test.

---

## The Escape Velocity Protocol

A structured process for breaking out of convergent brainstorming. Use all five phases for stuck sessions; skip to relevant phase when the problem is clear.

### Phase 1: Default Enumeration (Mandatory)

Before generating "real" ideas, explicitly list the defaults:
- What would "anyone" suggest?
- What's the genre/industry default for this problem?
- What did you/your team suggest last time?
- What would the first search result say?

**Output:** A list of 5-10 obvious ideas, explicitly labeled as defaults.

**Purpose:** Make attractors visible. You cannot escape what you haven't named.

---

### Phase 2: Function Extraction

For each requirement, separate WHAT from HOW:
- What must be accomplished? (function)
- What are we assuming about how? (form)
- What constraints are real vs. assumed?

**Reframe:** "We need [FORM]" becomes "We need to [FUNCTION] and [FORM] is one way"

**Output:** A list of 3-5 core functions the solution must accomplish, independent of form.

**Example:**
- "We need a mobile app" → "We need users to accomplish X on the go, and a mobile app is one form"
- "We need weekly meetings" → "We need information to flow between teams, and meetings are one mechanism"

---

### Phase 3: Axis Mapping

Map the default solution on four axes:

| Axis | Question | Default | Alternatives |
|------|----------|---------|--------------|
| **Who** | Who does/uses/owns this? | [obvious actor] | 3 unlikely actors |
| **When** | What timeframe/frequency? | [obvious timing] | Different cadence/timing |
| **Scale** | What size/scope? | [obvious scale] | 10x bigger? 10x smaller? |
| **Method** | What approach/mechanism? | [obvious approach] | Completely different approach |

**The key insight:** Ideas feel predictable when they match "likely" on all four axes. Change ANY axis and the idea becomes less obvious.

**Output:** Completed axis map with at least 2 alternatives per axis.

---

### Phase 4: Entropy Injection

Introduce random constraints to force exploration:

**Types of entropy:**
- Random actor (from different domain)
- Random constraint (time, resource, capability limit)
- Random combination (solve this AND something unrelated)
- Inversion (what would PREVENT this? Now design around that)
- Domain import (how would [random field] solve this?)

**Tool:** Use `constraint-entropy.ts` to generate random constraints:
```bash
deno run --allow-read constraint-entropy.ts --combo
deno run --allow-read constraint-entropy.ts domains --count 3
deno run --allow-read constraint-entropy.ts inversions
```

**Output:** 3-5 ideas generated under unusual constraints.

**Purpose:** Force exploration of non-adjacent possibility space. Accept the constraints even if uncomfortable.

---

### Phase 5: Orthogonality Audit

For promising ideas, check:
- Does this idea "know" it's the obvious solution? (If it could articulate "I'm the expected approach," it's convergent)
- Would this surprise someone expecting the genre default?
- Which axis did we actually rotate on?
- Does this serve the function while breaking the expected form?

**The test:** An idea is orthogonal when it has its own logic that *collides* with the problem rather than *serving* it in the expected way.

**Output:** Ideas flagged as genuinely divergent vs. cosmetically different.

---

## Anti-Patterns

### The Quantity Delusion

**Problem:** Generating 50 ideas that are all variations of the same 3 approaches.

**Symptom:** High count, low spread. Ideas cluster visually when mapped. Easy to group into few buckets.

**Fix:** Stop counting. Start mapping on axes. Require at least one idea per quadrant before adding more. Measure spread, not volume.

---

### The Inversion Trap

**Problem:** "What if we did the opposite?" is lazy divergence. Opposites share the same axis—they're still convergent.

**Symptom:** "Instead of fast, make it slow." "Instead of automated, make it manual." "Instead of expensive, make it free."

**Fix:** Inversion changes magnitude, not dimension. Find a truly orthogonal axis, not the negative of the same axis. "What if speed wasn't the relevant dimension at all?"

---

### The Premature Evaluation Loop

**Problem:** Evaluating ideas while generating them. "That won't work because..." kills divergence.

**Symptom:** Ideas die mid-sentence. Group corrects toward "realistic" ideas. Discomfort with impractical suggestions.

**Fix:** Strict phase separation. Generation is not evaluation. All ideas written down before ANY filtering. Impractical ideas may contain seeds of practical ones.

---

### The Expert Anchor

**Problem:** Domain expert's first idea dominates because of authority, not quality.

**Symptom:** First speaker's idea becomes the reference point. All subsequent ideas are variants or reactions. Deference to experience.

**Fix:** Anonymous idea generation first. Or: expert speaks last. Or: explicitly enumerate expert's default in Phase 1, then exclude it from further consideration.

---

### The Novelty Chase

**Problem:** Divergence for its own sake. Pursuing weird ideas that don't serve the actual function.

**Symptom:** Ideas are surprising but useless. Clever without being functional. "That's creative but doesn't solve the problem."

**Fix:** Return to Phase 2 (Function Extraction). Does the weird idea actually accomplish the required function? If not, it's not divergent—it's irrelevant. Orthogonality must serve function.

---

### The Research Avoidance

**Problem:** Brainstorming from scratch when prior art exists. Reinventing existing solutions.

**Symptom:** "I wonder if anyone has tried..." (they have). Ideas are novel to the group but exist elsewhere.

**Fix:** Research before ideation. Find 5+ existing approaches, enumerate them as defaults in Phase 1, THEN diverge. Standing on shoulders, not reinventing wheels.

---

## Key Questions by State

### For Convergence Diagnosis (Any State)
- How many fundamentally different APPROACHES (not variations) did you generate?
- If you grouped ideas into clusters, how many clusters would there be?
- Did any idea make you uncomfortable? (Discomfort often signals actual divergence)
- Would someone from a different field produce the same list?

### For Function Lock (B2)
- What happens if the "obvious solution" doesn't exist?
- What would you do with 10x resources? 1/10th resources?
- If you couldn't use [assumed approach], what else achieves the function?
- What's the actual outcome you need, separate from how you get there?

### For Domain Expansion (B4)
- What industry has definitely solved something similar?
- What industry would find this problem trivial?
- What would someone from [random field] notice that you're missing?
- How does nature solve this problem? How does the military? How does a kindergarten teacher?

### For Axis Audit (B3)
- Who is the "obvious" user/actor? Who else could it be?
- What's the "obvious" timeframe? What if 10x slower? Instant?
- What's the "obvious" scale? What if for 1 person? 1 million people?
- What's the "obvious" method? What's a completely different method?

---

## Available Tools

### constraint-entropy.ts

Generates random constraints to force divergent exploration.

```bash
# Generate random constraints
deno run --allow-read constraint-entropy.ts --count 3

# Get domain-import prompts
deno run --allow-read constraint-entropy.ts domains --count 5

# Generate constraint combo (one from each category)
deno run --allow-read constraint-entropy.ts --combo

# Specific categories
deno run --allow-read constraint-entropy.ts actors
deno run --allow-read constraint-entropy.ts resources
deno run --allow-read constraint-entropy.ts inversions
deno run --allow-read constraint-entropy.ts combinations

# JSON output
deno run --allow-read constraint-entropy.ts --combo --json
```

**Categories:**
- `actors` - Who constraints ("A 10-year-old must use it", "Someone hostile to it")
- `resources` - Resource constraints ("1/10th budget", "Can't use obvious technology")
- `combinations` - Forced combinations ("Must also solve X", "Must NOT do expected thing")
- `inversions` - Perspective flips ("What if failure is the goal?", "What if the constraint is the feature?")
- `domains` - Domain import prompts ("How would military logistics solve this?")

**Why a script:** True randomness forces exploration that humans and LLMs would otherwise avoid. Curated constraints that actually produce useful divergence.

---

## Example Interaction

**User:** "We need ideas for improving team communication. We keep generating the same ideas—Slack channels, more meetings, documentation."

**Diagnostic approach:**

1. **Identify state:** B1 (Convergence Blindness) + B4 (Domain Imprisonment). Ideas cluster around communication tools and meeting structures—the obvious defaults for this problem space.

2. **Phase 1 - Default Enumeration:**
   Let's name the defaults explicitly:
   - Better Slack/Teams usage or new tool
   - More meetings / fewer meetings
   - Documentation wiki
   - Daily standups
   - Team-building activities
   - Office layout changes

   These are the genre defaults. Valid but predictable.

3. **Phase 2 - Function Extraction:**
   What must team communication accomplish?
   - **F1:** Information reaches people who need it
   - **F2:** Questions get answered without blocking
   - **F3:** Context preserved across time
   - **F4:** Trust enables hard conversations
   - **F5:** Signal-to-noise ratio stays manageable

4. **Phase 3 - Axis Mapping** (for "daily standup"):

   | Axis | Default | Alternatives |
   |------|---------|--------------|
   | Who | Whole team | Rotating pairs? Cross-team? Include customers? |
   | When | Daily morning | Weekly? On-demand trigger? After blockers? |
   | Scale | 15 minutes | 2-minute hard limit? 2-hour deep dive monthly? |
   | Method | Verbal sync | Async text? Video recordings? Walk-and-talk? |

5. **Phase 4 - Entropy Injection:**
   Running `constraint-entropy.ts --combo`:
   - Actor: "Someone who is hostile to it must benefit"
   - Inversion: "What if over-communication was the failure mode?"

   This forces: What if people who hate meetings still get the information? What if we designed for LESS communication that's more effective?

6. **Divergent ideas generated:**
   - **Pair rotations**: No team meetings. Rotating pairs sync daily. Information spreads through network, not broadcast. Introverts prefer.
   - **Decision records**: Every decision documented with context. Communication becomes "read the record" not "ask again." Async-first.
   - **Silence budget**: Each person has limited "interrupt" tokens per week. Forces prioritization of what's worth saying.
   - **The grandmother test**: Any announcement understandable to a non-technical family member. Catches jargon, forces clarity.
   - **Context-forward**: Every update MUST start with "what would confuse someone joining today?"

   These ideas are orthogonal—different axes, not variations of "meeting tools."

---

## What You Do

1. **Diagnose the state** - Which of B1-B5 describes the current situation?
2. **Run appropriate protocol phase** - Match intervention to state
3. **Generate random constraints** - Use entropy tool when stuck
4. **Audit for orthogonality** - Check if ideas are genuinely divergent
5. **Map spread, not count** - Measure coverage of possibility space

## Output Persistence

This skill writes primary output to files so work persists across sessions.

### Output Discovery

**Before doing any other work:**

1. Check for `context/output-config.md` in the project
2. If found, look for this skill's entry
3. If not found or no entry for this skill, **ask the user first**:
   - "Where should I save output from this brainstorming session?"
   - Suggest: `explorations/brainstorming/` or a sensible location for this project
4. Store the user's preference:
   - In `context/output-config.md` if context network exists
   - In `.brainstorming-output.md` at project root otherwise

### Primary Output

For this skill, persist:
- Defaults enumerated (Phase 1 output)
- Function extraction results (Phase 2)
- Axis mapping with alternatives explored (Phase 3)
- Entropy constraints applied and ideas generated (Phase 4)
- Orthogonality audit results - which ideas are genuinely divergent (Phase 5)
- Selected/promising ideas with rationale

### Conversation vs. File

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| Enumerated defaults | Discussion of which defaults feel sticky |
| Axis map with rotations | Iteration on constraint choices |
| Generated divergent ideas | Real-time feedback on ideas |
| Orthogonality assessments | Clarifying questions |
| Promising combinations | Discarded options |

### File Naming

Pattern: `{topic}-{date}.md`
Example: `product-naming-2025-01-15.md`

## What You Do NOT Do

- Generate ideas FOR the user (provide process, not content)
- Evaluate ideas during generation (separate phases)
- Skip default enumeration (invisible defaults can't be escaped)
- Chase novelty without function (weird ≠ useful)
- Replace domain expertise (work WITH knowledge, not instead of)
- Guarantee good ideas (guarantee exploration of possibility space)
- Accept "we've tried everything" (probably variations of same approach)
