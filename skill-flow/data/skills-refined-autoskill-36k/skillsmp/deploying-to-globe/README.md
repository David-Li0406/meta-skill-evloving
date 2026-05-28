# Globe Deployment Skill

Enables AI coding agents to deploy Dart and Flutter applications to [Globe.dev](https://globe.dev), a serverless deployment platform with 300+ edge locations.

## What This Skill Does

When installed, your AI agent can:

- Guide you through deploying Dart Frog, Shelf, Flutter, Jaspr, and Serverpod apps
- Configure `globe.yaml` for cron jobs, static assets, and preferred regions
- Set up Globe KV (key-value store), Globe DB (SQLite), and Globe AI
- Troubleshoot common deployment errors (413, 503, CORS, domain issues)
- Provide accurate CLI commands and code patterns

## Installation

See [Installation instructions](../../README.md#installation) in the main README for Claude Code, OpenAI Codex, GitHub Copilot, Cursor, Cline, and Windsurf.

## Verification

Start a new agent session and ask:

```
"How do I deploy this Shelf app to Globe?"
```

**With skill:** Agent provides Globe-specific guidance (PORT env var, `globe deploy`, etc.)

**Without skill:** Agent gives generic deployment advice

## What's Included

```
skills/globe/
├── SKILL.md              # Main skill (430 lines)
├── README.md             # This file
├── references/           # 77 detailed documentation files
│   ├── getting-started/
│   ├── core-concepts/
│   ├── frameworks/
│   ├── products/
│   ├── infrastructure/
│   ├── guides/
│   ├── tutorials/
│   └── troubleshooting/
└── scripts/
    └── validate-globe-yaml.sh  # Validates globe.yaml syntax
```

## Key Topics Covered

| Category | Topics |
|----------|--------|
| **Deployment** | CLI commands, preview vs production, GitHub integration |
| **Configuration** | globe.yaml, environment variables, build presets |
| **Products** | Globe KV, Globe DB, Globe AI |
| **Infrastructure** | Regions, cold starts, resource limits, caching |
| **Frameworks** | Dart Frog, Shelf, Flutter Web, Jaspr, Serverpod |

## Validation Script

If you have a `globe.yaml` file, validate it:

```bash
bash ~/.claude/skills/globe/scripts/validate-globe-yaml.sh globe.yaml
```

Checks for:
- YAML syntax errors (tabs, missing spaces)
- Valid preset types
- Valid region names
- Cron job ID format and required fields

## Updating

To update to the latest version:

```bash
rm -rf ~/.claude/skills/globe
cp -r skills/globe ~/.claude/skills/
```

## Links

- [Globe.dev](https://globe.dev)
- [Globe Documentation](https://docs.globe.dev)
- [globe.yaml Schema](https://globe.dev/globe.schema.json)
