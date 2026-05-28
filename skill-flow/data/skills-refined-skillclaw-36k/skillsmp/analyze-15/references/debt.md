# Debt Analysis Reference

## Analysis Criteria

Look for technical debt that provides real improvement value. Working code has value - perfect is the enemy of good.

### Architecture

- Circular dependencies between modules
- Overly complex module structures
- Missing abstraction layers where patterns repeat
- Tight coupling between components that should be independent
- God objects/classes that do too much

### Code Quality

- Significant code duplication (not trivial repetition)
- Complex functions with high cyclomatic complexity
- Long methods/classes that should be split
- Poor naming that obscures intent
- Magic numbers/strings without explanation

### Patterns

- Outdated patterns (callbacks vs async/await)
- Inconsistent patterns across the codebase
- Anti-patterns (singletons abuse, global state, etc.)
- Framework misuse or fighting the framework

### Performance

- Obvious performance bottlenecks
- N+1 query patterns in database access
- Unnecessary re-renders in UI frameworks
- Missing caching opportunities for expensive operations
- Synchronous operations that should be async

## Effort Estimation

**Low Effort:**

- Simple refactoring
- Renaming for clarity
- Extracting small functions
- Adding types/documentation

**Medium Effort:**

- Extracting modules/classes
- Refactoring patterns
- Adding caching
- Query optimization

**High Effort:**

- Architectural changes
- Major refactoring
- Database schema changes
- API redesign

## Severity Guidelines

- **Critical**: Blocking further development or causing cascading issues
- **High**: Significant maintainability burden, frequently touched code
- **Medium**: Noticeable friction, moderate impact areas
- **Low**: Minor improvements, rarely touched code

## Notes

Include in the `notes` field when relevant:

- Category: architecture, code_quality, patterns, or performance
- Effort estimate: low, medium, or high
- Benefit of fixing (why it matters)
- Dependencies on other debt items
- Suggested refactoring approach
