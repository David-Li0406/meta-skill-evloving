# Phase 2: Quality Review (5 Parallel Agents)

## Goal

Review code quality across 5 dimensions. Launch all 5 agents in a single message.

## Pre-check: Load Pattern Files

Before launching agents, load relevant pattern files based on file types:

```
claude-patterns/react-typescript-antipatterns.md  → All components
claude-patterns/zod-form-patterns.md             → Form components
claude-patterns/tanstack-query-patterns.md       → Data fetching
claude-patterns/settings-patterns.md             → Hierarchical defaults
claude-patterns/service-refactoring-patterns.md  → Service files
CLAUDE.md                                        → All files
```

Pass loaded pattern content to agents.

## Agent 1: pattern-enforcer

**Uses**: `general-purpose` agent

**Prompt template**:

```
Review these files for project pattern compliance:

FILES: {file_list}

PATTERNS TO ENFORCE:
{loaded_pattern_content}

Check for violations of:

1. **CLAUDE.md Core Rules**
   - TanStack Query for data fetching (no direct service calls in components)
   - Result pattern for services: `{ data: T | null; error: string | null }`
   - Nullable DB fields use `T | null` (never `T | undefined`)
   - Filter by `organization_id` for multi-tenant isolation

2. **Zod Form Patterns**
   - Zod schemas define form shapes (not handwritten interfaces)
   - Types inferred from schemas
   - Validation on blur

3. **Contact Filtering**
   - Use `src/utils/contactFilters.ts` functions
   - Never inline filter like `contacts.filter(c => c.is_lt_member)`

4. **Service Patterns**
   - Large services (>500 lines) should use facade pattern
   - Repository + orchestrator structure

For each violation, report:
- File and line number
- Which pattern is violated (quote the rule)
- Severity (P0/P1/P2/P3)
- Suggested fix
```

## Agent 2: react-quality

**Uses**: `general-purpose` agent

Focuses on **quality/readability only** (bug-causing issues go to check-your-work).

**Prompt template**:

```
Review these React files for QUALITY issues (not bugs - those are checked by check-your-work):

FILES: {file_list}

Check for these React QUALITY issues:

1. **Component Size** (readability)
   - Components >300 lines should be split
   - Report line count for each component

2. **Props Count** (maintainability)
   - >10 props suggests component needs refactoring
   - Count props in each component's interface

3. **Component Structure** (readability)
   - Nested component definitions inside other components
   - JSX returned from internal functions (should be components)
   - Multiple boolean states that should be enum

4. **Naming Conventions** (readability)
   - Boolean variables without is/has/should/can prefix
   - Event handlers without handle/on prefix
   - Unclear component names

5. **Style Preferences** (consistency)
   - React.FC usage (prefer function declarations)
   - Inline styles (prefer Tailwind classes)

NOTE: Do NOT flag these (handled by check-your-work):
- useState for derived values (bug)
- Missing useEffect cleanup (bug)
- Missing effect dependencies (bug)
- Array index as key (bug)
- Hooks after conditional returns (bug)

For each issue, report:
- File and line number
- Issue type
- Severity (P0/P1/P2/P3)
- Code example of the problem
- Suggested fix
```

## Agent 3: architecture

**Uses**: `general-purpose` agent

**Prompt template**:

```
Review these files for architectural quality:

FILES: {file_list}

Check for SOLID principle violations:

1. **Single Responsibility Principle (SRP)**
   - Does each class/component have only one reason to change?
   - Red flags: high method count, many dependencies, mixed concerns
   - Components should not mix UI + business logic + data fetching

2. **Open/Closed Principle (OCP)**
   - Can code be extended without modification?
   - Red flags: long if/else chains checking types, switch on type strings
   - Solution: Use polymorphism, strategy pattern

3. **Liskov Substitution Principle (LSP)**
   - Can derived types substitute base types?
   - Red flags: instanceof checks, type casting

4. **Interface Segregation Principle (ISP)**
   - Are interfaces focused and minimal?
   - Red flags: many methods, implementations with empty/throw methods

5. **Dependency Inversion Principle (DIP)**
   - Does code depend on abstractions, not concretions?
   - Red flags: liberal use of "new" for dependencies, tight coupling

6. **Separation of Concerns**
   - UI, business logic, and data access properly isolated?
   - Services in services/, hooks in hooks/, components in components/

For each violation, report:
- File and line number
- Which SOLID principle is violated
- Severity (P0/P1/P2/P3)
- Why it matters
- Suggested refactoring
```

