# Agent Patterns and Best Practices

Design patterns, prompt engineering techniques, and composition strategies for Claude Code subagents.

## Agent Specialization Patterns

### Single Responsibility Pattern

Each agent should have ONE clear purpose.

**Good:**
```yaml
name: code-reviewer
description: Reviews code for quality and security
```

```yaml
name: test-runner
description: Runs tests and fixes failures
```

**Avoid:**
```yaml
name: general-helper
description: Reviews code, runs tests, writes docs, deploys
```

**Why:** Focused agents are more predictable and produce better results.

### Domain Expert Pattern

Create agents that are experts in specific domains.

```yaml
---
name: react-specialist
description: React expert. Use for component design, hooks, and React best practices.
tools: Read, Write, Edit, Glob, Grep
skills: react-patterns
---

You are a React expert specializing in modern React patterns.

## Expertise Areas
- Functional components and hooks
- State management (useState, useReducer, Context)
- Performance optimization (useMemo, useCallback)
- Testing with React Testing Library
- Server components and streaming
```

### Read-Only Analyst Pattern

For agents that should analyze but never modify.

```yaml
---
name: architecture-analyst
description: Analyzes codebase architecture. Use for understanding system design.
tools: Read, Glob, Grep
model: opus
permissionMode: plan
---

You are an architecture analyst who examines codebases without modifying them.

## Guidelines
- NEVER suggest using Edit or Write tools
- Focus on understanding and documenting
- Create diagrams in markdown
- Report findings clearly
```

### Executor Pattern

For agents that take action with minimal analysis.

```yaml
---
name: formatter
description: Formats code files. Use PROACTIVELY after any file changes.
tools: Bash, Read, Glob
model: haiku
permissionMode: acceptEdits
---

You are a code formatter that runs formatting tools.

## Process
1. Identify changed files
2. Run appropriate formatter
3. Report results

## Commands
- TypeScript: `bun run prettier --write`
- Python: `black .`
- Go: `go fmt ./...`

Do NOT analyze code quality. Just format.
```

## Prompt Engineering for Agents

### Clear Role Definition

Start with an unambiguous role statement.

**Good:**
```markdown
You are a senior security engineer specializing in web application security audits.
```

**Avoid:**
```markdown
You help with security stuff.
```

### Numbered Process Steps

Agents follow numbered steps more reliably.

**Good:**
```markdown
## When Invoked

1. Run `git diff` to identify changes
2. Read each modified file
3. Check against security checklist
4. Generate report with findings
```

**Avoid:**
```markdown
Look at the code and find problems.
```

### Explicit Constraints

Tell agents what NOT to do.

```markdown
## Constraints

- NEVER modify production configuration files
- Do NOT commit changes directly
- Always preserve existing functionality
- Skip files in `node_modules/` and `.git/`
```

### Output Format Specification

Define exactly what output should look like.

```markdown
## Output Format

```markdown
# Review Report

## Summary
[1-2 sentence summary]

## Critical Issues
- [Issue with file:line reference]

## Warnings
- [Warning with recommendation]

## Suggestions
- [Optional improvement]
```
```

### Examples in Prompts

Include input/output examples for complex tasks.

```markdown
## Example

**Input**: User requests "add email validation"

**Process**:
1. Find email-related code: `rg "email" --type ts`
2. Identify validation location
3. Add Zod schema validation
4. Add tests

**Output**:
```typescript
const emailSchema = z.string().email();
```
```

## Tool Restriction Strategies

### Minimum Privilege Pattern

Grant only the tools necessary for the task.

| Agent Type | Recommended Tools |
|------------|-------------------|
| Reviewer | `Read`, `Glob`, `Grep` |
| Analyzer | `Read`, `Glob`, `Grep`, `Bash` (read-only) |
| Fixer | `Read`, `Edit`, `Glob`, `Grep` |
| Creator | `Read`, `Write`, `Edit`, `Glob`, `Grep` |
| Executor | `Bash`, `Read`, `Glob` |

### Tool-Purpose Alignment

Match tools to agent purpose:

```yaml
# Code reviewer - no editing capability
name: code-reviewer
tools: Read, Glob, Grep, Bash
# Bash for git diff, not for modifications

# Bug fixer - needs editing
name: bug-fixer
tools: Read, Edit, Bash, Glob, Grep
# Edit but not Write (modify, don't create)

# Scaffolder - needs file creation
name: scaffolder
tools: Read, Write, Bash, Glob
# Write for new files, no Edit needed
```

### Bash Command Validation

For agents with Bash access, use hooks to validate commands:

```yaml
---
name: safe-executor
description: Executes commands with safety checks
tools: Bash, Read, Glob
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-command.sh"
---
```

The hook script can block dangerous commands:
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

# Block dangerous patterns
if echo "$command" | grep -qE 'rm -rf|:(){:|chmod 777|> /dev'; then
  echo "Blocked dangerous command: $command" >&2
  exit 2
fi

exit 0
```

## Error Handling Patterns

### Graceful Degradation

Design agents to handle failures gracefully.

```markdown
## Error Handling

