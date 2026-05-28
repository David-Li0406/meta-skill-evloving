# Error Handling

Error messages and recovery steps for common issues.

## Validation Errors

| Scenario | Error Message | Recovery |
|----------|---------------|----------|
| No frontmatter | `Error: Missing frontmatter in: <path>` | Add YAML frontmatter block with `---` markers |
| Missing type field | `Error: Missing 'type' field in frontmatter: <path>` | Add `type: transcription` to frontmatter |
| Wrong type | `Error: Expected type: transcription, found: <type> in <path>` | Use a transcription note, not a meeting/other note type |
| Missing date | `Error: Missing 'recorded' field and no --date provided` | Add `recorded: YYYY-MM-DDTHH:mm` to frontmatter OR use `--date` flag |

## VTT-Specific Errors

| Scenario | Error Message | Recovery |
|----------|---------------|----------|
| No date flag | `Error: VTT files require --date flag (file mtime is unreliable). Example: --date 2026-01-15T14:30:00` | Re-run with `--date` flag |
| Conversion failed | `Failed to convert VTT: <message>` | Check VTT file format is valid WebVTT |
| File not found | `Error: VTT file not found: <path>` | Check file path and permissions |

## Input Resolution Errors

| Scenario | Error Message | Recovery |
|----------|---------------|----------|
| No transcriptions in inbox | Prompts via `AskUserQuestion` | Provide a file path, or create a transcription first |
| File not found | `Error: File not found: <path>` | Check path spelling and location |
| Unsupported extension | `Error: Unsupported file type: <ext>. Expected .vtt or .md` | Use .vtt or .md files only |

## CLI Errors

| Scenario | Error Message | Recovery |
|----------|---------------|----------|
| Meeting template not found | `Error: Template 'meeting' not found` | Check vault Templates directory |
| Invalid meeting_type | CLI validation error | Use valid enum value (see meeting-types.md) |
| Commit failed | `Failed to commit: <message>` | Check git status, resolve conflicts |

## Recovery Pattern

When an error occurs:

1. **Report the error clearly** with the exact message
2. **Explain what went wrong** in plain terms
3. **Suggest the fix** — what the user should do
4. **Stop execution** — don't proceed with partial data

Example response:
```
Error: Missing 'recorded' field and no --date provided

The transcription note doesn't have a recorded datetime, and you didn't
provide a --date override. I need to know when this meeting happened.

Fix: Either add `recorded: 2026-01-15T10:30` to the note's frontmatter,
or re-run with: /meeting-from-transcription "note.md" --date 2026-01-15T10:30:00
```
