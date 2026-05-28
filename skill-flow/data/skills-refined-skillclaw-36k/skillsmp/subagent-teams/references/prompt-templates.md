# Subagent Prompt Templates

Optimized prompts for each subagent type to maximize effectiveness and minimize context waste.

---

## Prompt Structure

Every subagent prompt should follow:

```
[Action] [Target] in [Scope].
[Focus areas].
[Output format].
[Context from prior steps if any].
```

---

## Explore Agent Prompts

### Codebase Structure Discovery

```
"Explore the codebase structure in [directory/project].
Focus on: file organization, key modules, entry points, and conventions.
Return: structured summary with file paths and their purposes.
Thoroughness: [quick|medium|very thorough]"
```

### Pattern/Convention Finding

```
"Search for [pattern type] patterns in the codebase.
Look for: [specific things like error handling, auth, routing].
Focus areas: [directories or file types].
Return: list of patterns found with file:line references."
```

### Dependency/Import Analysis

```
"Analyze dependencies and imports for [module/feature].
Trace: how [component] connects to other parts of the system.
Return: dependency graph summary with key connection points."
```

### Bug Investigation

```
"Investigate potential causes of [error/symptom] in [scope].
Search for: [error messages, related function names, recent changes].
Return: ranked list of likely causes with file:line evidence."
```

---

## Plan Agent Prompts

### Architecture Design

```
"Design implementation approach for [feature/change].
Context: [findings from exploration phase].
Constraints: [user requirements, existing patterns to follow].
Consider: [trade-offs, alternatives].
Return: step-by-step implementation plan with file paths."
```

### Refactoring Strategy

```
"Plan refactoring of [target] from [current state] to [desired state].
Affected files: [list from exploration].
Constraints: [backwards compatibility, test coverage].
Return: ordered list of changes with risk assessment."
```

---

## General-Purpose Agent Prompts

### Implementation

```
"Implement [feature] in [file(s)].
Requirements: [specific behavior].
Follow patterns in: [reference files/existing code].
After implementation: [run tests/verify].
Return: summary of changes made with file paths."
```

### Test Creation

```
"Write [unit/integration] tests for [module/function] in [test file path].
Test cases: [list of scenarios].
Use patterns from: [existing test files].
Run tests after writing to verify they pass.
Return: test results summary."
```

### Test Execution

```
"Run [test command] and report results.
Focus on: [specific test files/modules if applicable].
If failures: identify root cause and fix if possible.
Return: pass/fail counts, any failures with details."
```

### Code Review

```
"Review [file(s)] for [security issues/bugs/performance/style].
Check for: [specific concerns].
Apply standards: [project conventions].
Return: list of issues found with severity and suggested fixes."
```

---

## Model Selection in Prompts

### Haiku Tasks (simple, fast)

```
# File finding
"Find all files matching [pattern] in [directory]. Return file paths only."

# Simple grep
"Search for [term] in [scope]. Return file:line matches."

# Test execution
"Run `[test command]`. Return pass/fail summary."

# Syntax validation
"Check [file] for syntax errors. Return any issues found."
```

### Sonnet Tasks (moderate complexity)

```
# Code implementation
"Implement [feature] following [patterns]. Write clean, tested code."

# Architecture analysis
"Analyze [module] architecture. Identify issues and improvements."

# Code review
"Review [changes] for bugs, security issues, and best practices."
```

### Opus Tasks (complex reasoning)

```
# Complex multi-file implementation
"Implement [complex feature] across [multiple modules]. Ensure consistency."

# Critical decision-making
"Evaluate [multiple approaches] for [problem]. Recommend best approach with reasoning."

# Large-scale refactoring
"Refactor [system] while maintaining [invariants]. Handle all edge cases."
```

---

## Context Passing Between Batches

When Batch 2 depends on Batch 1 results:

```
# Batch 1 result synthesis (in main context):
"Exploration found:
- Auth middleware in src/middleware/auth.ts
- User model in src/models/user.ts
- Existing tests use vitest with fixtures in tests/fixtures/"

# Batch 2 prompt (passes synthesized context):
"Implement login endpoint in src/api/auth/login.ts.
Context: Auth middleware is in src/middleware/auth.ts (uses JWT).
User model is in src/models/user.ts (has email, passwordHash fields).
Test pattern: Use vitest, fixtures in tests/fixtures/.
Follow existing endpoint patterns in src/api/."
```

Key: Pass only **synthesized findings**, not raw exploration output.

---

## Prompt Anti-Patterns

| Anti-Pattern | Problem | Better |
|--------------|---------|--------|
| "Look at the codebase" | Too vague, wastes context | "Find auth middleware in src/" |
| Pasting full file contents | Bloats subagent context | "Read src/auth.ts and extract the JWT validation logic" |
| Multiple unrelated tasks | Breaks specialization | One task per agent |
| No output format specified | Returns unpredictable format | "Return: bulleted list of findings" |
| Repeating info agent already has | Wastes tokens | Only pass NEW context |
