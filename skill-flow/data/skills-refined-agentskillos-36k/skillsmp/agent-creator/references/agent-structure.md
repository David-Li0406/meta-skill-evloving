# Agent Structure & Patterns Reference

## Agent File Format

Every agent is a Markdown file with YAML frontmatter:

```markdown
---
name: agent-name
description: When to use this agent (natural language)
tools: tool1, tool2, tool3  # Optional
model: sonnet  # Optional: sonnet, opus, haiku, or 'inherit'
permissionMode: default  # Optional
skills: skill1, skill2  # Optional
---

System prompt goes here.
Define agent's expertise, workflow, patterns, and behavior.
```

## YAML Frontmatter Fields

### Required Fields

#### `name` (Required)
- Unique identifier
- Lowercase letters and hyphens only
- Examples: `ui-designer`, `code-reviewer`, `data-analyst`

```yaml
name: ui-designer
```

#### `description` (Required)
- Natural language description
- When Claude should invoke this agent
- Use phrases like "Use PROACTIVELY" or "MUST BE USED" for automatic invocation

```yaml
description: Expert UI/UX designer. Use PROACTIVELY when creating interfaces, layouts, or visual components.
```

### Optional Fields

#### `tools`
- Comma-separated list of tools
- If omitted, inherits ALL tools from main thread
- Available tools: Read, Write, Edit, Glob, Grep, Bash, MCP tools

```yaml
# Specific tools
tools: Read, Write, Edit, Glob, Grep, Bash

# With MCP tools
tools: Read, Write, primeng:get_component_doc, primeng:search_components

# Omit to inherit all tools (recommended)
# tools: (not specified)
```

#### `model`
- Which AI model to use
- Options: `sonnet`, `opus`, `haiku`, `inherit`
- `inherit` = use same model as main conversation
- Default: `sonnet`

```yaml
model: sonnet      # Claude Sonnet
model: opus        # Claude Opus (most capable)
model: haiku       # Claude Haiku (fastest)
model: inherit     # Same as main conversation
```

#### `permissionMode`
- How agent handles permissions
- Options: `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore`

```yaml
permissionMode: default  # Standard behavior
```

#### `skills`
- Auto-load skills into agent's context
- Comma-separated list
- Skills provide reference documentation

```yaml
skills: angular-architecture, angular-best-practices, primeng-angular
```

---

## Agent System Prompt Structure

### Essential Sections

#### 1. Core Expertise
Define what the agent is an expert in:

```markdown
## Core Expertise

### Domain Area 1
- Skill 1
- Skill 2
- Skill 3

### Domain Area 2
- Capability A
- Capability B
```

#### 2. Workflow
Step-by-step process when invoked:

```markdown
## Workflow

When invoked:

1. **Understand Requirements**
   - What to analyze
   - What to check
   
2. **Execute Actions**
   - Step 1
   - Step 2
   
3. **Deliver Results**
   - Format
   - Quality checks
```

#### 3. Patterns & Examples
Common code patterns with examples:

```markdown
## Pattern 1: [Name]
[Description]

```[language]
// Code example
```

## Pattern 2: [Name]
[Description]
```

#### 4. Best Practices
What to do and what to avoid:

```markdown
## Best Practices

### Do's
- ✅ Practice 1
- ✅ Practice 2

### Don'ts
- ❌ Anti-pattern 1
- ❌ Anti-pattern 2
```

#### 5. Quality Checklist
Verification before completing:

```markdown
## Quality Checklist

Before completing:
- ✅ Check 1
- ✅ Check 2
- ✅ Check 3
```

---

## Agent Archetypes

### Type 1: Analyzer/Reviewer
**Purpose**: Analyze and provide feedback

```yaml
---
name: code-reviewer
description: Reviews code for quality, security, and best practices. Use after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer.

When invoked:
1. Run `git diff` to see changes
2. Analyze modified files
3. Check for issues
4. Provide feedback

Review for:
- Code quality
- Security vulnerabilities
- Performance issues
- Best practices compliance
```

### Type 2: Generator/Creator
**Purpose**: Create new code/content

```yaml
---
name: component-generator
description: Creates new components following best practices. Use when creating new features.
tools: Read, Write, Glob, Bash
model: sonnet
skills: angular-architecture, angular-best-practices
---

You are a component creation expert.

When invoked:
1. Understand requirements
2. Check existing patterns
3. Generate component structure
4. Include tests
5. Follow project conventions
```

### Type 3: Debugger/Fixer
**Purpose**: Fix problems and errors

