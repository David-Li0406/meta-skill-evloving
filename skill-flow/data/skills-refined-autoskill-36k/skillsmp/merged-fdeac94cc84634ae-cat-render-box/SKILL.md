---
name: cat:render-box
description: Use this skill to render boxes and tables with proper emoji-aware alignment using box-drawing characters.
---

# Render Box

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

# Helper to pad cell content
pad_cell() {
    local content="$1"
    local width="$2"
    local display_w=$(display_width "$content")
    local padding=$((width - display_w))
    printf '%s%*s' "$content" "$padding" ""
}

# Render header (rounded top corners)
echo "╭$(dashes $COL1_W)┬$(dashes $COL2_W)┬$(dashes $COL3_W)┬$(dashes $COL4_W)┬$(dashes $COL5_W)╮"
echo "│$(pad_cell " Type" $COL1_W)│$(pad_cell " Description" $COL2_W)│$(pad_cell " Tokens" $COL3_W)│$(pad_cell " Context" $COL4_W)│$(pad_cell " Duration" $COL5_W)│"
echo "├$(dashes $COL1_W)┼$(dashes $COL2_W)┼$(dashes $COL3_W)┼$(dashes $COL4_W)┼$(dashes $COL5_W)┤"

# Render data rows
echo "│$(pad_cell " Explore" $COL1_W)│$(pad_cell " Explore codebase" $COL2_W)│$(pad_cell " 68.4k" $COL3_W)│$(pad_cell " 34% ✓ OK" $COL4_W)│$(pad_cell " 1m 7s" $COL5_W)│"
echo "│$(pad_cell " general-purpose" $COL1_W)│$(pad_cell " Implement refactor" $COL2_W)│$(pad_cell " 170.0k" $COL3_W)│$(pad_cell " 85% ⚠ EXCEEDED" $COL4_W)│$(pad_cell " 3m 12s" $COL5_W)│"

# Render footer (rounded bottom corners)
echo "╰$(dashes $COL1_W)┴$(dashes $COL2_W)┴$(dashes $COL3_W)┴$(dashes $COL4_W)┴$(dashes $COL5_W)╯"
```

**Output:**
```
╭─────────────────┬────────────────────────────────┬────────┬───────────────┬──────────╮
│ Type            │ Description                    │ Tokens │ Context       │ Duration │
├─────────────────┼────────────────────────────────┼────────┼───────────────┼──────────┤
│ Explore         │ Explore codebase               │ 68.4k  │ 34% ✓ OK      │ 1m 7s    │
│ general-purpose │ Implement refactor             │ 170.0k │ 85% ⚠ EXCEEDED│ 3m 12s   │
╰─────────────────┴────────────────────────────────┴────────┴───────────────┴──────────╯
```

### 3. Nested Box

For hierarchical displays like project status.

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/box.sh"

box_init 72
box_top "🗺️ PROJECT STATUS"
box_empty

# Use inner_* functions for nested boxes
inner_top "📦 v1.0: Initial Release"
inner_line "☑️ v1.1: Core features (5/5)"
inner_line "🔄 **v1.2: Current** (3/5)"
inner_line "   🔳 pending-task-1"
inner_line "   🔳 pending-task-2"
inner_bottom

box_empty
box_bottom
```

## Key Functions

| Function | Purpose |
|----------|---------|
| `box_init WIDTH` | Initialize box width (default 74) |
| `box_top "TITLE"` | Top border with optional title |
| `box_bottom` | Bottom border |
| `box_line "CONTENT"` | Content line with borders |
| `box_empty` | Empty line with borders |
| `box_divider` | Horizontal divider |
| `display_width "TEXT"` | Calculate emoji-aware display width |
| `pad "TEXT" WIDTH` | Pad text to exact display width |
| `dashes COUNT` | Generate COUNT dash characters |
| `inner_top "TITLE"` | Nested box top border |
| `inner_line "CONTENT"` | Nested box content line |
| `inner_bottom` | Nested box bottom border |
| `progress_bar PCT [WIDTH]` | Generate progress bar string |

## Box-Drawing Characters

| Character | Name | Usage |
|-----------|------|-------|
| `─` | Horizontal | Borders, dividers |
| `│` | Vertical | Side borders, column separators |
| `╭` `╮` | Rounded top | Top corners (ALL boxes and tables) |
| `╰` `╯` | Rounded bottom | Bottom corners (ALL boxes and tables) |
| `├` `┤` | T-junction | Row dividers |
| `┬` `┴` | T-junction | Column headers/footers |
| `┼` | Cross | Grid intersections |
| `█` `░` | Block | Progress bars |

**Note:** Use rounded corners (`╭╮╰╯`) for all boxes and tables for visual consistency. Square corners (`┌┐└┘`) are deprecated.

## Anti-Patterns

### Never calculate padding manually

```bash
# ❌ WRONG - LLMs cannot reliably calculate emoji widths
printf "│ %-20s │\n" "✅ Task complete"

# ✅ CORRECT - Use display_width function
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/box.sh"
box_line "  ✅ Task complete"
```

### Never use markdown tables with emojis

```markdown
<!-- ❌ WRONG - Emojis break column alignment -->
| Status | Task |
|--------|------|
| ✅ | Complete |
| ⚠ | Warning |
```

Use box-drawing tables instead (see Table with Headers above).

### Never hardcode emoji widths

```bash
# ❌ WRONG - Emoji widths vary by terminal
EMOJI_WIDTH=2

# ✅ CORRECT - Use display_width function
WIDTH=$(display_width "✅")
```

## Related Skills

- `cat:token-report` - Uses render-box for subagent token tables
- `cat:status` - Uses render-box for project status display
- `cat:shrink-doc` - Uses render-box for validation tables

## Related References

- `display-standards.md` - Visual formatting guidelines
- `M142` - Learning about LLM padding calculation limitations