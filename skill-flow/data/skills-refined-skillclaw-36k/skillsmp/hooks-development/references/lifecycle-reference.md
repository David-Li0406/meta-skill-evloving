## Lifecycle Diagrams

### 1. Main Session Lifecycle

```
┌──────────────────┐
│   SessionStart   │
└──────────────────┘
  │
  │
  ∨
┌──────────────────┐
│ UserPromptSubmit │ <┐
└──────────────────┘  │
  │                   │
  │                   │
  ∨                   │
┌──────────────────┐  │
│    PreCompact    │  │
└──────────────────┘  │
  │                   │
  │                   │ new prompt
  ∨                   │
┌──────────────────┐  │
│    Tool Loop     │  │
└──────────────────┘  │
  │                   │
  │                   │
  ∨                   │
┌──────────────────┐  │
│       Stop       │ ─┘
└──────────────────┘
  │
  │
  ∨
┌──────────────────┐
│    SessionEnd    │
└──────────────────┘
```

**Hook Details:**

- **SessionStart** — Matchers: `startup|resume|clear|compact`. Cannot block. Outputs: `additionalContext`, `CLAUDE_ENV_FILE`
- **UserPromptSubmit** — CAN BLOCK (exit 2 or `decision:block`). Inputs: `prompt`, `cwd`, `session_id`
- **PreCompact** — Fires if context full OR `/compact`. Cannot block. Matchers: `manual|auto`. Fires BEFORE summarization
- **Tool Loop** — See Diagram 2 for details. May repeat multiple times per response
- **Stop** — CAN BLOCK (`decision:block` + reason). `stop_hook_active` prevents infinite loops
- **SessionEnd** — Reasons: `clear|logout|prompt_input_exit|other`. Cannot block

```{=latex}
\newpage
```

### 2. Tool Execution Loop

```
                 more tools    ┌───────────────────┐
  ┌──────────────────────────> │    PreToolUse     │ <┐
  │                            └───────────────────┘  │
  │                              │                    │
  │                              │                    │
  │                              ∨                    │
  │                            ┌───────────────────┐  │
  │                            │ PermissionRequest │  │
  │                            └───────────────────┘  │
  │                              │                    │
  │                              │                    │ more tools
  │                              ∨                    │
┌──────────────┐               ┌───────────────────┐  │
│ SubagentStop │ <──────────── │   Tool Executes   │  │
└──────────────┘               └───────────────────┘  │
  │                              │                    │
  │                              │                    │
  ∨                              ∨                    │
┌──────────────┐               ┌───────────────────┐  │
│     Stop     │ <──────────── │    PostToolUse    │ ─┘
└──────────────┘               └───────────────────┘
```

**Hook Details:**

- **PreToolUse** — CAN BLOCK. Output `permissionDecision`: `allow|deny|ask`. Can provide `updatedInput` to modify tool parameters
- **PermissionRequest** — CAN BLOCK. Output `behavior`: `allow|deny`. Skipped if PreToolUse already allowed
- **Tool Executes** — The actual tool runs (Bash, Edit, Read, Write, MCP tools)
- **SubagentStop** — CAN BLOCK. Task tool only. Validates subagent completion
- **PostToolUse** — CAN BLOCK (soft). Tool already ran; `decision:block` required for Claude to see `reason` (visibility, not blocking)

### 3. Blocking vs Non-Blocking Hooks

**CAN BLOCK** — These hooks can prevent or modify execution:

| Hook              | Block Type | Mechanism                           | Effect                                                |
| ----------------- | ---------- | ----------------------------------- | ----------------------------------------------------- |
| UserPromptSubmit  | Hard       | exit 2 OR `decision:block`          | Erases prompt, shows reason to user                   |
| PreToolUse        | Hard       | exit 2 OR `permissionDecision:deny` | Prevents execution, reason fed to Claude              |
| PermissionRequest | Hard       | `behavior:deny`                     | Rejects permission, optional interrupt flag           |
| PostToolUse       | Soft       | `decision:block` + reason           | Tool already ran; `decision:block` = visibility only  |
| SubagentStop      | Hard       | `decision:block` + reason           | Forces subagent to continue working                   |
| Stop              | Hard       | `decision:block` + reason           | Forces Claude to continue (check `stop_hook_active`!) |

**CANNOT BLOCK** — These hooks are informational only:

| Hook         | Purpose                                         |
| ------------ | ----------------------------------------------- |
| SessionStart | Inject context, set env vars, run setup scripts |
| PreCompact   | Backup transcripts before summarization         |
| Notification | Desktop/Slack/Discord alerts (parallel event)   |
| SessionEnd   | Cleanup, logging, archive transcripts           |

```{=latex}
\newpage
```

### 4. Parallel Events (Notification)

```
┌──────────────┐     ┌────────────┐
│  Main Flow   │ ──> │ Sequential │
└──────────────┘     └────────────┘
┌──────────────┐     ┌────────────┐
│ Notification │ ──> │  Parallel  │
└──────────────┘     └────────────┘
```

**Key Points:**

- **Main Flow** runs sequentially: SessionStart → UserPromptSubmit → PreCompact → Tools → Stop → SessionEnd
- **Notification** fires independently when Claude Code sends system notifications
- Not part of main execution flow; can fire at any time during session

**Notification Matchers:**

- `permission_prompt` — Permission dialog shown
- `idle_prompt` — Claude waiting for input
- `auth_success` — Authentication completed
- `elicitation_dialog` — Additional info requested

### 5. Universal Control (All Hooks)

Every hook can output these fields:

| Field                  | Effect                                          |
| ---------------------- | ----------------------------------------------- |
| `continue: false`      | Halts Claude entirely (overrides all decisions) |
| `stopReason: "..."`    | Message shown to user when `continue=false`     |
| `suppressOutput: true` | Hide stdout from transcript                     |
| `systemMessage: "..."` | Warning shown to user                           |

```{=latex}
\newpage
\begin{landscape}
```

## Lifecycle Behavior Details

### Blocking Mechanisms

