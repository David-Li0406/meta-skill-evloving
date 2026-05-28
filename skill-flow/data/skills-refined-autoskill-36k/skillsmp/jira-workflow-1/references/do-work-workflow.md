# Do Work - Detailed Workflow

Complete implementation guide for the "do work" operation.

## Table of Contents

1. [Pre-flight Checks](#pre-flight-checks)
2. [Fetch Ticket Details](#fetch-ticket-details)
3. [Assess Complexity & Create Subtasks](#assess-complexity--create-subtasks)
4. [Create Feature Branch](#create-feature-branch)
5. [Implement the Work](#implement-the-work)
6. [Commit Changes](#commit-changes)
7. [Update Jira Ticket](#update-jira-ticket)
8. [Optional: Transition Ticket](#optional-transition-ticket)

---

## Pre-flight Checks

Before starting work, verify:

```bash
# Verify git repository
git rev-parse --is-inside-work-tree

# Check for clean working tree
git status --porcelain
```

**If working tree is dirty:**

```
⚠️ You have uncommitted changes. Please commit or stash them before starting new work:
- `git stash` to temporarily save changes
- `git commit` to commit current work
```

**If not a git repo:**

```
⚠️ Current directory is not a Git repository. Navigate to a repository or initialize one.
```

## Fetch Ticket Details

1. Get Cloud ID:

   ```
   mcp_atlassian-mcp_getAccessibleAtlassianResources
   ```

2. Activate issue management tools:

   ```
   activate_jira_issue_management_tools
   ```

3. Fetch issue details using the issue key (e.g., PROJ-123)

4. Extract and display:
   - Summary (title)
   - Description
   - Issue type
   - Priority
   - Acceptance criteria (if present)
   - Linked issues/dependencies

**Present to user:**

```
📋 PROJ-123: Implement user authentication

Type: Story | Priority: High | Status: To Do

Description:
As a user, I want to log in with my credentials so that I can access
my personalized dashboard.

Acceptance Criteria:
- [ ] Login form with email/password
- [ ] JWT token generation
- [ ] Protected route middleware
- [ ] Error handling for invalid credentials

Ready to proceed? (Y/n)
```

## Assess Complexity & Create Subtasks

After fetching ticket details, assess whether the task should be broken into subtasks.

### Complexity Indicators

**Create subtasks when:**

- Multiple distinct components involved (API, UI, database, tests)
- Acceptance criteria span different technical domains
- Estimated effort exceeds 2-3 hours
- Natural logical divisions exist

**Keep as single task when:**

- Simple, localized change
- Single acceptance criterion
- Can complete in under an hour
- Bug fix with clear scope

### Creating Subtasks

1. **Analyze the ticket** and identify logical divisions:

   ```
   PROJ-123: Implement user authentication

   Subtask breakdown:
   - Authentication middleware setup
   - Login endpoint implementation
   - JWT token generation utility
   - Integration tests
   ```

2. **Create subtasks in Jira**:

   ```
   mcp_atlassian-mcp_createJiraIssue
   ```

   For each subtask:

   ```json
   {
     "projectKey": "PROJ",
     "issueTypeName": "Sub-task",
     "summary": "Set up authentication middleware",
     "parent": "PROJ-123",
     "description": "Create Express middleware for JWT validation...",
     "additional_fields": {
       "labels": ["created-by-github-copilot"]
     }
   }
   ```

3. **Present plan to user**:

   ```
   📋 PROJ-123: Implement user authentication

   This task is complex. Proposed subtask breakdown:

   | # | Subtask | Summary |
   |---|---------|---------|
   | 1 | PROJ-124 | Set up authentication middleware |
   | 2 | PROJ-125 | Implement login endpoint |
   | 3 | PROJ-126 | Add JWT token generation utility |
   | 4 | PROJ-127 | Write integration tests |

   Each subtask will get its own commit.
   Proceed with this breakdown? (Y/n/modify)
   ```

4. **If user wants to modify**, adjust subtasks before proceeding.

### Working with Subtasks

When a ticket has subtasks (either pre-existing or just created):

1. **Work on subtasks sequentially** in logical order
2. **For each subtask**:
   - Implement the specific scope
   - Stage and commit with subtask reference
   - Add comment to subtask in Jira
   - Transition subtask to "Done"
3. **After all subtasks complete**:
   - Add summary comment to parent ticket
   - Transition parent to "Done"

## Create Feature Branch

1. Determine branch type from issue type:
   - Story/Feature/Epic → `feature/`
   - Bug/Defect → `bugfix/`
   - Task/Sub-task/Chore → `chore/`
   - Improvement → `improvement/`

2. Generate branch name:

   ```
   <type>/<ticket-key>-<slugified-summary>
   ```

   Slugify rules:
   - Lowercase
   - Replace spaces with hyphens
   - Remove special characters
   - Truncate to ~50 chars

3. Create and checkout branch:

   ```bash
   git checkout -b feature/PROJ-123-user-authentication
   ```

4. Confirm to user:

   ```
   ✅ Created branch: feature/PROJ-123-user-authentication
   ```

## Implement the Work

This is the core development phase. Apply standard development practices:

1. **Analyze requirements** from ticket description and acceptance criteria

2. **Plan implementation** - identify files to create/modify

3. **Implement changes** following project conventions:
   - Code style consistency
   - Error handling
   - Documentation/comments where needed
   - Tests if applicable

4. **Verify implementation** - run relevant tests/linters:

   ```bash
   # Language-specific verification
   npm test        # Node.js
   pytest          # Python
   go test ./...   # Go
   ```

5. **Track changes** for the Jira update:
   - Files created
   - Files modified
   - Key decisions made
   - Any deviations from original requirements

## Commit Changes

### Single Task (No Subtasks)

1. Stage changes:

   ```bash
   git add -A
   ```

2. Create commit with proper format:

   ```bash
   git commit -m "<type>(<ticket-key>): <summary>

   <body>

   Refs: <ticket-key>
   Co-authored-by: GitHub Copilot <noreply@github.com>"
   ```

### With Subtasks (Commit Per Subtask)

For each subtask, create a separate commit:

1. Stage changes for the subtask:

   ```bash
   git add <files-for-this-subtask>
   ```

2. Create commit referencing subtask AND parent:

   ```bash
   git commit -m "<type>(<subtask-key>): <summary>

   <body>

   Refs: <subtask-key>
   Part-of: <parent-key>
   Co-authored-by: GitHub Copilot <noreply@github.com>"
   ```

3. Example subtask commits for PROJ-123:

   ```bash
   # Subtask 1: Middleware
   git commit -m "feat(PROJ-124): set up authentication middleware

   - Create authMiddleware.ts with JWT validation
   - Add middleware to protected routes
   - Handle token expiry and invalid tokens

   Refs: PROJ-124
   Part-of: PROJ-123
   Co-authored-by: GitHub Copilot <noreply@github.com>"

   # Subtask 2: Login endpoint
   git commit -m "feat(PROJ-125): implement login endpoint

   - Add POST /api/auth/login route
   - Validate email/password input
   - Return JWT token on success

   Refs: PROJ-125
   Part-of: PROJ-123
   Co-authored-by: GitHub Copilot <noreply@github.com>"
   ```

4. Update each subtask in Jira immediately after its commit.

### Type Mapping

- Story/Feature → `feat`
- Bug → `fix`
- Task/Chore → `chore`
- Documentation → `docs`
- Refactor → `refactor`
- Test → `test`

**Co-authored-by:** Always include this trailer. GitHub recognizes it and displays Copilot as a contributor in the commit history.

### Confirm to user

After each commit:

```
✅ Committed: feat(PROJ-125): implement login endpoint
   Subtask 2/4 complete
```

After all subtasks:

```
✅ All subtasks committed:
   - PROJ-124: set up authentication middleware
   - PROJ-125: implement login endpoint
   - PROJ-126: add JWT token generation utility
   - PROJ-127: write integration tests
```

## Update Jira Ticket

Add a comment summarizing the work done:

```
mcp_atlassian-mcp_addCommentToJiraIssue
```

**Comment template:**

```markdown
## Implementation Complete

### Changes Made
- Added login endpoint (`POST /api/auth/login`)
- Created JWT token utility (`src/utils/jwt.ts`)
- Implemented auth middleware (`src/middleware/auth.ts`)

### Files Modified
- `src/routes/auth.ts` (new)
- `src/utils/jwt.ts` (new)
- `src/middleware/auth.ts` (new)
- `src/routes/index.ts` (updated to include auth routes)

### Technical Notes
- Using HS256 algorithm for JWT signing
- Token expiry set to 24 hours
- Refresh token support planned for future iteration

### Branch
`feature/PROJ-123-user-authentication`

### Next Steps
- Push branch and create PR
- Await code review
```

## Optional: Transition Ticket

If user wants to update ticket status:

1. Get available transitions:

   ```
   mcp_atlassian-mcp_getTransitionsForJiraIssue
   ```

2. Show options to user:

   ```
   Available transitions for PROJ-123:
   1. In Progress
   2. In Review
   3. Done

   Move ticket? (Enter number or skip)
   ```

3. Execute transition if requested:

   ```
   mcp_atlassian-mcp_transitionJiraIssue
   ```

---

## Complete Workflow Summary

```
┌─────────────────────────────────────────────────────────┐
│                    DO WORK WORKFLOW                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. PRE-FLIGHT                                          │
│     ├── Verify git repo                                 │
│     └── Check clean working tree                        │
│                                                          │
│  2. FETCH TICKET                                        │
│     ├── Get Cloud ID                                    │
│     ├── Fetch issue details                             │
│     └── Display & confirm with user                     │
│                                                          │
│  3. ASSESS COMPLEXITY                                   │
│     ├── Check if task is large/complex                  │
│     ├── If yes: create subtasks in Jira                 │
│     └── Present breakdown for user approval             │
│                                                          │
│  4. CREATE BRANCH                                       │
│     ├── Determine type from issue                       │
│     ├── Generate branch name                            │
│     └── git checkout -b <branch>                        │
│                                                          │
│  5. IMPLEMENT (loop if subtasks)                        │
│     ├── Analyze requirements                            │
│     ├── Code changes                                    │
│     ├── Verify (tests/lint)                             │
│     └── Track changes for update                        │
│                                                          │
│  6. COMMIT                                              │
│     ├── Stage changes (per subtask if applicable)       │
│     ├── Commit with ticket/subtask reference            │
│     └── Include Part-of for subtasks                    │
│                                                          │
│  7. UPDATE JIRA                                         │
│     ├── Add comment to subtask/ticket                   │
│     ├── Transition subtask to Done                      │
│     └── Repeat 5-7 for each subtask                     │
│                                                          │
│  8. FINALIZE (if subtasks)                              │
│     ├── Add summary comment to parent                   │
│     └── Transition parent to Done                       │
│                                                          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```
