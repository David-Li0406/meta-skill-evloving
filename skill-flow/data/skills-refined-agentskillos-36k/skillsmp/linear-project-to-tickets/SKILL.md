---
name: linear-project-to-tickets
description: Convert a Linear project into child tickets with verification steps
---

# Linear Project to Tickets

Convert a Linear project into actionable tickets. This skill requires Linear MCP.

## Requirements

- Linear MCP must be configured and authenticated
- A Linear project must exist (use `linear-project-creation` first if needed)

## Philosophy

> "The project defines the END STATE. The agent/developer decides HOW to get there."

Focus on:
- **What** needs to exist when done
- **How to verify** it's correct
- NOT implementation details

## Process

### Step 1: Fetch Linear Project

Ask the user for the Linear project ID, then:
1. Fetch the project via Linear MCP
2. Read the project description
3. Understand the team and project structure
4. Get available labels (especially release labels)

### Step 2: Identify Target Release

Ask the user which release these tickets should be tagged with (e.g., "Dynamo 0.9.0").

Linear uses **nested labels** - release labels are under parent groups:
- Example: "Dynamo Releases > Dynamo 0.9.0"
- Fetch available labels from the team and look for the release label group first

### Step 3: Extract Tickets

From the project description, identify discrete units of work:
- Each task = one Linear issue
- Each task should have clear verification criteria
- Tasks ordered by dependency (blockers first)

### Step 4: Create Linear Issues

For each ticket, create a Linear issue with:

**Title**: Concise action (e.g., "Implement per-user rate limiting")

**Description**:
```
## What
[One sentence on what this accomplishes]

## Acceptance Criteria
- [ ] [Verification step 1]
- [ ] [Verification step 2]

## Notes
[Any context, dependencies, or constraints]
```

**Metadata**:
- Link to parent project
- **Add release label** (nested: "Dynamo Releases > Dynamo 0.9.0")
- Set labels based on category (setup, implementation, integration, testing)
- Add blocking relationships if dependencies exist

### Step 5: Confirm with User

Before creating tickets:
1. Show the list of issues to be created (title + acceptance criteria)
2. Show the release label that will be applied
3. Ask for confirmation
4. Create all issues via Linear MCP
5. Return the issue IDs/URLs

## Guidelines

- **Granularity**: Tickets should take 1-4 hours, not days
- **Independence**: Minimize coupling between tickets where possible
- **Verification focus**: If you can't verify it, the ticket isn't well-defined
- **No implementation details**: Don't specify *how* to code it, specify *what* it should do
- **Always tag release**: Every ticket must have a release label

## Example

Project description snippet:
> "Add rate limiting to the API. Should limit to 100 requests per minute per user."

Created Linear issue:
- **Title**: Implement per-user rate limiting
- **Labels**: `Dynamo Releases > Dynamo 0.7.1`, `implementation`
- **Description**:
  ```
  ## What
  Add rate limiting middleware that restricts API calls to 100/min per authenticated user

  ## Acceptance Criteria
  - [ ] Make 100 requests in <60s with same user token -> all succeed
  - [ ] Make 101st request -> returns 429 Too Many Requests
  - [ ] Wait 60s, make another request -> succeeds
  - [ ] Different user token is not affected by first user's limit
  ```