| Hook                  | Hard Block                          | Soft Block                | Effect                                               |
| --------------------- | ----------------------------------- | ------------------------- | ---------------------------------------------------- |
| **UserPromptSubmit**  | Exit 2 OR `decision:block`          | —                         | Erases prompt, shows reason to user only             |
| **PreToolUse**        | Exit 2 OR `permissionDecision:deny` | `permissionDecision:ask`  | Prevents tool execution, reason fed to Claude        |
| **PermissionRequest** | `behavior:deny`                     | —                         | Rejects permission, optional interrupt flag          |
| **PostToolUse**       | —                                   | `decision:block` + reason | Tool already ran; `decision:block` = visibility only |
| **SubagentStop**      | `decision:block` + reason           | —                         | Forces subagent to continue working                  |
| **Stop**              | `decision:block` + reason           | —                         | Forces Claude to continue (check stop_hook_active!)  |

### Universal Control (All Hooks)

- **`continue: false`** — Halts Claude entirely (overrides all other decisions)
- **`stopReason`** — Message shown to user when continue=false
- **`suppressOutput: true`** — Hide stdout from transcript
- **`systemMessage`** — Warning shown to user

### Key Flows Explained

**1. Tool Execution Loop**

- PreToolUse → PermissionRequest → Tool → PostToolUse repeats for EACH tool call
- Claude may call multiple tools in one response
- PreToolUse can skip PermissionRequest with `permissionDecision:allow`

**2. Prompt Loop**

- After Stop, user submits new prompt → cycle restarts at UserPromptSubmit
- Stop hook with `decision:block` forces continuation without new prompt

**3. Conditional Hooks**

- **PermissionRequest**: Only fires if permission dialog would be shown (skipped if PreToolUse allows or tool is pre-approved)
- **SubagentStop**: Only fires for Task tool sub-agents, not Bash/Edit/Read/Write
- **PreCompact**: Fires when context is full (auto) OR user runs /compact (manual)

**4. Parallel Events**

- **Notification**: Fires independently when Claude Code sends system notifications
- Not part of main execution flow; can fire at any time during session

**5. Loop Prevention**

- `stop_hook_active: true` in Stop/SubagentStop input means hook already triggered continuation
- MUST check this to prevent infinite loops when using `decision:block`

```{=latex}
\end{landscape}
\newpage
\begin{landscape}
```

## Hook Events Reference

### Overview

| Event                 | When It Fires                                       | Blocks? | Matchers                                                                 |
| --------------------- | --------------------------------------------------- | ------- | ------------------------------------------------------------------------ |
| **SessionStart**      | Session begins (new, `--resume`, `/clear`, compact) | No      | `startup`, `resume`, `clear`, `compact`                                  |
| **UserPromptSubmit**  | User presses Enter, BEFORE Claude processes         | **Yes** | None (all prompts)                                                       |
| **PreToolUse**        | After Claude creates tool params, BEFORE execution  | **Yes** | Tool names: `Task`, `Bash`, `Read`, `Write`, `Edit`, `mcp__*`            |
| **PermissionRequest** | Permission dialog about to show                     | **Yes** | Same as PreToolUse                                                       |
| **PostToolUse**       | After tool completes **successfully** (NOT errors!) | **Yes** | Same as PreToolUse                                                       |
| **Notification**      | System notification sent                            | No      | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` |
| **SubagentStop**      | Task sub-agent finishes                             | **Yes** | None (global)                                                            |
| **Stop**              | Main agent finishes (not on interrupt)              | **Yes** | None (global)                                                            |
| **PreCompact**        | Before context summarization                        | No      | `manual`, `auto`                                                         |
| **SessionEnd**        | Session terminates                                  | No      | None (global)                                                            |

### Input & Output Details

| Event                 | Key Inputs                                             | Output Capabilities                                                                              |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| **SessionStart**      | `session_id`, `source`, `transcript_path`              | `additionalContext`; `CLAUDE_ENV_FILE` for env vars                                              |
| **UserPromptSubmit**  | `prompt`, `cwd`, `session_id`                          | `{"decision": "block"}` to reject; `{"additionalContext": "..."}` to inject; Exit 2 = hard block |
| **PreToolUse**        | `tool_name`, `tool_input`, `tool_use_id`               | `permissionDecision`: `allow`/`deny`/`ask`; `updatedInput` to modify params                      |
| **PermissionRequest** | `tool_name`, `tool_input`, `tool_use_id`               | `decision.behavior`: `allow`/`deny`; `updatedInput`; `message`                                   |
| **PostToolUse**       | `tool_name`, `tool_input`, `tool_response`             | `{"decision": "block", "reason": "..."}` required for Claude visibility                          |
| **Notification**      | `message`, `notification_type`                         | stdout in verbose mode (Ctrl+O)                                                                  |
| **SubagentStop**      | `transcript_path`, `stop_hook_active`                  | `{"decision": "block", "reason": "..."}` forces continuation                                     |
| **Stop**              | `transcript_path`, `stop_hook_active`                  | `{"decision": "block"}` blocks stopping; `additionalContext` for info; `{}` allows stop          |
| **PreCompact**        | `trigger`, `custom_instructions`                       | stdout in verbose mode                                                                           |
| **SessionEnd**        | `reason`: `clear`/`logout`/`prompt_input_exit`/`other` | Debug log only                                                                                   |

### CRITICAL: Non-Existent Hook Types (Lesson Learned 2026-01-12)

**There is NO `PostToolUseError` hook in Claude Code.** This is a common misconception.

| Misconception                              | Reality                   | Consequence                                                                 |
| ------------------------------------------ | ------------------------- | --------------------------------------------------------------------------- |
| `PostToolUseError` exists for failed tools | **Does NOT exist**        | Adding to settings.json causes: `"PostToolUseError: Invalid key in record"` |
| PostToolUse fires for all tool completions | **Only fires on SUCCESS** | Failed Bash commands (exit ≠ 0) do NOT trigger PostToolUse                  |
| GitHub issues = implemented features       | **Issues are REQUESTS**   | Always verify against official docs before implementing                     |

**Valid hook types (exhaustive list):**

- `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `Notification`, `SubagentStop`, `Stop`, `PreCompact`, `SessionEnd`

**What this means:**

