---
name: plugin-validation-and-optimization
description: Use this skill when you need to validate and optimize a plugin's structure and quality, ensuring compliance with best practices.
---

# Skill body

## Overview

This skill orchestrates the validation and optimization of plugins against established best practices. It involves a structured approach to identify issues and apply necessary fixes.

## Core Principles

- **Strict Phases**: Follow the validation and optimization phases sequentially without skipping steps.
- **User Confirmation**: Ask for user input and decisions where specified.
- **Agent-Based Optimization**: Delegate fixes to a specialized agent based on validation results.
- **Reference-Driven**: Consult appropriate reference files for each issue category.

## Phase 1: Discovery & Validation

**Goal**: Validate plugin structure and detect all issues without applying fixes.

### Actions:

1. **Path Resolution**: Use `realpath` to resolve the absolute path from the provided plugin path.
2. **Existence Check**: Verify that the resolved path exists.
3. **Directory Structure Validation**:
   - Check for the presence of `.claude-plugin/plugin.json` manifest (required).
   - Identify component directories: `commands/`, `agents/`, `skills/`, `hooks/`.
   - Validate auto-discovery configuration.
   - Report any missing directories or files without creating them.
4. **Modern Architecture Assessment**:
   - If the `commands/` directory exists with `.md` files:
     - Ask the user: "This plugin uses a legacy `commands/` structure. Modern best practice recommends using `skills/` for better modularity. Would you like to migrate commands to skills structure?"
     - Options: "Yes, migrate to skills" / "No, keep commands as-is".
     - Record the user decision for the next phase.
5. **Execute Validation Suite**: Run all validation scripts using the Bash tool:
   - **Structure**: `bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate-file-patterns.sh "$TARGET"`
   - **Manifest**: `bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate-plugin-json.sh "$TARGET"`
   - **Components**: `bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate-frontmatter.sh "$TARGET"`
   - **Anti-Patterns**: `bash ${CLAUDE_PLUGIN_ROOT}/scripts/check-tool-invocations.sh "$TARGET"`.
6. **Analysis**: Review output from all scripts and compile a list of detected issues.

## Phase 2: Optimization

**Goal**: Apply fixes based on the validation results and user decisions.

### Actions:

1. **User Confirmation**: For each identified issue, ask the user for confirmation before applying fixes.
2. **Apply Fixes**: Use the specialized agent to implement the necessary changes based on the validation results and user input.
3. **Final Review**: After applying fixes, conduct a final review to ensure all issues have been addressed.

## Key Validation Rules

- Prefer Skills over Commands for new plugins.
- Ensure skills are under 500 lines with progressive disclosure.
- Verify agents have clear descriptions and single responsibility.
- Use kebab-case naming for components.
- Ensure scripts are executable with shebang and `${CLAUDE_PLUGIN_ROOT}` paths.
- Validate that all paths are relative and start with `./`.
- Confirm skills/commands are explicitly declared in `plugin.json`.

## Severity Levels

- **Critical**: Must fix before the plugin works correctly.
- **Warning**: Should fix for best practices compliance.
- **Info**: Nice to have improvements.

## Additional Resources

Refer to the `references/` directory for detailed validation patterns and guidelines.