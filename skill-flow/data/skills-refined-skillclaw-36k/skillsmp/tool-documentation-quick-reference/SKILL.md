---
name: Tool Documentation Quick Reference
description: This skill should be used when the user asks for "quick reference", "show me examples for [tool]", "common commands for pandoc", "how do I use pandoc", "pandoc cheatsheet", "show pandoc examples", "tool-lookup", or needs fast offline access to command-line tool commands without detailed explanations. Load when user wants working examples at a glance, not troubleshooting or in-depth documentation.
version: 1.0.0
---

# Tool Documentation Quick Reference

Fast access to common command-line tool commands and options without requiring internet access.

## Purpose

Provide instant offline reference for frequently-used command-line tool commands, organized by use case for quick scanning. Load when users need quick examples without full documentation explanation.

## When to Use

This skill should be used when the user:
- Requests quick reference or common commands for a tool
- Asks for examples without detailed explanation
- Wants to browse available options at a glance
- Needs fast command lookup

This skill should NOT be used when the user needs:
- Detailed explanations (use pandoc-guide agent instead)
- Troubleshooting assistance (use pandoc-guide agent)
- Official documentation (use pandoc-guide agent with WebFetch)

## Available Tools

Current quick references:
- **pandoc** - Document conversion tool (markdown, PDF, DOCX, HTML, etc.)

Future references planned:
- postgres - PostgreSQL database
- git - Version control
- docker - Container management

## Usage Pattern

When the user requests pandoc quick reference:

1. Display categorized command examples
2. Include brief descriptions of common flags
3. Provide links to official documentation

**Format:**
```
# [Tool Name] Quick Reference

## [Category 1]
### [Use Case]
```bash
[command with common flags]
```

## [Category 2]
...

## Resources
- Official docs
- Related tools
```

## Reference Files

Each tool has a reference file in `references/`:

**Current:**
- **`references/pandoc-quick-ref.md`** - Pandoc common commands categorized by use case (conversions, academic, filters, troubleshooting)

**Future:**
- `references/postgres-quick-ref.md`
- `references/git-quick-ref.md`
- `references/docker-quick-ref.md`

## Quick Reference Structure

Each reference file follows this structure:

1. **Tool Overview** - Brief description
2. **Common Conversions** - Most frequent use cases
3. **Advanced Features** - Filters, templates, customization
4. **Common Options** - Table of frequently-used flags
5. **Troubleshooting** - Common errors and quick fixes
6. **Resources** - Links to official documentation

Target length: 200-400 words (ultra-concise)
Focus: Working commands with minimal explanation

## Example Interaction

```
user: "Show me pandoc examples"

Display:
- Common conversions (MD→PDF, DOCX→MD, etc.)
- Academic writing commands (bibliography, citations)
- Filter examples
- Troubleshooting quick fixes
- Resource links
```

## Design Philosophy

**Quick reference vs. Documentation agent:**

| Quick Reference (this skill) | Documentation Agent (pandoc-guide) |
|------------------------------|-------------------------------------|
| Fast command lookup          | Detailed explanations              |
| Offline, no WebFetch         | Fetches official docs              |
| Categorized examples         | Root cause analysis                |
| Minimal explanation          | Flag-by-flag breakdowns            |
| User-initiated (`/tool-lookup`) | Auto-triggers on queries      |

**Progressive disclosure:**
Users start with quick reference for common tasks, escalate to pandoc-guide agent for troubleshooting or learning.

## Adding New Tool References

To add a new tool (e.g., postgres):

1. Create `references/postgres-quick-ref.md`
2. Follow structure: Overview → Common Commands → Advanced → Options Table → Troubleshooting → Resources
3. Keep ultra-concise (200-400 words)
4. Focus on working commands
5. Update this SKILL.md to list new tool

## Reference File Format

Each reference markdown file should:
- Start with tool name heading (`# Pandoc Quick Reference`)
- Use level 2 headings for categories (`## Common Conversions`)
- Use level 3 headings for specific use cases (`### Markdown to PDF`)
- Include code blocks for commands
- Provide tables for option flags
- End with Resources section

**Example structure:**
```markdown
# [Tool] Quick Reference

## Common Use Cases
### Use Case 1
```bash
command --flag value
```

### Use Case 2
...

## Common Options
| Flag | Purpose |
|------|---------|
| -o   | Output  |

## Resources
- Official docs URL
```

This design ensures users get immediate answers for common tasks while the pandoc-guide agent handles complex queries and troubleshooting.
