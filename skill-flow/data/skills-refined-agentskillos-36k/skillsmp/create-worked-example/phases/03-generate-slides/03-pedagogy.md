# Pedagogical Principles

**What this file covers:** Teaching principles, visual consistency, CFU rules, conciseness requirements.

---

## Core Principles (NON-NEGOTIABLE)

### 1. The "Click-to-Reveal" Principle

- CFU/Answer boxes start HIDDEN, appear when teacher clicks
- Forces mental commitment before seeing solution
- Animation handles reveal - no duplicate slides needed
- **No JavaScript, no onclick handlers in HTML**

### 2. The "Visual Stability" Principle

- Keep main visual (table, diagram) in SAME position across slides 3-6
- Add annotations AROUND the stationary element
- Mimics teacher at whiteboard - problem stays put, annotations appear

### 3. The "Scaffolding Removal" Principle

- Slides 3-6: Maximum scaffolding (step-by-step, highlighting, CFU+Answer stacked)
- Printable slide 7: ZERO scaffolding (just practice problems with work space)
- Students must apply the strategy independently on the printable worksheet

### 4. The "Consistent Step Names" Principle

- Use EXACT verbs from strategyDefinition.moves throughout
- Slide headers: "STEP 1: [VERB]", "STEP 2: [VERB]"
- CFU questions reference these exact verbs

### 5. The "Real World" Principle

- Use engaging, age-appropriate contexts
- Avoid boring textbook scenarios (no "John has 5 apples")
- Each scenario needs a visual anchor (icon or theme)

**Good scenario contexts by grade:**
- Grade 6-7: Video game items, YouTube views, TikTok followers, sports stats
- Grade 8-9: Drone flight, crypto mining, streaming subscriptions, esports tournaments
- Grade 10+: Investment returns, data science, engineering projects, startup growth

---

## Visual Consistency Across Step Slides (CRITICAL)

**This is the most important rule for student learning.**

The main visual (graph, table, diagram) must stay in the SAME position across all step slides (3-6).

### What "Consistency" Means

**Position stays fixed. Content evolves.**

| Stays Fixed | Changes Each Step |
|-------------|-------------------|
| Visual position (x, y, width, height) | Which elements are highlighted |
| Overall scale and dimensions | Annotations and labels added |
| Base structure (axes, grid, boxes) | Values revealed or filled in |
| Layout (two-column, left/right split) | Emphasis shifts to current step |

### Progressive Visual Revelation (REQUIRED)

**Each step slide must ADD something new to the visual.** If slides 3-6 show identical visuals, students see repetition instead of progression.

**The Visual Tells a Story:**
```
Slide 3 (Setup):  Shows the PROBLEM → unknowns visible, nothing solved yet
Slide 4 (Step 1): Shows Step 1 RESULT → first piece of solution highlighted (CFU+Answer stacked)
Slide 5 (Step 2): Shows Step 2 RESULT → builds on Step 1 (CFU+Answer stacked)
Slide 6 (Step 3): Shows COMPLETE SOLUTION → answer visible on visual (CFU+Answer stacked)
```

**Examples of What to ADD Each Step:**

| Visual Type | What Gets Added/Highlighted |
|-------------|----------------------------|
| Coordinate graph | New line plotted, point labeled, intersection marked |
| Tape diagram | Boxes divided, values filled in, count revealed |
| Hanger diagram | Terms removed from both sides, variable isolated |
| Double number line | Unit rate marked, unknown value found |
| Input-output table | Pattern arrow, missing value filled |
| Area model | Partial products computed, sum shown |

### Common Mistakes (NEVER DO THESE)

**Position/Structure Errors:**
- Moving the graph/visual between slides
- Changing visual dimensions or scale
- Changing the layout structure mid-sequence

**Repetition Errors:**
- Showing the IDENTICAL visual across multiple step slides
- Keeping the same elements highlighted without adding new information
- Not showing the result of each step ON the visual
- Showing the same concept/information in multiple places on the same slide (e.g., equation in left column AND on the visual)

### CFU/Answer Boxes ANIMATE in place

- They overlay the existing content
- The underlying slide content doesn't change
- Teacher clicks to reveal the box during presentation

---

## CFU Question Requirements

**Format Rules (STRICTLY ENFORCED):**
- **ONE question only** - never two-part questions
- **12 words max** - if longer, rewrite it shorter
- **Strategy-focused** - ask about WHY, not WHAT

