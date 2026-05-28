---
name: ai-rules-cli
description: >-
  Use ai-rules CLI to manage and synchronize AI coding rules across multiple AI
  assistants (Cursor, Claude Code, GitHub Copilot, Opencode, etc.). Use when:
  (1) Setting up ai-rules in a new project, (2) Updating AI coding guidelines
  and best practices, (3) Generating platform-specific rule files from source,
  (4) Checking if generated files are in sync with source files, (5) Managing
  multi-agent rule consistency, or (6) Adding new rules or modifying existing
  ones. Requires ai-rules CLI installed. The ai-rules/ directory serves as the
  single source of truth for all AI coding guidelines.
---

# AI Rules CLI

Use ai-rules CLI to manage and synchronize AI coding rules across multiple AI assistants, maintaining a single source of truth for coding guidelines that works with Cursor, Claude Code, GitHub Copilot, Opencode, Gemini, and other AI coding agents.

## Prerequisites

- ai-rules CLI installed: `curl -fsSL https://raw.githubusercontent.com/block/ai-rules/main/scripts/install.sh | bash`
- Git repository: ai-rules works best in a git repository context
- Repository root access: Run commands from the repository root where `ai-rules/` directory should exist

## Quick Start

**Check if ai-rules is installed:**
```bash
ai-rules --version
```

**Initialize ai-rules in a project:**
```bash
ai-rules init
```

**Generate platform-specific files:**
```bash
ai-rules generate
```

**Check sync status:**
```bash
ai-rules status
```

## Core Workflow

### 1. Setup (First Time)

**Install ai-rules CLI:**
```bash
curl -fsSL https://raw.githubusercontent.com/block/ai-rules/main/scripts/install.sh | bash
```

**Initialize in project:**
```bash
ai-rules init
```

This creates:
- `ai-rules/` directory
- `ai-rules-config.yaml` configuration file
- Initial example rule file

**Configure agents:**
Edit `ai-rules/ai-rules-config.yaml`:
```yaml
agents: [claude, cursor, copilot, codex, opencode, gemini]
nested_depth: 0
gitignore: false
```

**Generate initial files:**
```bash
ai-rules generate
```

### 2. Updating Rules

**Edit source files** in `ai-rules/` directory:
- Add new rule files: `ai-rules/my-new-rule.md`
- Edit existing rules: `ai-rules/react-router-7.md`
- Update project context: `ai-rules/00-project-context.md`

**Generate platform-specific files:**
```bash
ai-rules generate
```

This automatically creates/updates:
- `CLAUDE.md` - Rules for Claude Code
- `AGENTS.md` - Rules for Opencode and other agents
- `.cursor/rules/*.mdc` - Rules for Cursor
- `.github/copilot-instructions.md` - Symlink for GitHub Copilot
- Other agent-specific files as configured

### 3. Checking Sync Status

**Check all agents:**
```bash
ai-rules status
```

**Check specific agents:**
```bash
ai-rules status --agents claude,cursor
```

**Output interpretation:**
- ✅ `in sync` - Generated files match source files
- ⚠️ `out of sync` - Source files modified, need regeneration

**Use in CI/CD:**
```bash
ai-rules status || exit 1  # Fails if out of sync
```

## Usage Patterns

### Adding a New Rule

1. Create new rule file in `ai-rules/`:
   ```bash
   touch ai-rules/my-new-rule.md
   ```

2. Add rule content with optional frontmatter:
   ```markdown
   ---
   description: Context description for when to apply this rule
   alwaysApply: true
   fileMatching: "**/*.ts"
   ---
   
   # My New Rule
   
   Rule content here...
   ```

3. Generate platform files:
   ```bash
   ai-rules generate
   ```

4. Verify sync:
   ```bash
   ai-rules status
   ```

### Updating Existing Rules

1. Edit source file in `ai-rules/`:
   ```bash
   # Edit ai-rules/react-router-7.md
   ```

2. Regenerate platform files:
   ```bash
   ai-rules generate
   ```

3. Commit both source and generated files:
   ```bash
   git add ai-rules/ CLAUDE.md AGENTS.md .cursor/rules/
   git commit -m "docs: update React Router v7 rules"
   ```

### Initializing in New Project

1. Install CLI (if not already installed)
2. Run `ai-rules init` in repository root
3. Configure `ai-rules-config.yaml` for desired agents
4. Create initial project context rule
5. Run `ai-rules generate` to create platform files
6. Commit both source and generated files

### Maintaining Rule Consistency

**Regular workflow:**
1. Edit source files in `ai-rules/`
2. Run `ai-rules generate` to sync
3. Run `ai-rules status` to verify
4. Commit changes

**Before major changes:**
1. Check current status: `ai-rules status`
2. Make changes to source files
3. Generate: `ai-rules generate`
4. Verify: `ai-rules status`
5. Test that rules work in target agents
6. Commit

