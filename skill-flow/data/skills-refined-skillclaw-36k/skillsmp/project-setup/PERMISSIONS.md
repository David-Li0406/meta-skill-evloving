# Permissions Deep Dive

Comprehensive guide to Claude Code permission configuration, patterns, and security best practices.

## Permission Modes

Claude Code supports several permission modes:

| Mode | Description | Use Case |
|------|-------------|----------|
| `default` | Ask for most operations | Normal development |
| `plan` | Read-only mode | Code review, planning |
| `acceptEdits` | Auto-accept file edits | Trusted editing |
| `dontAsk` | Minimal prompts | Experienced users |
| `bypassPermissions` | Skip all permission checks | CI/CD, automation |

### Setting Permission Mode

```bash
# Start with specific mode
claude --permission-mode plan

# In conversation
/permissions plan
```

## Permission Configuration

### Structure

```json
{
  "permissions": {
    "allow": [
      "Tool",
      "Tool(pattern:*)"
    ],
    "deny": [
      "Tool(dangerous:*)"
    ]
  }
}
```

### Rule Precedence

1. **Explicit deny** - Always wins
2. **Explicit allow** - Permits action
3. **Default** - Prompts user

## Permission Patterns

### Basic Tool Permissions

| Pattern | Description |
|---------|-------------|
| `Read` | Allow all file reads |
| `Write` | Allow all file writes |
| `Edit` | Allow all file edits |
| `Glob` | Allow file globbing |
| `Grep` | Allow content search |
| `Bash` | Allow all bash commands |

### File Pattern Permissions

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Write(src/**)",
      "Write(tests/**)",
      "Write(*.md)",
      "Edit(src/**)",
      "Edit(tests/**)"
    ],
    "deny": [
      "Write(.env*)",
      "Write(*.key)",
      "Write(*.pem)",
      "Edit(.env*)",
      "Edit(secrets/**)"
    ]
  }
}
```

### Bash Command Patterns

```json
{
  "permissions": {
    "allow": [
      "Bash(bun:*)",
      "Bash(npm:*)",
      "Bash(npx:*)",
      "Bash(git:*)",
      "Bash(docker:*)",
      "Bash(make:*)",
      "Bash(cargo:*)",
      "Bash(python:*)",
      "Bash(pytest:*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(sudo:*)",
      "Bash(chmod 777:*)",
      "Bash(curl | sh:*)",
      "Bash(wget | sh:*)"
    ]
  }
}
```

### Pattern Syntax

| Syntax | Meaning | Example |
|--------|---------|---------|
| `*` | Wildcard (any characters) | `Bash(git:*)` matches `git status`, `git commit` |
| `**` | Recursive directory | `Write(src/**)` matches any file in src/ |
| Exact | Literal match | `Bash(npm install)` only matches `npm install` |

### Common Permission Patterns

#### Safe Read-Only Git

```json
{
  "allow": [
    "Bash(git status:*)",
    "Bash(git diff:*)",
    "Bash(git log:*)",
    "Bash(git show:*)",
    "Bash(git branch:*)"
  ]
}
```

#### Full Git Access

```json
{
  "allow": [
    "Bash(git:*)"
  ],
  "deny": [
    "Bash(git push --force:*)",
    "Bash(git reset --hard:*)"
  ]
}
```

#### Safe Docker

```json
{
  "allow": [
    "Bash(docker build:*)",
    "Bash(docker run:*)",
    "Bash(docker logs:*)",
    "Bash(docker ps:*)",
    "Bash(docker-compose up:*)",
    "Bash(docker-compose down:*)"
  ],
  "deny": [
    "Bash(docker rm -f:*)",
    "Bash(docker system prune:*)"
  ]
}
```

#### Safe Database

```json
{
  "allow": [
    "Bash(psql -c \"SELECT:*)",
    "Bash(psql -c \"EXPLAIN:*)"
  ],
  "deny": [
    "Bash(psql -c \"DROP:*)",
    "Bash(psql -c \"DELETE:*)",
    "Bash(psql -c \"TRUNCATE:*)"
  ]
}
```

## File and Directory Restrictions

### Protecting Sensitive Files

```json
{
  "permissions": {
    "deny": [
      "Read(.env*)",
      "Write(.env*)",
      "Edit(.env*)",
      "Read(*.key)",
      "Read(*.pem)",
      "Read(*.p12)",
      "Read(**/credentials.json)",
      "Read(**/secrets/**)",
      "Write(**/secrets/**)"
    ]
  }
}
```

### Restricting to Project Directory

```json
{
  "permissions": {
    "allow": [
      "Read(src/**)",
      "Read(tests/**)",
      "Read(docs/**)",
      "Read(package.json)",
      "Read(tsconfig.json)",
      "Write(src/**)",
      "Write(tests/**)",
      "Edit(src/**)",
      "Edit(tests/**)"
    ],
    "deny": [
      "Read(../**)",
      "Write(../**)",
      "Read(~/**)",
      "Write(~/**)"
    ]
  }
}
```

### Allow Specific File Types

```json
{
  "permissions": {
    "allow": [
      "Write(*.ts)",
      "Write(*.tsx)",
      "Write(*.js)",
      "Write(*.jsx)",
      "Write(*.json)",
      "Write(*.md)",
      "Write(*.css)",
      "Write(*.html)"
    ],
    "deny": [
      "Write(*.sh)",
      "Write(*.exe)",
      "Write(*.dll)"
    ]
  }
}
```

## MCP Tool Permissions

MCP tools follow the pattern `mcp__<server>__<tool>`.

### Allow Specific MCP Server

```json
{
  "permissions": {
    "allow": [
      "mcp__memory__*",
      "mcp__github__search_repositories",
      "mcp__github__list_issues"
    ],
    "deny": [
      "mcp__github__delete_*"
    ]
  }
}
```

### Allow All MCP Tools

```json
{
  "permissions": {
    "allow": [
      "mcp__*"
    ]
  }
}
```

## Team Permission Sharing

### Base Project Permissions

`.claude/settings.json` (committed):

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(bun:*)",
      "Bash(npm:*)",
      "Bash(git:*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(sudo:*)",
      "Write(.env*)"
    ]
  }
}
```

