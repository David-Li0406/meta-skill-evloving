---
name: refactor
description: Analyze code for refactoring opportunities using parallel agents with strict verification to eliminate false positives
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Bash
  - Task
---

# Refactor Advisor

## Purpose

Analyze code for refactoring opportunities, identify code smells, and suggest improvements for maintainability, readability, and adherence to project patterns using parallel analysis agents with strict verification.

## Core Responsibilities

1. **Parallel Analysis** - Run multiple specialized agents simultaneously for comprehensive coverage
2. **Strict Verification** - Double-check all findings to eliminate false positives
3. **Pattern Discovery** - Identify code smells, anti-patterns, and improvement opportunities
4. **Context Validation** - Verify findings against actual codebase behavior and conventions
5. **Prioritization** - Classify issues by severity and impact
6. **Actionable Recommendations** - Provide specific, implementable refactoring suggestions

## When to Invoke

- Proactively looking for code quality improvements
- After feature implementation to clean up technical debt
- Before major releases to ensure code health
- When onboarding to understand code quality issues
- During sprint planning to identify refactoring tasks

## Parallel Execution Strategy

### Analysis Agents (Run in Parallel)

Always launch these agents simultaneously for comprehensive coverage:

```
[Code Smell Detector]     → Duplicate code, long methods, large classes
[Pattern Analyzer]        → CQRS violations, repo issues, multi-tenancy
[Type Safety Checker]     → Missing types, any usage, Zod schemas
[Architecture Validator]  → Package organization, imports, dependencies
```

### Verification Agents (Run in Parallel)

After initial findings, verify in parallel:

```
[False Positive Eliminator] → Verify each finding exists and is actually a problem
[Context Validator]         → Check against project patterns and conventions
[Impact Assessor]           → Estimate effort vs benefit for each issue
```

### Sequential Flow

```
1. [Parallel Analysis Agents] → Collect all potential issues
2. [Sequential Consolidation] → Merge and deduplicate findings
3. [Parallel Verification] → Validate each finding
4. [Sequential Classification] → Prioritize by P0/P1/P2
5. [Final Report] → Output verified, actionable recommendations
```

**Detailed guidelines:** `.claude/rules/orchestrator-parallel-execution.md`

## Mandatory Verification Steps

### For Every Finding

1. **File Existence Check**
   - Verify the file actually exists at the specified path
   - Confirm line numbers are accurate

2. **Context Validation**
   - Read the surrounding code to understand intent
   - Check if the pattern is intentional (not a smell)
   - Verify against project conventions

3. **False Positive Elimination**
   - Is this actually a problem or just a style preference?
   - Does the "smell" serve a valid purpose in this context?
   - Is there a compelling reason for the current pattern?

4. **Impact Assessment**
   - What's the actual cost of this issue?
   - How much effort to fix?
   - What's the benefit of the fix?

### Common False Positives to Watch

| Finding        | May Be False Positive If...                              |
| -------------- | -------------------------------------------------------- |
| Duplicate code | Code is genuinely different logic that looks similar     |
| Long method    | Method is complex business logic that shouldn't be split |
| Magic number   | Number is a domain constant without a clear name         |
| Large class    | Class is a cohesive aggregate root or module             |
| Primitive      | Type is actually a simple value, not a domain concept    |

## Capabilities

### Code Smell Detection

- **Duplicate Code**: Identifies repeated patterns that could be extracted
- **Long Methods**: Flags functions exceeding reasonable length
- **Large Classes**: Detects files/classes with too many responsibilities
- **Feature Envy**: Finds code that belongs in a different module
- **Data Clumps**: Identifies grouped parameters that should be objects
- **Primitive Obsession**: Flags where domain concepts use primitives
- **Magic Strings/Numbers**: Finds hardcoded values that need constants

### Pattern Detection

- **Inconsistent Patterns**: Code not following established conventions
- **Missing Abstractions**: Opportunities for reusable components
- **Tight Coupling**: Dependencies that should be loosened
- **God Objects**: Modules with too many responsibilities
- **Shotgun Surgery**: Changes requiring many file modifications

### Specific to This Codebase

- **CQRS Violations**: Commands doing queries, queries doing writes
- **Repository Issues**: Direct database access bypassing repos
- **Multi-tenancy Issues**: Missing tenant context, data leakage risks
- **Type Safety**: Missing types, excessive `any`, loose Zod schemas
- **Package Organization**: Code in wrong packages, circular dependencies
- **Import Issues**: Relative import hell, wrong import sources

