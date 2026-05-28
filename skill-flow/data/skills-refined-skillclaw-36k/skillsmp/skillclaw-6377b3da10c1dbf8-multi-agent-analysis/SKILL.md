---
name: multi-agent-analysis
description: Use this skill when you need to conduct a comprehensive analysis of a problem by leveraging multiple agents to clarify questions, identify constraints, and propose solutions.
---

# Skill body

## Overview

This skill integrates the capabilities of multiple agents to analyze a problem from various perspectives, clarify ambiguities, and identify hidden assumptions. It is designed to facilitate thorough understanding and structured problem-solving.

## Steps

### Step 1: Clarification

1. **Receive the raw question** from the user.
2. **Restate the question** clearly and concisely (max 100 characters).
3. **Identify ambiguities** in the question (up to 3 points).
4. **Uncover hidden assumptions** that may not be explicitly stated (up to 3 assumptions).
5. **Assess cognitive biases** that may affect the question (up to 2 biases).
6. **Refine the question** based on the analysis.

### Step 2: Essence Analysis

1. **Identify the problem type** (e.g., resource allocation, timing decision).
2. **Determine the essence** of the problem in one sentence (max 50 characters).
3. **List immutable constraints** that cannot be changed (up to 5).
4. **Identify causal gears** that drive the problem (3-5 gears).
5. **Highlight the bottleneck gear** that is the most critical.
6. **Identify death traps** (actions to avoid) that could lead to failure (up to 3).

### Step 3: Implementation Recommendations

1. **Break down the implementation** into components, technologies, estimated efforts, and risks.
2. **Provide tool recommendations** based on the analysis.
3. **Identify integration points** necessary for the solution.
4. **Issue technical debt warnings** if applicable.

## Output Structure

The output should include:

- Restated question
- Identified ambiguities
- Hidden assumptions
- Cognitive biases
- Refined question
- Problem type
- Essence
- Immutable constraints
- Causal gears
- Bottleneck gear
- Death traps
- Implementation details
- Tool recommendations
- Integration points
- Technical debt warnings

## Example Usage

```json
{
  "raw_question": "How can we improve our user authentication process?",
  "constraints": ["Must comply with GDPR"],
  "stakeholders": ["Development Team", "Compliance Officer"]
}
```

This skill will provide a structured analysis and actionable recommendations based on the input provided.