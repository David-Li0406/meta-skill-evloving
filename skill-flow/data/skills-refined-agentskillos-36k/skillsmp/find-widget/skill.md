---
name: find-widget
description: Find a clickable widget by text/name using Haiku (context-efficient)
tags: [widget, ui, cooking, interface, click]
model: haiku
---

# Find Widget Skill

**Purpose:** Find a clickable widget in the game UI without flooding main context.

**When to use:**
- Need to find a widget to click (cooking interface, dialogue options, buttons)
- Using scan_widgets() directly would flood context (~13k tokens)
- Need widget_id for CLICK_WIDGET command

**Input:** Text or name to search for (e.g., "shrimp", "Cook", "Bank")

---

## Execution Steps

### 1. Scan All Widgets

Call the MCP tool:
```
scan_widgets()
```

This returns all visible widgets with their IDs, text, names, bounds, and actions.

### 2. Filter Results

Search for widgets matching the user's query:
- Check `text` field (case-insensitive)
- Check `name` field (case-insensitive, often contains item names)
- Check `actions` array (e.g., "Cook", "Bank", "Talk-to")

### 3. Return Compact Results

Return ONLY these fields for matching widgets:
```json
{
  "found": 2,
  "widgets": [
    {
      "widget_id": 17694735,
      "text": "Raw shrimps",
      "actions": ["Cook"],
      "bounds": {"x": 210, "y": 391, "width": 100, "height": 75}
    }
  ]
}
```

---

## Output Format

```
Found [N] widget(s) matching "[query]":

1. widget_id: [ID]
   text/name: [text]
   actions: [action list]
   bounds: x=[x], y=[y], w=[w], h=[h]

2. ...

To click: send_command("CLICK_WIDGET [widget_id]")
```

If no widgets found:
```
No widgets found matching "[query]"
Suggestions:
- Check if the interface is open
- Try a different search term
- Use scan_widgets() to see all available widgets
```

---

## Example Usage

### User says: "find cooking widget for shrimps"

1. Call scan_widgets()
2. Search for "shrimp" in name/text fields
3. Search for "Cook" in actions
4. Return:
```
Found 1 widget matching "shrimp":

1. widget_id: 17694735
   name: Raw shrimps
   actions: ["Cook"]
   bounds: x=210, y=391, w=100, h=75

To click: send_command("CLICK_WIDGET 17694735")
```

### User says: "find bank deposit button"

1. Call scan_widgets()
2. Search for "deposit" in text/name
3. Return matching widgets with IDs

---

## Important Notes

- **Run as Haiku** - This skill MUST run with model=haiku to avoid flooding context
- **Return compact results** - Never return full widget objects
- **Include widget_id** - This is the critical piece for clicking
- **Include bounds** - Helps user verify it's the right widget
- **Suggest CLICK_WIDGET** - Show the command to use the result
