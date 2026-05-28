---
name: multi-ai-perspective-assessment
description: Use this skill when facing complex design decisions or challenging problems, where insights from different AI models can enhance your understanding and decision-making.
---

# Multi-AI Perspective Assessment

This skill leverages insights from different AI models (OpenAI Codex and Google Gemini) to improve the accuracy of your thought process.

## When to Use

This skill automatically activates in the following situations:

1. **When uncertain about design decisions**
   - Multiple approaches exist, and it's difficult to determine the optimal one.
   - Lacking confidence in evaluating trade-offs.

2. **When encountering challenging problems**
   - Debugging has stalled.
   - Identifying the root cause is taking too long.
   - All attempted approaches have failed.

3. **When making important decisions**
   - Selecting architecture.
   - Judging disruptive changes.
   - Implementing security-related features.

## How to Use

### 1. Clearly articulate the problem

Include the following in the prompt for the AI models:

- Current situation and context.
- What has been tried and considered.
- Specific points where you seek opinions.

### 2. Start a session with the AI models

For Codex, use the following command:

```
mcp__codex__codex({
  prompt: "Describe the problem and ask your question",
  cwd: "working directory",
  sandbox: "read-only"  // Default is read-only
})
```

For Gemini, use the basic command:

```bash
gemini "Your prompt here"
```

### 3. Integrate insights from both models

After receiving responses from both Codex and Gemini:

- Compare the insights from both models.
- Analyze commonalities and differences.
- Derive a final judgment based on the analysis.

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
- [Analysis from Claude Code]

Please provide insights on:
- Are there any overlooked risks?
- Is there a better approach?
- Considerations for long-term maintainability.
```

### Challenging Problem

```
I am stuck on the following problem.

Symptoms:
- [Error messages, behaviors]

What I have tried:
1. [Attempt 1] → [Result]
2. [Attempt 2] → [Result]

Related code:
[Code snippet or file content]

Please suggest an alternative investigation approach.
```

## Important Notes

- Treat the opinions from both Codex and Gemini as reference information.
- The final judgment should be made by the user.
- If the opinions differ, analyze the reasons and present them to the user for clarity.