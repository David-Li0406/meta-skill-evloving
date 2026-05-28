---
name: lessons-extractor
description: Extracts lessons learned from Claude Code session logs into organized markdown and JSONL files
argument-hint: "[--since <date>] [--output <dir>] [--log-glob <glob>]"
---

# lessons-extractor

Extract reusable lessons from Claude Code session logs.

## Usage

```
/lessons-extractor
/lessons-extractor --since 2026-01-01
/lessons-extractor --output docs/ai/custom/
/lessons-extractor --log-glob "~/.claude/projects/specific-hash/**/*.jsonl"
```

## Arguments

Access via `$ARGUMENTS`:
- `--since <date>` - Only process logs modified after this date (ISO format). Recommended to limit volume.
- `--output <dir>` - Output directory (default: `docs/ai/lessons-extractor/`)
- `--log-glob <glob>` - Custom glob pattern for logs (default: `~/.claude/projects/**/*.jsonl`)

## Configuration

If `config.json` exists in the skill directory, load settings from it. Otherwise use defaults.

Config file location: `.claude/skills/lessons-extractor/config.json` or `~/.claude/skills/lessons-extractor/config.json`

## Workflow

### Step 1: Locate Logs

Claude Code stores session logs at `~/.claude/projects/**/*.jsonl` (user home directory). Project directories are **encoded hashes**, not human-readable project names.

**If shell execution is permitted**, use command injection to find logs:

**macOS/Linux:**
```
!find ~/.claude/projects -name '*.jsonl' -type f | head -50
```

With date filter (last 7 days):
```
!find ~/.claude/projects -name '*.jsonl' -mtime -7 -type f
```

**Windows (PowerShell):**
```
!powershell -NoProfile -NonInteractive -Command "Get-ChildItem -Path '~\.claude\projects' -Filter *.jsonl -Recurse -File -ErrorAction SilentlyContinue | Where-Object FullName -NotMatch '\\subagents\\' | Sort-Object LastWriteTime -Descending | Select-Object -First 50 -ExpandProperty FullName"
```

**If shell execution is NOT permitted** (or user prefers manual):
- User provides `--log-glob` with specific path
- User pastes selected log excerpts directly into conversation

**Note:** To enable shell commands, users may need to allow them in Claude Code settings. See Claude Code docs on permissions.

**Fallback behavior (automatic):**
If log discovery fails (no files found, permission denied, or command error):
1. Report the failure clearly with the exact error
2. List which sources were attempted and what failed
3. **Automatically** proceed to git history analysis (do not require confirmation)
4. Include troubleshooting suggestions in output
5. **Always** show "Sources Used" footer in final output

To disable git fallback, user can pass `--no-git-fallback` (not yet implemented).

### Step 2: Read and Redact

For each log file, read contents and apply redaction patterns before processing.

**If file access is blocked** (logs outside repo), ask the user to paste relevant JSONL excerpts (already-redacted if possible) and continue from there.

Apply redaction to remove:
- API keys, tokens, passwords, secrets
- Absolute paths containing usernames
- Any patterns matching config redact rules

Use these default redaction patterns:
- `(?i)api[_-]?key` followed by values
- `(?i)password` followed by values
- `(?i)secret` followed by values
- `(?i)token` followed by values
- `/Users/<username>/` paths
- `/home/<username>/` paths
- `C:\Users\<username>\` paths

### Step 3: Summarize Sessions

For each session log, apply the summarize_run prompt:
- Identify: what task was attempted, what worked, what didn't
- Extract: key decisions, tool usage patterns, error recovery
- Note: any surprising behaviors or gotchas

### Step 4: Extract Lessons

Apply the extract_lessons prompt to summarized sessions:
- Identify reusable patterns and anti-patterns
- Categorize: workflow, debugging, architecture, tool-specific
- Rate confidence/applicability (0.0-1.0)
- Include concrete examples where helpful

### Step 5: Merge and Deduplicate

Apply the merge_dedupe prompt to consolidate lessons:
- Merge similar lessons into single entries
- Remove exact duplicates
- Organize by category
- Add cross-references between related lessons

### Step 6: Write Outputs

Write to output directory (default `docs/ai/lessons-extractor/`):

**docs/ai/lessons-extractor/lessons.md** - Human-readable:
```markdown
# Lessons Learned

Last updated: 2026-01-22

## Workflow
- Lesson 1...
- Lesson 2...

## Debugging
...
```

**docs/ai/lessons-extractor/lessons.jsonl** - Machine-readable:
```jsonl
{"id":"lesson-001","category":"workflow","title":"...","description":"...","confidence":0.9}
{"id":"lesson-002","category":"debugging","title":"...","description":"...","confidence":0.8}
```

**Required: Sources Used footer in lessons.md:**

Every output MUST include this footer at the end:

```markdown
---
## Sources Used
- Session logs: ✓ (12 files from ~/.claude/projects/)
- Git history: ✗ (not needed)
```

If session logs failed:

```markdown
---
## Sources Used
- Session logs: ✗ (discovery failed: [error message])
- Git history: ✓ (automatic fallback)

⚠️ Lessons quality may be reduced without session logs. See Troubleshooting section.
Suggested fix: [specific troubleshooting step based on error]
```

If both sources used:

```markdown
---
## Sources Used
- Session logs: ✓ (5 files, partial - some files unreadable)
- Git history: ✓ (supplemental)
```

## Important Notes

- **Never commit raw logs** - they may contain sensitive data
- **Review outputs before committing** - redaction is best-effort; `docs/ai/lessons-extractor/*` may still contain sensitive strings
- Logs are read from `~/.claude/projects/` by default (Claude Code's storage location)
- Log directories use encoded names (e.g., `c--Users-YourName-Projects-myrepo`), not human-readable project names
- Use `--since` to limit volume when processing many sessions

## Troubleshooting

### Windows: Commands return empty or wrong paths

If running from Git Bash or another shell that strips `$` characters:

**Symptom:** Command returns `:USERPROFILE\.claude\projects` or similar broken paths.

**Cause:** The outer shell (Git Bash/sh) interprets `$` before PowerShell receives it.

**Solution:** All Windows commands in this skill use `$`-free syntax. If you customized commands and they fail, ensure:
- Use `~` instead of `$env:USERPROFILE` or `$HOME`
- Use `Where-Object PropertyName -Operator Value` instead of `Where-Object { $_.Property }`
- Use `Select-Object -ExpandProperty Name` instead of `ForEach-Object { $_.Name }`
- Use `-NotMatch '\\subagents\\'` for path filtering (double-escaped backslashes for regex)

**Test your environment:**

```powershell
# Should output your user profile path (e.g., C:\Users\YourName)
!powershell -NoProfile -Command "Resolve-Path '~'"
```

### Log directory not found

Claude Code stores logs at `~/.claude/projects/` with encoded project directory names (e.g., `c--Users-YourName-Projects-myrepo` encoding, not human-readable project names).

**Verify the path exists:**

```bash
# macOS/Linux
ls -la ~/.claude/projects/
```

```powershell
# Windows (PowerShell)
!powershell -NoProfile -Command "Get-ChildItem '~\.claude\projects' -ErrorAction SilentlyContinue | Select-Object -First 5 Name"
```

### Permission errors reading logs

If logs are outside the repo, Claude Code may not have read permission. Options:
1. User pastes log excerpts directly into conversation
2. User provides `--log-glob` pointing to copied logs inside repo
