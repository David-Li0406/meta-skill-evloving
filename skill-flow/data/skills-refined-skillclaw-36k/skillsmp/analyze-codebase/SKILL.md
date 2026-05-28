---
name: analyze-codebase
description: Perform semantic codebase analysis using Serena integration
argument-hint: "[directory]"
allowed-tools: [Read, Write, Bash, Glob, Grep, AskUserQuestion, serena_find_symbol, serena_semantic_search]
platforms: [opencode,claude,gemini]
---

<objective>
Analyze codebase structure semantically using AG4ONE Serena integration to create comprehensive understanding of project architecture, patterns, and relationships.

</objective>

<execution_context>
@ag4one/serena/semantic-analysis.md
@AG4-STYLE.md
@.planning/STATE.md
</execution_context>

<context>
Current directory: $ARGUMENTS
Platform: $PLATFORM
Available tools: Serena semantic analysis suite
</context>

<process>
1. **Discover Codebase Structure**
   - Use Serena to find all symbols (classes, functions, methods)
   - Map relationships and dependencies between components
   - Identify architectural patterns and conventions

2. **Create Semantic Index**
   - Generate comprehensive symbol catalog
   - Document component hierarchies
   - Store in `SERENA-ANALYSIS.md`

3. **Pattern Recognition**
   - Identify design patterns used in codebase
   - Document common conventions and idioms
   - Note framework-specific patterns

4. **Documentation Update**
   - Update AGENTS.md with discovered patterns
   - Create architectural overview
   - Store semantic findings for future reference
</process>

<success_criteria>
- [ ] Comprehensive symbol catalog created
- [ ] Code relationships mapped and documented
- [ ] Architectural patterns identified
- [ ] SERENA-ANALYSIS.md generated with semantic index
- [ ] Project knowledge preserved in AGENTS.md files
- [ ] Findings ready for AG4ONE workflows to use
</success_criteria>