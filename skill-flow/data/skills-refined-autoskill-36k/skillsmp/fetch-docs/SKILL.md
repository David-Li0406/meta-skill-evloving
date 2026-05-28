---
name: fetch-docs
description:
  Fetch relevant links to docs sites. Use when the user asks to "look up docs", "find documentation for", "get docs for [library]", "check the docs", "/docs", or when Claude needs library/framework documentation to complete a task.
model: claude-haiku-4-5
allowed-tools:
  - ListMcpResourcesTool
  - ReadMcpResourceTool
  - WebFetch
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
---

# Documentation Lookup

Retrieve up-to-date documentation links for libraries and frameworks,
prioritizing org-level best practices before falling back to external sources.

## Workflow

### Step 1: Check Org Docs First

Query the "docs" MCP server for library-specific documentation:

1. Use `ListMcpResourcesTool` with `server: "docs"` to list available resources
2. Look for matching library docs in `org://docs/libraries/` (e.g.,
   `org://docs/libraries/tanstack-query.md`)
3. If found, use `ReadMcpResourceTool` to read the org doc

Org docs contain:

- Best practices and recent updates specific to the organization
- Links to official documentation pages (often in markdown format)

This info might tell you what docs pages are most relevant to the user's
preferences.

### Step 2: Parse and Fetch Linked Documentation

When org docs contain documentation links:

1. If the org docs have a `llms.txt` link, use that to get the list of all docs
   pages, and then find the most relevant nested pages/sections for the user
   task.
1. Use `WebFetch` to retrieve each relevant page, to ensure it has the right
   information for the task.
   - When fetching URLs from `llms.txt`, ALWAYS use the `.md`/`.mdx` extension
     exactly as listed. Never strip the extension! Full HTML pages can be 20x
     larger than the markdown pages.

### Step 3: Fallback for Unknown Libraries

** ONLY PERFORM WEB SEARCH AFTER CHECKING ORG DOCS!! **

If the library is NOT found in org docs:

1. **First, search for llms.txt**: Use `WebSearch` to find
   `[library-name] llms.txt site:[official-domain]` or `[library-name] llms.txt`
   - llms.txt files are AI-optimized documentation indexes
   - If found, fetch and parse for relevant links

2. **Otherwise, use Context7 MCP**:
   - Use `mcp__context7__resolve-library-id` to find the library ID
   - Use `mcp__context7__query-docs` with the user's specific question
   - Extract relevant documentation links from the response

## Output Format

Return results with title/description on one line, URL on the next (avoids word
wrap issues):

```markdown
## Documentation for [Library Name]

**Page Title** — Brief description of what this page covers\
https://example.com/docs/page.md

**Page Title** — Section Name\
https://example.com/docs/page.md#section-id

**Getting Started** — Initial setup and configuration
https://library.dev/docs/getting-started.md

**API Reference - useQuery** — Hook API and options
https://library.dev/docs/api.md#useQuery
```

Each entry should include:

- **Title**: The document or page name (bold)
- **Description**: Brief context about what the page covers (after em dash)
- **URL**: On its own line for easy clicking/copying

## Examples

### Example 1: User asks about tanstack-query mutations docs

**Query**: "How do I use mutations in tanstack-query?"

**Process**:

1. Check org docs → Find `org://docs/libraries/tanstack-query.md`
2. Read org doc → Extract mutation-related links
3. Fetch linked pages → Find sections about mutations
4. Return a list of links and page titles

```markdown
## Documentation for TanStack Query (mutations)

### Sources

**TanStack Query Best Practices** — Org-specific patterns and recommendations
org://docs/libraries/tanstack-query.md

**Mutations** — Creating, updating, and deleting data
https://tanstack.com/query/latest/docs/react/guides/mutations.md

**Mutations - Side Effects** — Running code after mutation success/failure
https://tanstack.com/query/latest/docs/react/guides/mutations.md#mutation-side-effects

**useMutation API Reference** — Hook signature, options, and return values
https://tanstack.com/query/latest/docs/react/reference/useMutation.md

<answer/code-snippets/etc-goes-here>
```

### Example 2: User asks about an unknown library

**Query**: "How do I set up authentication with Lucia?"

**Process**:

1. Check org docs → Not found in `org://docs/libraries/`
2. Search (or use a subagent to search) for llms.txt →
   `WebSearch: "lucia auth llms.txt"`
3. If found, parse llms.txt for auth setup links
4. If not found, use Context7:
   - Resolve library ID for "lucia"
   - Query for authentication setup docs
5. Return relevant links

```markdown
## Documentation for Lucia (authentication)

### Sources

**Getting Started** — Installation and basic setup
https://lucia-auth.com/getting-started.md

**Sessions** — Creating and managing user sessions
https://lucia-auth.com/sessions.md

**Database Setup** — Configuring adapters for your database
https://lucia-auth.com/database.md

<answer-goes-here>
```

## Key Considerations

### Prioritization

1. ALWAYS check org docs first - they contain organization-specific best
   practices; DON'T WASTE CONTEXT DOING WEB SEARCHES BEFORE CHECKING ORG DOCS!
2. When using external sources, prefer `llms.txt` and corresponding `.md`/`.mdx`
   docs pages over regular `.html` docs pages; full HTML pages can be 20x larger

### Header-Level Links

When the user's query is specific:

- Fetch the page content
- Parse headers to find relevant sections
- Construct fragment URLs (e.g., `#getting-started`, `#useQuery`)
- Include both page-level and section-level links

### Handling Multiple Relevant Pages

- Limit to ~2-5 most relevant links
- Order by relevance to the user's query

## Tools Used

- `ListMcpResourcesTool` - List available org docs
- `ReadMcpResourceTool` - Read org documentation
- `WebFetch` - Fetch external documentation pages
- `WebSearch` - Search for llms.txt or documentation
- `mcp__context7__resolve-library-id` - Resolve library to Context7 ID
- `mcp__context7__query-docs` - Query Context7 for documentation
