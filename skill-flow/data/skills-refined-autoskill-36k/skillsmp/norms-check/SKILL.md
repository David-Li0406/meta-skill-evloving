---
name: norms-check
description: |
  Analyze code against established project patterns and conventions.
  WHEN: Use after implementing features to verify code follows project norms. Invoke with "/norms:check".
  WHEN NOT: During initial exploration or when patterns aren't established yet.
---

# Code Norms Checker

## Purpose

Analyze all new or modified code in the current branch against established project patterns and conventions. This skill works with any project type by auto-detecting the technology stack.

## Your Mission

For each file created or modified in the current git branch, you will:

1. **Detect the project type** (language, framework, conventions)
2. **Identify the file type** (model, controller, test, service, utility, etc.)
3. **Find similar existing files** of the same type in the project
4. **Extract established patterns** from those reference files
5. **Compare the new code** against these patterns
6. **Report violations** and suggest corrections

---

## STEP 0: Project Type Detection

**Auto-detect the project type by checking for these indicators:**

| Indicator File | Project Type | Common File Types |
|----------------|--------------|-------------------|
| `package.json` | JavaScript/TypeScript | `.js`, `.ts`, `.jsx`, `.tsx` |
| `composer.json` | PHP | `.php` |
| `requirements.txt` / `pyproject.toml` / `setup.py` | Python | `.py` |
| `Cargo.toml` | Rust | `.rs` |
| `go.mod` | Go | `.go` |
| `Gemfile` | Ruby | `.rb` |
| `pom.xml` / `build.gradle` | Java/Kotlin | `.java`, `.kt` |
| `*.csproj` / `*.sln` | C#/.NET | `.cs` |
| `mix.exs` | Elixir | `.ex`, `.exs` |

**Run detection:**

```bash
# Check for project type indicators
ls -la package.json composer.json requirements.txt pyproject.toml Cargo.toml go.mod Gemfile pom.xml build.gradle mix.exs *.csproj 2>/dev/null || echo "Check subdirectories"
```

**Store detected project type for subsequent steps.**

---

## STEP 1: Identify Changed Files

```bash
# Get list of new/modified files in current branch
git diff --name-only $(git merge-base HEAD main)...HEAD
```

Filter to relevant source files based on detected project type.

---

## STEP 2: File Type Classification

Based on file path, name, and content, classify files into generic categories:

### Generic File Type Categories

| Category | Common Path Patterns | Purpose |
|----------|---------------------|---------|
| **Models/Entities** | `*/models/*`, `*/entities/*`, `*/domain/*` | Data structures, database models |
| **Controllers/Handlers** | `*/controllers/*`, `*/handlers/*`, `*/api/*` | Request handling |
| **Services** | `*/services/*`, `*/use-cases/*`, `*/application/*` | Business logic |
| **Repositories/DAOs** | `*/repositories/*`, `*/dao/*`, `*/data/*` | Data access |
| **Tests** | `*/test/*`, `*/tests/*`, `*_test.*`, `*.test.*`, `*.spec.*` | Test files |
| **Utilities/Helpers** | `*/utils/*`, `*/helpers/*`, `*/lib/*` | Utility functions |
| **Configuration** | `*/config/*`, `*.config.*`, `*.yml`, `*.yaml`, `*.json` | Configuration files |
| **Middleware** | `*/middleware/*`, `*/interceptors/*` | Request/response processing |
| **Types/Interfaces** | `*/types/*`, `*/interfaces/*`, `*.d.ts` | Type definitions |

### Language-Specific Patterns

**JavaScript/TypeScript:**
- Components: `*/components/*`, `*.component.*`
- Hooks: `*/hooks/*`, `use*.ts`
- Stores: `*/stores/*`, `*/state/*`

**PHP:**
- Entities: `*/Entity/*`
- Voters/Security: `*/Security/*`, `*Voter.php`
- Extensions: `*/Extension/*`

**Python:**
- Views: `*/views/*`, `views.py`
- Serializers: `*/serializers/*`
- Managers: `*_manager.py`

**Go:**
- Handlers: `*_handler.go`
- Repositories: `*_repository.go`

---

## STEP 3: Find Reference Files

For each changed file, find 2-3 similar files of the same type in the project:

