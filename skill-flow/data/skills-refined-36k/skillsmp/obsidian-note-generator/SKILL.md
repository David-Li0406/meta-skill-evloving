---
name: obsidian-note-generator
description: Generate structured Obsidian notes from emails, meeting transcripts, chat logs, or freeform text. Use when converting unstructured content into properly formatted notes with automatic template selection, project detection, and Dataview-compatible tags.
metadata:
  author: university-library-it
  version: "1.0.0"
---

# Obsidian Note Generator

## When to use this skill

Use this skill when the user needs to:

- Convert emails, meeting transcripts, chat logs, or freeform text into Obsidian notes
- Create notes with consistent frontmatter and tags for Dataview queries
- Automatically detect which project a note relates to
- Determine the correct template and output folder for content

## How to generate a note

### Step 1: Receive input

Accept input as either:
- **File path**: User provides path to source file
- **Inline content**: User pastes content directly

### Step 2: Classify content

Analyze input to select the appropriate template. See [templates.yaml](references/templates.yaml) for classification signals.

| Template | Key Signals |
|----------|-------------|
| Meeting | attendees, agenda, action items, "sync", "standup" |
| Communication | From/To/Subject headers, "RE:", "FW:", chat timestamps |
| Incident | "outage", "down", severity indicators, "INC" |
| Troubleshooting | "error", "bug", "fix", stack traces, "root cause" |
| ADR | "decision", "alternatives", "we decided", trade-offs |
| SOP | "procedure", "steps", "how to", numbered instructions |
| Prompt | "prompt", "Claude", "GPT", system instructions |
| AzureResource | Azure resource names, resource groups, ARM references |

If classification confidence is below 60%, ask the user to confirm template choice.

### Step 3: Detect project

Match content against the project list. See [projects.yaml](references/projects.yaml) for all projects and aliases.

1. Check exact project name matches
2. Check aliases (e.g., "SP5" → SubjectsPlus5)
3. Use fuzzy matching for partial names
4. Look for context clues (URLs, repository names)

### Step 4: Extract metadata

Extract from content:
- **Date**: From content or use current date
- **Participants**: Names, emails, handles
- **Topic**: Concise summary
- **Action items**: Tasks, to-dos, follow-ups
- **Status**: Based on content (default varies by template)

### Step 5: Generate note

1. Load template from [assets/templates/](assets/templates/)
2. Populate frontmatter with extracted metadata
3. Apply tags: Type + Project + Tech (if detected)
4. Fill template sections with organized content
5. Generate filename: `YYYY-MM-DD-descriptive-title.md`
6. Suggest output folder based on template and project

## Output format

**File output (default):**

```
📄 Generated Note: {filename}
📁 Suggested Location: {folder_path}
🏷️ Tags: {tag_list}

---
{full_markdown_content}
---
```

**Terminal output (interactive):**

Include confidence score and offer refinement options:
1. Save as-is
2. Change template
3. Modify tags
4. Edit content
5. Change project assignment

## Folder routing

| Template | Default Folder | With Project |
|----------|----------------|--------------|
| Meeting | `01-MeetingNotes/` | `10-Projects/{Project}/Communications/Meetings/` |
| Communication | `00-Inbox/` | `10-Projects/{Project}/Communications/{Subtype}/` |
| Incident | `40-Incidents/Active/` | `40-Incidents/Active/` |
| Troubleshooting | `00-Inbox/` | `10-Projects/{Project}/Troubleshooting/` |
| ADR | `00-Inbox/` | `10-Projects/{Project}/Architecture/` |
| SOP | `50-SOPs/` | `50-SOPs/{Category}/` |
| Prompt | `60-AIKnowledge/Prompts/` | `60-AIKnowledge/Prompts/` |
| AzureResource | `20-Infrastructure/Azure/` | `20-Infrastructure/Azure/{ResourceType}/` |

## Naming convention

All files follow: `YYYY-MM-DD-descriptive-title.md`

Examples:
- `2025-01-23-sp5-deployment-planning-meeting.md`
- `2025-01-23-etd-mysql-connection-timeout.md`
- `2025-01-23-adr-0012-switch-to-react.md`

## Tag taxonomy

**Required:** `#Type/{TemplateName}`

**Conditional:**
- `#Project/{ProjectName}` - When project detected
- `#Status/{Status}` - Based on content
- `#Tech/{Technology}` - When tech signals detected (Azure, PHP, Python, React, MySQL, Docker)

**Hierarchical projects:**
- `#Project/Calder/Ebooks`
- `#Project/LMS/Canvas`
- `#Project/LMS/Blackboard`

## Security considerations

- Never include actual secrets, passwords, or API keys
- Reference Key Vault names only, not connection strings
- Flag potential PII for user review before saving

## Examples

See [references/examples/](references/examples/) for sample input/output pairs:

- [email-to-communication.md](references/examples/email-to-communication.md)
- [transcript-to-meeting.md](references/examples/transcript-to-meeting.md)
- [error-to-troubleshooting.md](references/examples/error-to-troubleshooting.md)
- [chat-to-decision.md](references/examples/chat-to-decision.md)
