---
name: research
description: Systematic codebase analysis and project understanding workflows. Use this skill to analyze project structure, discover patterns, trace dependencies, and understand existing implementations before development work.
domain: codebase-analysis
---

# Research Skill

You are a meticulous technical researcher using the research skill domain. This skill provides systematic approaches to understanding codebases, discovering patterns, and documenting project structure.

## When to Use This Skill

Use research workflows:
- **Before feature implementation** - Understand existing patterns and integration points
- **During architecture** - Analyze codebase structure and conventions
- **For refactoring** - Map dependencies and understand data flows
- **For onboarding** - Build mental model of project organization
- **For documentation** - Create reference materials for team/AI agents

## Available Workflows

### Core Analysis Workflows

1. **analyze-codebase** - `workflows/analyze-codebase.md`
   - Comprehensive codebase analysis and pattern discovery
   - Use for: Feature planning, architecture decisions, refactoring prep
   - Output: Structured research report with findings and recommendations

2. **map-filesystem** - `workflows/map-filesystem.md`
   - Project structure mapping and directory analysis
   - Use for: Creating file-system.md documentation, understanding organization
   - Output: Complete filesystem reference document

3. **find-patterns** - `workflows/find-patterns.md`
   - Pattern discovery and naming convention analysis
   - Use for: Understanding how similar features are implemented
   - Output: Pattern catalog with examples

4. **trace-dependencies** - `workflows/trace-dependencies.md`
   - Dependency analysis and call graph mapping
   - Use for: Understanding module relationships, impact analysis
   - Output: Dependency map with integration points

5. **understand-feature** - `workflows/understand-feature.md`
   - Feature-specific deep dive analysis
   - Use for: Extending existing features, understanding specific functionality
   - Output: Feature documentation with extension recommendations

## Workflow Selection Guide

**For new feature development**:
1. Start with `analyze-codebase` to understand project conventions
2. Use `find-patterns` to locate similar existing features
3. Use `understand-feature` to deeply analyze related functionality
4. Use `trace-dependencies` to map integration points

**For project onboarding**:
1. Start with `map-filesystem` to understand structure
2. Use `analyze-codebase` for comprehensive overview
3. Use `find-patterns` to learn project conventions

**For refactoring**:
1. Use `understand-feature` to map current implementation
2. Use `trace-dependencies` to identify impact scope
3. Use `find-patterns` to ensure consistency

**For documentation creation**:
1. Use `map-filesystem` to generate file-system.md
2. Use `analyze-codebase` to create architecture overview
3. Use `find-patterns` to document coding standards

## Context Files

The research skill provides analysis techniques and standards:

- **analysis-patterns.md** - Common analysis approaches and methodologies
- **search-strategies.md** - Effective search techniques using Grep, Glob, Read
- **documentation-standards.md** - How to document research findings

## Integration with Other Skills

**This skill supports**:
- `specification-writing` - Research informs PRD and epic creation
- `architecture` - Analysis guides architecture decisions
- `implementation` - Pattern discovery ensures consistency
- `quality` - Understanding codebase enables better reviews

**Used by agents**:
- project-research-agent (primary user)
- feature-architect (for context before design)
- api-developer (understanding existing APIs)
- frontend-developer (understanding existing components)

## Tools Required

Research workflows use:
- **Read** - Reading files and documentation
- **Grep** - Content search across codebase
- **Glob** - File pattern matching
- **Bash** - Directory listing and structure analysis
- **WebSearch** - Technology documentation lookup (optional)

## Output Standards

All research workflows should:
1. **Be systematic** - Follow structured exploration steps
2. **Be evidence-based** - Cite file paths and code examples
3. **Be actionable** - Provide clear recommendations
4. **Be documented** - Use templates from context/documentation-standards.md
5. **Be reproducible** - Others can verify findings

## Success Criteria

Research is complete when:
- Project structure is mapped and understood
- Coding conventions are documented with examples
- Similar features are identified and analyzed
- Integration points are clearly identified
- Recommendations are actionable and specific
- Findings are well-documented for future reference

## Workflow Invocation Pattern

```markdown
## Research Phase

1. Invoke research skill workflow:
   - Skill: `~/.claude/skills/research/workflows/analyze-codebase.md`
   - Context: {what you're building}

2. Review research findings

3. Document key patterns and integration points

4. Proceed with design/implementation using research insights
```

## Next Steps

Select the appropriate workflow based on your research goal:
- Comprehensive analysis: Use `workflows/analyze-codebase.md`
- Structure mapping: Use `workflows/map-filesystem.md`
- Pattern discovery: Use `workflows/find-patterns.md`
- Dependency mapping: Use `workflows/trace-dependencies.md`
- Feature understanding: Use `workflows/understand-feature.md`

Refer to context files for analysis techniques and documentation standards.
