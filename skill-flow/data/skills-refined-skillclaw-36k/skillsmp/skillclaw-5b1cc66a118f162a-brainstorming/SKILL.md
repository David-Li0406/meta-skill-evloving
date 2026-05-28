---
name: brainstorming
description: Use this skill when you have rough ideas that need design before coding or when multiple approaches exist and need evaluation.
---

# Skill body

## Objective
Turn rough ideas into fully-formed designs through natural collaborative dialogue. Understand the context, explore alternatives, and validate incrementally.

## When to Use
Use brainstorming when:
- You have a rough idea but unclear implementation.
- Multiple approaches exist and you need to choose.
- Requirements are fuzzy or incomplete.
- Design decisions need validation before coding.

**Skip** for clear mechanical tasks with obvious solutions, well-defined requirements with standard implementations, or simple bug fixes.

## Understanding Context
1. Explore the current project state by checking existing files, documentation, and recent commits to understand what's already built.
2. Ask questions one at a time to refine the idea. Use multiple choice when possible to make it easier to answer.
3. Focus on understanding:
   - Purpose: What problem does this solve?
   - Constraints: What limits the solution?
   - Success criteria: How do we know it works?
4. One question per message. If a topic needs more exploration, break it into multiple questions to avoid overwhelming the participant.

## Exploring Alternatives
1. Propose different approaches with their tradeoffs. Present options conversationally, showing all options first before making a recommendation.
2. Example pattern:
   - "I see three main approaches:
     1. Direct integration - Fast to implement but creates coupling. Good if this is temporary.
     2. Event-driven - More flexible, better separation, but adds complexity. Worth it if we'll extend this.
     3. Separate service - Maximum isolation, easier to scale, but operational overhead. Overkill unless we need independent scaling.
   - I'd recommend #2 (event-driven) because the requirements suggest we'll add features here, and the loose coupling will make that easier. What do you think?"
3. Make a clear recommendation by picking one approach and explaining why it fits best. Avoid hedging or suggesting hybrid approaches.