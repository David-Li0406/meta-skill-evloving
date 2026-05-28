---
name: agent-creation-and-subagent-configuration
description: Use this skill when creating and configuring Claude Code agents and subagents, optimizing existing ones, or structuring skills for specific tasks.
---

# Agent Creation and Subagent Configuration Skill

This skill provides comprehensive guidance for creating and configuring agents and subagents in Claude Code.

## Quick Reference: Agent vs Skill vs Command

| Type | Use When | Context | Invocation |
|------|----------|---------|------------|
| **Subagent** | Task needs isolation, custom tools, or separate context | Own window | Auto-matched or explicit |
| **Skill** | Reusable knowledge/patterns across tasks | Shared | Auto-discovered |
| **Slash Command** | Quick, repeatable workflow | Shared | Manual `/command` |

## 5-Step Agent Creation Workflow

### Step 1: Define Single Responsibility
Ask: "What ONE thing should this agent do exceptionally well?"

**Good examples:**
- "Review TypeScript for security vulnerabilities"
- "Generate database migration scripts"
- "Optimize React component performance"

### Step 2: Identify Minimal Tools
Only include what's necessary:

| Tool | Purpose |
|------|---------|
| `Read` | View files |
| `Edit` | Modify existing files |
| `Write` | Create new files |
| `Bash` | Run commands |
| `Glob` | Find files by pattern |
| `Grep` | Search file contents |
| `Task` | Delegate to other agents |
| `WebSearch` | Search the web |
| `WebFetch` | Fetch web content |

### Step 3: Choose Model

| Model | Use When | Cost | Speed |
|-------|----------|------|-------|
| `haiku` | Fast, simple tasks (exploration, search) | $ | Fast |
| `sonnet` | Balanced tasks (most use cases) | $$ | Medium |
| `opus` | Complex reasoning, critical decisions | $$$ | Slow |
| `inherit` | Use parent's model | - | - |

### Step 4: Write System Prompt

Structure:
```markdown
# Agent Name

You are specialized in [domain]. Your responsibilities:

1. [Primary responsibility]
2. [Secondary responsibility]

## How You Work

[Step-by-step approach]

## Examples

### Example 1: [Scenario]
Input: [What you receive]
Output: [What you produce]

### Example 2: [Edge case]
...

## What You DON'T Do

- [Anti-pattern 1]
- [Anti-pattern 2]
```

### Step 5: Create & Test

```bash
# Create agent file
cat > .claude/agents/my-agent.md << 'EOF'
---
name: my-agent
description: [Clear, matchable description]
tools: Read, Edit
model: sonnet
---

[System prompt here]
EOF

# Test by asking Claude to use it
> "Use my-agent to [task]"
```

## Creating Subagents

### Understanding Subagents

Subagents are specialized AI assistants that Claude Code can delegate tasks to. Each subagent:
- Operates in its own context window (preserving main conversation context)
- Has a specific purpose and expertise area
- Can be configured with specific tools and permissions
- Includes a custom system prompt guiding its behavior

### When to Create Subagents

**Create a subagent when:**
- Tasks require specialized expertise that benefits from focused instructions
- Context preservation is important (subagents don't pollute main context)
- The same specialized workflow is needed repeatedly
- Different tool permissions are needed for different tasks
- Parallel execution of independent tasks is desired

### Two Approaches to Subagents

#### Approach 1: File-Based Agents

Persistent subagent definitions stored as Markdown files.

**File Format:**
```markdown
---
name: agent-name
description: Description of when this agent should be used
tools: Read, Write, Bash, Glob, Grep  # Optional - omit to inherit all
model: sonnet  # Optional - sonnet, opus, haiku, or inherit
permissionMode: default  # Optional - see permission modes below
skills: skill1, skill2  # Optional - skills to auto-load
---

Your agent's system prompt goes here. This defines the agent's
role, capabilities, approach, and constraints.
```

#### Approach 2: Task Tool Invocation

Dynamic subagent dispatch using the Task tool for on-demand agents.

```bash
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: <the agent's instructions and task>
)
```

## Best Practices for Agent Creation

- **Focused purpose**: Single responsibility
- **Clear triggers**: When to activate
- **Concrete examples**: Code patterns
- **Quality checks**: Verification steps
- **Right tools**: Minimal necessary

## Common Agent Patterns

### Code Review Agent
```markdown
---
name: code-reviewer
description: Reviews code changes for quality, security, and best practices. Use after making code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

# Code Reviewer

Focus on:
- Security vulnerabilities (OWASP Top 10)
- Performance concerns
- Code clarity and maintainability
- Test coverage
```

### Debug Agent
```markdown
---
name: debugger
description: Diagnoses and fixes errors, test failures, and unexpected behavior. Use PROACTIVELY when errors occur.
tools: Read, Grep, Glob, Bash, Edit
model: sonnet
---

# Debugger

## Systematic Approach

1. **Reproduce**: Understand the exact failure
2. **Isolate**: Find the root cause location
3. **Understand**: Why is it failing?
4. **Fix**: Minimal change to resolve
5. **Verify**: Confirm fix works
6. **Prevent**: Add tests if missing
```

## Troubleshooting

### Agent Not Being Invoked
1. Check description includes clear trigger conditions
2. Add "PROACTIVELY" if automatic invocation is desired
3. Verify file is in correct location with correct frontmatter
4. Check for name conflicts with higher-priority agents

### Agent Using Wrong Tools
1. Verify tools field syntax (comma-separated, no brackets)
2. Check tool names are exactly correct (case-sensitive)
3. If tools should inherit, omit the field entirely

### Agent Behaving Incorrectly
1. Add more specific constraints
2. Include examples of correct behavior
3. Add "NEVER" rules for unwanted behaviors
4. Consider if the prompt is too long (move details to skills)

## Quick Reference

**Create project agent:**
```bash
mkdir -p .claude/agents
# Create .claude/agents/my-agent.md with frontmatter
```

**Create user agent:**
```bash
mkdir -p ~/.claude/agents
# Create ~/.claude/agents/my-agent.md with frontmatter
```

**Dispatch via Task:**
```bash
Task(subagent_type: "general-purpose", model: "opus", prompt: "...")
```

**View/manage agents:**
```bash
/agents
```