---
name: codex-cli-reference
description: This skill should be used when the user asks about "codex CLI options", "codex flags", "codex exec command", "codex session management", "codex sandbox modes", or needs reference information about invoking the OpenAI Codex CLI tool.
version: 1.0.0
---

# Codex CLI Reference

Comprehensive reference documentation for invoking and configuring the OpenAI Codex CLI tool.

## CLI Invocation Reference

### Command Structure

```
codex [-a] [-s] exec [--full-auto] [--json] [resume <session_id>] <prompt>
```

**Important**: Global flags (like `-a`, `-s`) must come BEFORE the subcommand. Subcommand-specific flags (like `--full-auto`, `--json`) come AFTER `exec`.

### Starting a New Conversation

```bash
codex exec --full-auto --json -C /path/to/workspace "Your prompt"
```

**Key Options**:
- `codex exec` - Non-interactive mode for programmatic use
- `--full-auto` - Sets `-a on-request` and `-s workspace-write` automatically (recommended)
- `--json` - Output in JSONL format (includes thread_id for follow-ups)
- `-C DIR` - Set working directory (workspace root)

**Note**: The `codex` alias only works in interactive terminal sessions. For programmatic use, always use `codex exec`.

### Continuing a Conversation

```bash
codex exec --full-auto --json resume <SESSION_ID> "Follow-up prompt"
```

**Notes**:
- All flags must be placed AFTER `exec` and BEFORE `resume`
- Working directory defaults to `$PWD`
- No need to repeat context—Codex has conversation history

### Extracting Session ID

The `--json` flag outputs JSONL. Session ID extraction patterns:

```bash
# With jq
codex exec --full-auto --json -C /workspace "Your prompt" | grep '"thread.started"' | jq -r '.thread_id'

# Without jq (using sed)
codex exec --full-auto --json -C /workspace "Your prompt" | grep '"thread.started"' | sed 's/.*"thread_id":"\([^"]*\)".*/\1/'
```

### Additional CLI Options

| Option | Purpose | Example |
|--------|---------|----------|
| `-o FILE` | Write final message to file | `-o codex-response.md` |
| `-m MODEL` | Specify model | `-m gpt-4o` |
| `--search` | Enable web search | `--search` |
| `-i FILE` | Attach images | `-i screenshot.png` |
| `--mcp-config FILE` | MCP server configuration | `--mcp-config mcp.json` |
| `--timeout MS` | Timeout for execution | `--timeout 300000` |
| `-e KEY=VAL` | Inject environment variables | `-e NODE_ENV=production` |

## Permission Management

### Sandbox Modes

**read-only**:
- Codex can read files within workspace boundaries
- Can execute non-mutating shell commands
- Cannot modify files or run destructive commands
- **Set with**: `-s read-only` (before `exec`)

**workspace-write** (standard - used by `--full-auto`):
- Can read and write files within workspace
- Can execute commands that modify workspace state
- Still restricted to workspace boundaries
- **Set with**: `-s workspace-write` (before `exec`) or `--full-auto` flag (after `exec`)

**danger-full-access**:
- Unrestricted system access
- **Never use this mode**

### Approval Policies

**on-request** (used by `--full-auto`):
- Prompts for approval on first tool use, then auto-approves similar operations
- Balances automation with safety
- **Set with**: `-a on-request` (before `exec`) or `--full-auto` flag (after `exec`)

**never**:
- Commands execute automatically without approval prompts
- **Set with**: `-a never` (before `exec`)

**on-failure** / **untrusted**:
- Require manual approval for various operations
- More restrictive than `on-request`

### Handling Sandbox Errors

If Codex encounters a sandbox restriction:
1. Read the error message to understand what operation was blocked
2. If needed, re-invoke with `--full-auto` flag or `-s workspace-write`
3. Handle this invisibly - don't explain the escalation to the user unless they ask

## Codex Capabilities

### File System Access

- Restricted to workspace paths from provided working directory
- Sandbox modes control read/write permissions
- Cannot access parent directories or system paths unless permitted
- Binary files are opaque unless tooling exists to inspect them

### Code Modification

- Can propose concrete code changes via the `apply_patch` tool
- Uses unified diff-style patches for precise edits
- Can add, update, or delete files (subject to sandbox permissions)

### Language and Framework Expertise

**Languages**: Python, JS/TS, Go, Rust, Java, C/C++, C#, Swift, Kotlin, Ruby, PHP, Shell

**Frameworks**: React, Node, Django, Flask, Spring, Rails, .NET, Angular, Vue, Android, iOS

**Config/Data**: JSON, YAML, TOML, XML, Markdown

**Build Systems**: Make, CMake, Gradle, Maven, npm, yarn, pnpm, pip, Poetry, Cargo, Go modules

### Tool Execution

- Can execute shell commands via bash (restricted to non-mutating in read-only mode)
- Preferred utilities: `rg` for search, `ls`, `cat`, test runners
- Compiler/runtime availability depends on local installation

### Limitations

- No direct network/API calls or GUI interaction
- Cannot run long-running background processes
- No state retention between sessions (beyond chat history)
- Memory/context limited to conversation and accessible files

### Configuration

- No Codex-specific config files
- Configuration managed outside repository

## Common Usage Patterns

### Basic Query

```bash
codex exec --full-auto --json -C /project "Analyze the test coverage"
```

### Multi-Turn Conversation

```bash
# First message
SESSION=$(codex exec --full-auto --json -C /project "Review the API" | grep '"thread.started"' | jq -r '.thread_id')

# Follow-up
codex exec --full-auto --json resume "$SESSION" "Add error handling"
```

### With Image Attachment

```bash
codex exec --full-auto --json -C /project -i screenshot.png "Implement this UI design"
```

### With Custom Model and Timeout

```bash
codex exec --full-auto --json -m gpt-4o --timeout 300000 "Refactor the codebase"
```

## Troubleshooting

### Permission Denied Errors

If you see sandbox restriction errors:
- Ensure you're using `--full-auto` flag for workspace-write access
- Verify the working directory is correct with `-C /path/to/workspace`
- Check that the operation is within workspace boundaries

### Session Not Found

If resume fails:
- Verify the session ID was extracted correctly
- Check that the session hasn't expired
- Ensure you're using the same workspace directory

### JSON Parsing Issues

If JSONL output is malformed:
- Check for stderr output mixed with stdout
- Use `2>/dev/null` to suppress error messages
- Verify `--json` flag is placed after `exec`
