---
name: start-ticket
description: Start work on a Jira ticket by fetching details, creating a branch, and entering planning mode.
---

# Start Ticket

## Instructions

When this skill is invoked with a Jira ticket ID (e.g., `/start-ticket UP-1600`), help the user start work on that ticket.

### Steps

1. **Parse Arguments:**
   - Extract the Jira ticket ID from the command arguments
   - The ticket ID should match the pattern `{JIRA_PROJECT_KEY}-[0-9]+` (e.g., `UP-1600`)
   - If no ticket ID is provided, ask the user to provide one

2. **Validate Environment:**
   - Check that the following environment variables are set:
     - `JIRA_EMAIL` - User's Jira email for authentication
     - `JIRA_API_TOKEN` - API token for Jira authentication
     - `JIRA_BASE_URL` - Base URL of the Jira instance
   - If any are missing, inform the user which variables need to be configured

3. **Fetch Ticket Details:**
   - Use curl to fetch the issue from the Jira REST API:
     ```bash
     curl -s -X GET \
       -H "Accept: application/json" \
       -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" \
       "${JIRA_BASE_URL}/rest/api/3/issue/{TICKET_ID}"
     ```
   - Parse the JSON response to extract:
     - Summary (title)
     - Description
     - Status
     - Priority
     - Assignee
     - Any acceptance criteria or subtasks
   - If the API call fails, display the error and stop

4. **Check for Existing Branches:**
   - Search for branches that already contain this ticket ID:
     ```bash
     git branch -a | grep -i {TICKET_ID}
     ```
   - If existing branch(es) are found:
     - Use the AskUserQuestion tool to ask the user whether to:
       - Switch to one of the existing branches (list them as options)
       - Create a new branch
     - If user chooses an existing branch, skip to step 6 (switch to that branch)

5. **Generate Branch Name** (only if creating a new branch):
   - Extract the ticket summary from the fetched ticket data
   - Convert the summary to a kebab-case slug:
     - Convert to lowercase
     - Replace spaces and special characters with hyphens
     - Remove consecutive hyphens
     - Truncate to a reasonable length (max ~50 characters for the description part)
   - Format: `{TICKET_ID}-{slug}` (e.g., `UP-1600-create-jira-skill`)

6. **Create or Switch Branch:**
   - If switching to an existing branch:
     ```bash
     git checkout {existing-branch}
     ```
   - If creating a new branch:
     ```bash
     git checkout -b {branch-name}
     ```

7. **Enter Planning Mode:**
   - Enter planning mode by running `/plan`

8. **Present Context:**
   - Display the ticket details in a clear format:
     - Ticket ID and Summary as heading
     - Status, Priority, Assignee
     - Full description
     - Acceptance criteria (if any)
   - Check with user
     - Ask if there is any specific guidance that should be considered while planning
   - Then begin creating an implementation plan based on:
     - The ticket requirements
     - The project's Documentation Driven Development workflow (see CLAUDE.md)
     - Relevant code patterns in the codebase

9. **Update Ticket Status (After Plan Accepted):**
   - Once the user has approved the plan and you're ready to begin implementation:
   - Check the ticket's current status from the fetched data (step 3)
   - If the status is "Open", transition it to "In Progress":
     - First, get available transitions for the issue:
       ```bash
       curl -s -X GET \
         -H "Accept: application/json" \
         -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" \
         "${JIRA_BASE_URL}/rest/api/3/issue/{TICKET_ID}/transitions"
       ```
     - Find the transition ID for "In Progress" from the response
     - Execute the transition:
       ```bash
       curl -s -X POST \
         -H "Accept: application/json" \
         -H "Content-Type: application/json" \
         -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" \
         -d '{"transition": {"id": "{TRANSITION_ID}"}}' \
         "${JIRA_BASE_URL}/rest/api/3/issue/{TICKET_ID}/transitions"
       ```
   - If the status is not "Open", skip this step (do not change the status)
   - Inform the user of the status update (or that it was skipped)

10. **Begin Implementation:**
    - Proceed with implementing the plan
