---
name: opened-daily-newsletter-writer
description: Creates Monday-Thursday OpenEd Daily newsletters (500-800 words) with Thought-Trend-Tool structure. Use when the user asks to create a daily newsletter, write daily content, or transform source material into newsletter segments. Not for Friday Weekly digests.
---

# OpenEd Daily Newsletter Writer

Creates Monday-Thursday daily newsletters (500-800 words) that challenge standardized education with contrarian angles and authentic voice.

**Not for:** Friday Weekly digests (use `weekly-newsletter-workflow`), social media only, or blog posts.

---

## Workflow Overview

```
Phase 1: Content Curation     → Source_Material.md
Phase 2: Angle Development    → Checkpoint_1.md (USER APPROVAL REQUIRED)
Phase 3: Newsletter Writing   → Newsletter_DRAFT.md
Phase 4: Social Media         → Optional repurposing
Phase 5: QA & Archive         → Newsletter_FINAL.md
```

---

## Phase 1: Content Curation

### Pull Staging Content from Notion

```
notion-search:
  query: "staging Thought Tool Trend"
  query_type: "internal"
  data_source_url: "collection://5d0c1ad8-e111-4162-91da-2cac9bd1269b"
  filters:
    created_date_range:
      start_date: "2025-10-01"
```

For specific items, use `notion-fetch` with the page ID.

### Segment Types

- **THOUGHT:** Contrarian takes, educational philosophy (~100-120 words)
- **TREND:** Current developments, research, data (~100-120 words)
- **TOOL:** Practical resources readers can use immediately (~100-120 words)

**Standard order:** THOUGHT → TREND → TOOL

### Sourcing Rules

**TOOLs:**
- Primary: [Tool Database](../../../Studio/Lead Magnet Project/OpenEd_Tool_Database.md)
- Must have concrete detail (stats, quotes, specific features)

**THOUGHTs:**
- Named individuals + direct quotes work best
- "Happy, not Fortune 500" > generic philosophy

**TRENDs:**
- Vary topics — avoid repeating "enrollment surge" every issue
- Look for: learning science, tech/AI, parent behavior, international comparisons
- Specific numbers + authoritative sources

**Avoid:**
- Heavy ESA/school choice policy content
- Federal tax programs
- State-specific policy details (unless story transcends the state)

### Create Working Folder

```bash
mkdir "Studio/OpenEd Daily/[YYYY-MM-DD] - [Brief Theme]/"
```

Create `Source_Material.md` with URLs, key quotes, and angle notes.

---

## Phase 2: Angle Development

🛑 **CHECKPOINT 1 - Do not proceed to Phase 3 without user approval.**

Create `Checkpoint_1_Angles.md` with:

### Socials-First Check (Before Drafting Angles)

Before developing newsletter angles, check if any segment has an obvious social format:

| Segment Content | Social Format Match | Action |
|-----------------|---------------------|--------|
| Single stat + hot take | X/LinkedIn one-liner | Draft social first, expand for newsletter |
| Visual comparison | Instagram carousel | Design visual, then write supporting copy |
| Story arc | LinkedIn transformation | Draft full story, then compress for newsletter |
| Contrarian take | X paradox hook | Test punchiest version first |

**Why:** Social constraints often produce tighter, more compelling angles. If a segment has a natural social format, draft that version first - it may reveal the strongest angle for the newsletter.

Load `TEMPLATE_INDEX.md` for format matching.

### For Each Segment (3-4 angle options)

Ask yourself:
- What's the contrarian but obviously true take?
- How does this challenge standardized education?
- Would Sarah (our One True Fan) forward this?

### Subject Lines (10 options, 8-10 words max)

- 3-4 Curiosity-Based
- 3-4 Specificity-Based
- 2-3 Hybrid

### Preview Text

Formula: `[Specific claim]. [Context]. [Gap/tension]. PLUS: [bonus]`

Example: "Students who test themselves retain 80% more. Researchers have known this since the 1900s. Schools still don't do it. PLUS: an app that does."

### Checkpoint Template

```markdown
# Checkpoint 1: Angles & Structure - [Date]

## SUBJECT LINE OPTIONS
[Organize by type: Curiosity, Specificity, Hybrid]

## PREVIEW TEXT
[Draft]

## SEGMENT 1: [TITLE] (Type)
**Source:** [URL]
**Angle Options:** [3-4 options]
**Recommended:** [Which and why]

## SEGMENT 2: [TITLE] (Type)
[Same format]

## SEGMENT 3: [TITLE] (Type)
[Same format]

## ORTHOGONALITY CHECK
- [ ] Thought and Trend are distinct (not repetitive)
- [ ] Aligns with OpenEd beliefs
- [ ] Would Sarah forward this?
```

### User Feedback Notation

- `***` = preferred choice
- `<>` = extrapolate contextually
- `{question}` = answer directly
- `~~text~~` = delete

