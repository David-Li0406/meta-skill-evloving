---
name: pm7y-codebase-review
description: Reviews a codebase for style consistency, patterns, idioms, and adherence to KISS, DRY, POLA, YAGNI principles. Automatically detects languages/frameworks present and applies appropriate analysis. Produces analysis findings and uses pm7y-ralph-planner to generate TASKS.md for autonomous execution.
allowed-tools: Read, Write, Edit, Grep, Glob, Task, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Codebase Review Skill

Reviews codebases for consistency, patterns, and adherence to software engineering principles. Produces analysis findings that are passed to `pm7y-ralph-planner` for TASKS.md generation.

---

## Overview

This skill performs comprehensive codebase analysis focusing on:

- **Style & pattern consistency** - Implicit and explicit conventions
- **Language idioms** - Following best practices for each language
- **Principle adherence** - KISS, DRY, POLA, YAGNI
- **Complexity reduction** - Identifying unnecessary complexity
- **Duplication detection** - Finding repeated code patterns

**Output:** Analysis findings passed to `pm7y-ralph-planner`, which generates a `TASKS.md` file with validation requirements and learnings tracking for autonomous execution via `pm7y-ralph-loop`.

**When to use:**

- Periodic codebase health checks with automated fixes
- Before major refactoring efforts
- Autonomous code quality improvement sessions
- After rapid feature development to address technical debt

---

## Review Depth Options

The review supports different depth levels via command arguments:

| Depth | Scope | Use When |
|-------|-------|----------|
| `--quick` | Sample key files, high-level patterns | Quick health check |
| `--standard` | Representative files from each area | Regular reviews (default) |
| `--comprehensive` | Full codebase scan, detailed analysis | Before major refactoring |

---

## Review Process

### Step 1: Study Documentation

Before analyzing code, read and understand:

1. **README.md** - Project overview, architecture decisions
2. **CLAUDE.md** - Codebase conventions (if exists)
3. **CONTRIBUTING.md** - Contribution guidelines
4. **Architecture docs** - Any docs in `/docs` or similar
5. **.editorconfig** - Formatting preferences
6. **Linter configs** - ESLint, Prettier, StyleCop, .pylintrc, .rubocop.yml, etc.

Use these to understand the project's stated conventions before comparing to actual code.

### Step 2: Detect Languages and Frameworks

Scan the codebase to identify all languages and frameworks present. Look for:

| Language/Framework | Indicators |
|-------------------|------------|
| **JavaScript/TypeScript** | `package.json`, `.js`, `.ts`, `.jsx`, `.tsx` files |
| **React** | React in package.json dependencies, JSX/TSX files, hooks |
| **Node.js** | `package.json` with node dependencies, no browser frameworks |
| **C#/.NET** | `.sln`, `.csproj`, `.cs` files, `Program.cs` |
| **Python** | `requirements.txt`, `pyproject.toml`, `setup.py`, `.py` files |
| **Go** | `go.mod`, `go.sum`, `.go` files |
| **Rust** | `Cargo.toml`, `Cargo.lock`, `.rs` files |
| **Java** | `pom.xml`, `build.gradle`, `.java` files |
| **Ruby** | `Gemfile`, `.rb` files, `Rakefile` |
| **PHP** | `composer.json`, `.php` files |
| **Kotlin** | `build.gradle.kts`, `.kt` files |
| **Swift** | `Package.swift`, `.swift` files, `.xcodeproj` |

**Record detected languages** for use in task grouping and analysis focus.

### Step 3: Analyze Code by Language

For each detected language, apply language-specific analysis. Use Context7 to look up current best practices for the detected languages/frameworks.

---

#### React/TypeScript Analysis

*Apply when React/TypeScript detected.*

**Component Patterns:**
- Functional vs class components (prefer functional)
- Hook usage patterns (custom hooks, composition)
- State management approach (local, context, external)
- Component file structure (co-location, barrel exports)

**TypeScript Idioms:**
- Type inference vs explicit types
- Interface vs type aliases
- Utility types usage
- Strict mode adherence

**Style Consistency:**
- Naming conventions (PascalCase components, camelCase functions)
- Import ordering and grouping
- Export patterns (default vs named)
- File naming conventions

**React Best Practices:**
- Prop drilling vs composition
- useEffect dependencies and cleanup
- Memoization (useMemo, useCallback, React.memo)
- Error boundaries
- Accessibility patterns