## Refactoring Categories

### P0 - Critical (Must Fix)

- Security vulnerabilities exposed by code structure
- Multi-tenancy violations (data leakage)
- Performance issues from inefficient patterns
- Breaking of architectural boundaries

### P1 - High Priority (Should Fix)

- Code that prevents feature development
- Complex code that's hard to maintain
- Duplicate code causing maintenance burden
- Missing error handling in critical paths

### P2 - Standard (Nice to Have)

- Naming inconsistencies
- Minor code organization issues
- Documentation improvements
- Small extraction opportunities

## Common Refactorings

| Code Smell             | Refactoring                     | Impact |
| ---------------------- | ------------------------------- | ------ |
| Duplicate Code         | Extract Method/Function         | High   |
| Long Method            | Extract Method, Compose Method  | High   |
| Magic Numbers          | Extract Constant                | Medium |
| Primitive Obsession    | Introduce Parameter Object      | Medium |
| Feature Envy           | Move Method                     | High   |
| Large Class            | Extract Class                   | High   |
| Data Clumps            | Introduce Parameter Object      | Medium |
| Conditional Complexity | Guard Clauses, Strategy Pattern | High   |
| Temp Field             | Introduce Parameter Object      | Low    |
| Lazy Element           | Inline Method/Class             | Low    |

## How to Use

### Full Codebase Scan

```
/refactor
"Scan the entire codebase for refactoring opportunities"
```

### Specific Package/Module

```
"Refactor the users module"
"Analyze packages/types for code smells"
"Check apps/api/src/modules/ for issues"
```

### Specific Pattern

```
"Find duplicate code across the codebase"
"Identify magic strings in the API"
"Look for CQRS violations in handlers"
"Find functions longer than 50 lines"
```

### After Feature Work

```
"I just finished feature X. Check if there are any refactoring opportunities"
```

## Output Format

1. **Summary** - Quick overview of findings (verified only)
2. **P0 Issues** - Critical problems requiring immediate attention
3. **P1 Issues** - High-priority improvements
4. **P2 Issues** - Nice-to-have enhancements
5. **Refactoring Suggestions** - Specific actionable changes with file locations
6. **Estimated Impact** - Effort vs benefit assessment
7. **Verification Notes** - How each finding was validated

## Quality Checklist

Before reporting any finding, verify:

- [ ] File exists and is readable
- [ ] Line numbers are accurate
- [ ] Code context was reviewed
- [ ] Finding is actually a problem (not just different style)
- [ ] Checked against project conventions
- [ ] No false positive conditions apply
- [ ] Impact assessment is realistic
- [ ] Suggested fix is implementable
- [ ] Fix doesn't introduce new issues
- [ ] Related findings were cross-referenced

## Quick Checks

Run these targeted searches to identify common issues (MUST verify findings):

```bash
# Magic strings - MUST verify not intentional
grep -r "'ACTIVE'" --include="*.ts" apps/ packages/

# Magic numbers - MUST verify not domain constant
grep -r "\b30\b" --include="*.ts" apps/ packages/

# Long files - MUST check if cohesive module
find . -name "*.ts" -exec wc -l {} + | awk '$1 > 300'

# Duplicate patterns - MUST verify actual duplication
grep -r "if.*&&.*&&" --include="*.ts" apps/api/src/

# CQRS violations - MUST verify actual violation
grep -r "Query.*write\|Command.*select" --include="*.ts" apps/

# Direct database access - MUST verify not in migration
grep -r "db\.select\|db\.insert" --include="*.ts" apps/api/ | grep -v "repository"
```

## Related Skills

- `review` - For focused code review of specific changes
- `architecture-advisor` - For structural/organizational guidance
- `orchestrator` - For coordinating complex refactoring tasks
- `api-nestjs-reviewer` - For API-specific pattern compliance

## Related Standards

- `.claude/rules/P0/` - Critical rules that refactoring should address
- `.claude/rules/P1/` - High-priority rules
- `CLAUDE.md` - Project architecture principles
- `.claude/rules/orchestrator-parallel-execution.md` - Parallel execution guidelines

---

**Remember:** False positives are worse than no findings. Always verify. Never report without context. When in doubt, exclude the finding.
