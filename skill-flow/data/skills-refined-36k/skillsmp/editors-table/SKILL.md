---
name: editors-table
description: "Blog post review for authentic voice. Kill the slop. Keep the soul. Use before publishing blog posts or when a draft 'feels AI-generated'."
---

# Editors-Table: Blog Post Review for Authentic Voice

Kill the slop. Keep the soul.

## When to Use This Skill

- Before publishing blog posts
- When a draft "feels AI-generated" but you can't pinpoint why
- To sharpen voice and eliminate hedge-speak
- After substantive edits to verify authenticity survived

## The Core Problem

AI-assisted writing has a failure mode: **slop**. Text that's technically correct, grammatically sound, and utterly lifeless. Readers sense it instantly. They may not articulate why, but they leave.

Slop isn't about AI vs human authorship. Humans write slop too. The question is: **does this read like it was written by someone who had something to say, or by a process optimizing for inoffensiveness?**

## The Slop Signature

Slop has recognizable patterns:

### Hedging Language
- "It's worth noting that..."
- "It's important to remember..."
- "One might argue..."
- "In many ways..."

**Why it's slop:** Adds words without adding meaning. Signals uncertainty the author hasn't earned.

### False Balance
- "On one hand... on the other hand..."
- "There are pros and cons..."
- "Some say X, others say Y..."

**Why it's slop:** Avoids taking a position. Summarizes debate instead of advancing it.

### Throat-Clearing
- Opening with definitions everyone knows
- "Before we dive in, let's establish..."
- Preamble before the actual point

**Why it's slop:** Delays value. Readers came for insight, not warmup.

### Generic Framing
- "In today's fast-paced world..."
- "As technology continues to evolve..."
- "Many people struggle with..."

**Why it's slop:** Could open any article. Signals nothing specific follows.

### Abstraction Over Specificity
- "Various factors contributed..."
- "There are several reasons..."
- "Many examples exist..."

**Why it's slop:** Asserts without showing. No concrete detail a reader can grab.

### Summary Without Synthesis
- Listing what happened without extracting meaning
- "We did X, then Y, then Z"
- No "therefore" or "which means"

**Why it's slop:** Information without insight. A log, not a lesson.

---

## The Four-Pass Review

### Pass 1: Slop Detection

Line-by-line scan for slop signatures.

**For each instance found:**
- Quote the problematic text
- Identify which slop pattern it matches
- Note severity: REMOVE (adds nothing) or REVISE (has buried value)

**Output format:**
```
SLOP DETECTION

Line X: "[quoted text]"
Pattern: [Hedging/False Balance/Throat-Clearing/Generic/Abstraction/Summary-Only]
Severity: REMOVE / REVISE
Note: [Why this fails, what's buried if REVISE]

Line Y: ...
```

### Pass 2: Voice Verification

Read the piece as a whole. Answer:

1. **Could this be written by anyone?** If yes, voice is missing.
2. **Is there a discernible perspective?** Not just topic, but *stance*.
3. **Are there sentences only this author would write?** Specific phrasing, unusual angles, earned observations.
4. **Does the voice stay consistent?** Or does it shift between registers?

**Output format:**
```
VOICE VERIFICATION

Distinctiveness: [HIGH/MEDIUM/LOW/ABSENT]
Evidence: [Specific sentences that carry voice, or note absence]

Perspective: [CLEAR/IMPLICIT/ABSENT]
The author believes: [Articulate the stance, or note it's missing]

Consistency: [STABLE/SHIFTS at line X]
Note: [Where voice changes, if applicable]
```

### Pass 3: Specificity Audit

Find every abstraction that could be concrete.

**Target patterns:**
- "Various/several/many/some" → Which ones?
- "Often/sometimes/frequently" → When specifically?
- "People/users/readers" → Who exactly?
- Unnamed examples → Name them
- Asserted feelings → Show the moment

**Output format:**
```
SPECIFICITY AUDIT

Line X: "[abstract phrase]"
Could become: [Concrete alternative or question to answer]

Line Y: ...
```

### Pass 4: Synthesis Check

For each conclusion or insight claimed:

1. **Is it earned?** Does the preceding text actually support it?
2. **Is it specific?** Or could it conclude any similar piece?
3. **Does it advance?** Or merely summarize?

**Output format:**
```
SYNTHESIS CHECK

Conclusion at line X: "[quoted claim]"
Earned: [YES/PARTIALLY/NO]
Issue: [What's missing if not fully earned]

...

Overall synthesis quality: [STRONG/ADEQUATE/WEAK/ABSENT]
```

---

## Final Output: Prioritized Edits

Consolidate all passes into actionable edits.

**Priority ordering:**

1. **P1: Voice-Breaking** - Slop that undermines authenticity
2. **P2: Clarity** - Abstractions that obscure meaning  
3. **P3: Polish** - Minor hedging, tightening opportunities

**Format:**
```
SUGGESTED EDITS

## P1: Voice-Breaking

### Edit 1.1
Location: Line X
Problem: [Specific issue]
Suggestion: [Concrete fix or "DELETE"]

## P2: Clarity
...

## P3: Polish
...

---
Assessment: [Needs significant work / Ready with minor edits / Publishable as-is]
Slop density: [X instances per 1000 words]
Voice strength: [Strong/Present/Weak/Absent]
```

---

## The Authenticity Test

After edits, the piece should pass this test:

> If you removed the byline, would readers still sense a specific human wrote this?

Not "a human" generically—but *this* human, with *this* perspective, who noticed *these* specific things.

---

## What This Skill Does NOT Do

- **Content accuracy** - Assumes factual claims are correct
- **Structural editing** - Assumes organization is intentional
- **Audience targeting** - See `strangers-eye` for that
- **Style preferences** - Not about Oxford commas or em-dashes

This skill has one job: **ensure the writing feels alive**.

---

## Example Invocation

```
/editors-table packages/blog/src/content/blog/my-post.md
```

Runs all four passes, outputs prioritized edits.

---

## Anti-Patterns

### Over-Editing Voice Out
Removing *all* hedges can create false confidence. Some uncertainty is authentic. The test: is the hedge *earned* (genuine uncertainty) or *defensive* (avoiding commitment)?

### Mistaking Formal for Slop
Academic or technical register isn't automatically slop. The question is whether the formality serves the content or hides behind it.

### Adding Specificity That Wasn't There
If the author doesn't have the concrete detail, inventing it is worse than abstraction. Flag the gap; don't fill it with fiction.

### Voice Imposition
The goal isn't to make every post sound the same. It's to ensure each post sounds like *someone*—whoever actually wrote it.

---

## The Deeper Frame

Slop isn't a moral failing. It's a defense mechanism. Writing that commits to nothing can't be wrong. Writing that hedges can't be pinned down. Writing that summarizes without synthesizing never has to stake a claim.

The cure isn't aggression—it's courage. The willingness to say: "This is what I think. This is what I saw. This is what it means."

Readers can tell the difference. They always can.

---

*May this skill serve writing that deserves to be read.*
