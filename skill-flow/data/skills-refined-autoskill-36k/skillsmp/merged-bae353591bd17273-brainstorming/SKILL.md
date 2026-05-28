---
name: brainstorming
description: Use this skill before any creative work to explore user intent, requirements, and design before implementation.
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue. Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## The Process

### Understanding the Idea
- Review the current project state first (files, docs, recent commits) to ensure the design fits existing patterns and doesn't duplicate work.
- Ask questions one at a time to refine the idea, focusing on understanding: purpose, constraints, and success criteria.
- Prefer multiple choice questions when possible, but open-ended questions are also acceptable.
- Structure exploration into separate messages if multiple topics need investigation to avoid overwhelming the conversation.

### Exploring Approaches
- Propose 2-3 different approaches with trade-offs to explore the design space and prevent premature convergence on the first idea.
- Present options conversationally with your recommendation and reasoning, leading with your recommended option and explaining the trade-offs.

### Presenting the Design
- Verify you understand the full scope before presenting. Ask clarifying questions until you can describe what's being built with confidence.
- Present the design in reviewable sections (200-300 words each) and ask after each section whether it looks right so far.
- Cover architecture, components, data flow, error handling, and testing to avoid gaps later.
- Be ready to go back and clarify if something doesn't make sense.

## After the Design

### Next Steps
- You have a validated design/plan document. The user can choose their next step:
  - Create an OpenSpec proposal for formal specification.
  - Use the plan for implementation planning.
  - Continue refining the design if needed.
  - Save the plan for later reference.
- Ask the user what they'd like to do next.

## Key Principles
- **One question at a time**: Don't overwhelm with multiple questions.
- **Multiple choice preferred**: Easier to answer than open-ended when possible.
- **YAGNI ruthlessly**: Remove unnecessary features from all designs.
- **Explore alternatives**: Always propose 2-3 approaches before settling.
- **Incremental validation**: Present design in sections, validate each.
- **Be flexible**: Go back and clarify when something doesn't make sense.
- **Focus on patterns**: Ensure designs align with established patterns and standards.

## Integration
This skill is typically invoked by agents when requirements are unclear or when starting a new component. It can also be invoked directly for architectural decisions or when facing ambiguous requirements.