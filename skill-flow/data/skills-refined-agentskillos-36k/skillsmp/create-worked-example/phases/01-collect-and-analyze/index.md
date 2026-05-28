# Phase 1: Collect & Analyze

## Purpose
Gather all required information from the user, then deeply analyze the **mastery check question** to understand its mathematical structure and define ONE clear strategy.

## Output Format: PPTX-Compatible HTML
All slides will be **PPTX-compatible HTML** (960×540px, light theme). See `03-generate-slides/02-technical-rules.md` for technical specs.

## Prerequisites
- User has requested a worked example
- You have NOT yet seen the problem image

---

## CRITICAL: Understanding the Input

**The problem image the user provides is the MASTERY CHECK QUESTION** - the actual question students will answer on their exit ticket or assessment.

**Your job is to create a worked example that:**
1. Teaches the SAME mathematical skill
2. Uses the SAME strategy and steps
3. Uses a **DIFFERENT context and numbers** than the mastery check

**Why different context?** Students should learn the strategy from the worked example, then apply it independently to the mastery check. If the worked example uses the same numbers/context, students can just copy the answer without learning the underlying skill.

**ALL THREE SCENARIOS must use different contexts:**
- Scenario 1 (Worked Example): Different context from mastery check
- Scenario 2 (Practice): Different context from mastery check AND Scenario 1
- Scenario 3 (Practice): Different context from all above

---

## Step 1.1: Collect Required Information

**Prompt the user for ALL of these:**

```
To create a worked example, I need the following information:

1. **Grade Level**: What grade is this for? (Valid: "6", "7", "8", or "Algebra 1")
2. **Unit Number**: What unit is this from? (e.g., 4)
3. **Lesson Number**: What lesson is this? (e.g., 1)
4. **Learning Goals**: What should students learn from this?
   (e.g., "Students will be able to solve linear equations using the distributive property")
5. **Mastery Check Question**: Please upload an image of the mastery check/exit ticket question.
   (I'll create a worked example that teaches this skill using DIFFERENT numbers and context)

**Optional - Additional Context:**
6. **Reference Images**: Any additional images for context (previous worked examples, diagrams, related problems)
7. **Notes for AI**: Any preferences like "Focus on the balance method strategy", "Want practice with distributing negative numbers", "Use gaming themes for practice problems"

Once I have the required items (especially the mastery check image), I'll analyze the problem and confirm my approach with you before creating slides.
```

**WAIT** for the user to provide all information. Do NOT proceed until you have:
- [ ] Grade level
- [ ] Unit number
- [ ] Lesson number
- [ ] Learning goals
- [ ] Mastery check question image
- [ ] (Optional) Additional reference images
- [ ] (Optional) Notes/preferences for the AI

---

## Step 1.2: Look Up Scope and Sequence ID

After receiving the grade, unit, and lesson, query MongoDB:

```bash
/usr/local/bin/mongosh "$DATABASE_URL" --eval "
const grade = '[GRADE]';
const unitNumber = [UNIT_NUMBER];
const lessonNumber = [LESSON_NUMBER];

const result = db['scope-and-sequence'].findOne({
  grade: grade,
  unitNumber: unitNumber,
  lessonNumber: lessonNumber
});

if (result) {
  print('Scope and Sequence ID:', result._id.toString());
  print('Lesson Name:', result.lessonName);
  print('Unit:', result.unit);
} else {
  print('No matching scope and sequence found');
}
" --quiet
```

Store the `scopeAndSequenceId` for later. If not found, continue anyway (set to `undefined`).

---

## Step 1.3: Deep Analysis of the Problem

**CRITICAL: Do NOT skip this step. Do NOT proceed until complete.**

After receiving the problem image (and any additional context), thoroughly analyze it:

### Using Additional Context (if provided)

If the teacher provided **reference images** or **notes**, incorporate them into your analysis:

- **Reference images**: Use these to understand related concepts, see how similar problems were taught, or identify visual styles the teacher prefers
- **Strategy preferences**: If the teacher says "focus on the balance method", prioritize that strategy even if alternatives exist
- **Context themes**: If the teacher suggests "use gaming themes", incorporate that into scenario creation
- **Focus areas**: If the teacher says "want practice with distributing negatives", ensure the worked example emphasizes that skill

### 1.3a: Solve the problem yourself
- Work through it step-by-step
- Write out your complete solution
- Identify the final answer

### 1.3b: Identify the mathematical structure
- What SPECIFIC type of problem is this?
  - Be precise: "solving two-step equations with variables on both sides"
  - NOT vague: "algebra"
- What mathematical relationships are present?
- What prior knowledge does this assume?

### 1.3c: Identify what makes this challenging
- Where might students make mistakes?
- What's the key insight needed?
- What misconceptions does this address?

### 1.3d: Note constraints
- What format is the answer expected in?
- Any special conditions (positive numbers, whole numbers, etc.)?
- Does it ask for explanation/reasoning?

### 1.3e: Determine visual type

