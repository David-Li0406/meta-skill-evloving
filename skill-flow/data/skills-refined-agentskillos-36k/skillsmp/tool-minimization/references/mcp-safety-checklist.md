# MCP Safety Checklist

Safety guidelines for using MCP (Model Context Protocol) servers in Kyora Agent OS.

## Core Safety Rules

### Rule 1: Treat MCP as Code Execution

- Local MCP servers execute code on your machine
- Only add trusted servers from known sources
- Review server code before enabling

### Rule 2: Never Paste Secrets

- Never paste API keys, tokens, or passwords in prompts
- Use VS Code input variables for sensitive values
- Never log secrets in MCP server outputs

### Rule 3: Keep Tool Counts Low

- Enable only tools needed for current task
- Disable entire servers when not in use
- Stay under model/tool limits (varies by model)

### Rule 4: Prefer Workspace Tools

- Use workspace read/search for local codebase
- MCP should supplement, not replace, workspace tools
- Don't use GitHub MCP for local-only tasks

## Pre-Use Checklist

Before enabling an MCP server:

- [ ] Server is from trusted source
- [ ] Server code has been reviewed (if local)
- [ ] Server doesn't require secrets in prompts
- [ ] Server tools are relevant to current task
- [ ] No other tool can accomplish the same goal

## Per-Server Guidelines

### Context7

**Purpose**: Up-to-date library documentation and code snippets.

**Safe to use when**:
- Learning a new library/framework
- Verifying API usage for unfamiliar dependencies
- Checking if library behavior has changed

**Do NOT use when**:
- Working with well-understood code
- Local patterns are sufficient
- Task doesn't involve third-party libraries

**Stop condition**: After finding the minimum needed information, stop querying.

### Playwright

**Purpose**: Browser automation, screenshots, UI testing.

**Safe to use when**:
- UI flows need verification
- RTL layout needs checking
- E2E smoke tests
- Screenshot capture for documentation

**Do NOT use when**:
- Simple backend-only tasks
- No UI component in scope
- Headless validation unnecessary

**Safety notes**:
- Don't navigate to untrusted URLs
- Don't input real credentials
- Use test/mock data only

### Chrome DevTools

**Purpose**: Layout, performance, and network debugging.

**Safe to use when**:
- Performance issues suspected
- Layout bugs hard to reproduce
- Network requests need inspection

**Do NOT use when**:
- No browser debugging needed
- Issue is purely backend
- Simpler tools would suffice

**Safety notes**:
- Don't capture sensitive network data
- Don't expose authentication tokens

### GitHub MCP

**Purpose**: GitHub issues, PRs, repository policies.

**Safe to use when**:
- Need issue/PR context
- Checking repository policies
- Cross-referencing with GitHub data

**Do NOT use when**:
- Task is local-only
- Workspace search is sufficient
- No GitHub integration needed

**Safety notes**:
- Don't create/modify issues without approval
- Don't expose private repository data
- Prefer read-only operations

## MCP Configuration

### Workspace Configuration

MCP servers configured in `.vscode/mcp.json` (workspace) or user settings.

Template available at: `.vscode/mcp.template.json`

### Tool List Reset

Tool lists are cached. Reset when:
- Server tools have changed
- New server added
- Tools behaving unexpectedly

Reset methods:
1. VS Code command: "Copilot: Reset Chat"
2. Restart VS Code
3. Start new chat session

## Incident Response

If MCP server behaves unexpectedly:

1. **Stop immediately**: Don't continue the task
2. **Disable the server**: Remove from enabled tools
3. **Document**: What happened, what commands ran
4. **Report**: To team/security if sensitive data involved
5. **Review**: Server code or configuration

## Secrets Handling

### Never Do

- Paste API keys in chat
- Include tokens in prompt text
- Log credentials in outputs
- Store secrets in MCP configs

### Always Do

- Use VS Code input variables
- Use environment variables
- Reference secrets by name, not value
- Rotate keys if accidentally exposed

## Summary Table

| Server | Default State | When to Enable | Safety Level |
|--------|---------------|----------------|--------------|
| Context7 | Off | New library/API | Medium |
| Playwright | Off | UI testing | Medium |
| Chrome DevTools | Off | Browser debugging | Medium |
| GitHub MCP | Off | GitHub context | Medium |

All servers should be **off by default** and enabled only when needed.

## SSOT Reference

- MCP + Tooling Policy: [KYORA_AGENT_OS.md#L791-L879](../../../KYORA_AGENT_OS.md#L791-L879)
- When NOT to use MCP: [KYORA_AGENT_OS.md#L847-L851](../../../KYORA_AGENT_OS.md#L847-L851)