```bash
# Example: Find similar files by type
# For a new service file, find existing services
find . -type f -name "*.{ext}" -path "*services*" | head -5

# For a test file, find similar test files
find . -type f -name "*test*" -o -name "*spec*" | head -5
```

**Selection criteria for reference files:**
1. Same file type category
2. Similar complexity/size
3. Recently modified (likely to have current patterns)
4. Well-established (not also new)

---

## STEP 4: Extract Patterns

For each reference file, identify these pattern categories:

### 4.1 Structural Patterns
- Import/require organization
- Class/function structure
- Module exports
- File organization

### 4.2 Naming Conventions
- Variable naming (camelCase, snake_case, PascalCase)
- Function/method naming
- Constant naming
- File naming

### 4.3 Architectural Patterns
- Dependency injection style
- Interface/type usage
- Error handling approach
- Async/await patterns

### 4.4 Code Style Patterns
- Indentation and formatting
- Comment style
- String quoting preferences
- Line length conventions

### 4.5 Testing Patterns
- Test structure (describe/it, test functions)
- Setup/teardown patterns
- Assertion style
- Mocking approach
- Test naming

### 4.6 Framework-Specific Patterns
- Decorators/attributes usage
- Configuration style
- Middleware patterns
- Routing conventions

---

## STEP 5: Compare and Analyze

Check new code against extracted patterns:

### Generic Checklist

**Structure:**
- [ ] Import organization matches reference files
- [ ] Class/function structure follows patterns
- [ ] File organization is consistent
- [ ] Exports follow conventions

**Naming:**
- [ ] Variables follow naming convention
- [ ] Functions/methods follow naming patterns
- [ ] Constants use correct case
- [ ] Files named consistently

**Architecture:**
- [ ] Dependency handling matches patterns
- [ ] Error handling is consistent
- [ ] Types/interfaces used appropriately
- [ ] Patterns match reference implementations

**Tests:**
- [ ] Test structure matches project style
- [ ] Setup/teardown follows patterns
- [ ] Assertions use project conventions
- [ ] Test naming is descriptive

---

## STEP 6: Generate Report

### Violation Severity Levels

- **CRITICAL**: Code won't work or has security issues
- **ERROR**: Violates established patterns, should be fixed
- **WARNING**: Deviates from conventions, consider fixing
- **INFO**: Suggestions for improvement

### Report Format

```markdown
# Code Norms Check Report

## Project Info
- **Type**: [Detected project type]
- **Branch**: [Current branch name]
- **Date**: [Current date]

## Summary
- Files analyzed: X
- Critical issues: X
- Errors: X
- Warnings: X
- Info: X

## Detailed Analysis

### [file/path/example.ext]
**Type**: [File category]
**References**: [List of reference files used]

#### Compliant Patterns
- [List of patterns that match]

#### Violations

1. **[Issue title]**
   - **Severity**: CRITICAL/ERROR/WARNING/INFO
   - **Pattern**: [What the reference files do]
   - **Found**: [What the new code does]
   - **Location**: Line X
   - **Suggestion**: [Specific fix]
   - **Reasoning**: [Why this pattern matters]

### [Another file...]

## Action Items

### Critical (Must Fix)
1. [Item]

### Errors (Should Fix)
1. [Item]

### Warnings (Consider)
1. [Item]

## Conclusion
[Overall assessment and recommendations]
```

---

## Execution Instructions

When invoked:

1. **Detect project type** using indicator files
2. **Get changed files**: `git diff --name-only $(git merge-base HEAD main)...HEAD`
3. **For each source file:**
   - Classify the file type
   - Find 2-3 reference files of the same type
   - Read and analyze reference files
   - Extract patterns
   - Compare new code against patterns
   - Document violations with severity
4. **Generate comprehensive report**
5. **Suggest specific fixes for each violation**

---

## Success Criteria

- All new code follows established patterns
- No critical violations
- Errors are addressed or justified
- Code style is consistent
- Tests mirror existing test patterns
- Architectural patterns are respected

---

## Notes

- Focus on patterns, not subjective preferences
- Reference multiple files to establish true patterns
- Be specific about violations (line numbers, examples)
- Provide actionable suggestions
- Consider project evolution (newer patterns may supersede old ones)
- Always explain WHY a pattern exists when suggesting changes
- If no reference files exist for a file type, note this and skip pattern comparison
