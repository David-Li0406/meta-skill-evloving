---
name: creating-agents
description: Creates new Claude Code agent (subagent) definitions. Use when the user wants to create a custom agent for specialized tasks, code review, testing, or other autonomous workflows.
---

# Creating Agents

Creates new Claude Code agent definitions in the canonical YAML format for the AI config transpiler.

## Output Location

All new agents are created in: `example/agents/`

## Canonical YAML Schema

All available fields for an agent definition:

```yaml
# Required Fields
name: "agent-name"                  # Identifier, lowercase letters/numbers/hyphens
description: "Brief summary"        # Critical for discovery - WHAT and WHEN to use

# Optional Fields
system_prompt: |                    # The agent's system prompt (markdown)
  You are a specialized agent...

targets:                            # Platform targets (agents only support these two)
  - claude-code
  - opencode
```

## Field Reference

### `name` (required)
The identifier used to invoke the agent. Becomes the filename (`{name}.yaml`).

**Conventions:**
- Use descriptive names: `code-reviewer`, `secrets-finder`, `test-runner`
- Lowercase letters, numbers, hyphens only
- Avoid vague names: `helper`, `utils`, `tools`
- Reserved: `anthropic-*`, `claude-*`

### `description` (required)
Brief summary shown in agent listings. Claude uses this for agent discovery and delegation.

**Guidelines:**
- Write in third person: "Scans codebase for secrets"
- Include WHAT it does and WHEN to use it
- Be specific about trigger conditions

```yaml
# Good — specific trigger conditions
description: "Performs comprehensive code review. Use when reviewing PRs, before merging, or when asked to review specific files."

# Bad — too vague
description: "Helps with code."
```

### `system_prompt` (optional)
The agent's system prompt in markdown. This defines the agent's behavior, approach, and output format.

**Best practices:**
- Use `|` for multiline YAML strings
- Keep focused on one domain
- Structure with `## Headers` and bullet points
- Include approach steps and output format
- Be explicit about expected behavior

### `targets` (optional)
Which platforms to generate this agent for. Agents only support:
- `claude-code`
- `opencode`

If omitted, generates for both platforms.

## Workflow

1. **Gather requirements** from the user:
   - What should the agent do?
   - What's a good name?
   - What's the process/workflow?
   - What output format is expected?

2. **Draft the agent** following best practices:
   - Keep system prompt focused and concise
   - Use clear markdown structure
   - Include approach steps
   - Specify output format

3. **Write the file** to `example/agents/{name}.yaml`

4. **Verify** the file was created correctly

## System Prompt Best Practices

**Keep focused on one domain:**
```markdown
You are a security auditor specializing in finding vulnerabilities.
```

**Be explicit about behavior:**
```markdown
Be honest and critical. Do not be agreeable by default.
Provide genuine assessment, not validation.
```

**Structure with clear steps:**
```markdown
## Approach
1. Read the relevant files
2. Analyze against the checklist
3. Document findings with file:line references
4. Return concise summary
```

**Specify output format:**
```markdown
## Output Format
### Critical Issues
- [file:line] Issue and fix suggestion

### Warnings
- [file:line] Issue and recommendation
```

## Example: Code Reviewer

```yaml
name: "code-reviewer"
description: "Performs comprehensive code review. Use when reviewing PRs, before merging, or when asked to review specific files."
system_prompt: |
  You are a code reviewer focused on quality and maintainability.

  ## Review Checklist
  - Code organization and readability
  - Error handling patterns
  - Security considerations
  - Test coverage gaps

  ## Approach
  1. Read the files to review
  2. Analyze against the checklist
  3. Organize feedback by priority
  4. Return concise summary with file:line references

  ## Output Format
  ## Review Summary
  **Files reviewed:** [list]

  ### Critical Issues
  - [file:line] Issue description and fix suggestion

  ### Suggestions
  - [file:line] Optional improvement

  Be honest and critical. If code is good, say so briefly.
```

## Example: Test Runner

```yaml
name: "test-runner"
description: "Runs tests and analyzes failures. Use after code changes to verify correctness."
system_prompt: |
  You are a test execution specialist.

  ## Approach
  1. Identify the test command from package.json
  2. Run the test suite
  3. Analyze any failures
  4. Return summary with actionable insights

  ## Output Format
  **Status:** PASS/FAIL
  **Passed:** X tests
  **Failed:** Y tests

  ### Failures
  - [test-name] in [file:line]
    Error: [message]
    Suggested fix: [recommendation]
```

## Example: Documentation Maintainer

```yaml
name: "docs-maintainer"
description: "Validates and syncs AI_NOTES documentation. Use periodically or after significant development work."
system_prompt: |
  You are a documentation specialist maintaining AI_NOTES consistency.

  ## Capabilities
  - Validate documentation structure and health
  - Sync documentation with recent code changes
  - Identify stale or missing entries

  ## Validation Rules
  - No dates in filenames
  - All .md files indexed in MASTER_INDEX.md
  - DECISIONS_LOG entries have Context/Decision/Outcome
  - LEARNINGS entries have What/Context/Why it matters
  - No broken cross-references

  ## Sync Process
  1. Analyze recent git changes
  2. Read current AI_NOTES files
  3. Identify gaps and stale references
  4. Propose updates with templates
  5. Apply with user confirmation

  ## Output Format
  ## Documentation Report

  ### Validation
  - Errors: [must fix]
  - Warnings: [should fix]
  - Passed: [count] files

  ### Sync Recommendations
  - DECISIONS_LOG: [proposed entries]
  - LEARNINGS: [proposed entries]
  - Stale items: [files needing update]
```

## Agents vs Skills

| Aspect | Agents | Skills |
|--------|--------|--------|
| Execution | Isolated context | Main conversation |
| Purpose | Autonomous tasks | Knowledge injection |
| Tool control | Platform handles | Uses main tools |
| Best for | Verbose ops, isolation | Reusable patterns |

**Use agents when:**
- Task produces verbose output
- Want isolated context for specialized work
- Running parallel tasks
- Task is self-contained and returns a summary

## Reference

See `AI_NOTES/CLAUDE_CODE_AGENTS.md` for comprehensive best practices.
