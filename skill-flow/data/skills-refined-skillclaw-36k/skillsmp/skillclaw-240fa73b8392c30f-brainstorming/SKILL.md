---
name: brainstorming
description: Use this skill before any creative work to explore user intent, requirements, and design options before implementation.
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specifications through natural collaborative dialogue. Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## The Process

**Understanding the Idea:**
- Review the current project state (files, docs, recent commits) to ensure the design fits existing patterns.
- Ask questions one at a time to clarify the idea, focusing on purpose, constraints, and success criteria.
- Prefer multiple choice questions when possible, but open-ended questions are acceptable as well.

**Exploring Approaches:**
- Propose 2-3 different approaches with trade-offs to explore the design space.
- Present options conversationally, leading with your recommended option and explaining the reasoning behind it.

**Presenting the Design:**
- Once you believe you understand what you're building, present the design in sections of 200-300 words.
- After each section, confirm with the user whether it looks right so far.
- Cover aspects such as architecture, components, data flow, error handling, and testing.

## After the Design

**Documentation:**
- Write the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`.
- Commit the design document to version control.

**Implementation (if continuing):**
- Ask, "Ready to set up for implementation?"
- Use appropriate tools to create an isolated workspace and detailed implementation plan.

## Key Principles
- **One Question Per Turn:** Avoid overwhelming the user with multiple questions.
- **Explore Before Committing:** Always propose multiple approaches before settling on one.
- **Incremental Validation:** Present designs in digestible sections and confirm understanding.
- **YAGNI Ruthlessly:** Remove unnecessary features to keep the design simple.
- **Context Determines Mode:** Adapt the approach based on the context of the discussion.