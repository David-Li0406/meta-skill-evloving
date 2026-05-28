---
name: allow-rules
description: Manages cc-allow.toml configuration files for bash command permission control. Use when the user wants to add, modify, or remove allow/deny rules, redirect rules, or pipe rules for Claude Code bash commands.
context: fork
---

# Managing cc-allow Rules

cc-allow evaluates bash commands and returns exit codes: 0=allow, 1=ask (defer), 2=deny, 3=error.

## Config Locations

1. `~/.config/cc-allow.toml` — Global defaults
2. `<project>/.claude/cc-allow.toml` — Project-specific (searches up from cwd)

**Merge behavior**: All configs are evaluated and combined. deny > allow > ask. Within a config, most specific matching rule wins.

## Config Structure

### Policy

```toml
[policy]
default = "ask"               # "allow", "deny", or "ask"
dynamic_commands = "ask"      # action for $VAR or $(cmd) as command name
default_message = "Command not allowed"
# allowed_paths = ["/usr/bin", "/bin"]  # optional: restrict command search paths
unresolved_commands = "ask"   # "ask" or "deny" for commands not found
```

**Command Path Resolution**: Commands are resolved to absolute paths. Shell builtins bypass resolution. Use `allowed_paths` to restrict where commands can be found.

### Quick Allow/Deny Lists

```toml
[commands.allow]
names = ["ls", "cat", "git", "go"]
# Can also use path: prefix for path-based matching:
# names = ["git", "path:$PROJECT_ROOT/bin/*", "path:/usr/bin/ls"]

[commands.deny]
names = ["sudo", "rm", "dd"]
message = "Dangerous command blocked"
```

### Constructs

```toml
[constructs]
function_definitions = "deny"  # foo() { ... }
background = "deny"            # command &
subshells = "ask"              # (command)
heredocs = "allow"             # <<EOF ... EOF (default: allow)
```

### Rules (Fine-grained Control)

When multiple rules match, the **most specific rule wins** based on specificity scoring. Rule order doesn't matter. Across configs, results are combined.

**Specificity points**: Named command (+100), each position arg (+20), each contains (+10), each pattern (+5), each pipe target (+10), pipe from wildcard (+5). Tie-break: deny > ask > allow.

The `command` field can be a name, `"*"` for any, or `"path:..."` for resolved path matching:

```toml
[[rule]]
command = "git"
action = "deny"
message = "Force push not allowed"
[rule.args]
any_match = ["--force", "-f"]
contains = ["push"]

[[rule]]
command = "curl"
action = "deny"
message = "No piping curl to shell"
[rule.pipe]
to = ["bash", "sh"]

# Match by resolved path
[[rule]]
command = "path:$PROJECT_ROOT/scripts/*"
action = "allow"
```

#### Argument Matching

```toml
[rule.args]
contains = ["--force"]           # must contain all (exact match)
any_match = ["-r", "-rf"]        # must match at least one
all_match = ["glob:*.txt"]       # all args must match
position = { 0 = "/etc/*" }      # arg at position must match
```

#### Pipe Context

```toml
[rule.pipe]
to = ["bash", "sh"]              # pipes directly to one of these
from = ["curl", "wget"]          # receives from any upstream (use for dangerous sinks)
```

Use `from = ["*"]` to match any piped input.

### Redirects

```toml
[[redirect]]
action = "allow"
[redirect.to]
exact = ["/dev/null"]

[[redirect]]
action = "deny"
message = "Cannot write to system paths"
append = true                    # only match >> (omit for both > and >>)
[redirect.to]
pattern = ["re:^/etc/.*", "re:^/usr/.*"]
exact = [".bashrc", ".zshrc"]
```

### Heredocs

Heredocs are separate from redirects (default: `constructs.heredocs = "allow"`).

```toml
# Deny all heredocs
[constructs]
heredocs = "deny"

# Or use fine-grained rules (only checked if constructs.heredocs = "allow")
[[heredoc]]
action = "deny"
message = "Dangerous content"
content_match = ["re:DROP TABLE", "re:DELETE FROM"]
```

## Pattern Matching

| Prefix | Description | Example |
|--------|-------------|---------|
| `glob:` | Shell glob (supports `**`) | `glob:*.txt`, `src/**/*.go` |
| `re:` | Regular expression | `re:^/etc/.*` |
| `path:` | Path pattern with variable expansion | `path:$PROJECT_ROOT/**` |
| `flags:` | Flag pattern (chars must appear) | `flags:rf`, `flags[--]:rec` |
| (none) | Exact match (or glob if contains `*?[`) | `--verbose` |

### Negation

Prepend "!" to patterns with explicit prefixes (`path:`, `re:`, `glob:`, `flags:`) to negate the match:

```toml
# Allow rm only for paths NOT under /etc
[[rule]]
command = "rm"
action = "allow"
[rule.args]
any_match = ["!path:/etc/**"]

# Match files that are NOT .txt
any_match = ["!glob:*.txt"]

# Match args that do NOT start with "--"
any_match = ["!re:^--"]
```

Note: Negation requires an explicit prefix. `!foo` matches the literal string "!foo".

### Path Patterns

Path patterns resolve arguments to absolute paths and expand variables:

| Variable | Description |
|----------|-------------|
| `$PROJECT_ROOT` | Directory containing `.claude/` or `.git/` |
| `$HOME` | User's home directory |

```toml
# Allow rm only under project root
[[rule]]
command = "rm"
action = "allow"
[rule.args]
any_match = ["path:$PROJECT_ROOT/**"]

# Block rm outside project
[[rule]]
command = "rm"
action = "deny"
message = "Cannot delete files outside project"
```

Path matching:
- Expands `~` to `$HOME`
- Resolves relative paths against cwd
- Follows symlinks (security)
- Uses gitignore-style `**` for recursive matching
- Only matches path-like arguments (starts with `/`, `./`, `../`, `~`, or contains `/`)

## Common Tasks

**Allow a command**: Add to `[commands.allow].names`

**Block a command**: Add to `[commands.deny].names`

**Block with specific args**: Add `[[rule]]` with `[rule.args]`

**Restrict to project directory**: Use `path:$PROJECT_ROOT/**` in `[rule.args].any_match`

**Allow redirect target**: Add `[[redirect]]` with `action = "allow"` (redirect rules still use first-match)

**Block piping to shell**: Add rule on the sink command with `[rule.pipe].from`

## Workflow

0. If no project config exists, initialize one:
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/bin/cc-allow --init
   ```
1. Read the existing config at `.claude/cc-allow.toml`
2. Determine what change is needed
3. Add new rules
4. Write the updated config
5. Validate with `--fmt` to check syntax and view rules by specificity:
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/bin/cc-allow --fmt
   ```
6. Test the new rule with a matching command:
   ```bash
   echo 'git push --force' | ${CLAUDE_PLUGIN_ROOT}/bin/cc-allow
   echo $?  # 0=allow, 1=ask, 2=deny
   ```
7. Use `--debug` for detailed evaluation trace:
   ```bash
   echo 'git push --force' | ${CLAUDE_PLUGIN_ROOT}/bin/cc-allow --debug
   ```
