---
name: library-management
description: >
  Create, update, and delete skills, commands, tools, and rules in the Open Agent Library.
  Trigger terms: library, skill, command, tool, rule, save skill, create skill, new skill.
---

## When to Use
- Creating a new skill, command, tool, or rule
- Updating existing library content
- Deleting library items
- Syncing library changes to git remote

## When NOT to Use
- Local file operations unrelated to the library
- Running missions or managing workspaces

## Quick Reference

| Resource | List | Get | Save | Delete |
|----------|------|-----|------|--------|
| Skills | `library-skills_list_skills` | `library-skills_get_skill` | `library-skills_save_skill` | `library-skills_delete_skill` |
| Commands | `library-commands_list_commands` | `library-commands_get_command` | `library-commands_save_command` | `library-commands_delete_command` |
| Tools | `library-commands_list_tools` | `library-commands_get_tool` | `library-commands_save_tool` | `library-commands_delete_tool` |
| Rules | `library-commands_list_rules` | `library-commands_get_rule` | `library-commands_save_rule` | `library-commands_delete_rule` |

### Git Operations
- `library-git_status` - Check for uncommitted changes
- `library-git_commit` - Commit with message
- `library-git_push` - Push to remote
- `library-git_sync` - Pull latest changes

## Procedure

1. **List** existing items to see what's there
2. **Get** current content before modifying (avoid overwrites)
3. **Save** with the full content (YAML frontmatter + body)
4. **Commit** with a descriptive message
5. **Push** to sync with remote

## File Formats

### Skill (`skill/<name>/SKILL.md`)
```yaml
---
name: skill-name
description: What this skill does
---
Instructions for using this skill...
```

### Command (`command/<name>.md`)
```yaml
---
description: Command description
---
Prompt template. Use $ARGUMENTS for user input.
```

### Tool (`tool/<name>.ts`)
```typescript
import { tool } from "@opencode-ai/plugin"
export const my_tool = tool({
  description: "What it does",
  args: { param: tool.schema.string().describe("Param description") },
  async execute(args) { return "result" },
})
```

### Rule (`rule/<name>.md`)
```yaml
---
description: Rule description
---
Instructions applied to agents referencing this rule.
```

## Checks & Guardrails
- Always read before updating to avoid overwriting
- Use descriptive commit messages
- Check `library-git_status` before pushing
- Skill names: lowercase, hyphens allowed, 1-64 chars
