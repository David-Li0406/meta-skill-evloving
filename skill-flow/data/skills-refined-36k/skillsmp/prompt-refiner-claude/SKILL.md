---
name: prompt-refiner-claude
description: Refine prompts for Claude models (Opus, Sonnet, Haiku) using Anthropic's best practices. Use when preparing complex tasks for Claude.
---

# Claude Prompt Refiner

## When to Use
Invoke this skill when you have a task for Claude that:
- Involves multiple steps or files
- Requires specific output formatting
- Needs careful reasoning or analysis
- Would benefit from structured context

## Refinement Process

### 1. Analyze the Draft Prompt
Review the user's prompt for:
- [ ] Clear outcome definition
- [ ] Sufficient context
- [ ] Explicit constraints
- [ ] Success criteria

### 2. Apply Claude-Specific Patterns

**Structure with XML tags:**
- `<context>` - Background information, codebase state
- `<task>` - The specific action to take
- `<requirements>` - Must-have criteria
- `<constraints>` - Limitations and boundaries
- `<examples>` - Sample inputs/outputs if helpful

**Ordering matters:**
1. Context first (what exists)
2. Task second (what to do)
3. Requirements third (how to do it)
4. Examples last (clarifying edge cases)

### 3. Enhance for Reasoning
For complex tasks, add:
- "Think through the approach before implementing"
- "Consider these edge cases: ..."
- "Explain your reasoning for key decisions"

### 4. Output the Refined Prompt
Present the improved prompt with:
- Clear section headers
- XML tags where beneficial
- Specific, measurable criteria

## Example Transformation

**Before:**
"Add caching to the API"

**After:**