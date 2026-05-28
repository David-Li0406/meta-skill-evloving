---
name: mermaid-diagram-creation
description: Use this skill when you need to create, edit, or validate Mermaid diagrams for various purposes, including flowcharts, architecture diagrams, and sequence diagrams.
---

# Skill body

## Core Principles

1. **Always validate syntax** - Run `mmdc` to check syntax before considering a diagram complete.
2. **Always inspect visually** - Read the generated SVG to evaluate node arrangement.
3. **Always get user approval** - Open the SVG for user review before finalizing.
4. **Prioritize clarity** - Diagrams are for humans; organized layouts matter.

## Workflow: Creating New Diagrams

### Step 1: Set Up Working Directory

Generate a unique session ID and create the working directory:

```bash
mkdir -p /tmp/claude/[uid]
```

Replace `[uid]` with a short unique identifier (e.g., timestamp or random string like `mmd-20241219-abc123`).

### Step 2: Write Initial Diagram

Write the mermaid code to a temporary file:

```bash
/tmp/claude/[uid]/diagram.mmd
```

### Step 3: Validate and Generate SVG

Run the Mermaid CLI to validate syntax and generate output:

```bash
mmdc -i /tmp/claude/[uid]/diagram.mmd -o /tmp/claude/[uid]/diagram.svg -w 4096
```

If syntax errors occur, analyze the error message, fix the mermaid code, and retry.

### Step 4: Inspect the SVG

Use the Read tool to examine the generated SVG file:

```bash
Read /tmp/claude/[uid]/diagram.svg
```

Evaluate the diagram for:
- Node positioning and flow direction
- Edge crossings (minimize these)
- Grouping of related elements
- Overall readability and organization

### Step 5: Iterate on Layout

If the layout is chaotic or unclear, refactor the diagram:
- Reorder node declarations (affects layout order)
- Change direction (TB, LR, RL, BT)
- Add subgraphs to group related nodes
- Simplify complex connections

Repeat Steps 2-4 until the diagram is well-organized.

### Step 6: User Review

Request permission to open the SVG for user inspection:

```bash
open /tmp/claude/[uid]/diagram.svg
```

Wait for user confirmation or feedback. If changes are requested, iterate on the diagram.

### Step 7: Finalize

Once approved, copy the final mermaid code to the target location.

## Diagram Standards

### Every Arrow Needs a Label

Unlabeled arrows force readers to guess the relationship.

```mermaid
%% BAD
A --> B

%% GOOD
A -->|float[] samples| B
A -->|HTTP 200| B
A -->|calls| B
```

### No Dead Ends

Every process node needs input AND output arrows. Data doesn't disappear.

```mermaid
%% BAD: normalize just ends
RawData --> Normalize

%% GOOD: show what normalized data becomes
RawData -->|int16[]| Normalize -->|float[] peak=1.0| Smoother
```

### Single Abstraction Level Per Diagram

Don't mix high-level modules with implementation functions. Create separate diagrams for each level.

### Connect All Subgraphs

Isolated subgraphs indicate missing relationships. If a subgraph modifies data elsewhere, show the arrow.

### Arrow Conventions

Pick ONE meaning per diagram and state it in a legend or title.

### Required Elements

Every diagram needs a legend explaining:
- Arrow meaning (data flow vs dependency)
- Shape meanings if non-obvious
- Any color coding