- You **cannot** hook into failed Bash commands
- You **cannot** remind users about errors via PostToolUse (it won't fire)
- The UV reminder for failed `pip` commands is **not possible** with current hooks

**Workarounds for error handling:**

1. Use `PreToolUse` to block dangerous commands BEFORE they run
2. Use `Stop` hook to validate overall session state
3. Accept the limitation until Claude Code adds error hooks

```{=latex}
\end{landscape}
\newpage
```

## Hook Input Delivery Mechanism

### How Hooks Receive Input

All hooks receive their input data via **stdin as a JSON object**. The JSON structure matches the "Key Inputs" column in the table above.

**Critical**: Hook inputs are NOT passed via environment variables. The only environment variables available to hooks are:

- `CLAUDE_PROJECT_DIR` — Project root directory
- `CLAUDE_CODE_REMOTE` — "true" if running in web mode
- `CLAUDE_ENV_FILE` — Env var persistence file (SessionStart only)

### Required Input Parsing Pattern

Every PreToolUse/PostToolUse hook MUST parse stdin:

```bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""' 2>/dev/null) || TOOL_NAME=""
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null) || COMMAND=""
CWD=$(echo "$INPUT" | jq -r '.cwd // ""' 2>/dev/null) || CWD=""
```

**Warning**: Without this parsing, `$COMMAND` will be empty and your validation logic will silently pass all commands.

### Example Input JSON

For a Bash tool call:

```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "gh issue list --limit 5"
  },
  "tool_use_id": "toolu_01ABC...",
  "cwd": "/Users/user/project"
}
```

### References

- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) — Official documentation
- [How to Configure Hooks](https://claude.com/blog/how-to-configure-hooks) — Anthropic blog

```{=latex}
\newpage
```

## Use Cases by Hook Event

| Hook                  | Use Case              | Description                                                  |
| --------------------- | --------------------- | ------------------------------------------------------------ |
| **SessionStart**      | Context loading       | Load git status, branch info, recent commits into context    |
|                       | Task injection        | Inject TODO lists, sprint priorities, GitHub issues          |
|                       | Setup scripts         | Install dependencies or run setup on session begin           |
|                       | Environment vars      | Set variables via `$CLAUDE_ENV_FILE` for persistence         |
|                       | Dynamic config        | Load project-specific CLAUDE.md or context files             |
|                       | Telemetry             | Initialize logging or telemetry for the session              |
|                       | Multi-account tokens  | Validate GH_TOKEN matches expected account for directory     |
|                       | Session tracking      | Track session start for duration/correlation reporting       |
| · · · · · · · · · · · | · · · · · · · · · · · | · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·    |
| **UserPromptSubmit**  | Audit logging         | Log timestamps, session IDs, prompt content for compliance   |
|                       | Security filtering    | Detect and block sensitive patterns (API keys, passwords)    |
|                       | Context injection     | Append git branch, recent changes, sprint goals to prompts   |
|                       | Policy validation     | Validate prompts against team policies or coding standards   |
|                       | Keyword blocking      | Block forbidden keywords or dangerous instructions           |
|                       | Ralph Wiggum          | Inject reminders about testing or documentation              |
|                       | Prompt capture        | Cache prompt text + timestamp for Stop hook session summary  |
| · · · · · · · · · · · | · · · · · · · · · · · | · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·    |
| **PreToolUse**        | Destructive blocking  | Block `rm -rf`, `git push --force`, `DROP TABLE`             |
|                       | File protection       | Prevent access to `.env`, `.git/`, `credentials.json`        |
|                       | Parameter validation  | Validate paths, check file existence before execution        |
|                       | Sandboxing            | Add `--dry-run` flags to dangerous commands                  |
|                       | Input modification    | Fix paths, inject linter configs, add safety flags           |
|                       | Auto-approve          | Reduce permission prompts for safe operations                |
|                       | Lock file protection  | Block writes to `package-lock.json`, `uv.lock`               |
|                       | Multi-account git     | Validate SSH auth matches expected GitHub account            |
|                       | HTTPS URL blocking    | Block git push with HTTPS (require SSH for multi-account)    |
|                       | ASCII art policy      | Block manual diagrams; require graph-easy source block       |
| · · · · · · · · · · · | · · · · · · · · · · · | · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·    |
| **PermissionRequest** | Auto-approve safe     | Auto-approve `npm test`, `pytest`, `cargo build`             |
|                       | Auto-deny dangerous   | Deny dangerous operations without user prompt                |
|                       | Command modification  | Inject flags, change parameters before approval              |
|                       | Team policies         | Implement team-specific permission policies                  |
|                       | Fatigue reduction     | Auto-approve known-safe tool patterns                        |
|                       | Audit trails          | Log all permission decisions                                 |
| · · · · · · · · · · · | · · · · · · · · · · · | · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·    |
| **PostToolUse**       | Auto-format           | Run `prettier`, `black`, `gofmt` after edits                 |
|                       | Lint checking         | Run `ruff check`, `eslint --fix`, `cargo clippy`             |
|                       | File validation       | Validate write success and file integrity                    |
|                       | Transcript conversion | Convert JSONL transcripts to readable JSON                   |
|                       | Task reminders        | Remind about related tasks when files modified               |
|                       | CI triggers           | Trigger CI checks or pre-commit hooks                        |
|                       | Output logging        | Log all tool outputs for debugging/compliance                |
|                       | Markdown pipeline     | markdownlint (MD058 table blanks) + prettier for .md files   |
|                       | Dotfiles sync         | Detect chezmoi-tracked files; remind to sync                 |
|                       | ADR-Spec sync         | Remind to update Design Spec when ADR modified (and v.v.)    |
|                       | Graph-easy reminder   | Prompt to use skill instead of CLI for reproducibility       |
| · · · · · · · · · · · | · · · · · · · · · · · | · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·    |
| **Notification**      | Desktop alerts        | `osascript` (macOS) or `notify-send` (Linux)                 |
|                       | Chat webhooks         | Slack/Discord/Teams integration for remote alerts            |
|                       | Sound alerts          | Custom sounds when Claude needs attention                    |
|                       | Email                 | Email notifications for long-running tasks                   |
|                       | Mobile push           | Pushover or similar for mobile notifications                 |
|                       | Analytics             | Log notification events for analytics                        |
| · · · · · · · · · · · | · · · · · · · · · · · | · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·    |
| **SubagentStop**      | Task validation       | Validate sub-agents completed full assigned task             |
|                       | TTS announcements     | Announce completion via text-to-speech                       |
|                       | Performance logging   | Log task results and duration                                |
|                       | Force continuation    | Continue if output incomplete or fails validation            |
|                       | Task chaining         | Chain additional sub-agent tasks based on results            |
| · · · · · · · · · · · | · · · · · · · · · · · | · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·    |
| **Stop**              | Premature prevention  | Block if tests failing or task incomplete                    |
|                       | Test suites           | Run `npm test`, `pytest`, `cargo test` on every stop         |
|                       | AI summaries          | Generate completion summaries with TTS playback              |
|                       | Ralph Wiggum          | Force Claude to verify task completion                       |
|                       | Validation gates      | Ensure code compiles, lints pass, tests succeed              |
|                       | Auto-commits          | Create git commits or PR drafts when work completes          |
|                       | Team notifications    | Send completion notifications to channels                    |
|                       | Link validation       | Lychee check on .md files; use `additionalContext` to inform |
|                       | Session summary       | Generate JSON summary: git status, duration, workflows       |
|                       | Background validation | Full workspace link scan (async, non-blocking)               |
| · · · · · · · · · · · | · · · · · · · · · · · | · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·    |
| **PreCompact**        | Transcript backups    | Create backups before context compression                    |
|                       | History preservation  | Preserve conversation to external storage                    |
|                       | Event logging         | Log compaction with timestamp and trigger type               |
|                       | Context extraction    | Save important context before summarization                  |
|                       | User notification     | Notify user that context is about to be compacted            |
| · · · · · · · · · · · | · · · · · · · · · · · | · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·    |
| **SessionEnd**        | Temp cleanup          | Cleanup temporary files, caches, artifacts                   |
|                       | Session stats         | Log duration, tool calls, tokens used                        |
|                       | State saving          | Save session state for potential resume                      |
|                       | Analytics             | Send session summary to analytics service                    |
|                       | Transcript archive    | Archive transcripts to long-term storage                     |
|                       | Environment reset     | Reset env vars or undo session-specific changes              |

```{=latex}
\newpage
```

## Configuration Reference

### Settings Priority

1. `.claude/settings.local.json` — Project local (highest priority)
2. `.claude/settings.json` — Project-wide
3. `~/.claude/settings.json` — User-wide (lowest priority)

### Exit Codes

- **0** — Success/allow (JSON output processed)
- **2** — Hard block, cannot bypass (stderr only)
- **Other** — Non-blocking error

### Environment Variables

- `CLAUDE_PROJECT_DIR` — Project root (available in all hooks)
- `CLAUDE_CODE_REMOTE` — `"true"` if running in web mode (all hooks)
- `CLAUDE_ENV_FILE` — Env var persistence file (SessionStart only)

### Hook Types

**Command Hook** — Deterministic, fast, full control:

```json
{ "type": "command", "command": "/path/to/script.py", "timeout": 60 }
```

**Prompt Hook** — LLM-evaluated via Haiku, context-aware:

```json
{ "type": "prompt", "prompt": "Check if task is complete", "timeout": 30 }
```

### MCP Tool Naming

- **Pattern**: `mcp__<server>__<tool>`
- **Examples**: `mcp__memory__create_entities`, `mcp__filesystem__read_file`
- **Matchers**: `"mcp__memory__.*"`, `"mcp__.*__write.*"`

### Blocking Output Format

**PreToolUse/PermissionRequest**:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "...",
    "permissionDecision": "allow|deny|ask"
  }
}
```

**Stop/SubagentStop (blocking)**:

```json
{ "decision": "block", "reason": "..." }
```

**Stop (informational, non-blocking)**:

```json
{
  "additionalContext": "Message for Claude to see and act on",
  "systemMessage": "Message for user to see in status line"
}
```

> **Note**: Stop hooks do NOT support `hookSpecificOutput`. Use `additionalContext` for Claude visibility, `systemMessage` for user visibility. Using only `systemMessage` means Claude won't see the message in context (verified 2026-01-21).

```{=latex}
\newpage
```

## JSON Field Visibility by Hook Type (Critical Reference)

**Source**: [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks), [GitHub Issue #3983](https://github.com/anthropics/claude-code/issues/3983)

This section documents exactly which JSON fields Claude can see for each hook type. **Getting this wrong means your hook runs but Claude never receives your message.**

### Decision Semantics: Blocking vs Visibility

| Hook Type            | `decision: "block"` Meaning               | Claude Sees `reason`? |
| -------------------- | ----------------------------------------- | --------------------- |
| **PostToolUse**      | **Visibility only** (tool already ran)    | ✅ Yes, if present    |
| **Stop**             | **ACTUALLY BLOCKS** stopping              | ✅ Yes, mandatory     |
| **SubagentStop**     | **ACTUALLY BLOCKS** subagent stopping     | ✅ Yes, mandatory     |
| **UserPromptSubmit** | Erases prompt, reason to USER only        | ❌ No                 |
| **PreToolUse**       | **Deprecated** - use `permissionDecision` | ❌ No                 |

### PostToolUse: Visibility Requires `decision: "block"`

**Counterintuitive but documented**: Claude only sees `reason` when `decision: "block"` is present.

```bash
# ❌ WRONG - Claude sees NOTHING
echo '{"reason": "Please fix this"}'

