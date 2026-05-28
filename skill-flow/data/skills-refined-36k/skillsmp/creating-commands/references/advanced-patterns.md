---
title: Advanced Slash Command Patterns
description: Advanced techniques for creating sophisticated slash commands including complex argument handling, error recovery, performance optimization, subagent coordination, and command composition patterns.
keywords: advanced patterns, argument handling, error recovery, performance, subagent coordination, command composition, conditional logic, rollback mechanisms
file-type: reference
skill: creating-commands
---

# Advanced Slash Command Patterns

This document covers advanced techniques and patterns for creating sophisticated slash commands.

## Advanced Preflight Check Patterns

### Combining Multiple Checks with Logic

```markdown
## Preflight Checks

- Repository and branch status: !`git rev-parse --git-dir 2>/dev/null && git branch --show-current | grep -v '^main$' && echo "✓ Safe to proceed" || echo "✗ Either not a git repo or on main branch"`
- Prerequisites met: !`which node && which npm && test -f package.json && echo "✓ All prerequisites met" || echo "✗ Missing prerequisites"`
```

### Conditional Preflight Checks Based on Arguments

```markdown
## Preflight Checks

- Target validation: !`if [ -n "$1" ]; then test -f "$1" && echo "✓ File exists: $1" || echo "✗ File not found: $1"; else echo "ℹ No target specified"; fi`
- Environment check: !`if [ "$2" = "production" ]; then git tag | grep -q "$(git describe --tags)" && echo "✓ On tagged release" || echo "✗ Not on tagged release"; else echo "ℹ Not production"; fi`
```

### Numeric Threshold Checks

```markdown
## Preflight Checks

- Not too many changes: !`changes=$(git diff --stat | wc -l); if [ $changes -lt 100 ]; then echo "✓ $changes lines changed (acceptable)"; else echo "⚠ $changes lines changed (consider splitting)"; fi`
- Test coverage acceptable: !`coverage=$(npm test -- --coverage 2>&1 | grep -oP '\d+(?=%)' | head -1); if [ $coverage -ge 80 ]; then echo "✓ Coverage: $coverage%"; else echo "✗ Coverage too low: $coverage%"; fi`
```

## Advanced Context Gathering Patterns

### Conditional Context Based on Project Type

```markdown
## Context

- Project type: !`test -f package.json && echo "Node.js" || test -f requirements.txt && echo "Python" || test -f Cargo.toml && echo "Rust" || echo "Unknown"`
- Node.js context: !`if test -f package.json; then cat package.json | head -30; fi`
- Python context: !`if test -f requirements.txt; then cat requirements.txt; fi`
- Rust context: !`if test -f Cargo.toml; then cat Cargo.toml; fi`
```

### Gathering Related Files Dynamically

```markdown
## Context

- Main file: @$1
- Related test file: !`test_file=$(echo "$1" | sed 's/\.ts$/.test.ts/' | sed 's/^src\//tests\//'); if test -f "$test_file"; then echo "@$test_file"; else echo "No test file found"; fi`
- Related files in same directory: !`dirname "$1" | xargs ls -1 2>/dev/null | head -10`
```

### Performance and Size Context

```markdown
## Context

- File sizes: !`git ls-files '$ARGUMENTS' | xargs ls -lh 2>/dev/null | awk '{print $5, $9}'`
- Lines of code: !`git ls-files '$ARGUMENTS' | xargs wc -l 2>/dev/null | tail -1`
- Git blame summary: !`git ls-files '$ARGUMENTS' | xargs -I {} git blame --line-porcelain {} | grep "^author " | sort | uniq -c | sort -rn`
```

## Advanced Argument Handling

### Named Arguments Pattern

```markdown
---
argument-hint: --type <type> --scope <scope> [message]
---

## Argument Processing

- Type argument: !`echo "$ARGUMENTS" | grep -oP '(?<=--type )\w+'`
- Scope argument: !`echo "$ARGUMENTS" | grep -oP '(?<=--scope )\w+'`
- Message: !`echo "$ARGUMENTS" | sed 's/--type [^ ]* //g' | sed 's/--scope [^ ]* //g'`

## Your Task

Create commit of type: $(echo "$ARGUMENTS" | grep -oP '(?<=--type )\w+')
With scope: $(echo "$ARGUMENTS" | grep -oP '(?<=--scope )\w+')
And message: $(echo "$ARGUMENTS" | sed 's/--type [^ ]* //g' | sed 's/--scope [^ ]* //g')
```

**Usage**: `/commit --type feat --scope auth "add login flow"`

### Variadic Arguments with Iteration

```markdown
---
argument-hint: <file1> [file2] [file3] ...
---

## Context

- All file arguments: !`for file in $ARGUMENTS; do echo "- $file"; done`
- Files existence check: !`for file in $ARGUMENTS; do test -f "$file" && echo "✓ $file" || echo "✗ $file"; done`
- Combined file contents: !`for file in $ARGUMENTS; do echo "=== $file ==="; cat "$file"; echo; done`
```

### Default Values for Arguments

