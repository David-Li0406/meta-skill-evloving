---
name: context-writes
description: writes the current context to the ".claude/context" directory.
  ONLY use this after `/compact` has been executed.
allowed-tools: Bash(git rev-parse:--show-toplevel), Read, Write
argument-hint: [filename.md]
---

# /context-writes

Write the current context to ".claude/context" directory at git repository root.
Use this to preserve context for future sessions.

## Arguments

- `$ARGUMENTS` (optional): Filename for the summary (basename only)
  - Default: `{git-root-basename}_context_{YYYY-MM-DDTZH:M:S}.md`
  - Example: "auth_refactor.md"
  - Must end with ".md" extension
  - Must not contain *any* path separators

## Workflow

### 1. Find repository root

   ```bash
   git rev-parse --show-toplevel
   ```

   If command fails: report "Not a git repository" and exit

### 2. Derive filename

- If `$ARGUMENTS` provided:
  - Validate: reject if contains *any* path separators
  - Validate: reject if doesn't end with ".md"
  - Use sanitized basename: `basename "$ARGUMENTS"`

- If not provided:

   ```bash
   git_basename=$(basename "$repo_root")
   today=$(date +%Y-%m-%d%Z%T)
   filename="${git_basename}_context_${today}.md"
   ```

### 3. Set target path

   ```bash
   target_dir="${repo_root}/.claude/context"
   target_path="${target_dir}/${filename}"
   ```

### 4. Check for conflicts

If file exists at "$target_path":

- Ask user: "File exists at '.claude/context/${filename}'. Overwrite? (yes/no)"
- Wait for response
- If not "yes": stop execution

### 5. Ensure directory exists

```bash
mkdir -p "$target_dir"
```

### 6. Write file

Write the generated content to "$target_path".

If write fails: Report "Cannot write to $target_path" with error details and
stop execution.

### 7. Confirm success

Report exactly:

   ```text
   Context written to "{absolute_path}"
   ({file_size} bytes)
   ```

## Success Criteria

- File created at "{repo_root}/.claude/context/{filename}"
- File size > 100 bytes (validates content was written)
- Content is valid markdown
- User receives confirmation with absolute path

## Example Usage

```text
/context-writes
→ Context written to "/home/user/myproject/.claude/context/myproject_context_2025-10-23.md"

/context-writes refactor_session.md
→ File exists at ".claude/context/refactor_session.md". Overwrite? (yes/no)
→ Context written to "/home/user/myproject/.claude/context/refactor_session.md"
  (3124 bytes)

/context-writes ../escape.md
→ Error: Invalid filename (contains path separators)

/context-writes .hidden.md
→ Error: Invalid filename (hidden files not allowed)

/context-writes notes.txt
→ Error: Invalid filename (must end with .md)
```

## Error Handling

- **Not a git repository**: Report error, do not attempt write
- **Invalid filename** (contains `/` or `..`): Reject immediately
- **Write fails**: Report error with path and system message
- **Directory creation fails**: Report error with attempted path and system message
- **User declines overwrite**: Stop execution silently
