# Managing Subagents via /agents Command

The `/agents` command provides the recommended interactive interface for managing subagents.

## Opening /agents Interface

```
/agents
```

This opens an interactive menu with full management capabilities.

## Interactive Menu Options

### View All Available Subagents
Displays:
- Built-in subagents (Explore, Plan, general-purpose)
- User-level custom subagents (~/.claude/agents/)
- Project-level custom subagents (.claude/agents/)
- Plugin-provided subagents

Shows which are active when duplicates exist (project-level takes precedence).

### Create New Subagent
Guided setup process:
1. Enter subagent name (lowercase-with-hyphens format)
2. Enter description (5+ trigger keywords, 1024 chars max)
3. Optionally configure tools (pre-populated with all available tools - uncheck unnecessary ones)
4. Optionally set model (default inherits system model)
5. Enter system prompt with activation contexts and workflow
6. Choose location: project (.claude/agents/) or user (~/.claude/agents/)
7. Review and confirm

**Advantage**: Full tool list displayed visually - easier than manual YAML editing

### Edit Existing Custom Subagents
Select a custom subagent to modify:
- Update name
- Refine description
- Adjust tool permissions with visual tool selector
- Modify system prompt
- Change model selection
- Change location

### Delete Custom Subagents
Remove project or user-level custom subagents (built-in subagents cannot be deleted).

### Inspect Subagent Configuration
View complete configuration for any subagent:
- Name, description, trigger keywords
- Tool access list
- Model selection
- System prompt
- File location

## Tool Management in /agents

The tool selector shows:
- Core tools: Read, Write, Edit, Glob, Grep, Bash
- Code tools: NotebookEdit
- Web tools: WebFetch, WebSearch
- AI tools: Task (for delegating to other agents)
- MCP tools: All configured MCP server tools
- Plugin tools: Any tools provided by installed plugins

**MCP Tool Visibility**: When tools field omitted from agent YAML, all MCP tools automatically inherited. When tools field specified, only explicit tools available unless explicitly listed.

## Best Practices for /agents

### When to Use /agents
- Creating first custom subagent (interactive guidance valuable)
- Adjusting tool permissions (visual interface easier than manual editing)
- Team collaboration (changes via UI more discoverable than file edits)

### When to Use File Management
- Programmatic creation (automation scripts)
- Version control workflows (manual edits tracked in git)
- Complex multi-file setups (scripts can create supporting resources)
- Sharing agent definitions in documentation

## Workflow: Create Agent via /agents

1. Open interface: `/agents`
2. Select "Create New"
3. Set:
   - Name: `my-custom-agent` (lowercase-with-hyphens)
   - Description: Include 5+ trigger keywords
   - Tools: Uncheck unnecessary tools (or leave all checked for flexibility)
   - Model: Leave default or select inherit/haiku/sonnet/opus
   - System prompt: Paste your custom instructions
   - Location: Choose .claude/agents/ (project) or ~/.claude/agents/ (user)
4. Review configuration
5. Confirm creation
6. Agent immediately available for use
7. Verify in agent list or test with explicit invocation

## Resolving Issues

### Agent Not Appearing in /agents List
- **If project agent**: Verify file in `.claude/agents/{name}.md`
- **If user agent**: Verify file in `~/.claude/agents/{name}.md`
- **YAML syntax issue**: Check YAML delimiters (---), no tabs, required fields
- **Solution**: Restart Claude Code to reload agent list

### Tool Permissions Restricted Too Much
- Open /agents, select agent
- Expand tool list
- Check additional tools needed for agent's purpose
- Save changes
- Tool access immediately takes effect

### Agent Not Activating When Expected
- **Issue**: Description doesn't match invocation pattern
- **Check**: Does description include specific trigger keywords user would naturally use?
- **Solution**: Edit description to add more context-specific keywords
- **Test**: Try explicit invocation: "Use [agent-name] to [task]"

## /agents vs Direct File Management

| Task | /agents | Direct File |
|------|---------|------------|
| Creating first agent | ✓ Recommended | Requires YAML knowledge |
| Adjusting tools | ✓ Visual picker | Manual editing |
| Team collaboration | ✓ UI changes discoverable | Git tracking better |
| Automation/scripts | Manual steps | ✓ Programmatic |
| Batch creation | ✓ Repeatability | ✓ Bulk operations |
| Sharing definitions | List in docs | ✓ Copy full config |

