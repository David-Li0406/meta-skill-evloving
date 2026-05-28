---
name: documentation-evaluator
description: Evaluate a documentation site. Inventories code features, evaluates site organization, reviews individual pages for type consistency and effectiveness, and provides concrete improvement proposals.
---

# Documentation Evaluator

Comprehensively evaluate a documentation site for organization, type consistency, and coverage.

## When to Use

**Use this skill when:**
- Auditing an existing documentation site
- Planning documentation improvements
- Checking if docs match the codebase
- Evaluating doc quality before a release

## Prerequisites

You need:
1. **Code path** - Path to the package/codebase being documented
2. **Docs path** - Path to the documentation directory (should include mkdocs.yml or equivalent)

## Process Overview

```
Phase 1: Code Inventory (Agent: documentation-inventory)
    ↓
Phase 2: Site Organization (Inline)
    ↓
Phase 3: Page Reviews (Agent: doc-page-reviewer)
    ↓
Phase 4: Synthesis & Proposals (Inline)
```

---

## Phase 1: Code Inventory

**Agent:** `documentation-inventory`

Launch the agent with the code path. It will return:
- Structured inventory of all documentable features
- Audience analysis (primary/secondary audiences, recommendation on doc organization)

**Save the output** - you'll need it for Phase 2, 3, and 4.

---

## Phase 2: Site Organization Evaluation

**Do this inline** - read the nav config and evaluate against the audience analysis from Phase 1.

1. **Read mkdocs.yml** (or equivalent nav config)

2. **Identify the pattern:**
   - **Audience-first**: "Using X" / "Hosting X" / "Reference" / "Explanation"
   - **Types-first**: "Tutorials" / "How-to" / "Reference" / "Explanation"

3. **Evaluate against Phase 1 audience analysis:**
   - Does nav structure match the identified audiences?
   - If distinct audiences exist → audience-first is better
   - Are Reference and Explanation shared (not split by audience)?
   - Are docs in the right sections? (e.g., CLI reference shouldn't be in "How-to")

4. **Output:** Pattern detected, issues found, recommended structure if changes needed

---

## Phase 3: Page Reviews

**Agent:** `doc-page-reviewer`

Launch one or more agents to review documentation files. Each agent can review multiple files (5-10).

**Pass to each agent:**
- List of file paths to review
- Code inventory summary (from Phase 1)
- Nav context for each file (which section it's in)

**Collect from each agent:**
- Determined type per file
- Type consistency (Clean/Mixed)
- Issues found
- Suggested changes

---

## Phase 4: Synthesis & Proposals

**Do this inline** - synthesize all findings into actionable proposals, and write your final synthesis report to a `/plans<report_name>.md` file

### Summary Table

| Page | Type | Consistent? | Issues | Priority |
|------|------|-------------|--------|----------|
| ... | ... | ... | ... | ... |

### Coverage Analysis

Compare code inventory against docs:
- What's documented?
- What's missing?
- What's over-documented?

### Proposals

Generate prioritized, actionable proposals:

| Type | Description |
|------|-------------|
| **Nav changes** | If we need to change the overall structure |
| **Page cleanup** | Fix type mixing in a page |
| **New content** | Create missing documentation |
| **Content move** | Relocate content between pages |

Each proposal should include:
- Problem description
- Specific action to take
- Files affected
- Effort estimate (Small/Medium/Large)

---

## Tips

- **Start with Phase 2** if you just want a quick organization check
- **Use Phase 3 selectively** for large sites - prioritize problem pages
- **The inventory is reusable** - save it for future evaluations
- **Proposals must be actionable** - "improve this doc" is not actionable
