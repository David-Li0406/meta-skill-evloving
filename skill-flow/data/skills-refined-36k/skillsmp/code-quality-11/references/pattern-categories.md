# Pattern Categories

## Positive Patterns (to detect and enforce)

### naming
- **variables**: camelCase, snake_case, SCREAMING_SNAKE, Hungarian notation
- **functions**: camelCase, snake_case, verb prefixes (get, set, is, has, can, should)
- **classes/types**: PascalCase, Interface prefix (IUser vs User), Type suffix
- **files**: kebab-case, camelCase, snake_case, PascalCase for components
- **constants**: SCREAMING_SNAKE, object grouping
- **prefixes**: is_, has_, on_, handle_, use (hooks), with (HOCs)
- **suffixes**: _id, _at, _count, Handler, Service, Controller, Repository
- **acronyms**: lowercase (httpRequest) vs uppercase (HTTPRequest)

**Detection regex:**
```
# camelCase: ^[a-z][a-zA-Z0-9]*$
# PascalCase: ^[A-Z][a-zA-Z0-9]*$
# snake_case: ^[a-z][a-z0-9_]*$
# SCREAMING_SNAKE: ^[A-Z][A-Z0-9_]*$
# kebab-case: ^[a-z][a-z0-9-]*$
```

### imports
- **ordering**: grouped (stdlib, external, internal, relative), alphabetical within groups
- **paths**: absolute paths, relative paths, path aliases (@/, ~/)
- **barrel_exports**: index files for public API, selective exports
- **dynamic_imports**: lazy loading, code splitting points
- **type_imports**: `import type` usage (TypeScript)
- **side_effect_imports**: CSS/style imports, polyfills

**Detection regex:**
```
# Import statement: ^import\s+.*\s+from\s+['"](.*)['"]
# Type import: ^import\s+type\s+
# Dynamic import: import\s*\(\s*['"]
# Side effect: ^import\s+['"][^'"]+['"]
```

### api_calls
- **wrappers**: service hooks, fetch wrappers, axios instances
- **error_handling**: try/catch, .catch(), Result/Either types
- **retry_logic**: exponential backoff, max retries, circuit breaker
- **caching**: react-query, swr, custom cache, cache invalidation
- **request_transformation**: interceptors, middleware
- **response_normalization**: adapters, mappers, DTOs

### state_management
- **local_state**: useState patterns, useReducer for complex state
- **global_state**: redux, zustand, jotai, context
- **form_state**: react-hook-form, formik, controlled vs uncontrolled
- **server_state**: react-query, swr, apollo client
- **derived_state**: useMemo, selectors, computed values
- **state_initialization**: lazy initialization, default values

### component_structure
- **file_organization**: feature-based, type-based, atomic design
- **prop_patterns**: destructuring, spreading, default props, required vs optional
- **composition**: hooks, render props, HOCs, compound components
- **separation**: container/presentational, smart/dumb, view/logic
- **co-location**: styles, tests, types alongside components

### async_patterns
- **promise_handling**: .then/.catch, async/await, Promise.all/race/allSettled
- **error_propagation**: re-throwing, error wrapping, error boundaries
- **cancellation**: AbortController, cleanup functions, race conditions
- **loading_states**: isLoading, isPending, skeleton screens
- **optimistic_updates**: immediate UI update, rollback on failure

### type_patterns (TypeScript/Flow)
- **type_definitions**: interfaces vs types, when to use each
- **generics**: generic functions, generic components, constraints
- **union_types**: discriminated unions, narrowing
- **utility_types**: Partial, Required, Pick, Omit, Record usage
- **type_guards**: is* functions, in operator, typeof, instanceof
- **branded_types**: nominal typing, NewType pattern

### error_handling
- **boundaries**: placement strategy, granularity
- **logging**: structured logging, log levels, context enrichment
- **user_feedback**: toast, modal, inline errors, error pages
- **recovery**: retry buttons, fallback UI, graceful degradation
- **error_types**: custom error classes, error codes, error hierarchy

### testing
- **file_location**: colocated (Button.test.tsx), __tests__/, spec/
- **naming**: *.test.*, *.spec.*, test descriptions
- **mocking**: manual mocks, jest.mock, msw, dependency injection
- **coverage**: thresholds, ignore patterns, critical path coverage
- **test_types**: unit, integration, e2e, snapshot
- **arrange_act_assert**: AAA pattern, given-when-then

