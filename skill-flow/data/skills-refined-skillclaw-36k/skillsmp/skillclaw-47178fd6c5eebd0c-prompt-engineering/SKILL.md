---
name: prompt-engineering
description: Use this skill when you want to improve prompts, learn prompting strategies, or debug agent behavior with advanced techniques.
---

# Prompt Engineering Patterns

Advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability.

## Core Capabilities

### 1. Few-Shot Learning

Teach the model by showing examples instead of explaining rules. Include 2-5 input-output pairs that demonstrate the desired behavior. Use when you need consistent formatting, specific reasoning patterns, or handling of edge cases. More examples improve accuracy but consume tokens—balance based on task complexity.

**Example:**

```markdown
Extract key information from support tickets:

Input: "My login doesn't work and I keep getting error 403"
Output: {"issue": "authentication", "error_code": "403", "priority": "high"}

Input: "Feature request: add dark mode to settings"
Output: {"issue": "feature_request", "error_code": null, "priority": "low"}

Now process: "Can't upload files larger than 10MB, getting timeout"
```

### 2. Chain-of-Thought Prompting

Request step-by-step reasoning before the final answer. Add "Let's think step by step" (zero-shot) or include example reasoning traces (few-shot). Use for complex problems requiring multi-step logic, mathematical reasoning, or when you need to verify the model's thought process. Improves accuracy on analytical tasks by 30-50%.

**Example:**

```markdown
Analyze this bug report and determine root cause.

Think step by step:

1. What is the expected behavior?
2. What is the actual behavior?
3. What changed recently that could cause this?
4. What components are involved?
5. What is the most likely root cause?

Bug: "Users can't save drafts after the cache update deployed yesterday"
```

### 3. Prompt Optimization

Systematically improve prompts through testing and refinement. Start simple, measure performance (accuracy, consistency, token usage), then iterate. Test on diverse inputs including edge cases. Use A/B testing to compare variations. Critical for production prompts where consistency and cost matter.

**Example:**

```markdown
Version 1 (Simple): "Summarize this article"
→ Result: Inconsistent length, misses key points

Version 2 (Add constraints): "Summarize in 3 bullet points"
→ Result: Better structure, but still misses nuance

Version 3 (Add reasoning): "Identify the 3 main findings, then summarize."
```