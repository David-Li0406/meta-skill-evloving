---
name: execute-sql
description: To read the DB, use mcp-postgres MCP tools
disable-model-invocation: true
---
To read the DB, use `mcp-postgres` MCP tools.

**Plan B - If MCP tools unavailable or timeout:**
- Use `psql` CLI as fallback. The project's connection string can be extracted with `cat .cursor/mcp.json | grep -oP '(?<="DATABASE_URI": ")[^"]*' | head -n1`
Then execute queries with: `psql "$DATABASE_URI" -c "SELECT ..."`
- Most DATABASE_URI from mcp.json include the search_path in the options parameter. Keep it implicit.
