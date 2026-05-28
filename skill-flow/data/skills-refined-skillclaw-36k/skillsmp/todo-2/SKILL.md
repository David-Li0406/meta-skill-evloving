---
name: "todo"
description: "Parse input and create todo items"
---

Parse user input and create todo items.

**Input**: `$ARGUMENTS` containing task descriptions

## Process

1. **Validate**: If `$ARGUMENTS` is empty, ask user to provide task descriptions.

2. **Parse**: Intelligently split input into items (numbered lists, comma-separated, natural language, etc.)

3. **Create**: Call TodoWrite tool with:
   - `content`: Imperative form (what needs to be done)
   - `activeForm`: Present continuous form (what's happening now)
   - `status`: "pending"
   - Append to existing todo list if it exists (don't replace)

4. **Report**: Print todo in claude format using TodoWrite tool's list output.

5. **Execute**: Continue working on next items in todo and push when done.
