# AI Rules CLI Command Reference

Complete reference for ai-rules CLI commands used in AI agent workflows.

## Installation

```bash
# Quick install (recommended)
curl -fsSL https://raw.githubusercontent.com/block/ai-rules/main/scripts/install.sh | bash

# Install specific version
curl -fsSL https://raw.githubusercontent.com/block/ai-rules/main/scripts/install.sh | VERSION=v1.0.0 bash

# Custom install directory
curl -fsSL https://raw.githubusercontent.com/block/ai-rules/main/scripts/install.sh | INSTALL_DIR=/usr/local/bin bash
```

## Initialization

### Basic Initialization

```bash
# Initialize ai-rules in current directory
ai-rules init
```

Creates:
- `ai-rules/` directory
- `ai-rules-config.yaml` configuration file
- Initial example rule file

### Advanced Initialization

```bash
# Pass parameters to custom recipes
ai-rules init --params service=payments --params owner=checkout

# Force initialization without confirmation prompts
ai-rules init --force
```

## Generation

### Basic Generation

```bash
# Generate rules for all configured agents
ai-rules generate
```

Generates platform-specific files:
- `CLAUDE.md` - Claude Code rules
- `AGENTS.md` - Opencode and other agents
- `.cursor/rules/*.mdc` - Cursor rules
- `.github/copilot-instructions.md` - GitHub Copilot symlink
- Other agent-specific files

### Selective Generation

```bash
# Generate for specific agents only
ai-rules generate --agents claude,cursor

# Generate with nested directory scanning
ai-rules generate --nested-depth 2

# Add generated files to .gitignore
ai-rules generate --gitignore
```

### Generation Options

- `--agents` - Comma-separated list of specific agents
- `--nested-depth` - Maximum directory depth to scan (default: 0)
- `--gitignore` - Add generated file patterns to .gitignore

## Status Checking

### Basic Status

```bash
# Check sync status for all configured agents
ai-rules status
```

Output:
- ✅ `in sync` - Generated files match source files
- ⚠️ `out of sync` - Source files modified, need regeneration

### Selective Status

```bash
# Check specific agents
ai-rules status --agents claude,cursor

# Check with nested scanning
ai-rules status --nested-depth 1
```

### Exit Codes

- `0` - All agents in sync
- `1` - One or more agents out of sync
- `2` - No rules found

Use in scripts:
```bash
ai-rules status || exit 1
```

## Cleanup

```bash
# Remove all generated files (keeps source files)
ai-rules clean

# Clean with nested scanning
ai-rules clean --nested-depth 2
```

## Utilities

```bash
# List all supported agents
ai-rules list-agents
```

Output:
```
Supported agents:
  • amp
  • claude
  • cline
  • codex
  • copilot
  • cursor
  • firebender
  • gemini
  • goose
  • kilocode
  • opencode
  • roo
```

## Configuration

### Configuration File Location

`ai-rules/ai-rules-config.yaml`

### Configuration Options

```yaml
# List of agents to generate rules for
agents: [claude, cursor, copilot, codex, opencode, gemini]

# Agents to generate commands for (defaults to agents list)
command_agents: [claude, cursor]

# Maximum nested directory depth to scan
nested_depth: 0

# Whether to add generated files to .gitignore
gitignore: false

# Experimental: Claude Code Skills Mode
use_claude_skills: false
```

### Configuration Precedence

1. CLI options (highest priority)
2. Config file
3. Default values (lowest priority)

## Common Workflows

### Initial Setup

```bash
# 1. Install CLI
curl -fsSL https://raw.githubusercontent.com/block/ai-rules/main/scripts/install.sh | bash

# 2. Initialize
ai-rules init

# 3. Configure (edit ai-rules-config.yaml)
# 4. Generate
ai-rules generate

# 5. Verify
ai-rules status
```

### Updating Rules

```bash
# 1. Edit source files in ai-rules/
# 2. Generate platform files
ai-rules generate

# 3. Verify sync
ai-rules status

# 4. Commit
git add ai-rules/ CLAUDE.md AGENTS.md .cursor/rules/
git commit -m "docs: update AI rules"
```

### Pre-Commit Check

```bash
# In .git/hooks/pre-commit
#!/bin/bash
ai-rules status || (echo "AI rules out of sync. Run 'ai-rules generate'" && exit 1)
```

### CI/CD Integration

```yaml
# .github/workflows/ai-rules.yml
- name: Check AI Rules Sync
  run: ai-rules status || exit 1

- name: Generate AI Rules
  run: ai-rules generate
```

## Error Handling

### Common Issues

**Not installed:**
```bash
curl -fsSL https://raw.githubusercontent.com/block/ai-rules/main/scripts/install.sh | bash
```

**Not in repository root:**
```bash
# Ensure you're in the repository root
cd /path/to/repo
ai-rules generate
```

**Config file not found:**
```bash
# Initialize first
ai-rules init
```

**Out of sync:**
```bash
# Regenerate
ai-rules generate
```

## See Also

- [AI Rules GitHub Repository](https://github.com/block/ai-rules)
- [AI Rules Documentation](https://github.com/block/ai-rules#readme)
- [Rule File Format](rule-format.md)
