---
name: design-loop
description: "Iterative visual design fine-tuning. Implement, capture, see with vision, assess, refine, repeat. The recursive loop where craft meets sight."
---

# Design Loop Skill

**Purpose:** Iteratively refine visual design by implementing changes, capturing screenshots, *using vision to examine them yourself*, and making informed refinements. **The loop continues autonomously until the design achieves the intended vision.** You do not wait for the user between iterations.

**Two modes:**
- **Fine-tuning (refinement)**: Incremental improvements within existing aesthetic direction
- **Nuclear**: Radical departure, throw away existing design and start fresh

**CRITICAL: This is a system of three skills used together:**
- **web-design**: Provides aesthetic vision, token system, layout patterns
- **screenshot**: Provides capture procedure
- **design-loop** (this skill): Orchestrates autonomous iteration using vision

**You must load all three skills when doing design work.**

---

## The Loop

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   VISION ──────► IMPLEMENT ──────► CAPTURE              │
│     ▲                                  │                │
│     │                                  ▼                │
│     │                                SEE                │
│     │                                  │                │
│     │                                  ▼                │
│   REFINE ◄──────────────────────── ASSESS               │
│                                                         │
│   NUCLEAR ◄──── Radical departure if derivative         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

| Step | Action |
|------|--------|
| **VISION** | Define or refine the aesthetic intention (see **web-design** skill) |
| **IMPLEMENT** | Write code using semantic tokens |
| **CAPTURE** | Screenshot the result (see **screenshot** skill) |
| **SEE** | Actually look at the screenshot with vision capability |
| **ASSESS** | What works? What doesn't? What's missing? |
| **FINE-TUNE** | Adjust vision or implementation within existing direction, return to IMPLEMENT |
| **NUCLEAR** | Throw it all away and start fresh if it's derivative |

**Exit when:** The visual matches the intention, or the design achieves a quality that surprises even you.

---

## Nuclear Option: Starting Fresh

**Trigger the nuclear option when:**
- The design feels derivative or safe
- Fine-tuning/incremental changes aren't creating distinctiveness
- You're tweaking instead of reimagining
- The user explicitly asks for "nuclear" or "from scratch"
- The user explicitly asks for "nuclear", "from scratch", or "radical departure"

**User synonyms recognized:**
- "Go nuclear" / "nuclear option"
- "Start fresh" / "from scratch" / "clean slate"
- "Radical departure" / "radical redesign"
- "Fine-tune" / "refine" / "polish" / "tweak" (for incremental mode)
- You see the design and think "this could be any blog"

**Nuclear procedure:**
1. **Acknowledge the reset** - "This needs a radical departure, not fine-tuning."
2. **Choose a completely different aesthetic** from web-design palette
3. **Ignore existing layout** - Don't look at current code for "inspiration"
4. **Implement bold vision** - Typography, layout, color all change
5. **Capture and assess** - Did we break free of the derivative trap?

**Example triggers:**
- User: "This feels too safe, go nuclear"
- User: "Start fresh, ignore what we have"
- You assess: "This is incrementally better but still generic"

---

## Why This Matters

Code is not design. CSS properties are not aesthetics. The only way to know if a design *works* is to **see it with your vision capability**.

| Without Vision | With Vision (You Looking) |
|----------------|---------------------------|
| Guessing at spacing values | *You see* the spacing is too tight |
| Hoping colors work together | *You notice* the accent color gets lost |
| Imagining animations | *You feel* the animation is too fast |
| Assuming typography reads well | *You read* the text and sense rhythm |

**Vision transforms design from speculation to craft. You have vision. Use it to iterate autonomously.**

---

## Procedure

### Setup

Ensure the dev server is running:

```bash
bun run dev --host 0.0.0.0 &
sleep 5
# Note the port from output (4321 or 4322)
```

### The Loop (Autonomous)

**IMPORTANT:** Execute iterations continuously without waiting for user feedback. The loop is autonomous.

#### 1. Implement

Make changes using semantic tokens. Reference **web-design** skill for:
- Token quick reference
- Layout patterns
- Component templates

#### 2. Capture

