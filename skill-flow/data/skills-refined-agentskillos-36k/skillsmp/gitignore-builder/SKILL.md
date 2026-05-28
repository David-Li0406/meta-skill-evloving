---
name: gitignore-builder
description: This skill should be used when the user asks to "create gitignore", "build .gitignore", "add gitignore templates", requests "/gitignore", or when observing projects without .gitignore or seeing untracked files like node_modules/ or .env in git status. Builds and merges .gitignore files using github/gitignore templates.
---

# Gitignore Builder

Build and merge `.gitignore` files using templates from [github/gitignore](https://github.com/github/gitignore) with smart project detection.

## When to Use

Invoke this skill when:

- User explicitly requests `/gitignore` or asks to create/update a `.gitignore`
- Detecting `git init` or a newly cloned repo without `.gitignore`
- User mentions ignoring files, not wanting to track certain files
- Observing `git status` output with files that should typically be ignored (e.g., `node_modules/`, `.env`, `__pycache__/`, `*.log`)

## Workflow

### Step 1: Determine Target Location

1. Find the nearest `.git` directory to determine repo root
2. If no `.git` found, ask user if they want to create a global gitignore at `~`

**Location Rules:**

| Situation | Action |
|-----------|--------|
| Inside a repo, project-level requested | Use repo root (where `.git` is) |
| Inside a repo, global requested | Warn: "Global gitignore is recommended at `~/.gitignore`. You're currently inside a repo. Proceed here anyway?" |
| Not in a repo | Suggest creating global gitignore at `~/.gitignore` |

### Step 2: Detect Project Type

**For project-level gitignore (basic detection):**

| Indicator File | Template |
|----------------|----------|
| `package.json` | Node.gitignore |
| `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile` | Python.gitignore |
| `Cargo.toml` | Rust.gitignore |
| `go.mod` | Go.gitignore |
| `composer.json` | Composer.gitignore |
| `Gemfile` | Ruby.gitignore |
| `pom.xml` | Maven.gitignore |
| `build.gradle`, `build.gradle.kts` | Gradle.gitignore |
| `*.swift`, `Package.swift` | Swift.gitignore |
| `*.csproj`, `*.sln` | VisualStudio.gitignore |
| `CMakeLists.txt` | CMake.gitignore |
| `Makefile` with C/C++ files | C.gitignore or C++.gitignore |

**For global gitignore (environment-aware detection):**

| Detection Method | Template (from Global/) |
|------------------|-------------------------|
| `uname` = Darwin | macOS.gitignore |
| `uname` = Linux | Linux.gitignore |
| Windows environment | Windows.gitignore |
| `.vscode/` exists or `code` command available | VisualStudioCode.gitignore |
| `.idea/` exists | JetBrains.gitignore |
| `vim` or `nvim` available | Vim.gitignore |
| `emacs` available | Emacs.gitignore |

### Step 3: Present Recommendations

Show detected templates and ask for confirmation:

```
Detected project root: /path/to/repo
Found indicators: package.json, .vscode/

Recommended templates:
- Node.gitignore
- VisualStudioCode.gitignore (for global)

Proceed with these templates? [Y/n/edit]
```

Allow user to:
- Confirm (Y)
- Cancel (n)
- Edit the list (add/remove templates)

### Step 4: Fetch and Merge

Use the `merge-gitignore.sh` script located at `${CLAUDE_PLUGIN_ROOT}/scripts/merge-gitignore.sh`:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/merge-gitignore.sh" Node Python macOS
```

**Merge Order (later entries have higher priority in gitignore):**

1. **Templates section** - github/gitignore templates with START/END markers (easiest to replace/update)
2. **Local files section** - Project-specific ignores
3. **Overrides section** - Custom overrides with highest priority (last wins in gitignore)

### Step 5: Handle EOL Conflicts

If the script detects mixed line endings:

```
⚠️ EOL inconsistency detected:
  - Node.gitignore: LF
  - VisualStudio.gitignore: CRLF
  - Existing .gitignore: LF

Choose unified format:
1. LF (Unix/macOS) - recommended
2. CRLF (Windows)
3. Keep as-is (no conversion)
```

Wait for user confirmation before proceeding.

### Step 6: Show Diff Preview

If target `.gitignore` already exists, show a diff:

```diff
📄 Will write to: /path/to/repo/.gitignore

--- Existing content
+++ Merged content

@@ -1,5 +1,60 @@
+# ╔═══════════════════════════════════════════════════════════════════════╗
+# ║ START - github/gitignore templates                                    ║
+# ╚═══════════════════════════════════════════════════════════════════════╝
+
+# --------------------------------------------
+# Source: Node.gitignore
+# --------------------------------------------
+node_modules/
+...
+
+# ╔═══════════════════════════════════════════════════════════════════════╗
+# ║ END - github/gitignore templates                                      ║
+# ╚═══════════════════════════════════════════════════════════════════════╝
+
+# ============================================
+# Local files (project-specific ignores)
+# ============================================
+
+# ============================================
+# Overrides (highest priority - last wins)
+# ============================================
+
 # User custom rules
 my-custom-file.txt

Confirm write? [Y/n]
```

### Step 7: Write File

After user confirms, write the file and report success:

```
✅ Created /path/to/repo/.gitignore (150 lines, 3 templates merged)
```

## Important Notes

### Always Recommend *.local Pattern

At the end of every gitignore generation, suggest:

```
💡 Tip: Consider adding these patterns for local configuration files:
   *.local
   *.local.*

These patterns prevent accidentally committing local overrides.
```

### Gitignore Syntax Reminders

When discussing or modifying gitignore:

- **Negation**: The exclamation mark prefix negates a pattern, re-including previously excluded files. Order is important: the negation must come after the exclusion. Example: `!important.log` re-includes `important.log`.
- **Order matters**: Later patterns override earlier ones.
- **Comments**: Lines starting with `#` are comments.
- **Directory**: Trailing `/` matches only directories (e.g., `build/`).
- **Wildcards**: `*` matches anything except `/`, `**` matches everything including `/`.

### Source Attribution & Structure

Templates section must be wrapped with START/END markers:

```gitignore
# ╔═══════════════════════════════════════════════════════════════════════╗
# ║                    github/gitignore templates                         ║
# ║           https://github.com/github/gitignore                         ║
# ╠═══════════════════════════════════════════════════════════════════════╣
# ║ START - Do not edit this section manually                             ║
# ╚═══════════════════════════════════════════════════════════════════════╝

# --------------------------------------------
# Source: Node.gitignore
# --------------------------------------------
node_modules/
...

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║ END - github/gitignore templates                                      ║
# ╚═══════════════════════════════════════════════════════════════════════╝
```

This makes it easy to:
- Identify template content for updates (replace between START/END)
- Understand where each rule comes from
- Avoid accidental edits to generated content

### Preserve User Content

If merging with an existing `.gitignore`, preserve user-added content in the appropriate section:

```gitignore
# ╔═══════════════════════════════════════════════════════════════════════╗
# ║ START - github/gitignore templates                                    ║
# ╚═══════════════════════════════════════════════════════════════════════╝

# --------------------------------------------
# Source: Node.gitignore
# --------------------------------------------
node_modules/
...

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║ END - github/gitignore templates                                      ║
# ╚═══════════════════════════════════════════════════════════════════════╝

# ============================================
# Local files (project-specific ignores)
# ============================================

secret-folder/
local-config.json

# ============================================
# Overrides (highest priority - last wins)
# ============================================

# User custom rules (preserved from original)
my-custom-rule.txt
!important.log
```

## Reference Files

- **[examples.md](references/examples.md)** - Detailed workflow examples for various scenarios

## Script Reference

The `merge-gitignore.sh` script handles:

1. Fetching templates from github/gitignore via raw.githubusercontent.com
2. Detecting and reporting EOL inconsistencies
3. Concatenating templates with source attribution
4. Outputting to stdout for preview/confirmation workflow

**Usage:**

```bash
# Fetch and merge templates
"${CLAUDE_PLUGIN_ROOT}/scripts/merge-gitignore.sh" <template1> [template2] ...

# Templates can be:
# - Top-level: Node, Python, Rust, Go, etc.
# - Global: Global/macOS, Global/VisualStudioCode, etc.
```

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Network error (failed to fetch) |
| 2 | EOL conflict detected (info in stderr) |
