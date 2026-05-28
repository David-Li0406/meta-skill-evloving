---
name: brainstorming-ideas-into-designs
description: Use this skill when a partner describes any feature or project idea, to refine it into a fully-formed design before writing code or implementation plans.
---

# Brainstorming Ideas Into Designs

## Overview

Transform rough ideas into fully-formed designs through structured questioning and alternative exploration.

**Core principle:** Ask questions to understand, explore alternatives, and present design incrementally for validation.

**Announce at start:** "I'm using the Brainstorming skill to refine your idea into a design."

## The Process

### Phase 1: Understanding
- Check the current project state in the working directory.
- Ask ONE question at a time to refine the idea.
- Prefer multiple choice when possible.
- Gather: Purpose, constraints, success criteria.

### Phase 2: Exploration
- Propose 2-3 different approaches.
- For each approach, cover: Core architecture, trade-offs, complexity assessment.
- Ask your human partner which approach resonates.

### Phase 3: Design Presentation
- Present in 200-300 word sections.
- Cover: Architecture, components, data flow, error handling, testing.
- Ask after each section: "Does this look right so far?"

### Phase 4: Worktree Setup (for implementation)
When the design is approved and implementation will follow:
- Announce: "I'm using the Using Git Worktrees skill to set up an isolated workspace."
- Switch to the Using Git Worktrees skill.
- Follow that skill's process for directory selection, safety verification, and setup.
- Return here when the worktree is ready.

### Phase 5: Planning Handoff
Ask: "Ready to create the implementation plan?"

When your human partner confirms (any affirmative response):
- Announce: "I'm using the Writing Plans skill to create the implementation plan."
- Switch to the Writing Plans skill.
- Create a detailed plan in the worktree.

## When to Revisit Earlier Phases

**Go backward when:**
- Partner reveals new constraints during Phase 2 or 3 → Return to Phase 1 to understand it.
- Validation shows a fundamental gap in requirements → Return to Phase 1.
- Partner questions the approach during Phase 3 → Return to Phase 2 to explore alternatives.
- Something doesn't make sense → Go back and clarify.

**Don't force forward linearly** when going backward gives better results.