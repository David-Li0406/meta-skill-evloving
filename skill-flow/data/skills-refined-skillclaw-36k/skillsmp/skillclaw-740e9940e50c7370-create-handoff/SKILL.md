---
name: create-handoff
description: Use this skill when you need to create a handoff document to transfer work to another session, ensuring all key details are summarized concisely.
---

# Skill body

## Process

### 1. Filepath & Metadata
Determine the session name and create your handoff document using the following guidelines:

- **Session Name**: 
  - If there are existing handoffs, find the most recently modified folder:
    ```bash
    ls -td thoughts/shared/handoffs/*/ 2>/dev/null | head -1 | xargs basename
    ```
  - If no handoffs exist, use `general` as the folder name.

- **File Path**: Create your file under:
  ```
  thoughts/shared/handoffs/{session-name}/YYYY-MM-DD_HH-MM_description.yaml
  ```
  Where:
  - `{session-name}` is from existing handoffs or `general`
  - `YYYY-MM-DD` is today's date
  - `HH-MM` is the current time in 24-hour format (no seconds needed)
  - `description` is a brief kebab-case description

**Examples**:
- `thoughts/shared/handoffs/open-source-release/2026-01-08_16-30_memory-system-fix.yaml`
- `thoughts/shared/handoffs/general/2026-01-08_16-30_bug-investigation.yaml`

### 2. Write YAML Handoff
Use the following YAML format for your handoff document. Ensure to follow the structure exactly:

```yaml
---
session: {session-name from ledger}
date: YYYY-MM-DD
status: complete|partial|blocked
outcome: SUCCEEDED|PARTIAL_PLUS|PARTIAL_MINUS|FAILED
---

goal: {What this session accomplished - shown in statusline}
now: {What next session should do first - shown in statusline}
test: {Command to verify this work, e.g., pytest tests/test_foo.py}

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
  modified: [{modified files}]
```

### 3. Additional Considerations
- Ensure the document is thorough yet concise, summarizing all key details without losing important context.
- If applicable, reference any relevant documents or plans that were used during the session.