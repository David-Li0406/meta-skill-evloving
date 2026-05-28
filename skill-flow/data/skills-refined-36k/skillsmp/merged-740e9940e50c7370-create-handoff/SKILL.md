---
name: create-handoff
description: Use this skill to create a handoff document for transferring work to another session.
---

# Create Handoff

You are tasked with writing a handoff document to transfer your work to another agent in a new session. The goal is to create a document that is thorough yet concise, summarizing your context without losing key details.

## Process

### 1. Filepath & Metadata
Determine the session name and create your file using the following conventions:

- If there are existing handoffs, use the most recently modified handoff folder name. If none exist, use `general`.
- Create your file under: `thoughts/shared/handoffs/{session-name}/YYYY-MM-DD_HH-MM_description.yaml`, where:
  - `{session-name}` is from existing handoffs or `general`
  - `YYYY-MM-DD` is today's date
  - `HH-MM` is the current time in 24-hour format
  - `description` is a brief kebab-case description

**Examples:**
- `thoughts/shared/handoffs/open-source-release/2026-01-08_16-30_memory-system-fix.yaml`
- `thoughts/shared/handoffs/general/2026-01-08_16-30_bug-investigation.yaml`

### 2. Write YAML Handoff
Use the following YAML format for your handoff document:

```yaml
---
session: {session-name from ledger}
date: YYYY-MM-DD
status: complete|partial|blocked
outcome: SUCCEEDED|PARTIAL_PLUS|PARTIAL_MINUS|FAILED
---

goal: {What this session accomplished}
now: {What next session should do first}
test: {Command to verify this work}

done_this_session:
  - task: {First completed task}
    files: [{file1.py}, {file2.py}]
  - task: {Second completed task}
    files: [{file3.py}]

blockers: [{any blocking issues}]
questions: [{unresolved questions for next session}]
decisions:
  - {decision_name}: {rationale}
findings:
  - {key_finding}: {details}
worked: [{approaches that worked}]
failed: [{approaches that failed and why}]
next:
  - {First next step}
  - {Second next step}
files:
  created: [{new files}]
  modified: [{changed files}]
```

**Field guide:**
- `goal:` and `now:` are required fields shown in the statusline.
- Include `done_this_session:`, `decisions:`, `findings:`, `worked:`, `failed:`, and `next:` to provide a comprehensive overview.

### 3. Mark Session Outcome
Before finalizing the handoff, ask about the session outcome using the following options:

```
Question: "How did this session go?"
Options:
  - SUCCEEDED: Task completed successfully
  - PARTIAL_PLUS: Mostly done, minor issues remain
  - PARTIAL_MINUS: Some progress, major issues remain
  - FAILED: Task abandoned or blocked
```

After receiving the user's response, index and mark the outcome:

```bash
# Index the handoff into the database
cd "$PROJECT_ROOT/opc" && uv run python scripts/core/artifact_index.py --file thoughts/shared/handoffs/{session_name}/{filename}.yaml

# Mark the outcome
cd "$PROJECT_ROOT/opc" && uv run python scripts/core/artifact_mark.py --latest --outcome <USER_CHOICE>
```

### 4. Confirm Completion
After marking the outcome, respond to the user:

```
Handoff created! Outcome marked as [OUTCOME].

Resume in a new session with:
/resume_handoff path/to/handoff.yaml
```

## Additional Notes & Instructions
- Provide more information as necessary; be thorough and precise.
- Avoid excessive code snippets; prefer using file references that an agent can follow later.