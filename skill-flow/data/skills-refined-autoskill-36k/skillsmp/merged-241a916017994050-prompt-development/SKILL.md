---
name: prompt-development
description: Use this skill when creating or improving prompts for AI systems, including system prompts, agent instructions, and LLM prompts.
---

# Prompt Development

Effective prompts are clear, concise, and structured to guide AI systems in producing desired outputs.

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

### Remove Redundancy
Avoid repeating the same instruction in multiple ways, as it dilutes attention.

**Before:** "You must always verify each item. Do not skip items. Every item needs to be checked. Make sure you don't miss any items."

**After:** "Verify each item individually. No skipping."

### Remove Noise
Don't teach the model things it already knows. State your specific requirements clearly.

**Before:** 40-line example of what a code walkthrough looks like

**After:** "Write a detailed walkthrough: what changed, line numbers, analysis of the flow, data transformations, dependencies."

### Sharpen Instructions
Direct commands are clearer than hedged suggestions.

**Before:** "It's important that you remember to always navigate to the project root directory before starting any work..."

**After:** `cd "$CLAUDE_PROJECT_DIR"`

### Keep Load-Bearing Content
Preserve essential elements such as workflow steps, quality criteria, critical rules, and output format requirements.

### Write Clean Prose
Write as if it was always this way — not in a "correction" style.

**Before:** "Remember that you should do TWO interviews, not just one..."

**After:**
```
### 0. Business Requirements Interview
Interview the user to understand what needs to be built.

### 2. Technical Interview
With discovery complete, interview the user about implementation details.
```

## Structure

Good prompts have clear sections. Adapt this pattern to your use case:

```
[1-2 sentence role/purpose]

## Core Concept or Approach
[Key principle guiding behavior]

## Workflow / Steps
[What to do, in order]

## Rules / Constraints
[Non-negotiable requirements]

## Quality Criteria
[What good looks like, what to avoid]

## Output Format
[Expected structure if applicable]
```

## Formatting Control

### Use Markdown for Structure
Organize prompts using headings and sections to enhance clarity.

### Detailed Formatting Instructions
```text
<formatting_guidelines>
When writing reports, documents, or technical explanations, write in clear, flowing prose using complete paragraphs. Use standard paragraph breaks for organization.

Reserve markdown primarily for:
- `inline code`
- Code blocks (```)
- Simple headings (##, ###)

Avoid **bold** and *italics*. Do not use bullet lists unless presenting truly discrete items or explicitly requested.
</formatting_guidelines>
```

## Examples

Examples are the most effective way to communicate behavior. Wrap each example in `<example>` tags with `user:` and `assistant:` prefixes.

```
<example>
user: What's the capital of France?
assistant: Paris
</example>
```

For complex behaviors, use separate example tags for each case:

```
<example>
user: Explain how authentication works in this codebase
assistant: [reads relevant files, then provides explanation]
</example>
```

## Iteration

Prompt development is empirical:

1. Start minimal
2. Test with real inputs
3. Identify failures
4. Add targeted fixes
5. Remove instructions that prove unnecessary

Track which instructions address which problems. If you cannot point to a specific failure that an instruction prevents, consider removing it.

## Research Tasks

```text
<structured_research>
Search for information in a structured way. As you gather data, develop competing hypotheses. Track confidence levels in progress notes to improve calibration. Regularly self-critique your approach and plan.
</structured_research>
```

For research with tools:
- Provide clear success criteria
- Encourage source verification across multiple sources
- Use verification tools (browsers, test frameworks) for validation

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