---
name: semantic-search
description: Search code semantically using AG4ONE Serena integration
argument-hint: "<query>"
allowed-tools: [Read, Write, Bash, serena_semantic_search, serena_find_symbol]
platforms: [opencode,claude,gemini]
---

<objective>
Perform semantic code search using AG4ONE Serena integration to find relevant symbols, patterns, and code sections more efficiently than traditional grep-based approaches.

</objective>

<execution_context>
@ag4one/serena/semantic-analysis.md
@AG4-STYLE.md
@.planning/STATE.md
</execution_context>

<context>
Search query: $ARGUMENTS
Platform: $PLATFORM
Available tools: Serena semantic search suite
</context>

<process>
1. **Query Analysis**
   - Parse search intent from $ARGUMENTS
   - Identify relevant symbol types (functions, classes, methods)
   - Determine scope (whole codebase vs specific directories)

2. **Semantic Search Execution**
   - Use Serena semantic search instead of grep
   - Apply intelligent filters for relevance
   - Include context relationships between symbols

3. **Result Processing**
   - Rank results by relevance and relationship strength
   - Present code snippets with full context
   - Include file locations and symbol metadata

4. **Pattern Discovery**
   - Identify related patterns not explicitly searched
   - Suggest additional relevant symbols
   - Document discovered relationships
</process>

<success_criteria>
- [ ] Semantic search completed with relevant results
- [ ] Results ranked by relevance and context
- [ ] Code snippets provided with sufficient context
- [ ] Related patterns and symbols discovered
- [ ] Search findings documented for future reference
- [ ] Token usage optimized vs traditional approaches
</success_criteria>