---

#### C#/.NET Analysis

*Apply when C#/.NET detected.*

**Architecture Patterns:**
- Layer separation (Controllers, Services, Repositories)
- Dependency injection usage
- Interface abstractions
- CQRS or traditional patterns

**C# Idioms:**
- Nullable reference types
- Async/await patterns
- LINQ usage (query vs method syntax)
- Record types vs classes
- Pattern matching

**Style Consistency:**
- Naming conventions (PascalCase, _camelCase for fields)
- File organization (one class per file)
- Namespace structure
- XML documentation

**.NET Best Practices:**
- Exception handling patterns
- Configuration management
- Logging patterns
- Validation approaches

---

#### Other Languages (Dynamic Analysis)

*Apply when languages other than React/TypeScript or C#/.NET are detected.*

For languages not covered above, use Context7 to look up current best practices:

1. **Identify the language** - Use the detection table from Step 2
2. **Query Context7** - Look up idioms, style guides, and best practices for that language
3. **Apply universal checks** - See "Generic Analysis" below
4. **Focus on consistency** - Even without deep language knowledge, inconsistencies are identifiable

**Common analysis patterns for any language:**
- Code organization and module structure
- Naming convention consistency
- Error/exception handling patterns
- Testing patterns and coverage
- Dependency management
- Documentation quality

---

#### Generic Analysis (Any Language)

*Always apply these checks regardless of language.*

**Universal Patterns:**
- Consistent naming within the codebase
- File/directory organization patterns
- Comment quality and accuracy
- Test organization and coverage
- Configuration management
- Environment handling
- Logging patterns
- Error handling consistency

### Step 4: Apply Engineering Principles

Evaluate code against each principle:

**KISS (Keep It Simple, Stupid):**
- Overly complex solutions for simple problems
- Unnecessary abstraction layers
- Convoluted control flow
- Over-engineered patterns

