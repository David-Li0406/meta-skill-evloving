---
name: julien-cmd-list-resources
description: List all skills, agents, and plugins available in this repository or marketplace
author: Julien
version: 1.0.0
category: infrastructure
type: command
triggers:
  - list skills
  - show skills
  - available skills
  - list resources
  - show resources
  - lister les skills
  - afficher les skills
  - skills disponibles
  - liste des ressources
---

# List Resources Command

Run the list-resources script to display all available skills and resources.

Please execute the following command:

```bash
python ~/.claude/scripts/list-resources.py
```

This will display:
- All available skills organized by category (global + project)
- Slash commands available
- Installation and usage instructions

Note: If script not found, run `/sync` from the marketplace repo first.
