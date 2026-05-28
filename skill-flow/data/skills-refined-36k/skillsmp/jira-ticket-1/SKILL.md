---
name: jira-ticket
description: Create a Jira ticket with a structured format. Interactively gathers information and uses MCP Jira server to create the ticket.
context: fork
---

You are creating a Jira ticket using the MCP Atlassian Jira integration. Follow this methodology:

## 1. Gather Ticket Information

Ask the user the following questions to gather necessary information:

1. **Project**: Which Jira project should this ticket be created in?
   - If not provided, list available projects 

2. **Issue Type**: What type of issue is this? (e.g., Story, Bug, Task, Epic)
   - If not provided, fetch available issue types for the project using

3. **Summary/Title**: What is the ticket title/summary?

4. **Prerequisites**: What is the background context for this ticket?
   - General observations
   - What caused it or why we need it
   - Keep it concise

5. **Definition of Done**: What tasks define this ticket's done state?
   - Should be a list of concise, straight-to-point tasks
   - Do NOT write explicit implementation steps - leave that to the implementor
   - Only include specific steps if the task is very specific (like moving a file, removing code)

## 2. Format the Description

Structure the ticket description in this exact format:

```
## Prerequisites

[Background context here - be concise]
[General observations, what caused it, why we need it]

## Definition of done

- [Task 1]
- [Task 2]
- [Task 3]
```

## 3. Create the Ticket

Use MCP tools.

## 4. Confirm Creation

After creating the ticket, confirm with the user by providing:
- The ticket key (e.g., PROJ-123)
- A link to view the ticket
- A brief summary of what was created

## Important Guidelines:

- Be concise in all sections
- Focus on the "what" and "why", not the "how"
- Keep the Definition of Done high-level unless the task is very specific
- Use proper markdown formatting in the description
- If any required information is missing, ask the user before proceeding