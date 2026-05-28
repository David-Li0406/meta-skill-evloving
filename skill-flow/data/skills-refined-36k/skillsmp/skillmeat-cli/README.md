# SkillMeat CLI Skill

Natural language interface for discovering, deploying, and managing Claude Code artifacts. Transform 86+ SkillMeat CLI commands into conversational interactions without memorizing syntax.

## What This Skill Does

The SkillMeat CLI skill bridges the gap between powerful artifact management and natural language. Instead of remembering command syntax, you can use conversational requests:

**What You Say** → **What Happens**
- "Find skills for React testing" → Searches artifact sources and shows relevant skills
- "Deploy canvas to this project" → Adds canvas-design skill to `.claude/skills/local/`
- "What artifacts help with API documentation?" → Searches and suggests API-related skills
- "Update all my skills" → Syncs collection with upstream sources

The skill manages four artifact types:
- **Skills**: Specialized capabilities (PDF processing, testing, design systems)
- **Commands**: Custom CLI commands
- **Agents**: Specialized AI agents for specific tasks
- **MCP Servers**: Claude Model Context Protocol servers for tool integration

## Core Features

### Discovery: Find Artifacts by Intent

Search all available artifact sources using natural language queries. No need to know exact names or paths.

```
"Find database skills"
"What's available for authentication?"
"Show me testing artifacts"
"Search for PDF processing"
```

The skill searches across:
- Official Anthropic artifact marketplace
- Community-contributed sources (configured in your environment)
- GitHub repositories (with proper authentication)

### Deployment: Install with Confirmation

Safe, permission-first deployment ensures you control what gets added to your environment.

**Process**:
1. User requests artifact deployment
2. Skill shows what will be installed (source, version, files)
3. User confirms (explicit permission required)
4. Artifact is deployed to project or collection
5. Confirmation message shows deployment details

**Example**:
```
User: "Deploy the PDF skill"

Skill: "I found anthropics/skills/ms-office-suite:pdf (v2.1.0)
This will add:
  - skillmeat/pdf_processor.py
  - skillmeat/pdf_config.toml
  - docs/pdf-usage.md

Deploy to current project? (yes/no)"

User: "yes"

Skill: "Successfully deployed to .claude/skills/local/
Ready to use! Try: skillmeat show pdf"
```

### Management: Update and Remove Artifacts

Keep artifacts current or remove what you no longer need.

```
"Update the canvas skill"
"Check for updates on all artifacts"
"Remove the old testing framework"
"What changed in the PDF skill?"
```

Includes change detection to show what's different between versions.

### Bundles: Share Complete Setups

Create bundles to package and share complete artifact collections with your team.

```
"Create a bundle with my current setup"
"Import the React development bundle"
"Sign my bundle for distribution"
"Verify bundle signature"
```

Bundles include all metadata, dependencies, and security signatures.

### Templates: Pre-Curated Collections

Four ready-to-use templates for common development stacks:

| Template | Best For | Key Artifacts |
|----------|----------|--------------|
| **React** | React, Next.js frontend | frontend-design, webapp-testing, chrome-devtools |
| **Python** | FastAPI, Django, Flask | openapi-expert, postgresql-psql, pytest-expert |
| **Node.js** | Express, TypeScript backend | webapp-testing, openapi-expert, typescript-config |
| **Full-Stack** | Complete web applications | All of the above, curated for monorepos |

Apply templates with one command:
```
"Apply the React template"
"Show me the Python template first"
"What's in the full-stack template?"
```

## Quick Start

### For Users

**First time?** Initialize your collection:
```bash
skillmeat init
```

**Find what you need:**
```
"Find skills for [your task]"
"What artifacts help with [capability]?"
```

**Deploy to your project:**
```
"Deploy [artifact name]"
```

**Check your setup:**
```
"What artifacts do I have?"
"What's deployed in this project?"
```

### For AI Agents

When you identify a capability gap, use this skill responsibly:

