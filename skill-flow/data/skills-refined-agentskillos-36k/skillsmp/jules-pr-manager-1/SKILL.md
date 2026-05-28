---
name: jules-pr-manager
description: Manage Google Jules PR lifecycle - batch investigation, reverse-order processing, and tiered decision presentation.
version: 3.1.0
---

# Jules PR Manager

## Core Principle

Your role:
1. Gather information using the scripts
2. Analyze and summarize findings
3. Present options with your recommendations

---

## Quick Reference

| Script | Purpose |
|:-------|:--------|
| `./summary.sh` | Overview of ALL open PRs (run first) |
| `./detail.sh <id>` | Deep dive on single PR |
| `./diff.sh <id1> [id2]` | Compare PRs for duplicates |
| `./merge.sh <id> [msg]` | Merge (USER APPROVAL REQUIRED) |
| `./close.sh <id> [msg]` | Close PR (USER APPROVAL REQUIRED) |
| `./request-changes.sh <id> <msg>` | Request fixes from Jules |
| `./mark-ready.sh <id>` | Convert Draft → PR |
| `./label.sh <id> <add\|remove> <label>` | Manage labels |

⚠️ Use scripts in `.gemini/skills/jules-pr-manager/`. Do not assemble `gh` commands manually.

---

## Workflow

### Step 1: Gather Data

Run `./summary.sh` and categorize PRs:

| Condition | Category |
|:----------|:---------|
| No labels | Unvetted (needs review) |
| `jules:copilot-review` + Copilot APPROVED + CI SUCCESS | Merge candidate |
| `jules:copilot-review` + Copilot commented | Needs feedback relay |
| `jules:copilot-review` + CI FAILURE | Needs CI fix |
| `jules:changes-requested` | Waiting on Jules |
| `mergeable: CONFLICTING` | Has conflicts |

**Duplicate Detection**: PRs with overlapping `files` arrays are likely duplicates.

### Step 2: Present Findings to User

Summarize what you found:
- How many PRs total, how many are Jules PRs
- Which are merge candidates
- Which appear to be duplicates (list the clusters)
- Which need attention (CI failures, stalled, conflicts)

### Step 3: Process One Decision at a Time

For each PR requiring action, present:

1. **The PR**: Number, title, what it does
2. **Your Analysis**: Is it a duplicate? Worth merging? Any concerns?
3. **Your Recommendation**: What you suggest and why
4. **Options**: Clear choices for the user

Example presentation:
```
**#796: Add indexes for issue severity and priority**

Analysis: This adds DB indexes for faster filtering. Appears to be
a duplicate of #794 (same files modified). #796 is newer.

Recommendation: Close #794 as duplicate, keep #796.

Options:
A) Close #794, keep #796 (recommended)
B) Close #796, keep #794
C) Keep both (explain why)
D) Close both
E) Need more info (I'll run detail.sh)
```

### Step 4: Execute Approved Actions

Only after user explicitly approves:
- Run the appropriate script(s)
- Report the result
- Move to the next decision

---

## Labels

| Label | Meaning |
|:------|:--------|
| `jules:copilot-review` | Vetted, waiting for Copilot |
| `jules:changes-requested` | Waiting for Jules fixes |
| `jules:agent-stalled` | >30m silence from Jules |
| `jules:merge-conflicts` | Has git conflicts |

No label = unvetted.

---

## Decision Types

### Duplicates
- Compare `files` arrays in summary output
- Use `./diff.sh <id1> <id2>` to confirm
- Present both PRs, recommend which to keep
- **User decides** which is the "keeper"

### Vetting (New PRs)
- Use `./detail.sh <id>` for full context
- Assess: Is this change valuable? Any risks?
- **User decides** approve or reject

### Merging
- Only for: vetted + Copilot approved + CI passing
- Present full summary of changes
- **User decides** to merge or not

### Closing
- For duplicates or rejected PRs
- Explain why you recommend closing
- **User decides** to close or not

---

## Jules Detection

Jules PRs have `author: "google-labs-jules[bot]"` in summary output.


