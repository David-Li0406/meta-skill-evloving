---
name: spec-writer
description: Use this skill when you need to create a specification, gather requirements, or develop user stories through a structured discovery process that emphasizes understanding the problem space.
---

# Spec Writer

## Purpose

Guide users through creating complete, unambiguous feature specifications using a discovery-driven process. Unlike traditional requirements gathering that starts with predefined user stories, this skill helps stories emerge naturally from deep problem understanding. The resulting specification is comprehensive enough for implementation without further clarification.

## Core Philosophy

**Stories emerge from discovery, they don't precede it.**

Begin by understanding the problem space. Stories crystallize as understanding deepens through iterative exploration. Stories may split, merge, be added, or be revised as learning progresses—even after being written into the specification.

## When to Use This Skill

Use this skill when you need to:

- Transform a feature idea into a detailed specification
- Understand and document a problem before designing solutions
- Develop user stories through structured discovery
- Create implementation-ready requirements documentation
- Guide stakeholders through requirements clarification

## State Management Architecture

### The Compaction Mechanism

SPEC.md serves as the compaction mechanism. As user stories reach full clarity, they graduate from working state into the deliverable specification. STATE.md holds only in-flight work. SPEC.md is a living document—graduated stories can be revised when new information warrants it.

### Discovery Directory Structure

```
discovery/
├── SPEC.md            # Progressive deliverable (mutable)
├── STATE.md           # Working memory (current work)
├── OPEN_QUESTIONS.md  # Current blockers
└── archive/
    ├── DECISIONS.md   # Decision history
    ├── RESEARCH.md    # Research log
    ├── ITERATIONS.md   # Iteration summaries
    └── REVISIONS.md   # Changes to graduated stories
```

## Discovery Process Overview

### Phase 1: Problem Space Exploration

**Goal**: Understand the problem before proposing solutions.

**Activities**:
- Ask open-ended questions about the problem to gather insights.
- Document findings in the STATE.md to track evolving understanding.
- Identify key stakeholders and their perspectives on the problem.