# Exa MCP Reference

## Server URL

- Base: `https://mcp.exa.ai/mcp`
- Enable tools via query param:
  - `https://mcp.exa.ai/mcp?tools=web_search_exa,get_code_context_exa`
- Enable all tools:
  - `https://mcp.exa.ai/mcp?tools=web_search_exa,web_search_advanced_exa,deep_search_exa,get_code_context_exa,crawling_exa,company_research_exa,linkedin_search_exa,deep_researcher_start,deep_researcher_check`
- API key (optional): `https://mcp.exa.ai/mcp?exaApiKey=YOUR_KEY`

**Default enabled tools:** `web_search_exa`, `get_code_context_exa`, `company_research_exa`. Others require the `tools` param.

## Tool catalog

### Enabled by default
- **web_search_exa**: Web search with clean content. Key params: `query`, `numResults`, `type`, `contextMaxCharacters`.
- **get_code_context_exa**: Code-focused search over repos/docs/StackOverflow. Key params: `query`, `tokensNum`.
- **company_research_exa**: Company research summaries. Key params: `companyName`, `numResults`.

### Available (enable via `tools`)
- **web_search_advanced_exa**: Advanced search with filters (category, domain, date, highlights, summaries, subpage crawling).
- **deep_search_exa**: Deep web search with expanded queries and summaries.
- **crawling_exa**: Fetch content from a specific URL. Key params: `url`, `maxCharacters`.
- **linkedin_search_exa**: People search on LinkedIn. Key params: `query`, `numResults`.
- **deep_researcher_start**: Start a deep research job. Key params: `instructions`, `model` (`exa-research` | `exa-research-pro`).
- **deep_researcher_check**: Poll for deep research completion. Key param: `taskId`.

