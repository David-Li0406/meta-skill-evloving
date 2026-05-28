# Project Setup Checklists

Complete checklists for setting up Claude Code in new projects, migrating existing projects, and onboarding team members.

## New Project Setup

### Prerequisites

- [ ] Claude Code CLI installed (`claude --version`)
- [ ] Project repository initialized
- [ ] Basic project structure exists

### Step 1: Create Directory Structure

- [ ] Create `.claude/` directory
- [ ] Create `.claude/commands/` directory (optional)
- [ ] Create `.claude/skills/` directory (optional)
- [ ] Create `.claude/hooks/` directory (optional)

```bash
mkdir -p .claude/{commands,skills,hooks}
```

### Step 2: Create CLAUDE.md

- [ ] Create `CLAUDE.md` in project root
- [ ] Add project overview
- [ ] Document common commands
- [ ] Describe architecture
- [ ] Note code style preferences
- [ ] Add important gotchas

```bash
cat > CLAUDE.md << 'EOF'
# CLAUDE.md

## Project Overview
[Description]

## Commands
```bash
bun install    # Install dependencies
bun dev        # Development server
bun test       # Run tests
bun build      # Build for production
```

## Architecture
[Key directories]

## Code Style
- [Preferences]

## Notes
- [Important information]
EOF
```

### Step 3: Configure Settings

- [ ] Create `.claude/settings.json`
- [ ] Configure permissions
- [ ] Set environment variables
- [ ] Add hooks (optional)

```bash
cat > .claude/settings.json << 'EOF'
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
      "Bash(sudo:*)"
    ]
  },
  "env": {},
  "hooks": {}
}
EOF
```

### Step 4: Set Up Personal Overrides

- [ ] Create `.claude/settings.local.json`
- [ ] Add personal permissions
- [ ] Set local environment variables

```bash
cat > .claude/settings.local.json << 'EOF'
{
  "permissions": {
    "allow": [
      "Write",
      "Edit"
    ]
  },
  "env": {}
}
EOF
```

### Step 5: Update .gitignore

- [ ] Add local settings to .gitignore
- [ ] Add any MCP data directories

```bash
cat >> .gitignore << 'EOF'

# Claude Code
.claude/settings.local.json
.claude/*.local.json
.mcp-data/
EOF
```

### Step 6: Configure MCP Servers (Optional)

- [ ] Create `.mcp.json` for shared servers
- [ ] Add required servers
- [ ] Set environment variable references

```bash
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
EOF
```

### Step 7: Create Project Commands (Optional)

- [ ] Create common slash commands
- [ ] Document command usage

```bash
cat > .claude/commands/test.md << 'EOF'
---
description: Run project tests
allowed-tools: Bash(bun test:*)
---

Run all tests for the project:

```bash
bun test
```

Report any failures with clear explanations.
EOF
```

### Step 8: Verify Setup

- [ ] Run `/init` in Claude Code
- [ ] Check `/permissions` shows correct config
- [ ] Verify MCP servers with `/mcp`
- [ ] Test a simple command

### Validation Checklist

- [ ] `.claude/settings.json` is valid JSON
- [ ] `.claude/settings.local.json` is in .gitignore
- [ ] `CLAUDE.md` exists and is readable
- [ ] Project commands work
- [ ] MCP servers connect

---

## Existing Project Migration

### Assessment

- [ ] Check for existing `.claude/` directory
- [ ] Look for existing `CLAUDE.md` files
- [ ] Identify current permissions setup
- [ ] Note any existing hooks or commands

### Step 1: Backup Existing Config

- [ ] Copy existing `.claude/` directory
- [ ] Save current settings

```bash
cp -r .claude .claude.backup
```

### Step 2: Create Missing Structure

- [ ] Add missing directories
- [ ] Create settings files if missing

```bash
mkdir -p .claude/{commands,skills,hooks}
touch .claude/settings.json
touch .claude/settings.local.json
```

### Step 3: Migrate Settings

- [ ] Move permissions to new format
- [ ] Consolidate environment variables
- [ ] Update hook configurations

**Old format:**
```json
{
  "allowedTools": ["Read", "Write"]
}
```

**New format:**
```json
{
  "permissions": {
    "allow": ["Read", "Write"],
    "deny": []
  }
}
```

### Step 4: Update CLAUDE.md

- [ ] Add missing sections
- [ ] Update commands
- [ ] Refresh architecture docs
- [ ] Add recent learnings

### Step 5: Test Migration

- [ ] Run `/init` to verify
- [ ] Check permissions work
- [ ] Test existing workflows
- [ ] Verify hooks still run

### Step 6: Remove Backup

- [ ] Confirm everything works
- [ ] Remove backup directory

```bash
rm -rf .claude.backup
```

---

## Team Onboarding

### For New Team Members

#### Prerequisites

- [ ] Claude Code CLI installed
- [ ] Repository cloned
- [ ] Required environment variables set

#### Step 1: Review Project Setup

- [ ] Read `CLAUDE.md`
- [ ] Review `.claude/settings.json`
- [ ] Check available commands (`.claude/commands/`)
- [ ] Understand project skills (`.claude/skills/`)

#### Step 2: Create Personal Settings

- [ ] Create `.claude/settings.local.json`
- [ ] Add personal permissions
- [ ] Set personal environment overrides

```bash
cat > .claude/settings.local.json << 'EOF'
{
  "permissions": {
    "allow": [
      "Write",
      "Edit"
    ]
  },
  "env": {
    "DEBUG": "true"
  }
}
EOF
```

#### Step 3: Set Up Environment

- [ ] Copy `.env.example` to `.env`
- [ ] Fill in required values
- [ ] Set MCP server credentials

#### Step 4: Verify Setup

