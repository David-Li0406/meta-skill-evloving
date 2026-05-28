# Anthropic Official Marketplace Format

Reference for Claude Code plugin marketplace structure based on https://github.com/anthropics/skills

## Table of Contents

- Official Repository Structure
- Official marketplace.json
- Key Patterns
- Your Template
- User Installation
- User Settings Configuration
- Comparison: Single vs Multiple Plugins
- References

## Official Repository Structure

```
anthropics/skills/
├── .claude-plugin/
│   └── marketplace.json          ← Only this file (no plugin.json)
├── skills/
│   ├── algorithmic-art/
│   │   └── SKILL.md
│   ├── skill-creator/
│   │   └── SKILL.md
│   └── [other skills]/
│       └── SKILL.md
├── README.md
└── LICENSE
```

## Official marketplace.json

```json
{
  "name": "anthropic-agent-skills",
  "owner": {
    "name": "Keith Lazuka",
    "email": "klazuka@anthropic.com"
  },
  "metadata": {
    "description": "Anthropic example skills",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "document-skills",
      "description": "Collection of document processing suite including Excel, Word, PowerPoint, and PDF capabilities",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/xlsx",
        "./skills/docx",
        "./skills/pptx",
        "./skills/pdf"
      ]
    },
    {
      "name": "example-skills",
      "description": "Collection of example skills demonstrating various capabilities",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/algorithmic-art",
        "./skills/brand-guidelines",
        "./skills/canvas-design",
        "./skills/frontend-design",
        "./skills/internal-comms",
        "./skills/mcp-builder",
        "./skills/skill-creator",
        "./skills/slack-gif-creator",
        "./skills/theme-factory",
        "./skills/web-artifacts-builder",
        "./skills/webapp-testing"
      ]
    }
  ]
}
```

## Key Patterns

### No plugin.json

Anthropic's repository has **only marketplace.json**, not plugin.json. This is the recommended approach.

### Source Field

```json
"source": "./"
```

Always points to repository root (`./`), not `./.claude-plugin`.

### Strict Mode

```json
"strict": false
```

Disables strict mode for flexibility.

### Skills Array

```json
"skills": [
  "./skills/skill-name",
  ...
]
```

Explicitly lists all skill paths relative to repository root.

### Multiple Plugins

One marketplace can contain multiple plugins, each grouping related skills:

```json
{
  "plugins": [
    {
      "name": "document-skills",
      "skills": ["./skills/xlsx", "./skills/pdf", ...]
    },
    {
      "name": "example-skills",
      "skills": ["./skills/skill-creator", ...]
    }
  ]
}
```

## Your Template

Adapt for your marketplace:

```json
{
  "name": "your-marketplace-name",
  "owner": {
    "name": "Your Name"
  },
  "metadata": {
    "description": "Brief description of your marketplace",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "your-plugin-name",
      "description": "What your plugin does",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/your-skill-one",
        "./skills/your-skill-two"
      ]
    }
  ]
}
```

## User Installation

Users install from GitHub:

```bash
# Add marketplace
/plugin marketplace add owner/repository

# Install specific plugin
/plugin install plugin-name@owner/repository
```

## User Settings Configuration

**.claude/settings.json** (in user's project):

```json
{
  "extraKnownMarketplaces": {
    "your-marketplace-name": {
      "source": {
        "source": "github",
        "repo": "owner/repository"
      }
    }
  },
  "enabledPlugins": {
    "your-plugin-name@your-marketplace-name": true
  },
  "permissions": {
    "allow": [
      "Skill(your-skill-one)",
      "Skill(your-skill-two)"
    ]
  }
}
```

## Comparison: Single vs Multiple Plugins

### Single Plugin Marketplace

Most common for personal repositories:

```json
{
  "plugins": [
    {
      "name": "skills-helper",
      "skills": [
        "./skills/creating-effective-skills",
        "./skills/reviewing-skills"
      ]
    }
  ]
}
```

### Multiple Plugins Marketplace

Used when grouping related skills:

```json
{
  "plugins": [
    {
      "name": "document-skills",
      "skills": ["./skills/pdf", "./skills/docx"]
    },
    {
      "name": "dev-skills",
      "skills": ["./skills/code-review", "./skills/testing"]
    }
  ]
}
```

Users can install specific plugins:
```bash
/plugin install document-skills@your-marketplace
/plugin install dev-skills@your-marketplace
```

## References

- Official repository: https://github.com/anthropics/skills
- marketplace.json: https://github.com/anthropics/skills/blob/main/.claude-plugin/marketplace.json
- Documentation: https://code.claude.com/docs/en/plugin-marketplaces.md
