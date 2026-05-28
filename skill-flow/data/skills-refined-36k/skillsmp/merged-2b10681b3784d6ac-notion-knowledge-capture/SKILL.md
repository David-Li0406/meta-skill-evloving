---
name: notion-knowledge-capture
description: Use this skill to transform conversations and discussions into structured documentation pages in Notion, capturing insights, decisions, and knowledge for easy discovery and reuse.
---

# Knowledge Capture

Convert conversations and notes into structured, linkable Notion pages for easy reuse.

## Quick Start
1. **Clarify what to capture**: Identify the content type (decision, how-to, FAQ, learning, documentation) and target audience.
2. **Locate destination**: Use `Notion:notion-search` to find the appropriate database/template in `reference/` (team wiki, how-to, FAQ, decision log, learning, documentation).
3. **Extract and structure**: Pull relevant context from Notion and extract key information from the conversation, organizing it into the appropriate format.
4. **Create/update in Notion**: Use `Notion:notion-create-pages` to save the structured content, setting necessary properties (title, tags, owner, status, dates, relations).
5. **Link and surface**: Add relations/backlinks to hub pages and related records, ensuring the new content is discoverable.

## Workflow
### 0) Setup Notion MCP
If any MCP call fails due to Notion MCP not being connected, set it up:
1. Add the Notion MCP:
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. Enable remote MCP client:
   - Set `[features].rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
3. Log in with OAuth:
   - `codex mcp login notion`

After successful login, restart codex to continue.

### 1) Define the capture
- Ask about the purpose, audience, freshness, and whether this is new or an update.
- Determine the content type: decision, how-to, FAQ, concept/wiki entry, learning/note, documentation page.

### 2) Locate destination
- Pick the correct database using `reference/*-database.md` guides; confirm required properties (title, tags, owner, status, date, relations).
- If multiple candidate databases exist, ask the user which to use; otherwise, create in the primary wiki/documentation DB.

### 3) Extract and structure
- Extract facts, decisions, actions, and rationale from the conversation.
- For decisions, record alternatives, rationale, and outcomes.
- For how-tos/docs, capture steps, prerequisites, links to assets/code, and edge cases.
- For FAQs, phrase as Q&A with concise answers and links to deeper docs.

### 4) Create/update in Notion
- Use `Notion:notion-create-pages` with the correct `data_source_id`; set properties (title, tags, owner, status, dates, relations).
- Use templates in `reference/` to structure content (section headers, checklists).
- If updating an existing page, fetch then edit via `Notion:notion-update-page`.

### 5) Link and surface
- Add relations/backlinks to hub pages, related specs/docs, and teams.
- Add a short summary/changelog for future readers.
- If follow-up tasks exist, create tasks in the relevant database and link them.

## Content Types
Choose appropriate structure based on content:
- **Concept**: Overview → Definition → Characteristics → Examples → Use Cases → Related
- **How-To**: Overview → Prerequisites → Steps (numbered) → Verification → Troubleshooting → Related
- **Decision**: Context → Decision → Rationale → Options Considered → Consequences → Implementation
- **FAQ**: Short Answer → Detailed Explanation → Examples → When to Use → Related Questions
- **Learning**: What Happened → What Went Well → What Didn't → Root Causes → Learnings → Actions

## Best Practices
1. **Capture promptly**: Document while context is fresh.
2. **Structure consistently**: Use templates for similar content.
3. **Link extensively**: Connect related knowledge.
4. **Write for discovery**: Use searchable titles and tags.
5. **Include context**: Explain why this matters and when to use it.
6. **Add examples**: Concrete examples aid understanding.
7. **Maintain**: Review and update periodically.
8. **Get feedback**: Ask if documentation is helpful.

## Common Issues
- **"Not sure where to save"**: Default to general wiki; can move later.
- **"Content is fragmentary"**: Group related fragments into cohesive documents.
- **"Already exists"**: Search first, update existing if appropriate.
- **"Too informal"**: Clean up language while preserving insights.

## References and Examples
- `reference/` — database schemas and templates (e.g., `team-wiki-database.md`, `how-to-guide-database.md`, `faq-database.md`, `decision-log-database.md`, `documentation-database.md`, `learning-database.md`, `database-best-practices.md`).
- `examples/` — capture patterns in practice (e.g., `decision-capture.md`, `how-to-guide.md`, `conversation-to-faq.md`).