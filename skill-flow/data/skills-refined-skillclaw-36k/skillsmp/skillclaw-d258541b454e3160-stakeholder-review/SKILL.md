---
name: stakeholder-review
description: Use this skill to conduct a multi-perspective review of implementation changes, ensuring quality assurance from various stakeholders before user approval.
---

# Skill body

## Purpose

Run parallel stakeholder reviews of implementation changes to identify concerns from multiple perspectives (architecture, security, quality, testing, performance) before user approval.

## When to Use

- After the implementation phase completes in `/cat:work`
- Before the user approval gate
- When significant code changes need multi-perspective validation

## Stakeholders

| Stakeholder | Reference | Focus |
|-------------|-----------|-------|
| requirements | @stakeholders/requirements.md | Requirement satisfaction verification |
| architect | @stakeholders/architect.md | System design, module boundaries, APIs |
| security | @stakeholders/security.md | Vulnerabilities, input validation |
| quality | @stakeholders/quality.md | Code quality, complexity, duplication |
| tester | @stakeholders/tester.md | Test coverage, edge cases |
| performance | @stakeholders/performance.md | Efficiency, resource usage |
| ux | @stakeholders/ux.md | Usability, accessibility, interaction design |
| sales | @stakeholders/sales.md | Customer value, competitive positioning |
| marketing | @stakeholders/marketing.md | Positioning, messaging, go-to-market |
| legal | @stakeholders/legal.md | Licensing, compliance, IP, data privacy |

## Progress Output

This skill orchestrates multiple stakeholder reviewers as subagents. Each reviewer's internal tool calls are invisible - users see only the Task tool invocations and aggregated results.

**On start:**
```
◆ Running stakeholder review...
```

**During execution:** Task tool invocations appear for each reviewer spawn, but their internal file reads and analysis are invisible.

**On completion:**
```
✓ Review complete: {APPROVED|CONCERNS|REJECTED}
  → requirements: ✓
  → architect: ✓
  → security: ⚠ 1 HIGH
  → tester: ✓
  → performance: ✓
```

## Process

<step name="prepare">

**Prepare review context:**

1. Identify files changed in implementation.
2. Get diff summary for reviewers.
3. Determine which stakeholders are relevant (skip if no applicable changes).

```bash
# Get changed files
CHANGED_FILES=$(git diff --name-only HEAD~1..HEAD 2>/dev/null || git diff --name-only --cached)

# Detect primary language from file extensions
PRIMARY_LANG=$(echo "$CHANGED_FILES" | grep -oE '\.[a-z]+$' | sort | uniq -c | sort -rn | head -1 | awk '{print $2}' | tr -d '.')
# Maps: java, py, ts, js, go, rs, etc.

# Categorize by type (language-agnostic patterns)
SOURCE_FILES=$(echo "$CHANGED_FILES" | grep -E '\.(java|py|ts|js|go|rs|c|cpp|cs)$' || true)
TEST_FILES=$(echo "$CHANGED_FILES" | grep -E '(Test|Spec|_test|_spec)\.' || true)
CONFIG_FILES=$(echo "$CHANGED_FILES" | grep -E '\.(json|yaml|yml|xml|properties|toml)$' || true)
```

<step name="analyze_context">

**Context-Aware Stakeholder Selection**

Analyze task context to determine which stakeholders are relevant, reducing token usage by skipping irrelevant reviewers.

### Selection Algorithm

```
RESEARCH MODE (pre-implementation):
1. Start with base set: [requirements, architect, security, quality, tester, performance, ux, sales, marketing, legal]
2. Filter based on the context of the changes.
```