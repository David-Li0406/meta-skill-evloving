---
name: author-skill
description: Create or capture a skill file for Layton
triggers:
  - create a skill
  - new skill
  - add skill
  - turn this into a skill
  - save as skill
  - capture skill
  - skill authoring
---

<required_reading>
**Read before starting:**

1. references/skill-authoring.md - Template and field guide
</required_reading>

## Objective

Help the user create a well-populated skill file. This workflow handles both:

- **Creating** a new skill from scratch (guided Q&A)
- **Capturing** a skill from recent conversation (retrospective extraction)

## Steps

### 1. Determine Mode

Ask the user:

> "I can help you create a skill file. Which mode?
>
> 1. **Create from scratch** - I'll guide you through defining a new skill
> 2. **Capture from conversation** - I'll extract a skill from what we just did
> 3. **Edit existing** - Update a skill file you already have"

**Wait for response.**

Route based on answer:

- 1 → Continue to "Create Mode" section
- 2 → Continue to "Capture Mode" section
- 3 → Ask which skill, then read and edit it

---

## Create Mode

### 2a. Understand the Data Source

Ask the user:

> "What system or tool do you want Layton to query?
>
> 1. **Name**: What should we call this skill? (lowercase, e.g., 'gmail', 'jira')
> 2. **Purpose**: When should Layton query this? What question does it answer?"

**Wait for response.** Extract `name` and `description`.

### 3a. Identify Commands

Ask the user:

> "How do you query this system from the command line?
>
> - An MCP server command?
> - A CLI tool (gh, jira-cli, etc.)?
> - A script or API call?
>
> Show me the exact command(s)."

**Wait for response.** Extract commands.

### 4a. Define Extraction

Ask the user:

> "When Layton runs this command, what matters most?
>
> - What should Layton look for?
> - What counts as 'needs attention'?"

**Wait for response.** Extract key data points.

### 5a. Identify Metrics

Ask the user:

> "What numbers or states should appear in briefings?
>
> Examples: counts, staleness, status indicators."

**Wait for response.** Extract metrics.

Continue to "Create the File" section.

---

## Capture Mode

### 2b. Review Conversation

Scan recent conversation for:

- **Commands run**: bash, MCP calls, API requests
- **Output parsed**: what information was extracted
- **Decisions made**: what counted as "important"

Present findings:

> "From our conversation, I found:
>
> - Commands: `{list}`
> - We extracted: `{list}`
> - Key signals: `{list}`
>
> Should I capture this as a skill? Anything to add?"

**Wait for confirmation.**

### 3b. Name and Describe

If not obvious, ask:

> "What should we call this skill? (lowercase, e.g., 'gmail')
> And a one-line description of when to use it?"

**Wait for response.**

Continue to "Create the File" section.

---

## Create the File

### 6. Check for Existing

```bash
layton skills
```

If skill name already exists, ask if user wants to overwrite or pick a different name.

### 7. Generate the Skill File

```bash
layton skills add <name>
```

This creates a file from `templates/skill.md`. Edit it to replace the skeleton placeholders with the gathered/captured information.

Reference `references/skill-authoring.md` for field guidance and optional sections.

### 8. Validate and Confirm

Show the user the created file.

> "Here's the skill file. Does this look right?
>
> Want to test the commands now?"

If testing:

- Run the commands
- Show output
- Confirm extraction logic works

## Context Adaptation

- **If user says "turn this into a skill"**: Go directly to Capture Mode
- **If user says "create a skill for X"**: Go directly to Create Mode
- **If user provides command examples upfront**: Skip the "Identify Commands" question
- **If skill already discovered**: Pre-populate source field

## Success Criteria

- [ ] Skill file created at `.layton/skills/<name>.md`
- [ ] All sections populated (not skeleton placeholders)
- [ ] Commands are executable from repo root
- [ ] User confirms the skill looks correct
