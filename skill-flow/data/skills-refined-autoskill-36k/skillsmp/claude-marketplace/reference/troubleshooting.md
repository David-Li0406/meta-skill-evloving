# Troubleshooting Reference

Comprehensive guide to debugging marketplace issues, resolving errors, and systematic troubleshooting workflows.

## Validation Errors

### JSON Syntax Errors

**Symptom:** `claude plugin validate .` reports syntax error

**Common causes:**

**Missing comma:**
```json
❌ Error
{
  "name": "marketplace"
  "owner": {...}
}

✅ Fixed
{
  "name": "marketplace",
  "owner": {...}
}
```

**Trailing comma:**
```json
❌ Error
{
  "name": "marketplace",
  "owner": {...},
  "plugins": [],
}

✅ Fixed
{
  "name": "marketplace",
  "owner": {...},
  "plugins": []
}
```

**Unquoted keys:**
```json
❌ Error
{
  name: "marketplace"
}

✅ Fixed
{
  "name": "marketplace"
}
```

**Single quotes instead of double:**
```json
❌ Error
{
  'name': 'marketplace'
}

✅ Fixed
{
  "name": "marketplace"
}
```

**Resolution:**
1. Run `claude plugin validate .` to identify error line
2. Use JSON validator/linter in editor
3. Check for missing/extra commas, quotes, brackets

### Schema Validation Failures

**Symptom:** Valid JSON but validation fails

**Missing required field (name):**

```json
❌ Error: Missing required field "name"
{
  "owner": {
    "name": "Team"
  },
  "plugins": []
}

✅ Fixed
{
  "name": "marketplace-name",
  "owner": {
    "name": "Team"
  },
  "plugins": []
}
```

**Missing required field (owner):**

```json
❌ Error: Missing required field "owner"
{
  "name": "marketplace",
  "plugins": []
}

✅ Fixed
{
  "name": "marketplace",
  "owner": {
    "name": "Team"
  },
  "plugins": []
}
```

**Missing required field (plugins):**

```json
❌ Error: Missing required field "plugins"
{
  "name": "marketplace",
  "owner": {
    "name": "Team"
  }
}

✅ Fixed
{
  "name": "marketplace",
  "owner": {
    "name": "Team"
  },
  "plugins": []
}
```

**Plugin missing required field (name):**

```json
❌ Error: Plugin missing required field "name"
{
  "plugins": [
    {
      "source": "./plugin"
    }
  ]
}

✅ Fixed
{
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugin"
    }
  ]
}
```

**Plugin missing required field (source):**

```json
❌ Error: Plugin missing required field "source"
{
  "plugins": [
    {
      "name": "plugin-name"
    }
  ]
}

✅ Fixed
{
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugin"
    }
  ]
}
```

### Field Constraint Violations

**Invalid name format (spaces):**

```json
❌ Error: Name must be kebab-case
{
  "name": "My Marketplace"
}

✅ Fixed
{
  "name": "my-marketplace"
}
```

**Invalid name format (camelCase):**

```json
❌ Error: Name should use kebab-case
{
  "name": "myMarketplace"
}

✅ Fixed
{
  "name": "my-marketplace"
}
```

**Invalid source object (missing repo):**

```json
❌ Error: GitHub source missing "repo" field
{
  "plugins": [
    {
      "name": "plugin",
      "source": {
        "source": "github"
      }
    }
  ]
}

✅ Fixed
{
  "plugins": [
    {
      "name": "plugin",
      "source": {
        "source": "github",
        "repo": "owner/plugin-repo"
      }
    }
  ]
}
```

**Invalid source object (missing url):**

```json
❌ Error: URL source missing "url" field
{
  "plugins": [
    {
      "name": "plugin",
      "source": {
        "source": "url"
      }
    }
  ]
}

✅ Fixed
{
  "plugins": [
    {
      "name": "plugin",
      "source": {
        "source": "url",
        "url": "https://gitlab.com/team/plugin.git"
      }
    }
  ]
}
```

**Invalid path format (absolute path):**

```json
❌ Error: Paths must be relative
{
  "plugins": [
    {
      "name": "plugin",
      "source": "/absolute/path/to/plugin"
    }
  ]
}

✅ Fixed
{
  "plugins": [
    {
      "name": "plugin",
      "source": "./relative/path/to/plugin"
    }
  ]
}
```

