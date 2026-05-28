---
name: audit-claude-md
description: Audit if CLAUDE.md and AGENTS.md follow best practices from humanlayer.dev blog. Use when (1) user wants to validate their documentation structure, (2) user invokes /audit-claude-md command, (3) user asks to audit or split CLAUDE.md files. Triggers on "audit claude.md", "split claude.md", "audit agents.md", "split agents.md", "validate documentation".
---

# Audit CLAUDE.md Skill

Goal: Audit CLAUDE.md and AGENTS.md files to ensure they follow best practices, and optionally help split monolithic files into smaller, focused files.

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

# Argument Parsing

Parse the following optional flags from $ARGUMENTS:

- `--check` or `-c`: Only validate files without suggesting changes
- `--split` or `-s`: Automatically split CLAUDE.md into smaller files

Examples:
- `/audit-claude-md` - Audit and suggest improvements
- `/audit-claude-md --check` - Only validate structure
- `/audit-claude-md --split` - Split into smaller files (will prompt for directory)

Any remaining text after flags is treated as additional context for the analysis.

# Configuration

## Step 0: Load Configuration

The PostToolUse hook **injects validated config into your context** via `additionalContext`. The config summary looks like:

```
Auto-split enabled: true/false
Check only: true/false
Best practices reference: <url>
```

**DISPLAY REQUIREMENT:** When you receive the injected config, you MUST immediately display it to the user with this format:

**Active Audit Config:**
```
<paste the exact config here>
```

This gives users visibility into their active configuration before proceeding. If no config appears, use default values.

**Config structure:**
```yaml
validation:
  checkOnly: false  # Only validate without suggesting changes
  autoSplit: false  # Automatically split files without confirmation

bestPractices:
  referenceUrl: https://humanlayer.dev/blog/best-practices  # Reference documentation
  maxFileSize: 500  # Max recommended file size in lines

files:
  claudeMd: CLAUDE.md  # Path to CLAUDE.md
  agentsMd: AGENTS.md  # Path to AGENTS.md
```

**Behavior based on config:**
- If `validation.checkOnly: true` - Skip splitting suggestions, only report issues
- If `validation.autoSplit: true` - Automatically split without confirmation
- If `bestPractices.maxFileSize` defined - Use this threshold for split recommendations
- If config file is missing - Use defaults (checkOnly: false, autoSplit: false)

**Override rules:**
- Command-line flags (`--check`, `--split`) always override config
- Config overrides defaults
- Defaults are: checkOnly: false, autoSplit: false

# Execution steps:

## Step 1: Analyze Current Structure

- Check if CLAUDE.md exists in the project root
- Check if AGENTS.md exists in the project root
- Read both files to understand current structure
- If neither file exists, inform the user and offer to create templates

## Step 2: Validate Against Best Practices

**Check CLAUDE.md for:**
- File size (warn if > maxFileSize lines from config)
- Clear section structure with headers
- Proper markdown formatting
- Separation of concerns (architecture, development, commits, etc.)
- Reference to external documentation when appropriate

**Check AGENTS.md for:**
- Proper agent definitions
- Clear responsibilities
- Tool access specifications
- Trigger conditions

**Common issues to check:**
- Monolithic files with multiple concerns
- Missing headers or poor organization
- Outdated or conflicting information
- Lack of separation between project docs and agent configs

## Step 3: Generate Report

Present findings in a structured format:

```
CLAUDE.md Analysis:
- File size: X lines (threshold: Y lines)
- Issues found:
  • Issue 1 description
  • Issue 2 description
- Suggestions:
  • Suggestion 1
  • Suggestion 2

AGENTS.md Analysis:
- [Similar format]
```

**If `--check` flag or `validation.checkOnly: true`:**
- Stop here and present the report
- Do not suggest splitting or modifications

## Step 4: Suggest Improvements

**If files have issues, suggest one or more actions:**

1. **Split monolithic CLAUDE.md** - Break into focused files:
   - `architecture.md` - System design and structure
   - `development.md` - Development guidelines
   - `commits.md` - Commit message conventions
   - `testing.md` - Testing guidelines
   - etc.

2. **Reorganize sections** - Better header structure

3. **Extract to AGENTS.md** - Move agent-specific config

**Use AskUserQuestion to present options:**
- "Split CLAUDE.md into focused files (recommended)"
- "Reorganize sections within current files"
- "Generate best practices template"
- "No changes needed"

## Step 5: Execute Improvements

**If user chooses to split files:**

1. Always ask the user which output directory should be used (e.g., `.claude/docs`, `docs/claude`, etc.)
2. Create the output directory specified by the user
3. **Check for existing files in the output directory:**
   - List all markdown files that would be created by the split operation
   - For EACH existing file, use AskUserQuestion to ask what to do:
     - **Merge (recommended)**: Combine existing content with new content from CLAUDE.md
     - **Overwrite**: Replace the existing file entirely with content from CLAUDE.md
     - **Keep**: Skip this file, leave the existing content unchanged
     - **Keep both**: Keep existing file and create new file with suffix (e.g., `architecture-new.md`)
   - Track the decision for each file to apply later
4. Parse CLAUDE.md into logical sections
5. Write each section to appropriate file in output directory:
   - **If "Merge"**: Read existing file, intelligently combine with new content (avoid duplication, preserve unique sections)
   - **If "Overwrite"**: Replace file content entirely
   - **If "Keep"**: Skip writing this file
   - **If "Keep both"**: Write new content to filename with `-new` suffix (e.g., `architecture-new.md`)
6. Create a new minimal CLAUDE.md that references the split files
7. Update any necessary imports or references

**Directory structure after split:**
```
.claude/
  docs/              # User-specified directory
    architecture.md
    development.md
    commits.md
    testing.md
CLAUDE.md            # Minimal file with references
AGENTS.md            # Agent configurations
```

**If `validation.autoSplit: true` or `--split` flag:**
- Still ask for output directory first
- Execute split automatically after directory is provided
- Show summary of files created

## Step 6: Verify and Report

After making changes:
1. Verify all files were created successfully
2. Show summary of changes made
3. Provide next steps (e.g., "Review the split files and commit when ready")

# Best Practices Reference

Reference the humanlayer.dev blog post on best practices:
- Keep CLAUDE.md focused on high-level project context
- Use AGENTS.md for agent-specific configurations
- Split complex documentation into focused files
- Use clear headers and organization
- Keep files under recommended size threshold
- Use markdown properly for formatting

# Error Handling

If errors occur during file operations:
- Clearly report what failed
- Suggest corrective actions
- Do not leave the project in a broken state
- Offer to rollback changes if needed
