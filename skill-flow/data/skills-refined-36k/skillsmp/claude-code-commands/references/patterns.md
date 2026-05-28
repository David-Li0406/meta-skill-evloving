# Claude Code Commands

## Patterns


---
  #### **Name**
Standard Workflow Command
  #### **Description**
Basic command structure with clear sections
  #### **When To Use**
Any repeatable workflow
  #### **Implementation**
    # .claude/commands/feature.md
    # Standard command for new feature development
    
    # New Feature Development
    
    You are starting development of a new feature.
    
    ## Context
    - Feature: $ARGUMENTS
    - Branch: Create from main with pattern feature/$ARGUMENTS
    
    ## Workflow
    
    ### 1. Research Phase
    - Search codebase for similar implementations
    - Identify files that will need changes
    - Check for existing tests to understand patterns
    
    ### 2. Planning Phase
    - List the files you'll modify
    - Identify any new files needed
    - Consider database/API changes
    
    ### 3. Implementation Phase
    - Implement changes incrementally
    - Add tests as you go
    - Run tests after each significant change
    
    ### 4. Review Checklist
    Before finishing:
    - [ ] All tests pass
    - [ ] No console.log/debug statements
    - [ ] Types are correct
    - [ ] Documentation updated if needed
    
    ## Output Format
    After completing, provide:
    1. Summary of changes made
    2. Files modified
    3. Any follow-up tasks
    
    ---
    # Usage: /feature user authentication
    # The $ARGUMENTS becomes "user authentication"
    

---
  #### **Name**
Issue-Linked Command
  #### **Description**
Command that integrates with issue tracking
  #### **When To Use**
Connecting development to tickets
  #### **Implementation**
    # .claude/commands/issue.md
    # Work on a JIRA/Linear/GitHub issue
    
    # Work on Issue: $ARGUMENTS
    
    ## First: Fetch Issue Details
    Run this command to get issue details:
    ```bash
    # For GitHub Issues:
    gh issue view $ARGUMENTS --json title,body,labels,assignees
    
    # For JIRA:
    # jira issue view $ARGUMENTS
    
    # For Linear:
    # linear issue $ARGUMENTS
    ```
    
    ## Understand the Issue
    Based on the issue details:
    1. Summarize what needs to be done
    2. Identify acceptance criteria
    3. Note any linked PRs or issues
    
    ## Create Branch
    ```bash
    git checkout -b issue-$ARGUMENTS
    ```
    
    ## Implementation
    - Work according to issue requirements
    - Reference issue number in commit messages
    - Update issue status as you progress
    
    ## Before Completion
    Verify all acceptance criteria are met.
    Run tests relevant to the changes.
    
    ## Closing
    When complete, prepare for PR:
    1. Push branch
    2. Create PR linking to issue
    3. Update issue status
    
    ---
    # Usage: /issue PROJ-123
    

---
  #### **Name**
Debug Investigation Command
  #### **Description**
Structured debugging workflow
  #### **When To Use**
Consistent approach to bugs
  #### **Implementation**
    # .claude/commands/debug.md
    # Structured debugging workflow
    
    # Debug: $ARGUMENTS
    
    ## Phase 1: Reproduce
    First, understand and reproduce the issue.
    - What is the expected behavior?
    - What is the actual behavior?
    - What are the steps to reproduce?
    
    ## Phase 2: Gather Information
    ```bash
    # Check recent changes
    git log --oneline -20
    
    # Check for related errors in logs
    grep -r "error\|Error\|ERROR" logs/ 2>/dev/null | tail -20
    ```
    
    Search codebase for:
    - Error messages mentioned in $ARGUMENTS
    - Functions/components involved
    - Recent changes to affected files
    
    ## Phase 3: Hypothesize
    Based on findings, list 2-3 most likely causes:
    1. [Hypothesis 1]
    2. [Hypothesis 2]
    3. [Hypothesis 3]
    
    ## Phase 4: Test Hypotheses
    For each hypothesis:
    - Add targeted logging
    - Write a test case if possible
    - Verify or eliminate
    
    ## Phase 5: Fix
    Once root cause found:
    - Implement minimal fix
    - Add regression test
    - Verify original issue resolved
    - Check for similar issues elsewhere
    
    ## Phase 6: Document
    Record:
    - Root cause
    - Fix applied
    - Prevention measures
    
    ---
    # Usage: /debug login fails after password reset
    

---
  #### **Name**
Review Command with Checklist
  #### **Description**
Code review with specific criteria
  #### **When To Use**
