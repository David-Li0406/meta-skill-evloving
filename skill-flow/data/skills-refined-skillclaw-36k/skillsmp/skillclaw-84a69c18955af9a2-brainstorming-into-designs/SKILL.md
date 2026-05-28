---
name: brainstorming-into-designs
description: Use this skill when creating or developing ideas into fully-formed designs through collaborative questioning, exploration of alternatives, and incremental validation.
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specifications through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## The Process

**Understanding the Idea:**

- Review the current project state (files, docs, recent commits) related to the idea.
- Ask questions one at a time to refine the idea.
- Prefer multiple choice questions when possible, but open-ended questions are acceptable.
- Focus on understanding: purpose, constraints, and success criteria.

**Exploring Approaches:**

- Propose 2-3 different approaches with trade-offs.
- Present options conversationally, leading with your recommended option and explaining your reasoning.

**Presenting the Design:**

- Once you believe you understand what you're building, present the design.
- Break it into sections of 200-300 words.
- After each section, ask if it looks right so far.
- Cover: architecture, components, data flow, error handling, and testing.
- Be ready to clarify if something doesn't make sense.

## After the Design

**Documentation:**

- Write the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`.
- Commit the design document to git.

**Implementation (if continuing):**

- Ask: "Ready to set up for implementation?"
- Create an isolated workspace for implementation.
- Create a detailed implementation plan.

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions.
- **Multiple choice preferred** - Easier to answer than open-ended when possible.
- **YAGNI ruthlessly** - Remove unnecessary features from all designs.
- **Explore alternatives** - Always propose 2-3 approaches before settling.
- **Incremental validation** - Present design in sections, validate each.
- **Be flexible** - Go back and clarify when something doesn't make sense.