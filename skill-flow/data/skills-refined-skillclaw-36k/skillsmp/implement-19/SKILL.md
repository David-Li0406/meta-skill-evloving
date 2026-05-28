---
name: implement
description: Execute an implementation plan, making changes and committing properly
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Implement Plan

Execute the implementation plan, making code changes and committing according to guidelines.

## Instructions

1. **Find and Load Plan**
   - Detect workflow folder from current git branch
   - Read `workflows/<folder>/plan.md`
   - If no plan exists, suggest running `/create-plan` first

2. **Verify Prerequisites**
   - Confirm on correct feature branch
   - Check working directory is clean (`git status`)
   - Ensure tests pass before starting: `go test ./...`

3. **Load Guidelines**
   - Read CODING_GUIDELINES.md for implementation standards
   - Read COMMIT_GUIDELINES.md for commit format
   - Read GIT_TEST_SCENARIOS.md when implementing tests (required for Git scenario setup)

4. **Execute Tasks**

   For each task in the plan:

   ### Before Each Task
   - Mark task as "in progress" mentally
   - Review task requirements
   - Identify all files to modify

   ### Implementation Standards (from CODING_GUIDELINES.md)
   - Follow three-layer command architecture
   - Load config once, pass to functions
   - Use custom error types from `internal/errors`
   - Follow configuration precedence: defaults → git config → flags
   - Document exported functions
   - Use `internal/git/` wrappers, never direct git commands

   ### Code Changes
   - Make focused, atomic changes
   - Follow existing patterns in the codebase
   - Add appropriate error handling
   - Keep changes minimal - don't over-engineer

   ### After Each Task
   - Verify build: `go build ./...`
   - Run tests: `go test ./...`
   - Review changes: `git diff`

5. **Commit Strategy**

   Following COMMIT_GUIDELINES.md:

   ### Commit Types
   - `feat`: New feature or functionality
   - `fix`: Bug fix
   - `refactor`: Code restructuring
   - `test`: Adding/modifying tests
   - `docs`: Documentation changes

   ### Commit Message Format
   ```
   <type>(<scope>): <subject>

   <body explaining what and why>

   Resolves #<issue-number>
   ```

   ### When to Commit
   - After completing a logical unit of work
   - After each checkpoint in the plan
   - Keep commits atomic and focused
   - Use `/commit` skill for proper formatting

6. **Checkpoint Verification**

   At each checkpoint in the plan:
   - [ ] Build succeeds: `go build ./...`
   - [ ] Tests pass: `go test ./...`
   - [ ] Expected behavior works
   - [ ] Changes committed

7. **Track Progress**

   Update plan.md checkboxes as tasks complete:
   ```markdown
   - [x] Completed task
   - [ ] Pending task
   ```

8. **Handle Issues**

   If problems arise:
   - Document the issue
   - Check if it affects the plan
   - Adjust approach if needed
   - Ask for clarification if blocked

## Anti-Patterns to Avoid

From CODING_GUIDELINES.md:

- Don't add unnecessary abstractions
- Don't ignore errors
- Don't call `config.LoadConfig()` multiple times
- Don't create option structs just to reduce parameters
- Don't use `os.Chdir()` in production code
- Don't skip error checking

## Completion

When all tasks are done:
1. Verify all tests pass
2. Check all checkboxes in plan.md are complete
3. Suggest running `/local-review` before PR
