# Rust Code Review Guidelines

What to look for when reviewing Rust code.

## Correctness

### Memory Safety
- [ ] No unsafe code without justification and safety comments
- [ ] Lifetimes correctly specified
- [ ] No dangling references
- [ ] Proper ownership transfer

### Error Handling
- [ ] No unwrap() in production code (use expect() with message or ?)
- [ ] All Result types handled
- [ ] Error types are descriptive
- [ ] No silently ignored errors

### Concurrency
- [ ] No data races (Send/Sync bounds correct)
- [ ] Proper synchronization (Mutex, RwLock)
- [ ] No deadlocks (lock order documented)
- [ ] Async code uses appropriate runtime

## Code Quality

### Style
- [ ] Follows Rust naming conventions
- [ ] rustfmt applied
- [ ] clippy warnings addressed
- [ ] No compiler warnings

### API Design
- [ ] Public API is minimal and clear
- [ ] Functions do one thing
- [ ] Appropriate use of Result vs Option vs panic
- [ ] Borrows vs ownership appropriate

### Documentation
- [ ] Public items have doc comments
- [ ] Examples in documentation
- [ ] Module-level documentation exists
- [ ] Complex code has explanatory comments

### Testing
- [ ] Unit tests for public functions
- [ ] Integration tests where appropriate
- [ ] Edge cases covered
- [ ] Property tests for complex logic

## Performance

- [ ] No unnecessary clones
- [ ] Appropriate data structures
- [ ] Collections pre-allocated where possible
- [ ] Iterators used instead of loops where appropriate
- [ ] No premature optimization

## Security

- [ ] Input validation
- [ ] No SQL injection (use parameterized queries)
- [ ] No path traversal vulnerabilities
- [ ] Secrets not in code
- [ ] Dependencies audited

## Common Anti-Patterns

### Avoid
```rust
// Unwrap in production
let value = map.get(&key).unwrap();

// Stringly-typed
fn process(user_type: String)

// Fighting borrow checker with Arc everywhere
struct Data { field: Arc<Vec<i32>> }

// Ignoring errors
let _ = risky_operation();
```

### Prefer
```rust
// Proper error handling
let value = map.get(&key).ok_or(Error::NotFound)?;

// Type-safe
enum UserType { Admin, Regular }
fn process(user_type: UserType)

// Proper ownership
struct Data { field: Vec<i32> }

// Handle errors
risky_operation()?;
```

## Review Checklist

**Before Merge:**
1. Code compiles without warnings
2. Tests pass
3. Documentation updated
4. No TODO comments (or tracked in issues)
5. Performance acceptable
6. Security reviewed
7. Dependencies justified
8. Public API reviewed for breaking changes

**Red Flags:**
- `unsafe` blocks
- `unwrap()` or `expect()` in library code
- Large functions (>50 lines)
- Deep nesting (>3 levels)
- Many generic parameters
- Commented-out code
- Magic numbers
- Global mutable state
