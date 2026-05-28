# DeepWiki MCP Reference

## Server URL

- `https://mcp.deepwiki.com/mcp`

DeepWiki MCP is a remote, no-auth server for public repositories.

## Tool catalog

### read_wiki_structure
Get a list of documentation topics for a GitHub repository.

- `repoName` (required): `owner/repo` (e.g. `facebook/react`)

### read_wiki_contents
View documentation about a GitHub repository.

- `repoName` (required): `owner/repo`

### ask_question
Ask a question about a GitHub repository.

- `repoName` (required): `owner/repo`
- `question` (required): question text

