# Using MCP Resources and Prompts

Accessing resources via @ mentions and invoking MCP prompts as slash commands.

**Note**: For comprehensive prompt engineering and management, see the **managing-prompts skill**. This file focuses on MCP-specific prompt invocation patterns.

## MCP Resources

Resources provide data, documents, or structured information from MCP servers.

### Resource Reference Syntax

**Basic syntax:**
```
@server:protocol://resource/path
```

**Examples:**
```
@github:issue://123
@database:schema://users
@filesystem:file:///path/to/file
@docs:http://api-docs.example.com/endpoints
```

### Discovering Resources

Type `@` in conversation to see available resources:

```
@github [autocomplete shows available resources]
@github:issue/
@github:pr/
@github:repo/
```

Resource paths are fuzzy-searchable - start typing and autocomplete suggests options.

## Resource Usage Examples

### Example 1: GitHub Issues

Reference specific issue:

```
@github:issue://owner/repo/123
```

Use in prompt:

```
"Analyze the bug described in @github:issue://anthropics/claude-code/456 and suggest a fix"
```

Claude Code:
1. Fetches issue #456 from claude-code repository
2. Includes content as context
3. Uses for analysis

### Example 2: Database Queries

Reference database results:

```
@postgres:schema://users
@postgres:query://select_top_users
```

Use in prompt:

```
"Show me statistics about @postgres:query://active_users_last_week"
```

### Example 3: Multiple Resources

Combine resources in single prompt:

```
"Compare @github:pr://123 implementation with @docs:architecture://database-design and suggest improvements"
```

Claude Code fetches:
- PR #123 content
- Architecture documentation
- Uses both for comparison

## MCP Prompts as Slash Commands

MCP servers can expose prompts that become slash commands.

**For prompt authoring and templates**: See managing-prompts skill

### Prompt Command Syntax

**Format:**
```
/mcp__server__prompt_name
```

**Examples:**
```
/mcp__github__list_prs
/mcp__github__pr_review 456
/mcp__jira__create_issue "Bug Title" high
```

### Prompt Execution

MCP prompts:
- Auto-discovered from connected servers
- Appear in slash command autocomplete
- Accept space-separated arguments
- Parsed by MCP server based on prompt definition

## Output Handling

### Output Limits

Claude Code monitors MCP tool and resource output:

**Thresholds:**
- Warning: 10,000 tokens
- Maximum: 25,000 tokens (configurable)

**When limit approaches:**
- Claude Code displays warning
- Suggests filtering or pagination if available
- Can continue or adjust query

### Configuring Output Limits

Set `MAX_MCP_OUTPUT_TOKENS` environment variable:

```bash
# Increase limit to 50,000 tokens
MAX_MCP_OUTPUT_TOKENS=50000 claude

# Set very high limit for data-heavy queries
MAX_MCP_OUTPUT_TOKENS=100000 claude
```

Default: 25,000 tokens

### Large Output Strategies

When MCP returns large data:

1. **Filter in query:** Use MCP server parameters to filter data
   ```
   /mcp__database__query --limit 100 --where "status='active'"
   ```

2. **Paginate:** Ask MCP server for pagination
   ```
   /mcp__database__query --page 1 --per-page 50
   ```

3. **Increase limit:** If large output needed
   ```bash
   MAX_MCP_OUTPUT_TOKENS=60000 claude
   ```

4. **Split queries:** Multiple smaller requests instead of one large query

## Real-World Workflow Examples

### Example 1: GitHub PR Review

Workflow:
1. List open PRs: `/mcp__github__list_prs`
2. Review specific PR: `/mcp__github__pr_review 123`
3. Reference code in PR: `@github:pr://123`
4. Request improvements based on fetched content

```
/mcp__github__list_prs

// Result shows PR #789 interesting
/mcp__github__pr_review 789

// Use in analysis
"Review the implementation in @github:pr://789 and suggest refactoring opportunities"
```

### Example 2: Database Analysis

Workflow:
1. Query table schema: `/mcp__database__schema users`
2. Query data: `/mcp__database__query_table users --limit 100`
3. Reference in analysis: `@database:table://users`
4. Request insights

```
/mcp__database__schema users

// Returns schema info
/mcp__database__query_table users --limit 100

// Use for analysis
"Analyze @database:table://users and identify performance optimization opportunities"
```

### Example 3: Jira Workflow

Workflow:
1. List issues: `/mcp__jira__list_issues --project ENG --status Open`
2. Reference specific issue: `@jira:issue://ENG-4521`
3. Create related issues: `/mcp__jira__create_issue "Related task" high`

```
/mcp__jira__list_issues --project ENG --status open

// Check issue ENG-4521
"Analyze @jira:issue://ENG-4521 and create related subtasks"

/mcp__jira__create_issue "Subtask 1: Database migration" high
/mcp__jira__create_issue "Subtask 2: API updates" high
```

### Example 4: API Documentation

Workflow:
1. Search documentation: `/mcp__docs__search_api "authentication"`
2. Reference endpoint: `@docs:http://api.example.com/v1/auth`
3. Request implementation

```
/mcp__docs__search_api "authentication"

// Returns relevant docs
"Implement authentication based on @docs:http://api-docs.example.com/auth and show example code"
```

## Resource and Prompt Availability

### Checking Server Status

Command to check all MCP servers and their capabilities:

```
/mcp
```

Shows:
- Connected servers
- Connection status
- Available resources (if server supports)
- Available prompts (if server supports)
- Authentication status

### Server-Specific Capabilities

Different MCP servers provide different capabilities:

- **GitHub:** Issues, PRs, code references as resources; review, analyze prompts
- **Jira:** Issues as resources; search, create, update prompts
- **Database:** Tables, queries as resources; query prompts
- **Filesystem:** Files as resources; read, write prompts
- **Slack:** Messages, channels as resources; post, search prompts

Verify with `/mcp` command which resources/prompts each server provides.

## Best Practices

### Resources

1. **Use fuzzy search:** Start typing resource path, autocomplete helps
2. **Reference in context:** Include @ references when asking for analysis
3. **Watch output size:** Large documents may hit token limits
4. **Filter as needed:** Use resource parameters to limit data scope

### Prompts

1. **Check parameters:** Understand what arguments each prompt expects
2. **Use consistently:** Learn prompt names for faster typing
3. **Combine with resources:** Use prompts to gather data, resources for analysis
4. **Test authorization:** Some prompts may require authentication

### Performance

1. **Set appropriate output limits:** Don't set too high unnecessarily
2. **Use pagination:** For large result sets, prefer paginated queries
3. **Cache when possible:** If repeatedly accessing same resource, consider storing locally
4. **Batch operations:** Group related queries to reduce round trips

## Troubleshooting

**Resources not appearing in autocomplete:**
- Verify MCP server supports resources (check `/mcp`)
- Confirm server is connected and authenticated
- Try full path if fuzzy search not working

**Prompts not executable:**
- Check server is listed in `/mcp`
- Verify prompt name spelling
- Confirm arguments match prompt definition
- Check authentication if needed

**Output limit warnings:**
- Increase `MAX_MCP_OUTPUT_TOKENS` if legitimate large output needed
- Filter query results if possible
- Use pagination for large datasets
- Split into multiple smaller queries

**Resource fetch fails:**
- Verify resource path exists and is accessible
- Check authentication if resource is private
- Try `/mcp` to confirm server connectivity
- Look for server-specific authentication requirements

**Prompt argument errors:**
- Check prompt definition for required/optional arguments
- Verify argument format (strings need quotes, etc.)
- Try prompt without arguments to see usage help