---

## Phase 3: Newsletter Writing

Create `Newsletter_DRAFT.md` after Checkpoint 1 approval.

### Opening Letter (~100-150 words)

**For more examples, load:** `references/opening-letter-patterns.md`

**Structure:**
1. **Greeting:** "Greetings Eddies!", "Welcome Eddies!", or "Greetings!"
2. **Hook:** Story, startling statistic, contrarian question, or community milestone
3. **Pivot:** Connect to "opening up education" or today's specific value
4. **Tease:** Mention what's coming without summarizing
5. **Sign-off:** "Let's dive in."

**Quick Examples (by hook type):**

**Milestone/Community:**
> Greetings Eddies! It just came to my attention that the OpenEd Daily hit a new milestone: 20,000 subscribers! Rather than resting on our laurels, we take this as a sign of the growing appetite for trustworthy content related to the opening up of education. Onward & upward,

**Contrarian/Data:**
> Greetings! An education expert recently published something that's making a lot of parents nervous. Chad Aldeman looked at data from 250,000 kids across 1,400 schools and concluded: if your child isn't reading on track by kindergarten, don't wait. Act fast. The data sounds brutal, but is he interpreting it correctly? Let's dive in.

**Story-Driven:**
> Greetings! Ken Danford had spent six years teaching eighth-grade U.S. history when a colleague handed him The Teenage Liberation Handbook. In it, he found case studies of teens who left school and turned out... fine! That was 1996. He quit his job, and ever since, he's been running North Star—a physical community center where teens can legally homeschool. Let's dive in.

**Personal/Humorous:**
> Greetings Eddies! Did you know that OpenEd is on Instagram? While I may not be able to compete with top-tier influencer homeschool moms, we're always looking for new ways to share the message (even if that means putting on a smelly latex horse mask and A/B testing silly gimmicks until we find something that sticks).

**Parental Anxiety:**
> Greetings! A few months ago, an OpenEd parent reached out with a familiar dilemma. Her student had done 9th grade on the diploma path, but she was switching to non-diploma-seeking status. Yet she still had concerns: "I worry a lot about not following the traditional path." Society has pushed one linear path for so long. Except that path is just one among many. Let's dive in.

### Newsletter Structure

```markdown
**SUBJECT:** [From Checkpoint 1]
**PREVIEW:** [From Checkpoint 1]
---

[Opening Letter]
---

## [SEGMENT 1 TITLE - ALL CAPS]
[100-120 words]
---

## [SEGMENT 2 TITLE - ALL CAPS]
[100-120 words]
---

## [SEGMENT 3 TITLE - ALL CAPS]
[100-120 words]
---

That's all for today!

– Charlie (the OpenEd newsletter guy)

P.S. [Optional announcement]
```

### Format Requirements

- ❌ NO EMOJIS (non-negotiable)
- ✅ ALL CAPS H2 titles for segments
- ✅ **Bold** for key quotes/stats
- ✅ Hyperlinks throughout (not just at ends)
- ✅ `---` between sections
- ✅ 500-800 words total

### Hyperlinking Rules

When provided a link, always hyperlink it **in the body of the text** (never at the end). Link the **main action or subject** using only **2-3 key words max**.

**Good:** "A new [MIT study](URL) claims LLM users underperform..."
**Good:** "Ken Danford has been [running North Star](URL) since 1996..."
**Bad:** "A new MIT study claims LLM users underperform. (Link)"
**Bad:** "[A new MIT study claims LLM users consistently underperform on cognitive tests](URL)"

When multiple sources are provided with body text to reference, **hyperlink ALL links** where the referenced content is used in the newsletter. Don't let any provided link go unhyperlinked.

---

## Segment Archetypes

**Load on-demand:** `references/segment-archetypes.md`

Contains 5 THOUGHT patterns, 4 TREND patterns, and 4 TOOL patterns with examples.

---

## Voice & Writing Style

**The Core Rhythm: Substance → Take**

The OpenEd Daily voice alternates between:
- **Substance:** Facts, quotes, data, specific details
- **Take:** Interpretation, implication, what it means

This creates prose that feels both informed and opinionated. Don't just report facts. Don't just share opinions. Weave them together: ground the reader in something specific, then tell them what to think about it.

**For full examples, load:** `references/opening-letter-patterns.md` (includes segment examples showing this rhythm)

**For detailed voice guidance, load:**
- `references/pirate-wires-segment-techniques.md` - A la carte techniques for TTT segments (longer excerpts, specific applications)
- `references/witty-voice-patterns.md` - General wit patterns (opening letters)
- `ai-tells` skill - Hard blocks (correlatives, banned words)
- `ghostwriter` skill - Humanization patterns

### Core Principles (Always Apply)

**Context + Substance:** Every segment needs both WHO/WHAT/WHY and the actual insight.

