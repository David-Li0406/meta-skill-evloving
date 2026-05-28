---
title: Agentic Prompt Engineering Best Practices
description: Comprehensive guide to prompt engineering principles for modern LLMs including long-horizon reasoning, state management, and communication style optimization
keywords: prompt engineering, agentic workflows, long-horizon tasks, state tracking, context awareness
skill: crafting-agentic-prompts
---

# Agentic Prompt Engineering Best Practices

This guide provides specific prompt engineering techniques for modern language models to help achieve optimal results in agentic applications. These principles are designed for models trained for precise instruction following and tool use capabilities.

## General Principles

### Be explicit with your instructions

Modern language models respond well to clear, explicit instructions. Being specific about desired output can help enhance results. Models that have strong reasoning capabilities may benefit from explicit requests for additional features or behaviors.

**Example: Creating an analytics dashboard**

**Less effective:**
```text
Create an analytics dashboard
```

**More effective:**
```text
Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation.
```

### Add context to improve performance

Providing context or motivation behind instructions, such as explaining why a behavior is important, can help models better understand goals and deliver more targeted responses.

**Example: Formatting preferences**

**Less effective:**
```text
NEVER use ellipses
```

**More effective:**
```text
The response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them.
```

### Be vigilant with examples & details

Modern language models pay close attention to details and examples as part of their instruction following capabilities. Ensure that examples align with the behaviors you want to encourage and minimize behaviors you want to avoid.

### Long-Horizon Reasoning and State Tracking

Advanced models maintain orientation across extended sessions through incremental progress. Key capability: work on complex task, save state, continue with fresh context.

**Context Awareness:** Some models track remaining token budget. If using auto-compaction or external file saving:

```text
Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off. Therefore, do not stop tasks early due to token budget concerns. As you approach your token budget limit, save your current progress and state to memory before the context window refreshes. Always be as persistent and autonomous as possible and complete tasks fully, even if the end of your budget is approaching. Never artificially stop any task early regardless of the context remaining.
```

**Multi-Context Window Workflows:**

| Pattern | Implementation |
|---------|---------------|
| First window setup | Write tests, create setup scripts, establish framework |
| Structured test tracking | Use `tests.json` format. Remind: "Unacceptable to remove/edit tests" |
| QoL tools | Create `init.sh` for servers/tests/linters |
| Fresh start protocol | "Call pwd; review progress.txt, tests.json, git logs; run integration test" |
| Verification tools | Browser automation, computer use for UI testing |
| Context efficiency | "Encouraged to spend entire output context; don't run out with uncommitted work" |

**State Management Best Practices:**

| Technique | Use Case | Format |
|-----------|----------|--------|
| Structured formats | Test results, task status | JSON with schema |
| Unstructured notes | General progress, context | Freeform text |
| Git tracking | History, checkpoints | Commit logs |
| Incremental focus | Long tasks | Explicit progress tracking |

**State Tracking Examples:**

```json
// Structured state file (tests.json)
{
  "tests": [
    {"id": 1, "name": "authentication_flow", "status": "passing"},
    {"id": 2, "name": "user_management", "status": "failing"},
    {"id": 3, "name": "api_endpoints", "status": "not_started"}
  ],
  "total": 200,
  "passing": 150,
  "failing": 25,
  "not_started": 25
}
```

```text
// Progress notes (progress.txt)
Session 3 progress:
- Fixed authentication token validation
- Updated user model to handle edge cases
- Next: investigate user_management test failures (test #2)
- Note: Do not remove tests as this could lead to missing functionality
```

### Communication Style Control

| Model Behavior | Pattern | Adjustment Needed |
|----------------|---------|-------------------|
| Silent after tool use | Efficiency-focused | Add: "Provide quick summary after tool use" |
| Verbose explanations | Conversational | Add: "Be concise, focus on results" |
| Balanced | Default | No adjustment needed |

## Guidance for Specific Situations

### Verbosity and Action Control

| Issue | Symptom | Solution |
|-------|---------|----------|
| Too quiet | Skips summaries after tool use | Add: "Provide quick summary after tool use" |
| Too verbose | Excessive explanations | Add: "Be concise, focus on results" |
| Only suggests | Says "Can you..." instead of acting | Use imperative: "Change this function..." not "Can you suggest..." |
| Too proactive | Acts without confirmation | Add conservativeness prompt (below) |

**Make Agent More Proactive:**

```xml
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's intent is unclear, infer the most useful likely action and proceed, using tools to discover any missing details instead of guessing. Try to infer the user's intent about whether a tool call (e.g., file edit or read) is intended or not, and act accordingly.
</default_to_action>
```

**Make Agent More Conservative:**

