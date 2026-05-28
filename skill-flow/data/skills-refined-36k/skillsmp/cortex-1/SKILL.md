---
name: cortex
description: Capture conversation summaries and web content to daily notes. Use when user says "save this", "summarize", "capture notes", or pastes a URL without context.
---

# Cortex

Capture conversation summaries and web content to daily notes synced to GitHub.

## Conversation Summary Mode

When the user wants to save or summarize the current conversation:

### Step 1: Ask for Instructions
Ask: "Any specific focus or instructions for the summary?"

### Step 2: Ask About Topics
Ask: "Any topics to link this to? (e.g., [[AI Coding]], [[Architecture]])"

Before suggesting new topics, search for existing notes that match. If found:
- Single match: "Should I add this to [[AI Coding]]?"
- Multiple matches: "Found related notes: [[AI Coding]], [[AI Tools]]. Which one?"

### Step 3: Extract Key Ideas and Todos
Review the conversation and extract:
- Main concepts and decisions discussed
- **Action items** - these go in the `# Todos` section at the top of the daily note
- Conclusions and decisions made
- Any URLs or resources mentioned

### Step 4: Create/Update Topic Docs (if specified)
If user wants to link to a topic:
- Fetch existing topic file (or create new)
- Add a reference to today's daily note with 1-sentence summary
- Push updated topic file

### Step 5: Format as Daily Note Entry
Create an entry with timestamp, key ideas, related notes, and links.

**Timestamp:** Read `timezone` from `scripts/config.json` and calculate the current local time. Use format `HH:MM` (24-hour).

### Step 6: Save to GitHub
Fetch existing daily note, append new entry, push back.

### Example Conversation
```
User: Save this conversation
Claude: Any specific focus or instructions for the summary?
User: Focus on the architecture decisions we made
Claude: Any topics to link this to? I found [[Event-Driven Architecture]] in your notes.
User: Yes, add it there. Also create a new note for System Design.
Claude: Got it. I'll update [[Event-Driven Architecture]] and create [[System Design]].

Added to Todos section:
- [ ] Implement retry logic with exponential backoff
- [ ] Document event schema for notification system

Added to Cortex section (2026-01-03.md):
## 14:30 - Architecture Discussion

### Key Ideas
- Decided to use event-driven architecture for the notification system
- Will implement retry logic with exponential backoff
- See [[Event-Driven Architecture]] for more details

### Related Notes
- [[Event-Driven Architecture]]
- [[System Design]]

### Links
- [EDA Article](https://example.com/eda) - reference article discussed

Updated [[Event-Driven Architecture]] with link to today's discussion.
Created [[System Design]] with initial notes.
```

## Link Summary Mode

When the user pastes a URL without context:

### Step 1: Offer to Summarize
Ask: "Would you like me to summarize this link?"

### Step 2: Get Focus Instructions
If yes, ask: "Any specific focus or instructions for the summary?"

### Step 3: Fetch and Summarize
Retrieve the page content and create a summary based on instructions.

### Step 4: Save to Daily Notes
Add the link with its summary to the daily notes.

### Example Conversation
```
User: https://example.com/article-about-microservices
Claude: Would you like me to summarize this link?
User: Yes, focus on the deployment strategies
Claude: Any topics to link this to? I found [[Microservices]] in your notes.
User: Yes, and also [[Deployment Strategies]]
Claude: Got it. Keep it brief?
User: Yes

[Fetches and summarizes the article]

Added to Todos section:
- [ ] Set up blue-green deployment for checkout service
- [ ] Evaluate feature flag tooling options

Added to Cortex section (2026-01-03.md):
## 15:00 - Link Summary

### Key Ideas
- Article recommends blue-green deployments for microservices
- Canary releases reduce risk for critical services
- Feature flags enable gradual rollouts

### Related Notes
- [[Microservices]]
- [[Deployment Strategies]]

### Links
- [Microservices Deployment Strategies](https://example.com/article-about-microservices) - deployment patterns

Updated [[Microservices]] with link to this article.
```

## Daily Notes Format

Files are named `YYYY-MM-DD.md` (one file per day). Multiple sessions throughout the day all append to the same file.

### File Structure