## Command Reference

### Initialization

```bash
# Initialize ai-rules in current directory
ai-rules init

# Initialize with custom parameters (for custom recipes)
ai-rules init --params service=payments --params owner=checkout

# Force initialization without prompts
ai-rules init --force
```

### Generation

```bash
# Generate rules for all configured agents
ai-rules generate

# Generate for specific agents only
ai-rules generate --agents claude,cursor

# Generate with nested directory scanning
ai-rules generate --nested-depth 2

# Add generated files to .gitignore
ai-rules generate --gitignore
```

### Status Checking

```bash
# Check sync status for all agents
ai-rules status

# Check specific agents
ai-rules status --agents claude,cursor

# Check with nested scanning
ai-rules status --nested-depth 1
```

### Cleanup

```bash
# Remove all generated files (keeps source files)
ai-rules clean

# Clean with nested scanning
ai-rules clean --nested-depth 2
```

### Utilities

```bash
# List all supported agents
ai-rules list-agents
```

## Configuration

### Configuration File: `ai-rules/ai-rules-config.yaml`

```yaml
# List of agents to generate rules for
agents: [claude, cursor, copilot, codex, opencode, gemini]

# Agents to generate commands for (defaults to agents list)
command_agents: [claude, cursor]

# Maximum nested directory depth to scan for ai-rules/ folders
nested_depth: 0

# Whether to add generated files to .gitignore
gitignore: false
```

### Configuration Precedence

1. CLI options (highest priority)
2. Config file (`ai-rules-config.yaml`)
3. Default values (lowest priority)

### Experimental Options

**Claude Code Skills Mode:**
```yaml
use_claude_skills: true  # Default: false
```

When enabled, rules with `alwaysApply: false` are generated as separate skills in `.claude/skills/` instead of being included in `CLAUDE.md`.

## Rule File Format

### Standard Mode (with frontmatter)

```markdown
---
description: Context description for when to apply this rule
alwaysApply: true
fileMatching: "**/*.ts"
---

# Rule Title

Rule content here...
```

**Frontmatter fields:**
- `description` - Context description (optional)
- `alwaysApply` - `true` (always included) or `false` (optional/contextual) (default: `true`)
- `fileMatching` - Glob patterns for file matching (Cursor-specific)

### Symlink Mode (simple markdown)

For simple setups, use a single `AGENTS.md` file without frontmatter:
- Must be named `AGENTS.md`
- Must be the only file in `ai-rules/`
- No YAML frontmatter
- Content used directly by all agents via symlinks

## Best Practices

### Source of Truth

- **Always edit source files** in `ai-rules/` directory
- **Never edit generated files** directly (they're overwritten on generation)
- **Commit both** source and generated files for team consistency

### Workflow

1. Edit source files in `ai-rules/`
2. Run `ai-rules generate` to sync
3. Verify with `ai-rules status`
4. Test rules in target agents
5. Commit both source and generated files

### Organization

- Use descriptive filenames: `react-router-7.md`, `testing-best-practices.md`
- Prefix foundational rules: `00-project-context.md`
- Group related rules logically
- Keep rules focused and modular

### Maintenance

- Run `ai-rules status` regularly to catch sync issues
- Use `ai-rules generate` after any source file changes
- Include `ai-rules status` in CI/CD to ensure sync
- Document rule changes in commit messages

## Integration with Development Workflow

### Pre-Commit Hook

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
ai-rules status || (echo "AI rules out of sync. Run 'ai-rules generate'" && exit 1)
```

### CI/CD Pipeline

```yaml
# .github/workflows/ai-rules.yml
- name: Check AI Rules Sync
  run: ai-rules status || exit 1

- name: Generate AI Rules
  run: ai-rules generate
```

### Team Collaboration

1. Team members edit source files in `ai-rules/`
2. Run `ai-rules generate` locally
3. Commit both source and generated files
4. CI/CD verifies sync status
5. All team members have consistent rules across agents

## Common Issues

### Generated Files Out of Sync

**Symptom:** `ai-rules status` shows "out of sync"

**Solution:**
```bash
ai-rules generate
```

### Missing CLI

**Symptom:** `command not found: ai-rules`

**Solution:**
```bash
curl -fsSL https://raw.githubusercontent.com/block/ai-rules/main/scripts/install.sh | bash
```

### Configuration Not Applied

**Symptom:** Changes in `ai-rules-config.yaml` not taking effect

**Solution:**
- Check file location (must be in `ai-rules/` directory)
- Verify YAML syntax
- CLI options override config file

## Reference Documentation

- **AI Rules CLI Docs**: [github.com/block/ai-rules](https://github.com/block/ai-rules)
- **Command Reference**: See [references/cli-commands.md](references/cli-commands.md) for complete command reference
- **Rule Format**: See [references/rule-format.md](references/rule-format.md) for detailed rule file format
