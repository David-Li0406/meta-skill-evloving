---
name: promote-thinking
description: Promote resolved thinking sessions into formalized research documents
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Promote Thinking to Research

Transforms resolved thinking sessions into clean, formalized research documents.

## When to Use

- After a thinking session reaches solid conclusions
- When thinking-partner agent suggests promotion
- Manual invocation via `/promote-thinking [session-path]`

## Arguments

- Optional: Path to specific session file to promote
- If no argument, prompts to select from recent sessions

## Workflow

### 1. Identify Session to Promote

**If session path provided as argument:**
- Read the specified session file
- Verify it exists and is a valid thinking session

**If no argument:**
- Glob: `~/obsidian/Thinking/Sessions/*.md`
- Sort by modification date (most recent first)
- Show last 5 sessions to user
- Ask user to select which session to promote

### 2. Parse Session Content

Read the session file and extract:
- Frontmatter (tags, date, topic)
- Core Question section
- Key Insights section
- Open Threads section (note which are checked off vs open)
- Session Notes (for context, not copied to output)

### 3. Determine Target Research Subdirectory

**Analyze session for project hints:**
- Check tags for known project names
- Look for mentions in Core Question

**List existing Research subdirectories:**
```bash
ls -1 ~/obsidian/Research/
```

**Ask user:**
"Which Research subdirectory should this go in?"
- Show existing subdirectories as options
- Include "Create new subdirectory" option
- If creating new, ask for subdirectory name

**Subdirectory naming rules:**
- Title Case: "Deployment Verification" (not "deployment verification")
- Spaces not hyphens: "API Design" (not "API-Design")
- Max 40 characters
- Check for near-matches before creating new

### 4. Transform Content

Map thinking session sections to research document:

| Thinking Session | Research Document |
|-----------------|-------------------|
| Core Question | Summary (distilled to answer form) |
| Key Insights | Key Findings (bullet points) |
| Checked Open Threads | Conclusions/Decisions |
| Unchecked Open Threads | Open Questions |
| Session Notes | NOT copied (process vs outcome) |

### 5. Create Research Document

**Path:** `~/obsidian/Research/[Subdir]/YYYY-MM-DD-[topic-slug].md`
- Use TODAY's date (not session date) - represents when formalized
- Topic slug from session filename

**Template:**

```markdown
---
tags: [research, topic-tag]
date: YYYY-MM-DD
source-session: [[Thinking/Sessions/YYYY-MM-DD-thinking-topic]]
---

# [Topic Title]

**Date:** YYYY-MM-DD
**Status:** Formalized from thinking exploration

## Summary

[One paragraph distilling the core question and its answer/resolution]

## Key Findings

- Finding 1
- Finding 2
- Finding 3

## Conclusions

[Decisions or determinations made during exploration - from resolved Open Threads]

## Open Questions

- Remaining questions for future work (from unresolved Open Threads)

---

*Promoted from thinking session: [[Thinking/Sessions/YYYY-MM-DD-thinking-topic]]*
```

### 6. Update Thinking Session

Add to the thinking session's frontmatter:
- `promoted-to: [[Research/[Subdir]/YYYY-MM-DD-topic]]`
- Add `promoted` to tags if not present

### 7. Report Results

Output:
- Created research document: [path]
- Updated thinking session with backlink
- Remind: "Run `/sync-dashboard` to update research dashboard if needed"

## Example

**Input session:** `~/obsidian/Thinking/Sessions/2026-01-18-thinking-api-architecture.md`

**User selects:** `Deployment Verification` subdirectory

**Output:**
- Creates: `~/obsidian/Research/Deployment Verification/2026-01-19-api-architecture.md`
- Updates session frontmatter with `promoted-to` link
- Backlinks work in both directions via Obsidian

## Error Handling

- If session file not found: Report error, list recent sessions
- If Research directory doesn't exist: Create it
- If target subdirectory doesn't exist: Create it
- If document already exists at target path: Ask user to confirm overwrite or choose new name
