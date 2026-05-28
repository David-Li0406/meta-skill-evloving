# Creating and Sharing Kyotee Skills

Skills are reusable knowledge packages that teach Kyotee how to build with specific tech stacks.

## Why Skills?

Without skills, Kyotee uses generic patterns that may not follow best practices for a specific framework. Skills provide:

- **Project structure** - Where files should go
- **Code patterns** - How to write idiomatic code
- **Configuration** - Correct config file contents
- **Setup commands** - How to install and run

## Skill Location

Skills are stored in `~/.kyotee/skills/` as TOML files:

```
~/.kyotee/skills/
├── cloudflare-hono-datastar.toml
├── go-gin-sqlite.toml
├── nextjs-tailwind.toml
└── python-fastapi.toml
```

## Creating a New Skill

### 1. Start from Template

Copy the template:
```bash
cp ~/.claude/skills/kyotee/references/skill-template.toml ~/.kyotee/skills/my-new-skill.toml
```

### 2. Fill in the Details

**Required sections:**
- `name` - Human-readable name
- `description` - When to use this skill
- `tags` - Keywords for matching (framework names, language, etc.)
- `[conventions]` - Project structure and naming
- `[patterns]` - Code patterns for entry point, components, etc.

**Optional sections:**
- `[setup]` - Installation and dev commands
- `[docs]` - Reference documentation URLs
- `[preferences]` - Styling, state management recommendations

### 3. Test the Skill

Run Kyotee with a project that matches the skill:
```
/kyotee

> Build a web app with [your framework]
```

Verify that:
- The skill is detected in the Context phase
- Patterns are followed in the Implement phase
- The result matches your expectations

### 4. Iterate

If issues occur:
- Kyotee will offer to update the skill
- Or manually edit `~/.kyotee/skills/your-skill.toml`

## Skill Matching

During the Context phase, Kyotee matches skills by:

1. **Tags** - Exact keyword matches (e.g., "hono", "cloudflare")
2. **Name/Description** - Fuzzy matching on tech stack terms
3. **User's spec** - Comparing spec requirements to skill capabilities

## Sharing Skills

Skills are just TOML files. Share them by:

1. **Copy the file** - Send `~/.kyotee/skills/my-skill.toml` to others
2. **Git repository** - Create a repo of skills
3. **Community collection** - (Future) Contribute to shared skill library

### Recommended Skill Naming

Use descriptive, searchable names:
- `cloudflare-hono-datastar.toml` ✓
- `my-web-skill.toml` ✗

Include the key technologies:
- Platform (cloudflare, vercel, aws)
- Framework (hono, next, gin, fastapi)
- Notable libraries (datastar, htmx, tailwind)

## Skill Quality Checklist

Before sharing a skill:

- [ ] Entry point pattern actually works
- [ ] Config files are valid (test with linters)
- [ ] Project structure is complete
- [ ] Setup commands work on a fresh project
- [ ] Documentation URLs are current
- [ ] Tags include all relevant keywords

## Example: Minimal Skill

```toml
name = "Express.js Basic"
description = "Simple Express.js API server"
tags = ["express", "node", "javascript", "api"]

[conventions]
project_structure = """
src/
  index.js
  routes/
package.json
"""

[patterns]
entry_point = """
const express = require('express')
const app = express()

app.use(express.json())

app.get('/', (req, res) => {
  res.json({ status: 'ok' })
})

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})
"""

[setup]
commands = ["npm install", "npm start"]
```

## Advanced: Skill Inheritance

(Future feature) Skills could extend other skills:

```toml
extends = "base-typescript"

[patterns]
# Only override what's different
entry_point = """..."""
```
