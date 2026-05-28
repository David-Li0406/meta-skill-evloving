---
name: brainstorming
description: Collaborative idea refinement - turns rough ideas into fully-formed designs through questioning, alternative exploration, and incremental validation. Use before writing code or implementation plans.
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## The Process

### Phase 1: Understanding the Idea

- Check the current project state first (files, docs, recent commits)
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

### Phase 2: Exploring Approaches

- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

### Phase 3: Presenting the Design

- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## After the Design

### Documentation

- Write the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Use clear, concise language
- Commit the design document to git

### Implementation (if continuing)

- Ask: "Ready to set up for implementation?"
- If yes, create a detailed implementation plan in `docs/plans/YYYY-MM-DD-<topic>-implementation.md`
- Break down into small, testable tasks
- Commit the implementation plan

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense

## Design Document Template

When writing the design document, use this structure:

```markdown
# <Topic> Design Document

**Date**: YYYY-MM-DD
**Status**: Draft | Approved
**Author**: Brainstorming session

---

## Overview

<1-2 sentence summary>

## Problem Statement

<What problem are we solving?>

## Goals & Non-Goals

**Goals:**
- ...

**Non-Goals:**
- ...

## Design

### Architecture

<High-level architecture>

### Components

<Key components and responsibilities>

### Data Flow

<How data moves through the system>

## Implementation Plan

<High-level steps>

## Testing Strategy

<How we'll verify correctness>

## Open Questions

<Unresolved decisions>
```