```markdown
## Context

- Target environment: !`echo ${1:-development}`
- Max iterations: !`echo ${2:-10}`
- Verbosity level: !`echo ${3:-normal}`

## Your Task

Deploy to environment: **${1:-development}**
With max iterations: **${2:-10}**
Verbosity: **${3:-normal}**
```

## Advanced Skill Integration Patterns

### Conditional Skill Usage

```markdown
## Your Task

1. Analyze the changes to determine commit type
2. If changes are complex (>50 files or >500 lines):
   - Use the **Explore** subagent (thoroughness: very thorough) to understand all changes
   - Create multiple commits using the **committing-atomically** skill
3. If changes are simple:
   - Use the **committing-atomically** skill to create a single commit

3. Verify all changes are committed
```

### Chaining Multiple Skills

```markdown
## Your Task

Follow this skill chain:

1. Use the **creating-skills** skill to scaffold the new capability
2. Use the **crafting-agentic-prompts** skill to write effective instructions in SKILL.md
3. Use the **committing-atomically** skill to commit the new skill

Each skill should inform the next step in the chain.
```

### Skill Usage with Specific Parameters

```markdown
## Your Task

Use the **committing-atomically** skill with these requirements:
- Commit type must be "feat"
- Scope must be derived from the directory of changed files
- Message should reference issue #$1
- Must include Co-Authored-By trailer if pair programming

Then use the **Explore** subagent to verify:
- No related files were missed
- All tests for modified code are updated
```

## Advanced Subagent Delegation Patterns

### Sequential Subagent Tasks

```markdown
## Your Task

1. **First exploration** - Use the **Explore** subagent (thoroughness: quick) to:
   - Get high-level overview of the codebase structure
   - Identify which modules are relevant

2. **Deep analysis** - Use the **Explore** subagent (thoroughness: very thorough) to:
   - Deeply analyze the identified modules
   - Find all related functions and dependencies
   - Map out the complete call graph

3. **Implementation** - Use the **general-purpose** subagent to:
   - Implement the changes based on the analysis
   - Follow patterns discovered in exploration
```

### Parallel Subagent Tasks

```markdown
## Your Task

Launch these subagents in parallel:

**Subagent 1** - **Explore** (thoroughness: medium):
- Find all components using the old API

**Subagent 2** - **Explore** (thoroughness: medium):
- Find all test files for these components

**Subagent 3** - **Explore** (thoroughness: quick):
- Check documentation for API references

After all complete, synthesize findings and proceed with migration.
```

### Subagent with Fallback Strategy

```markdown
## Your Task

1. Use the **Explore** subagent (thoroughness: quick) to find the target module
2. If not found, use the **Explore** subagent (thoroughness: very thorough) for comprehensive search
3. If still not found, use the **general-purpose** subagent to:
   - Search for similar patterns
   - Generate the module from scratch
```

## Advanced Tool Permission Patterns

### Granular Git Permissions

```markdown
---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:-m *), Bash(git push:origin *), Read, Edit
---
```

This allows:
- `git status` with any arguments
- `git diff` with any arguments
- `git add` with any arguments
- `git commit -m <message>` only (no other commit flags)
- `git push origin <branch>` only (prevents force push)

### Restricted Bash with Specific Commands

```markdown
---
allowed-tools: Bash(npm test:*), Bash(npm run lint:*), Bash(npm run build:*), Bash(echo:*), Read
---
```

This allows:
- Running tests via npm
- Running linter via npm
- Running build via npm
- Echo for output
- Reading files
- **Prevents**: Installing packages, running arbitrary scripts, modifying files

### Progressive Permission Expansion

```markdown
---
allowed-tools: Read, Grep, Glob
---

## Preflight Checks

- Files are not too large: !`git ls-files '$ARGUMENTS' | xargs wc -l | tail -1 | awk '{print $1}'`

## Your Task

1. **Analysis phase** (current permissions):
   - Read the target files
   - Search for patterns
   - Identify issues

2. **If modifications needed** (request user permission):
   - Inform user that Edit permission is needed
   - Wait for user to update allowed-tools
   - Proceed with edits after permission granted

**Note**: This command starts with read-only permissions for safety.
Add `Edit` to allowed-tools if you want automatic modifications.
```

## Advanced Success Criteria Patterns

### Quantifiable Success Metrics

```markdown
## Success Criteria

- All TypeScript errors resolved: !`npx tsc --noEmit 2>&1 | grep -c "error TS" | test $(cat) -eq 0 && echo "✓ No TS errors" || echo "✗ TS errors remain"`
- Test coverage maintained: !`npm test -- --coverage 2>&1 | grep -oP '\d+(?=%)' | head -1 | awk '{if ($1 >= 80) print "✓ Coverage:", $1"%" ; else print "✗ Coverage dropped:", $1"%"}'`
- Bundle size not increased: !`ls -lh dist/bundle.js | awk '{print $5}'`
```

### Conditional Success Criteria

```markdown
## Success Criteria

**If modifying core modules:**
- All integration tests must pass
- Performance benchmarks must not degrade
- API compatibility maintained

**If modifying tests only:**
- All new tests pass
- Coverage increased or maintained
- No flaky tests introduced

**In all cases:**
- Linter passes
- No console warnings
- Commit created with conventional format
```

