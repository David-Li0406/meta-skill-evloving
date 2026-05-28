# Permission Modes

Detailed guide to Claude Code permission modes and how to switch between them.

## Mode Overview

Claude Code provides five permission modes that control how tool access is handled:

| Mode | Approval Behavior | Best For |
|------|-------------------|----------|
| `default` | Prompts on first use | Standard development |
| `plan` | Blocks all modifications | Code review, analysis |
| `acceptEdits` | Auto-accepts file edits | Trusted editing |
| `dontAsk` | Auto-denies unless whitelisted | Restricted environments |
| `bypassPermissions` | Skips all prompts | Trusted automation |

## Default Mode

Standard behavior where Claude prompts for permission on first use of each tool type.

### Behavior

| Tool Type | First Use | Subsequent Uses |
|-----------|-----------|-----------------|
| Read-only (Read, Glob, Grep) | No prompt | No prompt |
| File modification (Edit, Write) | Prompts | Session-approved |
| Bash commands | Prompts | Project-approved per command |
| Network (WebFetch) | Prompts | Request-approved |

### Configuration

```json
{
  "defaultMode": "default"
}
```

### CLI

```bash
claude --permission-mode default
```

### "Yes, don't ask again" Behavior

When you select "Yes, don't ask again" in default mode:

| Tool Type | Scope |
|-----------|-------|
| Bash commands | Permanently per project directory and command |
| File modifications | Until session end |
| Network requests | Per-request approval |

## Plan Mode

Read-only mode where Claude can analyze code but cannot make modifications.

### Behavior

- **Allowed**: Reading files, searching, analyzing
- **Blocked**: Writing files, editing, executing commands
- **Purpose**: Safe code review and analysis

### Configuration

```json
{
  "defaultMode": "plan"
}
```

### CLI

```bash
claude --permission-mode plan
```

### Use Cases

- Code review sessions
- Understanding unfamiliar codebases
- Security audits
- Documentation generation without changes
- Learning how code works

### Switching to Plan Mode

In an active session:
```
/plan
```

Or start a new session:
```bash
claude --permission-mode plan
```

## Accept Edits Mode

Automatically accepts file edit permissions for the session.

### Behavior

| Tool Type | Approval |
|-----------|----------|
| Read operations | No prompt |
| Edit/Write | Auto-approved |
| Bash commands | Still prompts |
| Network | Still prompts |

### Configuration

```json
{
  "defaultMode": "acceptEdits"
}
```

### CLI

```bash
claude --permission-mode acceptEdits
```

### Use Cases

- Refactoring sessions where many files change
- Automated code generation
- Trusted formatting/linting operations
- When you've reviewed changes in real-time

### Caution

Only use when you're actively monitoring Claude's file changes. Changes are made without confirmation.

## Don't Ask Mode

Auto-denies tools unless explicitly pre-approved via permissions rules.

### Behavior

- Tools not in `allow` list are automatically denied
- Provides maximum control over what Claude can do
- Requires explicit whitelist for each operation

### Configuration

```json
{
  "defaultMode": "dontAsk",
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(git status)",
      "Bash(npm test)"
    ]
  }
}
```

### CLI

```bash
claude --permission-mode dontAsk --allowedTools "Bash(git status)" "Read"
```

### Use Cases

- Restricted CI/CD environments
- Compliance-sensitive projects
- When running with untrusted inputs
- Minimal-permission automation

### Building an Allow List

Start restrictive and add permissions as Claude requests them:

```json
{
  "defaultMode": "dontAsk",
  "permissions": {
    "allow": []
  }
}
```

Then add tools as you approve them:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Bash(npm run build)",
      "Edit(/src/**)"
    ]
  }
}
```

## Bypass Permissions Mode

Skips all permission prompts. Use only in trusted, isolated environments.

### Behavior

- All tool operations proceed without prompting
- Maximum automation capability
- No safety confirmations

### Configuration

```json
{
  "defaultMode": "bypassPermissions"
}
```

### CLI

```bash
claude --dangerously-skip-permissions
```

Or:
```bash
claude --permission-mode bypassPermissions
```

### Requirements

Only use when ALL conditions are met:
- [ ] Running in isolated environment (VM, container)
- [ ] No access to sensitive data
- [ ] No network access to production systems
- [ ] Input sources are fully trusted
- [ ] You understand the risks

### Use Cases

- Isolated CI/CD pipelines
- Automated testing in sandboxed environments
- Trusted batch processing
- Development containers

### Security Warning

This mode should NEVER be used:
- On production systems
- With untrusted inputs
- On machines with sensitive data
- Without network isolation

## Switching Modes

### During a Session

Use slash commands to switch modes:

| Command | Switches To |
|---------|-------------|
| `/plan` | Plan mode (read-only) |
| `/permissions` | View/manage permissions |

### At Session Start

```bash
claude --permission-mode <mode>
```

### In Settings

```json
{
  "defaultMode": "<mode>"
}
```

## Mode Comparison Matrix

| Feature | default | plan | acceptEdits | dontAsk | bypassPermissions |
|---------|---------|------|-------------|---------|-------------------|
| Read files | Yes | Yes | Yes | If allowed | Yes |
| Edit files | Prompts | No | Auto | If allowed | Yes |
| Write files | Prompts | No | Auto | If allowed | Yes |
| Bash commands | Prompts | No | Prompts | If allowed | Yes |
| Network requests | Prompts | Prompts | Prompts | If allowed | Yes |
| Safe for untrusted | Yes | Yes | No | Yes | No |
| Good for automation | Medium | Low | Medium | High | High |

## Environment Variable

Set default mode via environment:

```bash
export CLAUDE_PERMISSION_MODE=plan
claude
```

## Combining with Other Settings

Modes work with permission rules:

```json
{
  "defaultMode": "default",
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Read"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  }
}
```

Even in `bypassPermissions` mode, `deny` rules are respected (enterprise managed settings can enforce this).

## Enterprise Considerations

Organizations can enforce modes through managed settings:

```json
// managed-settings.json (admin-controlled)
{
  "defaultMode": "dontAsk",
  "permissions": {
    "deny": [
      "Bash(curl *)",
      "Bash(wget *)"
    ]
  }
}
```

Users cannot override managed settings to less restrictive modes.
