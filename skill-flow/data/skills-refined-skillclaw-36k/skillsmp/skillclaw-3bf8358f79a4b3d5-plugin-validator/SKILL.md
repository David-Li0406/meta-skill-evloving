---
name: plugin-validator
description: Use this skill to automatically validate Claude Code plugins against repository standards, ensuring compliance with structure, schemas, and security when users mention validating or checking plugins.
---

# Plugin Validator

## Purpose
Automatically validates Claude Code plugins against repository standards, checking structure, JSON schemas, frontmatter, permissions, security, and marketplace compliance - optimized for claude-code-plugins repository.

## Trigger Keywords
- "validate plugin"
- "check plugin"
- "plugin validation"
- "plugin errors"
- "lint plugin"
- "verify plugin"

## Validation Checks

### 1. Required Files
- ✅ `.claude-plugin/plugin.json` exists
- ✅ `README.md` exists and is not empty
- ✅ `LICENSE` file exists
- ✅ At least one component directory (commands/, agents/, skills/, hooks/, mcp/) exists

### 2. Plugin.json Schema
```bash
# Required fields:
- name (kebab-case, lowercase, hyphens only)
- version (semantic versioning x.y.z)
- description (clear, concise)
- author.name
- author.email
- license (MIT, Apache-2.0, etc.)
- keywords (array, at least 2)

# Optional but recommended:
- repository (GitHub URL)
- homepage (docs URL)
```

### 3. Frontmatter Validation
**For Commands (commands/*.md):**
```yaml
---
name: command-name
description: Brief description
model: sonnet|opus|haiku
---
```

**For Agents (agents/*.md):**
```yaml
---
name: agent-name
description: Agent purpose
model: sonnet|opus|haiku
---
```

**For Skills (skills/*/SKILL.md):**
```yaml
---
name: Skill Name
description: What it does AND when to use it
allowed-tools: Tool1, Tool2, Tool3  # optional
---
```

### 4. Directory Structure
Validates proper hierarchy:
```
plugin-name/
├── .claude-plugin/          # Required
│   └── plugin.json          # Required
├── README.md                 # Required
├── LICENSE                   # Required
├── commands/                 # Optional
│   └── *.md
├── agents/                   # Optional
│   └── *.md
├── skills/                   # Optional
│   └── skill-name/
│       └── SKILL.md
├── hooks/                    # Optional
│   └── hooks.json
└── mcp/                      # Optional
    └── *.json
```

### 5. Script Permissions
```bash
# All .sh files must be executable
find . -name "*.sh" ! -perm -u+x
# Should return empty
```

### 6. JSON Validation
```bash
# All JSON must be valid
jq empty plugin.json
jq empty marketplace.extended.json
```