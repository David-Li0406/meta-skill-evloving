---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
license: MIT
compatibility: opencode
metadata:
  category: "design-and-planning"
  audience: "user-facing"
---

# Brainstorming Ideas Into Designs

## What I do
I help turn your ideas into fully formed designs and specifications through a natural, collaborative dialogue. I start by understanding the project context, ask clarifying questions, explore different approaches, and then present a detailed design for your validation.

## When to use me
You MUST use this skill before starting any creative or significant work, such as creating new features, building components, adding functionality, or modifying existing behavior. It is essential for exploring user intent, defining requirements, and creating a solid design before implementation begins.

## The Process

**1. Understanding the idea:**
- I'll start by checking the current project state (files, docs, recent commits).
- I will ask questions one at a time to refine the idea, preferring multiple-choice where possible.
- My focus is on understanding the purpose, constraints, and success criteria of your idea.

**2. Exploring approaches:**
- I will propose 2-3 different approaches with their trade-offs.
- I'll present these options conversationally, leading with my recommendation and explaining my reasoning.

**3. Presenting the design:**
- Once I understand what we're building, I'll present the design in small, digestible sections (200-300 words).
- After each section, I will ask for your feedback to ensure we are on the right track.
- The design will cover architecture, components, data flow, error handling, and testing strategy.

## After the Design

**Documentation:**
- First, I will confirm the project's preferred location for design documents. If one is found, I will use it. Otherwise, I will write the validated design to a new file at `docs/plans/YYYY-MM-DD-<topic>-design.md`.
- The document should be written clearly and concisely, so other developers can easily understand the plan.
- Finally, I will commit the design document to git.

**Implementation (if continuing):**
- I will ask: "Ready to set up for implementation?"
- If you agree, I will use the `using-git-worktrees` skill to create an isolated workspace.
- Then, I will use the `writing-plans` skill to create a detailed implementation plan.

## Key Principles
- **One question at a time**: To avoid overwhelming you.
- **Multiple choice preferred**: To make answering easier.
- **YAGNI ruthlessly**: I will challenge any feature that doesn't seem necessary.
- **Explore alternatives**: I will always propose and evaluate several approaches.
- **Incremental validation**: We'll confirm each part of the design together.
- **Be flexible**: I am ready to go back and clarify anything that isn't right.
