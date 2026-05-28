---
name: render-box
description: Use this skill when you need to render boxes and tables with proper emoji-aware alignment using box-drawing characters.
---

# Skill body

## Purpose

Render boxes, tables, and bordered displays with proper emoji-aware alignment. LLMs cannot reliably calculate character-level padding for Unicode text, so this skill delegates width calculation to bash scripts that use Python's `unicodedata` module.

## When to Use

**MANDATORY** when rendering any bordered output containing emojis:
- Status boxes with emoji indicators (✅, ⚠, 🔄)
- Tables with emoji columns
- Checkpoint displays
- Progress displays with emoji prefixes

**Not needed** for:
- Plain markdown tables without emojis
- Unbordered lists with emojis
- Simple text output

## Prerequisites

The box rendering library is located in the plugin:
- `${CLAUDE_PLUGIN_ROOT}/scripts/lib/box.sh` - Core rendering functions
- `${CLAUDE_PLUGIN_ROOT}/scripts/pad-box-lines.sh` - Line padding with emoji widths
- `${CLAUDE_PLUGIN_ROOT}/emoji-widths.json` - Terminal-specific emoji width data

## Box Types

### 1. Simple Box

For status displays, checkpoints, and messages.

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/box.sh"

box_init 72  # Set box width (default 74)
box_top "✅ CHECKPOINT: Task Complete"
box_empty
box_line "  Task: fix-subagent-token-measurement"
box_line "  Status: Complete"
box_empty
box_divider
box_line "  Tokens: 45,000 (22% of context)"
box_empty
box_bottom
```

**Output:**
```
╭─── ✅ CHECKPOINT: Task Complete ──────────────────────────────────╮
│                                                                    │
│  Task: fix-subagent-token-measurement                              │
│  Status: Complete                                                  │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│  Tokens: 45,000 (22% of context)                                   │
│                                                                    │
╰────────────────────────────────────────────────────────────────────╯
```

### 2. Table with Headers

For data with multiple columns. Build rows as TSV, then render with column alignment. Use rounded corners for consistency with box displays.

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/box.sh"

# Define column widths (adjust based on content)
COL1_W=17  # Type
COL2_W=32  # Description
COL3_W=8   # Tokens
COL4_W=15  # Context
COL5_W=10  # Duration
```