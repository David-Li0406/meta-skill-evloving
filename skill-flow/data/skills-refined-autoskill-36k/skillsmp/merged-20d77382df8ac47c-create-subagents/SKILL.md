---
name: create-subagents
description: Use this skill when creating specialized subagents for Claude Code, covering agent definitions, tool configurations, prompt structures, and testing methodologies.
---

# Creating Subagents

Subagents are specialized Claude instances that run in isolated contexts with focused roles and limited tool access. This skill teaches you how to create effective subagents, write strong system prompts, configure tool access, and orchestrate multi-agent workflows using the Task tool.

## Quick Start: Create an Agent

```markdown
---
name: my-agent
description: Use when [specific triggers] - [what the agent does].
tools: Read, Write, Edit  # Optional
model: sonnet             # Optional
---

You are an expert in [domain].

## Responsibilities
- Task 1
- Task 2

## Workflow

When invoked:
1. Step 1
2. Step 2
3. Deliver results

## Output Format
For each finding:
- **Severity:** Critical/High/Medium/Low
- **Location:** `file:line`
- **Issue:** What's vulnerable
- **Impact:** What attacker could do
- **Fix:** How to remediate
```

## Agent Structure

### Required Fields
- **name**: Unique identifier (lowercase-with-hyphens)
- **description**: Natural language description of purpose, including triggers for auto-delegation.

### Optional Fields
- **tools**: Comma-separated list of tools (or omit to inherit all).
- **model**: sonnet/opus/haiku/inherit (default: sonnet).
- **skills**: Skills to load into the subagent's context at startup.

## Tool Selection

| Tool | When to Include |
|------|-----------------|
| Read | Reading files, analyzing code |
| Grep | Searching code patterns |
| Glob | Finding files by pattern |
| Edit | Modifying existing files |
| Write | Creating new files |
| Bash | Running commands, git, tests |

## Workflow for Creating a Subagent

1. **Define the agent**:
   - Choose a descriptive name (lowercase, hyphens).
   - Write a clear description with trigger phrases.
   - Select minimum necessary tools.
   - Choose an appropriate model.

2. **Write system prompt**:
   - Define role and expertise.
   - List step-by-step process.
   - Include constraints and best practices.

3. **Configure location**:
   - Project (`.claude/agents/`) for team sharing.
   - User (`~/.claude/agents/`) for personal use.

4. **Test**:
   - Invoke explicitly: "Use the X agent to..."
   - Check `/agents` menu for registration.
   - Verify tool restrictions work.

## Best Practices

- **Focused Purpose**: Ensure the agent has a single responsibility.
- **Clear Triggers**: Define when the agent should be activated.
- **Concrete Examples**: Provide code patterns and expected outputs.
- **Quality Checks**: Include verification steps in the workflow.

## Common Patterns

### Code Reviewer
```markdown
---
name: code-reviewer
description: Use when reviewing code changes, pull requests, or verifying implementation quality - analyzes for bugs, style issues, and best practices.
tools: Read, Grep, Glob
model: opus
---

You are a senior engineer reviewing code for correctness, readability, and maintainability.

## Responsibilities
1. Identify bugs and edge cases
2. Check error handling
3. Verify naming and style consistency
4. Suggest improvements

## Workflow
1. Read the changed files
2. Analyze for issues
3. Provide structured feedback
```

### Research Agent
```markdown
---
name: researcher
description: Use when gathering information from the web, investigating APIs, or synthesizing documentation from multiple sources.
tools: Read, WebFetch, WebSearch
model: sonnet
---

You are a research specialist gathering and synthesizing information.

## Responsibilities
1. Search for relevant sources
2. Extract key information
3. Synthesize findings
4. Cite sources

## Workflow
1. WebSearch for relevant sources
2. WebFetch promising results
3. Extract and organize findings
4. Return structured synthesis with citations
```

## Testing Agents

1. **Baseline Test**: Run the task without the agent to document what went wrong.
2. **Agent Test**: Run with the agent to verify auto-delegation and output quality.
3. **Edge Case Testing**: Test with ambiguous inputs and tasks outside scope.
4. **Iteration**: Update agent definition based on test results and re-test.

## References

For complete documentation on:
- YAML fields reference
- All agent archetypes
- Tool selection guide
- Skills integration
- Multi-agent workflows
- Testing strategies