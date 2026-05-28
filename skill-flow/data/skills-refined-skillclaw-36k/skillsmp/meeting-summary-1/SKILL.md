---
name: meeting-summary
description: |
  Transform meeting folders into structured summaries with actionable tasks. Use when:
  (1) Processing meeting recordings/transcripts into documentation
  (2) Creating summaries from meeting notes, agendas, and supporting materials
  (3) Extracting action items and tasks from meetings
  (4) Generating professional PDF meeting summaries

  Input: A meeting folder containing any combination of agenda, notes, transcript, and supporting docs.
  Output: Structured markdown summary + PDF + task file with assigned owners.
---

# Meeting Summary Skill

Transform meeting materials into actionable documentation.

## Workflow

### Step 1: Locate and Read Meeting Materials

Identify the meeting folder and read all available materials:

1. **Agenda** - Look for files containing "agenda" in the name
2. **Transcript** - Look for `.vtt`, `.srt`, or files with "transcript" in name
3. **Notes** - Look for "notes" or general `.md`/`.txt` files
4. **Supporting docs** - Any other files (PDFs, images, shared documents)

Read all materials before proceeding. If the folder path isn't provided, ask:

```
AskUserQuestion:
  header: "Meeting Folder"
  question: "Which meeting folder should I process?"
  options: [Allow free text - user selects "Other"]
```

### Source Priority

When synthesizing information from multiple sources:

| Source | Priority | Notes |
|--------|----------|-------|
| Transcript/Recording | Highest | Authoritative source of truth |
| Handwritten Notes | Medium | May contain errors, mishearings, or gaps |
| Agenda | Context | Pre-meeting expectations, may not reflect actual discussion |

**Conflict handling:**
- If transcript and notes conflict on facts (names, numbers, decisions), prefer transcript
- Flag significant discrepancies for user review:
  ```
  ⚠️ Conflict detected:
  - Notes say: "[X]"
  - Transcript says: "[Y]"
  - Using transcript version. Correct?
  ```
- Don't silently resolve conflicts - surface them for confirmation

### Step 2: Identify Meeting Type

Determine the meeting type to guide summary structure:

| Type | Indicators | Focus Areas |
|------|-----------|-------------|
| **Kickoff** | First meeting, introductions, "getting started" | Full context, stakeholders, systems, cadence |
| **Discovery** | Interview, research, learning | Pain points, insights, quotes |
| **Status** | Update, check-in, progress | Decisions, blockers, next steps |
| **Planning** | Strategy, roadmap, prioritization | Decisions, dates, ownership |

If unclear, ask:

```
AskUserQuestion:
  header: "Meeting Type"
  question: "What type of meeting was this?"
  options:
    - "Kickoff/Onboarding" - First meeting with new client or project
    - "Discovery/Interview" - Learning and research focused
    - "Status/Check-in" - Regular progress update
    - "Planning/Strategy" - Decision and roadmap focused
```

### Step 3: Generate Meeting Summary

Create `[Meeting Name] Summary.md` in the meeting folder.

**Reference:** Read `references/summary-template.md` for structure guidance.

**Key principles:**
- Include only sections relevant to meeting type and content
- Use specific names, dates, and numbers (not vague references)
- Capture direct quotes for important statements
- Organize by topic, not chronologically
- Write in active voice

**Required sections (always include):**
- Header with metadata (client, date, attendees)
- Executive summary (2-3 sentences)
- Key discussion points
- Next steps with clear ownership

**Conditional sections (include when relevant):**
- Key stakeholders (new people or roles clarified)
- Systems & tools (technology discussed)
- Pain points (problems raised)
- Key dates (deadlines mentioned)
- Key insights (memorable quotes/observations)

### Step 4: Extract Tasks

Create `[Meeting Name] - Tasks.md` in the meeting folder.

**Reference:** Read `references/task-template.md` for format.

**Task extraction rules:**

1. **Scan for action language:**
   - "I'll...", "We need to...", "Can you...", "Let's..."
   - "Action item:", "TODO:", "Follow up:"
   - Assignments: "[Name] will..."

2. **For each task, capture:**
   - Description (specific, actionable)
   - Owner (who is responsible)
   - Due date (if mentioned)
   - Context (why this task exists)

3. **Flag unclear ownership:**
   - If owner not obvious, mark as "⚠️ NEEDS ASSIGNMENT"
   - Suggest likely owner based on context
   - Group these in "Unassigned Tasks" section

### Step 5: Clarify Unassigned Tasks

If any tasks lack clear ownership, ask for clarification:

```
AskUserQuestion:
  header: "Task Owner"
  question: "Who should own: [task description]?"
  options:
    - "[Suggested person 1]" - [Their role/context]
    - "[Suggested person 2]" - [Their role/context]
    - "Myself" - I'll handle this
    - "Defer" - Leave unassigned for now
```

Update the task file with confirmed owners.

### Step 6: Generate PDF

Run the PDF generation script:

```bash
python3 ~/.claude/skills/meeting-summary/scripts/generate_pdf.py "[path/to/summary.md]"
```

This creates a professional PDF in the same folder as the markdown summary.

**Versioning:** If a PDF already exists, a versioned filename is created automatically:
- First run: `Summary.pdf`
- Re-run: `Summary_v2.pdf` (original preserved)
- Re-run again: `Summary_v3.pdf`

**Note:** Requires `reportlab` package. If not installed:
```bash
pip install reportlab
```

### Step 7: Confirm Completion

Summarize what was created:

```
Meeting processing complete:

Created files:
- [Meeting Name] Summary.md - Full meeting documentation
- [Meeting Name] Summary.pdf - Professional PDF version
- [Meeting Name] - Tasks.md - [N] action items extracted

Task summary:
- [Party 1]: [N] tasks
- [Party 2]: [N] tasks
- Unassigned: [N] tasks (if any)

Next: Use /clickup-push-tasks to load tasks into project management.
```

## Quick Reference

| Step | Action | Output |
|------|--------|--------|
| 1 | Read meeting folder | Understanding of materials |
| 2 | Identify meeting type | Summary structure |
| 3 | Generate summary | `[Name] Summary.md` |
| 4 | Extract tasks | `[Name] - Tasks.md` |
| 5 | Clarify ownership | Updated task file |
| 6 | Generate PDF | `[Name] Summary.pdf` |
| 7 | Confirm | Status message |

## File Naming Convention

All outputs go in the meeting folder:
- Summary: `[Meeting Name] Summary.md`
- PDF: `[Meeting Name] Summary.pdf` (or `_v2.pdf`, `_v3.pdf` if re-running)
- Tasks: `[Meeting Name] - Tasks.md`

**PDF Versioning:** Running the skill multiple times never overwrites existing PDFs. Each run creates a new version while preserving previous ones.

Example for a kickoff meeting (after two runs):
```
Clients/Acme Corp/Kickoff Meeting/
├── Agenda.md (input)
├── transcript.vtt (input)
├── notes.md (input)
├── Acme Corp Kickoff Summary.md (output)
├── Acme Corp Kickoff Summary.pdf (output - original)
├── Acme Corp Kickoff Summary_v2.pdf (output - second run)
└── Acme Corp Kickoff - Tasks.md (output)
```
