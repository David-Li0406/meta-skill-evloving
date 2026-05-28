---
name: research
description: Conduct thorough research on any topic with proper citations. Use when (1) gathering information from web sources or academic papers, (2) user asks to "research", "investigate", or "find information about" a topic, (3) creating documented findings with sources, (4) comparing options or technologies with evidence.
---

# Research Workflow

## Process

1. **Clarify scope** - Understand what information is needed and the desired depth
2. **Gather sources** - Use WebSearch, WebFetch, and arXiv as appropriate
3. **Analyze and synthesize** - Extract key findings, identify patterns
4. **Document with citations** - Present findings with proper source attribution

## Tool Selection

- **WebSearch** - Current information, news, general topics
- **WebFetch** - Deep dive into specific pages, documentation
- **arXiv** - Academic papers, research studies, technical depth
- **Chrome DevTools** - JS-rendered content that WebFetch can't access
- **Sequential Thinking** - Complex multi-faceted research requiring structured reasoning

## For Complex Research

Use sequential thinking tool when:
- Multiple competing hypotheses need evaluation
- Information from many sources needs synthesis
- Trade-offs require systematic analysis
- The research question has unclear scope

## Parallel Research

For broad topics with multiple facets, spawn parallel Explore agents using the Task tool:
- Each agent investigates one angle, source type, or subtopic
- Agents run concurrently to gather information faster
- Synthesize results after all agents complete

Example: Researching "state of LLM agents 2025" could spawn parallel agents for:
- Academic papers (arXiv)
- Industry reports and blog posts
- Open source projects and GitHub trends

## Citation Format

Present sources clearly. For academic papers:

```
**Author(s)** (Year). "Title." _Journal_, Volume(Issue), pages.
- DOI: [DOI number]
- Link: [Direct link]
```

For web sources:

```
**Source Name** - [Title](URL)
Brief description of what this source provides.
```

## Quality Standards

See [references/quality-standards.md](references/quality-standards.md) for detailed documentation standards.

## Output

End research with:
1. **Summary** - Key findings in 2-3 sentences
2. **Detailed findings** - Organized by theme or question
3. **Sources** - All citations with working links

## Saving Research

When user wants to save findings, write to `./research/`:
- Filename: `{topic}-{YYYY-MM-DD}.md` (kebab-case)
- Include all citations and sources
- Ask user before saving if not explicitly requested
