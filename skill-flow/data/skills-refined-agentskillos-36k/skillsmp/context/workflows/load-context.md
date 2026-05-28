# Load Context Workflow

**Trigger:** "load context for X", "get project context", "what do I know about X"

## Purpose
Load project-specific or topic-specific context from Obsidian vault into the current Claude Code session.

## Steps

### 1. Identify Context Scope
Determine what context to load:
- Project name (e.g., "PAI", "api-redesign")
- Topic area (e.g., "kubernetes", "authentication")
- Time period (e.g., "recent meetings", "last week")

### 2. Search for Relevant Notes

```bash
# Tag-based search for project
~/.claude/bin/obs/obs-wrapper search --tag "project/<name>"

# Semantic search for topic
~/.claude/bin/obs/obs-wrapper semantic "<topic>" --limit 10

# Recent notes if time-based
~/.claude/bin/obs/obs-wrapper recent --limit 20
```

### 3. Load and Summarize

For each relevant note:
1. Read the full content
2. Extract key information:
   - Decisions made
   - Open questions
   - Action items
   - Important references

### 4. Present Context

Structure the loaded context:

```markdown
## Project Context: <name>

### Key Decisions
- Decision 1: rationale
- Decision 2: rationale

### Open Questions
- Question 1
- Question 2

### Related Notes
- [[Note 1]] - brief description
- [[Note 2]] - brief description

### Recent Activity
- Date: activity summary
```

### 5. Offer Follow-up

- "Would you like me to read any of these notes in full?"
- "Should I search for something more specific?"
- "Want me to create a summary note?"

## Example

**User:** "Load context for the PAI project"

**Execution:**
```bash
obs search --tag "project/pai"
obs semantic "personal AI infrastructure" --limit 5
```

**Output:**
```
## Project Context: PAI

### Key Decisions
- Using Skills-as-Containers pattern (decided 2025-10-31)
- Telegram for multi-device capture
- SQLite for local state management

### Open Questions
- iOS Shortcuts implementation approach
- Backup strategy for embeddings DB

### Related Notes
- [[PAI Architecture]] - System design overview
- [[Context Management Skill]] - Implementation plan
- [[Telegram Bot Setup]] - Configuration notes

### Recent Activity
- 2025-12-02: Implemented Phase 4 multi-modal processing
- 2025-12-01: Completed semantic search embeddings
```
