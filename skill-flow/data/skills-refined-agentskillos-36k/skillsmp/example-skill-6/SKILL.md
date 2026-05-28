---
name: example-skill
description: "Example skill demonstrating the registry structure and format"
author: Skills Registry Team
date: 2024-12-10
---

# example-skill - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-10 |
| **Goal** | Create an example skill to demonstrate the skills registry format |
| **Environment** | Any system with Claude Code installed |
| **Status** | Success |

## Context
When setting up a skills registry, it helps to have a concrete example showing the expected structure and format. This skill serves as that reference.

## Verified Workflow

1. Copy the template folder:
```bash
cp -r templates/experiment-skill-template plugins/training/your-skill-name
```

2. Rename the skills subdirectory:
```bash
mv plugins/training/your-skill-name/skills/TEMPLATE_NAME \
   plugins/training/your-skill-name/skills/your-skill-name
```

3. Update plugin.json with your skill's metadata:
```json
{
  "name": "your-skill-name",
  "version": "1.0.0",
  "description": "Specific triggers: (1) when X, (2) when Y",
  "author": { "name": "Your Name" },
  "skills": "./skills",
  "repository": "https://github.com/smith-cop/Skills_Registry"
}
```

4. Fill in SKILL.md with your learnings, especially the Failed Attempts table.

5. Validate before committing:
```bash
python scripts/validate_plugins.py
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Generic descriptions | Skills weren't discoverable by /advise | Always include specific trigger conditions |
| Omitting failed attempts | Teammates repeated same mistakes | Document failures even more than successes |
| Vague parameters | Results weren't reproducible | Include exact, copy-pasteable configs |

## Final Parameters

The minimum required plugin.json structure:
```json
{
  "name": "skill-name",
  "description": "Trigger conditions...",
  "skills": "./skills"
}
```

## Key Insights
- The Failed Attempts table is referenced more than any other section
- Specific trigger conditions in descriptions make /advise more useful
- Include environment details for reproducibility
- Keep skills focused - one experiment per skill

## References
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- Instructions from the skills registry blog post
