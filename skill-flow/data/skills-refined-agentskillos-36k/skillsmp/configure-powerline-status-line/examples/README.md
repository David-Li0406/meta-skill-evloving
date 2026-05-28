# Powerline Configuration Examples

This directory contains example configurations for common powerline setups.

## Examples

### default.json
Complete default configuration as used when user requests "use my default status line".

**Features:**
- Tokyo Night theme with powerline style
- Two-line layout
- First line: directory (basename) + git status
- Second line: model + metrics + token usage + context

**Use this as:** Starting point for customization

---

### minimal.json
Simple single-line configuration showing only essential information.

**Features:**
- Directory (full path) + context percentage
- Single line layout
- Minimal visual clutter

**Use this when:** User wants "just show the directory and context"

---

### two-lines.json
Multi-line layout demonstrating vertical organization.

**Features:**
- Directory on first line (basename only)
- All metrics on second line (comprehensive)
- Clear separation of location info vs. performance info

**Use this when:** User says "directory on top then all metrics below"

---

### custom-theme.json
Alternative theme and style demonstration.

**Features:**
- Rose Pine theme with capsule style
- Fish-style directory abbreviation
- Extended git information (SHA, working tree, operation)

**Use this as:** Example of theme/style customization

---

## Notes

All examples are valid JSON and can be used directly as `.claude/.claude-powerline.json` configuration files.

Each example demonstrates different segment combinations and layouts. Mix and match segments based on user needs while maintaining the JSON structure.