### Verification Commands as Success Criteria

```markdown
## Success Criteria

Run these verification commands to confirm success:

1. Tests pass: `npm test`
2. Types are correct: `npx tsc --noEmit`
3. Linter passes: `npm run lint`
4. Build succeeds: `npm run build`
5. No git conflicts: `git diff --check`

All must succeed for the command to be considered complete.
```

## Command Composition Patterns

### Commands that Call Other Commands

```markdown
## Your Task

This is a meta-command that orchestrates multiple specialized commands:

1. First, run the `/review` command to check code quality
2. If review passes, run the `/test` command to verify functionality
3. If tests pass, run the `/commit` command to create atomic commit
4. Finally, run the `/pr` command to create pull request

Each step must succeed before proceeding to the next.
```

### Commands with Hooks

```markdown
## Your Task

1. **Pre-execution hook**:
   - Check if `.claude/hooks/pre-commit.sh` exists
   - If exists: !`bash .claude/hooks/pre-commit.sh`
   - Verify hook succeeded before proceeding

2. **Main execution**:
   [Main command logic]

3. **Post-execution hook**:
   - Check if `.claude/hooks/post-commit.sh` exists
   - If exists: !`bash .claude/hooks/post-commit.sh`
   - Report hook results
```

## Error Handling Patterns

### Graceful Degradation

```markdown
## Your Task

1. **Attempt optimal path**:
   - Try using TypeScript compiler for analysis
   - If TypeScript not available, fall back to regex patterns

2. **Verify results**:
   - If high confidence: proceed with changes
   - If low confidence: present findings for user review before modifying

3. **Recovery on failure**:
   - If changes cause test failures: revert and report
   - If changes cause build failures: revert and report
```

### Validation with Rollback

```markdown
## Your Task

1. Create git stash of current state: !`git stash push -u -m "pre-command-backup"`

2. Perform the requested changes

3. **Validate changes**:
   - Run tests
   - Run linter
   - Check TypeScript

4. **If validation fails**:
   - Rollback: !`git stash pop`
   - Report what went wrong
   - Suggest fixes

5. **If validation succeeds**:
   - Drop stash: !`git stash drop`
   - Proceed with commit
```

## Testing and Validation

### Self-Testing Commands

```markdown
---
allowed-tools: Bash(claude:*), Read
---

## Your Task

Test this slash command itself:

1. **Validation**:
   - Check frontmatter is valid YAML
   - Verify all tools in allowed-tools are valid
   - Check preflight commands are safe

2. **Dry run**:
   - Execute all preflight checks
   - Execute all context gathering commands
   - Verify no errors occur

3. **Report**:
   - List what the command would do
   - Show what context would be gathered
   - Highlight any potential issues
```

### Debug Mode Commands

```markdown
---
argument-hint: [--debug] <args>
---

## Your Task

1. Check if --debug flag is present: !`echo "$ARGUMENTS" | grep -q "\\--debug" && echo "yes" || echo "no"`

2. **If debug mode enabled**:
   - Show all preflight check results in detail
   - Display all gathered context
   - Show step-by-step execution plan
   - Wait for user confirmation before proceeding

3. **If normal mode**:
   - Execute silently
   - Only report final results
```

## Performance Optimization Patterns

### Lazy Context Loading

```markdown
## Context

- Basic context (always loaded): !`git status --short`
- Large file list (only if needed): !`if [ -n "$ARGUMENTS" ]; then git ls-files '$ARGUMENTS'; fi`
- Full diff (only if needed): !`if echo "$ARGUMENTS" | grep -q "verbose"; then git diff HEAD; fi`
```

### Cached Context

```markdown
## Context

- Project structure (cached): !`cache_file=/tmp/project-structure-cache; if test -f "$cache_file" && test $(find "$cache_file" -mmin -60); then cat "$cache_file"; else tree -L 3 | tee "$cache_file"; fi`
```

### Parallel Context Gathering

```markdown
## Context

Note: These commands can be executed in parallel for performance.

- Git status: !`git status --short`
- Branch info: !`git branch -vv`
- Recent commits: !`git log --oneline -10`
- Staged diff: !`git diff --cached --stat`
- Unstaged diff: !`git diff --stat`
```

## Summary

Advanced slash command patterns enable:

1. **Sophisticated Validation**: Multi-condition checks with fallbacks
2. **Dynamic Context**: Conditional and lazy-loaded context gathering
3. **Complex Workflows**: Multi-stage processes with error handling
4. **Flexible Arguments**: Named parameters, defaults, and variadic args
5. **Smart Delegation**: Conditional skill/subagent usage with chaining
6. **Fine-Grained Permissions**: Precise tool restrictions for security
7. **Measurable Success**: Quantifiable criteria with verification
8. **Composition**: Commands building on other commands
9. **Resilience**: Error handling with rollback capabilities
10. **Performance**: Optimized context loading and caching

Use these patterns judiciously - remember that complexity should drive you toward creating a skill instead of a command!