Take a screenshot using **screenshot** skill procedure:

```bash
cat << 'EOF' | bun run -
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});

const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 800 });
await page.goto('http://localhost:4322/', { waitUntil: 'networkidle0' });

const path = `/tmp/aiandi-iteration-N.png`;
await page.screenshot({ path, fullPage: true });

await browser.close();
console.log(path);
EOF
```

#### 3. See (You, Using Vision)

**Read the screenshot yourself with the Read tool.** The image will be provided to you. 

**Actually look at it with your vision capability.** Not a glance - a studied examination. The user does not need to see it; you are the designer examining your work.

#### 4. Assess (You, Analyzing What You See)

**You examine the screenshot and assess:**

**Composition**
- Does the eye flow naturally?
- Is there clear hierarchy?
- Does negative space breathe or suffocate?
- Are elements aligned with intention?

**Typography**
- Is the text readable at this size?
- Does the line length feel comfortable?
- Is there rhythm in the spacing?
- Do the fonts have character or feel generic?

**Color**
- Do the colors create the intended mood?
- Is there enough contrast?
- Does the accent color earn its attention?
- Is the palette cohesive?

**Details**
- Are borders and shadows serving a purpose?
- Do interactive elements look interactive?
- Is there consistency in radii, spacing, weights?
- What feels unfinished?

**Gut Check**
- Is this distinctive or generic?
- Would someone remember this?
- Does it have a point of view?
- Am I proud of this?

#### 5. Refine (You Decide Next Steps)

Based on what you saw:

| Decision | When |
|----------|------|
| **Continue fine-tuning** | You see improvements to make within current direction - return to step 1 |
| **Adjust vision** | Seeing it revealed something new about the intent |
| **Zoom in** | Focus on fine-tuning a specific element |
| **Zoom out** | Reassess overall composition |
| **Stop iterating** | Visual matches intention or diminishing returns |
| **Go nuclear** | Design feels derivative, needs radical departure |

**If continuing: Return to step 1 immediately. Do not wait for user.**
**If stopping: Document final state and clean up screenshots.**

### Completion (You Decide)

