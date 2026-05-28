# Plugin Agents: Integration and Management

Understanding how plugins provide custom subagents and managing them alongside your own agents.

## What are Plugin Agents?

Plugins can include pre-built subagents alongside their other components (skills, commands, hooks).

**Plugin structure with agents**:
```
my-plugin/
├── agents/
│   ├── agent-1.md
│   ├── agent-2.md
├── skills/
├── commands/
└── plugin.json
```

**Characteristics**:
- Part of plugin distribution
- Automatically discovered by Claude Code
- Managed via /agents command like custom agents
- Cannot be deleted (read-only)
- Update via plugin updates

## Discovering Plugin Agents

### Via /agents Command
```
/agents
```

Lists all agents including:
- Built-in agents (Explore, Plan, general-purpose)
- Your custom agents (~/.claude/agents/, .claude/agents/)
- **Plugin agents** (automatically discovered from installed plugins)

Plugin agents appear with plugin prefix in names: `plugin-name:agent-name`

### Identifying Plugin Agents
Plugin agents in /agents list marked as:
- Source: "Plugin"
- Location: Cannot be edited/deleted (read-only)
- Managed via: Plugin update mechanism

## Using Plugin Agents

### Explicit Invocation
```
Use the plugin-name:security-auditor agent to analyze this code
```

### Automatic Delegation
Claude proactively selects plugin agents when:
- Task description matches agent's activation triggers
- Plugin agent is more specialized than built-in agents
- User hasn't disabled plugin agent via settings

## Common Plugin Agent Examples

### Plugin: security-toolkit
Might include agents:
- `security-toolkit:vulnerability-scanner` - Searches for security issues
- `security-toolkit:dependency-auditor` - Analyzes dependencies
- `security-toolkit:compliance-checker` - Checks compliance requirements

### Plugin: data-engineering
Might include agents:
- `data-engineering:sql-optimizer` - Optimizes SQL queries
- `data-engineering:data-validator` - Validates data pipelines
- `data-engineering:schema-analyzer` - Analyzes database schemas

### Plugin: frontend-dev
Might include agents:
- `frontend-dev:component-reviewer` - Reviews React components
- `frontend-dev:accessibility-auditor` - Checks accessibility
- `frontend-dev:performance-analyzer` - Analyzes frontend performance

## Managing Plugin Agent Conflicts

### Scenario: Duplicate Agent Names

If plugin provides agent with same name as your custom agent:

**Priority order**:
1. Project custom agent (.claude/agents/agent-name.md) - **Highest**
2. User custom agent (~/.claude/agents/agent-name.md)
3. Plugin agent (plugin-name:agent-name) - **Lowest**
4. Built-in agents

**Example**: If you have `~/.claude/agents/code-reviewer.md` AND plugin provides `security-plugin:code-reviewer`:
- Your custom `code-reviewer` activates when requested
- Access plugin version via `security-plugin:code-reviewer`

### Resolving Conflicts

**Option 1: Use plugin agent explicitly**
```
Use security-plugin:code-reviewer for security analysis
```

**Option 2: Rename your custom agent**
```yaml
name: custom-code-reviewer  # Different from plugin's code-reviewer
```

**Option 3: Override plugin agent (if needed for major conflict)**
Create custom agent with same name in .claude/agents/ (project-level only)

## Creating Agents for Your Plugin

If distributing a plugin with agents:

### Plugin Structure
```
my-plugin/
├── agents/
│   ├── specialized-agent-1.md
│   ├── specialized-agent-2.md
├── skills/
│   └── supporting-skill.md
├── commands/
│   └── command.md
└── plugin.json
```

### Agent Naming Convention
- Use meaningful names: `security-auditor`, `performance-optimizer`
- Avoid generic: `helper`, `analyzer`, `agent`
- Include domain: `python-security-auditor`, `react-component-reviewer`
- Plugin prefix added automatically: `plugin-name:agent-name`

### Agent File Format
Same as custom agents - YAML frontmatter + system prompt:

```yaml
---
name: specialized-agent
description: Specific purpose, triggered by keywords, activates in context
tools: Read, Glob, Grep  # Optional
model: sonnet  # Optional
---

## System Prompt
[Agent instructions...]
```

### Discovery Enhancement
Make agents discoverable by including:
- Plugin domain in description: "security", "performance", "data"
- Specific triggers: vulnerability types, metrics, patterns
- Clear use cases: "Use when analyzing Python code"
- Domain keywords: "OWASP", "performance", "accessibility"

**Example discovery-optimized description**:
```yaml
description: Audits Python code for OWASP Top 10 security vulnerabilities including SQL injection, command injection, and insecure deserialization. Use when analyzing Python applications for security issues or when user mentions security concerns.
```

## Best Practices

### For Plugin Developers
1. **Clear naming**: Agent names clearly indicate purpose and domain
2. **Specific descriptions**: Include 5+ trigger keywords for discovery
3. **Complementary agents**: Each agent single focused responsibility
4. **Avoid conflicts**: Use domain-specific names unlikely to conflict
5. **Tool restrictions**: Only grant necessary tools for security
6. **Documentation**: Include agent purpose and examples in plugin docs

### For Plugin Users
1. **Discover available agents**: Use `/agents` to see what plugins provide
2. **Check agent scope**: Read agent description before using
3. **Explicit invocation**: Use full name if explicit control needed
4. **Custom overrides**: Create custom agent if you need different behavior
5. **Report issues**: If plugin agent not activating, check description triggers

## Workflow: Using Plugin Agents

### Step 1: Discover
```
/agents
```
Review available plugin agents

### Step 2: Understand
Read plugin agent description and purpose

### Step 3: Use Implicitly (Automatic)
```
Analyze this Python code for security issues
```
Claude automatically delegates to matching plugin agent if available

### Step 4: Use Explicitly (Targeted)
```
Use security-toolkit:vulnerability-scanner to review this code
```

### Step 5: Customize if Needed
If plugin agent doesn't meet needs:
- Create custom agent with specific enhancements
- Custom agent takes precedence in priority
- Keep for team-specific workflows

## Troubleshooting Plugin Agents

### Agent Not Appearing in /agents

**Causes**:
- Plugin not installed (check plugin list in settings)
- Plugin agents/ directory misconfigured (contact plugin author)
- YAML syntax error in agent file (contact plugin author)

**Solution**:
- Restart Claude Code
- Reinstall plugin if corrupted
- Check plugin documentation

### Plugin Agent Not Activating

**Causes**:
- Description lacks your specific keywords
- Custom agent has same name (takes precedence)
- Agent's trigger context doesn't match your task

**Solutions**:
- Use explicit invocation: `/plugin-name:agent-name`
- Create custom agent if plugin doesn't match needs
- Contact plugin author to suggest description enhancement

### Conflicts with Custom Agents

**Issue**: Both plugin and custom agent available

**Solution**:
- Rename custom agent if plugin version preferred
- Or keep both - custom takes precedence
- Use explicit names if you want specific version

## Plugin Management Commands

Note: Managing plugin agents is done through plugin management, not direct file editing.

### View Plugin Details
In Claude Code settings → Installed Plugins → select plugin

Shows:
- Plugin description
- Included agents
- Included skills and commands
- Plugin version

### Update Plugins
Plugin managers handle agent updates. When plugin updates:
- New agents automatically available
- Existing agents enhanced
- Your custom agents unaffected
- Priority unchanged (custom still takes precedence)

### Disable Specific Plugin
Some plugin managers allow per-plugin disabling:
- Disables all agents from that plugin
- Custom agents remain active
- Built-in agents unaffected

