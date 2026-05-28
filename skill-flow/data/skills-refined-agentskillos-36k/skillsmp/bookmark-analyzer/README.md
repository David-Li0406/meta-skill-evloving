# Bookmark Analyzer Skill

Context-forking skill for comprehensive Bookmark Vault codebase analysis from multiple perspectives simultaneously.

## Quick Start

Use the skill to analyze the codebase comprehensively:

```bash
# Using Claude Code CLI
claude "Analyze the bookmark vault codebase comprehensively"

# Or invoke the skill directly via Skill tool
Skill → bookmark-analyzer
```

## What It Does

Spawns three isolated analysis forks that run in parallel:

1. **Component Structure Analysis** - Maps component hierarchy, counts inventory, analyzes reusability and size distribution
2. **Data Flow Analysis** - Traces state flow from storage to UI, documents prop drilling, identifies hook dependencies
3. **Type Coverage Analysis** - Validates TypeScript strict mode, checks Zod schema alignment, identifies type gaps

Results merge into a unified report with:
- **Cross-Section Implications** - Observations connecting findings across the three analysis areas
- **Prioritized Recommendations** - Actionable improvements with effort estimates and file locations
- **Overall Assessment Score** - Codebase quality metric with supporting evidence

## Key Features

✅ **Isolated Contexts** - Each fork runs independently to prevent cross-contamination of findings
✅ **Structured Output** - Three analysis areas → synthesis → cross-section implications → recommendations
✅ **Metrics & Evidence** - All findings backed by specific metrics, file references, and line numbers
✅ **Discipline Enforcement** - Red flags and rationalization blocking ensure methodical analysis
✅ **Comprehensive** - Covers architecture, data flow, and type safety in single analysis pass

## Files in This Skill

- **SKILL.md** - Main skill documentation with analysis patterns, output formats, and success criteria
- **TEST-RESULTS.md** - Complete TDD test documentation showing baseline testing, skill compliance, and loophole analysis
- **README.md** - This file

## How It Works

The skill uses a structured analysis pattern:

```
Input: "Analyze bookmark vault comprehensively"
    ↓
Fork 1: Component Structure
├─ Search components/ directory
├─ Count by category (UI, features, etc.)
├─ Map parent-child relationships
└─ Analyze size distribution

Fork 2: Data Flow (parallel)
├─ Trace storage → hooks → components
├─ Document prop drilling paths
├─ Map hook dependencies
└─ Identify refresh mechanisms

Fork 3: Type Coverage (parallel)
├─ Check TypeScript configuration
├─ Count interfaces and Zod schemas
├─ Verify schema-interface alignment
└─ Find untyped functions

Synthesis: Merge Results
├─ Combine findings preserving section structure
├─ Identify cross-section implications
├─ Prioritize recommendations
└─ Create unified report
```

## Example Output Structure

```markdown
# Bookmark Vault Comprehensive Analysis

## Component Structure Analysis
### Inventory
- Total components: 79
- UI primitives: 15 (19%)
- Feature modules: 64 (81%)

### Hierarchy
[Component tree...]

### Key Findings
[Specific observations with metrics]

## Data Flow Analysis
### Flow Paths
[Storage → hooks → components]

### Prop Drilling Analysis
- Max depth: 4 levels
- Components with 8+ props: 3

### Key Findings
[Specific bottlenecks with file references]

## Type Coverage Analysis
### Configuration
- TypeScript strict mode: ✅ ENABLED

### Schema Alignment
- Coverage: 46%
- Missing: Space, PinnedView schemas

### Key Findings
[Type safety score with evidence]

## Cross-Section Implications
[Connections between findings from all three areas]

## Recommendations (Prioritized)
1. [Critical - Do first]
2. [High priority - Next sprint]
3. [Medium priority - When resources available]

## Overall Assessment Score
- Component Architecture: 7.5/10
- Data Flow: 7/10
- Type Safety: 8.2/10
- **OVERALL: 7.4/10**
```

## Test Results

This skill was created using Test-Driven Development (TDD) for documentation:

- **RED Phase**: Baseline test without skill showed monolithic sequential analysis (500+ lines)
- **GREEN Phase**: Test with skill produced structured forked analysis (+20% more recommendations, +213% more file references)
- **REFACTOR Phase**: Enhanced rationalization blocking to prevent future analysis merging

See TEST-RESULTS.md for complete test documentation.

## Success Criteria

✓ All three analysis areas present with structured section breaks
✓ Each area has 3+ specific findings with metrics or line references
✓ Fork isolation maintained (Fork 1 → Fork 2 → Fork 3 → Synthesis)
✓ Cross-section implications section non-empty
✓ Recommendations actionable with specific file paths
✓ Overall assessment score with supporting evidence
✓ Verification checklist completed
✓ No vague observations - all backed by data

## When to Use

- Comprehensive codebase review before major refactoring
- Understanding architecture before contributing to the project
- Identifying type safety gaps and architectural debt
- Planning feature work from multiple perspectives
- Performance profiling and optimization planning

## When NOT to Use

- Quick spot checks on specific files (use bookmark-safety or bookmark-validator instead)
- Single issue debugging (use superpowers:systematic-debugging)
- Code review of specific PRs (use superpowers:requesting-code-review)

## Related Skills

- **bookmark-safety** - Protects against accidental deletion of bookmark storage
- **bookmark-validator** - Validates bookmark data quality and duplicates
- **superpowers:systematic-debugging** - For investigating specific bugs
- **superpowers:requesting-code-review** - For PR review workflows

## Notes

- Skill assumes Bookmark Vault project structure (components/, hooks/, lib/, stores/ directories)
- Forks run in parallel for efficiency but may be sequential in some environments
- Analysis depth is fixed to three areas; future versions may allow customization
- Works best with projects 5,000-50,000 lines of code

## Future Enhancements

1. Add parallel execution metrics (wall-clock time comparisons)
2. Support analysis depth levels (beginner, intermediate, expert)
3. Allow custom analysis areas via prompts
4. Support JSON/HTML output formats in addition to Markdown
5. Enable incremental analysis (run individual forks, combine results)