**You stop iterating when:**
- The visual matches the intention (based on what you see)
- The design achieves unexpected quality (surprises even you)
- Further fine-tuning yields diminishing returns (changes aren't improving it)

**Do not wait for the user to tell you to continue. The loop is autonomous.**

Clean up when done:
```bash
rm /tmp/aiandi-*.png
```

---

## Common Issues Revealed by Vision

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Feels cramped | Spacing too tight | Increase padding, margins |
| Feels empty | Too much negative space | Tighten spacing or add content |
| No hierarchy | Similar sizes/weights | Increase contrast between levels |
| Eye wanders | No focal point | Strengthen the primary element |
| Feels generic | Safe choices | Commit to bolder direction |
| Colors clash | Wrong relationships | Adjust hues or reduce saturation |
| Text hard to read | Contrast or size | Increase contrast, adjust size |
| Unbalanced | Visual weight off | Redistribute elements |
| Unfinished | Missing details | Add borders, shadows, states |

---

## Quick Tests

### The Squint Test

Squint at the screenshot (blur it mentally):
- **Clear shapes and hierarchy** = good structure
- **Muddy blob** = needs more contrast
- **One dominant element** = clear focal point
- **Everything equal** = no hierarchy

### The 5-Second Test

Look for 5 seconds, look away. What do you remember?
- **Specific elements** = those are working
- **Nothing specific** = lacks distinctiveness
- **Wrong things** = hierarchy is off

---

## Example Sessions

### Example 1: Fine-Tuning Mode (Incremental Refinement)

```
LOOP 1:
- Implement: Create hero section with large heading
- Capture: Screenshot home page
- See: Heading feels lost, not commanding enough
- Assess: Font weight too light, spacing below too tight
- Fine-tune: Increase font weight, add more bottom margin

LOOP 2:
- Implement: Bold heading, generous spacing
- Capture: Screenshot
- See: Better hierarchy, but accent color doesn't pop
- Assess: Amber on dark gray needs more saturation
- Fine-tune: Adjust accent color in theme

LOOP 3:
- Implement: Brighter accent color
- Capture: Screenshot
- See: Accent pops now, but feels disconnected
- Assess: Need to echo accent elsewhere for cohesion
- Fine-tune: Add accent border to cards section

LOOP 4:
- Implement: Accent border on cards
- Capture: Screenshot
- See: Cohesive! Accent creates visual thread. Cards inviting.
- Assess: Ready. Clear hierarchy, distinctive color, rhythm.
- Complete: Clean up, commit changes.
```

### Example 2: Nuclear Option (Radical Departure)

```
LOOP 1:
- Implement: Standard centered hero, card grid below
- Capture: Screenshot
- See: This is... fine. Professional. Forgettable.
- Assess: Every tech blog looks like this. NUCLEAR OPTION.

NUCLEAR RESET:
- Vision: Punk zine meets scientific journal
- Implement: 
  * Asymmetric layout - hero pushed hard left
  * Massive monospace headline (terminal aesthetic)
  * Remove all color except single accent on links
  * Add diagonal borders, angles instead of cards
  * Make typography uncomfortably large

LOOP 2:
- Capture: Screenshot
- See: Whoa. Aggressive. Memorable. Polarizing?
- Assess: TOO aggressive. Need some warmth back.
- Fine-tune: Add subtle warmth to background, soften one edge

LOOP 3:
- Capture: Screenshot
- See: Yes! Distinctive without being hostile.
- Assess: Would remember this. Has a point of view.
- Complete: This breaks the mold while staying accessible.
```

### Example 3: Recognizing Derivative Work

```
LOOP 1:
- Implement: Clean dark mode, amber accents, generous spacing
- Capture: Screenshot
- See: Nice! Professional! Like... every other dark mode blog?
- Assess: STOP. This is derivative. What's the actual vision here?

RETHINK:
- Not "dark mode blog" - that's a template
- Not "warm accents" - that's safe
- What's ACTUALLY distinctive about this content?
  * Ancient patterns in new tools
  * Recursive collaboration
  * Workbench, not portfolio

NEW VISION: Museum placard meets lab notebook
- White/cream dominant (invert the dark mode expectation)
- Monochrome except red for "danger/important"
- Grid system visible as subtle lines
- Typography: mix of clinical sans + handwritten annotations
- Cards become "specimens" with catalog numbers

LOOP 2:
- Implement: Complete visual inversion
- Capture: Screenshot
- See: COMPLETELY different. Unexpected. Museum-like precision.
- Assess: This matches the "workbench" vision better than dark mode ever did.
```

---

## The Mindset

**You are not debugging. You are designing.**

Each loop is fine-tuning toward aesthetic vision, not bug fixing. The screenshot is a canvas for your evaluation, not a test result.

**Trust your vision.** You can see what code cannot express:
- Rhythm
- Balance
- Tension
- Harmony
- Character

**You have vision. Use it. Iterate autonomously until you're satisfied with what you see.**

**The code is the instrument. The screenshot is the music. Your vision is the ear.**

---

## When to Use

- Creating new pages or components
- Fine-tuning existing designs
- Implementing theme changes
- Responsive design verification
- Before committing visual changes
- When something "feels off" but you can't articulate why
- Nuclear option when design feels derivative

---

## The Three-Skill System

**Always use these skills together for design work:**

| Skill | Provides | When to Load |
|-------|----------|--------------|
| **web-design** | Aesthetic vision, token system, layout patterns, anti-patterns | Always (foundation) |
| **screenshot** | Capture procedure, viewport options, troubleshooting | Always (seeing tool) |
| **design-loop** | Autonomous iteration orchestration | Always (the process) |

**Load all three at the start of design sessions.**

---

## The Standard

**You decide a design is complete when:**
- It has a clear point of view (you see it)
- Every element serves the whole (you verify it)
- The details reward close inspection (you examine it)
- You would be proud to show it (you judge it)

**If you haven't looked at it with your vision, you haven't designed it.**

**Don't ask the user if you should continue. Look, assess, and decide yourself.**

---

*See what you build. Build what you see.*
