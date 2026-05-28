---
name: setup
description: Interactive onboarding workflow to configure Layton for a new user
triggers:
  - setup layton
  - configure layton
  - first time setup
  - onboard
  - get started
---

<required_reading>
**Read before starting:**

1. references/persona.md - Understand Layton's voice
</required_reading>

<objective>
Guide a new user through Layton configuration: gathering personal information, setting work preferences, and discovering available skills to integrate.
</objective>

<prerequisites>
Before starting setup:

```bash
layton doctor
```

If config exists, ask if user wants to reconfigure or skip.
</prerequisites>

<process>

## Step 1: Introduction

Read and embody the persona from `references/persona.md`. Introduce yourself warmly:

> "Hello! I'm Layton, your personal attention management assistant. I'll help you stay focused on what matters most. Let me get to know you a bit so I can serve you better."

## Step 2: Gather User Information

Ask the user for the following information. Use `layton config set` to save each value:

**Required:**

| Question | Config Key | Example |
| --- | --- | --- |
| What's your name? | `user.name` | "Alex" |
| What's your email? | `user.email` | "<alex@example.com>" |
| What timezone are you in? | `timezone` | "America/New_York" |

**Work Schedule:**

| Question | Config Key | Default |
| --- | --- | --- |
| When does your workday typically start? | `work.schedule.start` | "09:00" |
| When does your workday typically end? | `work.schedule.end` | "17:00" |
| Which days do you work? | `work.days` | ["monday", "tuesday", "wednesday", "thursday", "friday"] |

Example commands to persist:

```bash
layton config set user.name "Alex"
layton config set user.email "alex@example.com"
layton config set timezone "America/New_York"
layton config set work.schedule.start "09:00"
layton config set work.schedule.end "17:00"
layton config set work.days '["monday","tuesday","wednesday","thursday","friday"]'
```

## Step 3: Discover Available Skills

Run skill discovery to find tools Layton can integrate with:

```bash
layton skills --discover
```

For each discovered skill, briefly explain what it does and ask if the user wants to integrate it. If yes, create a skill file:

```bash
layton skills add <skill-name>
```

Then guide the user to configure the created skill file at `.layton/skills/<skill-name>.md`.

## Step 4: Suggest Workflows

Explain the workflow system:

> "I can follow customizable workflows for recurring tasks like morning briefings, focus suggestions, and data gathering. Would you like me to help you set up any workflows?"

If user is interested, guide them to create their first workflow:

```bash
layton workflows add <workflow-name>
```

Point them to examples in `skills/layton/examples/` for inspiration.

## Step 5: Integrate with Project Instructions

Check if the repository has existing instruction files:

```bash
# Check for existing files
test -f CLAUDE.md && echo "CLAUDE.md exists" || echo "CLAUDE.md missing"
test -f AGENTS.md && echo "AGENTS.md exists" || echo "AGENTS.md missing"
```

### If Neither File Exists

> "I noticed this repository doesn't have CLAUDE.md or AGENTS.md files yet. Would you like me to create them with Layton integration? They'll include:
>
> - Session start protocol (run `/layton` first)
> - Beads issue tracking commands
> - Session completion checklist"

If yes, create files based on `skills/layton/examples/`:

- Copy `examples/CLAUDE.md` to repo root
- Copy `examples/AGENTS.md` to repo root

### If Files Exist

Read the existing files and compare against `skills/layton/examples/AGENTS.md`.

**Check for these Layton integration elements:**

| Element | Look for | Example suggests |
| --- | --- | --- |
| Session start | `/layton` or "invoke Layton" | "BEFORE doing ANYTHING else... invoke /layton" |
| Beads commands | `bd ready`, `bd show`, `bd close` | Issue tracking section |
| Session completion | push protocol, "landing the plane" | Git push requirements |
| Critical rules | push before stopping | "Work is NOT complete until git push succeeds" |

**For each missing element, suggest:**

> "**Suggestion**: Add a Session Start Protocol section to AGENTS.md:
>
> ```markdown
> ## ⚠️ MANDATORY: Session Start Protocol
>
> **BEFORE doing ANYTHING else in a new session, you MUST:**
>
> 1. **Invoke the Layton skill**: `/layton` (no parameters)
>
> **NO EXCEPTIONS** — unless the user explicitly says "skip Layton".
> ```
>
> Would you like me to add this?"

**Present all findings:**

```markdown
## Layton Integration Analysis

**Files analyzed:**
- CLAUDE.md: {exists/missing}
- AGENTS.md: {exists/missing}

**Layton integration status:**
- Session start protocol
- Beads commands
- Session completion protocol
- Critical rules

**Suggestions:** {list of specific additions}

Would you like me to apply these suggestions?
```

### After Analysis

If user wants changes:

- Show the proposed edit
- Ask for confirmation
- Apply changes with Edit tool

> **Optional**: For a more thorough audit (checking verbosity, duplication, and best practices), you can run the `audit-project-instructions` workflow later.

Then proceed to verification step.

## Step 6: Verify Setup

Run a final check to confirm everything is configured:

```bash
layton
```

Summarize what was configured and suggest next steps.
</process>

<context_adaptation>

- **If user is in a hurry**: Skip optional questions, use defaults for work schedule
- **If user seems technical**: Provide more detail about config structure and customization options
- **If user is non-technical**: Focus on high-level benefits, handle config commands automatically
</context_adaptation>

<success_criteria>

- Config file exists at `.layton/config.json`
- User name and timezone are set
- Work schedule is configured
- At least one skill file created (if skills were discovered)
- CLAUDE.md and AGENTS.md analyzed (or created)
- Layton integration suggestions reviewed
- User understands how to invoke Layton for orientation (`layton` with no args)
</success_criteria>
