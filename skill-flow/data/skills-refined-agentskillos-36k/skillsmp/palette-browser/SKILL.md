---
name: palette-browser
description: Browse and manage color palettes from the curated library with visual previews
---

# Palette Browser

Browse, preview, and select color palettes from the curated library of 85+ palettes.

## Visual Palette Listing

Use the `list-palettes.sh` script to show palettes with color swatches:

```bash
# List all palettes with colors
bash ${CLAUDE_PLUGIN_ROOT}/scripts/list-palettes.sh

# List specific source
bash ${CLAUDE_PLUGIN_ROOT}/scripts/list-palettes.sh tailwind
bash ${CLAUDE_PLUGIN_ROOT}/scripts/list-palettes.sh material
bash ${CLAUDE_PLUGIN_ROOT}/scripts/list-palettes.sh terminal-classics

# Compact view (one line per palette)
bash ${CLAUDE_PLUGIN_ROOT}/scripts/list-palettes.sh --compact
bash ${CLAUDE_PLUGIN_ROOT}/scripts/list-palettes.sh tailwind --compact
```

Output shows color swatches: `[bg][fg] █red █green █yellow █blue █magenta █cyan`

## Available Sources (85 palettes)

| Source | Count | Description |
|--------|-------|-------------|
| tailwind | 21 | Tailwind CSS utility colors |
| material | 12 | Material Design 3 color system |
| terminal-classics | 11 | Popular terminal themes (Catppuccin, Dracula, Nord...) |
| radix | 12 | Radix accessible color system |
| open-color | 10 | Open-source UI color scheme |
| ibm-carbon | 8 | IBM Carbon design system |
| github-primer | 7 | GitHub's design system |
| apple-hig | 4 | Apple Human Interface Guidelines |

## Commands

### 1. List All Palettes
```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/list-palettes.sh
```

### 2. Filter by Source
```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/list-palettes.sh <source>
```
Sources: `tailwind`, `material`, `terminal-classics`, `radix`, `open-color`, `ibm-carbon`, `github-primer`, `apple-hig`

### 3. Filter by Mode
```bash
# Show only dark palettes
jq -r '.palettes[] | select(.mode == "dark") | "\(.source)/\(.id)"' ${CLAUDE_PLUGIN_ROOT}/palettes/_index.json

# Show only light palettes
jq -r '.palettes[] | select(.mode == "light") | "\(.source)/\(.id)"' ${CLAUDE_PLUGIN_ROOT}/palettes/_index.json
```

### 4. Preview Specific Palette
```bash
# Show full palette details
cat ${CLAUDE_PLUGIN_ROOT}/palettes/<source>/<id>.json | jq '.'

# Show just the key colors
cat ${CLAUDE_PLUGIN_ROOT}/palettes/<source>/<id>.json | jq '{bg: .derived.bg, fg: .derived.fg, red: .derived.red, green: .derived.green, blue: .derived.blue}'
```

### 5. Set Active Palette
```bash
mkdir -p ~/.claude/plugins/ghostty-claude-setup
cat > ~/.claude/plugins/ghostty-claude-setup/palette.local.json << EOF
{
  "active": "<palette-id>",
  "favorites": []
}
EOF
```

### 6. Add to Favorites
```bash
# Read current config and add favorite
CONFIG=$(cat ~/.claude/plugins/ghostty-claude-setup/palette.local.json 2>/dev/null || echo '{"active":"catppuccin-mocha","favorites":[]}')
echo "$CONFIG" | jq '.favorites += ["<palette-id>"] | .favorites |= unique' > ~/.claude/plugins/ghostty-claude-setup/palette.local.json
```

### 7. Search Palettes
```bash
# Search by name
jq -r '.palettes[] | select(.name | ascii_downcase | contains("dark"))' ${CLAUDE_PLUGIN_ROOT}/palettes/_index.json

# Find warm-toned palettes
jq -r '.palettes[] | select(.name | test("gruvbox|stone|amber|orange|warm"; "i"))' ${CLAUDE_PLUGIN_ROOT}/palettes/_index.json

# Find cool-toned palettes
jq -r '.palettes[] | select(.name | test("nord|slate|blue|cyan|cool"; "i"))' ${CLAUDE_PLUGIN_ROOT}/palettes/_index.json
```

## User Workflow

When user asks to browse palettes:

1. **Show visual list** using `list-palettes.sh`
2. **Ask which source** they want to explore (or show all)
3. **Filter by preference** (dark/light, warm/cool)
4. **Preview selected** palette with full color details
5. **Set as active** when user confirms choice

## Example Session

```
User: Show me the available palettes

Agent: [runs list-palettes.sh to show visual palette list]

Here are the 85 available palettes with color previews:
[output with color swatches]

Which source would you like to explore?
- tailwind (21) - Modern utility colors
- material (12) - Google's design system
- terminal-classics (11) - Popular themes like Catppuccin, Dracula
- [etc.]

User: Show me the terminal classics

Agent: [runs list-palettes.sh terminal-classics]

Here are the terminal classic themes:
[output with visual swatches for each theme]

Would you like to set one as your active palette?
```
