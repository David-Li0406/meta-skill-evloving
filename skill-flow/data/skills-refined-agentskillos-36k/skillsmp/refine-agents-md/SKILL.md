---
name: refine-agents-md
description: Analyzes and improves CLAUDE.md or AGENTS.md files for clarity, structure, and effectiveness. Use when the user wants to review, refine, or optimize their agent instruction files.
---

# Refine AGENTS.md / CLAUDE.md

Evaluates agent instruction files against best practices and provides concrete improvements.

## When to Use

- User asks to review/improve their CLAUDE.md or AGENTS.md
- User wants feedback on agent instructions
- User is creating new agent configuration files

## Workflow

1. Read the target file (CLAUDE.md, AGENTS.md, or specified path)
2. Evaluate against the framework below
3. Output structured assessment with specific rewrites

## Evaluation Framework

### Structure Check

| Section | Purpose | Required |
|---------|---------|----------|
| Identity/Role | Who the agent is, core expertise | Yes |
| Constraints | Hard rules, non-negotiables | Yes |
| Preferences | Soft rules, style guidance | Recommended |
| Workflows | Multi-step procedures | If applicable |
| Examples | Concrete demonstrations | Recommended |

### Quality Signals

**Effective instructions are:**
- **Specific** - "Use pytest with `-v` flag" not "write tests"
- **Actionable** - Commands to run, patterns to follow
- **Scoped** - Clear boundaries on what's in/out
- **Layered** - Most important rules first, details later

**Red flags:**
- Vague directives: "be helpful", "write good code"
- Contradictions: "be concise" + walls of text in instructions
- Over-specification: explaining things the model already knows
- Missing context: rules without rationale

### Density Analysis

Calculate signal-to-noise ratio:
- **High signal**: Unique project context, specific commands, concrete examples
- **Low signal**: Generic advice, redundant explanations, filler phrases

Target: >70% high-signal content.

## Output Format

```markdown
## Assessment

**File**: [path]
**Lines**: [count]
**Signal density**: [percentage estimate]

### Strengths
- [what's working]

### Issues
| Problem | Location | Severity |
|---------|----------|----------|
| [issue] | [line/section] | High/Med/Low |

### Recommended Structure

[Proposed outline if reorganization needed]

### Specific Rewrites

**Before** (lines X-Y):
```
[original text]
```

**After**:
```
[improved version]
```

[Repeat for each significant improvement]
```

## Principles

**Preserve intent** - Improve expression, don't change meaning unless explicitly wrong.

**Respect existing style** - Match the file's voice and formatting conventions.

**Prioritize impact** - Focus on changes that materially improve agent behavior.

**Explain rationale** - Each rewrite should include why it's better.

## Anti-Patterns to Flag

- Instructions that fight model defaults (redundant safety disclaimers)
- Nested conditionals that create ambiguity
- Time-sensitive content without expiration handling
- Platform-specific paths without alternatives
- Instructions the model will ignore (too long, buried, contradictory)