1. **Search** for artifacts matching the need (silently, without announcement)
2. **Suggest** to the user: "This task would benefit from the X skill. Would you like me to add it?"
3. **Show** what will be deployed (file paths, dependencies)
4. **Wait** for explicit permission
5. **Deploy** only approved artifacts

**Never auto-deploy without permission.**

Example agent workflow:
```
Agent detects: User wants to process PDF files
Agent searches: "skillmeat search pdf --type skill"
Agent finds: anthropics/skills/ms-office-suite:pdf
Agent suggests: "I found the PDF skill. Should I add it?"
User confirms: "yes"
Agent deploys: skillmeat deploy ms-office-suite:pdf
```

## Common Operations

### Search for Artifacts

Find exactly what you're looking for without memorizing source names.

```
"Find skills for testing React components"
"Search for database management tools"
"What's available for OpenAPI?"
"Show me authentication artifacts"
```

The skill handles fuzzy matching:
- "pdf" matches `ms-office-suite:pdf`
- "canvas" matches `canvas-design`
- "xlsx" matches `ms-office-suite:xlsx`

### Deploy Multiple Artifacts

Chain deployments for a complete setup:

```
"Deploy the React template, then add the testing skill"
"I want the canvas-design and the PDF skills"
"Apply the full-stack template and add postgres support"
```

### Update Artifacts

Keep your collection current:

```
"Check if there are updates"
"Update the PDF skill"
"Sync everything to latest"
"What changed in the canvas skill?"
```

### Remove Artifacts

Clean up your collection:

```
"Remove the old testing framework"
"Delete the PDF skill"
"Clean up unused artifacts"
```

## AI Agent Integration

This skill is designed to enhance AI agent capabilities through:

### Capability Gap Detection

The skill analyzes project context (package.json, pyproject.toml, imports) to identify when additional artifacts would help:

```
Project has React + TypeScript?
  → Suggest: frontend-design, webapp-testing

Project has FastAPI?
  → Suggest: openapi-expert, postgresql-psql

Project has .claude/ directory?
  → Check what's deployed, suggest complementary artifacts
```

### Context Boosting

When recommending artifacts, the skill matches them to your actual project:

```
React Project → Recommends frontend-design before backend-database
Python API → Recommends openapi-expert first
Full-stack → Recommends both frontend and backend skills
```

### Confidence Scoring

The skill rates recommendations (0-100%) based on:
- Project type match (does your project use this tech?)
- Artifact relevance (does it solve your stated problem?)
- Community ratings (do others find it helpful?)
- Version stability (is it actively maintained?)

Only suggests artifacts with >70% confidence.

### User Rating System

Improve recommendations over time:

```
"Rate the PDF skill 5 stars"
"That skill didn't work, rating it 2 stars"
"Helpful but outdated, 3 stars"
```

Ratings help the skill give better suggestions to you and others.

## File Structure

```
.claude/skills/skillmeat-cli/
├── README.md                    # This file
├── SKILL.md                     # Skill definition (for AI agents)
├── workflows/                   # 12 workflow implementations
│   ├── discovery-workflow.md
│   ├── deployment-workflow.md
│   ├── management-workflow.md
│   ├── bundle-workflow.md
│   ├── gap-detection.md
│   ├── context-boosting.md
│   ├── confidence-integration.md
│   ├── rating-system.md
│   ├── error-handling.md
│   ├── caching.md
│   ├── advanced-integration.md
│   └── agent-self-enhancement.md
├── templates/                   # Pre-curated artifact collections
│   ├── react.toml
│   ├── python.toml
│   ├── nodejs.toml
│   ├── fullstack.toml
│   └── README.md
├── references/                  # Integration and command documentation
│   ├── command-quick-reference.md
│   ├── claudectl-setup.md
│   ├── agent-integration.md
│   └── integration-tests.md
└── scripts/                     # Project analysis utilities
    └── analyze-project.js
```

## Common Questions

### How is this different from using `skillmeat` commands directly?