**High-Density Prose:** Every sentence carries meaning. Cut dramatic pauses.

**Trust the Reader:** Show, don't tell how to feel. No fake questions.

### Setup Phrases to Eliminate

- "Here's the thing..." / "But here's the kicker..."
- "The clever part:" / "What's interesting:"
- "Here's why that matters..." / "Let that sink in."

### Tone: Curious > Accusatory

Notice gaps, don't blame. Let readers draw conclusions.

**Bad:** "Schools prioritize fun over learning. Educators are failing our kids."

**Good:** "Skycak's point isn't that educators are villains. It's that maximizing learning isn't the only thing schools are trying to do."

---

## Segment Titles

**For detailed patterns and examples, load:** `references/segment-titles.md`

### Quick Reference

- **1-6 words max** - must fit one line of narrow email box
- **ALL CAPS** in final output
- **Create information gap** - reader must read to understand

### Patterns

| Pattern | Example | Why It Works |
|---------|---------|--------------|
| **Label** | THE GETTING BY TRAP | Names phenomenon, creates curiosity |
| **Stat** | 83% OF PARENTS AGREE | Number + incomplete info |
| **Object** | TOOL: CHOMPSAW | Clear, direct |
| **Contrast** | SMALL SCHOOLS BIG IMPACT | Tension between two things |
| **Counterintuitive** | THE OTHER KIND OF TESTING | Challenges assumption |

### Sticky Techniques (Use Sparingly)

- **Alliteration:** PRACTICE PRODUCES PERMANENCE
- **Contrast:** SMALL SCHOOLS BIG DIFFERENCE
- **Rhythm:** Two short balanced phrases

---

## Transitions

Avoid clunky transitions between segments:
- ❌ "Speaking of Janssen..."
- ❌ "On a related note..."
- ❌ "While we're on the topic of..."

Jump straight into the new segment with a hook that stands alone. The `---` divider already signals a new section.

If segments are thematically connected, let the reader make the connection. Don't spell it out.

---

## Phase 4: Social Media (Optional)

For social repurposing, use the `social-content-creation` skill or create `Social_Media_Plan.md`.

---

## Phase 5: QA & Archive

### Final Checklist

- [ ] Segments are orthogonal (related but not repetitive)
- [ ] NO EMOJIS in body
- [ ] ALL CAPS H2 titles
- [ ] 500-800 words total
- [ ] All links work
- [ ] Voice sounds human, not performative
- [ ] Headlines create information gaps

### Archive

```bash
cp [working-folder]/Newsletter_FINAL.md daily-newsletter-workflow/examples/[YYYY-MM-DD]-newsletter.md
```

---

## Quick Reference

### Edition Types

**Type A (Integrated):** All 3 segments orbit a single theme. Use when you have one strong anchor piece.

**Type B (Modular):** Segments stand alone, connected by voice. Use when pieces don't naturally connect - don't force integration.

### Anti-Patterns

- **Forced cheerfulness:** "TGIF Eddies! Hope your week was AMAZING!" → Just "Greetings Eddies."
- **Transcript dump:** Pasting quotes with minimal synthesis → Extract one insight, reframe in your voice
- **Info overload:** 5 stats and 3 sources → One stat, one human voice, one implication
- **Fake question:** "What if schools actually taught kids to think?" → Just tell them
- **Setup-payoff crutch:** "The clever part: [explanation]" → Remove the label, write naturally

---

## Reference Files

**Skill references (load on-demand):**
- `references/pirate-wires-segment-techniques.md` - A la carte Pirate Wires techniques for TTT segments (longer excerpts)
- `references/segment-archetypes.md` - THOUGHT, TREND, TOOL patterns
- `references/opening-letter-patterns.md` - Charlie's voice examples + substance→take rhythm
- `references/segment-titles.md` - Segment headline patterns (1-6 words, sticky)
- `references/witty-voice-patterns.md` - General wit patterns for opening letters

**Content resources:**
- [Tool Database](../../../Studio/Lead Magnet Project/OpenEd_Tool_Database.md)
- [Content Queue](../../../Studio/OpenEd Daily/CONTENT_QUEUE.md)

**Related skills:**
- `ai-tells` - Hard blocks (correlatives, banned words)
- `ghostwriter` - Humanization patterns
- `newsletter-subject-lines` - Subject line writing (dedicated skill)
- `opened-weekly-newsletter-writer` - Friday digest
- `newsletter-to-social` - Social repurposing router
- `TEMPLATE_INDEX.md` - Social format matching

---

## File Naming

Working folder: `Studio/OpenEd Daily/[YYYY-MM-DD] - [Theme]/`

Files:
- `Source_Material.md`
- `Checkpoint_1_Angles.md`
- `Newsletter_DRAFT.md`
- `Newsletter_FINAL.md` (only after approval)
