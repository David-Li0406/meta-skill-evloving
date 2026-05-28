---
name: chezmoi
description: This skill should be used whenever the user mentions "chezmoi" in any way. Manages dotfiles with chezmoi including tracking config files, comparing dotfiles, checking status, working with chezmoi templates, and handling local file changes. CRITICAL SAFETY RULES ENFORCED.
---

# Chezmoi Dotfiles Management

## When to Use
Use this skill when the user needs to:
- Track configuration file changes with chezmoi
- Compare local files with chezmoi-managed versions
- Check chezmoi status or differences
- Work with chezmoi templates (.tmpl files)
- Update dotfiles repository

## CRITICAL SAFETY RULES

⚠️ **NEVER use these dangerous commands:**
- `chezmoi apply` - Overwrites local changes with stored config (destructive!)
- `chezmoi apply --force` - Bypasses safety checks
- Any command with `--force` flag

✅ **Safe workflow:**
- `chezmoi add <file>` - Add local changes TO chezmoi tracking
- `chezmoi diff` - Compare tracked config with local files
- `chezmoi status` - Show files needing updates

## Common Commands

### Track Local Changes
```bash
chezmoi add ~/.config/hypr/hyprland.conf
```
This saves the current local file to chezmoi's source directory.

### Check What Changed
```bash
chezmoi diff
```
Shows differences between chezmoi's tracked version and local files.

### Check Status
```bash
chezmoi status
```
Lists files that differ between chezmoi source and local system.

### Test Template Rendering
```bash
chezmoi execute-template < ~/.local/share/chezmoi/dot_config/example.conf.tmpl
```
Previews how a template will render without applying it.

### Source Directory Location
Chezmoi source files are stored in `~/.local/share/chezmoi/`
- `dot_*` files become `.*` in home directory
- `.tmpl` files are processed as Go templates

## Workflow Pattern

1. **User edits local config file** (e.g., `~/.bashrc`)
2. **Add changes to chezmoi:** `chezmoi add ~/.bashrc`
3. **Verify with diff:** `chezmoi diff` (optional)
4. **Commit changes:** Standard git operations in `~/.local/share/chezmoi/`

## Handling Local Changes to Template Files

When a user reports that their local file has changes that differ from the chezmoi template:

### Critical Understanding
The user has ALREADY made changes to their local file and wants the template updated to MATCH those changes. Do NOT suggest applying the template to overwrite their local changes.

**CRITICAL - Template Conditionals:**
- **NEVER remove template conditionals** (e.g., `{{ if .is_work }}...{{ end }}`) from .tmpl files unless EXPLICITLY requested
- Template conditionals exist for environment-specific logic and should be preserved
- When updating templates to match local changes, preserve all existing conditionals and template variables
- If the local file differs from the template due to conditional logic, the LOCAL file should be updated to match the template logic, NOT the other way around
- Only when the user explicitly says to remove or modify conditionals should they be changed

### Step-by-Step Process

1. **Identify the exact local changes:**
   ```bash
   chezmoi diff ~/.config/path/to/file
   ```
   This shows the difference between what chezmoi would generate vs what exists locally.

   **CRITICAL - Understanding chezmoi diff output:**

   Chezmoi diff compares two things:
   - **SOURCE**: What chezmoi has tracked in `~/.local/share/chezmoi/` (the "source state")
   - **TARGET**: What actually exists in your home directory (the "destination state")

   The diff format shows:
   - Lines with `-` prefix: Content that exists in chezmoi's SOURCE (would be written to target)
   - Lines with `+` prefix: Content that exists in the TARGET (actual local file)

   **Common scenario**: User edits local file, hasn't run `chezmoi add` yet
   - Lines with `-` = old content still in chezmoi source
   - Lines with `+` = new content in local file that needs to be saved
   - **Action needed**: Run `chezmoi add` or manually edit the source file to match the `+` lines

   **Opposite scenario**: User pulled changes from git, hasn't applied them yet
   - Lines with `-` = new content in chezmoi source
   - Lines with `+` = old content in local file
   - **Action needed**: Run `chezmoi apply` (but ONLY if you want to overwrite local changes!)

   **Critical**: The `-`/`+` symbols show LOCATION (source vs target), NOT time (old vs new). Always check timestamps to determine which direction to sync.

