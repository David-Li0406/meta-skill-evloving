---
title: Slash Command Examples
description: Eight production-ready slash command examples demonstrating preflight checks, context gathering, skill integration, and subagent delegation. Includes commit, review, scaffold, refactor, PR, test, documentation, and cleanup commands.
keywords: examples, slash commands, production ready, commit command, code review, feature scaffold, refactor, pull request, test runner, documentation, cleanup
file-type: reference
skill: creating-commands
---

# Slash Command Examples

This document provides production-ready examples of custom slash commands demonstrating best practices for preflight checks, context gathering, skill integration, and subagent delegation.

## Example 1: Commit Command

**File**: `.claude/commands/commit.md`

**Purpose**: Create atomic git commits using conventional commit format

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*)
argument-hint: [message]
description: Create atomic commit with conventional format
---

## Preflight Checks

- Git repository exists: !`git rev-parse --git-dir 2>/dev/null && echo "yes" || echo "no"`
- Working directory has changes: !`git status --short`
- Not on main/master branch: !`git branch --show-current | grep -E '^(main|master)$' && echo "WARNING: on main branch" || echo "safe"`

## Context

- Current branch: !`git branch --show-current`
- Staged changes: !`git diff --cached --stat`
- Unstaged changes: !`git diff --stat`
- Recent commits (for style reference): !`git log --oneline -10`
- Current diff (staged): !`git diff --cached`
- Current diff (unstaged): !`git diff`

## Your Task

Use the **committing-atomically** skill to create a git commit.

Steps:
1. Analyze all changes shown in the context above
2. If message is provided via $ARGUMENTS, use it as the commit message
3. If no message is provided, generate an appropriate conventional commit message
4. Create the commit following conventional commit format
5. Confirm the commit was created successfully

## Success Criteria

- Commit created with conventional format (feat:, fix:, docs:, etc.)
- Commit message accurately describes the changes
- No uncommitted changes remain (unless intentionally excluded)
```

**Usage**:
```bash
/commit
/commit "feat: add user authentication"
```

---

## Example 2: Code Review Command

**File**: `.claude/commands/review.md`

**Purpose**: Comprehensive code review focusing on security, performance, and best practices

```markdown
---
allowed-tools: Bash(git diff:*), Bash(git ls-files:*), Read, Grep, Glob, Task
argument-hint: [file-pattern]
description: Review code for security and performance issues
---

## Preflight Checks

- Git repository: !`git rev-parse --git-dir 2>/dev/null && echo "yes" || echo "no"`
- Files exist matching pattern: !`git ls-files '$ARGUMENTS' 2>/dev/null | head -5 || echo "no matches"`

## Context

- Files to review: !`git ls-files '$ARGUMENTS' 2>/dev/null | head -20`
- Recent changes to these files: !`git diff HEAD -- $ARGUMENTS 2>/dev/null | head -100`
- Git status: !`git status --short`

## Your Task

Review the files matching pattern: **$ARGUMENTS** (or all changed files if no pattern provided)

Use the **Explore** subagent with thoroughness level **medium** to:
1. Find all files matching the pattern (or all modified files)
2. Identify similar patterns used elsewhere in the codebase
3. Check for consistent error handling approaches

Then perform a comprehensive code review focusing on:

### Security
- Input validation and sanitization
- Authentication and authorization checks
- Secrets or credentials in code
- SQL injection vulnerabilities
- XSS vulnerabilities
- Insecure dependencies

### Performance
- Inefficient algorithms or data structures
- Unnecessary re-renders or computations
- Memory leaks
- Database query optimization
- Caching opportunities

### Code Quality
- Code style consistency
- Error handling completeness
- Test coverage gaps
- Documentation needs
- Maintainability concerns

## Success Criteria

- All security vulnerabilities identified and documented
- Performance bottlenecks highlighted with suggestions
- Code quality issues listed with actionable recommendations
- Severity ratings provided (critical/high/medium/low)
```

**Usage**:
```bash
/review
/review "src/**/*.ts"
/review "src/auth/*"
```

---

## Example 3: Feature Scaffold Command

**File**: `.claude/commands/feature.md`

**Purpose**: Scaffold a new feature with all necessary files (code, tests, docs)

```markdown
---
allowed-tools: Bash(ls:*), Bash(test:*), Bash(mkdir:*), Read, Write, Edit, TodoWrite, Task, Bash(git add:*), Bash(git commit:*)
argument-hint: <feature-name>
description: Scaffold new feature with tests and docs
---

## Preflight Checks

