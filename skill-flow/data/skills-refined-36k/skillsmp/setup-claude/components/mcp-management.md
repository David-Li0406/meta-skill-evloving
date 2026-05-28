# MCP Management Component

This component guides MCP configuration with a focus on context window management.

## Core Principle

> **Context Window is Precious**: Each MCP adds tool definitions to your context.
> - Recommended: Under 10 MCPs enabled
> - Recommended: Under 80 total tools active
> - **CLI-First**: Only use MCP when no CLI exists

## When to Use MCP vs CLI

| Scenario | Use MCP | Use CLI |
|----------|---------|---------|
| Service has CLI | No | Yes |
| Documentation lookup | Yes (context7) | N/A |
| UI component reference | Yes (shadcn) | N/A |
| Database operations | No | Yes (supabase, convex) |
| Deployment | No | Yes (vercel, netlify) |
| Payments | No | Yes (stripe) |
| Version control | No | Yes (gh) |

## MCP Configuration

### Project-Level Configuration

Create `.mcp.json` in project root:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/context7-mcp"]
    }
  },
  "disabledMcpServers": []
}
```

### Global Configuration

Located at `~/.claude/.mcp.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    }
  },
  "disabledMcpServers": []
}
```

## Context Window Impact

### Typical Tool Counts per MCP

| MCP | Approximate Tools | Use Case |
|-----|-------------------|----------|
| context7 | ~5 | Framework documentation |
| shadcn | ~3 | UI component documentation |
| filesystem | ~10 | File system operations |
| github | ~20 | GitHub operations |
| supabase | ~15 | Database operations |
| stripe | ~15 | Payment operations |
| memory | ~5 | Persistent memory |

### Calculating Total Tools

```
Base Claude tools: ~25
+ MCP tools: (sum of enabled MCPs)
+ Plugin tools: (sum of enabled plugins)
= Total context window tools
```

**Target**: Total < 80 tools

### Example Calculation

```
Base tools:        25
+ context7:         5
+ shadcn:           3
+ filesystem:      10
───────────────────────
Total:             43 ✓ (healthy)
```

vs.

```
Base tools:        25
+ context7:         5
+ shadcn:           3
+ filesystem:      10
+ github:          20
+ supabase:        15
+ stripe:          15
+ memory:           5
───────────────────────
Total:             98 ⚠ (exceeds 80)
```

## Setup Flow

### Step 1: Audit Current MCPs

```bash
# Check project MCPs
cat .mcp.json 2>/dev/null || echo "No project MCPs"

# Check global MCPs
cat ~/.claude/.mcp.json 2>/dev/null || echo "No global MCPs"

# Count enabled MCPs
cat .mcp.json 2>/dev/null | grep -c '"command"' || echo "0"
```

### Step 2: Identify Redundant MCPs

For each enabled MCP, check if CLI alternative exists:

```
MCP Redundancy Check:
├── supabase MCP → CLI available (supabase) → REMOVE MCP
├── stripe MCP → CLI available (stripe) → REMOVE MCP
├── github MCP → CLI available (gh) → REMOVE MCP
├── context7 MCP → No CLI → KEEP
└── shadcn MCP → No CLI → KEEP
```

### Step 3: Present Recommendations

```
AskUserQuestion: "Configure MCPs?"

Current state:
- MCPs enabled: 7
- Estimated tools: ~78

Recommendations:
1. Keep: context7, shadcn (no CLI alternatives)
2. Remove: supabase, stripe, github (CLI available)
3. Result: 4 MCPs, ~43 tools

Options:
├── "Apply recommendations"
├── "Let me choose"
└── "Keep current setup"
```

### Step 4: Create/Update .mcp.json

For new projects:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/context7-mcp"]
    }
  },
  "disabledMcpServers": []
}
```

For existing projects with redundant MCPs:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/context7-mcp"]
    },
    "shadcn": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/shadcn-mcp"]
    }
  },
  "disabledMcpServers": [
    "supabase",
    "stripe",
    "github"
  ]
}
```

## Recommended MCPs

### Essential (Low Impact)

| MCP | Tools | Purpose | When to Use |
|-----|-------|---------|-------------|
| context7 | ~5 | Framework documentation | Using any framework |
| shadcn | ~3 | UI component documentation | Using shadcn/ui |

### Situational (Consider Carefully)

| MCP | Tools | Purpose | Alternative |
|-----|-------|---------|-------------|
| filesystem | ~10 | File operations outside project | Usually not needed |
| memory | ~5 | Persistent memory | Usually not needed |

### Avoid (Use CLI Instead)

| MCP | Tools | CLI Alternative |
|-----|-------|-----------------|
| github | ~20 | `gh` |
| supabase | ~15 | `supabase` |
| stripe | ~15 | `stripe` |
| vercel | ~10 | `vercel` |
| netlify | ~10 | `netlify` |

## Disabling MCPs

To disable an MCP without removing it:

```json
{
  "mcpServers": { ... },
  "disabledMcpServers": [
    "mcp-name-to-disable"
  ]
}
```

This keeps the configuration but prevents loading.

## Troubleshooting

### MCP Not Loading

1. Check command path: `which npx`
2. Check package exists: `npm view @package/name`
3. Check for typos in args
4. Restart Claude Code after config changes

### Too Many Tools Warning

If you see context window warnings:

1. Count enabled MCPs
2. Identify redundant MCPs (have CLI alternatives)
3. Move to `disabledMcpServers`
4. Restart Claude Code

### MCP Conflicts

If MCPs provide overlapping functionality:

1. Prefer CLI over MCP
2. Prefer project MCP over global MCP
3. Disable the redundant one

## Integration with Other Components

- **CLI Discovery**: Check CLI availability before enabling MCP
- **CLAUDE.md Writing**: Document enabled MCPs and their usage
- **Plugin Setup**: Consider total tool count from MCPs + plugins

## Output Format

Present MCP status clearly:

```
═══════════════════════════════════════════════════════════════════════════
MCP Configuration Summary
═══════════════════════════════════════════════════════════════════════════

Enabled MCPs: 3
├── context7 (~5 tools) - Framework documentation
├── shadcn (~3 tools) - UI components
└── memory (~5 tools) - Persistent memory

Disabled MCPs: 2
├── github - Using gh CLI instead
└── supabase - Using supabase CLI instead

Context Window Impact:
├── MCP tools: ~13
├── Estimated total: ~38
└── Status: ✓ Healthy (under 80)
```