2. **Find the template source file:**
   ```bash
   chezmoi source-path ~/.config/path/to/file
   ```
   This returns the path to the `.tmpl` file (e.g., `~/.local/share/chezmoi/dot_config/path/to/file.tmpl`)

3. **Check modification timestamps to determine which is newer:**
   ```bash
   stat -c '%y %n' ~/.config/path/to/file && chezmoi source-path ~/.config/path/to/file | xargs stat -c '%y %n'
   ```
   This shows the modification times of both files. The newer file typically represents the user's intended state.
   - If local file is newer: User likely made intentional changes to be saved to the template
   - If template is newer: Template may have been updated from another machine or git pull
   - Present this information to help guide the decision

4. **Read both files to understand the exact difference:**
   - Read the template file directly to see its current content
   - Use `cat -A` or `od -c` to reveal hidden characters (trailing spaces, tabs, etc.)
   - Compare line-by-line, character-by-character if needed

5. **Confirm with user if needed:**
   - If timestamps are ambiguous or the change is significant, present the timestamp information and ask which direction to sync
   - Most commonly, the local file is newer and should be saved to the template

6. **Use `chezmoi add` for non-template files:**
   - If the file is NOT a `.tmpl` file and local is newer, use `chezmoi add <file>` to save local changes to the template
   - Example: `chezmoi add ~/.bashrc`
   - This is the preferred method for simple files

7. **For template files, update manually:**
   - **ALWAYS check the render first** using `chezmoi execute-template` or by reading the template to see what conditionals and variables exist
   - Edit the template file directly using the Edit tool
   - Pay attention to:
     - Template conditionals (`{{ if }}`, `{{ range }}`, etc.) - preserve these unless explicitly asked to change
     - Template variables (`{{ .chezmoi.username }}`, etc.) - preserve these
     - Commented vs uncommented lines
     - Trailing whitespace (spaces, tabs)
     - Line endings
     - Exact character positions

8. **Verify the fix:**
   ```bash
   chezmoi diff ~/.config/path/to/file
   ```
   This should show NO diff if the template was updated correctly.

### Common Pitfalls

- **Removing template conditionals**: NEVER remove `{{ if }}...{{ end }}` blocks or other template logic unless explicitly requested. These conditionals exist for environment-specific configuration and should be preserved.
- **Not checking render before editing**: Always read the template file first to identify what conditionals and variables exist before making changes.
- **Confusing diff symbols with chronology**: The `-` and `+` symbols show SOURCE (template vs local), NOT time (old vs new). Use timestamps to determine which change is newer.
- **Reading files instead of diff**: Always read BOTH the template file AND the local file directly to verify their actual content. Don't rely solely on diff interpretation.
- **Describing changes backwards**: When describing what will happen, be clear about the direction. DON'T say "The local file has X changes" when you mean "The template will be updated with X changes from the local file." The local file ALREADY HAS the changes; they are being SAVED TO the template.
- **Invisible whitespace**: Trailing spaces are significant. Use `cat -A` or `od -c` to see them.
- **Assuming templates need git commits**: Templates are read from the filesystem, not git HEAD. Changes take effect immediately without committing.
- **Swapping logic**: If local file has line A active and line B commented, the template must also have line A active and line B commented.

### Example Scenario

User says: "My local monitors.conf has changes"

**Correct approach:**
1. Run `chezmoi diff ~/.config/hypr/configs/monitors.conf`
2. Read the diff carefully - the `+` lines show what the local file contains
3. Find the template: `chezmoi source-path ~/.config/hypr/configs/monitors.conf`
4. Edit the template to match the local file (the `+` lines from the diff)
5. Verify with `chezmoi diff` - should show no differences

**Incorrect approach:**
- Suggesting `chezmoi apply` to overwrite local changes
- Misreading the diff and updating the template backwards
- Ignoring whitespace differences
- Claiming the template is correct when a diff still exists

## Template Variables

Access chezmoi data in templates:
```
{{ .chezmoi.hostname }}
{{ .chezmoi.os }}
{{ .chezmoi.username }}
```

## Error Handling

If chezmoi commands fail:
- Check if file is tracked: `chezmoi managed | grep filename`
- Verify source directory: `ls ~/.local/share/chezmoi/`
- Check for template errors: `chezmoi execute-template` on specific file

## When NOT to Use Chezmoi

Do not use chezmoi commands for:
- Files not in the dotfiles repository
- Temporary files or caches
- Files with secrets (use chezmoi's encrypted files feature instead)