- Project has standard structure: !`ls -la src/ tests/ docs/ 2>/dev/null || echo "non-standard structure"`
- Feature doesn't already exist: !`test ! -d src/features/$1 && test ! -d tests/features/$1 && echo "ok" || echo "feature exists"`
- Package.json exists: !`test -f package.json && echo "yes" || echo "no"`

## Context

- Project structure: !`tree -L 2 -I 'node_modules|dist|build' src/ tests/ 2>/dev/null || ls -la`
- Existing features: !`ls -1 src/features/ 2>/dev/null || echo "no features directory"`
- Test file patterns: !`find tests/ -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | head -5`
- Example feature for reference: !`ls -la src/features/ 2>/dev/null | head -1`

## Your Task

Create a new feature named: **$1**

Follow these steps:

1. **Plan the structure** using TodoWrite:
   - Create feature directory
   - Create test directory
   - Generate implementation files
   - Generate test files
   - Create documentation
   - Commit the scaffold

2. **Use the Explore subagent** (thoroughness: medium) to:
   - Find existing feature patterns to follow
   - Identify the testing framework and patterns used
   - Locate documentation standards

3. **Create the scaffold**:
   - Create `src/features/$1/` directory
   - Create `src/features/$1/index.ts` with boilerplate
   - Create `tests/features/$1/` directory
   - Create test file following project patterns
   - Create `docs/features/$1.md` with feature documentation template

4. **Use the committing-atomically skill** to commit:
   - Message: "feat: scaffold $1 feature"
   - Include all created files

## Success Criteria

- Feature directory created in correct location
- Implementation file(s) created with proper boilerplate
- Test file(s) created following project patterns
- Documentation file created with feature overview
- All files committed atomically
```

**Usage**:
```bash
/feature user-authentication
/feature shopping-cart
```

---

## Example 4: Refactor Command

**File**: `.claude/commands/refactor.md`

**Purpose**: Safely refactor a symbol across the entire codebase

```markdown
---
allowed-tools: Bash(git:*), Read, Edit, Grep, Glob, Task, TodoWrite
argument-hint: <from-name> <to-name>
description: Refactor symbol across entire codebase
---

## Preflight Checks

- Git working tree is clean: !`git status --short | grep -q . && echo "WARNING: uncommitted changes" || echo "clean"`
- Symbol exists in codebase: !`git grep -n "$1" 2>/dev/null | head -5 || echo "symbol not found"`
- Not on main/master: !`git branch --show-current | grep -E '^(main|master)$' && echo "WARNING: on main" || echo "safe"`

## Context

- Current branch: !`git branch --show-current`
- Occurrences count: !`git grep -c "$1" 2>/dev/null | wc -l`
- Sample occurrences: !`git grep -n "$1" 2>/dev/null | head -10`
- Files containing symbol: !`git grep -l "$1" 2>/dev/null`

## Your Task

Refactor symbol from **$1** to **$2** across the entire codebase.

Follow this workflow:

1. **Create task list** using TodoWrite:
   - Search for all occurrences
   - Analyze usage patterns
   - Perform refactoring
   - Update tests
   - Update documentation
   - Verify changes
   - Commit

2. **Use the Explore subagent** (thoroughness: very thorough) to:
   - Find all occurrences of "$1" in code, tests, and docs
   - Identify usage patterns and contexts
   - Check for test coverage of the symbol
   - Find references in configuration files
   - Locate any string literals or comments referencing it

3. **Perform the refactoring**:
   - Update all code occurrences
   - Update all test files
   - Update documentation files
   - Update configuration if needed
   - Update comments and string literals where appropriate

4. **Verify the changes**:
   - Search for any remaining occurrences of "$1"
   - Run tests to ensure nothing broke
   - Check for TypeScript/ESLint errors
   - Verify no broken imports or references

5. **Use the committing-atomically skill** to commit:
   - Message: "refactor: rename $1 to $2"
   - Include all modified files

## Success Criteria

- All occurrences of "$1" updated to "$2"
- Tests still passing
- No TypeScript/linting errors
- No broken references or imports
- Changes committed atomically with descriptive message
```

**Usage**:
```bash
/refactor getUserData fetchUserData
/refactor handleClick onButtonClick
```

---

## Example 5: PR Creation Command

**File**: `.claude/commands/pr.md`

**Purpose**: Create a pull request with comprehensive description

```markdown
---
allowed-tools: Bash(git:*), Bash(gh:*), Read, Grep
argument-hint: [base-branch]
description: Create pull request with detailed description
---

## Preflight Checks

