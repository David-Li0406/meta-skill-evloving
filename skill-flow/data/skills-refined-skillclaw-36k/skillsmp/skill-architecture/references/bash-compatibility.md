# Bash Compatibility for Skills

This reference documents the mandatory bash compatibility patterns for skill files.

**ADR**: [Skill Bash Compatibility Enforcement](/docs/adr/2025-12-22-skill-bash-compatibility-enforcement.md)

## Problem

Claude Code's Bash tool on macOS runs through zsh by default. Bash-specific syntax fails:

| Pattern                              | Error in Zsh             |
| ------------------------------------ | ------------------------ |
| `declare -A`                         | bad substitution         |
| `VAR=$(cmd) other-cmd`               | parse error near '('     |
| `[[ $x =~ regex ]]` + `BASH_REMATCH` | undefined variable       |
| `\!=` (escaped)                      | condition expected       |
| `grep -oP`                           | invalid option (no PCRE) |

## Mandatory Pattern

All bash code blocks in skill files MUST use heredoc wrapper:

```bash
/usr/bin/env bash << 'SCRIPT_NAME_EOF'
# Your bash script here
# All bash-specific syntax works inside heredoc:

declare -A MAP
MAP["key"]="value"

if [[ "$var" =~ pattern ]]; then
  echo "${BASH_REMATCH[1]}"
fi

RESULT=$(some_command)
echo "$RESULT"
SCRIPT_NAME_EOF
```

### Why This Works

1. `/usr/bin/env bash` - Invokes bash explicitly (portable across macOS, Linux, BSD)
2. `<< 'NAME_EOF'` - Heredoc with quoted delimiter prevents variable expansion in the outer shell
3. All bash syntax inside the heredoc is interpreted by bash, not zsh

## Prohibited Patterns

| Pattern            | Why                        | Fix                          |
| ------------------ | -------------------------- | ---------------------------- |
| `declare -A NAME`  | Bash 4+ only, fails in zsh | Use parallel indexed arrays  |
| `grep -oP`         | Perl regex not portable    | Use `grep -oE` + awk         |
| `$'\n'`            | ANSI-C quoting             | Use literal newlines         |
| `\!=` in `[[ ]]`   | Unnecessary escape         | Use `!=` directly            |
| Unwrapped `$(...)` | Fails in inline assignment | Wrap entire block in heredoc |

### Parallel Indexed Arrays (Replacing `declare -A`)

```bash
/usr/bin/env bash << 'BASH_COMPATIBILITY_SCRIPT_EOF'
# ❌ WRONG: Associative array (bash 4+ only)
declare -A ACCOUNTS
ACCOUNTS["alice"]="ssh-key"
ACCOUNTS["bob"]="gh-cli"

# ✅ CORRECT: Parallel indexed arrays
ACCOUNT_NAMES=()
ACCOUNT_SOURCES=()

add_account() {
  local name="$1" source="$2"
  for idx in "${!ACCOUNT_NAMES[@]}"; do
    if [[ "${ACCOUNT_NAMES[$idx]}" == "$name" ]]; then
      ACCOUNT_SOURCES[$idx]+="$source "
      return
    fi
  done
  ACCOUNT_NAMES+=("$name")
  ACCOUNT_SOURCES+=("$source ")
}

add_account "alice" "ssh-key"
add_account "bob" "gh-cli"
BASH_COMPATIBILITY_SCRIPT_EOF
```

### Portable Regex (Replacing `grep -P`)

```bash
/usr/bin/env bash << 'MISE_EOF'
# ❌ WRONG: Perl regex (not available on all systems)
account=$(grep -oP '(?<=GH_ACCOUNT=")[^"]+' .mise.toml)

# ✅ CORRECT: Extended regex + awk
account=$(grep -E 'GH_ACCOUNT\s*=' .mise.toml | sed 's/.*=\s*"\([^"]*\)".*/\1/')
MISE_EOF
```

## Heredoc Naming Convention

Use descriptive EOF markers matching the script purpose:

| Script Purpose    | EOF Marker            |
| ----------------- | --------------------- |
| Preflight checks  | `PREFLIGHT_EOF`       |
| Account detection | `DETECT_ACCOUNTS_EOF` |
| Setup scripts     | `SETUP_ORPHAN_EOF`    |
| Validation        | `VALIDATE_EOF`        |
| Configuration     | `CONFIG_EOF`          |

## Examples

### Skill SKILL.md

```markdown
## Preflight Check

\`\`\`bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
MISSING=()

for tool in git gh jq; do
command -v "$tool" &>/dev/null || MISSING+=("$tool")
done

if [[${#MISSING[@]} -gt 0]]; then
echo "Missing: ${MISSING[*]}"
exit 1
fi

echo "All tools installed"
PREFLIGHT_EOF
\`\`\`
```

### Command File (commands/\*.md)

```markdown
## Execute

\`\`\`bash
/usr/bin/env bash << 'COMMAND_EOF'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

if [[-f "$PROJECT_DIR/.claude/config.json"]]; then
cat "$PROJECT_DIR/.claude/config.json" | python3 -m json.tool
else
echo "Config not found"
fi
COMMAND_EOF
\`\`\`
```

## Validation

Run the validation script to check for bash compatibility issues:

```bash
# Marketplace plugins (strict)
bun run plugins/plugin-dev/scripts/validate-skill.ts plugins/your-plugin/skills/your-skill/

# Project-local skills with documentation-only bash blocks
bun run plugins/plugin-dev/scripts/validate-skill.ts .claude/skills/your-skill/ --skip-bash
```

The validator checks for:

- Bash blocks without heredoc wrapper (ERROR if contains `$()`, `[[`, etc.)
- `declare -A` usage (ERROR)
- `grep -P` usage (WARNING)

**Note**: Use `--skip-bash` for project-local skills where bash blocks are user-facing documentation examples (not executed by Claude). This is common for workflow/tutorial skills.

To auto-fix bash blocks by adding heredoc wrappers:

```bash
bun run plugins/plugin-dev/scripts/fix-bash-blocks.ts plugins/your-plugin/ --dry  # Preview
bun run plugins/plugin-dev/scripts/fix-bash-blocks.ts plugins/your-plugin/        # Apply
```

## Reference

- [Shell Command Portability ADR](/docs/adr/2025-12-06-shell-command-portability-zsh.md)
- [Plugin Authoring Guide](/docs/plugin-authoring.md)