# ❌ WRONG - additionalContext alone not visible
echo '{"hookSpecificOutput": {"additionalContext": "..."}}'

# ✅ CORRECT - Claude sees the reason
jq -n --arg reason "Please fix this" '{decision: "block", reason: $reason}'
```

**What Claude sees with correct format**:

```
> Bash operation feedback:
 - Please fix this
```

**Key insight**: The `decision: "block"` is required for visibility, but it does NOT actually block anything - the tool already ran.

### Stop Hooks: Blocking vs Informational

**CRITICAL DIFFERENCE**: For Stop hooks, `decision: "block"` **actually prevents Claude from stopping**.

| Intent                    | Output Format                                          | Effect                            |
| ------------------------- | ------------------------------------------------------ | --------------------------------- |
| **Allow stop normally**   | `{}` (empty object)                                    | Claude stops normally             |
| **Block stop (continue)** | `{"decision": "block", "reason": "..."}`               | Claude CANNOT stop, must continue |
| **Informational message** | `{"additionalContext": "...", "systemMessage": "..."}` | Claude sees info, stops normally  |
| **Hard stop (emergency)** | `{"continue": false, "stopReason": "..."}`             | Claude halted immediately         |

> **Note**: Stop hooks do NOT support `hookSpecificOutput`. Use `additionalContext` for Claude visibility + `systemMessage` for user visibility. Using only `systemMessage` means Claude won't see the message (verified 2026-01-21).

**Example: Informational Stop Hook (non-blocking)**

```bash
# ✅ Informs BOTH Claude (additionalContext) and user (systemMessage)
if [[ "$ISSUES" -gt 0 ]]; then
    jq -n --arg msg "[INFO] Found $ISSUES issues in repo" \
        '{additionalContext: $msg, systemMessage: $msg}'
