# Anthropic Best Practices for Writing Skills

## Overview

This document provides Anthropic-recommended best practices for writing effective skills (prompt engineering for process documentation).

## Core Principles

### 1. Conciseness Matters

**Target: <500 lines per skill**

Research shows Claude performs better with concise, focused prompts.

```markdown
❌ BAD (1000+ lines):
# Mega Debugging Guide
[Everything about debugging in one massive document]

✅ GOOD (<500 lines each):
# Systematic Debugging
[5-step process, focused]

# Root Cause Tracing
[Backward tracing, focused]

# Test Pollution Detection
[Binary search for polluters, focused]
```

**Why shorter is better:**
- Better attention to relevant details
- Easier to load selectively
- Faster processing
- More focused guidance

### 2. Progressive Disclosure

**Show complexity gradually**

Start simple, add detail progressively.

```markdown
✅ GOOD Structure:

## Core Principle
One sentence essence

## When to Use
3-5 bullet points

## The Iron Law
One clear rule

## Basic Process
High-level steps

## Detailed Process
Step 1: [Overview]
  - Detail A
  - Detail B

## Advanced Techniques
[For experienced users]

## Edge Cases
[When basic process isn't enough]
```

**Progressive disclosure benefits:**
- Quick scanning for experienced users
- Gradual learning for new users
- Easy to find relevant section
- Doesn't overwhelm

### 3. Test Across All Models

**Skills should work across Claude model tiers**

Write skills that are effective for:
- Claude 3.5 Sonnet (most capable)
- Claude 3.5 Haiku (fastest)
- Claude 3 Opus (previous generation)

```markdown
Testing checklist:
- [ ] Tested with Sonnet 3.5
- [ ] Tested with Haiku 3.5
- [ ] Still effective with Opus 3

If skill requires specific model:
- Document requirement clearly
- Explain why needed
- Provide fallback for other models
```

### 4. Use Gerund Form for Names

**Skill names should be action-oriented**

Use gerund (-ing) form for process skills:

```markdown
✅ GOOD:
- writing-plans
- executing-plans
- debugging-systematically
- tracing-root-causes

❌ BAD:
- plan-writer
- plan-execution
- debugger
- root-cause-tracer
```

**Why gerunds:**
- Implies ongoing process
- Action-oriented
- Natural in "I'm [skill-name]" context
- Consistent with Superpowers convention

**Exception:** Reference skills can be nouns
```markdown
✅ GOOD for reference:
- testing-anti-patterns
- anthropic-best-practices
- persuasion-principles
```

## Writing Style Guidelines

### Clarity Over Cleverness

```markdown
❌ BAD (clever):
"Embark on a journey of bug discovery..."

✅ GOOD (clear):
"Follow these 5 steps to find bugs:"
```

### Active Voice

```markdown
❌ BAD (passive):
"The test should be written first"

✅ GOOD (active):
"Write the test first"
```

### Imperative Mood for Instructions

```markdown
❌ BAD (indirect):
"You should probably run the tests"

✅ GOOD (imperative):
"Run the tests"
```

### Specific Over Generic

```markdown
❌ BAD (generic):
"Handle errors appropriately"

✅ GOOD (specific):
"Catch exceptions, log the error with context,
return user-friendly message, and alert monitoring"
```

## Structural Patterns

### The Iron Law Pattern

Every skill should have ONE core rule stated clearly:

```markdown
## The Iron Law

**[CLEAR, BOLD STATEMENT]**

Explanation of why this is non-negotiable.
```

**Examples:**
- TEST FIRST, CODE SECOND
- NEVER SKIP THE REVIEW BETWEEN TASKS
- ALWAYS BACKUP BEFORE RUNNING TESTS

**Why it works:**
- Creates clear commitment
- Easy to remember
- Forces prioritization
- Builds discipline

### The Before/After Pattern

Show contrast to demonstrate value:

```markdown
## Why [Skill Name]?

**Benefits:**
✅ Outcome 1
✅ Outcome 2

**Without [skill]:**
❌ Problem 1
❌ Problem 2
```

**Why it works:**
- Shows clear value proposition
- Motivates adoption
- Addresses skepticism
- Demonstrates ROI

### The Process Pattern

For technique skills, use numbered steps:

```markdown
## The [X]-Step Process

### Step 1: [Action]

**Goal**: What this step achieves

[Instructions]

**Output**: What you should have after this step

### Step 2: [Action]

...
```

**Why it works:**
- Clear progression
- Easy to follow
- Checkpoints built-in
- Can resume if interrupted

### The Example Pattern

Show real scenarios, not toy examples:

```markdown
## Example: [Real Scenario]

**Problem**: Specific issue
**Context**: Relevant details

**Without skill:**
1. What happens
2. What goes wrong
3. Outcome (negative)

**With skill:**
1. Apply step 1
2. Apply step 2
3. Outcome (positive)

**Improvement**: Measurable difference
```

**Why it works:**
- Concrete, not abstract
- Shows actual application
- Demonstrates value
- Provides template

## Persuasion Techniques

### Authority

Cite credible sources:

```markdown
## Authority

**This skill is based on:**
- Kent Beck's Test-Driven Development
- Research: TDD reduces bugs by 40-80%
- Industry standard: Used by Google, Microsoft
```

### Social Proof

Show widespread adoption:

```markdown
**Social Proof**: All major tech companies
use this approach for critical systems.
```

### Commitment and Consistency

End with commitment checklist:

```markdown
## Your Commitment

When [doing task]:
- [ ] I will [action 1]
- [ ] I will [action 2]
- [ ] I will not [anti-pattern]
```

