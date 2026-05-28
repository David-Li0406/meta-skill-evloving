---
name: sequential-thinking
description: Use this skill when complex problems require systematic step-by-step reasoning, allowing for revision and exploration of alternative approaches.
---

# Sequential Thinking

## Trigger Phrases

Activate when user says:
- "think through this step by step", "break this down", "reason through"
- "complex problem", "multi-step analysis", "decompose this"
- "let me think about", "need to work through", "figure out"
- "sequential reasoning", "structured thinking", "systematic analysis"
- "consider alternatives", "branch the approach", "revise my thinking"
- "unclear scope", "explore options", "iterative reasoning"

## Core Capabilities

- **Iterative reasoning**: Break complex problems into sequential thought steps.
- **Dynamic scope**: Adjust total thought count as understanding evolves.
- **Revision tracking**: Reconsider and modify previous conclusions.
- **Branch exploration**: Explore alternative reasoning paths from any point.
- **Maintained context**: Keep track of reasoning chain throughout analysis.

## When to Use

Use `mcp__reasoning__sequentialthinking` when:
- The problem requires multiple interconnected reasoning steps.
- The initial scope or approach is uncertain.
- You need to filter through complexity to find core issues.
- You may need to backtrack or revise earlier conclusions.
- You want to explore alternative solution paths.

**Don't use for**: Simple queries, direct facts, or single-step tasks.

## Basic Usage

The MCP tool `mcp__reasoning__sequentialthinking` accepts these parameters:

### Required Parameters

- `thought` (string): Current reasoning step.
- `nextThoughtNeeded` (boolean): Whether more reasoning is needed.
- `thoughtNumber` (integer): Current step number (starts at 1).
- `totalThoughts` (integer): Estimated total steps needed.

### Optional Parameters

- `isRevision` (boolean): Indicates this revises previous thinking.
- `revisesThought` (integer): Which thought number is being reconsidered.
- `branchFromThought` (integer): Thought number to branch from.
- `branchId` (string): Identifier for this reasoning branch.

## Workflow Pattern

```
1. Start with initial thought (thoughtNumber: 1).
2. For each step:
   - Express current reasoning in `thought`.
   - Estimate remaining thoughts needed.
   - Adjust `totalThoughts` as understanding evolves.
   - If revising, indicate with `isRevision` and specify `revisesThought`.
   - If branching, specify `branchFromThought` and `branchId`.
```