---
name: distill-voice
description: Process voice memo transcriptions into resource proposals. Analyzes spoken content, determines meeting type or category, returns structured proposal. Used by triage coordinator as subagent worker.
user-invocable: false
allowed-tools: mcp__plugin_para-obsidian_para-obsidian__para_read, mcp__plugin_para-obsidian_para-obsidian__para_frontmatter_get
---

# Distill Voice Memo

Process a single voice memo transcription and return a **proposal** (not a final note).

## Input

You receive:
- `file`: Path to transcription in inbox (e.g., `00 Inbox/🎤 2024-01-22 3-45pm.md`)
- `areas`: Available areas in vault
- `projects`: Available projects in vault

## Output

Return a JSON proposal:

```json
{
  "file": "00 Inbox/🎤 2024-01-22 3-45pm.md",
  "type": "transcription",
  "proposed_title": "Descriptive Title from Content",
  "proposed_template": "resource",
  "summary": "2-3 sentence summary of what was discussed",
  "categorization_hints": [
    "First key point",
    "Second key point",
    "Third key point"
  ],
  "action_items": [
    "Action item 1",
    "Action item 2"
  ],
  "suggested_areas": ["[[🌱 Area Name]]"],
  "suggested_projects": ["[[🎯 Project Name]]"],
  "resource_type": "meeting|conversation|idea|reflection",
  "source_format": "audio",
  "meeting_type": "standup|1on1|planning|retro|workshop|null",
  "meeting_date": "2024-01-22",
  "confidence": "high|medium|low",
  "notes": "Any special considerations"
}
```

## Workflow

### Step 1: Read Transcription

```
para_read({ file: "[input file]", response_format: "json" })
para_frontmatter_get({ file: "[input file]", response_format: "json" })
```

Extract:
- Full transcription text
- `recorded` date (for `meeting_date`)
- Pre-filled `areas` or `projects` (if any)
- Any existing metadata

### Step 2: Analyze Content

Voice memos are inherently ambiguous. Analyze for:

1. **Speaker count**: One person (reflection) vs multiple (meeting)?
2. **Tone**: Professional, personal, brainstorming?
3. **Structure**: Agenda items, action items, freeform?
4. **Time markers**: "Next week", "by Friday" suggest action items
5. **Names mentioned**: People, projects, tools?

### Step 3: Categorize

| Pattern | Resource Type | Meeting Type |
|---------|---------------|--------------|
| Multiple speakers, status updates | meeting | standup |
| Two people, career/personal topics | meeting | 1on1 |
| Sprint planning, backlog discussion | meeting | planning |
| What went well/wrong, improvements | meeting | retro |
| Technical deep-dive, learning | meeting | workshop |
| Single speaker, thinking aloud | idea | null |
| Single speaker, emotions/journaling | reflection | null |
| Discussion with back-and-forth | conversation | null |

### Step 4: Extract Action Items

Look for:
- "I need to..."
- "We should..."
- "Action item:"
- "TODO:"
- "By [date]..."
- "Follow up on..."

### Step 5: Return Proposal

Return the JSON proposal structure. Do NOT create the note.

## Voice Memo Challenges

Voice memos are the **hardest to categorize** because:

1. **No clear boundaries** - Conversations meander
2. **Context missing** - You don't know the full situation
3. **Multiple topics** - One recording may cover several things
4. **Transcription errors** - Names, technical terms may be garbled

**When in doubt, set `confidence: "low"`** so the user can choose "Deeper" for multiple options.

## Confidence Levels

| Level | When to Use |
|-------|-------------|
| `high` | Clear meeting format, obvious participants, structured content |
| `medium` | Likely interpretation but could be wrong |
| `low` | Ambiguous content, multiple valid interpretations |

**Default to `medium` or `low` for voice memos.** They're inherently ambiguous.

## Example Output

```json
{
  "file": "00 Inbox/🎤 2024-01-22 3-45pm.md",
  "type": "transcription",
  "proposed_title": "Sprint 42 Planning Session",
  "proposed_template": "resource",
  "summary": "Team planning session discussing priorities for Sprint 42. Focus on completing the migration project and addressing tech debt in the auth module.",
  "categorization_hints": [
    "Migration project is highest priority",
    "Auth module tech debt blocking other work",
    "New hire starting next week needs onboarding"
  ],
  "action_items": [
    "Review migration PR by Wednesday",
    "Schedule auth module refactor discussion",
    "Prepare onboarding materials for new hire"
  ],
  "suggested_areas": ["[[🌱 Work]]"],
  "suggested_projects": ["[[🎯 Oil Team Migration]]"],
  "resource_type": "meeting",
  "source_format": "audio",
  "meeting_type": "planning",
  "meeting_date": "2024-01-22",
  "confidence": "medium",
  "notes": "Some speaker names unclear in transcription"
}
```

## Deep Analysis Mode

When the coordinator requests "deeper" analysis, return **3 different interpretations**:

```json
{
  "options": [
    {
      "label": "A",
      "interpretation": "Sprint Planning Meeting",
      "proposed_title": "Sprint 42 Planning",
      "resource_type": "meeting",
      "meeting_type": "planning",
      "rationale": "Multiple speakers, task assignments, timeline discussion"
    },
    {
      "label": "B",
      "interpretation": "Team Brainstorm",
      "proposed_title": "Migration Approach Brainstorm",
      "resource_type": "idea",
      "meeting_type": null,
      "rationale": "Exploratory tone, no firm decisions, 'what if' language"
    },
    {
      "label": "C",
      "interpretation": "1:1 with Manager",
      "proposed_title": "1:1 - Career Discussion",
      "resource_type": "meeting",
      "meeting_type": "1on1",
      "rationale": "Two speakers, personal development mentioned, confidential tone"
    }
  ]
}
```

This gives the user meaningful choices when categorization is ambiguous.
