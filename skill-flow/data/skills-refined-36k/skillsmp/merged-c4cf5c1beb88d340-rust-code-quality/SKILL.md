---
name: rust-code-quality
description: Use this skill to perform comprehensive Rust code quality reviews against best practices for async Rust, error handling, testing, and project structure.
---

# Rust Code Quality Review

Systematically review Rust code quality against industry best practices, focusing on async patterns, error handling, module organization, testing, documentation, performance, and security.

## Quality Dimensions

| Dimension | Focus | Tools |
|-----------|-------|-------|
| Structure | Files <500 LOC, module hierarchy | `find . -name "*.rs"` |
| Error Handling | Custom Error, Result<T>, no unwrap | `rg "unwrap\|Result<"` |
| Async Patterns | async fn, spawn_blocking, no blocking | `rg "async fn\|spawn_blocking"` |
| Testing | >90% coverage, integration tests | `cargo tarpaulin` |
| Documentation | Public APIs 100% documented | `cargo doc --no-deps` |
| Performance | Minimize allocations, zero-copy | `rg "clone\|to_string\|Arc<|Rc<"` |
| Security | Memory safety, input validation | `rg "unsafe"` |

## Analysis Workflow

### Step 1: Project Structure Analysis
```bash
# Check workspace
cat Cargo.toml

# Verify crate organization
ls -la memory-*/

# Check file sizes
find . -name "*.rs" -not -path "*/target/*" -exec wc -l {} + | sort -rn
```

### Step 2: Code Pattern Analysis
```bash
# Error handling
rg "Result<|Error::" --glob "*.rs" | wc -l
rg "unwrap\(\)" --glob "!*/tests/*" --glob "*.rs"

# Async patterns
rg "async fn|spawn_blocking|tokio::" --glob "*.rs"

# Performance patterns
rg "clone\(\)|to_string\(\)|Arc<|Rc<" --glob "*.rs"
```

### Step 3: Testing Analysis
```bash
# Run all tests
cargo test --all -- --nocapture

# Coverage
cargo tarpaulin --out Html

# Benchmarks
cargo bench --no-run
```

### Step 4: Documentation Analysis
```bash
# Generate docs
cargo doc --no-deps

# Check for missing docs
cargo rustdoc -- -D missing_docs
```

### Step 5: Linting & Formatting
```bash
# Format check
cargo fmt -- --check

# Clippy (strict mode)
cargo clippy --all-targets --all-features -- -D warnings

# Audit dependencies
cargo audit
```

## Output Format

```markdown
# Rust Code Quality Report
**Generated**: [Date]
**Project**: rust-self-learning-memory

## Executive Summary
- **Overall Score**: X/100
- **Critical Issues**: N
- **Warnings**: M
- **Best Practices**: P/Q met

## Quality Dimensions

### 1. Project Structure: 8/10 ⭐⭐⭐⭐
✅ Good workspace organization  
✅ Clear crate separation  
⚠️ Some files exceed 500 LOC limit  

### 2. Error Handling: 9/10 ⭐⭐⭐⭐⭐
✅ Custom Error enum with thiserror  
✅ Consistent Result<T> usage  
✅ Minimal unwrap() usage (only in tests)  

### 3. Async Patterns: 7/10 ⭐⭐⭐⭐
✅ Proper async fn usage  
✅ spawn_blocking for redb  
❌ Blocking call found in async context  

### 4. Memory & Performance: 8/10 ⭐⭐⭐⭐
✅ Good use of borrowing  
✅ Minimal allocations  
⚠️ Unnecessary clones in 3 locations  

### 5. Testing: 6/10 ⭐⭐⭐
⚠️ Test coverage: 78% (target: >90%)  
✅ Good unit test coverage  

### 6. Documentation: 9/10 ⭐⭐⭐⭐⭐
✅ Crate-level docs complete  
✅ Most public APIs documented  

### 7. Type Safety: 9/10 ⭐⭐⭐⭐⭐
✅ Strong typing with Uuid  
✅ Good use of newtypes  

### 8. Security: 8/10 ⭐⭐⭐⭐
✅ No unsafe code  
✅ Parameterized SQL queries  

## Detailed Findings

### Critical Issues (Must Fix)
1. **Blocking call in async context**
   - File: memory-core/src/sync.rs:89
   - Issue: std::fs::read blocks the Tokio runtime
   - Fix: Use tokio::fs::read

### Warnings (Should Fix)
1. **File size exceeds limit**
   - File: memory-core/src/memory.rs (623 lines)
   - Target: <500 lines
   - Recommendation: Split into submodules

### Recommendations (Nice to Have)
1. Add property-based tests with proptest
2. Implement more comprehensive benchmarks

## Action Items

### High Priority
- [ ] Fix blocking call in sync.rs
- [ ] Increase test coverage to 90%

### Medium Priority
- [ ] Refactor memory.rs (split into submodules)

### Low Priority
- [ ] Reduce unnecessary clones
```

## Best Practices Checklist

Use this checklist when reviewing code:

**Project Structure**:
- [ ] Files <500 LOC
- [ ] Clear module hierarchy

**Error Handling**:
- [ ] Custom Error enum
- [ ] Result<T> for fallible ops
- [ ] No unwrap() in production

**Async/Await**:
- [ ] async fn for IO operations
- [ ] spawn_blocking for sync/CPU work
- [ ] No blocking calls in async

**Testing**:
- [ ] Unit tests (>90% coverage)
- [ ] Integration tests

**Documentation**:
- [ ] Crate docs
- [ ] Module docs
- [ ] Function docs with examples

**Performance**:
- [ ] Minimize allocations
- [ ] Use borrowing

**Security**:
- [ ] No unsafe (unless justified)
- [ ] Input validation
- [ ] Parameterized queries

## Example Usage

When invoked, this skill will:
1. Analyze project structure and organization
2. Review error handling patterns
3. Check async/await usage
4. Assess testing quality and coverage
5. Evaluate documentation completeness
6. Identify performance anti-patterns
7. Verify security practices
8. Generate comprehensive quality report with actionable items