---
name: rust-development
description: Guide for Rust code development, testing, and verification harnesses. Use when asked about Rust coding standards, clippy, formatting, memory management, or debugging Rust code.
---

# Rust Development Guide

## Coding Conventions

### General Standards
- Follow standard Rust formatting (run `cargo fmt` before committing)
- Address all clippy warnings (`cargo clippy -- -D warnings`)
- Write tests for new functionality
- Use meaningful test names prefixed with `test_`

### Code Organization
- **Testbench tests are integration tests** (in `testbench/tests/`, not unit tests)
- Each test file in `testbench/tests/` is compiled as a separate binary
- Use `HashMap<u32, u32>` for instruction/data memory
- Prefer Safe Rust over `unsafe` (only use `unsafe` at FFI boundaries)

## Mandatory Code Quality Checks

**BEFORE COMMITTING ANY RUST CODE:**

### 1. Format Code
```bash
cargo fmt
```

For the `rust-test-program` (if modified):
```bash
cd rust-test-program
cargo fmt
cd ..
```

Check formatting without modifying:
```bash
cargo fmt -- --check
```

### 2. Run Clippy (Zero Tolerance for Warnings)

**ALWAYS use auto-fix first to save time:**
```bash
cargo clippy --fix --allow-dirty
```

Then rerun clippy to check for any remaining or newly introduced warnings:
```bash
cargo clippy -- -D warnings
```

All clippy warnings must be addressed. The `--fix --allow-dirty` flags automatically fix many common issues even with uncommitted changes, avoiding unnecessary manual work. Always rerun clippy after auto-fix to catch any new warnings introduced by the fixes.

For the `rust-test-program` (if modified):
```bash
cd rust-test-program
cargo clippy --fix --allow-dirty
cargo clippy -- -D warnings
cd ..
```

### 3. Run Tests
```bash
cargo test --verbose
```

All tests must pass before committing.

**Note:** The `rust-test-program/` directory is a separate Rust project that builds for the RISC-V target platform (`riscv32imafc-unknown-none-elf`). If you modify any files in this directory, you MUST run the formatting and clippy checks in that directory as well, as it is checked separately in CI.

## Best Practices

### Memory Management

**DO:**
- ✅ Use callbacks for event handling
- ✅ Use proper ownership patterns (move semantics, borrowing)
- ✅ Consider `Rc<T>` or `Arc<T>` for shared ownership
- ✅ Use `RefCell<T>` or `Mutex<T>` for interior mutability when needed

**DON'T:**
- ❌ **Never use `Box::leak()`** to circumvent lifetime issues
  - This creates memory leaks
  - Bad practice that defeats Rust's safety guarantees
  - Restructure your code instead

### Choosing the Right Approach

The best solution for lifetime/ownership issues depends on the situation:

- **Single-threaded shared ownership:** Consider `Rc<RefCell<T>>`
- **Multi-threaded shared ownership:** Consider `Arc<Mutex<T>>`
- **Callbacks/closures:** Often the cleanest solution for event-driven code
- **Restructure ownership:** Sometimes refactoring is the right answer

**Key Principle:** Prefer solutions that work with Rust's ownership system, not against it.

### Error Handling

- Never use `.unwrap()` in production code
- Propagate errors with `Result<T, E>`
- Define custom error types for clarity
- Use `?` operator for error propagation

### Type Safety

- Prefer explicit types (`u8`, `u32`, `u64`) over `usize` when modeling hardware
- Use `#[repr(C)]` structs for FFI compatibility
- Avoid `as` casting - use `try_into()` or explicit masking

### Documentation

- Document public APIs with `///` doc comments
- Explain non-obvious implementation details with `//` comments
- Include examples in doc comments when helpful

## Debugging Rust Code

### Enable Verbose Output
```bash
cargo test -- --nocapture  # See println! output from tests
cargo test -- --show-output # Show output even for passing tests
```

### Run Single Test
```bash
cargo test test_name --nocapture
```

### Debug Build
```bash
cargo build  # Debug build (default)
cargo build --release  # Release build (optimized)
```

## Working with Hardware Simulations

### Verilator Integration

When interfacing with Verilator-generated C++ code:

1. **Use marlin crate abstractions** - don't call Verilator directly
2. **Clean build after RTL changes:** `cargo clean` to clear Verilator cache
3. **Check target/verilator/** for compilation artifacts if issues arise

### Concrete Data Debugging

**CRITICAL:** When debugging hardware simulations:

- ✅ **Extract actual signal values** from simulation
- ✅ **Add `$display()` to RTL** to observe hardware state
- ✅ **Print actual register/signal values** before forming hypotheses
- ✅ **Base all reasoning on concrete evidence**
- ❌ **Don't predict** what hardware "should" be doing without checking

### Example: Debugging Hardware Behavior

**Wrong approach:**
```rust
// "The PC should be X because..." (assumption-based reasoning)
assert_eq!(core.pc, expected_value);  // May fail
```

**Right approach:**
```rust
// First, add debug output to observe actual behavior
println!("Actual PC: 0x{:08x}", core.pc);
// Then form hypothesis based on observed data
// Then add assertions based on understanding from data
```

## Project-Specific Patterns

### Test Structure

```rust
#[test]
fn test_descriptive_name() {
    // Setup
    let runtime = create_runtime();
    let mut dut = TestModule::new(&runtime);
    
    // Initialize
    dut.reset.set(true);
    dut.prop();
    dut.reset.set(false);
    
    // Test logic
    // ...
    
    // Assertions
    assert_eq!(dut.output.get(), expected_value);
}
```

### Helper Macros

```rust
// Clock cycle helper
clock_cycle!(dut);

// Runtime creation
create_runtime()
```

### Memory Access Patterns

For memory operations in testbenches:

```rust
// Read dmem_addr AFTER eval() for stores
dut.eval();
let addr = dut.dmem_addr.get();

// Set dmem_rdata BEFORE eval() for loads
dut.dmem_rdata.set(value);
dut.eval();
```

## Common Anti-Patterns to Avoid

1. **Global mutable state:** Avoid `static mut`
2. **Unwrapped results:** Never use `.unwrap()` in long-running code
3. **Skipping code quality checks:** Always run `cargo fmt` and `cargo clippy --fix --allow-dirty` then `cargo clippy -- -D warnings`
4. **Manual clippy fixes:** Don't manually fix warnings that `cargo clippy --fix --allow-dirty` can handle automatically
5. **Implicit casting:** Use `try_into()` instead of `as`
6. **Memory leaks:** Never use `Box::leak()` to solve lifetime issues

## Resources

- **Rust Book:** https://doc.rust-lang.org/book/
- **Rust by Example:** https://doc.rust-lang.org/rust-by-example/
- **Clippy Lints:** https://rust-lang.github.io/rust-clippy/
- **Marlin Documentation:** https://docs.rs/marlin/