**Resolution steps:**
1. Run `claude plugin validate .`
2. Read error message carefully for field name and expected format
3. Check schema reference for field requirements
4. Fix field value to match expected format
5. Re-validate until no errors

## Installation Issues

### Marketplace Not Loading

**Symptom:** Marketplace doesn't appear in `/plugin marketplace list`

**Cause 1: marketplace.json not at correct location**

```
❌ Wrong location
my-marketplace/
└── marketplace.json

✅ Correct location
my-marketplace/
└── .claude-plugin/
    └── marketplace.json
```

**Resolution:**
```bash
mkdir -p .claude-plugin
mv marketplace.json .claude-plugin/
```

**Cause 2: Invalid JSON syntax**

**Resolution:**
```bash
claude plugin validate .
# Fix syntax errors shown
```

**Cause 3: Repository not accessible**

For private repositories:

```bash
# Test GitHub access
git clone git@github.com:company/private-marketplace.git

# Test GitLab access
git clone git@gitlab.com:company/marketplace.git
```

**Resolution:**
- Verify SSH keys configured
- Confirm repository access permissions
- Check git credentials

**Cause 4: Wrong marketplace source URL**

```json
❌ Typo in repo name
{
  "source": {
    "source": "github",
    "repo": "company/markteplace"
  }
}

✅ Correct
{
  "source": {
    "source": "github",
    "repo": "company/marketplace"
  }
}
```

**Resolution:**
- Verify repository exists
- Check for typos in owner/repo name
- Confirm repository is not renamed/moved

### Plugin Installation Failures

**Symptom:** `/plugin install plugin-name@marketplace` fails

**Cause 1: Plugin source not accessible**

```bash
# Test plugin source directly
git clone git@github.com:company/plugin-repo.git

# Or for local sources
ls -la ./path/to/plugin
```

**Resolution:**
- Verify plugin source URL in marketplace.json
- Check repository access permissions
- Confirm path exists for local sources

**Cause 2: Plugin directory structure incorrect**

**Required structure (strict: true, default):**

```
plugin/
├── .claude-plugin/
│   └── plugin.json     # Required
└── ...
```

**Resolution:**
```bash
mkdir -p plugin/.claude-plugin
# Create plugin.json with at minimum:
{
  "name": "plugin-name"
}
```

**Cause 3: Plugin.json validation fails**

```bash
cd plugin-directory
claude plugin validate .
```

**Resolution:**
- Fix validation errors in plugin.json
- Ensure required fields present (name)
- Verify JSON syntax

**Cause 4: Component files missing**

```json
Marketplace entry specifies:
{
  "commands": "./commands/deploy.md"
}

But file doesn't exist at ./commands/deploy.md
```

**Resolution:**
- Verify all referenced files exist
- Check path spellings
- Ensure paths are relative to plugin root

**Cause 5: Conflicting plugin name**

**Symptom:** Plugin already installed with same name

```shell
/plugin list
# Shows plugin-name already installed
```

**Resolution:**
```shell
# Uninstall conflicting plugin
/plugin uninstall plugin-name

# Or use different plugin name in marketplace
```

### Source URL Accessibility

**Testing source URLs:**

**GitHub:**
```bash
# Test HTTPS access
git clone https://github.com/owner/repo.git

# Test SSH access
git clone git@github.com:owner/repo.git
```

**GitLab:**
```bash
git clone https://gitlab.com/owner/repo.git
git clone git@gitlab.com:owner/repo.git
```

**Private repositories:**

```bash
# Check SSH key authentication
ssh -T git@github.com
# Should show: "Hi username! You've successfully authenticated"

# Check token authentication (if using HTTPS)
git credential fill
# Enter host, username to verify stored credentials
```

**Resolution for access issues:**
1. Configure SSH keys for git hosting service
2. Add personal access tokens for HTTPS
3. Verify repository permissions granted to user
4. Check organization/team access settings

### Permission Errors

**Symptom:** "Permission denied" during installation

**Cause 1: SSH key not configured**

**Resolution:**
```bash
# Generate SSH key if needed
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub/GitLab
cat ~/.ssh/id_ed25519.pub
```

**Cause 2: Repository access not granted**

**Resolution:**
- Request repository access from owner
- Verify organization membership
- Check team permissions

**Cause 3: File system permissions**

