---
name: mcp-toolbox
description: Leverage MCP servers for AI-native development with context, automation, and integrations.
---

# MCP Toolbox Skill

Use Model Context Protocol servers to extend AI capabilities beyond code generation.

## When to Use
- Need up-to-date library documentation
- Automating browser tasks or testing
- Database queries without writing SQL
- Breaking down complex problems
- Connecting to external services

## 1. Essential MCP Servers

### Documentation & Context
| MCP Server | Command | Use Case |
|------------|---------|----------|
| **Context7** | `resolve-library-id` → `query-docs` | Get latest library docs, prevent hallucinations |
| **Sequential Thinking** | — | Break complex problems into logical steps |
| **Memory Bank** | — | Retain context across sessions |

### Development Tools
| MCP Server | Use Case |
|------------|----------|
| **GitHub MCP** | Repo management, PR reviews, issue tracking |
| **Filesystem MCP** | Local file read/write/edit operations |
| **Puppeteer MCP** | Browser automation, scraping, UI testing |
| **E2B MCP** | Secure code execution, sandboxing |

### Database & Backend
| MCP Server | Use Case |
|------------|----------|
| **Supabase MCP** | Auth, database, storage, edge functions |
| **PostgreSQL MCP** | Natural language → SQL queries |

### Design & Productivity
| MCP Server | Use Case |
|------------|----------|
| **Figma MCP** | Convert designs to code |
| **Notion MCP** | Access docs, tasks, specs |
| **Slack MCP** | Team notifications, updates |

## 2. Usage Patterns

### Before Coding
```
1. context7: resolve-library-id → query-docs
2. Check for latest syntax/patterns
3. Implement with confidence
```

### Debugging Flow
```
1. Sequential Thinking: break down the problem
2. Context7: verify correct API usage
3. Puppeteer: test in browser if UI issue
```

### Database Work
```
1. Supabase MCP: list_tables, execute_sql
2. Check schema before writing queries
3. Use apply_migration for DDL changes
```

## 3. Quick Reference

```typescript
// Always start with context7 for any library
mcp_context7_resolve-library-id({ libraryName: "react", query: "how to use useEffect" })
mcp_context7_query-docs({ libraryId: "/facebook/react", query: "useEffect cleanup" })

// Supabase operations
mcp_supabase_list_tables({ project_id: "xxx", schemas: ["public"] })
mcp_supabase_execute_sql({ project_id: "xxx", query: "SELECT * FROM users" })
```

## 4. Best Practices

- **Always verify docs first** — Don't assume, use Context7
- **Batch operations** — Combine related MCP calls when possible
- **Check advisors** — Run `get_advisors` after DDL changes
- **Use right tool** — MCP for external integrations, local tools for files

---

> **Cross-reference**: See `best-practices` for UI standards, `vibe-coding` for workflow philosophy.
