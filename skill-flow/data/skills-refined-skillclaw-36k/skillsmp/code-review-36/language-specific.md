# Language-Specific Review Checklists

Supplement to the main review criteria. Apply the relevant section based on project type.

---

## Rust

### Ownership & Borrowing

- [ ] No unnecessary `.clone()` calls
- [ ] References preferred over owned values where lifetime permits
- [ ] Lifetime elision used where possible (avoid explicit `'a` when inferrable)
- [ ] No `Rc`/`Arc` where ownership transfer would suffice
- [ ] `Cow<'_, T>` considered for functions that sometimes need to allocate

### Error Handling

- [ ] `?` operator used consistently (no manual match-and-return)
- [ ] Error types implement `std::error::Error`
- [ ] `thiserror` or similar for custom error types
- [ ] `anyhow` only in application code, not library code
- [ ] No `.unwrap()` outside of tests (use `.expect()` with context or propagate)
- [ ] `panic!` only for programmer errors, not runtime conditions

### Unsafe Code

- [ ] Is `unsafe` actually necessary?
- [ ] Safety invariants documented in `// SAFETY:` comment
- [ ] Unsafe block is minimal (don't wrap more than needed)
- [ ] No undefined behaviour (aliasing, uninit memory, data races)

### Idioms

- [ ] `impl Trait` for return types where appropriate
- [ ] `#[must_use]` on functions with important return values
- [ ] `#[non_exhaustive]` on public enums that may grow
- [ ] `Default` derived or implemented where sensible
- [ ] Iterators preferred over indexed loops
- [ ] `if let` / `let else` instead of match with single arm + wildcard

### Clippy & Lints

- [ ] `cargo clippy` passes
- [ ] Allowed lints have `// Reason:` comment
- [ ] No `#[allow(clippy::all)]` or similar blanket suppressions

### Performance

- [ ] No allocations in hot loops
- [ ] `Vec::with_capacity` when size is known
- [ ] `&str` preferred over `String` for parameters
- [ ] `collect::<Result<Vec<_>, _>>()` for fallible iteration

---

## Python

### Type Hints

- [ ] All function signatures have type hints
- [ ] Return types specified (including `-> None`)
- [ ] `Optional[X]` or `X | None` for nullable types
- [ ] Generic types parameterised (`list[str]` not `list`)
- [ ] `TypedDict` or dataclass for structured dicts
- [ ] `mypy` passes in strict mode (or project's configured mode)

### Error Handling

- [ ] No bare `except:` clauses
- [ ] No `except Exception:` without re-raise or logging
- [ ] Custom exceptions inherit from appropriate base
- [ ] `raise ... from e` preserves exception chain
- [ ] Context managers used for cleanup (`with` statements)

### Resource Management

- [ ] Files opened with `with` statement
- [ ] Database connections properly closed/returned to pool
- [ ] `contextlib.contextmanager` for custom cleanup
- [ ] No file handles stored in long-lived objects without cleanup

### Idioms

- [ ] List/dict/set comprehensions where clearer than loops
- [ ] `enumerate()` instead of manual counter
- [ ] `zip()` for parallel iteration
- [ ] `pathlib.Path` instead of `os.path`
- [ ] f-strings for formatting (not `%` or `.format()`)
- [ ] `dataclass` or `NamedTuple` instead of plain tuples/dicts for structured data
- [ ] `functools.cached_property` for expensive computed properties

### Imports

- [ ] No wildcard imports (`from x import *`)
- [ ] Standard library, third-party, local imports separated
- [ ] No circular imports
- [ ] `TYPE_CHECKING` block for type-only imports

### Testing

- [ ] `pytest` fixtures used appropriately
- [ ] Parametrized tests for multiple inputs
- [ ] Mocks scoped narrowly (don't mock what you don't own)
- [ ] No `time.sleep()` in tests (use freezegun or similar)

---

## TypeScript

### Type Safety

- [ ] No `any` type (use `unknown` and narrow)
- [ ] No `@ts-ignore` without explanation
- [ ] Strict null checks enabled and respected
- [ ] Discriminated unions for variant types
- [ ] `as const` for literal inference where needed
- [ ] Generic constraints where applicable

### Null Handling

- [ ] Optional chaining (`?.`) used appropriately
- [ ] Nullish coalescing (`??`) preferred over `||` for defaults
- [ ] `!` non-null assertion only with known invariants
- [ ] Early return on null/undefined checks

### Async Patterns

- [ ] `Promise` rejections handled (`.catch()` or try/catch)
- [ ] No floating promises (unhandled async calls)
- [ ] `Promise.all` for parallel operations
- [ ] `AbortController` for cancellable operations
- [ ] No `async` on functions that don't `await`

### Modules

- [ ] No circular dependencies
- [ ] Barrel exports (`index.ts`) used judiciously
- [ ] Named exports preferred over default exports
- [ ] Import paths use aliases (if configured)

### React (if applicable)

- [ ] Components are pure (no side effects during render)
- [ ] `useEffect` dependencies are correct and complete
- [ ] `useMemo`/`useCallback` used for expensive computations/stable references
- [ ] Keys are stable and unique (not array index for dynamic lists)
- [ ] State updates are immutable
- [ ] Custom hooks extract reusable logic

### Testing

- [ ] Tests don't depend on implementation details
- [ ] Async tests properly awaited
- [ ] Mocks typed correctly
- [ ] No snapshot tests for logic (only UI when justified)

---

## Common Across Languages

### Git Hygiene

- [ ] Commits are atomic (one logical change)
- [ ] Commit messages explain why, not just what
- [ ] No commented-out code committed
- [ ] No debug logging left in
- [ ] No secrets or credentials

### Documentation

- [ ] Public APIs documented
- [ ] Changed behaviour reflected in docs
- [ ] README updated if user-facing changes
- [ ] CHANGELOG entry if project uses one

### Dependencies

- [ ] New dependencies justified
- [ ] License compatible
- [ ] Actively maintained
- [ ] Version pinned appropriately
- [ ] No duplicate functionality with existing deps