```bash
# Check permissions on marketplace directory
ls -la .claude-plugin/

# Fix if needed
chmod 644 .claude-plugin/marketplace.json
```

### Authentication Problems

**GitHub authentication:**

**HTTPS with token:**
```bash
# Configure Git credential helper
git config --global credential.helper store

# Clone with token
git clone https://token@github.com/company/repo.git
```

**SSH key:**
```bash
# Test authentication
ssh -T git@github.com

# Should show: "Hi username!"
```

**GitLab authentication:**

**Deploy tokens:**
```bash
# Use deploy token in URL
git clone https://username:token@gitlab.com/company/repo.git
```

**SSH keys:**
```bash
ssh -T git@gitlab.com
```

**Corporate proxies:**

```bash
# Configure git to use proxy
git config --global http.proxy http://proxy.company.com:8080
git config --global https.proxy https://proxy.company.com:8080
```

## Runtime Issues

### Commands Not Appearing

**Symptom:** Plugin installed but commands missing from `/` menu

**Cause 1: Commands in wrong directory**

```
❌ Wrong
plugin/
└── .claude-plugin/
    └── commands/      # Wrong location
        └── cmd.md

✅ Correct
plugin/
├── .claude-plugin/
│   └── plugin.json
└── commands/          # Correct location (plugin root)
    └── cmd.md
```

**Resolution:**
```bash
mv .claude-plugin/commands ./commands
```

**Cause 2: Command file format incorrect**

**Required format:**
```markdown
---
description: Brief command description
---

# Command Implementation

Command content...
```

**Resolution:**
- Add YAML frontmatter with description
- Ensure proper markdown format

**Cause 3: Plugin not enabled**

```shell
/plugin list
# Check if plugin shows as enabled
```

**Resolution:**
```shell
/plugin enable plugin-name
```

### Components Not Loading

**Skills not loading:**

**Correct structure:**
```
plugin/
└── skills/
    ├── skill-name/
    │   └── SKILL.md    # Note: SKILL.md, not skill.md
    └── another-skill/
        └── SKILL.md
```

**Resolution:**
- Ensure SKILL.md filename is uppercase
- Verify skill directory structure
- Check YAML frontmatter in SKILL.md

**Agents not loading:**

**Correct structure:**
```
plugin/
└── agents/
    ├── agent-one.md
    └── agent-two.md
```

**Required frontmatter:**
```markdown
---
description: Agent description
capabilities: ["cap1", "cap2"]
---
```

**Resolution:**
- Add required frontmatter fields
- Ensure .md extension
- Verify markdown format

**Hooks not firing:**

**Cause: Script not executable**

```bash
# Check script permissions
ls -la scripts/hook.sh

# Make executable
chmod +x scripts/hook.sh
```

**Cause: Incorrect hook configuration**

```json
✅ Correct
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/hook.sh"
          }
        ]
      }
    ]
  }
}
```

**MCP servers not starting:**

**Check logs:**
```bash
claude --debug
# Look for MCP server initialization errors
```

**Common issues:**
- Missing ${CLAUDE_PLUGIN_ROOT} in paths
- Server binary not executable
- Missing dependencies
- Invalid server configuration

### Path Resolution Errors

**Symptom:** "File not found" errors for plugin components

**Cause: Absolute paths used**

```json
❌ Wrong
{
  "commands": "/absolute/path/cmd.md"
}

✅ Correct
{
  "commands": "./relative/path/cmd.md"
}
```

**Resolution:**
- Convert all paths to relative
- Ensure paths start with `./`

**Cause: Missing pluginRoot resolution**

```json
Marketplace has:
{
  "metadata": {
    "pluginRoot": "./packages"
  }
}

Plugin source:
{
  "source": "./plugin"
}

Resolves to: ./packages/plugin
```

**Verify:**
```bash
ls -la packages/plugin
```

### ${CLAUDE_PLUGIN_ROOT} Issues

**Symptom:** Hooks or MCP servers fail with path errors

**Cause: Missing environment variable usage**

```json
❌ Wrong
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "./scripts/hook.sh"
      }]
    }]
  }
}

✅ Correct
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/hook.sh"
      }]
    }]
  }
}
```

**Resolution:**
- Use ${CLAUDE_PLUGIN_ROOT} for all runtime paths
- Applies to hooks, MCP servers, script references
- Ensures paths work regardless of installation location

