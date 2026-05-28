---
name: debugging
description: Comprehensive debugging guide for hardware and software issues. Use when debugging test failures, RTL bugs, or troubleshooting build/runtime problems.
---

# Debugging and Troubleshooting Guide

## General Debugging Philosophy

### Concrete Data Over Abstract Reasoning

**CRITICAL PRINCIPLE:** When debugging this hardware verification project, always prioritize concrete, observable data over abstract reasoning or assumptions.

**Why this matters:**
- Hardware behavior is complex and timing-dependent
- Multi-cycle FSMs have subtle state transitions
- Memory interfaces have timing constraints
- Small mistakes in assumptions lead to large debugging detours

## Debugging Hardware (RTL)

### Correct Approach: Data-Driven Debugging

**✅ DO THIS:**

1. **Add `$display()` statements** to observe actual signal values
2. **Print state transitions** to see FSM behavior
3. **Observe timing** with cycle-by-cycle output
4. **Base hypotheses on concrete data** from simulation
5. **Verify assumptions** with additional instrumentation

### Example: Debugging State Machine Issues

```systemverilog
// Add to top.sv or relevant module
always_ff @(posedge clk) begin
    if (state != next_state) begin
        $display("STATE TRANSITION: %s -> %s (pc=%h)", 
                 state_name(state), state_name(next_state), pc);
    end
    
    if (state == S_FETCH) begin
        $display("FETCH: pc=%h imem_req=%b imem_ready=%b imem_data=%h", 
                 pc, imem_req, imem_ready, imem_data);
    end
    
    if (state == S_EXECUTE) begin
        $display("EXECUTE: alu_op=%h rs1=%h rs2=%h result=%h", 
                 alu_op, rs1_data, rs2_data, alu_result);
    end
end
```

### What NOT to Do

**❌ DON'T DO THIS:**

- Assuming signal values without checking them
- Predicting FSM state transitions without observation
- Guessing timing relationships
- Reasoning through complex logic without concrete data
- Saying "it should be X because..." without verifying

### Example: Wrong vs Right Debugging

**❌ WRONG:**
```
"The PC should be 0x104 after this instruction because it's a 4-byte 
instruction and we started at 0x100, so the problem must be..."
```

**✅ RIGHT:**
```systemverilog
// First, add debug output to RTL
always_ff @(posedge clk) begin
    if (state == S_WRITEBACK) begin
        $display("WRITEBACK: pc=%h next_pc=%h", pc, pc_next);
    end
end
```

```rust
// Then run test and observe actual output:
// Output: "WRITEBACK: pc=00000100 next_pc=00000102"
// Now we know it's a compressed instruction (2 bytes), not 4 bytes!
```

## Debugging Rust Tests

### Enable Verbose Output

```bash
# See all println! output from tests
cargo test -- --nocapture

# Show output even for passing tests
cargo test -- --show-output

# Run single test with output
cargo test test_name -- --nocapture
```

### Add Debug Prints

```rust
#[test]
fn test_something() {
    // ... setup ...
    
    println!("PC before: 0x{:08x}", dut.pc.get());
    clock_cycle!(dut);
    println!("PC after: 0x{:08x}", dut.pc.get());
    
    println!("State: {:?}", get_state(&dut));
    println!("ALU result: 0x{:08x}", dut.alu_result.get());
    
    // Now you have concrete data to reason about
}
```

### Check Memory State

```rust
// Inspect memory contents
println!("Memory at 0x{:08x}: 0x{:08x}", addr, mem.get(&addr).unwrap_or(&0));

// Check instruction memory
println!("Instruction at PC: 0x{:08x}", imem.get(&pc).unwrap_or(&0));
```

## Delegating Complex Debugging Tasks

**IMPORTANT:** For non-trivial debugging that doesn't relate to your main task, delegate to specialized agents.

### When to Delegate Debugging

Delegate when:
- Debugging session becomes extensive (>5 minutes)
- Issue spans multiple modules or layers
- You need deep expertise in a specific area
- The debugging distracts from your main task

**Exception:** If the user's primary request IS debugging, handle it directly.

### How to Delegate

Use the `task` tool to spawn specialized debugging agents:

```
For RTL debugging:
  agent_type="fpga-architect"
  prompt="Debug why the ALU is producing incorrect results for SRA instruction"

For Rust test debugging:
  agent_type="rust-verification-architect"
  prompt="Debug why test_branch_conditions is failing"

For integration issues:
  agent_type="hw-sw-integration-architect"
  prompt="Debug why memory loads are taking 20 cycles instead of expected 8"
```

### Benefits of Delegation

- **Preserves main context:** Keep your primary task context clean
- **Specialized expertise:** Get domain-specific debugging skills
- **Parallel work:** Can investigate while you continue other work
- **Better solutions:** Specialized agents have deeper knowledge

## Common Issues and Solutions

### Issue: Tests fail with "Verilator not found"

**Symptoms:**
```
Error: Invocation of Verilator failed
Error: No such file or directory
```

**Solution:**
```bash
sudo apt-get update
sudo apt-get install -y verilator
verilator --version  # Verify installation
```

### Issue: Tests fail after RTL changes

**Symptoms:**
- Tests that passed before now fail
- Unexpected behavior in simulation
- Verilator compilation errors

**Solution:**
```bash
cargo clean  # Clear cached Verilator builds
cargo test   # Rebuild from scratch
```

