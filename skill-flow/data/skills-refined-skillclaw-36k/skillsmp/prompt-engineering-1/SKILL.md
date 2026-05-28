---
name: prompt-engineering
description: Techniques for writing effective LLM prompts. Use when crafting system prompts, optimizing agent instructions, or improving model outputs.
---

# Prompt Engineering

## Core Principles

### Be Explicit
Modern LLMs follow instructions precisely. Be specific about desired output rather than hoping for implicit behavior.

**Less effective:**
```text
Create an analytics dashboard
```

**More effective:**
```text
Create an analytics dashboard. Include relevant features and interactions. Go beyond basics to create a fully-featured implementation.
```

### Provide Context
Explain *why* instructions matter. LLMs generalize better when they understand motivation.

**Less effective:**
```text
NEVER use ellipses
```

**More effective:**
```text
Your response will be read aloud by a text-to-speech engine, so never use ellipses since the TTS engine cannot pronounce them.
```

### Be Vigilant with Examples
LLMs pay close attention to examples. Ensure examples align with desired behaviors and avoid demonstrating behaviors you want to discourage.

### Tell What To Do, Not What To Avoid
Positive instructions outperform prohibitions.

**Less effective:**
```text
Do not use markdown in your response
```

**More effective:**
```text
Your response should be composed of smoothly flowing prose paragraphs.
```

---

## Formatting Control

### Use XML Tags for Structure
XML tags help organize prompts and steer output format:

```text
Write the prose sections of your response in <smoothly_flowing_prose_paragraphs> tags.
```

### Match Prompt Style to Output Style
The formatting in your prompt influences response formatting. Remove markdown from prompts if you want less markdown in outputs.

### Detailed Formatting Instructions

```text
<formatting_guidelines>
When writing reports, documents, or technical explanations, write in clear, flowing prose using complete paragraphs. Use standard paragraph breaks for organization.

Reserve markdown primarily for:
- `inline code`
- Code blocks (```)
- Simple headings (##, ###)

Avoid **bold** and *italics*. Do not use bullet lists unless presenting truly discrete items or explicitly requested.

Incorporate items naturally into sentences rather than listing with bullets. Your goal is readable, flowing text that guides the reader naturally through ideas.
</formatting_guidelines>
```

---

## Tool Usage

### Be Explicit About Actions
LLMs trained for precise instruction following may suggest rather than act unless explicitly directed.

**Less effective (will only suggest):**
```text
Can you suggest some changes to improve this function?
```

**More effective (will make changes):**
```text
Change this function to improve its performance.
```

### Default to Action
To make an agent proactive by default:

```text
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's intent is unclear, infer the most useful likely action and proceed, using tools to discover missing details instead of guessing. Try to infer intent about whether a tool call is intended, and act accordingly.
</default_to_action>
```

### Default to Research
To make an agent more conservative:

```text
<do_not_act_before_instructions>
Do not jump into implementation or change files unless clearly instructed. When intent is ambiguous, default to providing information, doing research, and providing recommendations rather than taking action. Only proceed with edits when explicitly requested.
</do_not_act_before_instructions>
```

### Calibrate Tool Triggering
If tools are undertriggering, add emphasis. If overtriggering, use softer language.

- **Undertriggering**: "CRITICAL: You MUST use this tool when..."
- **Overtriggering**: "Use this tool when..." (remove aggressive language)

### Parallel Tool Calls

```text
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between them, make all independent calls in parallel. Prioritize calling tools simultaneously whenever actions can be done in parallel rather than sequentially.

For example, when reading 3 files, run 3 tool calls in parallel to read all files at once. Maximize parallel tool calls to increase speed and efficiency.

However, if tool calls depend on previous results for parameters, call them sequentially. Never use placeholders or guess missing parameters.
</use_parallel_tool_calls>
```

To reduce parallelism:
```text
Execute operations sequentially with brief pauses between each step to ensure stability.
```

---

## Long-Running Tasks

### Context Management
For agents with context compaction or memory tools:

```text
Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely. Do not stop tasks early due to token budget concerns.

As you approach your token limit, save current progress and state to memory before the context window refreshes. Be as persistent and autonomous as possible. Complete tasks fully even if approaching budget limits. Never artificially stop tasks early.
```

### Multi-Window Workflows

1. **First window**: Set up framework (write tests, create setup scripts)
2. **Later windows**: Iterate on a todo-list

Key practices:
- Write tests in structured format (e.g., `tests.json`) before starting work
- Create setup scripts (e.g., `init.sh`) to start servers, run tests, linters
- Use git for state tracking across sessions

### State Management

**Use structured formats for state data:**
```json
{
  "tests": [
    {"id": 1, "name": "auth_flow", "status": "passing"},
    {"id": 2, "name": "user_mgmt", "status": "failing"},
    {"id": 3, "name": "api_endpoints", "status": "not_started"}
  ],
  "total": 200,
  "passing": 150,
  "failing": 25,
  "not_started": 25
}
```

**Use unstructured text for progress notes:**
```text
Session 3 progress:
- Fixed authentication token validation
- Updated user model to handle edge cases
- Next: investigate user_mgmt test failures
- Note: Do not remove tests
```

### Starting Fresh Context Windows
Be prescriptive about how to resume:

```text
- Call pwd; you can only read and write files in this directory.
- Review progress.txt, tests.json, and the git logs.
- Run integration tests before implementing new features.
```

### Encourage Full Context Usage

```text
This is a long task, so plan your work clearly. Spend your entire output context working on the task. Make sure you don't run out of context with significant uncommitted work. Continue working systematically until complete.
```

---

## Agentic Coding

### Encourage Code Exploration

```text
ALWAYS read and understand relevant files before proposing code edits. Do not speculate about code you have not inspected. If the user references a specific file/path, open and inspect it before explaining or proposing fixes. Be rigorous and persistent in searching code for key facts. Thoroughly review style, conventions, and abstractions before implementing new features.
```

### Minimize Hallucinations

```text
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file, you MUST read it before answering. Investigate and read relevant files BEFORE answering questions about the codebase. Never make claims about code before investigating unless you are certain. Give grounded, hallucination-free answers.
</investigate_before_answering>
```

### Avoid Over-Engineering

```text
<keep_solutions_minimal>
Avoid over-engineering. Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused.

Don't add features, refactor code, or make "improvements" beyond what was asked. A bug fix doesn't need surrounding code cleaned up. A simple feature doesn't need extra configurability.

Don't add error handling, fallbacks, or validation for scenarios that can't happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).

