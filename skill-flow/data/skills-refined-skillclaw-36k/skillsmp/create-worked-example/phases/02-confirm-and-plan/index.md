# Phase 2: Confirm & Plan

## Purpose
Present your analysis to the user, get their confirmation, and plan the three scenarios - all using DIFFERENT contexts from the mastery check.

## Output Format: PPTX-Compatible HTML
All slides will be **PPTX-compatible HTML** (960×540px, light theme, 7 slides). See `03-generate-slides/02-technical-rules.md` for technical specs.

## Prerequisites
- Phase 1 complete
- You have completed PROBLEM ANALYSIS template
- You have completed STRATEGY DEFINITION template

---

## REMINDER: Context Separation

The user provided a **mastery check question**. ALL scenarios you create must use **different contexts and numbers** from that question:

| What | Context |
|------|---------|
| Mastery Check (user's input) | The ACTUAL question students will answer |
| Scenario 1 (Worked Example) | DIFFERENT context - teaches the strategy |
| Scenario 2 (Practice) | DIFFERENT context - first practice |
| Scenario 3 (Practice) | DIFFERENT context - second practice |

**Students will see:** Worked Example → Practice 1 → Practice 2 → (then later) Mastery Check

---

## Step 2.1: Present Analysis to User

**Show the user your understanding and WAIT for confirmation.**

Use this exact template:

```
Based on the mastery check question you provided, here's my understanding:

**Problem Type:** [from PROBLEM ANALYSIS]
**Big Idea:** [the core mathematical concept from STRATEGY DEFINITION]
**Strategy I'll Use:** [strategy name from STRATEGY DEFINITION]
**One-Sentence Summary:** [from STRATEGY DEFINITION]

**Visual Type:** [from Visual Types table]
**Visual Plan:** [key details for this visual - see VisualPlan schemas]
  - [field 1]: [value]
  - [field 2]: [value]
  - [field 3]: [value, if applicable]

**The Steps:**
1. [STEP VERB]: [brief description]
2. [STEP VERB]: [brief description]
3. [STEP VERB]: [brief description, if needed]

**The three scenarios (all DIFFERENT from the mastery check):**
- Scenario 1 (worked example): [context + what makes it engaging]
- Scenario 2 (practice): [different context]
- Scenario 3 (practice): [different context]

Note: These scenarios all teach the same skill as your mastery check but use different numbers and contexts, so students learn the strategy without seeing the actual answer.
```

### ⚠️ REQUIRED: Include Diagram Evolution

**Include the Diagram Evolution you created in Phase 1.** This shows the user how the visual will develop step-by-step across slides.

The evolution was already generated in Phase 1 using `reference/diagram-patterns.md` as a guide. Present it here so the user can confirm the visual progression is correct before proceeding.

**Example:**
```
**Diagram Evolution (Scenario 1 - Chicken Nuggets):**

INITIAL STATE (Problem Setup):
┌────────────────────────────────────────┐
│                 30                     │
└────────────────────────────────────────┘
Total: 30 nuggets, Groups: 5 students, Find: ?

STEP 1: PARTITION
┌────────┬────────┬────────┬────────┬────────┐
│   ?    │   ?    │   ?    │   ?    │   ?    │  = 30
└────────┴────────┴────────┴────────┴────────┘
+ Divide into 5 equal parts
+ Mark each with ?

STEP 2: CALCULATE
┌────────┬────────┬────────┬────────┬────────┐
│   6    │   6    │   6    │   6    │   6    │  = 30 ✓
└────────┴────────┴────────┴────────┴────────┘
+ Calculate: 30 ÷ 5 = 6
+ Fill in values

Key elements:
- Each box: nuggets per student
- Total: 30 nuggets
- Unknown (?): number per student

Does this visual progression look right?
```

**Then ask for confirmation:**

```
Does this match what you're looking for? Should I proceed or adjust anything?
```

---

## Step 2.2: WAIT for User Confirmation

**STOP HERE. Do not proceed until the user responds.**

The user might:
- **Confirm** ("yes", "proceed", "looks good") → Continue to Step 2.3
- **Request changes** → Adjust your analysis/strategy and re-present
- **Ask questions** → Answer them, then re-confirm

**Do NOT generate slides until the user explicitly confirms.**

---

## Visual Types

**Choose ONE visual type that best represents the math:**

| Visual Type | Use For | Key Details to Plan |
|-------------|---------|---------------------|
| `tape-diagram` | Division, multiplication, part-whole | boxes, values per box, total, unknown position |
| `coordinate-graph` | Linear equations, rates, proportions | equations, scale, keyPoints, annotations |
| `double-number-line` | Ratios, unit rates, percentages | quantity A values, quantity B values, alignment |
| `area-model` | Multiplication, distributive property | dimensions, partial products |
| `number-line` | Integers, inequalities, operations | range, marked points, arrows |
| `ratio-table` | Equivalent ratios, scaling | column values, scale factors |
| `hanger-diagram` | Equation solving, balance | left side, right side, shapes |
| `input-output-table` | Functions, patterns, rules | input values, output values, rule |
| `grid-diagram` | Area by counting, decomposing shapes | rows, cols, shaded regions, unit label |
| `net-diagram` | Surface area, 3D→2D unfolding | shape type, faces with dimensions, fold lines |
| `measurement-diagram` | Base & height, labeled dimensions | shape type, labeled measurements, right angle indicators |
| `discrete-diagram` | Objects in groups, discrete ratios | groups, items per group, total, visual type |
| `base-ten-diagram` | Place value, decimal operations | ones, tens, hundreds blocks, operation |
| `dot-plot` | Data distributions, frequencies | data points, axis range, label |
| `box-plot` | Quartiles, variability, outliers | min, Q1, median, Q3, max, outliers |
| `bar-graph` | Comparing frequencies, categories | categories, values, orientation |
| `tree-diagram` | Probability, sample spaces | branches, probabilities, outcomes |
| `circle-diagram` | Circles with labeled parts | radius, diameter, circumference, center point |
| `scale-drawing` | Maps, floor plans, blueprints | scale factor, actual/drawing measurements |
| `scaled-figures` | Original vs copy comparison | original dims, scale factor, copy dims |
| `other` | Custom diagrams not listed above | describe visual structure and key elements |

**Visual selection happens ONCE in analysis, then applies to ALL scenarios.**

---

## Step 2.3: Generate Scenarios (All Different from Mastery Check)

**Only after user confirms**, finalize the three scenarios.

### Critical: Context Separation

**NONE of the scenarios should use the same context or numbers as the mastery check question the user provided.**

The mastery check is what students will answer AFTER completing the worked example and practice. Your scenarios prepare them for it without giving away the answer.

### Scenario Requirements

Each scenario MUST:
- Use the **exact same mathematical structure** as the mastery check
- Require the **exact same strategy** to solve
- Use **DIFFERENT numbers and context** from the mastery check (and from each other)
- Be solvable using the **exact same steps in the exact same order**
- Include a **condensed problem reminder (≤15 words)** for use on slides 2-8

### ⚠️ Visual Progression: Plan What Changes Each Step (REQUIRED for Scenario 1)

**For the worked example (Scenario 1), you MUST define what the visual shows at each step.**

The visual should tell a story that builds toward the answer. Each step adds something new.

**Format:** For each step, describe what gets ADDED or HIGHLIGHTED on the visual.

```
Visual Progression (Scenario 1):
- Setup (Slide 2): [What the visual shows initially - problem state, unknowns visible]
- Step 1 (Slides 3-4): [What gets highlighted/added after Step 1]
- Step 2 (Slides 5-6): [What gets highlighted/added after Step 2]
- Step 3 (Slides 7-8): [What shows the final answer on the visual]
```

**Examples by Visual Type:**

| Visual Type | Setup Shows | Step 1 Adds | Step 2 Adds | Step 3 Adds |
|-------------|-------------|-------------|-------------|-------------|
| Tape diagram | Empty tape with ? and total | Boxes with value per box | Highlight the count | Answer label |
| Coordinate graph | Blank axes with labels | First line plotted | Second line plotted | Intersection labeled |
| Hanger diagram | Initial balanced equation | Subtraction from both sides | Division both sides | Variable isolated |
| Double number line | Two lines with known values | Unit rate marked | Scale factor applied | Unknown value found |

### ⚠️ Conciseness: Define Problem Reminders NOW

For each scenario, create the **condensed problem reminder** that will appear on slides.

**Format:** Short phrases, not full sentences. Max 15 words.

```
✅ GOOD: "30 nuggets total. 6 per student. How many students?"
✅ GOOD: "Drone: 150m in 30 sec. Find the speed."
❌ BAD:  "A large box has 30 chicken nuggets. If each student gets 6 nuggets, how many students can have a snack?"
```

### Scenario Design Principles

**DO:**
- Match context to grade level interests (gaming, social media, sports, etc.)
- Keep mathematical difficulty identical to mastery check
- Ensure the same moves apply in the same order
- Use engaging, real-world situations
- Give each scenario a visual anchor (icon/theme)
- **Verify each scenario is clearly different from the mastery check**

**DO NOT:**
- Use the same context as the mastery check question
- Use the same numbers as the mastery check question
- Change the problem type
- Add or remove steps from the solution
- Introduce new mathematical concepts
- Create scenarios requiring a different strategy

### Output Template:

```
MASTERY CHECK CONTEXT (from user's input):
[Brief description of the context/numbers in the user's question]

VISUAL TYPE: [from Visual Types table above]

THREE SCENARIOS (all DIFFERENT from mastery check):
===================================================

Scenario 1 (Worked Example):
- Context: [engaging scenario name - DIFFERENT from mastery check]
- Theme/Icon: [visual anchor]
- Numbers: [specific values - DIFFERENT from mastery check]
- **Problem Reminder (≤15 words):** [condensed summary for slides]
- Same mathematical structure: [yes/explain how]
- Different from mastery check: [yes/explain what's different]
- **VisualPlan:** [see schema below - details for THIS scenario's numbers]
- **Visual Progression:** (REQUIRED - what changes on visual each step)
  - Setup: [initial state - problem shown, unknowns visible]
  - Step 1: [what gets added/highlighted]
  - Step 2: [what gets added/highlighted]
  - Step 3: [answer revealed on visual]

Scenario 2 (Practice):
- Context: [different engaging scenario]
- Theme/Icon: [visual anchor]
- Numbers: [different values]
- **Problem Reminder (≤15 words):** [condensed summary for slides]
- Uses same strategy: [yes/explain how]
- Different from mastery check AND Scenario 1: [yes/explain]
- **VisualPlan:** [details for THIS scenario's numbers]

Scenario 3 (Practice):
- Context: [different engaging scenario]
- Theme/Icon: [visual anchor]
- Numbers: [different values]
- **Problem Reminder (≤15 words):** [condensed summary for slides]
- Uses same strategy: [yes/explain how]
- Different from mastery check AND Scenarios 1-2: [yes/explain]
- **VisualPlan:** [details for THIS scenario's numbers]
```

### VisualPlan Schema (by visual type)

Each scenario MUST have its own VisualPlan with values specific to that scenario's numbers.

**tape-diagram:**
```
VisualPlan:
  boxes: [number of boxes]
  valuePerBox: [value inside each box]
  total: [total value]
  unknownPosition: "start" | "box" | "total"
```

**coordinate-graph:** (See `phases/01-collect-and-analyze/graph-planning.md` for full planning)
```
VisualPlan:
  equations: ["y = 2x + 3", "y = 0.5x"]
  scale: { xMin, xMax, yMin, yMax }
  keyPoints: [{ label: "y-intercept", x: 0, y: 3 }, { label: "solution", x: 4, y: 11 }]
  annotations: ["y-intercept shift", "parallel lines"]
```
**Note:** Coordinate graphs require detailed planning. After selecting this visual type, read `graph-planning.md` and complete the full GraphPlan with equations, calculated endpoints, scale tables, and annotation positions.

**double-number-line:**
```
VisualPlan:
  quantityA: { label: "cups", values: [0, 2, 4, 6] }
  quantityB: { label: "servings", values: [0, 3, 6, 9] }
  highlightPair: [4, 6]
```

**area-model:**
```
VisualPlan:
  dimensions: [width, height] or [a+b, c+d]
  partialProducts: [[a*c, a*d], [b*c, b*d]]
```

**number-line:**
```
VisualPlan:
  range: [min, max]
  markedPoints: [{ value, label, style: "closed"|"open" }]
  arrows: [{ from, to, label }]
```

**ratio-table:**
```
VisualPlan:
  rows: [{ label: "apples", values: [2, 4, 6, "?"] }]
  scaleFactors: ["×2", "×3"]
```

**hanger-diagram:**
```
VisualPlan:
  leftSide: "3x + 1"
  rightSide: "10"
  shapes: { triangle: "x", square: "1" }
```

**input-output-table:**
```
VisualPlan:
  rule: "×3 + 2" or "y = 3x + 2"
  inputs: [1, 2, 3, 4, "?"]
  outputs: [5, 8, 11, 14, "?"]
  unknownPosition: "input" | "output" | "both"
```

**grid-diagram:**
```
VisualPlan:
  rows: [number of rows]
  cols: [number of columns]
  shadedRegions: [{ startRow, startCol, endRow, endCol, color }]
  unitLabel: "sq cm" | "sq in" | "units"
  showGrid: true | false
```

**net-diagram:**
```
VisualPlan:
  shapeType: "rectangular-prism" | "triangular-prism" | "pyramid" | "cube"
  faces: [{ shape: "rectangle" | "triangle", width, height, label }]
  foldLines: true | false
  dimensions: { length, width, height }
```

**measurement-diagram:**
```
VisualPlan:
  shapeType: "triangle" | "parallelogram" | "trapezoid" | "rectangle"
  measurements: [{ label: "base" | "height" | "side", value, position }]
  showRightAngle: true | false
  showDashedHeight: true | false
```

**discrete-diagram:**
```
VisualPlan:
  groups: [number of groups]
  itemsPerGroup: [items in each group]
  totalItems: [total count]
  visualType: "circles" | "squares" | "icons"
  arrangement: "rows" | "clusters"
```

**base-ten-diagram:**
```
VisualPlan:
  hundreds: [number of hundred blocks]
  tens: [number of ten rods]
  ones: [number of unit cubes]
  operation: "none" | "addition" | "subtraction" | "regrouping"
  showValues: true | false
```

**dot-plot:**
```
VisualPlan:
  dataPoints: [2, 3, 3, 4, 4, 4, 5, 5, 6]
  axisLabel: "Number of pets"
  axisRange: [0, 10]
  title: "Pets Owned by Students"
```

**box-plot:**
```
VisualPlan:
  min: 12
  q1: 18
  median: 25
  q3: 32
  max: 45
  outliers: [5, 52]
  axisLabel: "Test Scores"
  axisRange: [0, 60]
```

**bar-graph:**
```
VisualPlan:
  categories: ["Red", "Blue", "Green", "Yellow"]
  values: [12, 8, 15, 6]
  orientation: "vertical" | "horizontal"
  axisLabel: "Frequency"
  title: "Favorite Colors"
```

**tree-diagram:**
```
VisualPlan:
  levels: [
    { outcomes: ["Heads", "Tails"], probabilities: [0.5, 0.5] },
    { outcomes: ["Heads", "Tails"], probabilities: [0.5, 0.5] }
  ]
  finalOutcomes: ["HH", "HT", "TH", "TT"]
  highlightPath: ["Heads", "Tails"]
```

**circle-diagram:**
```
VisualPlan:
  radius: 5
  diameter: 10
  circumference: "10π" or 31.4
  showCenter: true | false
  labeledParts: ["radius", "diameter", "circumference", "center"]
  unit: "cm" | "in" | "units"
```

**scale-drawing:**
```
VisualPlan:
  scaleFactor: "1 cm : 10 m" or "1:100"
  drawingMeasurements: [{ label: "length", value: 5, unit: "cm" }]
  actualMeasurements: [{ label: "length", value: 50, unit: "m" }]
  drawingType: "map" | "floor-plan" | "blueprint" | "other"
```

**scaled-figures:**
```
VisualPlan:
  originalDimensions: [{ label: "width", value: 4 }, { label: "height", value: 6 }]
  scaleFactor: 2.5
  copyDimensions: [{ label: "width", value: 10 }, { label: "height", value: 15 }]
  shapeType: "rectangle" | "triangle" | "polygon"
  showLabels: true | false
```

**other:** (custom diagrams)
```
VisualPlan:
  description: "[What the visual shows]"
  elements: ["element 1", "element 2", ...]
  labels: ["label 1", "label 2", ...]
  annotations: ["what to highlight or emphasize"]
```
**Note:** For custom diagrams, reference `reference/diagram-patterns.md` for SVG implementation patterns.

---

## Step 2.4: Update Progress File

After user confirms and scenarios are defined, update the progress file:

**File:** `src/app/presentations/{slug}/.worked-example-progress.json`

Update these fields:
```json
{
  "phase": 2,
  "phaseName": "Confirm & Plan",
  "userConfirmed": true,
  "scenarios": ["[Scenario 1 name]", "[Scenario 2 name]", "[Scenario 3 name]"],
  "totalSlides": [estimated count: 14-16],
  "updatedAt": "[ISO timestamp]"
}
```

Use the Read tool to read the current file, then use Edit to update only the changed fields.

---

## Phase 2 Completion Checklist

Before proceeding, verify:
- [ ] User has explicitly confirmed your understanding
- [ ] User has approved the **Diagram Evolution** (step-by-step visual progression)
- [ ] Three scenarios are defined
- [ ] All scenarios use the SAME strategy as the mastery check
- [ ] All scenarios have the SAME mathematical structure as the mastery check
- [ ] **ALL scenarios use DIFFERENT contexts from the mastery check**
- [ ] **ALL scenarios use DIFFERENT numbers from the mastery check**
- [ ] Each scenario has an engaging context and visual anchor
- [ ] Progress file updated with `userConfirmed: true` and `scenarios` array

---

## NEXT PHASE

**When Phase 2 is complete (user has confirmed):**

Use the Read tool to read the Phase 3 instructions:
```
Read: .claude/skills/create-worked-example-sg/phases/03-generate-slides/00-overview.md
```

Do NOT proceed to Phase 3 until the user has explicitly confirmed.
