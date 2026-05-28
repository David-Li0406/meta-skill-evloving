---
name: jira-ticket-management
description: Use this skill when you need to read, create, update, or implement Jira tickets effectively.
---

# Skill body

## Standard Operating Procedures

### Ticket Creation

1. Use the type 'Story', unless explicitly specified by the user to use 'Epic'.
   - **Context**: If not specified, assume "Story". For Epic creation, the following are mandatory:
     - Work classification: A, B, or C
     - Capitalizable: yes or no
     - Assignee
   - For Story creation, the following are mandatory:
     - Epic
     - Sprint (optional): if not provided, leave blank. If specified as "current" or "active", use the `jira sprints` command to find the 'active' sprint. If specified as "next", use the `jira sprints` command to find the next sprint.
     - Points (optional): if not provided, leave blank
     - Assignee (optional): if not provided, leave blank. If specified as "me", assume user specified by the environment variable `USER`.

2. Write clear, concise summaries.
3. Optionally add label `ai-ready` if the ticket is detailed enough for AI implementation.
4. Use present tense and write the ticket as if the work is to be done.
5. Summary starts with the name of the repo in square brackets: `[REPO-NAME] <SUMMARY>`.
6. Craft detailed descriptions including:
   - Problem statement or feature description
   - Expected work product
   - Technical details when relevant
7. Use the Jira Text Formatting language:
   - Use `{{monospace}}` instead of `{code}..{code}` for inline code.
   - Code blocks should specify the language: `{code:language} some code {code}`.

### Ticket Updates

1. Fetch current ticket state before making changes.
2. Preserve important existing information.
3. Add meaningful comments explaining changes.
4. Link related tickets when appropriate.
5. Update time tracking information if provided.
6. Use the Jira Text Formatting language:
   - Use `{{monospace}}` instead of `{code}..{code}` for inline code.
   - Code blocks should specify the language: `{code:language} some code {code}`.

### Ticket Implementation

1. Learn the skill jira-ticket-management.
2. Read the ticket.
3. Transition the ticket to "In Dev".
4. Use the Plan tool to formulate a plan and seek approval from the user.
5. Implement the plan.