Consistent review standards
  #### **Implementation**
    # .claude/commands/review.md
    # Code review with checklist
    
    # Code Review
    
    ## Files to Review
    Check the current staged/changed files:
    ```bash
    git diff --name-only HEAD~1
    ```
    
    ## Review Checklist
    
    ### Security
    - [ ] No hardcoded secrets or credentials
    - [ ] Input validation on user data
    - [ ] No SQL injection vulnerabilities
    - [ ] Proper authentication/authorization checks
    
    ### Code Quality
    - [ ] Functions are single-purpose
    - [ ] No code duplication
    - [ ] Error handling is comprehensive
    - [ ] Edge cases are considered
    
    ### Testing
    - [ ] New code has tests
    - [ ] Tests cover happy path and errors
    - [ ] Tests are deterministic
    
    ### Performance
    - [ ] No N+1 queries
    - [ ] No unnecessary re-renders (React)
    - [ ] Appropriate caching
    
    ### Documentation
    - [ ] Complex logic is commented
    - [ ] Public APIs are documented
    - [ ] README updated if needed
    
    ## Output Format
    For each issue found:
    - **File:Line** - Issue description
    - **Severity**: Critical/High/Medium/Low
    - **Suggestion**: How to fix
    
    ---
    # Usage: /review
    

---
  #### **Name**
Parameterized Multi-Use Command
  #### **Description**
Command with multiple use patterns
  #### **When To Use**
Commands that serve multiple purposes
  #### **Implementation**
    # .claude/commands/db.md
    # Database operations helper
    
    # Database: $ARGUMENTS
    
    Parse the command: $ARGUMENTS
    
    ## Common Operations
    
    ### If "migrate" or "migration":
    ```bash
    npm run db:migrate
    ```
    Verify migration applied correctly.
    
    ### If "seed":
    ```bash
    npm run db:seed
    ```
    Verify seed data is correct.
    
    ### If "reset":
    ⚠️ WARNING: This will delete all data!
    Only proceed if explicitly confirmed.
    ```bash
    npm run db:reset
    ```
    
    ### If "status":
    ```bash
    npm run db:status
    ```
    Show current migration status.
    
    ### If starts with "query":
    Run the SQL query that follows "query".
    Explain results in plain language.
    
    ### If "schema":
    Show current database schema.
    ```bash
    npm run db:schema
    ```
    
    ---
    # Usage: /db migrate
    # Usage: /db seed
    # Usage: /db query SELECT * FROM users LIMIT 5
    

---
  #### **Name**
File Reference Command
  #### **Description**
Command that includes file contents
  #### **When To Use**
Commands needing specific file context
  #### **Implementation**
    # .claude/commands/refactor.md
    # Refactor with architecture guidelines
    
    # Refactor: $ARGUMENTS
    
    ## Architecture Guidelines
    Follow these patterns from our codebase:
    
    @src/architecture.md
    
    ## Current Code
    First, read and understand the code to refactor:
    $ARGUMENTS
    
    ## Refactoring Goals
    1. Improve readability
    2. Follow established patterns
    3. Reduce complexity
    4. Improve testability
    
    ## Process
    1. Identify code smells
    2. Plan refactoring steps
    3. Apply changes incrementally
    4. Verify tests still pass after each change
    
    ## Constraints
    - Don't change public API unless necessary
    - Maintain backwards compatibility
    - Keep commits atomic
    
    ---
    # The @src/architecture.md includes that file's content
    # Usage: /refactor src/services/auth.ts
    

## Anti-Patterns


---
  #### **Name**
Command as Script
  #### **Description**
Trying to make commands do conditional logic
  #### **Why Bad**
    Commands are prompts, not programs.
    Claude interprets them, doesn't execute them.
    Conditional logic creates confusion.
    
  #### **What To Do Instead**
    Create separate commands for different workflows.
    /feature for new features, /bugfix for bugs.
    Let Claude handle interpretation, not branching.
    

---
  #### **Name**
Massive Monolithic Command
  #### **Description**
Single command that tries to do everything
  #### **Why Bad**
    Too long to read and understand.
    Claude may miss parts or get confused.
    Can't reuse parts in other contexts.
    
  #### **What To Do Instead**
    Break into focused commands that compose.
    /plan-feature, /implement-feature, /test-feature.
    Each command does one thing well.
    

---
  #### **Name**
Undocumented Arguments
  #### **Description**
Using $ARGUMENTS without explaining format
  #### **Why Bad**
    Users don't know what to pass.
    Wrong arguments cause unexpected behavior.
    Team members can't learn commands.
    
  #### **What To Do Instead**
    Add usage comment at the end of every command:
    # Usage: /issue PROJ-123
    # Arguments: Issue ID (e.g., PROJ-123, GH#45)
    

---
  #### **Name**
Hardcoded Paths and Names
  #### **Description**
Commands with specific paths that differ per user
  #### **Why Bad**
    Breaks on different machines.
    Requires editing for each project.
    Not portable across team.
    
  #### **What To Do Instead**
    Use relative paths from project root.
    Use $ARGUMENTS for variable parts.
    Use @file references that resolve dynamically.
    

---
  #### **Name**
No Output Format
  #### **Description**
Commands that don't specify expected output
  #### **Why Bad**
    Claude's output varies unpredictably.
    Hard to use output in next steps.
    No consistency across invocations.
    
  #### **What To Do Instead**
    Specify output format explicitly:
    ## Output Format
    - Summary: [one line]
    - Files changed: [list]
    - Next steps: [list]
    