---
name: writing-skills
description: Use when creating new Claude skills, updating existing skills, or helping users develop process documentation. Covers skill structure, directive writing principles, and TDD-based testing methodology.
---

# Writing Effective Claude Skills

## Overview

Writing skills is Test-Driven Development applied to process documentation. A skill captures techniques, patterns, or references that weren't intuitively obvious, apply across multiple projects, and would benefit others.

## Core Philosophy

**Claude is smart. Only write what it doesn't already know.**

- Explain motivation behind rules; Claude generalizes from understanding *why*
- Use positive framing: "Update existing files in place" not "Don't create duplicates"
- Supply context rather than commands; bare imperatives trigger overtriggering in Claude 4.x

## When to Create a Skill

Create a skill when you observe:
- A pattern you've explained multiple times
- A technique that wasn't obvious to discover
- A workflow that applies across projects
- Behavior you want Claude to consistently follow

Do NOT create a skill for:
- One-off instructions
- Project-specific conventions (use CLAUDE.md instead)
- Common knowledge Claude already has

**Can't articulate the pattern yet?** Use `/discover-skill` to prototype through a real example first. Discovery produces working notes; this skill converts them into a structured skill.

## SKILL.md Structure

```markdown
---
name: skill-name-kebab-case
description: Use when [specific triggers]. [One sentence explaining the skill's purpose.]
---

# Skill Title

## Overview
One paragraph explaining what this skill does and why it matters.

## When to Use
Bullet list of specific triggers, error messages, or symptoms.

## Core Pattern
The primary technique or workflow, presented as numbered steps or a checklist.

## Examples (optional, for code-focused skills)
Brief good/bad code examples for each Core Pattern item.

## Quick Reference
Condensed version for rapid lookup after the skill is learned.

## Common Mistakes
| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| ... | ... | ... |

## Anti-Rationalizations
Explicit counters to excuses Claude might generate to bypass the skill.

## Summary
3-4 highest-priority rules repeated for attention anchoring (see Attention Anchoring section).
```

## Core Pattern Formats

Choose the format based on skill purpose:

**Numbered steps** — Use for sequential workflows where order matters:
```markdown
1. Read the existing code
2. Identify the change location
3. Make the minimal edit
4. Verify the change works
```

**Checkbox lists** — Use for verification checklists and pressure-check scenarios:
```markdown
- [ ] No mutable default arguments
- [ ] No bare `except:` clauses
- [ ] Resources managed with `with` statements
```

Checkboxes signal "verify each item" rather than "follow this sequence." Prefer checkboxes when the skill will be used under time pressure to validate work.

## Description Field: Discovery Optimization

The `description` field determines skill findability. Requirements:
- Start with "Use when..." plus specific triggers
- Write in third person
- Include error messages or symptoms as searchable keywords
- Keep under 200 characters

**Good:** `Use when writing API endpoints. Covers authentication patterns, error handling, and rate limiting.`

**Bad:** `This skill helps with APIs.`

## Efficiency Guidelines

- Maintain ~150 instruction limit across all loaded rules to prevent degradation
- Keep frequently-loaded directives under 200 words
- Use progressive disclosure: overview in SKILL.md, detailed references in linked files
- Cross-reference instead of duplicating content

**Exception:** Skills used under pressure (code review checklists, debugging guides) may exceed word limits to keep critical content inline. Users under time pressure won't navigate to linked files. See "Code-Focused Skills" section.

## Attention Anchoring

LLMs attend more strongly to the end of context windows. Place a **Summary** section at the end of skills containing 3-4 highest-priority rules. This ensures critical guidance remains salient in longer sessions where earlier content may receive less attention.

The Summary should:
- Repeat (not merely reference) the most important rules
- Use imperative, actionable phrasing
- Stay under 5 items to maintain focus

## Compliance Methods (Ranked)

1. **Context and motivation** — Explain *why*; Claude generalizes from understanding
2. **Structural enforcement** — Numbered workflows, checklists, verification gates
3. **Imperatives** — Reserve "YOU MUST" for true boundaries; use sparingly

## Technical Formatting

- XML structures preserve rules better than markdown/JSON in long prompts
- Match prompt formatting style to desired output style
- Use workflow checklists with blocking conditions before proceeding
- Implement feedback loops with validation gates

## Code-Focused Skills

Skills for writing or reviewing code benefit from an **Examples** section with good/bad code snippets.

### Example Format

Always append rationale to `# Bad` comments:

```python
# Good
with open("data.txt") as f:
    content = f.read()

# Bad — manual cleanup is error-prone, prefer context managers
f = open("data.txt")
content = f.read()
f.close()
```

The rationale (`— manual cleanup is error-prone...`) enables quick scanning under pressure.

### Keep Examples Minimal

Code examples should show the pattern, not production-ready code. Users need to grasp the concept quickly.

**Include:**
- The specific pattern being demonstrated
- Just enough context to understand the scenario

**Omit:**
- Imports (unless the import itself is the point)
- Configuration/setup boilerplate
- Type definitions and dataclasses
- Multiple examples of the same pattern

