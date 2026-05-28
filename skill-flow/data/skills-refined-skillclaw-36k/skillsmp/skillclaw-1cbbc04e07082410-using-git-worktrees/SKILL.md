---
name: using-git-worktrees
description: Use this skill whenever you need to create an isolated workspace with Git worktrees.
---

# Skill body

*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. **Find the worktrees directory.**
   - Check existing directories using the Bash tool: 
     ```bash
     ls -d .worktrees 2>/dev/null
     ```
   - If not found, ask for permission to create a `.worktrees` directory. If given permission, create it.

2. **Verify .gitignore before creating a worktree.**
   - Check if the directory pattern is in `.gitignore`:
     ```bash
     grep -q "^\.worktrees/$" .gitignore || grep -q "^worktrees/$" .gitignore
     ```
   - If not found, add the appropriate line to the `.gitignore`.

3. **Create the worktree.**
   - Come up with a good branch name based on the request.
   - Create the worktree with the Bash tool:
     ```bash
     git worktree add ".worktrees/$BRANCH_NAME" -b "$BRANCH_NAME"
     ```
   - Change into the newly created path:
     ```bash
     cd ".worktrees/$BRANCH_NAME"
     ```

4. **Auto-detect and run project setup.**
   - Check for common project files and run the appropriate setup:
     ```bash
     # Node.js
     if [ -f package.json ]; then npm install; fi

     # Rust
     if [ -f Cargo.toml ]; then cargo build; fi

     # Python
     if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
     if [ -f pyproject.toml ]; then poetry install; fi

     # Go
     if [ -f go.mod ]; then go mod download; fi
     ```
   - If there is no obvious project setup, you _MUST_ ask for guidance.

5. **Run tests to ensure the worktree is clean.**
   - Use project-appropriate commands:
     ```bash
     npm test
     cargo test
     pytest
     go test ./...
     ```
   - If tests fail, report failures and ask whether to proceed or investigate. If tests pass, report that you are ready.

6. **Report Location.**
   - Provide the following information:
     ```
     New working directory: <full-path>
     Tests passing (<N> tests, 0 failures)
     All commands and tools will now refer to: <full-path>
     ```

7. **Understand your working context.**
   - You are now in a new working directory. Your Bash tool instructions from here on out should refer to the worktree directory, NOT your original directory. This is ABSOLUTELY CRITICAL.

# Maintaining Working Directory in Worktree

**CRITICAL:** Once you create and enter a worktree, you must stay within it for the entire session.

**Rules:**
1. Never use `cd ..` from within a worktree - it will eventually take you outside the worktree boundary.
2. Always use absolute paths for commands - use `npm run lint` from within the worktree, not `cd .. && npm run lint`.
3. If you need to run root-level commands, use the full worktree path.