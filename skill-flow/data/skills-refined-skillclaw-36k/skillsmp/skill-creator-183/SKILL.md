---
name: skill-creator
description: "AI-assisted skill creation for OpenCode. Use when creating a new skill, designing skill structure, or scaffolding skill files. Handles search-before-create, adaptive interview, and generation."
allowed-tools: Read Write Edit Glob Grep Bash Task WebFetch
context: fork
---

# Skill Creator

Create well-structured OpenCode skills through guided design or quick scaffolding.

**Announce at start:** "I'm using the skill-creator skill to help design your new skill."

## Workflow

### Phase 1: Search Before Create

Before creating any skill, search for similar existing skills:

1. **Search local skills:**
   ```bash
   ls skills/
   ```
   Review names and read SKILL.md files that might overlap

2. **Ask about external search:**
   "Should I check external skill repositories (Gentleman-Skills, awesome-claude-skills) for similar skills?"

3. **If similar found, offer options:**
   - Adapt existing skill to your needs
   - Extend existing skill with new capabilities
   - Create new skill (explain why it's different)

4. **If no similar found:** Proceed to Phase 2

### Phase 2: Adaptive Interview

Adjust depth based on skill complexity:

**Always ask:**
1. What's the primary purpose? (1 sentence)
2. What tools will it need? (Bash, Read, WebFetch, Task, etc.)

**Ask if unclear:**
3. Will it have executable scripts or just instructions?
4. Does it need configuration files (YAML/JSON)?
5. Does it need template assets?

**Determine structure from answers:**

| Complexity | Structure | When |
|------------|-----------|------|
| Simple | Just SKILL.md | Instructions only, no automation |
| With scripts | SKILL.md + `scripts/` | Executable bash scripts |
| With config | SKILL.md + `config/` | Domain-specific data in YAML |
| With assets | SKILL.md + `assets/` | Templates, examples, reference files |
| With tests | Above + `tests/` | Scripts that need validation |

### Phase 3: Generate Skill

1. **Validate name:**
   - Pattern: `^[a-z][a-z0-9-]*[a-z0-9]$`
   - Minimum 3 characters
   - Directory must not exist

2. **Create structure:**
   ```bash
   mkdir -p skills/<name>
   mkdir -p skills/<name>/scripts  # if needed
   mkdir -p skills/<name>/config   # if needed
   mkdir -p skills/<name>/assets   # if needed
   mkdir -p skills/<name>/tests    # if needed
   ```

3. **Generate SKILL.md** with:
   - Proper frontmatter (name, description, allowed-tools, context)
   - Purpose and usage sections
   - Quick reference table (if has actions)
   - Script documentation (if has scripts)

4. **Generate stub scripts** (if applicable):
   - Main script with action pattern
   - Proper shebang and error handling

5. **Generate smoke test** (if has scripts):
   - `tests/smoke.sh` that validates basic functionality

### Phase 4: Validation Checklist

Before finishing, verify:

- [ ] Name matches directory name
- [ ] Description explains WHEN to use (trigger conditions)
- [ ] `allowed-tools` is minimal and scoped
- [ ] Scripts have `#!/usr/bin/env bash` and `set -euo pipefail`
- [ ] Smoke test exists if scripts exist
- [ ] No duplicate of existing skill

## Quick Mode

When invoked with `--quick` flag:

1. Skip Phase 1 (search)
2. Skip Phase 2 (interview)
3. Create directory + SKILL.md from template
4. Inform user what to customize

```bash
mkdir -p skills/<name>
# Copy template from assets/SKILL-TEMPLATE.md
# Replace name placeholder
# Write to skills/<name>/SKILL.md
```

## Frontmatter Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Matches directory, lowercase-kebab-case |
| `description` | Yes | Include "Use when..." trigger conditions |
| `allowed-tools` | Yes | Whitelist, scope bash commands (e.g., `Bash(gh:*)`) |
| `context` | Recommended | Use `fork` for isolated execution |

### allowed-tools Patterns

| Pattern | Meaning |
|---------|---------|
| `Bash` | Any bash command (broad) |
| `Bash(gh:*)` | Only `gh` commands |
| `Bash(./scripts/*)` | Only scripts in skill's scripts/ dir |
| `Read Glob Grep` | File reading tools |
| `Task` | Can spawn subagents |
| `WebFetch` | Can fetch URLs |

## Script Conventions

All bash scripts must include:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Script implementation
```

Action pattern for multi-command scripts:

```bash
ACTION="${1:-help}"
case "$ACTION" in
    action1) do_action1 "$@" ;;
    action2) do_action2 "$@" ;;
    help|*) show_help ;;
esac
```

## Smoke Test Template

For skills with scripts, generate `tests/smoke.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Smoke Test: <skill-name> ==="

# Test 1: Help command works
echo "Testing help command..."
bash "$SCRIPT_DIR/scripts/main.sh" help > /dev/null
echo "✓ Help command works"

# Test 2: Basic functionality
echo "Testing basic functionality..."
# Add skill-specific tests here
echo "✓ Basic tests pass"

echo "=== All smoke tests passed ==="
```

## Progressive Disclosure

Keep skills efficient:

- **Description** (~100 tokens): Loaded at startup, include trigger keywords
- **SKILL.md** (<5,000 tokens): Core instructions, loaded on activation
- **Subdirectories**: Heavy content, loaded on-demand

## Reference Examples

For well-structured skills in this repo, see:
- `@skills/github-ops/SKILL.md` - Multi-script skill with domains
- `@skills/asu-discover/SKILL.md` - Script with YAML config