**Questions MUST reference the strategy verb:**
- "Why did I [VERB] first?" (6 words)
- "How did I know to [VERB] here?" (8 words)
- "Why is the '?' at the beginning?" (7 words)

**Questions must NOT be:**
- "What is 6 / 2?" (computation)
- "What's the answer?" (result-focused)
- "What is X? How did you calculate it?" (TWO questions - WRONG!)
- Questions longer than 12 words

---

## Answer Box Requirements

**Format Rules (STRICTLY ENFORCED):**
- **25 words max** - 1-2 short sentences only
- **Direct answer** - no extra context or "fun facts"
- **No redundancy** - don't repeat what the visual shows

**Good answers:**
- "Each box represents one student. The 6 inside shows nuggets per student." (12 words)
- "I subtracted 4 to isolate the variable term on one side." (11 words)

**Bad answers:**
- "To ISOLATE the variable term! Subtracting 4 removes the constant, leaving just 2x alone on one side. This is also called the constant of proportionality - the slope of line g!" (too long, extra context)

---

## Left Column Conciseness (CRITICAL)

**The left column is for TEXT CONTENT ONLY. Keep it minimal.**

### Problem Reminder Box (Slides 3-6, bottom left corner)

**Format:** Ultra-condensed summary, max 15 words
**Position:** Bottom left corner (y=450) using `problem-reminder.html` pattern

```
GOOD: "30 nuggets total. 6 per student. How many students?"
GOOD: "Turtle g travels at constant speed. Find when it catches turtle f."
BAD:  "A large box has 30 chicken nuggets. If each student gets 6 nuggets, how many students can have a snack?"
```

### Step Content (Left Column)

**NO explanatory prose.** The step title + equation IS the content.

| Element | Max Words | Purpose |
|---------|-----------|---------|
| Step title | 6-8 words | "STEP 1: Write the Equations" |
| Subtitle | 0 words | REMOVE entirely - no "First, let's..." |
| Problem reminder | 15 words | Condensed problem summary |
| Main content | n/a | Large (36-48px) - equation, key text, or focus element |
| Supporting text | 10 words | Only if absolutely needed |

**What to REMOVE from left column:**
- "First, let's figure out how fast turtle g is moving by finding a point on the line."
- "Now we need to identify what each number represents in this problem."
- "Let's start by writing the equation that represents this situation."
- Any sentence starting with "Let's", "Now", "First", "Next"

**What to KEEP in left column:**
- Step badge and title
- Condensed problem reminder (15 words max)
- Large main content (36-48px)
- Brief bullet points (if needed, 3-5 words each)

---

## Two-Column Rule: COMPLEMENTARY, NOT DUPLICATE

```
LEFT COLUMN              RIGHT COLUMN
-------------            -------------
Problem reminder    →    Visual diagram
Equations (as text)      Diagram showing same math visually
Brief explanation        Labels & annotations

If you wrote it on the left, DON'T write it on the right
```

**Test:** Cover the right column. Can you understand the step from just the left?
**Test:** Cover the left column. Can you understand the step from just the right?
If BOTH columns show the same information, you've duplicated. DELETE from one side.

---

## The 3-Second Scan Test

**Can a student understand the slide's key point in 3 seconds?**

If not, it's too cluttered. Remove:
- Explanatory subtitles
- Redundant info boxes
- Text that explains what the visual already shows
- Multiple pieces of information competing for attention

---

## Visual Annotation Rules (ALL Diagram Types)

**Reference:** `reference/diagram-patterns.md` contains diagram-specific examples.

### The Core Principle (Transferable Across All Visuals)

**Annotations are LABELS, not EXPLANATIONS.**

| ✅ Labels (SHORT, on visual) | ❌ Explanations (LONG, belongs in left column) |
|------------------------------|-----------------------------------------------|
| `6` | `Each box represents 6 nuggets` |
| `?` | `The question mark shows what we're solving for` |
| `(0, 6)` | `y-intercept = 6` |
| `g` | `This line represents turtle g` |

### The Delete Test

**Before finalizing any slide:** For each text element on the visual, ask: "If I delete this, does the visual still make sense?"

- If YES → delete it (the left column can explain it)
- If NO → keep it (it's a necessary label)

### Why This Works Across Contexts

This principle applies whether the visual is:
- A tape diagram (label boxes with numbers, not sentences)
- A coordinate graph (label points with coordinates, not descriptions)
- An area model (label partial products, not "this is where we multiply")
- A hanger diagram (label sides with expressions, not "left side equals right side")

The left column EXPLAINS. The visual SHOWS. They complement, never duplicate.