fi
exit 0
```

**Example: Blocking Stop Hook (forces continuation)**

```bash
# ⚠️ ACTUALLY prevents Claude from stopping
if [[ "$TESTS_FAILED" == "true" ]]; then
    jq -n --arg reason "Tests are failing. Fix them before stopping." \
        '{decision: "block", reason: $reason}'
fi
exit 0
```

### PreToolUse: Use `permissionDecision`, Not `decision`

`decision: "block"` is **deprecated** for PreToolUse. Use the new format:

```bash
# ❌ DEPRECATED - still works but don't use
echo '{"decision": "block", "reason": "..."}'

# ✅ CORRECT - new format
jq -n --arg reason "Blocked because..." \
    '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: $reason}}'

# ✅ ALSO CORRECT - exit code 2 with stderr
echo "Blocked: dangerous command" >&2
exit 2
```

### Complete Field Visibility Matrix

| Field                            | PostToolUse | Stop         | PreToolUse    | UserPromptSubmit |
| -------------------------------- | ----------- | ------------ | ------------- | ---------------- |
| `reason` (with `decision:block`) | ✅ Claude   | ✅ Claude    | ❌ Deprecated | ❌ User only     |
| `additionalContext`              | ⚠️ Maybe    | ✅ Claude    | ❌ N/A        | ✅ Claude        |
| `permissionDecisionReason`       | ❌ N/A      | ❌ N/A       | ✅ Claude     | ❌ N/A           |
| `systemMessage`                  | ✅ Both     | ⚠️ User only | ✅ Both       | ✅ Both          |
| `stopReason`                     | ❌ N/A      | ✅ User      | ❌ N/A        | ❌ N/A           |
| Plain stdout (exit 0)            | ❌ Log only | ❌ Log only  | ❌ Log only   | ✅ Claude        |
| stderr (exit 2)                  | ❌ N/A      | ❌ N/A       | ✅ Claude     | ❌ N/A           |

**CRITICAL (Verified 2026-01-21)**: For Stop hooks, `systemMessage` displays to user in status line but does NOT get injected into Claude's conversation context. Use `additionalContext` for Claude visibility, `systemMessage` for user visibility, or both for maximum visibility.

### Common Mistakes and Fixes

| Mistake                                        | Symptom                            | Fix                                        |
| ---------------------------------------------- | ---------------------------------- | ------------------------------------------ |
| PostToolUse without `decision:block`           | Hook runs, Claude ignores          | Add `decision: "block"`                    |
| Stop hook with `decision:block` for info       | Claude can't stop                  | Use `additionalContext` instead            |
| Stop hook with `continue: false` to allow stop | "Stop hook prevented continuation" | Use `{}` (empty object)                    |
| PreToolUse with `decision:block`               | Works but deprecated               | Use `permissionDecision: "deny"`           |
| Mixing stdout and JSON                         | JSON parsing fails                 | Use only JSON or only plain text           |
| Logging to stdout                              | Extra text breaks JSON             | Log to stderr or /dev/null                 |
| Stop hook using only `systemMessage`           | User sees, Claude doesn't          | Use `additionalContext` for Claude context |

### Recommended Patterns

**PostToolUse: Emit feedback to Claude**

```bash
if [[ condition ]]; then
    jq -n --arg reason "[CATEGORY] Your message" '{decision: "block", reason: $reason}'
fi
exit 0
```

**Stop: Informational (allow stopping)**

```bash
if [[ "$INFO" != "" ]]; then
    # Use BOTH fields: additionalContext for Claude, systemMessage for user
    jq -n --arg msg "$INFO" '{additionalContext: $msg, systemMessage: $msg}'
fi
exit 0
```

**Stop: Blocking (force continuation)**

```bash
if [[ "$MUST_CONTINUE" == "true" ]] && [[ "$STOP_HOOK_ACTIVE" != "true" ]]; then
    jq -n --arg reason "Cannot stop: $REASON" '{decision: "block", reason: $reason}'
fi
exit 0
```

**PreToolUse: Block with reason**

```bash
if [[ dangerous_command ]]; then
    jq -n --arg reason "Blocked: $WHY" \
        '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: $reason}}'
fi
exit 0
```

### References

- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) - Official documentation
- [GitHub Issue #3983](https://github.com/anthropics/claude-code/issues/3983) - PostToolUse visibility confirmation
- [ADR: PostToolUse Hook Visibility](https://github.com/terrylica/cc-skills/blob/main/docs/adr/2025-12-17-posttooluse-hook-visibility.md) - Documented discovery

### Loop Prevention

When `stop_hook_active` is `true` in Stop/SubagentStop, a hook is already active. Check the transcript to prevent infinite loops.

### Stop Hook Schema (Critical - Verified 2025-12-18)

**CORRECT schema based on live testing:**

| Intent               | Correct Output                             | Wrong Output                              |
| -------------------- | ------------------------------------------ | ----------------------------------------- |
| **Allow stop**       | `{}` (empty object)                        | ~~`{"continue": false}`~~                 |
| **Continue session** | `{"decision": "block", "reason": "..."}`   | ~~`{"continue": true, "reason": "..."}`~~ |
| **Hard stop**        | `{"continue": false, "stopReason": "..."}` | (same)                                    |

**Key insight**: `{"continue": false}` means "HARD STOP Claude entirely" - it does NOT mean "allow normal stop". Using it incorrectly causes the confusing message:

```
Stop hook prevented continuation
```

This message appears because `continue: false` is an **active intervention** to halt Claude, not a passive "allow stop".

**Helper pattern for clarity:**

```python
def allow_stop(reason: str | None = None):
    """Allow session to stop normally."""
    print(json.dumps({}))  # Empty object = allow stop

