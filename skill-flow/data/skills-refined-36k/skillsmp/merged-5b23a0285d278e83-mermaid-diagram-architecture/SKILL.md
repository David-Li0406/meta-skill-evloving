---
name: mermaid-diagram-architecture
description: Use this skill when the user asks to create or update diagrams, including flowcharts, architecture diagrams, or any Mermaid diagrams, ensuring clarity and adherence to best practices.
---

# Mermaid Diagram and Architecture Standards

Create, edit, and validate Mermaid diagrams using the `mmdc` command-line tool while adhering to established standards for clarity and organization.

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

Replace `[uid]` with a short unique identifier (e.g., timestamp or random string).

### Step 2: Write Initial Diagram

Write the mermaid code to a temporary file:

```
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

```
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

Once approved, copy the final mermaid code to the target location (markdown file or standalone .mmd file).

## Workflow: Editing Existing Diagrams

### Step 1: Read Source File

Read the file containing the mermaid diagram. For markdown files, extract the content within the mermaid code fence:

````
```mermaid
... diagram code ...
```
````

### Step 2: Set Up Working Directory

Generate a unique session ID and create the working directory:

```bash
mkdir -p /tmp/claude/[uid]
```

### Step 3: Write to Working File

Write the extracted mermaid code to `/tmp/claude/[uid]/diagram.mmd`.

### Step 4: Validate, Inspect, and Iterate

Follow Steps 3-6 from "Creating New Diagrams" to validate, generate SVG, inspect, and refine the layout.

### Step 5: Update Original

Once approved, update the original source file with the improved diagram code.

## Diagram Standards

### Core Rules

- **Every Arrow Needs a Label**: Unlabeled arrows force readers to guess the relationship.
  
  ```mermaid
  %% BAD
  A --> B
  
  %% GOOD
  A -->|float[] samples| B
  ```

- **No Dead Ends**: Every process node needs input AND output arrows. Data doesn't disappear.

  ```mermaid
  %% BAD: normalize just ends
  RawData --> Normalize
  
  %% GOOD: show what normalized data becomes
  RawData -->|int16[]| Normalize -->|float[] peak=1.0| Smoother
  ```

- **Single Abstraction Level Per Diagram**: Don't mix high-level modules with implementation functions.

- **Connect All Subgraphs**: Isolated subgraphs indicate missing relationships.

### Arrow Conventions

Pick ONE meaning per diagram and state it in a legend or title:

| Arrow Type | Meaning | Use When |
|------------|---------|----------|
| `-->` | Data flows from A to B | Showing data transformation pipelines |
| `-.->` | Async/event-based | Callbacks, message queues |
| `==>` | High-volume/critical path | Emphasizing main data path |

### Required Elements

- **Legend**: Every diagram needs a legend explaining arrow meanings and any color coding.
- **Title**: Descriptive title that clarifies arrow semantics.

## Verification Checklist

Before finalizing any diagram:

- [ ] Every arrow has a label describing what flows/relationship.
- [ ] No orphaned nodes or subgraphs.
- [ ] Every process has both input and output arrows.
- [ ] Single abstraction level throughout.
- [ ] Legend explains arrow and shape meanings.
- [ ] Title clarifies diagram's semantic intent.

## Supported Diagram Types

| Type | Declaration | Use Case |
|------|-------------|----------|
| Flowchart | `flowchart TB` | Processes, workflows, decisions |
| Sequence | `sequenceDiagram` | API calls, interactions, messaging |
| State | `stateDiagram-v2` | State machines, lifecycles |
| Class | `classDiagram` | OOP structures, relationships |
| ER | `erDiagram` | Database schemas |
| Git | `gitGraph` | Branch histories |
| Pie | `pie` | Data distributions |
| Mindmap | `mindmap` | Brainstorming, hierarchies |

## Example: Complete Data Flow

```mermaid
flowchart LR
    subgraph Capture[Audio Capture]
        CB[Callback] -->|int16[] stereo| RB[(Ring Buffer)]
    end

    subgraph Process[Waveform Processing]
        RB -->|int16[4096]| Norm[Normalize]
        Norm -->|float[1024] peak=1.0| Smooth[Smooth]
        Smooth -->|float[2048] palindrome| Interp[CubicInterp]
    end

    subgraph Render[Visualization]
        Interp -->|Vector2[]| Draw[DrawCircular]
        Draw -->|pixels| Accum[(accumTexture)]
        Accum -->|texture| Blur[Gaussian Blur]
        Blur -->|decayed texture| Accum
        Accum -->|final frame| Screen[Display]
    end

%% Legend:
%% → data flow with payload type
%% [(name)] persistent buffer
%% [name] processing function
```