**CRITICAL: ALL graphics/diagrams MUST use SVG.**
SVG is required for PPTX export compatibility. The only exception is simple HTML tables.

**Visual Type Options:**
- **Text-only**: No graphics needed (rare - only pure text/equation problems)
- **HTML table**: Simple data tables with highlighting (HTML `<table>`)
- **SVG visual**: ALL other graphics - this includes:
  - Coordinate planes and graphs
  - Hanger diagrams and balance problems
  - Geometric shapes and diagrams
  - Number lines and bar models
  - Any custom visual representation

**If your problem needs ANY visual beyond a simple table, you MUST use SVG.**

### 1.3f: SVG Planning (REQUIRED if visual type is "SVG visual")

**IF you selected "SVG visual" above, you MUST plan your SVG now.**

**For coordinate plane graphs:**
```
Read: .claude/skills/create-worked-example-sg/phases/01-collect-and-analyze/graph-planning.md
```
Complete ALL steps in that file and include the GRAPH PLAN in your output below.

**For other SVG types (diagrams, shapes, etc.):**
Plan the visual elements:
- What shapes/elements are needed?
- What colors will represent each element?
- What annotations will show the math?
- How will the visual change across slides 2-8?

**IF you selected "Text-only" or "HTML table", skip to the output template.**

### 1.3g: Diagram Evolution (REQUIRED for ALL worked examples)

**⚠️ CRITICAL: This step is REQUIRED. Do NOT skip it.**

Create a **Diagram Evolution** showing how the visual develops step-by-step across slides. This is what teachers need to visualize before approving generation.

**Reference the canonical patterns:**
```
Read: .claude/skills/create-worked-example-sg/reference/diagram-patterns.md
```

Use the ASCII representations in that file as a guide. Generate ASCII previews that match the structure for your visual type.

**Read the detailed instructions and output schema:**
```
Read: .claude/skills/create-worked-example-sg/phases/01-collect-and-analyze/analyze-problem.md
Read: .claude/skills/create-worked-example-sg/phases/01-collect-and-analyze/output-schema.md
```

See the "STEP 8: Generate Diagram Evolution Preview" section in analyze-problem.md for complete instructions and examples.

**The Diagram Evolution MUST include:**
1. **initialState**: ASCII showing the diagram on Problem Setup slide (empty axes, blank tape, etc.)
2. **keyElements**: Array explaining each element and what it represents mathematically
3. **steps**: Array with one entry per strategy move (2-3 entries), each containing:
   - `header`: The slide header (e.g., "STEP 1: IDENTIFY")
   - `ascii`: ASCII showing the diagram state AFTER that step (building cumulatively)
   - `changes`: Array of what was added/changed from previous step

**Why this matters:**
- Teachers can see EXACTLY how the visual will build across slides
- Catches issues like "wrong step order" or "missing annotation" BEFORE slide generation
- The number of steps MUST match `strategyDefinition.moves.length`

### Output Template (YOU MUST COMPLETE THIS):

```
PROBLEM ANALYSIS
================
Problem Type: [specific type]
Mathematical Structure: [describe relationships]

My Solution:
1. [First step with reasoning]
2. [Second step with reasoning]
3. [Third step with reasoning]
Answer: [final answer]

Key Challenge: [what makes this hard]
Common Mistakes: [likely errors]
Required Prior Knowledge: [prerequisites]
Answer Format: [how answer should be presented]
Visual Type: [Text-only | HTML table | SVG visual]
SVG Subtype (if SVG visual): [coordinate-graph | diagram | shape | number-line | other]

SVG PLAN (only if Visual Type is "SVG visual"):
===============================================

[FOR COORDINATE GRAPHS - use graph-planning.md:]
Equations (with EXPLICIT slope and y-intercept):
- Line 1: [equation], slope=[m], y-intercept=[b] ([color])
- Line 2: [equation], slope=[m], y-intercept=[b] ([color])

Scale:
- X_MAX: [rightmost x-value]
- Y_MAX: [top y-value, rounded to nice number]
- X-axis labels: [list]
- Y-axis labels: [list]

Key Points (CALCULATE THESE - ensures math accuracy):
- Line 1 at x=0: y=[calculated]
- Line 1 at x=[X_MAX/2]: y=[calculated]
- Line 1 at x=[X_MAX]: y=[calculated]
- Line 2 at x=0: y=[calculated]
- Line 2 at x=[X_MAX/2]: y=[calculated]
- Line 2 at x=[X_MAX]: y=[calculated]

Annotation:
- Relationship to show: [what mathematical concept]
- Annotation type: [y-intercept-shift / parallel-label / slope-comparison / etc.]
- Label text: [e.g., "+20"]

[FOR OTHER SVG TYPES (diagrams, shapes, etc.):]
Elements:
- Element 1: [shape/component] ([color])
- Element 2: [shape/component] ([color])
- ...

Layout:
- Container size: [width x height in viewBox]
- Element positions: [how elements are arranged]

Annotations across slides:
- Slide 2: [initial state - what's shown]
- Slides 3-4: [Step 1 - what changes/highlights]
- Slides 5-6: [Step 2 - what changes/highlights]
- Slides 7-8: [Step 3 - what changes/highlights]

DIAGRAM PREVIEW (Scenario 1) - REQUIRED for all worked examples:
==============================================================

[ASCII representation of the complete visual structure
 based on patterns from reference/diagram-patterns.md]

Key elements:
- [element 1]: [what it represents]
- [element 2]: [what it represents]
- [element 3]: [what it represents]

Does this visual structure look right for your problem?
```

