---
name: amp-permissions
description: Configure Amp's permissions -- allowing, rejecting, or asking for tool invocations in Amp. Activates with phrases like "reject using this tool", "I want to modify the tool permissions", or "change Amp's permissions".
---

## Permissions Reference

> source: https://ampcode.com/manual/appendix#permissions-configuration

Amp’s permission system controls **every** tool invocation before execution. The system uses a single, ordered list of rules that are evaluated sequentially until the first match is found.

### How Permissions Work

Before running any tool, Amp evaluates permissions through these steps:

1. **Find matching rule**: The first rule that matches the tool _and_ its arguments wins
2. **Determine action**: The matching rule tells Amp to:
   - `allow` - run the tool silently
   - `reject` - block the call (optionally with custom message)
   - `ask` - prompt the operator for approval
   - `delegate` - delegate decision to an external program
3. **Examine builtin rules**: If no user rule matches, Amp falls back to built-in rules (e.g., allowing `ls` via Bash)
4. **Default Behavior**: If no matching entry is found at all:
   - Main thread: Amp asks the operator
   - Sub-agent: Amp rejects the tool call

### Configuration

Rules are defined in the `amp.permissions` setting. Each rule is a JSON object with these properties:

| Key       | Type                                            | Required                        | Description                                                                                           |
| --------- | ----------------------------------------------- | ------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `tool`    | string (glob)                                   | Yes                             | Name of the tool this rule applies to. Supports globs (`Bash`, `mcp__playwright__*`, `**/my-tool`)    |
| `matches` | object                                          | –                               | Map of _tool-argument → condition_. If omitted, the rule matches _all_ calls to the tool              |
| `action`  | `"allow"` / `"reject"` / `"ask"` / `"delegate"` | Yes                             | What Amp should do if the rule matches                                                                |
| `context` | `"thread"` / `"subagent"`                       | –                               | Restrict the rule to the main thread or to sub-agents. Omit to apply everywhere                       |
| `to`      | string (program)                                | only when `action = "delegate"` | Program that decides. Must be on `$PATH`                                                              |
| `message` | string                                          | only when `action = "reject"`   | Message returned to the model. If set, the rejection continues the conversation instead of halting it |

### Match Conditions

Each `matches` key corresponds to a tool argument. Values can be:

- **string** – glob pattern (`*` = any characters) or regex pattern (`/pattern/`)
- **array** – OR of each entry (`["rm -rf *", "git commit *"]`)
- **boolean/number/null/undefined** – literal value match
- **object** – nested structure matching

#### Regular Expression Patterns

Strings that start and end with `/` are treated as regular expressions:

```
{
  "tool": "Bash",
  "matches": { "cmd": "/^git (status|log|diff)$/" },
  "action": "allow"
}
```

This matches exactly `git status`, `git log`, or `git diff` but not `git commit`.

#### Value Type Matching

- **String patterns** only match string values using glob syntax
- **Literal values** (boolean, number, null, undefined) require exact matches
- **Array conditions** provide OR logic across multiple patterns
- **Nested objects** enable deep property matching with dot notation for objects and numeric strings for array indices

### Examples

#### Basic Permission Rules

Allow all Bash commands in main thread, but restrict sub-agents:

```
{
  "tool": "Bash",
  "action": "allow",
  "context": "thread"
},
{
  "tool": "Bash",
  "matches": { "cmd": ["rm -rf *", "find *", "git commit *"] },
  "action": "reject",
  "context": "subagent"
}
// In text form:
// allow --context thread Bash
// reject --context subagent Bash --cmd "rm -rf *" --cmd "find *" --cmd "git commit *"
```

Ask before grepping in the home directory:

```
{
  "tool": "Grep",
  "matches": { "path": "$HOME/*" },
  "action": "ask"
}
// In text form:
// ask Grep --path '$HOME/*'
```

Forbid editing dotfiles:

```
{
  "tool": "edit_file",
  "matches": { "path": ".*" },
  "action": "reject"
}
// In text form:
// reject edit_file --path '.*'
```

Reject destructive git commands with a helpful message (allows the model to continue):

```
{
  "tool": "Bash",
  "matches": { "cmd": ["*git checkout*", "*git reset*"] },
  "action": "reject",
  "message": "Do not use git checkout or git reset. Use edit_file to make manual changes instead."
}
```

#### Delegation

Delegate GitHub CLI calls to external validator:

```
{
  "tool": "Bash",
  "matches": { "cmd": "gh *" },
  "action": "delegate",
  "to": "my-gh-permission-helper"
}
// In text form:
// delegate --to my-gh-permission-helper Bash --cmd "gh *"
```

When instructed to delegate, Amp will:

- Execute the program named in `to` (must be on `$PATH`, or an absolute path)
- Export `AMP_THREAD_ID`, `AGENT_TOOL_NAME=nameOfInvokedTool` and `AGENT=amp` environment variables
- Pipe tool parameters to **stdin** as JSON
- Interpret exit status:
  - `0` → allow
  - `1` → ask operator
  - `≥ 2` → reject (stderr is surfaced to the model)

### Text Format

For editing many rules conveniently, you can use the text format with `amp permissions` commands:

```
<action> [--<action-arg> ...] <tool> [--<match-key>[:<op>] <value>] ...
```

The text format is designed to be compatible with UNIX shell syntax, allowing you to copy/paste rules from and to the command line without further editing.

```bash
# Basic allow/reject rules
allow Bash --cmd 'git *'
reject Bash --cmd 'python *'

# Multiple conditions
allow Bash --cmd 'git diff*' --cmd 'git commit*'

# Delegation
delegate --to amp-git-permissions Bash --cmd '*'
```

- Single- and double-quoted strings are supported
- unquoted true, false, null and numeric words are interpreted as JSON literals
- Any value containing `*` must be quoted

### Listing Rules

```bash
amp permissions list                    # Show user rules
amp permissions list --builtin          # Only built-in rules
```

### Testing Rules

For example, testing if it would ask on a git commit:

```
$ amp permissions test Bash --cmd "git commit -m 'test'"
tool: Bash
arguments: {"cmd":"git commit -m 'test'"}
action: ask
matched-rule: 12
source: builtin
```

or testing if it would ask to edit.env in the current directory

```
$ amp permissions test edit_file --path "$PWD/README.md"
tool: edit_file
arguments: {"path":"/Users/your/project/README.md"}
action: allow
matched-rule: 29
source: builtin
```

The test subcommand allows you to test permission rules without actually running any tools or hoping that the agent will generate the right parameters.

### Editing Rules

You can use `$EDITOR` to edit rules interactively in the text format:

```
$ amp permissions edit
```

And you can edit from STDIN:

```
$ amp permissions edit <<'EOF'
# Ask before every tool use
ask '*'
EOF
```

### Add Rules

For example, reject all mermaid diagrams:

```
$ amp permissions add reject mermaid
```

or ask before searching about node.js or npm packages:

```
$ amp permissions add ask web_search --query "*node*" --query "*npm*"
```

### Matching multiple tools with a single rule

Tool names support glob patterns for managing groups of tools:

- `Bash` - matches only the Bash tool
- `mcp__playwright__*` - matches all Playwright MCP tools

### Context Restrictions

Use the `context` field to restrict rules to the main agent or subagents

- `"context": "thread"` - only applies in main conversation thread
- `"context": "subagent"` - only applies to sub-agent tool calls
- Omit `context` - applies everywhere