def continue_session(reason: str):
    """Prevent stop and continue session."""
    print(json.dumps({"decision": "block", "reason": reason}))

def hard_stop(reason: str):
    """Hard stop Claude entirely (overrides everything)."""
    print(json.dumps({"continue": False, "stopReason": reason}))
```

### Common Pitfalls

| Pitfall                                  | Problem                                                 | Solution                                                                                                                                                                                         |
| ---------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Session-locked hooks**                 | Hook changes don't take effect                          | Hooks snapshot at session start. Run `/hooks` to apply pending changes OR restart Claude Code                                                                                                    |
| **Script not executable**                | Hook silently fails                                     | Run `chmod +x script.sh` on all hook scripts                                                                                                                                                     |
| **Non-zero exit codes**                  | Hook blocks Claude unexpectedly                         | Ensure scripts return 0 on success; non-zero = error                                                                                                                                             |
| **Missing file matchers**                | Hook doesn't trigger on edits                           | Use `Edit\|MultiEdit\|Write` to catch ALL file modifications                                                                                                                                     |
| **Case sensitivity**                     | Matcher doesn't match                                   | Matchers are case-sensitive: `Bash` ≠ `bash`                                                                                                                                                     |
| **Relative paths**                       | Script not found                                        | Use `$CLAUDE_PROJECT_DIR` or absolute paths                                                                                                                                                      |
| **Timeout too short**                    | Hook killed mid-execution                               | Default is 60s; increase for slow operations                                                                                                                                                     |
| **JSON syntax errors**                   | All hooks fail to load                                  | Validate with `cat settings.json \| python -m json.tool`                                                                                                                                         |
| **Stop hook wrong schema**               | "Stop hook prevented continuation"                      | Use `{}` to allow stop, NOT `{"continue": false}` (see Stop Hook Schema above)                                                                                                                   |
| **Local symlink caching**                | Edits to source not picked up                           | Release new version, `/plugin install`, restart Claude Code (see Plugin Cache section below)                                                                                                     |
| **Reading input from env vars**          | Hook receives empty input, silently fails               | Use `INPUT=$(cat)` + `jq` to parse stdin JSON (see Hook Input Delivery Mechanism above)                                                                                                          |
| **Using non-existent hook types**        | `"Invalid key in record"` error, settings.json rejected | Only use valid types: SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, Notification, SubagentStop, Stop, PreCompact, SessionEnd. **PostToolUseError does NOT exist.** |
| **Assuming PostToolUse fires on errors** | Hook never fires for failed commands                    | PostToolUse ONLY fires on successful tool completion. Use PreToolUse to prevent errors instead.                                                                                                  |
| **Trusting GitHub issues as features**   | Implement non-existent functionality                    | Issues are REQUESTS not implementations. Always verify against official Claude Code docs.                                                                                                        |

```{=latex}
\newpage
```

## Plugin Cache and Symlink Resolution (Lesson Learned 2025-12-21)

### Plugin Cache Structure

Plugins are stored in `~/.claude/plugins/cache/<marketplace>/<plugin-name>/`:

```
~/.claude/plugins/cache/cc-skills/ralph/
├── 5.15.0/              # Released version (immutable)
│   ├── commands/
│   └── hooks/
├── 5.16.0/              # Newer released version
│   ├── commands/
│   └── hooks/
└── local -> /path/to/source/repo/plugins/ralph   # Development symlink
```

### Critical Insight: Version vs Content Resolution

**Claude Code resolves version and content DIFFERENTLY:**

| What                | Resolution Source      | Example                            |
| ------------------- | ---------------------- | ---------------------------------- |
| **Version display** | `local` symlink first  | Banner shows `v5.15.0 (local)`     |
| **Skill content**   | VERSION DIRECTORY only | Executes code from `5.15.0/` cache |

**The local symlink is for version detection, NOT skill execution.**

This means:

- Editing source files does NOT affect running sessions
- Version banner shows `(local)` but code comes from version cache
- Your fix appears to be "in" but isn't being used

### Symptom: Fix Not Applied

```
========================================
  RALPH WIGGUM v5.15.0 (local)        <-- Version from local symlink
========================================

Adapter: universal                     <-- OLD CODE from 5.15.0 cache!
```

Even though the source file has the fix, Claude Code reads skill content from the cached version directory.

### Correct Update Workflow

1. **Edit source file** - `plugins/ralph/commands/start.md`
2. **Commit and push** - `git add . && git commit -m "fix: ..." && git push`
3. **Release new version** - `npm run release` (creates v5.16.0)
4. **Remove local symlink** (optional) - `rm ~/.claude/plugins/cache/cc-skills/ralph/local`
5. **Reinstall plugin** - `/plugin install cc-skills`
6. **Restart Claude Code** - Exit (Ctrl+C) and run `claude` again
7. **Verify** - Banner shows `v5.16.0 (cache)` not `(local)`

### Why Remove the Local Symlink?

The local symlink can cause confusing behavior:

| Symlink State | Version Banner    | Content Source | Confusion Level   |
| ------------- | ----------------- | -------------- | ----------------- |
| Present       | `v5.15.0 (local)` | `5.15.0/`      | HIGH - misleading |
| Removed       | `v5.16.0 (cache)` | `5.16.0/`      | LOW - accurate    |

When developing, the local symlink is useful for **version detection**. But for testing fixes, remove it to ensure you're using the released version.

### zsh Compatibility: Heredoc Wrapper Required

Skill markdown code blocks must use bash heredoc wrapper for zsh compatibility:

**Correct (works in zsh):**

```bash
/usr/bin/env bash << 'SCRIPT_NAME'
if [[ "$VAR" != "value" ]]; then
    echo "bash-specific syntax works"
fi
SCRIPT_NAME
```

**Incorrect (fails in zsh):**

```bash
/usr/bin/env bash << 'LIFECYCLE_REFERENCE_SCRIPT_EOF'
# Without heredoc, zsh interprets directly
if [[ "$VAR" != "value" ]]; then  # ERROR: condition expected: \!=
    echo "fails"