- Git repository: !`git rev-parse --git-dir 2>/dev/null && echo "yes" || echo "no"`
- Current branch is not main: !`git branch --show-current | grep -E '^(main|master)$' && echo "ERROR: on main" || echo "safe"`
- Branch has commits: !`git log --oneline -1 2>/dev/null || echo "no commits"`
- GitHub CLI available: !`which gh || echo "not installed"`
- GitHub CLI authenticated: !`gh auth status 2>&1 || echo "not authenticated"`

## Context

- Current branch: !`git branch --show-current`
- Target base branch: !`echo ${1:-main}`
- Remote tracking: !`git rev-parse --abbrev-ref @{upstream} 2>/dev/null || echo "not tracking remote"`
- Commit history: !`git log ${1:-main}..HEAD --oneline`
- Full diff from base: !`git diff ${1:-main}...HEAD`
- Changed files: !`git diff ${1:-main}...HEAD --name-only`
- Branch is pushed: !`git rev-parse --abbrev-ref @{upstream} 2>/dev/null && echo "pushed" || echo "not pushed"`

## Your Task

Create a pull request for the current branch targeting **${1:-main}**.

Follow this workflow:

1. **Analyze all commits and changes**:
   - Review the full commit history from the context
   - Understand the complete diff from the base branch
   - Identify the purpose and scope of changes

2. **Draft PR description** including:
   - Summary section with 2-4 bullet points describing what changed
   - Detailed description of the changes and why they were made
   - Test plan with checklist of how to verify the changes
   - Any breaking changes or migration notes
   - Related issues or dependencies

3. **Push and create PR**:
   - If branch is not pushed: `git push -u origin $(git branch --show-current)`
   - Create PR using: `gh pr create --base ${1:-main} --title "..." --body "..."`
   - Include the generated description with proper markdown formatting

4. **Include in PR description footer**:
   ```
   ---
   Generated with Claude Code
   ```

## Success Criteria

- Branch pushed to remote
- PR created successfully
- PR description is comprehensive and well-formatted
- PR URL returned to user
```

**Usage**:
```bash
/pr
/pr develop
/pr main
```

---

## Example 6: Test Runner Command

**File**: `.claude/commands/test.md`

**Purpose**: Run tests and analyze failures

```markdown
---
allowed-tools: Bash(npm test:*), Bash(npm run:*), Bash(pytest:*), Bash(jest:*), Read, Grep, TodoWrite, Task
argument-hint: [test-pattern]
description: Run tests and analyze any failures
---

## Preflight Checks

- Package.json exists: !`test -f package.json && echo "yes" || echo "no"`
- Test script available: !`npm run 2>&1 | grep -q "test" && echo "yes" || echo "no"`
- Test directory exists: !`test -d tests || test -d test || test -d __tests__ && echo "yes" || echo "no"`

## Context

- Available test scripts: !`npm run 2>&1 | grep -A 50 "available via"`
- Test files: !`find . -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | grep -v node_modules | head -10`
- Test pattern argument: $ARGUMENTS

## Your Task

Run tests and analyze results.

Follow this workflow:

1. **Create task list** using TodoWrite:
   - Run tests
   - Analyze failures (if any)
   - Identify root causes
   - Suggest fixes

2. **Run the tests**:
   - If pattern provided: Run tests matching "$ARGUMENTS"
   - If no pattern: Run full test suite
   - Capture full output including stack traces

3. **If tests fail**:
   - Use TodoWrite to create a task for each failing test
   - Use the **Explore** subagent (thoroughness: medium) to:
     - Find the test file and implementation
     - Understand the test's purpose
     - Identify what changed that might have broken it

   For each failure:
   - Read the test file
   - Read the implementation being tested
   - Identify the root cause
   - Suggest a fix

4. **If tests pass**:
   - Confirm all tests passed
   - Report test count and coverage (if available)

## Success Criteria

- Tests executed successfully
- If failures occurred: Root cause identified for each failure
- If failures occurred: Actionable fix suggestions provided
- Test output clearly communicated to user
```

**Usage**:
```bash
/test
/test user
/test "auth/*.test.ts"
```

---

## Example 7: Documentation Generator Command

**File**: `.claude/commands/docs.md`

**Purpose**: Generate documentation for a module or feature

```markdown
---
allowed-tools: Read, Write, Edit, Bash(git ls-files:*), Grep, Glob, Task
argument-hint: <file-or-directory>
description: Generate comprehensive documentation
---

## Preflight Checks