**DRY (Don't Repeat Yourself):**
- Duplicated code blocks
- Similar functions that could be generalized
- Repeated configuration
- Copy-pasted logic with minor variations

**POLA (Principle of Least Astonishment):**
- Surprising function behaviors
- Misleading names
- Unexpected side effects
- Non-obvious API designs

**YAGNI (You Aren't Gonna Need It):**
- Unused code or features
- Premature abstractions
- Over-configurable systems
- Speculative generality

See [principles-reference.md](principles-reference.md) for detailed examples.

### Step 5: Use Context7 for Documentation

When evaluating idioms or best practices, use Context7 MCP tools to look up:

- Current React patterns and hooks documentation
- C# language feature documentation
- .NET framework best practices
- Package-specific usage patterns

This ensures recommendations align with current (not outdated) best practices.

### Step 6: Pass Findings to pm7y-ralph-planner

After completing the analysis, invoke the `pm7y-ralph-planner` agent using the Task tool. Pass your findings as structured input so the planner can generate a proper TASKS.md with validation requirements and learnings tracking.

**Invoke pm7y-ralph-planner with this prompt:**

```
Generate a TASKS.md for codebase review remediation.

## Goal
Fix code quality issues identified during codebase review.

## Project Context
- **Technologies:** [Languages, frameworks, build tools detected]
- **Build command:** [detected build command]
- **Test command:** [detected test command]
- **Review scope:** [quick/standard/comprehensive]

## Key Conventions (from documentation)
- [Convention 1]
- [Convention 2]

## Findings

### High Priority (Critical issues affecting correctness or maintainability)

- **[PRINCIPLE]**: [Brief description]
  - Files: `file1.ext:line`, `file2.ext:line`
  - Action: [Specific action to take]
  - Verify: [How to verify the fix]

[Repeat for each high priority finding]

### Medium Priority (Consistency and pattern improvements)

- **[CATEGORY]**: [Brief description]
  - Files: `file1.ext`, `file2.ext`
  - Action: [Specific action to take]
  - Verify: [How to verify the fix]

[Repeat for each medium priority finding]

### Low Priority (Minor improvements and cleanup)

- **[CATEGORY]**: [Brief description]
  - Files: `file1.ext`
  - Action: [Specific action to take]
  - Verify: [How to verify the fix]

[Repeat for each low priority finding]

## Positive Observations (patterns to maintain)
- [Observation 1]
- [Observation 2]

## Notes
- [Any blockers or dependencies between tasks]
```

**Why use pm7y-ralph-planner:**

The planner will:
1. Add proper validation requirements (build, test, lint checks)
2. Include the Learnings Log section for preserving insights across iterations
3. Add the iteration workflow guidance
4. Format tasks for optimal autonomous execution

---

## Critical Rules

### Rule 1: Documentation First

ALWAYS read available documentation before analyzing code. Understanding stated conventions prevents false positives.

### Rule 2: Autonomous-Friendly Findings

Every finding MUST be:
- **Self-contained** - Can be completed in isolation
- **Specific** - Exact files and line numbers
- **Verifiable** - Clear success criteria
- **Safe** - Include test verification step

### Rule 3: Context Over Rules

Apply principles pragmatically. Small amounts of duplication may be acceptable. Simple code may look "boring" but is often correct. Consider the context before flagging violations.

### Rule 4: Prioritize Correctly

- **High**: Bugs, security issues, principle violations causing real problems
- **Medium**: Inconsistencies, pattern violations, maintainability issues
- **Low**: Style nitpicks, minor cleanup, optional improvements

### Rule 5: Use pm7y-ralph-planner

ALWAYS pass findings to `pm7y-ralph-planner` for TASKS.md generation. This ensures proper validation requirements, learnings tracking, and iteration workflow are included.

---

## Output Format

The analysis produces structured findings that are passed to `pm7y-ralph-planner`. The planner handles TASKS.md generation.

**Finding Format Requirements:**

Each finding must include:
1. **Category tag** in bold (e.g., `**DRY**`, `**KISS**`, `**Naming**`)
2. **Brief description** of the issue
3. **Files** with specific paths and line numbers where possible
4. **Action** describing exactly what to do
5. **Verify** explaining how to confirm the fix worked

**Example Finding:**

```markdown
- **DRY**: Duplicate email validation logic
  - Files: `src/controllers/UserController.cs:45-60`, `src/controllers/AdminController.cs:32-47`
  - Action: Extract shared validation to `src/helpers/ValidationHelpers.cs` as `ValidateEmail()` method. Update both controllers to use the shared helper.
  - Verify: Run `dotnet test` - all tests pass. Grep for email regex - only one occurrence.
```

---

## Validation Checklist

Before passing findings to pm7y-ralph-planner:

- [ ] Read all available documentation (README, CLAUDE.md, etc.)
- [ ] Detected and documented all languages/frameworks
- [ ] Analyzed patterns and idioms for each detected language
- [ ] Applied KISS, DRY, POLA, YAGNI principle evaluations
- [ ] Used Context7 for current best practice verification (if needed)
- [ ] All findings have specific file references
- [ ] All findings have clear Action and Verify steps
- [ ] Findings are correctly prioritized (High/Medium/Low)
- [ ] Positive observations documented
- [ ] Invoked pm7y-ralph-planner with structured findings

---

## Examples

### Example: High Priority DRY Task

```markdown
- [ ] **DRY**: Duplicate validation logic
  - Files: `src/controllers/UserController.cs:45-60`, `src/controllers/AdminController.cs:32-47`
  - Action: Extract email validation regex and error handling to `src/helpers/ValidationHelpers.ValidateEmail()`. Update both controllers to use shared helper.
  - Verify: `dotnet test` passes. Only one email regex in codebase.
```

### Example: Medium Priority KISS Task

```markdown
- [ ] **KISS**: Over-abstracted service layer
  - Files: `src/Services/UserService.cs`, `src/Services/IUserService.cs`, `src/Services/UserServiceBase.cs`, `src/Services/UserServiceExtensions.cs`
  - Action: Consolidate to single `UserService.cs` with interface `IUserService.cs`. Remove unnecessary base class and extensions.
  - Verify: `dotnet build` succeeds. `dotnet test` passes. Service still injectable via DI.
```

### Example: Low Priority Naming Task

```markdown
- [ ] **Naming**: Inconsistent hook file naming
  - Files: `src/hooks/useAuth.ts`, `src/hooks/useFetchData.ts`, `src/hooks/UseCart.tsx`
  - Action: Rename `UseCart.tsx` to `useCart.ts` (camelCase, .ts extension for non-component hooks).
  - Verify: `npm run build` succeeds. `npm test` passes. No import errors.
```

---

## Reference Documents

For detailed guidance on principles and patterns:

- [principles-reference.md](principles-reference.md) - Detailed KISS, DRY, POLA, YAGNI examples