### Scarcity

Emphasize cost of not following:

```markdown
**Without this skill:**
- Bugs found in production (expensive)
- 10x more work to fix later
- Technical debt compounds
```

## Common Mistakes to Avoid

### Mistake 1: Too Much Context

```markdown
❌ BAD:
[2000 words of background before getting to point]

✅ GOOD:
## Core Principle
[Get to the point immediately]

## Background (Optional)
[Additional context if needed]
```

### Mistake 2: Assumed Knowledge

```markdown
❌ BAD:
"Use the repository pattern with DI and IoC"
[Assumes reader knows these terms]

✅ GOOD:
"Use the repository pattern (separating data
access from business logic) with dependency
injection (passing dependencies in rather than
creating them inside)"
[Explains terms in context]
```

### Mistake 3: Missing Examples

```markdown
❌ BAD:
"Follow these steps: [abstract description]"

✅ GOOD:
"Follow these steps:
1. [Step description]

Example:
[Concrete code showing step in action]"
```

### Mistake 4: No Clear Action

```markdown
❌ BAD:
"Testing is important and should be done properly"
[What does "properly" mean?]

✅ GOOD:
"Write test first (must fail), then write code
to make it pass, then refactor while keeping
tests green"
[Clear, actionable steps]
```

## Format Requirements

### YAML Frontmatter

Every skill must have:

```yaml
---
name: skill-name
description: "One-line description for quick reference"
---
```

**Description format:**
- Start with when to use: "Use when..."
- Include what it does: "Follow [process]..."
- Keep under 200 characters
- Be specific and actionable

### Markdown Structure

Required elements:

```markdown
# Skill Name

## Core Principle
## When to Use This Skill
## The Iron Law
## [Main Content]
## Examples
## Common Mistakes
## Integration with Skills
## Authority
## Your Commitment
## Bottom Line
```

### Code Blocks

Use appropriate language tags:

````markdown
```php
// PHP code
```

```bash
# Shell commands
```

```markdown
# Nested markdown
```
````

### Lists and Bullets

Be consistent:

```markdown
✅ Use checkboxes for:
- [ ] Process steps
- [ ] Checklists
- [ ] Commitments

✅ Use bullets for:
- Options
- Features
- Examples

✅ Use numbers for:
1. Sequential steps
2. Ordered processes
3. Prioritized items
```

## Testing Your Skill

### Readability Test

```markdown
Can someone scan this in 30 seconds and understand:
- [ ] What the skill is for
- [ ] When to use it
- [ ] What the core rule is
- [ ] Where to find details
```

### Actionability Test

```markdown
Can someone read this and immediately:
- [ ] Know what to do first
- [ ] Follow the process step-by-step
- [ ] Recognize when they're done
- [ ] Identify mistakes to avoid
```

### Model Test

```markdown
Test with subagents:
- [ ] Works with Sonnet 3.5
- [ ] Works with Haiku 3.5
- [ ] Improves outcomes measurably
- [ ] Handles edge cases
```

## Length Guidelines

### Optimal Lengths

```markdown
Minimum effective length:
- Discipline skill: 300 lines
- Technique skill: 400 lines
- Pattern skill: 250 lines
- Reference skill: 300 lines

Maximum recommended length:
- Any skill: 600 lines (if longer, split into multiple skills)
```

### When to Split

Split a skill if:
- Exceeds 600 lines
- Covers multiple distinct topics
- Has independent sub-processes
- Takes >5 minutes to read

```markdown
Example: Split "complete-testing-guide" into:
- test-driven-development
- testing-anti-patterns
- test-pollution-detection
- condition-based-waiting
```

## Version Control

### Tracking Changes

```markdown
Document changes in skill:

## Version History

v2.1 (2024-01-15):
- Added pressure scenario guidance
- Closed time-constraint loophole
- Added 3 new examples

v2.0 (2024-01-01):
- Major update: Changed core process
- Re-tested all scenarios
- Updated all examples

v1.0 (2023-12-15):
- Initial release
```

### Breaking Changes

If changing core process:
- Bump major version
- Document what changed
- Explain why changed
- Re-test thoroughly
- Update dependent skills

## Integration Guidelines

### Referencing Other Skills

```markdown
✅ GOOD:
"Use with test-driven-development skill to write
tests first, then implement."

❌ BAD:
"Use with TDD" [unclear reference]
```

### Skill Dependencies

```markdown
## Integration with Skills

**Required:**
- skill-name - Why required

**Use with:**
- skill-name - How they complement

**Enables:**
- skill-name - What this unlocks
```

## Bottom Line Format

Every skill ends with one-sentence summary:

```markdown
---

**Bottom Line**: [One sentence capturing essence of skill]
```

**Examples:**
- "Write tests first, always."
- "Trace backward until you find the original trigger."
- "Review every task output, no exceptions."

**Why it works:**
- Memorable
- Repeatable
- Reinforces core message
- Easy to cite

## Quick Reference Checklist

Use this when writing any skill:

- [ ] Under 600 lines
- [ ] Progressive disclosure (simple → complex)
- [ ] Tested across models
- [ ] Gerund name (if process skill)
- [ ] Has Iron Law
- [ ] Has Before/After
- [ ] Real examples (not toy)
- [ ] Common mistakes section
- [ ] Authority cited
- [ ] Commitment checklist
- [ ] Bottom line summary
- [ ] YAML frontmatter complete

---

**Note**: These are guidelines from Anthropic's prompt engineering research. They represent best practices for writing skills that work effectively with Claude models. Follow them for maximum effectiveness.