### Personal Overrides

`.claude/settings.local.json` (gitignored):

```json
{
  "permissions": {
    "allow": [
      "Write",
      "Edit",
      "Bash(docker:*)",
      "Bash(kubectl:*)"
    ]
  }
}
```

### Role-Based Permission Templates

#### Developer Permissions

```json
{
  "permissions": {
    "allow": [
      "Read", "Write", "Edit", "Glob", "Grep",
      "Bash(bun:*)", "Bash(npm:*)", "Bash(git:*)",
      "Bash(docker:*)"
    ],
    "deny": [
      "Bash(sudo:*)",
      "Bash(rm -rf:*)",
      "Write(.env.production)"
    ]
  }
}
```

#### Reviewer Permissions (Read-Only)

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)"
    ],
    "deny": [
      "Write",
      "Edit",
      "Bash"
    ]
  }
}
```

#### CI/CD Permissions

```json
{
  "permissions": {
    "allow": [
      "Read", "Write", "Edit", "Glob", "Grep",
      "Bash(bun:*)", "Bash(npm:*)",
      "Bash(git:*)",
      "Bash(docker:*)"
    ],
    "deny": [
      "Bash(sudo:*)",
      "Bash(rm -rf /*))"
    ]
  }
}
```

## Security Best Practices

### 1. Principle of Least Privilege

Start restrictive, add permissions as needed.

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep"
    ],
    "deny": []
  }
}
```

### 2. Protect Sensitive Files

Always deny access to secrets.

```json
{
  "deny": [
    "Read(.env*)",
    "Read(**/secrets/**)",
    "Read(*.key)",
    "Read(*.pem)",
    "Write(.env*)",
    "Edit(.env*)"
  ]
}
```

### 3. Restrict Dangerous Commands

Block destructive operations.

```json
{
  "deny": [
    "Bash(rm -rf:*)",
    "Bash(sudo:*)",
    "Bash(chmod 777:*)",
    "Bash(chown:*)",
    "Bash(mkfs:*)",
    "Bash(dd:*)",
    "Bash(curl | bash:*)",
    "Bash(wget | bash:*)"
  ]
}
```

### 4. Limit Network Access

Restrict external connections.

```json
{
  "deny": [
    "Bash(curl:*)",
    "Bash(wget:*)",
    "Bash(ssh:*)",
    "Bash(scp:*)",
    "Bash(rsync:*)"
  ]
}
```

### 5. Protect System Directories

Prevent access outside project.

```json
{
  "deny": [
    "Read(/etc/**)",
    "Read(/var/**)",
    "Read(/root/**)",
    "Read(~/.ssh/**)",
    "Write(/tmp/**)",
    "Write(~/**)"
  ]
}
```

## Permission Validation

### Check Active Permissions

```bash
# In Claude Code
/permissions

# View settings
claude config get permissions
```

### Test Permission Rules

Create test scenarios:

```bash
# Should be allowed
echo "Test: Write to src/"
# Claude attempts Write(src/test.ts)

# Should be denied
echo "Test: Write to .env"
# Claude attempts Write(.env) - should fail
```

### Audit Permission Usage

```bash
# Check what permissions were used
/history permissions

# View in transcript
cat ~/.claude/transcripts/*.jsonl | jq 'select(.type=="tool_use")'
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Always prompted | No allow rule | Add to `permissions.allow` |
| Denied despite allow | Deny rule exists | Check `permissions.deny` |
| Pattern not matching | Wrong syntax | Use `Tool(pattern:*)` format |
| MCP tool blocked | Missing MCP pattern | Add `mcp__server__*` |
| Local override not working | Wrong file name | Must be `settings.local.json` |

### Debug Permissions

```bash
# Start with debug mode
claude --debug

# Look for permission checks in output
```

## Quick Reference Cheatsheet

### Common Allow Patterns

```json
"allow": [
  "Read",                      // All reads
  "Write(src/**)",             // Write in src/
  "Edit(*.ts)",                // Edit TypeScript
  "Bash(bun:*)",               // All bun commands
  "Bash(git commit:*)",        // Specific command
  "mcp__memory__*"             // All memory tools
]
```

### Common Deny Patterns

```json
"deny": [
  "Write(.env*)",              // Protect env files
  "Bash(rm -rf:*)",            // Block dangerous rm
  "Bash(sudo:*)",              // Block sudo
  "Read(~/.ssh/**)",           // Protect SSH keys
  "mcp__*__delete_*"           // Block MCP deletes
]
```
