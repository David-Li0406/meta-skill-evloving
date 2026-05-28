---
name: brainstorming
description: Use this skill when creating or developing anything, before writing code or implementation plans, to refine rough ideas into fully-formed designs through structured questioning, alternative exploration, and incremental validation.
---

# Brainstorming Ideas Into Designs

## Overview

Transform rough ideas into fully-formed designs through structured questioning and alternative exploration.

**Core principle:** Ask questions to understand, explore alternatives, and present design incrementally for validation.

**Announce at start:** "🔧 Using Skill: brainstorming | I'm refining your idea into a design."

## Quick Reference

| Phase | Key Activities | Tool Usage | Output |
|-------|---------------|------------|--------|
| **1. Understanding** | Ask questions (one at a time) | AskUserQuestion for choices | Purpose, constraints, criteria |
| **2. Exploration** | Propose 2-3 approaches | AskUserQuestion for approach selection | Architecture options with trade-offs |
| **3. Design Presentation** | Present in 200-300 word sections | Open-ended questions | Complete design with validation |
| **4. Worktree Setup** | Set up isolated workspace | using-git-worktrees skill | Ready development environment |
| **5. Planning Handoff** | Create implementation plan | writing-plans skill | Detailed task breakdown |

## The Process

Copy this checklist to track progress:

```
Brainstorming Progress:
- [ ] Phase 1: Understanding (purpose, constraints, criteria gathered)
- [ ] Phase 2: Exploration (2-3 approaches proposed and evaluated)
- [ ] Phase 3: Design Presentation (design validated in sections)
- [ ] Phase 4: Worktree Setup (if implementing)
- [ ] Phase 5: Planning Handoff (if implementing)
```

### Phase 1: Understanding
- Check current project state in working directory.
- Ask ONE question at a time to refine the idea.
- **Use AskUserQuestion tool** when you have multiple choice options.
- Gather: Purpose, constraints, success criteria.

### Phase 2: Exploration
- Propose 2-3 different approaches.
- For each: Core architecture, trade-offs, complexity assessment.
- **Use AskUserQuestion tool** to present approaches as structured choices.

### Phase 3: Design Presentation
- Present in 200-300 word sections.
- Cover: Architecture, components, data flow, error handling, testing.
- Ask after each section: "Does this look right so far?"

### Phase 4: Worktree Setup (for implementation)
When design is approved and implementation will follow:
- Announce: "I'm using the Using Git Worktrees skill to set up an isolated workspace."
- Follow that skill's process for directory selection, safety verification, and setup.

### Phase 5: Planning Handoff
Ask: "Ready to create the implementation plan?"
When your human partner confirms (any affirmative response):
- Announce: "I'm using the Writing Plans skill to create the implementation plan."
- Create detailed plan in the worktree.

## When to Revisit Earlier Phases
You can and should go backward when:
- New constraints are revealed during Phase 2 or 3.
- Validation shows fundamental gaps in requirements.
- Questions arise about the approach during Phase 3.
- Something doesn't make sense and needs clarification.

## Remember
- One question per message during Phase 1.
- Apply YAGNI ruthlessly.