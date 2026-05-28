# Jira Integration Skill

Quick reference for using the Jira integration skill in PRISM.

## Quick Start

### 1. Setup (First Time Only)

Generate your Jira API token:
1. Visit: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Name it (e.g., "PRISM Local Dev")
4. Copy the token

Configure credentials:
```bash
# Create .env file in repository root
cp .env.example .env

# Add your credentials to .env
JIRA_EMAIL=your.email@resolve.io
JIRA_API_TOKEN=your_token_here
```

### 2. Usage

**Automatic Detection**:
```
User: "Let's work on PLAT-456"
# Skill automatically detects and fetches PLAT-456
```

**Explicit Command**:
```
User: "jira PLAT-789"
# Fetches and displays PLAT-789 details
```

**Proactive Inquiry**:
```
User: "Implement login feature"
Agent: "Do you have a JIRA ticket number so I can get more context?"
User: "PLAT-123"
# Fetches and displays context
```

## Features

- Automatic issue key detection (`PLAT-123`, `PROJ-456`)
- Fetch full issue details with acceptance criteria
- Show recent comments and context
- Display linked issues and dependencies
- Epic to Story to Task hierarchy
- Session caching (fetch once, use multiple times)
- Graceful degradation (continues if Jira unavailable)
- Read-only (safe, non-invasive)

## Commands

| Command | Description |
|---------|-------------|
| `jira {key}` | Fetch and display issue details |
| `jira-epic {key}` | Fetch epic with all child stories |
| `jira-search {jql}` | Search issues with JQL query |

## Integration with Other Skills

The Jira skill enhances all PRISM skills:

- **Story Master (sm)**: Fetch epics for decomposition
- **Developer (dev)**: Get story context for implementation
- **Product Owner (po)**: Validate stories against tickets
- **QA (qa)**: Get acceptance criteria for testing
- **Support (support)**: Investigate bugs with full context
- **Architect (architect)**: Review epic technical requirements
- **Peer (peer)**: Verify implementation against AC

## Examples

### Decomposing an Epic

```
User: "Decompose PLAT-789"

# Jira skill automatically:
# 1. Fetches epic details
# 2. Shows epic goal and AC
# 3. Lists existing child stories (to avoid duplication)
# 4. Provides context to Story Master skill
```

### Implementing a Story

```
User: "Implement PLAT-456"

# Jira skill automatically:
# 1. Fetches story details
# 2. Shows acceptance criteria
# 3. Displays technical notes from comments
# 4. Lists blocking issues
# 5. Provides context to Developer skill
```

### Investigating a Bug

```
User: "Investigate bug PLAT-999"

# Jira skill automatically:
# 1. Fetches bug details
# 2. Shows reproduction steps
# 3. Displays customer comments
# 4. Lists related bugs
# 5. Provides context to Support skill
```

## Troubleshooting

### "Jira authentication failed"

**Problem**: Invalid or missing credentials

**Solution**:
1. Verify `.env` file exists in repository root
2. Check `JIRA_EMAIL` is correct Atlassian email
3. Generate new API token and update `JIRA_API_TOKEN`
4. Restart terminal/IDE to reload environment

### "Access denied to PLAT-123"

**Problem**: You lack permission to view issue

**Solution**:
1. Verify you can view issue in Jira web UI
2. Request access from Jira administrator
3. Check issue key spelling

### "Issue PLAT-123 not found"

**Problem**: Issue doesn't exist

**Solution**:
1. Verify issue key spelling (uppercase, correct number)
2. Check if issue was deleted or moved
3. Try viewing in Jira web UI

### "Rate limit exceeded"

**Problem**: Too many requests in short time

**Solution**:
1. Wait 60 seconds before retrying
2. Use cached data from earlier in conversation
3. Avoid fetching same issue multiple times

## Configuration

Configuration in [core-config.yaml](../../../core-config.yaml):

```yaml
jira:
  enabled: true                              # Master switch
  baseUrl: https://resolvesys.atlassian.net  # Your Jira instance
  email: ${JIRA_EMAIL}                       # From .env file
  token: ${JIRA_API_TOKEN}                   # From .env file
  defaultProject: PLAT                       # Default project key
  issueKeyPattern: "[A-Z]+-\\d+"             # Issue key regex
```

## Security

**Best Practices**:
- Use environment variables (`.env` file)
- Each developer has their own API token
- `.env` file is gitignored (never commit!)
- Rotate tokens every 90 days
- Revoke unused tokens immediately

**Never**:
- Hardcode credentials in code
- Commit credentials to git
- Share API tokens with teammates
- Use passwords (API tokens only!)
- Embed credentials in URLs

## Documentation

**Detailed Guides**:
- [SKILL.md](../SKILL.md) - Complete skill overview
- [API Reference](./api-reference.md) - Jira REST API details
- [Extraction Format](./extraction-format.md) - Issue formatting standards
- [Authentication](./authentication.md) - Security and setup
- [Error Handling](./error-handling.md) - Troubleshooting guide

**Quick Links**:
- [Generate API Token](https://id.atlassian.com/manage-profile/security/api-tokens)
- [Jira Status](https://status.atlassian.com/)
- [JQL Documentation](https://support.atlassian.com/jira-service-management-cloud/docs/use-advanced-search-with-jira-query-language-jql/)

## FAQ

**Q: Is this read-only?**
A: Yes! The skill only fetches data, never creates or modifies issues.

**Q: Does this work automatically?**
A: Yes! Just mention an issue key (PLAT-123) and it fetches automatically.

**Q: Can I disable auto-detection?**
A: Yes, use `auto-detect off` command.

**Q: What if Jira is down?**
A: The skill gracefully degrades. It informs you and continues without Jira context.

**Q: Do I need a Jira license?**
A: You need access to view issues in Jira. A basic Jira Software license is sufficient.

**Q: Can I search for issues?**
A: Yes! Use `jira-search "project = PLAT AND type = Bug"`

## Support

**Issues**:
- Check [Error Handling Guide](./error-handling.md)
- Verify [Authentication Setup](./authentication.md)
- Review `.env` configuration

**Enhancement Requests**:
- Propose in team wiki or project documentation
- Consider custom field mappings for your Jira instance

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-11-20
