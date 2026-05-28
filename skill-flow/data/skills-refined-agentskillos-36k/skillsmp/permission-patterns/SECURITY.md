# Security Best Practices

Comprehensive security guidance for Claude Code permissions in individual, team, and enterprise environments.

## Core Security Principles

### Principle of Least Privilege

Grant only the permissions necessary for the task:

```json
{
  "defaultMode": "dontAsk",
  "permissions": {
    "allow": [
      "Read",
      "Bash(npm test)",
      "Bash(git status)"
    ]
  }
}
```

Start with minimal permissions and add as needed rather than starting permissive.

### Defense in Depth

Layer multiple security controls:

1. **Permission mode** - Set appropriate default mode
2. **Allow rules** - Whitelist specific operations
3. **Deny rules** - Explicitly block dangerous operations
4. **Sandboxing** - Enable filesystem/network isolation
5. **Hooks** - Add custom validation

## Sandboxing

### Enabling Sandbox Mode

```bash
/sandbox
```

### Sandbox Protections

| Protection | Description |
|------------|-------------|
| Filesystem isolation | Writes restricted to project directory |
| Parent directory protection | Cannot modify files above project root |
| Network controls | Configurable network access |
| Command restrictions | Blocked risky commands |

### Default Filesystem Boundaries

- **Allowed**: Read/write within project directory and subdirectories
- **Read-only**: Files outside project (system libraries, dependencies)
- **Blocked**: Parent directories, system files

## Command Security

### Always Block These Commands

```json
{
  "permissions": {
    "deny": [
      "Bash(rm -rf *)",
      "Bash(rm -rf /)",
      "Bash(curl *)",
      "Bash(wget *)",
      "Bash(sudo *)",
      "Bash(chmod 777 *)",
      "Bash(> /dev/*)",
      "Bash(mkfs *)",
      "Bash(dd *)"
    ]
  }
}
```

### Risky Commands to Review

| Command | Risk | Recommendation |
|---------|------|----------------|
| `curl`, `wget` | Fetch arbitrary content | Deny or use WebFetch |
| `sudo` | Elevated privileges | Deny in most cases |
| `rm -rf` | Destructive deletion | Deny with wildcards |
| `chmod 777` | Insecure permissions | Deny |
| `eval`, `exec` | Arbitrary execution | Review carefully |
| `env` | Expose secrets | Review carefully |

### Command Injection Detection

Claude Code detects suspicious commands and requires manual approval even if previously allowlisted. This includes:

- Commands with unusual redirects
- Commands with encoded content
- Commands accessing sensitive paths
- Commands with variable expansion risks

## File System Security

### Sensitive Files to Deny

```json
{
  "permissions": {
    "deny": [
      "Edit(/.env*)",
      "Edit(/.env)",
      "Edit(/.env.local)",
      "Edit(/.env.production)",
      "Edit(/secrets/**)",
      "Edit(/credentials/**)",
      "Edit(/*.key)",
      "Edit(/*.pem)",
      "Edit(/*.p12)",
      "Edit(/id_rsa*)",
      "Edit(/id_ed25519*)",
      "Edit(~/.ssh/**)",
      "Edit(~/.aws/**)",
      "Edit(~/.config/gcloud/**)",
      "Read(/.env*)",
      "Read(/secrets/**)"
    ]
  }
}
```

### Directory Restrictions

```json
{
  "permissions": {
    "deny": [
      "Edit(//etc/**)",
      "Edit(//usr/**)",
      "Edit(//var/**)",
      "Edit(//root/**)",
      "Edit(~/.ssh/**)",
      "Edit(~/.gnupg/**)"
    ]
  }
}
```

## Network Security

### WebFetch Controls

```json
{
  "permissions": {
    "allow": [
      "WebFetch(domain:docs.example.com)",
      "WebFetch(domain:api.internal.com)"
    ],
    "deny": [
      "WebFetch(domain:*)"
    ]
  }
}
```

### MCP Server Security

- Only enable MCP servers from trusted sources
- Review server permissions before enabling
- Use per-tool permissions rather than server-wide

```json
{
  "permissions": {
    "allow": [
      "mcp__github__search_repositories",
      "mcp__github__get_file_contents"
    ],
    "deny": [
      "mcp__github__delete_repository"
    ]
  }
}
```

## Team Security Policies

### Shared Project Settings

Create `.claude/settings.json` for team-wide policies:

```json
{
  "defaultMode": "default",
  "permissions": {
    "allow": [
      "Read",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(npm test:*)",
      "Bash(npm run lint:*)"
    ],
    "deny": [
      "Edit(/.env*)",
      "Edit(/secrets/**)",
      "Bash(curl *)",
      "Bash(wget *)"
    ]
  }
}
```

Commit this to version control for team consistency.

### Local Overrides

Create `.claude/settings.local.json` for individual settings (add to `.gitignore`):

```json
{
  "permissions": {
    "allow": [
      "Bash(npm install:*)"
    ]
  }
}
```

### Security Policy Template

```json
{
  "defaultMode": "default",
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(npm test:*)",
      "Bash(npm run build:*)",
      "Bash(npm run lint:*)"
    ],
    "ask": [
      "Edit",
      "Write",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(npm install:*)"
    ],
    "deny": [
      "Edit(/.env*)",
      "Edit(/secrets/**)",
      "Edit(/*.key)",
      "Edit(/*.pem)",
      "Bash(curl *)",
      "Bash(wget *)",
      "Bash(rm -rf *)",
      "Bash(sudo *)"
    ]
  }
}
```

## Enterprise Security

### Managed Settings

Organizations can enforce policies through managed settings that users cannot override:

```json
// managed-settings.json (admin-controlled)
{
  "defaultMode": "dontAsk",
  "permissions": {
    "deny": [
      "Bash(curl *)",
      "Bash(wget *)",
      "Edit(/.env*)",
      "Edit(/secrets/**)"
    ]
  }
}
```

### Enterprise Features

| Feature | Description |
|---------|-------------|
| Managed settings | Admin-enforced policies |
| Audit logging | All operations logged |
| Network restrictions | Configurable domain allowlists |
| Credential protection | Secure proxy for authentication |
| Branch restrictions | Git push limited to working branch |

### Cloud Execution Security

When using Claude Code in cloud/web environments:

- Isolated VMs per session
- Network access limited by default
- Automatic session cleanup
- Compliance logging enabled

## Windows-Specific Security

### WebDAV Warning

On Windows, avoid enabling WebDAV access:

```json
{
  "permissions": {
    "deny": [
      "Read(//\\\\*)",
      "Edit(//\\\\*)"
    ]
  }
}
```

WebDAV can trigger network requests that bypass the permission system.

## Prompt Injection Protection

### Built-in Protections

Claude Code includes safeguards against prompt injection:

1. Permission system requires approval for sensitive operations
2. Context-aware analysis of requests
3. Input sanitization
4. Command blocklist

### Best Practices with Untrusted Content

1. **Review suggested commands** before approval
2. **Avoid piping untrusted content** directly to Claude
3. **Verify file changes** before accepting
4. **Use virtual machines** for testing untrusted code
5. **Report suspicious behavior** with `/bug`

## Monitoring and Auditing

### View Active Permissions

```bash
/permissions
```

### Debug Mode

```bash
claude --debug
```

Shows permission rule evaluation and tool execution.

### OpenTelemetry Integration

Track Claude Code activity for compliance:

- Usage monitoring per user
- Operation logging
- Analytics and insights

## Security Checklist

### Before Starting a Project

- [ ] Review project security requirements
- [ ] Create appropriate `.claude/settings.json`
- [ ] Deny access to sensitive files
- [ ] Block dangerous commands
- [ ] Set appropriate default mode
- [ ] Test permissions with `/permissions`

### Ongoing Security

- [ ] Regularly review permission rules
- [ ] Update deny rules for new sensitive files
- [ ] Audit permission prompts you've approved
- [ ] Use plan mode for code review
- [ ] Enable sandbox for untrusted operations

### Enterprise Deployment

- [ ] Deploy managed settings
- [ ] Configure network restrictions
- [ ] Enable audit logging
- [ ] Train team on security practices
- [ ] Establish incident response procedures

## Reporting Security Issues

If you discover security vulnerabilities:

1. **Do not disclose publicly**
2. **Report via [HackerOne VDP](https://hackerone.com/anthropic-vdp)**
3. **Include reproduction steps**
4. **Allow time for remediation**

## Quick Reference: Security Levels

| Level | Mode | Key Settings |
|-------|------|--------------|
| Maximum Security | `dontAsk` | Explicit whitelist only |
| High Security | `default` | Deny dangerous, ask for changes |
| Standard | `default` | Allow common tools, deny dangerous |
| Development | `acceptEdits` | Auto-approve edits, deny dangerous |
| Trusted Automation | `bypassPermissions` | Isolated environment only |

Choose the level appropriate for your environment and security requirements.
