---
name: council
description: Gather design feedback from AI consultants (Gemini and Codex). Use for architecture decisions, design review, or when you want multiple expert perspectives on SENTINEL development. (project)
allowed-tools: Bash, Read, Glob, Grep
user-invocable: true
proactive: true
---

<!-- PROACTIVE USE: Invoke /council without being asked when:
  - Facing architectural decisions with multiple valid approaches
  - Uncertain about implementation strategy
  - Making changes that affect multiple subsystems
  - Design tradeoffs need external perspective
-->

# The Council

Invoke external AI consultants for design feedback on SENTINEL.

## Consultants

| Model | Strength | Best For |
|-------|----------|----------|
| **Gemini** | Big-picture thinking, design patterns | Architecture, conceptual clarity |
| **Codex** | Technical depth, implementation focus | Code quality, practical constraints |

## How to Run

When the user invokes `/council`, gather context and consult both AIs:

### Step 1: Prepare Context

Read the project brief and any relevant files the user mentions:
```
C:\dev\SENTINEL\SENTINEL_PROJECT_BRIEF.md
```

### Step 2: Consult Gemini

Run non-interactively with the user's question + context:
```bash
gemini "You are reviewing SENTINEL, a tactical TTRPG with an AI Game Master.

<context>
[Insert project brief or relevant code]
</context>

<question>
[User's design question]
</question>

Provide focused feedback on design patterns, architecture, or the specific question asked. Be concise."
```

### Step 3: Consult Codex

Run non-interactively:
```bash
codex exec "You are reviewing SENTINEL, a tactical TTRPG with an AI Game Master.

<context>
[Insert project brief or relevant code]
</context>

<question>
[User's design question]
</question>

Provide focused feedback on implementation, code quality, or the specific question asked. Be concise."
```

### Step 4: Synthesize

Present both perspectives, noting:
- Where they agree (strong signal)
- Where they differ (worth investigating)
- Actionable recommendations

## Example Usage

User: `/council` Should we use SQLite instead of JSON for campaign persistence?

Then:
1. Read `SENTINEL_PROJECT_BRIEF.md` and `src/state/schema.py`
2. Ask Gemini about data model evolution and query patterns
3. Ask Codex about migration complexity and performance
4. Synthesize into recommendation

## Tips

- Keep prompts focused on one question at a time
- Include relevant code snippets, not entire files
- The consultants don't have project context — you must provide it
- Use when genuinely uncertain, not for validation
