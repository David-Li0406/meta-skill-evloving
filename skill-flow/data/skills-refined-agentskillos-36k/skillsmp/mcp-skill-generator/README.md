# MCP Skill Generator

Convert MCP servers into Claude Code skills with progressive disclosure pattern.

## Why Use This?

### 1. Context Window Savings

MCP servers configured directly in Claude Code consume significant context - all tool definitions are loaded into the system prompt immediately. For example, the GitHub MCP server alone consumes ~10k tokens (5% of context).

Skills use **progressive disclosure**: minimal context at startup (just tool names and descriptions), with detailed documentation loaded on demand from `tools/` directory.

### 2. Efficiency - Scripted Batch/Parallel Calls

Traditional MCP tool calling requires AI to call tools one-by-one, each time going through "AI decision → call → result → AI decision" cycles. This is unreliable (AI may skip steps) and token-expensive (every result goes into context).

Generated skills include `api.mjs` for programmatic access:

```javascript
import { callTool } from "./scripts/api.mjs";

// Parallel calls - process results in code, not AI context
const repos = ["facebook/react", "vuejs/vue", "sveltejs/svelte"];
const results = await Promise.all(
  repos.map((repo) =>
    callTool("search_issues", { repo, query: "memory leak" }),
  ),
);

// Return only what's needed
const summary = results.flatMap(
  (r, i) =>
    r.content[0].text.items?.slice(0, 3).map((issue) => ({
      repo: repos[i],
      title: issue.title,
      url: issue.html_url,
    })) ?? [],
);
console.log(JSON.stringify(summary, null, 2));
```

This approach can reduce token consumption by up to **98.7%** ([Anthropic research](https://www.anthropic.com/engineering/code-execution-with-mcp)).

### 3. Version Locking

MCP servers typically run via `npx @some/mcp-server` (always latest version). This means maintainers can push malicious updates at any time.

Skills lock package versions in `config.toml`, preventing supply chain attacks.

## Usage

```
/mcp-skill-generator convert @anthropic/mcp-server-filesystem
/mcp-skill-generator convert https://docs.devin.ai/work-with-devin/deepwiki-mcp
```

The skill will:

1. Fetch MCP server documentation or extract schema directly
2. Ask where to save (project `.claude/skills/` or personal `~/.claude/skills/`)
3. Generate skill files with version locking (when applicable)

## Design Principles

- **Zero runtime dependencies** - All scripts use pure Node.js built-ins
- **Optional authentication** - Missing env vars gracefully skip auth headers
- **Environment variable isolation** - Uses `MCP_<SKILL_NAME>_<VAR>` naming convention
- **AI-friendly API** - `api.mjs` provides simple interface for scripted operations
- **Progressive disclosure** - Follows Claude Code skill best practices

## Updating Skills

To update an existing MCP skill to a newer server version:

1. Run `/mcp-skill-generator`
2. Provide the existing skill's path
3. The generator will check for newer versions and show changes
