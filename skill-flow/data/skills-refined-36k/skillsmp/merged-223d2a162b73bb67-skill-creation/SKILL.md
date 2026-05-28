---
name: skill-creation
description: Use this skill when you need to create, manage, or improve Claude Code skills, ensuring they follow best practices and are well-documented.
---

# Skill Creation

This skill guides the creation and management of Claude Code skills, including best practices for structure, documentation, and integration with existing skills.

## When to Use

- "Create a skill for X"
- "Help me make a new skill"
- "Turn this script into a skill"
- "How do I create a skill?"
- "Improve an existing skill"
- "Review skill quality"

## Skill Structure

Skills are organized in the following directory structure:

```
.claude/skills/<skill-name>/
├── SKILL.md          # Required: Main skill definition
├── scripts/          # Optional: Supporting scripts
└── templates/        # Optional: Templates, examples
```

### SKILL.md Format

```yaml
---
name: skill-name
description: Brief description (shown in skill list)
version: 1.0.0
allowed-tools: [Bash, Read, Write]  # Optional: restrict tools
---

# Skill Name

## Purpose
[2-3 sentences explaining what this skill helps accomplish and why it matters]

## When to Use This Skill
- [Specific scenario 1]
- [Specific scenario 2]
- [Specific scenario 3]

## Instructions
[Step-by-step instructions for Claude to follow]

## Examples
[Usage examples]
```

## Creating a New Skill

### Step 1: Use a Template

Copy an existing skill template to start your new skill:

```bash
cp $CLAUDE_PROJECT_DIR/scripts/template.py $CLAUDE_PROJECT_DIR/scripts/my_skill.py
```

### Step 2: Customize the Script

Edit your new script to implement the desired functionality. For example:

```python
async def main():
    # Your skill logic here
    print("Hello from my skill!")
```

### Step 3: Create the SKILL.md

Create the `.claude/skills/my-skill/SKILL.md` file with the appropriate structure and content.

### Step 4: Add Triggers (Optional)

Add triggers to the skill rules configuration to enable discovery:

```json
{
  "skills": {
    "my-skill": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "medium",
      "description": "What it does",
      "promptTriggers": {
        "keywords": ["keyword1", "keyword2"],
        "intentPatterns": ["(pattern).*?(match)"]
      }
    }
  }
}
```

## Best Practices

- **Clear Structure**: Organize content into logical sections.
- **YAML Frontmatter**: Ensure proper metadata format.
- **Tool Declaration**: Explicitly list allowed tools.
- **Documentation**: Include comments and explanations.

## Creation Checklist

- [ ] Does a similar skill already exist?
- [ ] Is this knowledge needed repeatedly (3+ times)?
- [ ] Is there enough depth for a skill (500+ words)?
- [ ] Does it apply across multiple contexts?
- [ ] SKILL.md has frontmatter (name, description)
- [ ] "When to Use" section is clear
- [ ] Instructions are copy-paste ready

## Learning Points

From this skill, you can learn how to:

- Structure YAML frontmatter
- Include necessary sections in skill content
- Declare tool permissions
- Organize workflows effectively
- Follow best practices for documentation

## Related Skills

- `implementation-planning` - Plan skill creation
- `frankx-brand` - Ensure voice consistency
- `parallel-agents` - Create multiple skills concurrently

## Maintenance

Regularly review skills for outdated patterns and update as necessary. Ensure versioning is consistent with changes made.

```yaml
# When to bump versions:
version: 1.0.0  # Initial release
version: 1.1.0  # New content added
version: 2.0.0  # Breaking changes/restructure
```