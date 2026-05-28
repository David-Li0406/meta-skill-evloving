# Research Skill

**Domain**: Codebase Analysis & Project Understanding
**Version**: 1.0
**Created**: 2025-12-09
**Status**: Active

## Overview

The research skill provides systematic workflows for understanding codebases, discovering patterns, and mapping project structure. It consolidates analysis methodologies from project-research-agent and map-file-system command into reusable workflows that any agent can leverage.

## Purpose

Before implementing features or making changes, developers (human or AI) need to:
- Understand existing project structure and conventions
- Discover how similar features are implemented
- Map dependencies and integration points
- Document findings for team knowledge sharing

This skill provides standardized approaches to these research tasks, ensuring comprehensive analysis and consistent documentation.

## Skill Structure

```
research/
├── SKILL.md                         # Router and workflow selection guide
├── README.md                        # This file - skill documentation
├── workflows/
│   ├── analyze-codebase.md         # Comprehensive codebase analysis
│   ├── map-filesystem.md           # Project structure mapping
│   ├── find-patterns.md            # Pattern discovery in code
│   ├── trace-dependencies.md       # Dependency analysis
│   └── understand-feature.md       # Feature-specific analysis
└── context/
    ├── analysis-patterns.md        # Common analysis approaches
    ├── search-strategies.md        # Effective search techniques
    └── documentation-standards.md  # How to document findings
```

## Workflows

### 1. Analyze Codebase (`workflows/analyze-codebase.md`)

**Purpose**: Comprehensive codebase analysis for feature planning or architecture decisions.

**When to use**:
- Starting a new feature and need to understand project conventions
- Preparing for major refactoring
- Onboarding to a new project
- Creating architecture documentation

**Output**: Structured research report with:
- Project structure overview
- Coding standards and conventions
- Technology stack analysis
- Related feature analysis
- Integration points
- Actionable recommendations

**Estimated time**: 30-60 minutes depending on project size

---

### 2. Map Filesystem (`workflows/map-filesystem.md`)

**Purpose**: Generate comprehensive filesystem reference documentation.

**When to use**:
- Creating `/docs/architecture/file-system.md`
- Project onboarding documentation
- Understanding project organization
- Identifying where to add new code

**Output**: Complete filesystem reference with:
- Directory tree structure
- Folder responsibilities and conventions
- Critical files cheat sheet
- Navigation and extension guides

**Estimated time**: 15-30 minutes

---

### 3. Find Patterns (`workflows/find-patterns.md`)

**Purpose**: Discover and document code patterns and naming conventions.

**When to use**:
- Understanding how to implement similar features
- Learning project coding style
- Ensuring consistency with existing code
- Creating coding standards documentation

**Output**: Pattern catalog with:
- Naming conventions (files, functions, classes, etc.)
- Architectural patterns (services, repositories, controllers)
- Code organization patterns
- Examples from codebase

**Estimated time**: 20-40 minutes

---

### 4. Trace Dependencies (`workflows/trace-dependencies.md`)

**Purpose**: Map module dependencies and integration points.

**When to use**:
- Understanding impact of changes
- Planning refactoring scope
- Identifying circular dependencies
- Creating dependency documentation

**Output**: Dependency analysis with:
- Module relationship map
- Integration points
- Shared utilities and services
- Potential coupling issues

**Estimated time**: 30-45 minutes

---

### 5. Understand Feature (`workflows/understand-feature.md`)

**Purpose**: Deep dive into specific feature implementation.

**When to use**:
- Extending existing feature
- Debugging feature behavior
- Understanding specific functionality
- Evaluating modification vs. new code

**Output**: Feature documentation with:
- Complete feature implementation map
- Data flows and transformations
- Extension opportunities
- Risk assessment for modifications

**Estimated time**: 45-90 minutes depending on feature complexity

## Context Files

### analysis-patterns.md
Documents common analysis approaches:
- Breadth-first analysis (overview before depth)
- Pattern matching and comparison
- Dependency tracing strategies
- Data flow analysis
- Architecture layer mapping
- Feature isolation techniques

### search-strategies.md
Effective search techniques using tools:
- Grep patterns for different scenarios
- Glob patterns for file discovery
- Read strategies for large codebases
- Bash commands for directory analysis
- Progressive search refinement
- Avoiding common search pitfalls

### documentation-standards.md
Templates and standards for documenting findings:
- Research report structure
- Evidence citation format
- Recommendation formatting
- Code example conventions
- Integration point documentation
- Knowledge sharing best practices

## Integration Points

### Commands that invoke this skill

- `/map-fs` or `/map` - Quick filesystem mapping (→ map-filesystem workflow)
- `/analyze` - Deep codebase analysis (→ analyze-codebase workflow)
- `/find-pattern` - Pattern search (→ find-patterns workflow)