fi
LIFECYCLE_REFERENCE_SCRIPT_EOF
```

**Error signature:** `(eval):91: condition expected: \!=`

This happens when Claude Code strips the heredoc wrapper and zsh tries to interpret bash-specific `!=` in `[[ ]]`.

**Fix:** Always wrap skill bash code in heredoc per [ADR: Shell Command Portability](https://github.com/terrylica/cc-skills/blob/main/docs/adr/2025-12-06-shell-command-portability-zsh.md)

### Diagnostic Commands

```bash
# Check symlink status
ls -la ~/.claude/plugins/cache/cc-skills/<plugin>/local

# Verify version content
grep -A5 "PATTERN" ~/.claude/plugins/cache/cc-skills/<plugin>/<version>/commands/file.md

# Compare local vs version
diff <(cat ~/.../local/commands/file.md | grep "PATTERN") \
     <(cat ~/.../5.16.0/commands/file.md | grep "PATTERN")

# Remove local symlink for clean testing
rm ~/.claude/plugins/cache/cc-skills/<plugin>/local
```

### Quick Reference: Fix Not Working Checklist

- [ ] Fix is in source file? (`grep` the source)
- [ ] Fix is committed and pushed? (`git status`)
- [ ] New version released? (`git tag` shows new version)
- [ ] Local symlink removed? (`ls -la .../local`)
- [ ] Plugin reinstalled? (`/plugin install cc-skills`)
- [ ] Claude Code restarted? (Exit and re-enter)
- [ ] Banner shows new version + `(cache)`? (Not `(local)`)

### Debugging Techniques

| Technique                  | Command/Method                        | Use Case                                 |
| -------------------------- | ------------------------------------- | ---------------------------------------- |
| **Disable all hooks**      | `claude --no-hooks`                   | Recover from broken hook blocking Claude |
| **Interactive management** | `/hooks`                              | Review, edit, apply pending hook changes |
| **Capture hook input**     | `cat > /tmp/hook-input.json`          | Inspect JSON data passed to hooks        |
| **Check hook status**      | `/status`                             | View conversation stats and loaded hooks |
| **Validate JSON**          | `python -m json.tool < settings.json` | Find syntax errors in configuration      |
| **Test script manually**   | Run script in terminal                | Verify script works outside Claude       |
| **Check permissions**      | `ls -la script.sh`                    | Ensure executable bit is set             |

### Timeout Defaults

- **Command hooks**: 60 seconds (if not specified)
- **Prompt hooks**: 30 seconds (Haiku evaluation)
- **Recommended**: 180s for linting/testing operations

## Hook Configuration Example

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-write.py",
            "timeout": 30
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if the task is truly complete. If not, explain what remains.",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

## Hook Implementation Language Policy

**Preferred Language: TypeScript (Bun)**

Use TypeScript with Bun as the default choice for new hooks. Only use bash when there's a significant technical advantage.

### Decision Matrix

| Criteria                      | Bash              | TypeScript/Bun     | Winner     |
| ----------------------------- | ----------------- | ------------------ | ---------- |
| **Testability**               | Hard to unit test | Full test support  | TypeScript |
| **Type Safety**               | None              | Full inference     | TypeScript |
| **Error Handling**            | Fragile ($?)      | try/catch/finally  | TypeScript |
| **Complex Validation**        | Awkward           | Native             | TypeScript |
| **JSON Parsing**              | Requires jq       | Native             | TypeScript |
| **Async Operations**          | Subprocess spawns | Native async/await | TypeScript |
| **Large Reference Content**   | Heredocs messy    | Template literals  | TypeScript |
| **External API Calls**        | curl + jq         | fetch() native     | TypeScript |
| **Simple Pattern Match Only** | grep -E one-liner | Regex overkill     | **Bash**   |
| **System Command Wrappers**   | Natural fit       | subprocess call    | **Bash**   |
| **Zero Dependencies**         | Built-in          | Requires Bun       | **Bash**   |

### When to Use Bash

Only use bash scripts for hooks when:

1. **One-liner patterns** - Simple `grep -E` or `[[ ]]` checks with no complex logic
2. **System command wrappers** - Thin wrappers around git, shellcheck, or other CLI tools
3. **Legacy compatibility** - Maintaining existing bash hooks (but consider migration)
4. **Portability requirements** - Environments where Bun isn't available

### When to Use TypeScript (Default)

Use TypeScript/Bun for:

1. **Any validation with business logic** - Type checking, schema validation, complex rules
2. **Hooks that provide educational feedback** - Large reference material, formatted output
3. **Multi-step validation** - Multiple checks with aggregated results
4. **Hooks that call external APIs** - GitHub, Slack, webhooks
5. **New hooks** - Start with TypeScript unless bash has clear advantage

### Migration Path

Existing bash hooks with >50 lines or complex logic should be migrated to TypeScript:

1. Create `.ts` version following the TypeScript template below
2. Test both versions produce identical JSON output for same inputs
3. Replace settings.json reference
4. Archive bash version in `legacy/` directory

```{=latex}
\newpage
```

## Complete PreToolUse Hook Template (Bash)

Use this template ONLY for simple pattern matching hooks. For complex validation, use the TypeScript template instead.

```bash
#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# INPUT PARSING (Required - hooks receive JSON via stdin, NOT env vars)
# Reference: https://claude.com/blog/how-to-configure-hooks
# ============================================================================
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""' 2>/dev/null) || TOOL_NAME=""
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null) || COMMAND=""
CWD=$(echo "$INPUT" | jq -r '.cwd // ""' 2>/dev/null) || CWD=""

# ============================================================================
# TOOL TYPE CHECK (Optional - filter by tool)
# ============================================================================
if [[ "$TOOL_NAME" != "Bash" ]]; then
    exit 0  # Not our target tool
fi

# ============================================================================
# COMMAND PATTERN CHECK (Optional - filter by command content)
# ============================================================================
if ! echo "$COMMAND" | grep -qE 'your-pattern-here'; then
    exit 0  # Not a matching command
fi

# ============================================================================
# VALIDATION LOGIC
# ============================================================================
if [[ dangerous_condition ]]; then
    jq -n --arg reason "Blocked: explanation of why this is blocked" \
        '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: $reason}}'
    exit 0
fi

