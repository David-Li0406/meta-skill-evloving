---
name: julien-skill-help
description: "Interactive catalog of all available skills. Use when: user asks for help, wants to discover skills, or asks what you can do."
license: Apache-2.0
metadata:
  author: "Julien"
  version: "1.0.0"
  category: "discovery"
triggers:
  # Discovery questions (specific)
  - "list skills"
  - "show skills"
  - "what skills"
  - "which skills"
  - "available skills"
  - "skill catalog"
  - "discover skills"
  # French equivalents
  - "liste des skills"
  - "quels skills"
  - "montre les skills"
  - "catalogue skills"
  - "decouvrir skills"
  # Capability questions
  - "what can you do"
  - "qu'est-ce que tu sais faire"
  - "que sais-tu faire"
  # Help with skills (not generic help)
  - "help with skills"
  - "aide sur les skills"
  - "skill help"
---

# Skill Help

Interactive catalog of all available Claude Code skills.

## Observability

**First**: Display activation message:
```
🔧 Skill "julien-skill-help" activated
```

## Execution

### Step 1: Load the Registry

Read the hybrid registry to get all available skills:

```bash
cat ~/.claude/configs/hybrid-registry.json
```

If the file doesn't exist, inform the user to run `/sync` first.

### Step 2: Display Skills by Category

Group skills by their prefix and display as a formatted table.

**Categories:**
- **office**: Document manipulation (xlsx, docx, pdf, pptx)
- **dev**: Development tools (commit, hooks, claude-md)
- **infra**: Infrastructure & hosting (hostinger, docker, deployment)
- **ref**: Reference guides (ahk, batch, powershell, markdown)
- **skill**: Skill management (creator, reviewer, router)
- **web**: Web development (frontend, artifacts, testing)
- **workflow**: Automation (gemini, codex, background tasks)
- **media**: Media processing (subtitle, onepiece, jellyfin)
- **wp**: WordPress tools

### Step 3: Show Summary

Display:
```
📚 Skill Catalog
================

Total: {count} skills available

🏢 Office (4 skills)
  • anthropic-office-xlsx - Excel spreadsheets
  • anthropic-office-docx - Word documents
  • anthropic-office-pdf  - PDF manipulation
  • anthropic-office-pptx - PowerPoint presentations

🛠️ Development (4 skills)
  • julien-dev-commit-message - Generate commit messages
  • julien-dev-hook-creator   - Create Claude Code hooks
  • julien-dev-claude-md      - Document projects
  • julien-dev-powershell     - PowerShell profile

... (continue for each category)

💡 Usage:
  • Type naturally - the router will suggest relevant skills
  • Invoke directly: Skill("skill-name")
  • Run /show-routing to see last suggestions
```

### Step 4: Offer Interactive Exploration

Ask if user wants:
1. Details on a specific category
2. Details on a specific skill
3. Search by keyword

## Output Format

Use clear Markdown formatting:
- Headers for categories
- Tables or bullet lists for skills
- Brief descriptions (1 line max)
- Highlight top 5 most useful skills

## Skill Chaining

### Input Expected
- None (standalone entry point)

### Output Produced
- **Format**: Formatted Markdown catalog
- **Side effects**: None (read-only)

### Tools Used
- `Read` (usage: read hybrid-registry.json)
- `Bash` (usage: cat registry file)
