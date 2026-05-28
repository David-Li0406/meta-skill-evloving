---
name: obsidian-save
description: |
  Save current session context to Obsidian vault. INVOKE THIS SKILL when user:
  - Says "save to obsidian", "note this to obsidian", "add to vault"
  - Wants to capture session insights to their notes
  - Says "save this session", "dump to obsidian"
  - Asks to "create a note from this conversation"
  - Mentions wanting to remember or archive the current discussion
  Trigger phrases: "save to obsidian", "note this", "add to vault", "save session", "dump to notes", "obsidian note"
allowed-tools: Bash, Write
---

# obsidian-save - Save Session to Obsidian

Capture current session context as a note in the Obsidian vault.

## When to Use

Use when user wants to save conversation insights, decisions, or context to their Obsidian knowledge base.

## Process

1. **Parse user prompt**: The text accompanying the skill invocation guides the note:
   - **Focus areas**: "just the debugging steps", "only architecture decisions"
   - **Exclusions**: "skip the failed attempts", "don't include the tangents"
   - **Structure**: "as a how-to guide", "as bullet points", "as a decision log"
   - **Title**: Extract explicit title if given, otherwise derive from topic

2. **Generate filename**: `YYYY-MM-DDTHH-MM-SS-<slug>.md`
   - Use provided title as slug, or derive from session topic
   - Slugify: lowercase, hyphens for spaces, no special chars

3. **Summarize session** based on user's direction:
   - Default (no direction): decisions, solutions, key insights, action items
   - With direction: prioritize what user asked for, shape content accordingly
   - Use concise bullet points unless user requests different structure

4. **Create note** at `~/obsidian/Notes/<filename>`:

```markdown
---
date: <ISO8601 timestamp>
daily: [[YYYY-MM-DD]]
tags:
  - claude-session
source: claude-code
---

# <Title>

## Summary

<Bulleted summary of session>

## Details

<Any additional context, code snippets, or specifics worth preserving>
```

5. **Confirm**: Echo the full path and brief summary of what was captured.

## Prompt Steering

The user's prompt is your primary guide. Examples:
- **Title**: "save to obsidian: webpack config fixes" → title is "webpack-config-fixes"
- **Focus**: "just the solution" → skip context, emphasize what worked
- **Format**: "as a checklist" → use `- [ ]` items instead of prose
- **Filter**: "only the API changes" → exclude unrelated discussion

When no direction given, default to a balanced summary of key outcomes.

## Examples

| User says | Action |
|-----------|--------|
| "save this to obsidian" | Summarize full session, auto-generated title |
| "note this discussion about auth" | Save with title "auth" as slug |
| "save to obsidian, focus on the fix we found" | Emphasize the solution, minimize context |
| "add to vault as a how-to guide for setting up the dev env" | Structure as step-by-step guide, not bullet summary |
| "dump to obsidian, just the architecture decisions we made" | Filter to only architectural choices |
| "save session, skip the debugging tangents" | Omit failed attempts, focus on outcomes |

## Notes

- Always include `daily: [[YYYY-MM-DD]]` for today's date to create backlink
- Keep summaries focused on actionable/memorable content
- Include code snippets only if they're the key takeaway
