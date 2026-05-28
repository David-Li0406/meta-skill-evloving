---
name: brainstorming
description: Turn ideas into fully formed designs through collaborative dialogue, memory context, and targeted research.
metadata:
   source: https://skills.sh/obra/superpowers/brainstorming
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

**User Idea:** $ARGUMENTS

## Skills

Load the following skills:
- `memory`
- `spawn-subagent`
- `design-to-proposal`

## The Process

**Understanding the idea:**
- Read memory context first, then check current project state (files, docs, recent commits)
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria
- If external documentation about a library, tool, framework, API, or any other technical topic could be relevant, spawn the Research subagent to research the topic and present the findings.  Do not research the topic yourself.

**Exploring approaches:**
- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why
- If codebase context (existing patterns, dependencies, structure) is needed, spawn the Explore subagent to gather it.

**Presenting the design:**
- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense

## Subagent Spawning

- Subagents spawn in a fresh context; include all necessary background and constraints.
- Spawn Research when external documentation would improve accuracy or completeness.
- Spawn Explore when codebase context (existing patterns, dependencies, structure) is required.

**Research subagent prompt template:**
- **Query**: [Specific question to answer]
- **Context**: [Project details, current idea, why research is needed]
- **Constraints**: [Scope, do not modify code, cite sources if available]

**Explore subagent prompt template:**
- **What to find**: [Files, patterns, APIs, conventions]
- **Scope**: [Directories or areas to search]
- **Constraints**: [No changes, summarize findings]

## Output

- Write the final design to `.workflow/designs/<feature-slug>/design.md`.
- Create `<feature-slug>` from the design title using kebab-case.
- Use `.workflow/designs/TEMPLATE.md` as the starting point and populate all relevant sections.

After the design is finalized prompt: "Would you like to create an OpenSpec proposal from this design?"
	- If the user opts in, invoke the `design-to-proposal` skill.
	- If the user opts out, STOP and remind them they can run `/propose <design-path>` later.

## Workflow Steps

1. Read memory for relevant past designs/decisions/patterns.
2. Ask clarifying questions one at a time; spawn Research if external docs could help.
3. Explore approaches; spawn Explore if codebase context is needed.
4. Draft and validate the design in sections with user feedback.
5. Write final design to `.workflow/designs/<feature-slug>/design.md`.
6. Optionally create an OpenSpec proposal from the design (see Output).
7. Use the `memory` skill to determine if memories should be captured.