### documentation
- **comments**: when to comment, comment styles, TODO/FIXME conventions
- **jsdoc**: @param, @returns, @example, @deprecated
- **type_annotations**: inline types, separate type files
- **readme**: structure, badges, examples, API documentation
- **adr**: architecture decision records format
- **changelog**: keep-a-changelog format, semantic versioning

---

## Anti-Patterns (to detect and flag)

### code_smells
| Anti-Pattern | Description | Detection Hint |
|--------------|-------------|----------------|
| God class/function | Single unit doing too much | >300 LOC, >10 methods, >5 dependencies |
| Feature envy | Method uses another class more than its own | Count external vs internal references |
| Data clumps | Same data groups appear together | Repeated parameter lists |
| Primitive obsession | Using primitives instead of small objects | String IDs, numeric status codes |
| Long parameter list | Functions with many parameters | >4 parameters |
| Shotgun surgery | One change requires many small changes | High coupling metrics |

**Detection:**
```
# Long functions (>50 lines)
# Count lines between function start and end

# Many parameters
\([^)]{100,}\)  # Long parameter lists

# God files
wc -l <file> | awk '$1 > 500'
```

### complexity_issues
| Issue | Threshold | Detection |
|-------|-----------|-----------|
| Deep nesting | >4 levels | Count indentation/braces |
| Long functions | >50 LOC | Line count between function boundaries |
| High cyclomatic complexity | >10 | Count if/else/switch/for/while/&& |
| Long files | >500 LOC | wc -l |
| Many imports | >15 | Count import statements |

### coupling_issues
- **circular_dependencies**: A imports B, B imports A
- **hidden_dependencies**: global state, singletons, implicit context
- **tight_coupling**: direct instantiation, hardcoded dependencies
- **god_modules**: modules that everything depends on

**Detection:**
```
# Find circular: analyze import graph
# Hidden deps: grep for global., window., process.env (outside config)
```

### duplication
- **copy_paste**: identical or near-identical code blocks
- **similar_logic**: same algorithm with different variables
- **repeated_patterns**: patterns that should be utilities

### naming_violations
- **misleading_names**: names that don't match behavior
- **single_letter**: variables like x, y (except loop counters i, j, k)
- **magic_numbers**: unexplained numeric literals
- **magic_strings**: unexplained string literals
- **abbreviations**: unclear shortened names

**Detection:**
```
# Single letter variables (not loop counters)
\b[a-z]\s*=

# Magic numbers
[^a-zA-Z_"][0-9]{2,}[^a-zA-Z_0-9"]

# Magic strings
['"]{2,}[^'"]{10,}['"]{2,}  # Long unexplained strings
```

### error_antipatterns
- **swallowed_exceptions**: catch blocks that do nothing
- **generic_catch**: catching Error/Exception without discrimination
- **missing_context**: errors without helpful messages
- **thrown_strings**: throw "error" instead of throw new Error()
- **console_only**: console.error without proper logging

**Detection:**
```
# Empty catch
catch\s*\([^)]*\)\s*\{\s*\}

# Generic catch
catch\s*\(\s*(e|err|error|ex|exception)\s*\)

# Thrown strings
throw\s+['"]
```

### security_smells
| Smell | Risk | Detection |
|-------|------|-----------|
| Hardcoded secrets | Credential exposure | password\|secret\|api_key.*=.*['"] |
| SQL concatenation | SQL injection | query.*\+.*\$\|query.*\$\{.*\} |
| eval usage | Code injection | eval\( |
| innerHTML | XSS | innerHTML\s*= |
| dangerouslySetInnerHTML | XSS | dangerouslySetInnerHTML |
| Disabled security | Various | no-verify\|unsafe-eval |

---

## Context-Aware Detection

Patterns should be evaluated in context:

| Context | Relaxed Rules | Stricter Rules |
|---------|---------------|----------------|
| Tests | Magic numbers OK, mocking OK | Test isolation required |
| Scripts/CLI | console.log OK, process.exit OK | Error handling still required |
| Config files | Long files OK | Clear structure required |
| Generated code | Skip analysis | Mark as generated |
| Migrations | Specific SQL OK | Reversibility required |

---

## Language-Specific Patterns

### JavaScript/TypeScript
- Hook rules (React)
- Module patterns (CommonJS vs ESM)
- Type-only imports
- Nullish coalescing vs OR

### Python
- PEP 8 compliance
- Type hints (3.5+)
- f-strings vs format()
- Context managers

### Go
- Error handling (if err != nil)
- Interface composition
- Package naming

### Rust
- Result/Option handling
- Ownership patterns
- Trait implementations
