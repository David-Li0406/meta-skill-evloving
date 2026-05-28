---
name: notion-knowledge-capture
description: Use this skill to transform conversations and discussions into structured documentation pages in Notion, capturing insights, decisions, and knowledge for easy organization and discovery.
---

# Knowledge Capture

Convert conversations and notes into structured, linkable Notion pages for easy reuse and discovery.

## Quick Start
1. **Clarify what to capture**: Determine the purpose (decision, how-to, FAQ, learning, documentation) and target audience.
2. **Identify the right database/template**: Use `reference/` to find the appropriate database (team wiki, how-to, FAQ, decision log, learning, documentation).
3. **Extract content**: Pull key information from the conversation context, including facts, decisions, actions, and rationale.
4. **Structure the information**: Organize the extracted content into the appropriate documentation format, using templates for consistency and including relevant metadata.
5. **Create/update in Notion**: Use `Notion:notion-create-pages` to save the structured content, setting properties like title, tags, and owner.
6. **Make content discoverable**: Link the new page from relevant hub pages and update navigation to ensure others can find it.

## Workflow
### 0) Setup Notion MCP
If any MCP call fails because Notion MCP is not connected, set it up:
1. Add the Notion MCP:
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. Enable remote MCP client:
   - Set `[features].rmcp_client = true` in `config.toml` or run `codex --enable rmcp_client`
3. Log in with OAuth:
   - `codex mcp login notion`
After successful login, restart codex.

### 1) Define the capture
- Ask about the purpose, audience, freshness, and whether this is new or an update.
- Determine the content type: decision, how-to, FAQ, concept/wiki entry, learning/note, documentation page.

### 2) Locate destination
- Pick the correct database using `reference/*-database.md` guides; confirm required properties (title, tags, owner, status, date, relations).
- If multiple candidate databases exist, ask the user which to use; otherwise, create in the primary wiki/documentation DB.

### 3) Extract and structure
- For decisions, record alternatives, rationale, and outcomes.
- For how-tos/docs, capture steps, prerequisites, links to assets/code, and edge cases.
- For FAQs, phrase as Q&A with concise answers and links to deeper documentation.

### 4) Create the page
- Use `Notion:notion-create-pages` with the correct `data_source_id`; set properties (title, tags, owner, etc.).

### 5) Make discoverable
- Link from hub pages and related records; update status/owners as the source evolves.