# ============================================================================
# ALLOW (Default - let the command proceed)
# ============================================================================
exit 0
```

**Key points:**

- `INPUT=$(cat)` reads JSON from stdin (NOT environment variables)
- `jq -r '.field // ""'` extracts fields with empty string fallback
- Exit 0 with JSON for soft block; exit 2 for hard block
- The template is safe to copy verbatim and customize

## Complete PreToolUse Hook Template (Bun/TypeScript) — PREFERRED

Use this template as the **default** for all new hooks. TypeScript provides type safety, testability, and cleaner error handling. See "Hook Implementation Language Policy" above.

```typescript
#!/usr/bin/env bun
/**
 * PreToolUse hook template - Bun/TypeScript version
 * More testable than bash; same lifecycle semantics.
 */

// ============================================================================
// TYPES
// ============================================================================

interface PreToolUseInput {
  tool_name: string;
  tool_input: {
    command?: string;
    file_path?: string;
    [key: string]: unknown;
  };
  tool_use_id?: string;
  cwd?: string;
}

interface HookResult {
  exitCode: number;
  stdout?: string;
  stderr?: string;
}

// ============================================================================
// OUTPUT FORMATTERS
// ============================================================================

function createBlockOutput(reason: string): string {
  return JSON.stringify(
    {
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: reason,
      },
    },
    null,
    2,
  );
}

// ============================================================================
// MAIN LOGIC - Pure function returning result (no process.exit in logic)
// ============================================================================

async function runHook(): Promise<HookResult> {
  // Read JSON from stdin
  const stdin = await Bun.stdin.text();
  if (!stdin.trim()) {
    return { exitCode: 0 }; // Empty stdin, allow through
  }

  let input: PreToolUseInput;
  try {
    input = JSON.parse(stdin);
  } catch (parseError: unknown) {
    const msg =
      parseError instanceof Error ? parseError.message : String(parseError);
    return {
      exitCode: 0,
      stderr: `[HOOK] JSON parse error (allowing through): ${msg}`,
    };
  }

  // TOOL TYPE CHECK - filter by tool
  if (input.tool_name !== "Bash") {
    return { exitCode: 0 }; // Not our target tool
  }

  const command = input.tool_input?.command || "";

  // COMMAND PATTERN CHECK - filter by command content
  if (!/your-pattern-here/.test(command)) {
    return { exitCode: 0 }; // Not a matching command
  }

  // VALIDATION LOGIC
  if (/* dangerous_condition */ false) {
    return {
      exitCode: 0,
      stdout: createBlockOutput("Blocked: explanation of why this is blocked"),
    };
  }

  // ALLOW - let the command proceed
  return { exitCode: 0 };
}

// ============================================================================
// ENTRY POINT - Single location for process.exit
// ============================================================================

async function main(): Promise<never> {
  let result: HookResult;

  try {
    result = await runHook();
  } catch (err: unknown) {
    // Unexpected error - log and allow through to avoid blocking on bugs
    console.error("[HOOK] Unexpected error:");
    if (err instanceof Error) {
      console.error(`  Message: ${err.message}`);
      console.error(`  Stack: ${err.stack}`);
    }
    return process.exit(0);
  }

  if (result.stderr) console.error(result.stderr);
  if (result.stdout) console.log(result.stdout);
  return process.exit(result.exitCode);
}

void main();
```

**Key points (TypeScript-specific):**

- `Bun.stdin.text()` reads JSON from stdin (equivalent to bash `cat`)
- Pure `runHook()` function returns `HookResult` - no `process.exit()` in logic
- Single `main()` entry point handles all `process.exit()` calls
- Structured error handling with full stack trace logging
- Type-safe interfaces prevent silent failures from typos
- Easier to unit test than bash scripts

**Note:** See the "Hook Implementation Language Policy" section above for the complete decision matrix on when to use TypeScript vs bash. TypeScript is the default choice for new hooks.

```{=latex}
\end{document}
```

---

## BUILD INSTRUCTIONS (Not printed in PDF)

This section is excluded from PDF output via `\end{document}` above.

### Required Files

All files must be in the same directory (`tmp/`):

1. `claude-code-hooks-lifecycle.md` — This source file
2. `header.tex` — LaTeX header for landscape pages
3. `table-spacing-template.tex` — Table row spacing

### header.tex

```latex
\usepackage{pdflscape}
```

### table-spacing-template.tex

```latex
\usepackage{array}
\renewcommand{\arraystretch}{1.3}
```

### Build Command

```bash
cd /Users/terryli/eon/alpha-forge/tmp

pandoc claude-code-hooks-lifecycle.md \
  -o claude-code-hooks-lifecycle.pdf \
  --pdf-engine=xelatex \
  -V documentclass=extarticle \
  -V geometry:margin=0.5in \
  -V mainfont="DejaVu Sans" \
  -V monofont="DejaVu Sans Mono" \
  -V fontsize=8pt \
  -H table-spacing-template.tex \
  -H header.tex
```

### Key Options Explained

| Option                          | Purpose                                                      |
| ------------------------------- | ------------------------------------------------------------ |
| `documentclass=extarticle`      | Enables 8pt font (standard article only supports 10/11/12pt) |
| `geometry:margin=0.5in`         | Narrow margins for more table space                          |
| `mainfont="DejaVu Sans"`        | Unicode support for box-drawing characters                   |
| `monofont="DejaVu Sans Mono"`   | Monospace font for code blocks                               |
| `fontsize=8pt`                  | Smaller font to fit wide tables                              |
| `-H header.tex`                 | Include pdflscape for landscape pages                        |
| `-H table-spacing-template.tex` | Increase table row spacing (1.3x)                            |

### Landscape Sections

Use these raw LaTeX blocks to switch orientation:

````markdown
```{=latex}
\begin{landscape}
```

... content in landscape ...

```{=latex}
\end{landscape}
```
````

### Page Breaks

````markdown
```{=latex}
\newpage
```
````

### Troubleshooting

| Issue                     | Solution                                             |
| ------------------------- | ---------------------------------------------------- |
| "File not found" for .tex | Ensure you're in the `tmp/` directory                |
| 8pt font not working      | Must use `documentclass=extarticle`                  |
| Box-drawing chars broken  | Use DejaVu Sans fonts (has Unicode support)          |
| Tables overlapping        | Put section in `\begin{landscape}...\end{landscape}` |
| Section separators        | Use `· · · · · · ·` rows between table sections      |
