---
name: jacked
description: Search and load context from past Claude Code sessions. Use when: user mentions a past project like "configurator" or other previous work, asks to continue/resume previous work, says "how did I do X before", references past sessions, or starts work on a feature that may have been done before.
---

# Jacked

Search and load context from past Claude Code sessions using semantic search.

## Usage

```
/jacked <description of what you want to work on>
```

Example:
```
/jacked implement overnight OB time handling
```

## How It Works

1. Takes your description and searches for similar past sessions
2. Shows matching sessions with relevance scores and content indicators
3. You pick which session(s) to load context from
4. Uses **smart mode** by default - loads plan files, agent summaries, and key user messages (NOT the full transcript which would blow up context)
5. If the session exists locally, suggests native Claude resume as an option

## Instructions for Claude

When the user runs `/jacked <description>`, follow these steps:

### Step 1: Search for Similar Sessions

Run the search command:

```bash
jacked search "<user's description>" --limit 5
```

The output includes:
- Relevance score (percentage)
- User (YOU or @username for teammates)
- Age (relative time like "24 days ago")
- Repository name
- Content indicators: 📋 = has plan file, 🤖 = has agent summaries
- Preview of matched content

### Step 2: Present Results Using AskUserQuestion

Use the AskUserQuestion tool with multiSelect=true to let the user pick which sessions to load:

```json
{
  "questions": [{
    "question": "Which sessions would you like to load context from?",
    "header": "Sessions",
    "multiSelect": true,
    "options": [
      {
        "label": "1. YOU - 24d ago 📋🤖",
        "description": "hank-coder: Implementing overnight time calculation..."
      },
      {
        "label": "2. @bob - 3mo ago 🤖",
        "description": "hank-coder: Time handling refactor for multiple..."
      },
      {
        "label": "3. YOU - 2d ago",
        "description": "krac-llm: Staff time merging edge cases..."
      },
      {
        "label": "None - skip",
        "description": "Don't load any previous context"
      }
    ]
  }]
}
```

Note: AskUserQuestion supports max 4 options, so if there are 5+ results, show top 3 + "None" option.

### Step 3: Retrieve Selected Sessions

When the user selects one or more sessions:

```bash
# Default: smart mode (recommended) - plan + summaries + labels + user msgs
jacked retrieve <session_id> --mode smart

# For full transcript (use sparingly - can be 50K+ chars)
jacked retrieve <session_id> --mode full
```

Smart mode retrieval output includes:
- Session metadata with relative age
- Token budget accounting
- Plan file content (if exists)
- Subagent summaries (exploration/planning results)
- Summary labels (chapter titles)
- First few user messages

### Step 4: Handle Based on Session Location

**If session is local:**
Tell the user:
```
This session exists locally on your machine!
To resume it natively (with full Claude memory), run in a new terminal:

claude --resume <session_id>

Or I can inject the smart context into our current conversation.
Would you like me to inject it here? (yes/no)
```

**If session is remote only:**
Tell the user:
```
This session is from another machine (<machine_name>).
I'll inject the context into our conversation.
```

### Step 5: Context Injection with Staleness Warning

The retrieve output already includes proper formatting with staleness warnings.

**For context older than 7 days, include the staleness warning** that appears in the output:
- 7-30 days: Mild warning - "Code may have changed"
- 30-90 days: Medium warning - "Use as starting point for WHERE to look"
- 90+ days: Strong warning - "Treat as historical reference only"

After injection, summarize:
1. What the previous session covered
2. Key decisions or implementations found
3. Ask what the user wants to work on now

## Retrieval Modes

| Mode | What's Included | When to Use |
|------|-----------------|-------------|
| smart | Plan + agent summaries + labels + user msgs | Default - best balance |
| plan | Just the plan file | Quick strategic overview |
| labels | Just summary labels (tiny) | Quick topic check |
| agents | All subagent summaries | Deep dive into exploration results |
| full | Everything including transcript | Need full details (use sparingly) |

## Error Handling

- If search returns no results: "No matching sessions found. Try a different description or run `jacked backfill` to index your sessions."
- If retrieve fails: "Session not found in index. It may have been deleted or the session ID is invalid."
- If jacked command not found: "jacked not installed or not on PATH. Run `pipx install claude-jacked` to install."

## Notes

- Sessions are indexed automatically via a Stop hook (after each Claude response)
- **New in v0.2.6**: Indexes plan files, subagent summaries, and summary labels for smarter retrieval
- Smart mode prevents context explosion by returning ~5-10K tokens instead of 50-200K
- The index is stored in Qdrant Cloud, accessible from any machine
- Local sessions can be resumed natively with `claude --resume` for the best experience
- Remote sessions are retrieved and injected as context (works but Claude won't have internal memory state)
- Use `jacked cleardb` to wipe your data before re-indexing with a new schema