### Conflict Resolution

**Symptom:** Multiple plugins provide same command/component

**Namespace collision:**

```
Plugin A: /deploy command
Plugin B: /deploy command
```

**Resolution options:**

1. **Disable one plugin:**
   ```shell
   /plugin disable plugin-b
   ```

2. **Use namespaced commands:**
   Plugin authors should namespace commands:
   ```
   Plugin A: /deploy-app command
   Plugin B: /deploy-infra command
   ```

3. **Configure plugin priority:**
   Last enabled plugin takes precedence

## Debugging Workflow

### Step 1: Identify Error Type

**Run validation:**
```bash
claude plugin validate .
```

**Categories:**
- JSON syntax error → Fix syntax
- Schema validation error → Fix field values
- File not found → Check paths
- Permission denied → Fix access
- Runtime error → Check logs

### Step 2: Use Debug Mode

**Start Claude Code with debug output:**
```bash
claude --debug
```

**Debug output shows:**
- Plugin loading sequence
- Marketplace installation
- Component registration
- Error stack traces
- MCP server initialization

### Step 3: Check Installation Status

```shell
# List marketplaces
/plugin marketplace list

# List plugins
/plugin list

# Check specific plugin status
/plugin info plugin-name
```

### Step 4: Verify File Structure

```bash
# Check marketplace structure
ls -la .claude-plugin/marketplace.json

# Check plugin structure
ls -la plugin-directory/.claude-plugin/plugin.json
ls -la plugin-directory/commands/
ls -la plugin-directory/agents/
ls -la plugin-directory/skills/
```

### Step 5: Test Components Individually

**Test command file:**
```bash
# Verify markdown format
cat commands/command.md

# Check frontmatter
head -n 10 commands/command.md
```

**Test hook script:**
```bash
# Check executable
ls -la scripts/hook.sh

# Test script manually
./scripts/hook.sh
```

**Test MCP server:**
```bash
# Run server directly
./servers/server --help
```

### Step 6: Review Logs

**Claude Code logs location:**
```bash
# macOS
~/Library/Logs/claude/

# Linux
~/.local/share/claude/logs/

# Windows
%APPDATA%\claude\logs\
```

**Look for:**
- Plugin load errors
- Component registration failures
- Runtime exceptions
- MCP server crashes

### Systematic Troubleshooting Checklist

**Marketplace issues:**
- [ ] marketplace.json at correct location (.claude-plugin/)
- [ ] JSON syntax valid (claude plugin validate .)
- [ ] Required fields present (name, owner, plugins)
- [ ] Marketplace source URL accessible
- [ ] Repository permissions granted

**Plugin issues:**
- [ ] Plugin source accessible
- [ ] Plugin directory structure correct
- [ ] plugin.json exists (if strict: true)
- [ ] plugin.json syntax valid
- [ ] All referenced files exist

**Component issues:**
- [ ] Components at correct locations (commands/, agents/, skills/)
- [ ] File formats correct (YAML frontmatter, markdown)
- [ ] Scripts executable (chmod +x)
- [ ] Paths relative and use ${CLAUDE_PLUGIN_ROOT}

**Installation issues:**
- [ ] Marketplace added successfully
- [ ] Plugin installed without errors
- [ ] Plugin enabled in /plugin list
- [ ] Commands appear in / menu
- [ ] Hooks fire on expected events
- [ ] MCP servers start without errors

### Common Error Solutions Summary

| Error | Quick Fix |
| :---- | :-------- |
| JSON syntax error | Run `claude plugin validate .` and fix shown errors |
| Marketplace not loading | Check `.claude-plugin/marketplace.json` location |
| Plugin not installing | Verify source URL accessibility with `git clone` |
| Commands not appearing | Move commands to plugin root, not .claude-plugin/ |
| Hook not firing | Make script executable: `chmod +x script.sh` |
| MCP server fails | Use ${CLAUDE_PLUGIN_ROOT} in server paths |
| Permission denied | Configure SSH keys for git hosting service |
| File not found | Convert absolute paths to relative with `./` |

## See Also

- [SKILL.md](../SKILL.md) - Main marketplace management guide
- [marketplace-schema.md](marketplace-schema.md) - Complete schema reference
- [plugin-management.md](plugin-management.md) - Plugin configuration details
- [team-distribution.md](team-distribution.md) - Team distribution setup
