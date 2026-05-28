# How to Use memex-cli Skill

## When to Use This Skill

Use the `memex-cli` skill when you need to:

1. **Execute AI backend tasks** with Codex, Claude, or Gemini
2. **Resume interrupted runs** using run_id for continuity
3. **Stream outputs** in text or JSONL format for integration
4. **Run parallel tasks** with DAG dependencies
5. **Multi-file context** using glob patterns

## Quick Start

### Basic Task Execution

Ask Claude:
- "Run a Codex task to implement user authentication"
- "Execute a Gemini task to design UX mockups"
- "Resume the previous run and continue implementation"

Claude will generate the appropriate `memex-cli` command using stdin protocol.

### Example Requests

**Code Generation:**
> "Use memex-cli with Codex backend to implement a REST API for user management"

**Design Review:**
> "Run a Gemini task to review these UI mockups (attach files)"

**Resume Work:**
> "Resume run ID abc123 and continue from the previous context"

## Expected Workflow

1. **User describes task** in natural language
2. **Claude generates stdin protocol** with proper task structure
3. **Command executes** via memex-cli
4. **Output streams** in chosen format (text/JSONL)
5. **Results available** with run_id for resumption

## Common Patterns

### Single Backend Task

```
User: "Implement authentication using Codex"

Claude generates:
memex-cli run --stdin <<'EOF'
---TASK---
id: auth-20260109100000
backend: codex
workdir: ./project
---CONTENT---
实现用户认证模块
---END---
EOF
```

### Multi-Backend Workflow

```
User: "Design with Gemini, then implement with Codex"

Claude generates parallel or DAG tasks with dependencies
```

### Resume Previous Work

```
User: "Resume run abc123 and add error handling"

Claude uses:
memex-cli resume --run-id abc123 --stdin < continuation.md
```

## Integration Tips

- **File context**: Use `files:` parameter with glob patterns for multi-file tasks
- **Output parsing**: Use `--stream-format jsonl` for programmatic processing
- **Task dependencies**: Chain tasks with `dependencies:` for sequential execution
- **Model selection**: Specify `model:` for precise backend control

## Skill Scope

This skill handles:
- ✅ Command generation and stdin protocol formatting
- ✅ Backend selection (codex, claude, gemini)
- ✅ Parameter configuration (model, timeout, retry)
- ✅ Output format selection (text, JSONL)
- ✅ Resume logic with run_id

This skill does NOT handle:
- ❌ memex-cli installation or configuration
- ❌ API key management
- ❌ Direct AI model interaction (delegated to memex-cli)

## Troubleshooting

**Issue**: "memex-cli command not found"
- Ensure memex-cli is installed: `npm install -g memex-cli`

**Issue**: "Backend authentication failed"
- Check API keys are configured in memex-cli

**Issue**: "Resume failed with unknown run_id"
- Verify run_id from previous execution output

## Additional Resources

- Full command reference: See SKILL.md
- Backend documentation: memex-cli official docs
- JSONL event types: See "Output Formats" section in SKILL.md
