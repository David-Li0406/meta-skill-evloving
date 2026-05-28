# Subagent Prompts for ClickUp Operations

Copy-paste these prompts when spawning the clickup-task-agent. Replace placeholders with actual values.

---

## Fetch Task Details

```
Task tool with subagent_type="task:clickup-task-agent":

"Fetch ClickUp task CU-{TASK_ID}:
1. Get task details (clickup_get_task)
2. Get comments (clickup_get_task_comments)
3. Update status to 'in progress' and assign to me (clickup_update_task)

Return ONLY:
**Task:** CU-{id} - {name}
**Status:** {old} → in progress
**Priority:** {priority}

**Requirements:**
- {bullet points from description}

**Acceptance Criteria:**
- {extracted criteria}

**Suggested Branch:** feat/CU-{id}-{slug} or fix/CU-{id}-{slug}"
```

---

## Create New Task

```
Task tool with subagent_type="task:clickup-task-agent":

"Create ClickUp task:
1. Call clickup_create_task with:
   - name: '{TASK_NAME}'
   - description: '{FORMATTED_DESCRIPTION}'
   - tags: ['{TASK_TYPE}']

Return ONLY:
**Created:** CU-{id} - {name}
**URL:** {task_url}
**Status:** Ready to start"
```

---

## Mark Ready for Review

```
Task tool with subagent_type="task:clickup-task-agent":

"Mark task CU-{TASK_ID} ready for review:
1. Update status to 'ready for review' (clickup_update_task)
2. Add comment with PR URL (clickup_create_task_comment):
   'PR created: {PR_URL}

   {WORK_SUMMARY}'

Return ONLY:
**Task:** CU-{TASK_ID} → ready for review
**Comment:** Posted PR link"
```

---

## Mark Complete

```
Task tool with subagent_type="task:clickup-task-agent":

"Mark task CU-{TASK_ID} complete:
1. Update status to 'complete' (clickup_update_task)

Return ONLY:
**Task:** CU-{TASK_ID} → complete"
```

---

## Check Status

```
Task tool with subagent_type="task:clickup-task-agent":

"Check status of CU-{TASK_ID}:
1. Get task details (clickup_get_task)

Return ONLY:
**Task:** CU-{id} - {name}
**Status:** {status}
**Assignee:** {assignee}
**Due Date:** {due_date}
**Last Updated:** {date_updated}"
```

---

## Add Comment

```
Task tool with subagent_type="task:clickup-task-agent":

"Add comment to CU-{TASK_ID}:
1. Call clickup_create_task_comment with:
   - task_id: '{TASK_ID}'
   - comment_text: '{COMMENT_TEXT}'

Return: 'Comment added to CU-{TASK_ID}'"
```
