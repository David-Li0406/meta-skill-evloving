---
name: check-links
description: This skill should be used when the user asks to "check internal links", "validate relative paths", "find broken file references", "audit documentation links", or wants to ensure all relative paths and anchors in documentation are valid. This is for internal links only, not external URLs.
---

# /check-links

Validate internal URLs and relative paths across the repository to ensure all links are valid and maintained.

## Instructions

1. **Scan for files containing links**:
   - Search all markdown files (`**/*.md`)
   - Optionally include other file types if specified (`.rst`, `.txt`, source code comments)

2. **Extract internal links** using these patterns:
   - Markdown links: `[text](relative/path.md)`
   - Markdown references: `[text]: relative/path.md`
   - Image links: `![alt](relative/path.png)`
   - HTML links: `<a href="relative/path">`
   - Anchor links: `[text](#heading)` (validate heading exists)

   **Exclude from validation:**
   - External URLs (starting with `http://`, `https://`, `mailto:`, etc.)
   - Template placeholders (containing `{{`, `${`, etc.)

3. **Validate each link**:
   - Check if the target file/directory exists
   - For anchor links (`#heading`), verify the heading exists in the target file
   - For links to specific line numbers (`file.py:42`), verify the file has that many lines
   - Resolve paths relative to the file containing the link

4. **Report findings**:

   **Summary:**

   ```
   Files scanned: X
   Links found: Y
   Valid: Z
   Broken: N
   ```

   **Broken Links:** (grouped by source file)

   ```
   src/README.md:
     - Line 15: [docs](./missing-file.md) → File not found
     - Line 42: [API](#api-reference) → Heading not found

   docs/guide.md:
     - Line 8: [config](../config.yaml) → File not found
   ```

   **Valid Links:** (only if verbose mode requested)
   - List all validated links

5. **Provide fix suggestions**:
   - For each broken link, suggest possible corrections:
     - Similar file names that exist (fuzzy match)
     - Files that were recently renamed (check git history)
     - Correct relative path if the file exists elsewhere

## Modes

### Check Mode (default)

```
/check-links
/check-links docs/
```

Validate all links and report issues without making changes.

### Fix Mode

```
/check-links --fix
```

Interactively offer to fix broken links:

1. Show each broken link
2. Suggest possible replacements
3. Ask for confirmation before updating

### Watch Mode (for file moves)

```
/check-links --update old/path.md new/path.md
```

When a file is moved/renamed, find and update all links pointing to it:

1. Search for all references to the old path
2. Show files that will be updated
3. Replace old paths with new paths

## Common Patterns to Validate

| Link Type     | Pattern           | Validation                  |
| ------------- | ----------------- | --------------------------- |
| Relative file | `./file.md`       | File exists                 |
| Parent dir    | `../file.md`      | File exists                 |
| Repo root     | `/docs/file.md`   | File exists from repo root  |
| Directory     | `./folder/`       | Directory exists            |
| Anchor        | `#heading`        | Heading exists in same file |
| File + anchor | `file.md#heading` | File and heading exist      |
| Image         | `![](./img.png)`  | Image file exists           |

## Integration with Git

When run without arguments, prefer checking:

1. Files changed in current branch (vs main)
2. Staged files
3. All files (if no changes detected)

This helps catch broken links before commits.
