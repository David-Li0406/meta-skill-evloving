# Codex Integration

How to invoke Codex effectively for task implementation.

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

## Model Selection

| Task complexity | Model |
|-----------------|-------|
| Simple fix, single file | `o4-mini` |
| Standard feature | `o3` |
| Complex logic, multi-file | `o3` |
| Architectural changes | `o3` |

## Sandbox Modes

| Task type | Sandbox |
|-----------|---------|
| Analysis only | `read-only` |
| Code changes | `workspace-write` |
| Needs network (npm install, etc) | `danger-full-access` |

## Common Issues

### Timeout

Codex has a context/time limit. Signs of timeout:
- Incomplete changes
- Missing files mentioned in plan
- Abrupt stop mid-implementation

**Fix**: Split task into smaller pieces.

### Context exceeded

Large codebases may exceed context window.

**Fix**:
- Specify exact files to work with
- Split into file-specific tasks
- Use `-C <DIR>` to narrow scope

### Wrong approach

Codex took an unexpected direction.

**Fix**:
- Be more specific in prompt
- Add constraints: "Do NOT create new files" or "Use existing X pattern"
- Reference specific files: "Follow pattern in src/existing.ts"
