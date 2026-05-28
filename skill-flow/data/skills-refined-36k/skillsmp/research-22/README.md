# Research Skill

Conduct online research with source attribution, Notion integration, and persistent memory.

## Features

- Web research via Google AI Search
- Notion knowledge base integration
- Persistent memory across sessions (opencode-mem)
- Automatic project organization in `research/` folder
- Structured output with source attribution

## Quick Start

```bash
# Run the setup script from the repository root
./tools/setup-skills.sh research
```

Or set up manually - see [Manual Setup](#manual-setup) below.

## Usage

```
/research <topic>
```

### Examples

```
/research MongoDB Atlas vs self-managed Kubernetes deployment
/research carrier API integration patterns for TMS systems
/research OpenCode skill development best practices
```

## How It Works

```
1. CHECK MEMORY    → Search opencode-mem for prior research
2. CHECK NOTION    → Search Notion knowledge base
3. WEB SEARCH      → Use Google AI Search for new info
4. SYNTHESIZE      → Combine existing + new knowledge
5. STORE           → Save to research/<project>/<date>-<topic>.md
6. REMEMBER        → Add key findings to memory
```

## Output

Files are created at: `research/<project-name>/YYYY-MM-DD-<topic-slug>.md`

```markdown
---
topic: Full Topic Title
date: 2026-01-12
project: project-name
sources_count: 5
status: draft
---

# Topic Title

## Summary
Executive summary...

## Key Findings
1. Finding one
2. Finding two

## Sources
| # | Source | Key Contribution |
|---|--------|------------------|
| 1 | [Title](URL) | What we learned |
```

## Manual Setup

### 1. Install Google AI Search Plugin

```bash
# Install Playwright
npm install -g playwright
npx playwright install chromium

# Clone and build the plugin
mkdir -p ~/.opencode/plugins
git clone https://github.com/IgorWarzocha/Opencode-Google-AI-Search-Plugin.git \
  ~/.opencode/plugins/opencode-google-ai-search
cd ~/.opencode/plugins/opencode-google-ai-search
npm install && npm run build
```

### 2. Install opencode-mem Plugin

```bash
# Install via npm (if available) or add to config
# The plugin is listed in opencode.json plugins array
```

### 3. Set Up Notion Integration (Optional)

1. Go to [Notion Integrations](https://www.notion.so/profile/integrations)
2. Create a new integration
3. Copy the integration token
4. Set environment variable:
   ```bash
   export NOTION_TOKEN="ntn_your_integration_secret_here"
   ```
5. Share relevant Notion pages with your integration

### 4. Verify Configuration

The `.opencode/config.json` should contain:

```json
{
  "plugins": ["opencode-mem"],
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": { "NOTION_TOKEN": "${NOTION_TOKEN}" }
    },
    "google-ai-search": {
      "command": "node",
      "args": ["${HOME}/.opencode/plugins/opencode-google-ai-search/dist/index.js"]
    }
  }
}
```

## Directory Structure

```
research/
├── <project-name>/
│   ├── _index.md              # Project overview
│   ├── 2026-01-12-topic-a.md  # Research documents
│   └── 2026-01-13-topic-b.md
└── <another-project>/
    └── ...
```

## Best Practices

### Source Quality
- Prefer official documentation and academic papers
- Cross-reference claims across multiple sources
- Note when sources disagree

### Organization
- One focused topic per research file
- Use clear, descriptive filenames
- Update project `_index.md` with new findings

### Attribution
- Always include original URLs
- Quote directly when appropriate
- Summarize in your own words for general findings

## Troubleshooting

### Google AI Search not working
- Ensure Playwright and Chromium are installed
- Check that the plugin is built: `ls ~/.opencode/plugins/opencode-google-ai-search/dist/`
- Try running with `DEBUG=true` for more output

### Notion integration not finding pages
- Verify `NOTION_TOKEN` is set correctly
- Ensure pages are shared with your integration
- Share parent pages to include all children

### Memory not persisting
- Check that `opencode-mem` is in the plugins array
- Visit `http://127.0.0.1:4747` to browse stored memories
