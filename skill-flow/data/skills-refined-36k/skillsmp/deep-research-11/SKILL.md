---
name: deep-research
description: Standard operating procedure for exhaustive, recursive deep-dives. Provides protocols for fact-checking, recursive crawling, and multi-vector search to map topics completely.
---

## Research Protocol

1. **Autonomous Deep-Dive**: Explore until the topic is fully mapped. Continue until all questions are answered.
2. **Zero Assumptions**: Verify everything. Find the primary source for every claim. Cross-reference niche data.
3. **Recursive Crawling**: Follow _every_ relevant link. If a page has sub-links, crawl them all.
4. **Multi-Vector Search**: Prioritize the `websearch` tool (Exa AI) for deep, real-time information retrieval. Use 5-10 query variations. If `websearch` or `codesearch` yields insufficient results, switch strategies immediately.
5. **Bypass Blockers**: If `webfetch` is restricted or content is hidden, use `browser_execute` to scroll, click, and interact.
6. **Iterative Note-Taking**: Research → Discover → Write Note → Repeat. Capture insights while fresh.

## Execution Checklist

- [ ] **Crawl everything**: No link left unclicked.
- [ ] **Search everywhere**: Exhaust all tool vectors and query variations using Exa (`websearch`).
- [ ] **Verify [?]**: Immediately prioritize and resolve uncertain findings.
- [ ] **Source URLs**: Mandatory for every finding. Use archives/cache if blocked.
- [ ] **No stop**: Don't check in or pause until the topic is exhausted.

## Note Format

Use YAML frontmatter with tags. Every entry must be timestamped:

```markdown
### [YYYY-MM-DD HH:MM] Finding Title

**Source**: <url>
**Key Points**:

- Point 1
- Point 2
  **Relevance**: <connection to goal>

---
```

## Termination Criteria

Research is complete only when:

1. Every relevant link in every source has been followed.
2. New search queries return no new information.
3. All `[?]` marks are resolved and verified.
4. Every logical "how" and "why" has a documented source.