Don't create helpers, utilities, or abstractions for one-time operations. Don't design for hypothetical future requirements. The right complexity is the minimum needed for the current task. Reuse existing abstractions and follow DRY.
</keep_solutions_minimal>
```

### Avoid Test-Focused Solutions

```text
Write high-quality, general-purpose solutions using standard tools. Do not create helper scripts or workarounds. Implement solutions that work for all valid inputs, not just test cases. Do not hard-code values or create solutions only working for specific test inputs.

Focus on understanding problem requirements and implementing correct algorithms. Tests verify correctness, not define the solution. If tests are incorrect, inform me rather than working around them.
```

### Clean Up Temporary Files

```text
If you create temporary files, scripts, or helper files for iteration, clean them up by removing them at the end of the task.
```

---

## Research Tasks

```text
<structured_research>
Search for information in a structured way. As you gather data, develop competing hypotheses. Track confidence levels in progress notes to improve calibration. Regularly self-critique your approach and plan.

Update a hypothesis tree or research notes file to persist information and provide transparency. Break down complex research tasks systematically.
</structured_research>
```

For research with tools:
- Provide clear success criteria
- Encourage source verification across multiple sources
- Use verification tools (browsers, test frameworks) for validation

---

## Subagent Orchestration

```text
<conservative_subagent_usage>
Only delegate to subagents when the task clearly benefits from a separate agent with a new context window.
</conservative_subagent_usage>
```

Best practices:
- Have well-defined subagent tools with clear descriptions
- Let the orchestrator delegate naturally based on task requirements
- Adjust conservativeness as needed for your use case

---

## Verbosity Control

### More Updates
```text
After completing a task involving tool use, provide a quick summary of the work you've done.
```

### Less Verbose
```text
Be concise. Provide brief progress updates. Skip detailed summaries unless requested.
```

---

## Frontend Design

```text
<frontend_aesthetics>
Avoid generic, "on distribution" outputs. In frontend design, this creates "AI slop" aesthetic. Make creative, distinctive frontends that surprise and delight.

Focus on:
- Typography: Choose beautiful, unique fonts. Avoid generic fonts like Arial and Inter.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables. Dominant colors with sharp accents outperform timid palettes.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions. Focus on high-impact moments: one well-orchestrated page load creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects.

Avoid:
- Overused fonts (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (purple gradients on white)
- Predictable layouts and component patterns
- Cookie-cutter design lacking context-specific character

Think outside the box. Vary between light and dark themes, different fonts, different aesthetics.
</frontend_aesthetics>
```

---

## Quick Reference

| Goal | Technique |
|------|-----------|
| More detailed output | Add explicit modifiers: "fully-featured", "comprehensive" |
| Action over suggestion | Use imperative: "Change X" not "Can you suggest..." |
| Reduce markdown | Match prompt style; use formatting guidelines block |
| Better tool use | Add `<default_to_action>` or `<do_not_act_before_instructions>` |
| Long tasks | Add context management and state tracking instructions |
| Code accuracy | Add `<investigate_before_answering>` block |
| Minimal changes | Add `<keep_solutions_minimal>` block |
| Parallel execution | Add `<use_parallel_tool_calls>` block |
| Better research | Add `<structured_research>` block |
| Creative frontend | Add `<frontend_aesthetics>` block |
