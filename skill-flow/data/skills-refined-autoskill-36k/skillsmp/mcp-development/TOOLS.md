# MCP Tool Creation Guide

## Tool Template

```typescript
import { z } from "zod";

// 1. Define input schema with detailed descriptions
const inputSchema = z.object({
  requiredParam: z.string()
    .min(1)
    .describe("Description of required parameter"),

  optionalParam: z.string()
    .optional()
    .describe("Description of optional parameter"),

  paramWithDefault: z.number()
    .int()
    .positive()
    .max(1000)
    .default(100)
    .describe("Parameter with default (default: 100, max: 1000)"),

  enumParam: z.enum(["option1", "option2", "option3"])
    .default("option1")
    .describe("Choose from: option1, option2, option3"),
});

// 2. Register the tool
server.registerTool(
  "tool_name", // snake_case, descriptive
  {
    description: `Brief description of what the tool does.

When to use:
- Use case 1
- Use case 2

Limitations:
- Limitation 1
- Limitation 2`,
    inputSchema,
  },
  async (args) => {
    try {
      // 3. Implement handler
      const result = await operation(args);

      // 4. Return formatted result
      return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        structuredContent: result,
      };
    } catch (error) {
      // 5. Error handling
      return {
        content: [{
          type: "text",
          text: `Error: ${error instanceof Error ? error.message : "Unknown error"}`
        }],
        isError: true,
      };
    }
  }
);
```

## Common Tool Patterns

### Query/Read Tool
```typescript
server.registerTool(
  "resource_get",
  {
    description: "Retrieve a resource by ID",
    inputSchema: z.object({
      id: z.string().describe("Resource ID"),
    }),
  },
  async ({ id }) => {
    const result = await repository.findById(id);
    if (!result) {
      return {
        content: [{ type: "text", text: `Resource ${id} not found` }],
        isError: true,
      };
    }
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result,
    };
  }
);
```

### List Tool with Pagination
```typescript
server.registerTool(
  "resources_list",
  {
    description: "List resources with filtering and pagination",
    inputSchema: z.object({
      filter: z.string().optional().describe("Filter expression"),
      limit: z.number().int().positive().max(100).default(20)
        .describe("Max results (default: 20, max: 100)"),
      offset: z.number().int().nonnegative().default(0)
        .describe("Skip N results for pagination"),
    }),
  },
  async ({ filter, limit, offset }) => {
    const results = await repository.list({ filter, limit, offset });
    const total = await repository.count({ filter });

    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
      structuredContent: {
        items: results,
        count: results.length,
        total,
        hasMore: offset + results.length < total,
      },
    };
  }
);
```

### SQL Query Tool
```typescript
server.registerTool(
  "sql_select",
  {
    description: `Execute a read-only SQL SELECT query.

When to use:
- Retrieve data from tables
- Run aggregate queries (COUNT, SUM, AVG)
- Join multiple tables

Limitations:
- Only SELECT queries allowed
- Maximum 1000 rows returned
- 30 second timeout`,
    inputSchema: z.object({
      query: z.string().describe("SQL SELECT query with @param placeholders"),
      params: z.record(z.unknown()).default({})
        .describe("Named parameters (without @)"),
      limit: z.number().int().positive().max(1000).default(100)
        .describe("Max rows (default: 100, max: 1000)"),
    }),
  },
  async ({ query, params, limit }) => {
    // Validate query is SELECT only
    const normalized = query.trim().toLowerCase();
    if (!normalized.startsWith("select")) {
      return {
        content: [{ type: "text", text: "Only SELECT queries are allowed" }],
        isError: true,
      };
    }

    const pool = await getPool();
    const request = pool.request();

    for (const [key, value] of Object.entries(params)) {
      request.input(key, value);
    }

    const result = await request.query(query);
    const rows = result.recordset?.slice(0, limit) ?? [];

    return {
      content: [{ type: "text", text: JSON.stringify(rows, null, 2) }],
      structuredContent: { rowCount: rows.length, rows },
    };
  }
);
```

## Naming Conventions

| Type | Pattern | Examples |
|------|---------|----------|
| Query | `{domain}_get`, `{domain}_list` | `user_get`, `orders_list` |
| Action | `{domain}_{verb}` | `user_create`, `order_cancel` |
| Schema | `{domain}_describe`, `{domain}_schema` | `table_describe` |

## Schema Tips

```typescript
// String with pattern
z.string().regex(/^[A-Z]{3}$/).describe("3-letter currency code")

// Array with limits
z.array(z.string()).min(1).max(10).describe("1-10 tags")

// Union types
z.union([z.string(), z.number()]).describe("ID as string or number")

// Transform
z.string().transform(s => s.toLowerCase()).describe("Case-insensitive input")
```