### Agents that use this skill

**Primary consumer**:
- `project-research-agent` - Dedicated research coordinator

**Secondary consumers**:
- `feature-architect` - Understanding context before design
- `api-developer` - Understanding existing API patterns
- `frontend-developer` - Understanding existing component patterns
- `backend-architect` - Understanding existing backend architecture
- Any agent needing codebase understanding

### Skill dependencies

**This skill supports**:
- `specification-writing` - Research informs PRD creation
- `architecture` - Analysis guides architecture decisions
- `implementation` - Pattern discovery ensures consistency
- `quality` - Understanding enables better code review

**This skill uses**:
- None (foundational skill)

## Tool Requirements

Research workflows require these tools:
- **Read** - File reading
- **Grep** - Content search
- **Glob** - File pattern matching
- **Bash** - Directory operations
- **WebSearch** - Documentation lookup (optional)

All these tools are available in standard Claude Code environment.

## Success Criteria

Research is effective when:
1. **Comprehensive** - All relevant aspects explored
2. **Evidence-based** - Findings cite specific files/code
3. **Actionable** - Recommendations are concrete and implementable
4. **Well-documented** - Findings follow documentation standards
5. **Reproducible** - Others can verify and build on findings
6. **Efficient** - Analysis completes in reasonable time

## Usage Examples

### Example 1: Before Feature Implementation

```markdown
## Before Implementation

1. Research existing patterns:
   - Invoke: `~/.claude/skills/research/workflows/analyze-codebase.md`
   - Focus: Similar features to planned work

2. Document findings:
   - Project conventions identified
   - Integration points mapped
   - Code patterns to follow

3. Proceed with implementation using research insights
```

### Example 2: Project Onboarding

```markdown
## Onboarding Process

1. Map project structure:
   - Invoke: `~/.claude/skills/research/workflows/map-filesystem.md`
   - Output: `/docs/architecture/file-system.md`

2. Analyze codebase:
   - Invoke: `~/.claude/skills/research/workflows/analyze-codebase.md`
   - Output: Architecture overview and conventions

3. Find common patterns:
   - Invoke: `~/.claude/skills/research/workflows/find-patterns.md`
   - Output: Pattern catalog for reference
```

### Example 3: Refactoring Preparation

```markdown
## Refactoring Prep

1. Understand current implementation:
   - Invoke: `~/.claude/skills/research/workflows/understand-feature.md`
   - Target: Feature to refactor

2. Map dependencies:
   - Invoke: `~/.claude/skills/research/workflows/trace-dependencies.md`
   - Identify: Impact scope

3. Plan refactoring:
   - Use research findings to guide approach
   - Ensure consistency with patterns
```

## Best Practices

### Do's

1. **Start broad, then narrow** - Use analyze-codebase before understand-feature
2. **Cite evidence** - Always include file paths and examples
3. **Document as you go** - Don't wait until end to write findings
4. **Use multiple search strategies** - Combine Grep, Glob, and Read
5. **Follow documentation standards** - Use templates from context/
6. **Be systematic** - Complete each analysis phase before moving on

### Don'ts

1. **Don't assume** - Verify patterns by reading actual code
2. **Don't skip documentation** - Undocumented research is wasted effort
3. **Don't analyze in isolation** - Consider how findings inform next steps
4. **Don't ignore inconsistencies** - Document both patterns if project is inconsistent
5. **Don't over-analyze** - Research should inform action, not delay it

## Maintenance

### Adding New Workflows

To add a new research workflow:

1. Create workflow file in `workflows/`
2. Follow existing workflow structure:
   - Goal and scope definition
   - Required tools
   - Systematic exploration steps
   - Documentation template
   - Success criteria
3. Update SKILL.md with workflow description
4. Update this README with workflow documentation
5. Test on real codebase before committing

### Updating Context Files

Context files should evolve based on:
- New analysis techniques discovered
- Improved search strategies
- Better documentation approaches
- Lessons learned from research sessions

## Migration Notes

This skill consolidates:
- **From project-research-agent**: Analysis methodology, pattern recognition, reporting
- **From map-file-system command**: Filesystem mapping logic and structure

These source files remain functional during transition but should be slimmed to reference this skill.

## Version History

**v1.0** (2025-12-09)
- Initial skill creation
- Five core workflows implemented
- Three context files with analysis patterns
- Extracted from project-research-agent and map-file-system command

## Support

For questions or improvements:
- Review existing research outputs for examples
- Check context files for analysis techniques
- Consult SKILL.md for workflow selection guidance
- Test workflows on sample projects before production use
