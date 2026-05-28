---
name: deepwiki
description: "DeepWiki MCP for GitHub repo docs and Q&A. Use for deepwiki, repo docs, GitHub repository questions, or codebase queries. Load the mcporter skill to execute this skill’s MCP calls."
---

# DeepWiki MCP

Use DeepWiki MCP for public GitHub repo documentation and Q&A.

## Constraints

- Public repos only (private needs Devin account)
- `repoName` must be `owner/repo`

## Suggested flow

1) `read_wiki_structure` for topic map  
2) `read_wiki_contents` for scoped docs  
3) `ask_question` for targeted Q&A  
If empty/insufficient: fall back to Exa/Brave.

## Notes

- `read_wiki_contents` can be large; use `ask_question` for narrow answers.

## Quick start

```bash
read_wiki_structure repoName="owner/repo"
```

## Common calls

```bash
read_wiki_contents repoName="owner/repo"
ask_question repoName="owner/repo" question="..."
```

## Query templates

See `assets/query-templates.json` for reusable parameter templates.

## Reference

See `reference.md` for server URL details, tool catalog, and defaults.