- [ ] Start Claude Code in project
- [ ] Run `/init`
- [ ] Check `/permissions`
- [ ] Test `/mcp` status
- [ ] Run a test command

#### Step 5: Learn Project Conventions

- [ ] Review commit message format
- [ ] Understand branching strategy
- [ ] Learn testing requirements
- [ ] Know deployment process

### For Team Leads

#### Setting Up Shared Configuration

- [ ] Define base permissions
- [ ] Create common commands
- [ ] Set up shared MCP servers
- [ ] Document in CLAUDE.md

#### Onboarding Checklist Template

Create `.claude/ONBOARDING.md`:

```markdown
# Team Onboarding Checklist

## Before Starting
- [ ] Install Claude Code CLI
- [ ] Clone repository
- [ ] Get access to required services

## Environment Setup
- [ ] Copy `.env.example` to `.env`
- [ ] Get API keys from team lead
- [ ] Set up database access

## Claude Code Setup
- [ ] Create `.claude/settings.local.json`
- [ ] Review available slash commands
- [ ] Test MCP server connections

## Verification
- [ ] Run `/init` successfully
- [ ] Complete a test task
- [ ] Submit first PR
```

---

## CI/CD Preparation

### Prerequisites

- [ ] CI/CD system supports Claude Code
- [ ] API keys available for CI
- [ ] Permissions reviewed for automation

### Step 1: Create CI Configuration

- [ ] Add CI-specific settings
- [ ] Configure appropriate permissions
- [ ] Set up environment variables

```json
// .claude/settings.ci.json
{
  "permissions": {
    "allow": [
      "Read", "Write", "Edit", "Glob", "Grep",
      "Bash(bun:*)", "Bash(npm:*)", "Bash(git:*)"
    ],
    "deny": [
      "Bash(sudo:*)"
    ]
  }
}
```

### Step 2: Set Up API Keys

- [ ] Store API key in CI secrets
- [ ] Configure key rotation (if needed)
- [ ] Test key access

```yaml
# GitHub Actions example
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Step 3: Create CI Commands

- [ ] Create automation-specific commands
- [ ] Test in CI environment

```bash
cat > .claude/commands/ci-review.md << 'EOF'
---
description: CI code review
allowed-tools: Read, Grep, Glob
---

Review the changed files and provide feedback:
- Check for code style issues
- Identify potential bugs
- Suggest improvements
EOF
```

### Step 4: Test CI Integration

- [ ] Run test workflow
- [ ] Verify permissions work
- [ ] Check output formatting
- [ ] Confirm error handling

---

## Security Review

### Permission Audit

- [ ] Review all `allow` rules
- [ ] Verify `deny` rules are comprehensive
- [ ] Check for overly permissive patterns
- [ ] Ensure sensitive files protected

### Sensitive File Checklist

- [ ] `.env*` files protected
- [ ] `*.key` files denied
- [ ] `*.pem` files denied
- [ ] Credentials directories blocked
- [ ] SSH keys protected

```json
{
  "deny": [
    "Read(.env*)",
    "Write(.env*)",
    "Edit(.env*)",
    "Read(*.key)",
    "Read(*.pem)",
    "Read(**/credentials.json)",
    "Read(~/.ssh/**)"
  ]
}
```

### Command Restrictions

- [ ] `rm -rf` blocked
- [ ] `sudo` blocked
- [ ] Dangerous chmod blocked
- [ ] Network commands reviewed

### MCP Server Review

- [ ] Review server permissions
- [ ] Check credential handling
- [ ] Verify server sources
- [ ] Test server sandboxing

### Compliance Checklist

- [ ] Permissions meet company policy
- [ ] Sensitive data handled correctly
- [ ] Audit logging in place
- [ ] Access controls documented

---

## Quick Start Templates

### Minimal Setup (5 minutes)

```bash
# Create structure
mkdir -p .claude
cat > CLAUDE.md << 'EOF'
# Project Name
Basic project description.
## Commands
- `bun dev` - Start dev server
EOF

cat > .claude/settings.json << 'EOF'
{"permissions":{"allow":["Read","Glob","Grep"],"deny":[]}}
EOF

echo ".claude/settings.local.json" >> .gitignore
```

### Standard Setup (15 minutes)

```bash
# Create structure
mkdir -p .claude/{commands,hooks}

# CLAUDE.md
cat > CLAUDE.md << 'EOF'
# CLAUDE.md
## Overview
[Description]
## Commands
- `bun install` - Install deps
- `bun dev` - Start dev
- `bun test` - Run tests
## Code Style
- TypeScript preferred
- Prefer for-loops over forEach
EOF

# Settings
cat > .claude/settings.json << 'EOF'
{
  "permissions": {
    "allow": [
      "Read", "Glob", "Grep",
      "Bash(bun:*)", "Bash(git:*)"
    ],
    "deny": ["Bash(rm -rf:*)", "Bash(sudo:*)"]
  }
}
EOF

# Local settings
cat > .claude/settings.local.json << 'EOF'
{"permissions":{"allow":["Write","Edit"]}}
EOF

# gitignore
echo ".claude/settings.local.json" >> .gitignore
```

### Full Setup (30 minutes)

Follow complete "New Project Setup" checklist above.

---

## Troubleshooting Setup Issues

| Issue | Check | Solution |
|-------|-------|----------|
| Settings not loading | JSON syntax | Run `jq . .claude/settings.json` |
| Permissions denied | Allow rules | Add to `permissions.allow` |
| Commands not appearing | File location | Must be in `.claude/commands/` |
| MCP not connecting | Server status | Run `/mcp` and check logs |
| CLAUDE.md not read | File location | Must be in cwd or project root |
| Hooks not running | Script permissions | Run `chmod +x script.sh` |
| Local settings ignored | Filename | Must be `settings.local.json` |
