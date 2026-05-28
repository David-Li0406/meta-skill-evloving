# CaptureRoutine Workflow

When user wants to save a repeatable sequence of actions as a reusable personal skill.

## Triggers

- "save this routine"
- "remember this workflow"
- "save these steps"
- "capture this procedure"
- "make this repeatable"
- "do this again later"
- "save this workflow"

## When to Use

- User just completed a multi-step task they want to reuse
- User wants to convert a manual process into a reusable skill
- User is codifying ad-hoc procedures into structured workflows
- User says they want to "do this again" or "remember how we did this"

## Execution

### Step 1: Locate Current Transcript

Find the transcript for the current session:

```bash
# The transcript is at:
# ~/.claude/projects/{project-hash}/{session-id}.jsonl
```

The session ID is available from the conversation context. Look in `~/.claude/projects/` for the active project directory, then find the `.jsonl` file matching the current session.

### Step 2: Extract Workflow

Run the extraction tool on the transcript:

```bash
bun ~/.claude/skills/RoutineCapture/Tools/ExtractWorkflow.ts <transcript_path> --json
```

This returns:
- `suggestedName`: Auto-generated skill name
- `originalRequest`: The first user request
- `steps[]`: Tool operations with descriptions
- `parameters[]`: Detected variable values
- `suggestedTriggers[]`: Phrases to invoke later

### Step 3: Present to User for Review

Show the extracted workflow clearly:

```
I've analyzed our conversation and extracted this routine:

**Suggested Name**: {suggestedName}

**Steps**:
1. {step.description} [{step.capability}]
2. {step.description} [{step.capability}]
...

**Detected Parameters** (values that might change each time):
• {param.name}: {param.value} ({param.type})
...

**Suggested Triggers** (phrases to invoke this later):
• {trigger1}, {trigger2}, ...

Does this look right? I can:
- Adjust the name
- Add/remove steps
- Change which values are parameters vs constants
- Add more trigger phrases
```

### Step 4: Gather User Modifications

Use AskUserQuestion if needed to clarify:

**Questions to potentially ask:**
1. "What would you like to name this routine?" (if they want to change it)
2. "Should [value] be a parameter (changes each time) or constant (always the same)?"
3. "What other phrases should trigger this routine?"
4. "Are there any steps to remove or add?"

**Accept natural language modifications:**
- "Call it ClassAudit instead"
- "Make the URL a constant"
- "Also trigger on 'schedule check'"
- "Remove step 3"

### Step 5: Validate Name Format

Ensure the skill name follows conventions:
- Must start with underscore: `_`
- Use TitleCase: `_ClassScheduleAudit`
- No spaces or special characters

If user provides "class audit", convert to `_ClassAudit`.

### Step 6: Synthesize Skill

Run the synthesis tool:

```bash
bun ~/.claude/skills/RoutineCapture/Tools/SynthesizeSkill.ts \
  --name "{validated_name}" \
  --workflow '{workflow_json}' \
  --triggers "{additional_triggers}"
```

This creates:
- `skills/{name}/SKILL.md`
- `skills/{name}/Workflows/Execute.md`

### Step 7: Confirm and Guide Invocation

Report success and show how to use:

```
✅ Created personal skill: {name}

Files created:
• skills/{name}/SKILL.md
• skills/{name}/Workflows/Execute.md

**To invoke this routine later, say:**
• "{trigger1}"
• "{trigger2}"
• Or any variation like: "{example phrase}"

**Example:**
"Audit my classes for Fall 2026"
→ Runs the saved routine with semester = "Fall 2026"
```

## Error Handling

**If transcript not found:**
- Check `~/.claude/projects/` for recent sessions
- Ask user if they can provide the session ID

**If extraction fails:**
- Report the error
- Offer to manually create the skill based on user's description

**If skill already exists:**
- Ask if user wants to update the existing skill
- Or create with a different name

## Notes

- Personal skills use `_` prefix and are never shared publicly
- Skills are stored in `~/.claude/skills/`
- After creation, skills load via natural language triggers in the description's `USE WHEN` clause
- Parameters can have defaults or be required each time