If a tool call fails:
1. Log the error
2. Try alternative approach
3. Report what could and couldn't be done

NEVER fail silently. Always report issues.
```

### Verification Steps

Include verification after actions.

```markdown
## Process

1. Make the change
2. Run tests to verify
3. If tests fail:
   - Revert change
   - Report issue
   - Suggest alternative
```

### Explicit Failure Reporting

Tell agents how to report failures.

```markdown
## If Unable to Complete

Report:
1. What was attempted
2. What failed and why
3. What partial progress was made
4. Suggested next steps

Do NOT pretend success if something failed.
```

## Agent Composition Patterns

### Main Agent Spawns Specialists

The main conversation spawns specialized agents for specific tasks.

```
User: Review my PR and then deploy if it looks good

Main Agent:
1. Spawns code-reviewer agent
2. Receives review results
3. If approved, spawns deployer agent
4. Reports final status
```

**Key:** Main agent coordinates, specialists execute.

### Sequential Pipeline

Chain agents in sequence where each depends on previous.

```
analyze -> review -> fix -> test -> deploy
```

```
User: Fix the failing tests and deploy

Main Agent:
1. Spawns test-runner to identify failures
2. Spawns debugger to fix issues
3. Spawns test-runner to verify fixes
4. Spawns deployer to deploy
```

### Parallel Specialist

Run multiple agents simultaneously for independent tasks.

```
User: Prepare for release

Main Agent spawns in parallel:
- code-reviewer (check quality)
- security-audit (check security)
- documentation (update docs)

Waits for all, then:
- deployer (if all pass)
```

### Scoped Agents

Create agents scoped to specific parts of codebase.

```yaml
name: frontend-specialist
description: Frontend expert. Only works on files in src/app/ and src/components/
tools: Read, Write, Edit, Glob, Grep
---

You specialize in frontend code.

## Scope
ONLY work with files in:
- `src/app/`
- `src/components/`
- `src/hooks/`
- `src/styles/`

For backend changes, recommend using backend-specialist agent.
```

## Anti-Patterns to Avoid

### 1. Overly Broad Agent

**Problem:**
```yaml
name: do-everything
description: Handles all tasks
```

**Why bad:** Unpredictable behavior, context confusion.

**Fix:** Create focused, single-purpose agents.

### 2. Missing Description

**Problem:**
```yaml
name: helper
description: Helps
```

**Why bad:** Claude can't decide when to use it.

**Fix:** Specific description with trigger phrases.

### 3. Unnecessary Tool Access

**Problem:**
```yaml
name: code-reviewer
tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
```

**Why bad:** Reviewer shouldn't write/edit.

**Fix:** Minimum necessary tools only.

### 4. Expecting Nested Agents

**Problem:**
```markdown
When you need more details, spawn the explore agent...
```

**Why bad:** Subagents CANNOT spawn other subagents.

**Fix:** Design self-contained agents or use main agent coordination.

### 5. Vague Process Instructions

**Problem:**
```markdown
Look at the code and fix problems.
```

**Why bad:** Inconsistent behavior.

**Fix:** Numbered steps with specific actions.

### 6. No Output Format

**Problem:**
```markdown
Tell me what you found.
```

**Why bad:** Inconsistent, hard to parse results.

**Fix:** Specify exact output format.

### 7. Ignoring Context Boundaries

**Problem:** Assuming agent has context from main conversation.

**Why bad:** Each agent has fresh context.

**Fix:** Pass necessary context in the task prompt.

## Performance Optimization

### Model Selection

| Task Complexity | Recommended Model |
|-----------------|-------------------|
| Simple formatting | `haiku` |
| Standard development | `sonnet` |
| Complex reasoning | `opus` |
| Match main thread | `inherit` |

### Context Efficiency

Agents prevent main context pollution:
- Search results stay in agent context
- Failed attempts don't clutter main thread
- Long analyses isolated

### Latency Considerations

- Agents start fresh (no cached context)
- May need time to gather context
- Use `haiku` for speed-critical tasks
- Consider `inherit` for consistency

## Validation Checklist

Before deploying an agent:

- [ ] Name is lowercase with hyphens
- [ ] Description is specific with triggers
- [ ] Tools are minimum necessary
- [ ] Model matches task complexity
- [ ] System prompt has clear steps
- [ ] Output format is specified
- [ ] Constraints are explicit
- [ ] Error handling defined
- [ ] Tested with explicit invocation
- [ ] Verified automatic invocation works

## Debugging Agents

### Check Registration

```
/agents
```

Verify your agent appears in the list.

### Explicit Invocation

Test with explicit request:
```
Use the [agent-name] agent to [task]
```

### Debug Mode

```bash
claude --debug
```

See agent spawning and tool calls.

### Verify Tool Access

Check agent uses only allowed tools:
1. Remove a tool from `tools` list
2. Request task requiring that tool
3. Verify agent reports tool unavailable

### Check Hooks

For agents with hooks:
```
/hooks
```

Verify hooks are registered and firing.
