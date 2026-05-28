---
name: oss-research
description: Research OSS libraries and frameworks using DeepWiki MCP. Use for understanding APIs, finding usage examples, investigating implementation details, comparing libraries, and troubleshooting OSS-related issues.
context: fork
agent: general-purpose
---

# OSS Research Skill

Research open-source libraries and frameworks with evidence-based responses using DeepWiki MCP.

## Core Principles

1. **Never guess**: Always verify with DeepWiki before responding
2. **Cite sources**: Include repository and documentation references
3. **Prefer fresh data**: Use MCP-fetched information over potentially outdated training data
4. **Explore structure first**: Understand documentation layout before diving into specifics

## MCP Tools to Use

### DeepWiki (Primary)
- `mcp__deepwiki__read_wiki_structure`: Get documentation structure of a repository
- `mcp__deepwiki__read_wiki_contents`: Read specific documentation pages
- `mcp__deepwiki__ask_question`: Ask questions about a repository

### Google Search (Supplementary)
- `mcp__gemini-google-search__google_search`: Find additional resources, blog posts, community discussions

## Research Workflow

1. **Identify repository**: Determine the GitHub `owner/repo` format
2. **Explore structure**: Use `read_wiki_structure` to understand available docs
3. **Read relevant sections**: Use `read_wiki_contents` for specific topics
4. **Ask focused questions**: Use `ask_question` for complex queries
5. **Supplement if needed**: Use Google search for community insights

## Supported Tasks

### Library Research
- API documentation and usage patterns
- Configuration options and defaults
- Migration guides between versions
- Comparison with alternatives

### Implementation Guidance
- Best practices and recommended patterns
- Common pitfalls and how to avoid them
- Performance considerations
- Security implications

### Troubleshooting
- Error message interpretation
- Known issues and workarounds
- Debugging strategies
- Community-reported solutions

### Integration Research
- How libraries work together
- Compatibility matrices
- Plugin/extension ecosystems

## Common Repository Formats

| Category | Example Repositories |
|----------|---------------------|
| Frontend | `facebook/react`, `vuejs/vue`, `sveltejs/svelte` |
| Backend | `expressjs/express`, `fastify/fastify`, `pallets/flask` |
| Database | `prisma/prisma`, `typeorm/typeorm`, `drizzle-team/drizzle-orm` |
| Testing | `jestjs/jest`, `vitest-dev/vitest`, `pytest-dev/pytest` |
| Build | `vitejs/vite`, `webpack/webpack`, `esbuild/esbuild` |
| Infra | `hashicorp/terraform`, `pulumi/pulumi`, `kubernetes/kubernetes` |
| Language | `rust-lang/rust`, `golang/go`, `python/cpython` |

## Response Format

```
## Answer

[Response to the question]

## Sources

- Repository: [owner/repo]
- Documentation: [specific pages referenced]
- Additional: [any supplementary sources]

## Code Examples (if applicable)

[Relevant code snippets from documentation]

## Additional Notes

- Version considerations
- Alternative approaches
- Related libraries
```

## Task: $ARGUMENTS

Research the following OSS-related question:

$ARGUMENTS

You MUST use DeepWiki MCP to gather evidence before responding. Identify the relevant repository first.
