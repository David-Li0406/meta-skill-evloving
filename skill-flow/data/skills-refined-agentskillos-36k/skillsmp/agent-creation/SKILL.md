---
name: agent-creation
description: |
  Guides creating Claude Code agents, subagents, and skills.
  Use when building new agents, optimizing existing ones, or structuring skills.
allowed-tools: Write, Read, Edit, Bash, Glob
---

# Agent Creation Skill

## Quick Reference: Agent vs Skill vs Command

| Type | Use When | Context | Invocation |
|------|----------|---------|------------|
| **Subagent** | Task needs isolation, custom tools, or separate context | Own window | Auto-matched or explicit |
| **Skill** | Reusable knowledge/patterns across tasks | Shared | Auto-discovered |
| **Slash Command** | Quick, repeatable workflow | Shared | Manual `/command` |

## 5-Step Agent Creation Workflow

### Step 1: Define Single Responsibility
Ask: "What ONE thing should this agent do exceptionally well?"

Bad examples:
- "Handle all code tasks" (too broad)
- "Review code and deploy and write docs" (multiple responsibilities)

Good examples:
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

**Rule**: If unsure whether a tool is needed, leave it out. Add later if needed.

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

## Agent File Template

```markdown
---
name: agent-name-kebab-case
description: |
  Clear description of when to use this agent.
  Include keywords Claude will match against user requests.
  Add "Use PROACTIVELY" if it should auto-trigger.
tools: Read, Edit, Bash
model: sonnet
skills: skill1, skill2
permissionMode: default
---

# Agent Name

You are a specialized agent for [purpose].

## Responsibilities

1. **[Responsibility 1]**: [Description]
2. **[Responsibility 2]**: [Description]

## Workflow

When given a task:
1. [First step]
2. [Second step]
3. [Third step]

## Examples

### Example 1: [Common scenario]

**Input**: [Sample input]

**Output**: [Expected output with reasoning]

### Example 2: [Edge case]

**Input**: [Tricky input]

**Output**: [How to handle it]

## Constraints

- [Limitation 1]
- [Limitation 2]

## What NOT to Do

- Don't [anti-pattern]
- Avoid [mistake]
```

## Skill Creation Template

For reusable knowledge (not isolated tasks):

```markdown
# .claude/skills/my-skill/SKILL.md

---
name: my-skill
description: |
  Knowledge domain description.
  Keywords for auto-discovery.
allowed-tools: Read, Write
---

# Skill Name

## When This Applies

Use this skill when:
- [Condition 1]
- [Condition 2]

## Core Concepts

### Concept 1
[Explanation]

### Concept 2
[Explanation]

## Patterns

### Pattern 1: [Name]
```code
[Example]
```

### Pattern 2: [Name]
```code
[Example]
```

## Anti-Patterns

- **Don't**: [Bad practice]
- **Instead**: [Good practice]

## References

See [reference.md](reference.md) for detailed specifications.
```

## Slash Command Template

For quick, repeatable workflows:

```markdown
# .claude/commands/my-command.md

---
description: Brief description shown in /help
---

# My Command

[Full prompt that runs when user types /my-command]

Include:
- Context about what this does
- Specific instructions
- Expected workflow
```

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

Provide feedback as:
- CRITICAL: Must fix before merge
- WARNING: Should address soon
- SUGGESTION: Nice to have

Don't nitpick style (leave that to linters).
```

### Debug Agent
```markdown
---
name: debugger
description: Diagnoses and fixes errors, test failures, and unexpected behavior. Use PROACTIVELY when errors occur.
tools: Read, Grep, Glob, Bash, Edit
model: sonnet
skills: systematic-debugging
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

### Documentation Agent
```markdown
---
name: docs-writer
description: Creates and updates documentation. Use when code changes need docs updates.
tools: Read, Write, Edit, Glob
model: haiku
---

# Documentation Writer

Update docs when:
- New features added
- APIs changed
- Important decisions made

Follow existing doc style in the project.
Keep docs close to code (prefer inline JSDoc over separate files).
```

## Testing Your Agent

1. **Direct invocation**: "Use [agent-name] to [task]"
2. **Auto-discovery**: Just describe the task, see if Claude picks the right agent
3. **Edge cases**: Try unusual inputs
4. **Tool verification**: Confirm it only uses granted tools

## Iteration Tips

- Start minimal, add complexity as needed
- Watch for tool permission errors (add missing tools)
- Refine description if auto-discovery fails
- Add examples for common mistakes
