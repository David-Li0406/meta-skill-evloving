---
name: multi-ai-design-assistance
description: Use this skill when you need diverse perspectives from different AI models to enhance decision-making in complex design judgments or troubleshooting difficult problems.
---

# Skill body

## Overview

This skill allows you to leverage insights from multiple AI models (e.g., OpenAI Codex and Google Gemini) to improve the accuracy of your design decisions and problem-solving processes.

## When to Use

Automatically activate this skill in the following situations:

1. **When you are uncertain in design decisions**
   - Multiple approaches exist, and it's challenging to determine the optimal one.
   - You lack confidence in evaluating trade-offs.

2. **When you encounter difficult problems**
   - Debugging has stalled.
   - Identifying the root cause is taking too long.
   - All attempted solutions have failed.

3. **When making significant decisions**
   - Selecting architecture.
   - Judging disruptive changes.
   - Implementing security-related features.

## How to Use

### 1. Clearly articulate the problem

Include the following in your prompt to the AI models:

- Current situation and context.
- What you have tried and considered.
- Specific points where you need opinions.

### 2. Start a session with each AI model

For OpenAI Codex:

```bash
mcp__codex__codex({
  prompt: "Describe the problem and your questions",
  cwd: "working-directory",
  sandbox: "read-only"  // Default is read-only
})
```

For Google Gemini:

```bash
gemini "Describe the problem and your questions"
```

### 3. Integrate insights from both models

After receiving responses:

- Compare the insights from both models.
- Analyze commonalities and differences.
- Derive a final decision based on the integrated perspectives.

## Prompt Templates

### Design Decision

```
I am considering the implementation of [feature name].

Context:
- [Technology stack, constraints]

Approaches under consideration:
A) [Approach A]
B) [Approach B]

My current thoughts:
- [Analysis from one AI model]

Please provide insights on:
- Are there any overlooked risks?
- Is there a better approach?
- Considerations for long-term maintainability.
```

### Troubleshooting Difficult Problems

```
I am stuck on the following issue.

Symptoms:
- [Error messages, behaviors]

What I have tried:
1. [Attempt 1] → [Result]
2. [Attempt 2] → [Result]

Related code:
[Code snippet or file content]

Please suggest an alternative investigation approach.
```

## Notes

- Treat the opinions from both AI models as reference information.
- The final decision should be made by the user.
- If the opinions differ, analyze the reasons and present them to the user for clarity.