## Agent 4: readability

**Uses**: `general-purpose` agent

**Prompt template**:

```
Review these files for readability and maintainability:

FILES: {file_list}

Apply the 30-Second Rule: Another developer should understand this code in under 30 seconds.

Check for:

1. **Naming Conventions**
   - Boolean variables: must have is/has/should/can prefix
     - BAD: `loading`, `visible`, `active`
     - GOOD: `isLoading`, `isVisible`, `isActive`
   - Event handlers: must have handle/on prefix
     - BAD: `clickHandler`, `submit`
     - GOOD: `handleClick`, `onSubmit`
   - Functions: clear verb + noun
     - BAD: `data()`, `process()`
     - GOOD: `fetchUserData()`, `processPayment()`

2. **Complexity**
   - Functions >20 lines should be reviewed
   - Nesting >3 levels deep is hard to read
   - Cyclomatic complexity >10 needs refactoring

3. **Code Clarity**
   - Magic numbers without constants
     - BAD: `if (status === 3)`
     - GOOD: `if (status === STATUS_PENDING)`
   - Unclear abbreviations
   - Dense one-liners that should be expanded

4. **Function Design**
   - Functions with >4 parameters
   - Boolean parameters (use options object instead)
   - Side effects in functions that look pure

For each issue, report:
- File and line number
- Issue type
- Severity (P0/P1/P2/P3)
- Current code
- Improved version
```

## Agent 5: ai-smell-detector

**Uses**: `general-purpose` agent

**Prompt template**:

```
Review these files for AI-specific code smells:

FILES: {file_list}

AI-generated code often exhibits these anti-patterns. Check for:

1. **Over-Engineering**
   - Abstractions for one-time operations
   - Generic solutions for specific problems
   - Excessive configuration options
   - Factory patterns for simple object creation
   - Strategy patterns with only one strategy

2. **Unnecessary Complexity**
   - Helper functions used only once
   - Utility classes that could be inline code
   - Wrapper functions that add no value
   - Deep inheritance hierarchies

3. **Premature Optimization**
   - useMemo/useCallback on simple values
   - Caching mechanisms for rarely-accessed data
   - Custom hooks that wrap simple useState
   - Performance optimizations without profiling

4. **Config/Options Explosion**
   - Functions with options objects when simple params suffice
   - Too many optional parameters
   - Feature flags for non-existent features

5. **"Helpful" Additions Not Requested**
   - Error handling beyond requirements
   - Logging that wasn't asked for
   - Type guards for impossible states
   - Fallbacks that mask bugs

6. **Defensive Over-Coding**
   - Null checks on values that can't be null
   - Type assertions that are always true
   - Redundant validation at every layer

For each smell, report:
- File and line number
- Smell type
- Severity (P0/P1/P2/P3)
- Why this is over-engineered
- Simpler alternative
```

## Severity Guidelines

Map impact to P0-P3:

| Severity | Quality Impact                               |
| -------- | -------------------------------------------- |
| P0       | Major pattern violation, architectural issue |
| P1       | SOLID violation, component structure         |
| P2       | Readability issue, minor pattern deviation   |
| P3       | Style preference, optional improvement       |

## Output Format

Each agent returns findings in this format:

```typescript
interface Finding {
  file: string;
  line: number;
  category:
    | "pattern"
    | "react-quality"
    | "architecture"
    | "readability"
    | "ai-smell";
  rule: string; // Which rule was violated
  severity: "P0" | "P1" | "P2" | "P3";
  description: string; // What's wrong
  suggestion: string; // How to fix
  codeSnippet?: string; // Relevant code
}
```

## After Completion

Wait for all 5 agents to complete.
Collect and merge their findings.
Proceed to Phase 3 (Red Team) with combined findings list.
