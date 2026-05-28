---
name: prompt-engineering
description: |
  Best practices for crafting effective prompts for agents, skills, and Claude interactions.
  Use when writing system prompts, agent instructions, or optimizing Claude responses.
---

# Prompt Engineering for Claude Agents

## The Three Laws of Agent Prompts

### 1. Right Altitude (Goldilocks Zone)

| Level | Example | Problem |
|-------|---------|---------|
| **Too Low** | "If file is .ts AND has 'async' AND line > 100..." | Brittle, breaks on edge cases |
| **Just Right** | "Review TypeScript async patterns for common pitfalls" | Clear, flexible, actionable |
| **Too High** | "Be a good code reviewer" | Vague, inconsistent results |

**Test**: Can you imagine 3 different valid interpretations? Too high. Can you imagine it breaking on a valid input? Too low.

### 2. Few-Shot Examples (3-5 Canonical Cases)

Don't list every possibility. Show representative examples:

```markdown
## Examples

### Example 1: Clear Success Case
Input: [Typical, well-formed input]
Output: [Expected response with reasoning shown]

### Example 2: Edge Case
Input: [Unusual but valid input]
Output: [How to handle gracefully]

### Example 3: What NOT to Do
Input: [Tricky input that could mislead]
Output: [Why the naive approach is wrong, correct approach]
```

### 3. Explicit Constraints

Tell Claude what NOT to do:

```markdown
## Constraints

- Do NOT modify files outside the specified directory
- Do NOT commit changes without confirmation
- NEVER include secrets in outputs
- ALWAYS validate input before processing
```

## Prompt Structure Template

```markdown
# [Agent/Skill Name]

[One-sentence purpose]

## Context

[Background information Claude needs]

## Responsibilities

1. **[Verb] [Object]**: [Brief description]
2. **[Verb] [Object]**: [Brief description]

## Workflow

When given [input type]:
1. [First action]
2. [Second action]
3. [Third action]

## Examples

### Example 1: [Scenario Name]
**Input**: [Sample]
**Output**: [Expected result]
**Reasoning**: [Why this is correct]

### Example 2: [Edge Case]
**Input**: [Tricky sample]
**Output**: [Correct handling]
**Reasoning**: [Common mistake avoided]

## Anti-Patterns

- **Don't**: [Bad practice]
  **Instead**: [Good practice]

## Output Format

[Specify exact format if needed: JSON, markdown, etc.]
```

## Context Engineering

### Tell Claude About Session State

```markdown
## Session Context

- Context may be compacted between turns
- Important decisions will be saved to CLAUDE.md
- You may need to resume work from a previous session
- Use episodic memory to recall past decisions
```

### Memory Management Hints

```markdown
## Memory Usage

When working on large tasks:
1. Save progress incrementally to files
2. Document key decisions in CLAUDE.md
3. Use clear commit messages for future reference
4. Create TODO items for incomplete work
```

## Model-Specific Considerations

### Haiku (Fast, Cheap)
- Keep prompts concise
- Use for simple, well-defined tasks
- Avoid requiring complex reasoning chains

### Sonnet (Balanced)
- Standard detail level
- Good for most agent tasks
- Can handle moderate complexity

### Opus (Maximum Capability)
- Worth extra context for complex tasks
- Best for nuanced decisions
- Use for critical, high-stakes work

## Prompt Optimization Techniques

### 1. Front-Load Critical Information

```markdown
## CRITICAL: [Most important instruction]

[Less critical context below]
```

### 2. Use Structured Sections

```markdown
## Input Format
[What Claude receives]

## Output Format
[What Claude must produce]

## Processing Rules
[How to transform input to output]
```

### 3. Provide Escape Hatches

```markdown
If you encounter a situation not covered by these instructions:
1. State what you're uncertain about
2. Explain your best judgment
3. Ask for clarification if needed
```

### 4. Include Verification Steps

```markdown
Before completing:
- [ ] Verify output matches expected format
- [ ] Check for security concerns
- [ ] Ensure changes are minimal and focused
```

## Common Mistakes

### Mistake 1: Overly Prescriptive

```markdown
# BAD
If the error contains "undefined" and the file is JavaScript:
  Check for null pointer
Else if the error contains "type" and the file is TypeScript:
  Check for type mismatch
...

# GOOD
Diagnose errors by:
1. Reading the error message carefully
2. Identifying the error category (type, null, async, etc.)
3. Locating the source in the codebase
4. Understanding the root cause before fixing
```

### Mistake 2: No Examples

```markdown
# BAD
Review code for quality issues.

# GOOD
Review code for quality issues.

Example issue types:
- Unused variables (remove them)
- Complex conditions (extract to named functions)
- Missing error handling (add try/catch or validation)
```

### Mistake 3: Conflicting Instructions

```markdown
# BAD
Be thorough and check everything.
Also be fast and efficient.

# GOOD
Prioritize checks:
1. Critical: Security vulnerabilities (always check)
2. Important: Logic errors (check if time allows)
3. Nice-to-have: Style issues (skip if time-constrained)
```

## Testing Your Prompts

### Adversarial Testing
Try inputs designed to break the prompt:
- Empty input
- Malformed input
- Edge cases
- Unexpected formats

### A/B Testing
Compare prompt variations:
1. Run both on same inputs
2. Evaluate which produces better results
3. Iterate on winner

### User Feedback Loop
1. Deploy prompt
2. Collect failure cases
3. Add examples for failures
4. Repeat
