---
name: testing
description: Guide for writing, running, and debugging tests in the RISC-V verification project. Use when asked about test structure, test best practices, running tests, or debugging test failures.
---

# Testing Guide

## Test Structure

**Important:** The `testbench` package uses **integration tests** (not unit tests). Each test file in `testbench/tests/` is compiled as a separate binary. This is the recommended pattern for Verilator-based tests because:
- Integration tests run in separate processes, preventing C++ memory conflicts
- Each test binary gets its own Verilator runtime, avoiding destructor race conditions
- Follows marlin crate's recommended usage patterns
- No manual locking or serialization required

## Test Suite Overview

The project has 264 comprehensive tests across all packages:

### testbench package (95 integration tests):
- **ALU tests (16 tests):** Validate arithmetic/logic operations + M extension (MUL, MULH, MULHSU, MULHU, DIV, DIVU, REM, REMU)
- **Register file tests (6 tests):** Validate register behavior (including x0 immutability)
- **FP register file tests (7 tests):** Validate floating-point register file with 3 read ports
- **FPU tests (25 tests):** Validate all 26 FP operations (arithmetic, comparisons, conversions, etc.)
- **Decompressor tests (41 tests):** Validate all 27 RV32C compressed instructions

### Other packages (169 tests):
- **cpu-sim: 108 integration tests including:**
  - ELF loading and execution
  - FIFO communication and packet protocol
  - VCD waveform dumping validation
  - Instruction trace callbacks with comprehensive validation
  - Programmatic instruction sequence testing with trace verification
  - FP integration tests (16 tests): Validate all 26 FP instructions in CPU context
  - Combined trace + VCD testing
  - Variable memory latency testing
  - RV32C compressed instruction tests (9 tests): Basic instructions and critical transition scenarios (C→C, C→U, U→C, U→U, mixed)
- **riscv_core: 33 utility and tracing tests**
- **riscv_protocol: 6 packet serialization/deserialization tests**
- **riscv_macros: 13 macro functionality tests**

## New Validation Tests

- `test_comprehensive_trace_validation`: Validates instruction trace accuracy for 12+ instructions with full operand checking (PC, register values, immediates)
- `test_trace_with_branches`: Ensures branch instructions skip correct sequences in trace output
- `test_trace_and_vcd_together`: Demonstrates VCD + instruction trace working simultaneously

## Running Tests

### Run all tests
```bash
cargo test
```

### Run specific test suite
```bash
cargo test --package testbench -- alu_test
cargo test --package testbench -- regfile_test
cargo test --package testbench -- cpu_test
```

### Run with verbose output
```bash
cargo test --verbose
```

### Run single test
```bash
cargo test --package testbench -- test_cpu_branch_beq_bne --nocapture
```

### Build only (without running tests)
```bash
cargo build
```

### Clean build artifacts
```bash
cargo clean  # Important after RTL changes to clear Verilator cache
```

## Testing Best Practices

### When Adding New Tests

1. **Location:** Add to appropriate test file (`alu_test.rs`, `regfile_test.rs`, or `cpu_test.rs`)
2. **Register in lib.rs:** Add module declaration if creating new test file
3. **Use helper macros:** 
   - `clock_cycle!(dut)` for clock edge transitions
   - `create_runtime()` for consistent test setup
4. **Memory management:** 
   - Use `HashMap<u32, u32>` for instruction/data memory
   - Read `dmem_addr` AFTER `eval()` for stores
   - Set `dmem_rdata` BEFORE `eval()` for loads

### Test Naming Convention

- Prefix with `test_`
- Use descriptive names: `test_cpu_branch_beq_bne`, `test_alu_shift_ops`
- Group related tests logically

## Verilator Build Process

The marlin crate automatically:
1. Compiles SystemVerilog files with Verilator
2. Creates shared libraries in `target/verilator/`
3. Links them to Rust test code

Build artifacts are cached between runs for performance.

## Debugging Tests

### Enable Verbose Output

```bash
cargo test -- --nocapture  # See println! output from tests
cargo test -- --show-output # Show output even for passing tests
```

### Check Verilator Compilation

Verilator creates intermediate C++ files in `target/verilator/`. Check these if you suspect compilation issues.

### Debugging Strategy

When debugging test failures:

1. **Enable debug output:** Use `--nocapture` flag
2. **Run single test:** Isolate the failing test
3. **Add print statements:** Use `println!()` in Rust or `$display()` in SystemVerilog
4. **Check RTL signals:** Add `$display()` statements to observe hardware state
5. **Verify assumptions:** Don't rely on abstract reasoning - observe actual signal values
6. **Clean and rebuild:** If behavior is inconsistent, run `cargo clean` first

### Non-Trivial Debugging Tasks

**IMPORTANT:** For complex debugging sessions that don't directly relate to the main task:

- **Delegate to specialized agents:** Use the `task` tool to spawn debugging-focused agents
- **Preserve main context:** Keep your primary context clean by offloading debug work
- **Exception:** If the user's primary request IS debugging, handle it directly

**When to delegate debugging:**
- Unexpected hardware behavior requiring extensive signal analysis
- Complex timing issues across multiple cycles
- Memory interface problems requiring trace analysis
- Multi-module interaction bugs

**Example delegation:**
```
Use the task tool with agent_type="fpga-architect" for RTL debugging
Use the task tool with agent_type="rust-verification-architect" for test harness debugging
```

## After Modifying RTL

1. **Lint the RTL:** `verilator --lint-only rtl/modified_file.sv`
2. **Clean build:** `cargo clean` (Verilator cache may be stale)
3. **Run tests:** `cargo test`
4. **Verify all tests pass:** Look for `test result: ok` with all tests passed
