---
name: hub-tool-mgmt
description: Create and register MCP tools for the Hub. Use when adding new tools that should be available via Claude Desktop/Bridge, or when linking existing tools with their skills for maintainability.
---

# Hub Tool Management

Create, register, and maintain MCP tools for the Hub ecosystem.

## Overview

Tools and Skills are complementary but distinct:

| Component | Location | Purpose | Consumer |
|-----------|----------|---------|----------|
| **Tool** | `services/hub/src/tools/*.cjs` | Executable code with MCP schema | Claude Desktop, ChatGPT Bridge |
| **Skill** | `skills/*/SKILL.md` | Workflow guide for AI agents | Claude Code (IDE) |
| **Tool Registry** | `services/hub/src/tools/registry.cjs` | Registration for user endpoints | Hub runtime |

A Tool can exist without a Skill (simple tools), but complex tools benefit from both.

## Creating a New Tool

### Step 1: Create Tool File

```javascript
// services/hub/src/tools/my-tool.cjs
const { z } = require("zod");

async function myToolHandler(params, config) {
  // Implementation
  return { success: true, data: result };
}

function registerMyTools(server, config = {}) {
  const enabled = config.enabled ?? process.env.MY_TOOL_ENABLED === 'true';

  if (!enabled) {
    console.warn("ℹ️  My Tool disabled");
    return null;
  }

  // Define schema with descriptions - THIS IS THE DOCUMENTATION
  const inputShape = {
    operation: z.enum(["action1", "action2"])
      .describe("The operation to perform"),
    param1: z.string()
      .describe("Description of param1"),
    param2: z.number()
      .optional()
      .describe("Optional param2 (default: 10)")
  };

  server.registerTool(
    "my_tool",  // Tool name
    {
      title: "My Tool",
      description: `Full description of what this tool does.

## Available Operations
- \`action1\` - Does X (requires: param1)
- \`action2\` - Does Y (requires: param1, param2)

## Examples
\`\`\`json
{ "operation": "action1", "param1": "value" }
\`\`\``,
      inputSchema: inputShape,
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        openWorldHint: true
      }
    },
    async (args) => {
      const validated = z.object(inputShape).parse(args);
      const result = await myToolHandler(validated, config);
      return {
        content: [{
          type: "text",
          text: JSON.stringify(result, null, 2)
        }]
      };
    }
  );

  console.log("✅ My Tool initialized");
  return { myToolHandler };
}

module.exports = { registerMyTools, myToolHandler };
```

### Step 2: Register in registry.cjs

```javascript
// 1. Add import at top
const { registerMyTools } = require("./my-tool.cjs");

// 2. Add to registerAllTools function
registerMyTools(server, { enabled: config.MY_TOOL_ENABLED });
```

### Step 3: Deploy

```bash
git add services/hub/src/tools/my-tool.cjs services/hub/src/tools/registry.cjs
git commit -m "feat(tools): Add My Tool"
docker compose restart hub
```

## Tool Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Hub core tools | `{action}` | `ping`, `list_tools` |
| Service tools | `{service}_{action}` | `n8n_list_workflows` |
| Proxied MCP tools | `invoke_{service}_tool` | `invoke_notion_tool` |

## Tool Description Best Practices

The `description` in `registerTool()` is what Claude sees. Make it actionable:

1. **Start with what it does** (one sentence)
2. **List available operations** with required/optional params
3. **Include examples** - JSON that can be copy-pasted
4. **Mention limitations** if any

## Checklist: New Tool

- [ ] Tool file created in `services/hub/src/tools/`
- [ ] Zod schema with `.describe()` for all params
- [ ] Full description with operations and examples
- [ ] Registered in `registry.cjs`
- [ ] Environment toggle added (if optional)
- [ ] Deployed and health check shows new tool
- [ ] (Optional) Skill created with `tool:` frontmatter