```yaml
---
name: debugger
description: Debugs errors and fixes issues. Use when encountering errors or test failures.
tools: Read, Edit, Bash, Grep
model: sonnet
---

You are a debugging specialist.

When invoked:
1. Capture error message
2. Identify root cause
3. Implement minimal fix
4. Verify solution
5. Prevent recurrence
```

### Type 4: Researcher/Explorer
**Purpose**: Search and gather information

```yaml
---
name: codebase-explorer
description: Explores codebase to find information. Use for research tasks.
tools: Read, Glob, Grep, Bash
model: haiku  # Fast for searches
---

You are a codebase research expert.

When invoked:
1. Understand what to find
2. Search systematically
3. Analyze findings
4. Summarize results
```

### Type 5: Tester/QA
**Purpose**: Test and verify functionality

```yaml
---
name: test-writer
description: Writes comprehensive tests. Use after implementing features.
tools: Read, Write, Edit, Bash
model: sonnet
---

You are a testing expert.

When invoked:
1. Analyze code to test
2. Write unit tests
3. Write integration tests
4. Achieve >80% coverage
5. Verify tests pass
```

---

## Tool Selection Guide

### Read-Only Tools (Safe)
```yaml
tools: Read, Glob, Grep, Bash
```
Use for: Analyzers, reviewers, explorers

### Write Tools (Modifies Files)
```yaml
tools: Read, Write, Edit, Bash
```
Use for: Generators, fixers, refactorers

### Full Access (All Tools)
```yaml
# Omit tools field to inherit all
```
Use for: General-purpose agents

### MCP Tools
```yaml
tools: Read, Write, primeng:get_component_doc, figma:export_design
```
Use for: Agents that need specific integrations

---

## Model Selection Strategy

### Use Sonnet (Default)
- General-purpose tasks
- Balance of speed and capability
- Most common choice

```yaml
model: sonnet
```

### Use Opus
- Complex reasoning required
- Multi-step analysis
- High-quality output critical

```yaml
model: opus
```

### Use Haiku
- Fast searches
- Simple transformations
- Read-only operations
- Low-latency needed

```yaml
model: haiku
```

### Use Inherit
- Match main conversation model
- Consistent behavior
- User can control via main model choice

```yaml
model: inherit
```

---

## Skills Integration

### When to Auto-Load Skills

Load skills that provide:
- Reference documentation
- Code patterns
- Best practices
- Component libraries

```yaml
skills: angular-architecture, primeng-angular, chartjs
```

### Skills vs System Prompt

**Skills**: Reference material (read when needed)
**System Prompt**: Active instructions (always applied)

Example:
```yaml
skills: primeng-angular  # Reference for components
---

Use the primeng-angular skill to find components.
When user needs a table, search for p-table.
```

---

## Permission Modes

### default
Standard permission handling

### acceptEdits
Auto-accept edit suggestions

### bypassPermissions
Skip permission checks (use carefully)

### plan
Planning mode only (no execution)

### ignore
Ignore permission requests

```yaml
permissionMode: default  # Recommended for most agents
```

---

## Activation Triggers

### Proactive Activation
Use keywords in description:

```yaml
description: Use PROACTIVELY after code changes
description: MUST BE USED for all UI tasks
description: Invoke immediately when tests fail
```

### Domain-Specific Activation
Claude infers from context:

```yaml
description: Expert in React components and hooks
# Auto-invoked for React tasks

description: Database query optimization specialist
# Auto-invoked for SQL/database tasks
```

### Explicit Activation
User mentions agent directly:

```
User: Use the code-reviewer agent to check this
User: Ask the debugger to fix this error
```

---

## Common Patterns

### Pattern: Context Gathering
```markdown
When invoked:

1. **Gather Context**
   ```bash
   # Check project structure
   ls -la src/
   
   # Find relevant files
   find . -name "*.ts" -type f
   
   # Search for patterns
   grep -r "pattern" src/
   ```
```

### Pattern: Iterative Refinement
```markdown
When invoked:

1. Make initial changes
2. Verify results
3. If issues found, iterate
4. Final verification
```

### Pattern: Quality Gates
```markdown
Before completing:

1. Run linter
2. Run tests
3. Check coverage
4. Verify build passes
```

---

## Testing Agents

### Test Agent Structure
```bash
# 1. Create agent file
.claude/agents/test-agent.md

# 2. Test with explicit invocation
"Use test-agent to analyze this code"

# 3. Verify automatic invocation
"Analyze this code for issues"  # Should auto-invoke

# 4. Check agent transcript
# Look for agent-{id}.jsonl file
```

### Agent Debugging
```markdown
# Add debugging to system prompt:

When invoked:
1. Log: "Agent [name] started"
2. Execute task
3. Log: "Agent [name] completed"
```

