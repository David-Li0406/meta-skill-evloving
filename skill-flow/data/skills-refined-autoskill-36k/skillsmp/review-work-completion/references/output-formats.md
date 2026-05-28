# Output Formats

## Contents

- [Agent Output Format](#agent-output-format-single-source-of-truth)
- [Consolidation Rules](#consolidation-rules)
- [Consolidated Findings Table](#consolidated-findings-table)
- [Issue Documentation Format](#issue-documentation-format)
- [Task Description Format](#task-description-format)
- [Review Summary Format](#review-summary-format)
- [Zero Issues Handling](#zero-issues-handling)
- [Review File Format](#review-file-format)

## Agent Output Format (Single Source of Truth)

Each agent outputs issues in this exact format:

```
[{AGENT_NAME}] {emoji} {description} | File: {path or "N/A"} | Task: {id or "general"}
```

**Severity emojis:** 🔴 Critical, 🟠 High, 🟡 Medium, ⚪ Low

**Rules:**
- One issue per line
- Use "N/A" for file if issue is architectural/cross-cutting
- Use "general" for task if issue spans multiple tasks or is a PRD gap
- If zero issues found: `[{AGENT_NAME}] ✅ No issues found`

**Examples:**
```
[ALICE] 🔴 SQL injection in query builder | File: src/db/query.ts | Task: 3
[BOB] 🟠 Missing error handling strategy | File: N/A | Task: general
[CARL] 🟡 PRD section 2.3 not implemented | File: N/A | Task: 5
```

## Consolidation Rules

Parse agent outputs and merge:

1. **Normalize** - Match similar issues by file+description
2. **Score by consensus**:
   - `[3/3]` - all agents, highest priority
   - `[2/3]` - majority, high priority
   - `[1/3]` - single agent, normal priority
3. **Deduplicate** - Keep best description, note which agents found it

## Consolidated Findings Table

| Consensus | Severity | Issue | File | Found By |
|-----------|----------|-------|------|----------|
| [3/3] | 🔴 Critical | XSS in input handler | src/input.ts | Alice, Bob, Carl |
| [2/3] | 🟠 High | Missing null check | src/api.ts | Alice, Bob |
| [1/3] | 🟡 Medium | No test coverage | src/utils.ts | Carl |

## Issue Documentation Format

```
- {severity emoji} {description}
  - File: {path}
  - Task: {task ID}
  - PRD ref: {section if applicable}
  - Found by: {agent list}
```

## Task Description Format

```
Fix: {issue summary}

Issues addressed:
- {issue 1}
- {issue 2}

Found by: {agents}
Severity: {🔴/🟠/🟡/⚪}

Acceptance criteria:
- [ ] {criterion 1}
- [ ] {criterion 2}
```

## Review Summary Format

```
## Review Summary

Reviewed: {N} completed tasks
PRDs checked: {list}

### Agent Status
- Alice: ✅ Available | ⚠️ Unavailable: {reason}
- Bob: ✅ Available | ⚠️ Unavailable: {reason}
- Carl: ✅ Available | ⚠️ Unavailable: {reason}

## Consolidated Findings

### [3/3] Full Consensus
- [3/3] 🔴 {issue} | {file} | Found by: Alice, Bob, Carl

### [2/3] Majority Consensus
- [2/3] 🟠 {issue} | {file} | Found by: Alice, Bob

### [1/3] Single Agent
- [1/3] 🟡 {issue} | {file} | Found by: Carl

## Follow-up Tasks Created

1. {task title} (S/M/L) - 🔴 consensus - addresses X, Y
2. {task title} (S/M/L) - 🟠 consensus - addresses Z

_If no issues found: "✅ No follow-up tasks needed. All reviewers passed the implementation."_
```

## Zero Issues Handling

When consolidation yields no issues:
- Skip task creation entirely (don't create empty/placeholder tasks)
- In review summary, note: "✅ All agents passed - no issues found"
- Still save the review file (documents the clean review)
- Report success to user with agent consensus on passing

## Review File Format

Location: `.local/reviews/<prd-filename-without-ext>-review-<NN>.md`

Example: PRD `00004-exchanger-web-ui-v1.md` → review `00004-exchanger-web-ui-v1-review-01.md`

```yaml
---
prd: .local/prds/wip/<prd-filename>
review: 1
date: YYYY-MM-DD
agents:
  alice: available
  bob: available
  carl: unavailable
---

# Review: <prd-name>

{review summary content}
```