- Target exists: !`test -e "$1" && echo "exists" || echo "not found"`
- Docs directory exists: !`test -d docs && echo "yes" || test -d documentation && echo "alt" || echo "none"`

## Context

- Target type: !`test -f "$1" && echo "file" || test -d "$1" && echo "directory" || echo "unknown"`
- Target contents: @$1
- Existing docs structure: !`find docs -name "*.md" 2>/dev/null | head -10 || find documentation -name "*.md" 2>/dev/null | head -10`
- Related files: !`dirname "$1" | xargs ls -la 2>/dev/null`

## Your Task

Generate comprehensive documentation for: **$1**

Follow this workflow:

1. **Analyze the target**:
   - If it's a file: Read and understand the code/module
   - If it's a directory: Use **Explore** subagent (thoroughness: medium) to understand structure and purpose

2. **Use the Explore subagent** (thoroughness: medium) to:
   - Find similar documentation in the project
   - Identify the documentation style and format used
   - Locate any existing docs that should be updated

3. **Generate documentation** including:
   - Overview and purpose
   - API reference (if applicable)
   - Usage examples
   - Parameters and return types
   - Error handling
   - Related modules or dependencies

4. **Determine output location**:
   - Follow existing documentation structure
   - Place in appropriate subdirectory
   - Use consistent naming convention

5. **Create or update the documentation file**

## Success Criteria

- Documentation file created or updated
- Follows project documentation standards
- Includes comprehensive coverage of functionality
- Examples are clear and runnable
```

**Usage**:
```bash
/docs src/utils/validation.ts
/docs src/features/authentication
```

---

## Example 8: Cleanup Command

**File**: `.claude/commands/cleanup.md`

**Purpose**: Clean up unused imports, dead code, and formatting issues

```markdown
---
allowed-tools: Bash(npm run:*), Bash(git:*), Read, Edit, Grep, Glob, Task, TodoWrite
argument-hint: [scope]
description: Remove unused imports and fix formatting
---

## Preflight Checks

- Git working tree clean: !`git status --short | grep -q . && echo "WARNING: uncommitted changes" || echo "clean"`
- Linter available: !`npm run 2>&1 | grep -E "lint|format" | head -3`
- TypeScript project: !`test -f tsconfig.json && echo "yes" || echo "no"`

## Context

- Project type: !`test -f tsconfig.json && echo "TypeScript" || test -f package.json && echo "JavaScript" || echo "unknown"`
- Linting scripts: !`npm run 2>&1 | grep -A 3 -E "lint|format"`
- Files in scope: !`git ls-files '$ARGUMENTS' 2>/dev/null | head -20 || git ls-files '*.ts' '*.tsx' '*.js' '*.jsx' | head -20`

## Your Task

Clean up code in scope: **${ARGUMENTS:-entire project}**

Follow this workflow:

1. **Create task list** using TodoWrite:
   - Find code to clean
   - Remove unused imports
   - Fix formatting
   - Run linter
   - Verify changes

2. **Use the Explore subagent** (thoroughness: medium) to find:
   - Files with unused imports
   - Dead code or unreachable statements
   - Formatting inconsistencies
   - Linter violations

3. **Perform cleanup**:
   - Remove unused imports
   - Remove commented-out code
   - Fix formatting issues
   - Remove console.log statements (unless intentional)
   - Fix simple linter violations

4. **Run linter and formatter**:
   - Execute available lint/format scripts
   - Fix any auto-fixable issues

5. **Verify changes**:
   - Check that no functionality was broken
   - Ensure all imports still resolve
   - Confirm linter passes

## Success Criteria

- Unused imports removed
- Code formatted consistently
- Linter violations fixed
- No functionality broken
```

**Usage**:
```bash
/cleanup
/cleanup "src/**/*.ts"
/cleanup src/components
```

---

## Best Practices Demonstrated

These examples demonstrate:

1. **Comprehensive Preflight Checks**: Validate environment, state, and prerequisites
2. **Rich Context Gathering**: Collect all information needed for execution
3. **Explicit Task Instructions**: Step-by-step workflows with clear expectations
4. **Skill Integration**: Reference specific skills by name when appropriate
5. **Subagent Delegation**: Use specialized subagents for complex sub-tasks
6. **Tool Restrictions**: Limit allowed tools to only what's necessary
7. **Success Criteria**: Define clear completion conditions
8. **Argument Handling**: Proper use of $ARGUMENTS and positional parameters
9. **Error Handling**: Check for error conditions in preflight checks
10. **Progressive Enhancement**: Commands work with or without optional arguments
