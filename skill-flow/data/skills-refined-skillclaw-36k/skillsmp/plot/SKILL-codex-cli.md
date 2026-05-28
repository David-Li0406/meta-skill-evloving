---
name: plot-annotator
description: Trigger when user asks to see a plot, show annotations, load a figure, or apply plot modifications. Also trigger when user mentions ~/.claude/plots/ or plot annotator.
metadata:
  short-description: Visual plot annotation workflow
---

# Plot Annotator Skill

When the user wants to work with plots, follow these steps.

## When user says "show my plot" or "see the plot"

Run these commands:

```bash
# Read the current plot image
cat ~/.claude/plots/current.png  # (use file read tool)

# Read metadata to find source script
cat ~/.claude/plots/current_meta.json

# Read annotations if they exist
cat ~/.claude/plots/current_annotations.json 2>/dev/null || echo "No annotations yet"
```

Then display the image and summarize:
- Image dimensions
- Source script (from meta.json)
- Number of annotation groups

## When user says "load this plot" with an image path

```bash
# Copy image to plots directory
cp <user_provided_path> ~/.claude/plots/current.png

# Find the source script automatically
filename=$(basename <user_provided_path> .png)
grep -r "$filename" --include="*.py" --exclude-dir=".venv" ~/Github /media/*/Data/Github 2>/dev/null | head -5

# Create metadata
cat > ~/.claude/plots/current_meta.json << EOF
{
  "name": "$filename",
  "source": "<user_provided_path>",
  "source_script": "<found_script>",
  "created": "$(date -Iseconds)"
}
EOF

# Start annotator server
pkill -f "annotate_server.py" 2>/dev/null || true
cd ~/.claude/plots && python3 ~/.claude/tools/annotate_server.py &

# Open browser
xdg-open "http://localhost:8888/annotate.html?load=true"
```

Tell user: "Annotator opened at http://localhost:8888/annotate.html - annotate and click Save when done"

## When user says "open annotator" or "annotate"

```bash
pkill -f "annotate_server.py" 2>/dev/null || true
cd ~/.claude/plots && python3 ~/.claude/tools/annotate_server.py &
xdg-open "http://localhost:8888/annotate.html"
```

## When user says "apply annotations" or "apply changes"

1. Read the files:
```bash
cat ~/.claude/plots/current_annotations.json
cat ~/.claude/plots/current_meta.json
```

2. Parse annotations by group_id - each group has shapes + text instruction

3. Read the source script from `source_script` in metadata

4. For each annotation group:
   - Find the matplotlib element based on bbox position
   - Apply the text instruction to modify the code

5. Save the modified script and regenerate if possible

## File Locations

| File | Purpose |
|------|---------|
| `~/.claude/plots/current.png` | Current plot image |
| `~/.claude/plots/current_meta.json` | Source script path, project info |
| `~/.claude/plots/current_annotations.json` | Annotation zones from the HTML app |
| `~/.claude/tools/annotate_server.py` | Python server (port 8888) |
| `~/.claude/tools/annotate.html` | HTML annotation app |

## Important

- The annotator runs at http://localhost:8888/annotate.html
- User must click 💾 Save in the browser to write files to disk
- After saving, read the JSON files to see the annotations
- The `source_script` field tells you which Python file generates the plot
