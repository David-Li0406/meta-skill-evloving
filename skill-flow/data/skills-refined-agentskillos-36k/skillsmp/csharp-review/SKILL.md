---
name: csharp-review
description: An agent designed to assist with software development tasks for C#/.NET projects.
---

# C#/.NET Code Review

Review C# code changes for best practices, modern patterns, and maintainability.

## Getting Changes to Review

Determine what the user wants reviewed, then get the diffs:

```bash
# Last N commits
git --no-pager diff HEAD~3..HEAD -- '*.cs'

# Since a specific commit
git --no-pager diff abcd1234..HEAD -- '*.cs'

# Between two commits
git --no-pager diff abcd1234..2345bcde -- '*.cs'

# Staged changes
git --no-pager diff --cached -- '*.cs'

# Unstaged changes
git --no-pager diff -- '*.cs'
```

For full file context when needed:
```bash
git --no-pager show HEAD:path/to/file.cs
```

## Review Checklist

Review changes against these principles:

### Modern C# 14/.NET 10

- [ ] Use collection expressions `[1, 2, 3]` instead of `new List<int> { 1, 2, 3 }`
- [ ] Use primary constructors where appropriate
- [ ] Use file-scoped namespaces
- [ ] Use pattern matching over type checks and casts
- [ ] Use switch expressions where applicable

### DTOs and Records

- [ ] DTOs should be `record` types, not classes
- [ ] Records should be immutable (use `init` properties or positional parameters)
- [ ] Records should use primary constructors
- [ ] Collections in records should be `ImmutableList<T>`/`ImmutableDictionary<K,V>` or `IReadOnlyList<T>`/`IReadOnlyDictionary<K,V>`
- [ ] DTOs/Records should have minimal behavior (no business logic)

### SOLID Principles

- [ ] **Single Responsibility**: Each class has one reason to change
- [ ] **Open-Closed**: Open for extension, closed for modification
- [ ] **Dependency Inversion**: Depend on interfaces, not concrete implementations
- [ ] Always question inheritance — prefer composition

### Error Handling

- [ ] Do not use `null` for control flow
- [ ] Avoid redundant null checks—let errors bubble up
- [ ] Avoid unnecessary try/catch blocks—don't swallow exceptions
- [ ] Use result types or exceptions appropriately for the context

### Code Smells

- [ ] Avoid primitive obsession (use domain types)
- [ ] No new `Newtonsoft.Json` references — use `System.Text.Json`
- [ ] No new Reflection-based code
- [ ] Use `HostApplicationBuilder` not legacy `IHostBuilder`

### Documentation

- [ ] Public and internal classes/members are documented
- [ ] Comments explain *why*, not *what*

### Dependency Injection

- [ ] If using DI, consider: could this be a service?
- [ ] Services should depend on interfaces

### Testing

- [ ] Tests use FluentAssertions/AwesomeAssertions/Shouldly if present in project
- [ ] Do not add unnecessary Arrange-Act-Assert comments

## Output Format

For each issue found:

```
### [Category]: Brief description

**File**: `path/to/file.cs` (lines X-Y)

**Issue**: Explain what's wrong and why it matters.

**Suggestion**:
```cs
// Recommended code
```
```

Prioritize issues by impact: correctness > security > maintainability > style.