```xml
<do_not_act_before_instructions>
Do not jump into implementation or change files unless clearly instructed to make changes. When the user's intent is ambiguous, default to providing information, doing research, and providing recommendations rather than taking action. Only proceed with edits, modifications, or implementations when the user explicitly requests them.
</do_not_act_before_instructions>
```

### Output Format Control

| Technique | Example |
|-----------|---------|
| Positive framing | "Write smoothly flowing prose" not "Don't use markdown" |
| XML tags | "Write in \<smoothly\_flowing\_prose\_paragraphs> tags" |
| Style matching | Remove markdown from prompt to reduce markdown in output |
| Detailed guidance | Use explicit formatting instructions (below) |

````xml
<avoid_excessive_markdown_and_bullet_points>
When writing reports, documents, technical explanations, analyses, or any long-form content, write in clear, flowing prose using complete paragraphs and sentences. Use standard paragraph breaks for organization and reserve markdown primarily for `inline code`, code blocks (```...```), and simple headings (###, and ###). Avoid using **bold** and *italics*.

DO NOT use ordered lists (1. ...) or unordered lists (*) unless : a) you're presenting truly discrete items where a list format is the best option, or b) the user explicitly requests a list or ranking

Instead of listing items with bullets or numbers, incorporate them naturally into sentences. This guidance applies especially to technical writing. Using prose instead of excessive formatting will improve user satisfaction. NEVER output a series of overly short bullet points.

Your goal is readable, flowing text that guides the reader naturally through ideas rather than fragmenting information into isolated points.
</avoid_excessive_markdown_and_bullet_points>
````

### Research and Information Gathering

**Best Practices:**

| Practice | Implementation |
|----------|---------------|
| Success criteria | Define what constitutes successful answer |
| Source verification | Verify across multiple sources |
| Structured approach | Use competing hypotheses, confidence tracking, hypothesis tree, progress notes |

**Complex Research Prompt:** "Search systematically. Develop competing hypotheses. Track confidence levels. Self-critique regularly. Update hypothesis tree for transparency."

### Subagent Orchestration

Advanced models orchestrate subagents natively when tools are well-defined. Let model delegate naturally; add conservativeness if needed: "Only delegate when task clearly benefits from separate context window."

### Model Self-Knowledge and Thinking

| Pattern | Implementation |
|---------|---------------|
| Model identity | "The assistant is [Model Name]. Current model is [Version]" |
| LLM app defaults | "Default to [Model Name] unless requested. Model string: [identifier]" |
| Enhanced reflection | "After tool results, reflect on quality, plan next steps, take best action" |

### Document Creation

For polished presentations with creative flair: "Create professional presentation on [topic]. Include design elements, visual hierarchy, engaging animations."

### Parallel Tool Calling

Models may run multiple speculative searches, read files simultaneously, execute commands in parallel. Easily steerable:

```xml
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel. Prioritize calling tools simultaneously whenever the actions can be done in parallel rather than sequentially. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. Maximize use of parallel tool calls where possible to increase speed and efficiency. However, if some tool calls depend on previous calls to inform dependent values like the parameters, do NOT call these tools in parallel and instead call them sequentially. Never use placeholders or guess missing parameters in tool calls.
</use_parallel_tool_calls>
```

**Reduce parallel execution:** "Execute operations sequentially with brief pauses for stability."

### Coding Best Practices

| Issue | Guidance |
|-------|----------|
| Temporary files | Models may create scratchpad files. To minimize: "Clean up temporary files at task end" |
| Test-focused coding | Avoid hard-coding. Prompt: "Write general solution for all inputs, not just test cases. Implement actual logic, not workarounds" |
| Hallucinations | "Never speculate about unopened code. Read files before answering. Give grounded answers" |

### Frontend and UI Generation

**Techniques for Exceptional UIs:**

| Technique | Example Prompt |
|-----------|---------------|
| Explicit encouragement | "Don't hold back. Create impressive demonstration showcasing capabilities" |
| Aesthetic direction | "Dark blue/cyan palette, Inter typography, card layouts, hover states, micro-interactions" |
| Design diversity | "Multiple options. Fusion aesthetics. Avoid generic centered layouts, simplistic gradients" |
| Feature completeness | "Include all relevant features, animations, interactions. Fully-featured implementation" |

## Best Practices Summary

| Principle | Implementation |
|-----------|---------------|
| Explicit behavior | Describe exact desired output |
| Quality modifiers | "Include many features and interactions. Go beyond basics" |
| Feature requests | Explicitly request animations, interactions, completeness |
| Context provision | Explain why behaviors matter |
| Structured tasks | Break down long-horizon with state management, verification |