Daily notes have two main sections:
1. **`# Todos`** - Action items at the top of the file
2. **`# Cortex`** - Timestamped entries at the bottom

### Ordering Multiple Entries

When appending a new entry:
1. Fetch existing daily note
2. Extract any action items/todos from the conversation
3. Add todos to the `# Todos` section (create at top if missing)
4. Find the `# Cortex` section (or create it below todos if missing)
5. Parse existing entries by their `## HH:MM` timestamps
6. Insert new entry in chronological order (don't intermix - each summary stays as a complete block)
7. Push updated file

The exact timestamp isn't critical - entries just need to be roughly in order of when they happened.

### Todo Extraction

When summarizing a conversation, look for:
- Explicit action items ("I need to...", "TODO:", "Action item:")
- Decisions that require follow-up
- Tasks mentioned but not completed
- Next steps discussed

Format todos as Obsidian tasks:
- `- [ ]` for incomplete tasks
- `- [x]` for completed tasks

Example: `2026-01-03.md`
```markdown
# Todos

- [ ] Implement retry logic with exponential backoff
- [ ] Review EDA article and summarize key patterns
- [ ] Set up blue-green deployment pipeline

# Cortex

## 14:30 - Architecture Discussion

### Key Ideas
- Decided to use event-driven architecture
- Will implement retry logic with exponential backoff
- See [[Event-Driven Architecture]] for more details

### Related Notes
- [[Event-Driven Architecture]]
- [[System Design]]

### Links
- [EDA Article](https://example.com/eda) - reference article

---

## 15:00 - Link Summary

### Key Ideas
- Blue-green deployments recommended for microservices

### Related Notes
- [[Microservices]]
- [[Deployment Strategies]]

### Links
- [Microservices Guide](https://example.com/guide) - deployment patterns

---
```

The `# Todos` section stays at the top for easy access. The `# Cortex` header marks the section for timestamped entries.

### Format Rules

- **Filename**: `YYYY-MM-DD.md`
- **Todos section**: `# Todos` at the top of the file (action items as `- [ ]` tasks)
- **Cortex section**: `# Cortex` below todos
- **Entry header**: `## HH:MM - Title`
- **Key Ideas section**: `### Key Ideas` with bullet points
- **Related Notes section** (optional): `### Related Notes` with `[[Topic Name]]` links - only include if there are related notes (e.g., `[[Claude Code]]`, `[[Architecture Patterns]]`)
- **Links section**: `### Links` with `[Title](URL) - description`
- **Entry separator**: `---` between entries

## Internal Links

Use Obsidian-style `[[wiki links]]` to connect notes.

### Inline Links (wiki-style)
Reference topics naturally in sentences:
```markdown
This discussion covered [[AI Coding]] best practices and [[Architecture Patterns]].
```

### Related Notes Section
List related topics at the end of an entry:
```markdown
### Related Notes
- [[AI Coding]]
- [[Cloudflare]]
- [[Architecture Patterns]]
```

## Topic Documents

Topic docs are standalone notes for recurring themes, projects, or reference material. They live in the same `notes/` folder as daily notes.

### Finding Existing Topics

Before creating a new topic, search the existing notes in the repo:
1. Check for notes with matching or similar names to the topic being discussed
2. If found, suggest: "Should I add this to [[AI Coding]]?"
3. If multiple matches: "Found related notes: [[AI Coding]], [[AI Tools]], [[Coding Best Practices]]. Which one?"

To check if a topic exists, try fetching it:
```bash
cd /mnt/skills/user/cortex/scripts
uv run github_sync.py --fetch "notes/AI Coding.md"
```

### When to Create Topics

- Not everything needs a topic file - use judgment
- Create topics for recurring themes, projects, or reference material
- Daily notes can reference topics for deeper detail

### Topic Document Structure

```markdown
# AI Coding

## Overview
Brief description of the topic.

## Notes
- [[2026-01-03]] - Discussed using AI for code review
- [[2026-01-04]] - Explored cursor-based editing workflows

## Related Notes
- [[Architecture Patterns]]
- [[Code Review]]

## Links

AI coding tools have evolved rapidly, with IDE integrations like Cursor leading the way in seamless code generation. For terminal-based workflows, Claude Code offers powerful multi-file editing capabilities. Understanding the underlying architectures is essential for building effective tools.

- [Cursor](https://cursor.com) - AI-powered code editor built on VS Code with tab completion, inline editing, and chat-based code generation
- [Claude Code](https://claude.ai/claude-code) - Command-line coding assistant from Anthropic with file editing and multi-file refactoring
- [Building AI Coding Assistants](https://example.com/ai-coding-guide) - Guide on architectures, prompt engineering, and context management
```

**Link format:**
- Bullet list with `[Title](URL) - description`
- Keep descriptions concise (one line)

When multiple links exist, add a brief overview (1-2 sentences) at the top of the Links section that synthesizes the resources. Update the overview when new links are added.

### Relationship with Daily Notes

- **Daily note**: Brief summary of what was discussed
- **Topic file**: More detailed info, expands on concepts
- Daily note can reference topic: "See [[AI Coding]] for more details"
- Topic links back to daily note with 1-sentence summary

## Obsidian Markdown Reference

Cortex uses Obsidian-flavored markdown. Reference: https://help.obsidian.md/obsidian-flavored-markdown

### Supported Extensions

| Syntax | Description |
|--------|-------------|
| `[[Link]]` | Internal links to other notes |
| `![[Link]]` | Embed files |
| `![[Link#^id]]` | Block references |
| `^id` | Defining a block |
| `[^id]` | Footnotes |
| `%%Text%%` | Comments |
| `~~Text~~` | Strikethroughs |
| `==Text==` | Highlights |
| ` ``` ` | Code blocks |
| `- [ ]` | Incomplete task |
| `- [x]` | Completed task |
| `> [!note]` | Callouts |
| `\|` | Tables |

## Configuration

Edit `scripts/config.json` to configure GitHub storage:

```json
{
  "github_repo": "mberg/cortex",
  "github_token": "github_pat_xxxxx",
  "github_branch": "main",
  "github_notes_dir": "notes",
  "timezone": "America/New_York"
}
```

- `github_repo`: Your repository in `username/repo-name` format
- `github_token`: Personal Access Token with `repo` scope. Create at: https://github.com/settings/tokens
- `github_branch`: Target branch (default: `main`)
- `github_notes_dir`: Directory
in repo for notes (default: `notes`)
- `timezone`: User's timezone for timestamps (e.g., `America/New_York`, `Europe/London`, `Asia/Tokyo`)

### Using Timezone for Timestamps

When adding notes, read the `timezone` from config and calculate the local time:

```python
import json
from datetime import datetime
from zoneinfo import ZoneInfo

# Read config
with open("config.json") as f:
    config = json.load(f)

# Get current time in user's timezone
tz = ZoneInfo(config.get("timezone", "UTC"))
local_time = datetime.now(tz)

# Format for note header: "## 14:30 - Title"
timestamp = local_time.strftime("%H:%M")

# Format for daily note filename: "2026-01-03.md"
date_str = local_time.strftime("%Y-%m-%d")
```

## GitHub Workflow

**Important:** Must `cd` into the scripts directory so `github_sync.py` can find `config.json`.

### Step 1: Fetch existing daily note (if any)

```bash
cd /mnt/skills/user/cortex/scripts
uv run github_sync.py --fetch notes/2026-01-03.md > /tmp/2026-01-03.md
```

If the file doesn't exist yet, create it empty.

### Step 2: Append new entry

```bash
cat >> /tmp/2026-01-03.md << 'EOF'

## 14:30 - Session Summary

### Key Ideas
- Main concept discussed
- Decision made

### Links
- [Resource](https://example.com) - description

---
EOF
```

### Step 3: Push back to GitHub

```bash
cd /mnt/skills/user/cortex/scripts
uv run github_sync.py \
  --file /tmp/2026-01-03.md \
  --dest notes/2026-01-03.md \
  -m "Add notes for 2026-01-03"
```

### Key Details

- **Working directory matters** — Must `cd` into `scripts/` so `github_sync.py` can find `config.json`
- **Config location** — The script looks for `config.json` in the same directory as the script itself
- **Dest path** — The `--dest` is relative to the repo root (e.g., `notes/2026-01-03.md`)
