# Plugin Setup Component

This component guides the installation and configuration of Claude Code plugins.

## Core Principle

> **Context Window Budget**: Plugins add tools like MCPs.
> Keep total tools (base + MCPs + plugins) under 80.

## Setup Flow

### Step 1: Assess Current State

```bash
# Check current plugins
claude plugins list 2>/dev/null || echo "Unable to list plugins"

# Estimate current tool count
# Base: ~25
# MCPs: (count from .mcp.json)
# Plugins: (count from plugins list)
```

### Step 2: Determine Project Needs

Based on tech stack from Phase 3:

| Tech Stack | Recommended Plugins |
|------------|---------------------|
| Any | hookify |
| TypeScript | hookify, typescript-lsp (optional) |
| Python | hookify, pyright-lsp (optional) |
| Large codebase | hookify, mgrep |

### Step 3: Present Recommendations

```
AskUserQuestion: "Install recommended plugins?"
(Multi-select, show context impact)

Based on your TypeScript project:

├── hookify - Create hooks conversationally
│   Impact: ~3 tools (Low)
│   Recommendation: Highly recommended
│
├── typescript-lsp - TypeScript intelligence
│   Impact: ~8 tools (Medium)
│   Recommendation: Optional - useful for complex types
│
└── None - I'll add plugins later

Current context budget:
├── Base tools: ~25
├── MCP tools: ~8
├── Current plugins: 0
└── Available: ~47 tools
```

### Step 4: Install Selected Plugins

```bash
# Install hookify
claude plugins install hookify

# Install typescript-lsp (if selected)
claude plugins install typescript-lsp
```

### Step 5: Verify Installation

```bash
# List plugins to confirm
claude plugins list

# Test hookify
# (User can now use /hookify command)
```

### Step 6: Document in CLAUDE.md

Add to the Plugins section:

```markdown
## Plugins

| Plugin | Purpose | Usage |
|--------|---------|-------|
| hookify | Create hooks conversationally | `/hookify` |
| typescript-lsp | TypeScript intelligence | Automatic |
```

## Plugin Recommendations by Priority

### Always Install

**hookify** (~3 tools)
- Makes hook creation accessible
- Low context impact
- High value for any project

### Consider Based on Tech Stack

**typescript-lsp** (~8 tools)
- TypeScript projects
- Complex type scenarios
- Trade-off: medium context impact

**pyright-lsp** (~8 tools)
- Python projects with type hints
- Similar trade-off to typescript-lsp

### Rarely Needed

**mgrep** (~2 tools)
- Very large codebases only
- Built-in Grep usually sufficient

## Context Window Calculation

Before installing, calculate impact:

```
Current state:
├── Base tools: 25
├── MCP tools: 8 (from .mcp.json)
├── Plugin tools: 0
└── Total: 33

After hookify:
├── Base tools: 25
├── MCP tools: 8
├── Plugin tools: 3
└── Total: 36 ✓

After hookify + typescript-lsp:
├── Base tools: 25
├── MCP tools: 8
├── Plugin tools: 11
└── Total: 44 ✓
```

## Interview Questions

When setting up plugins:

1. **For all projects**:
   ```
   AskUserQuestion: "Install hookify for easier hook creation?"
   ├── Yes (Recommended) - Makes hooks accessible
   └── No - I'll configure hooks manually
   ```

2. **For TypeScript projects**:
   ```
   AskUserQuestion: "Install TypeScript LSP?"
   ├── Yes - I work with complex types
   └── No - Basic TypeScript is fine
   ```

3. **For Python projects**:
   ```
   AskUserQuestion: "Install Python type checker?"
   ├── Yes - I use type hints extensively
   └── No - I don't need type checking
   ```

4. **For large codebases**:
   ```
   AskUserQuestion: "Install enhanced search?"
   ├── Yes - My codebase is large
   └── No - Built-in search is sufficient
   ```

## Managing Plugin State

### Enable/Disable Without Uninstalling

```bash
# Disable temporarily
claude plugins disable typescript-lsp

# Re-enable when needed
claude plugins enable typescript-lsp
```

### When to Disable

- Working on non-TypeScript files (disable typescript-lsp)
- Context window getting tight
- Plugin causing issues

### When to Re-enable

- Back to TypeScript work
- Need the specific functionality
- After removing other tools

## Integration with Other Components

### With MCP Management

Total tools = Base + MCPs + Plugins

If MCPs are heavy (~40 tools), keep plugins minimal (~5 tools).
If MCPs are light (~10 tools), can add more plugins (~20 tools).

### With Hooks Configuration

hookify plugin complements hooks-configuration:
- Plugin: Create hooks conversationally
- Component: Understand hook patterns and templates

### With CLAUDE.md Writing

Document installed plugins:
```markdown
## Installed Plugins

- **hookify**: Use `/hookify` to create hooks
- **typescript-lsp**: Provides TypeScript intelligence (automatic)
```

## Troubleshooting

### Plugin Won't Install

1. Check Claude Code version
2. Check network connectivity
3. Try with verbose flag: `claude plugins install -v <name>`

### Plugin Not Working

1. Restart Claude Code
2. Check plugin is enabled: `claude plugins list`
3. Check for conflicts with other plugins

### Context Window Issues

1. List all plugins: `claude plugins list`
2. Disable non-essential plugins
3. Consider alternatives (CLI tools)

## Output Format

Present plugin status clearly:

```
═══════════════════════════════════════════════════════════════════════════
Plugin Configuration
═══════════════════════════════════════════════════════════════════════════

Installed Plugins:
├── hookify (~3 tools) - Create hooks conversationally
└── typescript-lsp (~8 tools) - TypeScript intelligence

Context Impact:
├── Plugin tools: ~11
├── Total with MCPs: ~36
└── Status: ✓ Healthy (under 80)

Usage:
├── /hookify - Create or modify hooks
└── typescript-lsp - Active automatically
```