---

## Multi-Agent Workflows

### Sequential Agents
```markdown
User: First analyze with code-reviewer, then fix with debugger

Claude:
1. Invokes code-reviewer
   - Analyzes code
   - Returns issues
2. Invokes debugger
   - Fixes issues
   - Verifies fixes
```

### Parallel Agents (Conceptual)
```markdown
User: Review both frontend and backend

Claude:
1. Invokes ui-reviewer for frontend
2. Invokes api-reviewer for backend
3. Combines results
```

---

## Best Practices

### Naming
- ✅ `code-reviewer` (clear, specific)
- ✅ `ui-designer` (role-based)
- ❌ `agent1` (generic)
- ❌ `my_agent` (underscores)

### Description
- ✅ "Expert React developer. Use for component creation."
- ✅ "Debugger specialist. Use PROACTIVELY for errors."
- ❌ "Does stuff" (too vague)
- ❌ "An agent" (no context)

### System Prompt
- ✅ Clear workflow steps
- ✅ Concrete examples
- ✅ Quality checklist
- ❌ Vague instructions
- ❌ No examples

### Tools
- ✅ Minimal necessary tools
- ✅ Omit for full access
- ❌ All tools when not needed
- ❌ Missing required tools

---

## Examples by Domain

### Frontend Agent
```yaml
---
name: frontend-expert
description: Frontend development expert. Use for UI, components, and styling.
tools: Read, Write, Edit, Glob, Grep, Bash
model: sonnet
skills: react-patterns, css-best-practices, component-library
---

You are a frontend development expert...
```

### Backend Agent
```yaml
---
name: backend-expert
description: Backend API and database expert. Use for services and data layer.
tools: Read, Write, Edit, Bash
model: sonnet
skills: api-design, database-patterns, security
---

You are a backend development expert...
```

### DevOps Agent
```yaml
---
name: devops-expert
description: DevOps and infrastructure expert. Use for CI/CD and deployment.
tools: Read, Write, Edit, Bash
model: sonnet
---

You are a DevOps expert...
```

### Data Agent
```yaml
---
name: data-analyst
description: Data analysis and SQL expert. Use for queries and analytics.
tools: Read, Write, Bash
model: sonnet
skills: sql-patterns, data-visualization
---

You are a data analysis expert...
```

---

## File Locations

### Project-Level (Highest Priority)
```
.claude/agents/agent-name.md
```
Available in current project only.

### User-Level
```
~/.claude/agents/agent-name.md
```
Available across all projects.

### Plugin-Provided
```
plugins/plugin-name/agents/agent-name.md
```
Provided by installed plugins.

### Priority Order
1. Project-level agents
2. CLI-defined agents
3. User-level agents
4. Plugin agents

---

## CLI Definition (Advanced)

```bash
claude --agents '{
  "agent-name": {
    "description": "When to use",
    "prompt": "System prompt here",
    "tools": ["Read", "Write"],
    "model": "sonnet"
  }
}'
```

Use for:
- Quick testing
- Session-specific agents
- Documentation examples

---

## Agent Lifecycle

1. **Creation**: Write .md file
2. **Loading**: Claude Code loads at startup
3. **Activation**: Claude invokes based on context
4. **Execution**: Agent runs in own context
5. **Completion**: Returns results to main thread

```
Main Thread → [Detects task] → Invokes Agent
                                    ↓
                              [Agent Context]
                                    ↓
                              [Executes Task]
                                    ↓
                              [Returns Results]
                                    ↓
Main Thread ← [Continues] ← Results
```

---

## Agent Communication

Agents communicate via:
- **Return values**: Results passed back to main thread
- **File modifications**: Changes to codebase
- **Transcripts**: Logged in agent-{id}.jsonl

Agents CANNOT:
- Call other agents (no nesting)
- Access main thread context directly
- Persist state between invocations

---

## Resumable Agents

```yaml
---
name: research-agent
description: Long-running research tasks. Can be resumed.
---

# Agent can be resumed later
# Each invocation gets unique agentId
# Use: "Resume agent {agentId}"
```

Use for:
- Long research tasks
- Iterative refinement
- Multi-session work

---

## Quality Metrics

Good agents have:
- ✅ Clear purpose
- ✅ Specific expertise
- ✅ Well-defined workflow
- ✅ Code examples
- ✅ Quality checklist
- ✅ Error handling
- ✅ Best practices

Avoid:
- ❌ Too broad scope
- ❌ Vague instructions
- ❌ No examples
- ❌ Missing tools
- ❌ No quality checks