**One or two examples per concept suffices.** Each example should demonstrate something distinct. If you need three examples, you're likely covering multiple concepts—split them.

```python
# Good — minimal, shows the pattern
def process_order(order_id: str) -> None:
    logger.info("order_started", order_id=order_id)
    result = _do_process(order_id)
    logger.info("order_completed", order_id=order_id)

# Bad — too much detail, obscures the pattern
import logging
import structlog
from typing import Any
from myapp.models import Order, OrderResult
from myapp.config import configure_logging

configure_logging()
logger = structlog.get_logger(__name__)

def process_order(order_id: str, items: list[dict[str, Any]]) -> OrderResult:
    # ... 20 more lines
```

### Rationale Sourcing

When a skill is based on an authoritative source (style guide, specification, RFC), rationale should trace back to that source's reasoning:

| Source Type | Rationale Style |
|-------------|-----------------|
| Style guide | "non-idiomatic", "violates style guide section X" |
| Specification | "undefined behavior per spec", "violates invariant" |
| Best practice | "causes X problem", "prevents Y benefit" |

Avoid purely practical rationale ("causes bugs") when style-based rationale exists ("non-idiomatic, use X instead"). The authoritative source carries more weight.

### Inline vs Linked Examples

For pressure-check scenarios (code review, debugging), keep examples **inline** in SKILL.md even if it exceeds the 200-word guideline. Users under pressure won't navigate to linked files.

Reserve linked reference files for:
- Comprehensive rule documentation
- Extended examples with edge cases
- Background context that isn't needed during active use

## The RED-GREEN-REFACTOR Cycle

Skills require pressure testing before deployment.

### RED Phase: Baseline Without Skill
1. Run realistic scenarios WITHOUT the skill loaded
2. Document exact failures and rationalizations verbatim
3. Identify the gap between desired and actual behavior

### GREEN Phase: Minimal Skill
1. Write the minimum skill addressing only observed failures
2. Re-run scenarios WITH the skill loaded
3. Verify compliance on previously-failed cases

### REFACTOR Phase: Close Loopholes
1. Identify new rationalizations Claude uses to bypass rules
2. Add explicit negations and anti-rationalization entries
3. Re-test until bulletproof under combined pressure

## Pressure Testing Scenarios

Effective tests combine multiple pressures:
- Time constraints + sunk cost fallacy
- Authority pressure + economic stakes
- Exhaustion simulation + conflicting requirements

**Single-pressure tests are insufficient.** Claude resists easily but breaks under combined pressure.

Good scenarios feature:
- Concrete A/B/C choices
- Specific real-world constraints
- Actual consequences
- Force action rather than hypothesizing

## Closing Loopholes

When Claude violates rules despite having the skill, capture exact rationalizations and add:
- Explicit negations in rule sections
- Entries in Common Mistakes table
- Anti-Rationalization section entries
- Updated description noting violation symptoms

## Verification Checklist

Before committing a new skill:

- [ ] RED phase documented with baseline failures
- [ ] GREEN phase shows minimal skill addressing failures
- [ ] REFACTOR phase closes identified loopholes
- [ ] Pressure tested with combined-pressure scenarios
- [ ] Description field optimized for discovery
- [ ] Under 200 words for frequently-loaded skills
- [ ] Cross-references used instead of duplication
- [ ] Anti-rationalizations address observed excuses

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Deploying untested skills | Inevitably contains loopholes | Complete RED-GREEN-REFACTOR cycle |
| Bare imperatives everywhere | Triggers overtriggering, reduces compliance | Explain motivation, use imperatives sparingly |
| Single-pressure testing | Claude resists easily alone | Combine multiple pressures |
| Vague description field | Skill never discovered | "Use when..." + specific triggers |
| Duplicating content | Bloats context, causes drift | Cross-reference linked files |
| Too many instructions | Degradation past ~150 rules | Keep skills focused, link to references |
| `# Bad` without rationale | Loses teaching moment, requires re-lookup | Always append `— reason` to Bad comments |
| Practical vs style rationale | Weaker authority, easier to rationalize around | Trace rationale to authoritative source |
| Production-ready code examples | Obscures the pattern with boilerplate | Show minimal code; omit imports, setup, types |
| Too many examples per concept | Bloats skill, diminishes focus | One or two examples; each should teach something distinct |

## Anti-Rationalizations

When tempted to skip testing:
- "This skill is simple enough" — Simple skills still have loopholes
- "I'll test it later" — Later never comes; test before committing
- "Testing is overkill" — The phrase itself signals the need to test

When tempted to over-engineer:
- "Users might need X" — Write for observed needs, not hypotheticals
- "I'll add flexibility" — Flexibility without use cases is complexity
- "This should be configurable" — Start concrete, abstract when patterns emerge

## Supporting References

- [skill-template.md](skill-template.md) — Read this file and copy its structure when creating a new skill from scratch
- [testing-scenarios.md](testing-scenarios.md) — Consult when designing pressure tests; use the scenario template and examples to construct combined-pressure tests for your skill
- [directive-patterns.md](directive-patterns.md) — Reference when drafting directive language; contains framing examples, compliance patterns, and anti-patterns to avoid
