# Common snforge Test Errors and Solutions

## 1. "found an unexpected cycle during cost computation"

### Symptoms
- `scarb build` succeeds
- `scarb test` or `snforge test` fails with:
  ```
  [ERROR] found an unexpected cycle during cost computation
  [ERROR] Error while compiling Sierra...
  ```

### Root Cause
The `enable-gas = false` setting in `Scarb.toml` breaks the Sierra cost computation system when compiling tests. This setting prevents the compiler from properly calculating gas costs, which are required for test execution.

### Solution
In `Scarb.toml`, either:
1. Remove the `enable-gas = false` line entirely, OR
2. Change it to `enable-gas = true`

```toml
# Before (broken)
[cairo]
enable-gas = false

# After (fixed)
[cairo]
enable-gas = true
```

### Why This Happens
snforge needs to compute execution costs for tests. When gas computation is disabled, the Sierra compiler encounters a cycle trying to resolve costs that don't exist, leading to this cryptic error.

---

## 2. "Error while compiling Sierra. Make sure you have the latest universal-sierra-compiler"

### Symptoms
- Cairo compilation succeeds
- Sierra compilation fails with version-related hints

### Root Cause
Version mismatch between:
- Cairo compiler version (e.g., 2.14.0)
- universal-sierra-compiler version (e.g., 2.6.0)

### Diagnosis
```bash
# Check versions
scarb --version
snforge --version
universal-sierra-compiler --version
snforge check-requirements
```

### Solution
Update the entire toolchain:
```bash
# Update snforge and universal-sierra-compiler
curl -L https://raw.githubusercontent.com/foundry-rs/starknet-foundry/master/scripts/install.sh | sh
snfoundryup

# Also update snforge_std in Scarb.toml to match
```

### Version Compatibility
- snforge 0.55.0 requires universal-sierra-compiler 2.7.0+
- Cairo 2.14.0 requires Sierra 1.7.0 support
- Always keep snforge_std version in sync with snforge CLI version

---

## 3. Generic Implementation Compilation Errors

### Symptoms
- Generic trait implementations fail to compile
- Errors about missing `Drop` or `Copy` implementations

### Root Cause
Generic implementations in Cairo require explicit trait bounds to tell the compiler how to handle generic types.

### Solution
Add trait bounds to the implementation:

```cairo
// Before (may fail)
impl PairSwap<T> of Swap<T> {
    fn swap(self: Pair<T>) -> Pair<T> { ... }
}

// After (correct)
impl PairSwap<T, +Drop<T>, +Copy<T>> of Swap<T> {
    fn swap(self: Pair<T>) -> Pair<T> { ... }
}
```

Also add derives to generic structs:
```cairo
#[derive(Drop, Copy)]
struct Pair<T> {
    first: T,
    second: T,
}
```

### When to Use Which Bounds
- `+Drop<T>`: When values of type T might be dropped (most cases)
- `+Copy<T>`: When values need to be copied (field access, multiple uses)
- `+Destruct<T>`: For types that need explicit destruction

---

## 4. Debugging Strategy

### Step 1: Isolate the Problem
```bash
# Does build work?
scarb build

# Does the simplest possible test work?
# Create a test with just: assert(true, 'ok');
```

### Step 2: Check Configuration
```bash
# Review Scarb.toml
cat Scarb.toml

# Check for problematic settings:
# - enable-gas = false
# - Mismatched dependency versions
```

### Step 3: Check Toolchain
```bash
snforge check-requirements
scarb --version
universal-sierra-compiler --version
```

### Step 4: Try Direct Sierra Compilation
```bash
# Build and get Sierra file
scarb build

# Try compiling Sierra directly
universal-sierra-compiler compile-raw --sierra-path target/dev/*.sierra.json
```

---

## 5. Quick Reference: Scarb.toml for Testing

```toml
[package]
name = "my_project"
version = "0.1.0"
edition = "2024_07"

[scripts]
test = "snforge test"

[cairo]
# Do NOT set enable-gas = false when using snforge
# enable-gas = true  # This is the default, can be omitted

[dependencies]
snforge_std = "0.55.0"  # Match your snforge CLI version

[dev-dependencies]
# Add test-only dependencies here
```
