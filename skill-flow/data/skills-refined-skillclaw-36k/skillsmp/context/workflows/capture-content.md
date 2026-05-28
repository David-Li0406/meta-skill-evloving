# Capture Content Workflow

**Trigger:** "save this to obsidian", "capture this", "add to my notes", "create a note"

## Purpose
Capture content from the current conversation or provided input directly to Obsidian vault.

## Workflow Steps

### 1. Determine Content Type

What are we capturing?
- **Conversation insight** - Summary of discussion
- **Decision** - Architectural or design decision
- **Code snippet** - Useful code with explanation
- **Reference** - External resource or documentation
- **Meeting notes** - Discussion summary
- **Quick thought** - Brief idea to process later

### 2. Extract/Format Content

Based on type, structure the content:

**Decision:**
```markdown
# [Decision Title]

## Context
What prompted this decision?

## Decision
What was decided?

## Rationale
Why this approach?

## Alternatives Considered
- Option A: pros/cons
- Option B: pros/cons

## Consequences
What this means going forward
```

**Code Snippet:**
```markdown
# [Descriptive Title]

## Problem
What this solves

## Solution
\`\`\`language
code here
\`\`\`

## Usage
How to use it

## Notes
Any caveats or considerations
```

**Quick Thought:**
```markdown
# [Brief Title]

[Content]

---
*Captured from Claude session on [date]*
```

### 3. Determine Tags

Select appropriate tags:
- `inbox` - Default for quick captures
- `project/<name>` - If project-specific
- `decision` - For decisions
- `reference` - For reference material
- `meeting` - For meeting notes
- `code` - For code snippets

### 4. Create Note

```bash
~/.claude/bin/obs/obs-wrapper write "Title" \
  --tag "tag1" \
  --tag "tag2" \
  --content "formatted content"
```

Or for longer content, create file directly:
```bash
# Generate filename
FILENAME="$(date +%Y-%m-%d)-title-slug.md"

# Write to vault
cat > ~/Documents/personal/Inbox/$FILENAME << 'EOF'
---
generation_date: YYYY-MM-DD HH:MM
tags:
  - tag1
  - tag2
source: claude-session
---

# Title

Content here...
EOF
```

### 5. Confirm and Link

After creation:
1. Confirm file path
2. Suggest related notes to link
3. Offer to update embeddings if significant content

## Examples

### Capture a Decision

**User:** "Save this auth decision to my notes"

**Action:**
```bash
obs write "API Authentication Decision" \
  --tag "project/api" \
  --tag "decision" \
  --content "## Decision\nUse OAuth2 with JWT tokens...\n\n## Rationale\n..."
```

**Output:**
```
Created: ~/Documents/personal/Inbox/2025-12-02-api-authentication-decision-decision.md

Related notes you might want to link:
- [[API Design Notes]]
- [[Security Requirements]]
```

### Quick Capture

**User:** "Capture: look into Redis caching for session storage"

**Action:**
```bash
obs write "Redis Caching Investigation" \
  --tag "inbox" \
  --tag "todo" \
  --content "Look into Redis caching for session storage\n\n*Captured from Claude session*"
```

## Tips

- Default to `inbox` tag if unsure - can be re-tagged later
- Include source context (date, session topic)
- Keep quick captures brief - elaborate later
- Link related notes when obvious connections exist