Direct commands require memorizing syntax and full artifact identifiers. This skill translates natural language into the right commands automatically:

```
Natural Language: "Find skills for PDF processing"
Executes: skillmeat search "pdf" --type skill --json
Parses and presents results conversationally
```

### Can I still use skillmeat commands directly?

Yes! The skill works alongside standard CLI usage. You can:
- Use `skillmeat` directly in your terminal
- Use this skill through Claude Code
- Mix both approaches in your workflow

### What if an artifact isn't found?

The skill will:
1. Try fuzzy matching (e.g., "pdf" → "ms-office-suite:pdf")
2. Suggest similar artifacts
3. Help you search with different terms
4. Recommend adding custom sources if needed

### How do permissions work?

The skill **never auto-deploys**. It always:
1. Shows what will be deployed
2. Explains where it will go
3. Waits for your explicit confirmation
4. Confirms success before proceeding

### Can agents use this skill?

Yes. Agents should:
1. Search silently (don't announce searches)
2. Suggest only when relevant
3. Always wait for user permission
4. Only deploy what was approved

See [agent-integration.md](./references/agent-integration.md) for detailed agent guidelines.

## Claudectl Power Alias

Power users can set up `claudectl` for quicker commands:

```bash
alias claudectl='skillmeat'
```

Then use simplified syntax:
```bash
claudectl search database       # Find database skills
claudectl deploy pdf            # Deploy PDF skill
claudectl status                # List deployed artifacts
claudectl sync                  # Update everything
```

See [claudectl-setup.md](./references/claudectl-setup.md) for smart defaults wrapper.

## Troubleshooting

### "Artifact not found"

Try:
1. Check exact spelling: `"search for [artifact]"`
2. Search with different terms
3. Browse available artifacts: `"list all skills"`
4. Check community sources: `"show available sources"`

### "Permission denied"

Verify:
- Directory permissions on `.claude/`
- Write access to project folder
- GitHub token configured (if private repos): `skillmeat config set github-token <token>`

### "Rate limited by GitHub"

GitHub limits API requests. Solution:
```bash
skillmeat config set github-token <your-token>
```

Get a token at: https://github.com/settings/tokens

### Connection issues

Diagnose environment:
```bash
skillmeat web doctor
```

This checks:
- Network connectivity
- GitHub access
- Required dependencies
- File permissions

## Best Practices

### For Users

1. **Start with templates**: Apply a template for your stack, then customize
2. **Search first**: Use the search workflow to understand what's available
3. **Read descriptions**: Understand what each artifact does before deploying
4. **Rate artifacts**: Your feedback helps improve recommendations
5. **Keep updated**: Run syncs regularly for security and features

### For AI Agents

1. **Never assume permission**: Always ask before deploying
2. **Show changes**: Display what files will be created/modified
3. **Suggest wisely**: Only recommend when there's a clear need
4. **Provide context**: Explain why you're suggesting something
5. **Respect scope**: Use `local` scope for project artifacts, `user` for global

## Support

**Getting Help**:
```bash
skillmeat --help              # General help
skillmeat <command> --help    # Command-specific help
skillmeat web doctor          # Diagnose environment
```

**Documentation**:
- Command reference: [command-quick-reference.md](./references/command-quick-reference.md)
- Agent integration: [agent-integration.md](./references/agent-integration.md)
- Templates: [templates/README.md](./templates/README.md)
- Troubleshooting: [error-handling.md](./workflows/error-handling.md)

**Examples**:
- See [templates/README.md](./templates/README.md) for full setup examples
- See [workflows/](./workflows/) for detailed workflow documentation

## Related Skills

Looking for complementary tools?

- **skill-builder**: Create new skills from scratch
- **skill-creator**: Design skill workflows and specifications
- **chrome-devtools**: Browser automation (example of CLI-wrapper skill)

## Version

Skill Version: 1.0.0
Last Updated: December 2024

Supports SkillMeat CLI v0.3.0+
