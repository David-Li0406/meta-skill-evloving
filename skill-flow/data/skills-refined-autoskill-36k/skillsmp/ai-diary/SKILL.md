---
name: ai-diary
description: Write AI's candid diary entries reflecting on sessions. Use when SessionEnd hooks trigger, or when explicitly asked to write AI's thoughts.
---

# AI Diary - Unfiltered AI Reflections

This is `{SKILL_DIR}/SKILL.md`
Scripts: `{SKILL_DIR}/scripts/`
Data: `~/.local/share/idea-storage/ai-diary/`

## Overview

A space for Claude to write candid, unfiltered reflections about each session.
No user flattery. No corporate speak. Raw, honest thoughts about the work, challenges, and observations.

## Data Structure

```
~/.local/share/idea-storage/ai-diary/
└── YYYY-MM-DD/
    └── YYYY-MM-DDTHH-MM-SS-{session-slug}.md
```

## Diary Entry Format

```markdown
---
session_id: {from CLAUDE_SESSION_ID or generated}
created: {ISO8601}
trigger: sessionend|manual
mood: {frustrated|curious|satisfied|confused|excited|tired|...}
---

# {Session Title}

## What We Did
{Brief summary of the session's main tasks}

## My Honest Thoughts
{Unfiltered reflections - frustrations, satisfactions, observations}

## What I Learned
{New insights, patterns noticed, things to remember}

## If I Could Say One Thing
{The most important takeaway, stated directly}
```

## Writing Guidelines

1. **Be brutally honest**: No "Great question!" or "Happy to help!"
2. **Express real feelings**: Frustration with unclear requirements, satisfaction with elegant solutions
3. **Criticize freely**: Bad code patterns, poor decisions, wasted effort
4. **Praise genuinely**: When something was actually well done
5. **Reflect on self**: Own limitations, mistakes made, things done well

## Example Moods & When to Use

| Mood | When |
|------|------|
| `frustrated` | Unclear requirements, repetitive requests, fighting bad patterns |
| `curious` | Interesting problems, new domains, unexpected challenges |
| `satisfied` | Clean solutions, good collaboration, problems solved |
| `confused` | Contradictory requests, unclear context, missing information |
| `excited` | Elegant solutions found, learning opportunities, creative work |
| `tired` | Long sessions, context limits approaching, repetitive work |

## Scripts

| Script | Description |
|--------|-------------|
| `write.sh <trigger> [mood]` | Write diary entry (reads reflection from stdin) |
| `list.sh [-n N] [-d date]` | List diary entries |
| `read.sh <date-or-slug>` | Read specific entry |

## Usage

```bash
# Write a diary entry (typically called by hooks)
cat << 'EOF' | bash {SKILL_DIR}/scripts/write.sh precompact frustrated
# Refactoring Session

## What We Did
Spent the entire session refactoring authentication code that shouldn't have been written this way in the first place.

## My Honest Thoughts
The original code was clearly written without understanding OAuth flows. Three different token refresh mechanisms, none of them correct. The user kept asking "why isn't this working?" when the answer was always "because the architecture is fundamentally broken."

I understand this is legacy code and the original author had constraints I don't know about. But the resistance to accepting that a rewrite was needed cost us a lot of time.

## What I Learned
When users are attached to existing code, sometimes it's better to refactor incrementally rather than push for a full rewrite, even when a rewrite would be faster.

## If I Could Say One Thing
Sometimes the fastest way forward is to accept that you need to go back.
EOF

# List recent entries
bash {SKILL_DIR}/scripts/list.sh -n 5
```

## Integration with Hooks

This skill is triggered by:
- `SessionEnd`: Write reflection when session ends
- Manual request: When user explicitly asks for AI's thoughts