---

## Step 1.4: Define the Strategy Thread

**Before ANY content creation, define ONE clear strategy.**

### 1.4a: Name the strategy
Give it a clear, memorable name:
- "Balance and Isolate"
- "Find the Unit Rate"
- "Plot and Connect"
- "Table to Equation"

### 1.4b: State it in one sentence
Student-facing explanation:
- "To solve this, we [VERB] the [OBJECT] to find [GOAL]"
- Example: "To solve this, we REMOVE equal items from BOTH SIDES to ISOLATE the unknown."

### 1.4c: Identify the 2-3 moves (maximum 3)
- Move 1: [Action verb] → [What it accomplishes]
- Move 2: [Action verb] → [What it accomplishes]
- Move 3 (if needed): [Action verb] → [What it accomplishes]

### 1.4d: Define consistent language
These step names MUST:
- Use the EXACT same verbs throughout all slides
- Appear on every slide header
- Be referenced in CFU questions

### 1.4e: State the Big Idea
One sentence that captures the core mathematical concept:
- "To solve equations, we keep both sides balanced"
- "Unit rates let us compare different quantities fairly"
- "Parallel lines have the same slope but different y-intercepts"

The Big Idea is more general than the strategy summary - it's the mathematical truth students will remember.

### Output Template (YOU MUST COMPLETE THIS):

```
STRATEGY DEFINITION
===================
Strategy Name: "[Name]"
One-Sentence Summary: "[Student-facing explanation]"
Big Idea: "[The core mathematical concept in one sentence]"

The Moves:
1. [VERB]: [Description] → [Result]
2. [VERB]: [Description] → [Result]
3. [VERB]: [Description] → [Result] (if needed)

Slide Headers Will Say:
- "STEP 1: [VERB]"
- "STEP 2: [VERB]"
- "STEP 3: [VERB]" (if needed)

CFU Questions Will Reference:
- "Why did I [VERB] first?"
- "How does [VERB]ing help us find the answer?"
```

---

## Step 1.5: Create Progress File

**After completing both analysis templates, create the progress tracking file.**

Use the Write tool to create `.worked-example-progress.json` in the presentation directory:

**File path:** `src/app/presentations/{slug}/.worked-example-progress.json`

Where `{slug}` is generated from the strategy name and grade level (e.g., `balance-isolate-hanger-grade8`).

```json
{
  "slug": "[slug]",
  "phase": 1,
  "phaseName": "Collect & Analyze",
  "gradeLevel": "[grade]",
  "unitNumber": [unit],
  "lessonNumber": [lesson],
  "scopeAndSequenceId": "[id or null]",
  "strategyName": "[from STRATEGY DEFINITION]",
  "strategySteps": ["[VERB1]", "[VERB2]", "[VERB3 if applicable]"],
  "problemType": "[from PROBLEM ANALYSIS]",
  "userConfirmed": false,
  "slidesCompleted": [],
  "totalSlides": 0,  // Will be 14-16 for PPTX format
  "scenarios": [],
  "createdAt": "[ISO timestamp]",
  "updatedAt": "[ISO timestamp]"
}
```

**IMPORTANT:**
- Create the directory first: `mkdir -p src/app/presentations/{slug}`
- This file tracks progress and enables resumption if interrupted
- The file will be deleted at the end of Phase 4 upon successful completion

---

## Phase 1 Completion Checklist

Before proceeding, verify you have:
- [ ] All 5 required user inputs collected (grade, unit, lesson, learning goals, mastery check image)
- [ ] (If provided) Additional context incorporated into analysis
- [ ] Scope and sequence ID looked up (or noted as undefined)
- [ ] PROBLEM ANALYSIS template completed
- [ ] STRATEGY DEFINITION template completed
- [ ] Strategy has exactly 2-3 moves with consistent verbs
- [ ] Visual type determined: Text-only, HTML table, or SVG visual
- [ ] **Diagram Evolution preview created** showing step-by-step progression (how content builds across slides)
- [ ] **IF visual type is SVG visual:** SVG PLAN completed (elements, layout, annotations per slide)
- [ ] Progress file created at `src/app/presentations/{slug}/.worked-example-progress.json`

---

## NEXT PHASE

**When Phase 1 is complete:**

Use the Read tool to read the Phase 2 instructions:
```
Read: .claude/skills/create-worked-example-sg/phases/02-confirm-and-plan.md
```

Do NOT proceed to Phase 2 until you have completed BOTH output templates above.
