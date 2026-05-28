# Gemini Integration

How to invoke Gemini via copilot CLI for task implementation.

## Prompt Template

```
Task: {task.subject}

Description:
{task.description}

Acceptance Criteria:
{task.acceptance_criteria or "Complete the task as described"}

Context:
- Working directory: {cwd}
- Relevant files: {list files if known}

Instructions:
1. Read existing code before making changes
2. Follow existing patterns and conventions
3. Run tests if available
4. Keep changes minimal and focused
```

## Permission Modes

| Task type | Flags |
|-----------|-------|
| Analysis only | `-p "prompt"` (no extra flags) |
| Code changes | `--allow-all-tools -p "prompt"` |
| Full autonomy | `--allow-all -p "prompt"` or `--yolo -p "prompt"` |
| Specific dirs | `--add-dir <path> -p "prompt"` |

## Execution Modes

| Mode | Flag | Use case |
|------|------|----------|
| Non-interactive | `-p "prompt"` | Scripted execution, exits after completion |
| Interactive | `-i "prompt"` | Needs user input during execution |
| Silent | `-s -p "prompt"` | Clean output for parsing |

## Common Issues

### Session needs context

Gemini may need access to files outside the working directory.

**Fix**: Use `--add-dir <path>` to grant access to additional directories.

### Tool approval interrupts

Default mode prompts for tool approval.

**Fix**: Use `--allow-all-tools` for auto-approval, or `--allow-all` for full permissions.

### Wrong approach

Gemini took an unexpected direction.

**Fix**:
- Be more specific in prompt
- Add constraints: "Do NOT create new files" or "Use existing X pattern"
- Reference specific files: "Follow pattern in src/existing.ts"

### Resume needed

Incomplete work needs continuation.

**Fix**: Use `copilot --continue` to resume most recent session, or `copilot --resume` to pick a session.
