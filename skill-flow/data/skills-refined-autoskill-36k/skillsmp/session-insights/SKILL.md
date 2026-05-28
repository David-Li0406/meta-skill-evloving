---
name: session-insights
description: Session retrospective using Kolb's Learning Cycle and KPT framework. Updates memory file (CLAUDE.md/AGENTS.md) and creates GitHub Issues. Use when the user says "session insights", "what did we learn", "update memory", or wants to extract reusable principles from the session.
disable-model-invocation: true
allowed-tools: Bash(gh issue create:*), Edit, Glob, Grep, Read, TodoWrite
---

# Session Insights

## Context

- Repository root: !`git rev-parse --show-toplevel`
- Memory files: !`ls CLAUDE.md .claude/CLAUDE.md AGENTS.md .codex/AGENTS.md 2>/dev/null`
- Recent commits: !`git log --oneline -10`

## Guidelines

- Use user's session language for all output
- Focus on systemic insights, not one-off fixes
- Extract root causes, not symptoms
- Formulate actionable principles, not vague aspirations

---

## Step 1: Detect Memory File

Search for memory file in repository root and `.claude/` or `.codex/` directories:

- If you are Codex CLI → prefer `AGENTS.md`, fallback to `CLAUDE.md`
- Otherwise → prefer `CLAUDE.md`, fallback to `AGENTS.md`
- If neither exists → ask user: "No memory file found. Create CLAUDE.md or AGENTS.md?"

Report detected file before proceeding:

```
Memory file: [path/to/file]
```

---

## Step 2: Fact Collection & Analysis

Execute together and present in a single message.

### Fact Collection

List observable facts. NO analysis at this stage.

### Analysis & Abstraction

- **For Keep**: Identify success factors
- **For Problem**: Apply "Why?" repeatedly until reaching root cause (typically 2-5 times)

**Abstraction Gate** - Transform each insight: remove concrete details, add "Apply when" conditions, formulate as reusable principle.

**Output format:**

```
## Fact Collection & Analysis

### Keep
- [Fact]: [Outcome]
  - Success factor: [Why it worked]
  - Principle: [Abstracted insight]
  - Apply when: [Condition/trigger]

### Problem
- [Fact]: [Outcome]
  - Root cause: [Why] → [Why] → ... → [Root cause]
  - Principle: [Abstracted insight]
  - Apply when: [Condition/trigger]

Proceed to improvement proposals? (yes/no)
```

- **If Keep is empty**: Omit Keep section, note "No notable successes identified."
- **If Problem is empty**: Omit Problem section, note "No notable problems identified."
- **If both empty**: Output "No significant insights from this session." and end command.

If user says "no" → end command.

---

## Step 3: Improvement Proposals

### 3.1 Memory File Updates

Read current memory file, check for conflicts, then present proposals.

**If no proposals**: Output "No memory file updates needed." and skip to 3.2.

**If proposals exist**:

```
### Memory File Updates

**1. [ADD/MODIFY/DELETE]: [Section]**
- Reason: [Why]
- Content:
  [Exact markdown]

**2. ...**

Approve? ("1,2" / "all" / "none")
```

- If "none" → skip to 3.2
- If approved → apply changes, report result, then proceed to 3.2

### 3.2 Codebase Improvements

**If no proposals**: Output "No codebase improvements identified." and end command.

**If proposals exist**:

```
### Codebase Improvements

**1. [Type]: [Description]**
- Problem: [Issue]
- Solution: [Change]

**2. ...**

Create GitHub Issues? ("1,2" / "all" / "none")
```

Type examples: Bug fix, Refactor, Test, Performance, Documentation

- If "none" → end command
- If approved → create issues, report URLs, then end command

**GitHub Issue format:** `gh issue create --title "[Type]: [Description]" --body "..."` with Context, Problem, Proposed Solution, Expected Benefit sections.

If any command fails, report error and ask user how to proceed.