**Why:** Verilator caches compiled RTL. Changes may not be picked up without cleaning.

### Issue: Formatting errors in CI

**Symptoms:**
```
error: some files are not formatted correctly
```

**Solution:**
```bash
cargo fmt              # Auto-format all Rust code
git add .
git commit -m "Apply cargo fmt"
git push
```

### Issue: Clippy warnings

**Symptoms:**
```
warning: unused variable: `x`
warning: this expression creates a reference which is immediately dereferenced
```

**Solution:**
```bash
cargo clippy --fix     # Auto-fix when possible
# Manually fix remaining issues
cargo clippy -- -D warnings  # Verify all fixed
```

### Issue: Memory address out of range

**Symptoms:**
- Tests accessing invalid memory addresses
- Segmentation faults in simulation

**Solution:**
- DRAM range is 0x80000000 - 0xFFFFFFFF
- Use `lui(reg, 0x80000000)` then `sw(reg, val, offset)` for memory ops
- Check test is using valid address ranges

### Issue: Test hangs or times out

**Symptoms:**
- Test never completes
- CI times out
- Infinite loop suspected

**Debugging:**
1. Add timeout to test:
```rust
#[test]
#[timeout(5000)]  // 5 second timeout
fn test_name() {
    // ...
}
```

2. Add debug output to find where it hangs:
```rust
println!("Before operation A");
operation_a();
println!("Before operation B");
operation_b();
// Last printed line shows where hang occurs
```

3. Check for infinite FSM loops in RTL:
```systemverilog
always_ff @(posedge clk) begin
    $display("Cycle %d: state=%s", cycle_count, state_name(state));
end
```

### Issue: Assertion failure with unclear cause

**Symptoms:**
```
assertion `left == right` failed
  left: 0x00000104
 right: 0x00000108
```

**Debugging:**
1. Add context to assertion:
```rust
assert_eq!(
    actual, expected,
    "PC mismatch after instruction: actual=0x{:08x}, expected=0x{:08x}",
    actual, expected
);
```

2. Print intermediate values:
```rust
println!("Before: pc=0x{:08x}", dut.pc.get());
execute_instruction(&mut dut);
println!("After: pc=0x{:08x}", dut.pc.get());
assert_eq!(dut.pc.get(), expected);
```

3. Check RTL signals:
```systemverilog
$display("PC update: old=%h new=%h taken=%b", pc, pc_next, branch_taken);
```

## Advanced Debugging Techniques

### VCD Waveform Analysis

Generate VCD files for signal inspection:

```rust
use riscv_core::VcdDumper;

let mut vcd = VcdDumper::new("debug.vcd");
// Run simulation
vcd.dump(&dut);
```

View with GTKWave:
```bash
gtkwave debug.vcd
```

### Instruction Trace Analysis

Enable instruction tracing:

```rust
cpu.set_trace_callback(|instr| {
    println!("PC: 0x{:08x} Instr: {:?}", instr.pc, instr);
});
```

### Cycle-by-Cycle Stepping

Single-step through simulation:

```rust
for cycle in 0..100 {
    println!("\n=== Cycle {} ===", cycle);
    println!("PC: 0x{:08x}", dut.pc.get());
    println!("State: {:?}", get_state(&dut));
    clock_cycle!(dut);
    if condition_met {
        break;
    }
}
```

### Memory Dump

Inspect memory contents:

```rust
fn dump_memory(mem: &HashMap<u32, u32>, start: u32, count: usize) {
    for i in 0..count {
        let addr = start + (i as u32 * 4);
        let value = mem.get(&addr).unwrap_or(&0);
        println!("0x{:08x}: 0x{:08x}", addr, value);
    }
}
```

## Debugging Workflow

### Recommended Process

1. **Reproduce the issue** locally with minimal test case
2. **Add debug output** to observe actual behavior
3. **Collect concrete data** from simulation
4. **Form hypothesis** based on observed data
5. **Test hypothesis** with additional instrumentation
6. **Fix the issue** based on understanding
7. **Verify fix** with original test and edge cases
8. **Remove debug output** (or keep if useful for future)

### Debugging Checklist

- [ ] Can reproduce issue locally
- [ ] Have minimal test case that triggers issue
- [ ] Added debug output to observe actual behavior
- [ ] Collected concrete signal values from simulation
- [ ] Understand root cause (not just symptoms)
- [ ] Tested fix with original failing test
- [ ] Tested fix with edge cases
- [ ] All tests pass
- [ ] Debug output removed (or kept if valuable)

## Getting Help

### When to Ask for Help

- Spent >30 minutes debugging without progress
- Issue appears to be tool/infrastructure problem
- Behavior seems non-deterministic or unexplainable
- Need expertise in unfamiliar area

### How to Ask for Help

Provide:
1. Clear description of expected vs actual behavior
2. Minimal reproducible test case
3. Relevant debug output showing concrete data
4. What you've already tried
5. Any hypotheses about root cause

### Resources

- **RISC-V Spec:** https://riscv.org/technical/specifications/
- **Verilator Manual:** https://verilator.org/guide/latest/
- **Marlin Docs:** https://docs.rs/marlin/

## Summary

**Remember:** Debugging is experimental science. Observe actual behavior, collect concrete data, then reason based on evidence—not assumptions.
