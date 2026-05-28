# Subagent Investigation Patterns

For complex test failures, leverage Claude Code's built-in subagents to explore the codebase efficiently.

## Built-in Subagents for Test Debugging

| Subagent | Model size | Use Case |
|----------|------------|----------|
| **Explore** | small (haiku) | Fast codebase search, finding test files, fixtures |
| **general-purpose** | medium (sonnet) | Complex multi-step debugging investigations |

## By Failure Type

| Failure Type | Subagent Strategy |
|--------------|-------------------|
| **Flaky tests** | Explore (very thorough) - Find shared state, global variables, fixture scopes |
| **Import errors** | Explore (medium) - Map module dependencies and `__init__.py` files |
| **Multi-file failures** | Explore (very thorough) - Trace imports, find all related tests |
| **Fixture issues** | Explore (medium) - Find all conftest.py files and fixture definitions |
| **Unknown code** | general-purpose - Full investigation with code reading |

## Example Invocations

**Finding fixture dependencies:**
```
Use the Explore agent (medium thoroughness) to find:
- All conftest.py files in the test directory
- Fixtures with session or module scope
- Files that import or use the failing fixture
```

**Investigating flaky test state:**
```
Use the Explore agent (very thorough) to find:
- Global variables and module-level state in src/
- Singleton patterns or caches
- Database fixtures and their cleanup patterns
- Files that modify shared test resources
```

**Tracing import chains:**
```
Use the Explore agent (medium thoroughness) to find:
- All __init__.py files in the package
- Circular import patterns between modules
- Missing or misnamed imports
```

## When to Use Subagents vs Direct Tools

**Use Explore subagent when:**
- Failure involves unfamiliar code areas
- Need to search multiple directories for fixtures/state
- Want to preserve main context for debugging output
- Investigating order-dependent or flaky tests

**Use direct tools when:**
- Failure is localized to a single file
- You know exactly which function to examine
- Simple assertion mismatch with clear cause
- Already near context limit

## Benefits

| Benefit | Description |
|---------|-------------|
| **Context isolation** | Test output and search results don't bloat main conversation |
| **Speed** | Small model size (haiku) searches faster than manual Glob/Grep |
| **Focus** | Returns curated findings instead of raw file lists |
| **Parallelization** | Can run multiple Explore agents for different investigation paths |
