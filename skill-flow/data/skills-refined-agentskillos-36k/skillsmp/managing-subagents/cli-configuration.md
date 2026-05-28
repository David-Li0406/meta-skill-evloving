# CLI-Based Configuration: Dynamic Agents

Define subagents dynamically using the `--agents` CLI flag instead of saving agent files.

## Basic Syntax

```bash
claude --agents '{
  "agent-name": {
    "description": "Agent description",
    "prompt": "System prompt here",
    "tools": ["Read", "Grep", "Glob"],
    "model": "sonnet"
  }
}'
```

## JSON Format

Complete specification for CLI agent definitions:

### Required Fields
```json
{
  "name": {
    "description": "What agent does and when to use it"
  }
}
```

### Optional Fields
```json
{
  "name": {
    "description": "...",
    "prompt": "Agent system prompt...",
    "tools": ["Read", "Grep", "Glob"],
    "model": "sonnet"
  }
}
```

**Field Details**:
- `description`: Trigger keywords, use cases (same as file-based agents)
- `prompt`: System prompt (complete activation instructions)
- `tools`: Array of tool names (omit to inherit all tools)
- `model`: haiku|sonnet|opus|inherit (defaults to inherit)

## Use Cases

### 1. Session-Specific Agents

Create agent for current session only without saving files:

```bash
claude --agents '{
  "temp-analyzer": {
    "description": "Temporary analysis agent for this session",
    "prompt": "Analyze the provided code for patterns..."
  }
}'
```

**Benefit**: No file clutter, session-scoped agent, quick testing

### 2. Automation Scripts

Define agents in automation without creating agent files:

```bash
#!/bin/bash
claude --agents '{
  "ci-builder": {
    "description": "CI build automation agent",
    "prompt": "Run build pipeline...",
    "tools": ["Read", "Bash", "Grep"],
    "model": "haiku"
  }
}' <<< "Run build for $(git rev-parse --short HEAD)"
```

**Benefit**: Self-contained script, no agent file dependencies

### 3. Sharing Agent Definitions

Include agent config in documentation without requiring agent files:

```markdown
## Setup

Run Claude with this agent:

\`\`\`bash
claude --agents '{
  "project-assistant": {
    "description": "Project-specific assistant with domain knowledge",
    "prompt": "You are the assistant for ProjectX. Use this knowledge: [specific context]"
  }
}'
\`\`\`
```

**Benefit**: Copy-paste setup, documentation-embedded, no file installation

### 4. Testing Agent Configurations

Quickly test agent before saving as file:

```bash
# Test agent via CLI
claude --agents '{
  "test-agent": {
    "description": "Test description",
    "prompt": "Test system prompt"
  }
}' <<< "Test this agent"

# If it works, save as file
mkdir -p ~/.claude/agents
cat > ~/.claude/agents/test-agent.md <<'EOF'
---
name: test-agent
description: Test description
---

Test system prompt
EOF
```

**Benefit**: Iterate quickly before committing to files

## Complete Example

### Development Agent
```bash
claude --agents '{
  "dev-guide": {
    "description": "Development guide for project setup, patterns, troubleshooting. Use for onboarding developers, explaining project structure, or when newcomer asks 'how do I...'",
    "prompt": "You are the ProjectX development guide. Help developers by:\n1. Explaining project structure\n2. Sharing setup instructions\n3. Guiding through common workflows\n4. Troubleshooting issues\n\nKey information:\n- Tech stack: Node.js, React, PostgreSQL\n- Setup: npm install && npm run dev\n- Testing: npm test\n- Common issue: Clear npm cache if dependency issues\n\nProvide concise, actionable guidance.",
    "tools": ["Read", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

### Analysis Agent
```bash
claude --agents '{
  "codebase-explorer": {
    "description": "Explores codebase structure, finds files, understands architecture. Use for architecture questions, finding implementations, understanding module relationships.",
    "prompt": "Analyze the codebase structure. For each request:\n1. Find relevant files using Glob\n2. Examine patterns in the code\n3. Explain architecture and relationships\n4. Point to specific examples\n\nBe specific with file paths and line numbers.",
    "tools": ["Read", "Glob", "Grep", "Bash"],
    "model": "sonnet"
  }
}'
```

## Priority: CLI vs File-Based Agents

| Scenario | Preferred | Reason |
|----------|-----------|--------|
| Permanent agent | File-based | Persistence, git tracking |
| Team-shared agent | File-based | Collaboration, version control |
| Session-specific | CLI | No file clutter, quick setup |
| Testing new agent | CLI | Quick iteration |
| Automation script | CLI | Self-contained script |
| Documentation example | CLI | Easy copy-paste |
| Production use | File-based | Reliability, auditability |

## Multi-Agent CLI Configuration

Define multiple agents in single CLI invocation:

```bash
claude --agents '{
  "reviewer": {
    "description": "Code review agent",
    "prompt": "Review code..."
  },
  "analyzer": {
    "description": "Analysis agent",
    "prompt": "Analyze code..."
  },
  "fixer": {
    "description": "Fix bugs",
    "prompt": "Fix issues..."
  }
}'
```

All three agents available in single session.

## Precedence: Agent Priority

When duplicate agent names exist:

1. **CLI agents** (--agents flag) - Highest priority
2. **Project agents** (.claude/agents/) - Second
3. **User agents** (~/.claude/agents/) - Third
4. **Built-in agents** (Explore, Plan, general-purpose) - Lowest

CLI definition overrides all saved agents.

## Workflow: From Testing to File

Suggested workflow for developing production agents:

### Step 1: Test via CLI
```bash
# Quick test in CLI
claude --agents '{
  "new-agent": {
    "description": "Description",
    "prompt": "Prompt"
  }
}' <<< "test task"
```

### Step 2: Evaluate Agent Behavior
- Does it activate when expected?
- Does it perform the intended task?
- Are results correct?
- Any improvements needed?

### Step 3: Iterate
If needed, adjust agent definition and test again via CLI.

### Step 4: Promote to File
Once satisfied, save as permanent file:

```bash
cat > ~/.claude/agents/new-agent.md <<'EOF'
---
name: new-agent
description: Description
tools: Read, Grep
model: sonnet
---

Prompt here
EOF
```

### Step 5: Verify File Version
Test that file-based agent works identically to CLI version.

## Best Practices

1. **Escape quotes properly**: Use single quotes for bash, proper JSON escaping
2. **Keep prompts concise**: CLI flags get unwieldy with long prompts
3. **Use files for production**: CLI agents don't persist across sessions
4. **Document agent definitions**: Include in README or setup docs
5. **Version control file versions**: Save to git once stable
6. **Test before committing**: Don't save broken agents as files

## Escaping Guide

### Bash Single Quotes
```bash
claude --agents '{"agent": {"description": "Use single quotes for bash"}}'
```

### Newlines in Prompt
```bash
claude --agents '{
  "agent": {
    "prompt": "Line 1\nLine 2\nLine 3"
  }
}'
```

### Special Characters
```bash
# Escape quotes in JSON value
"description": "Use \"quoted text\" in description"

# Backslashes
"prompt": "Path: C:\\\\Users\\\\name"
```

