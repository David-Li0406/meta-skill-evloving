---
name: rtl-development
description: Guide for RTL design and SystemVerilog development on the RISC-V CPU. Use when asked about CPU architecture, instruction set, FSM states, memory interface, or SystemVerilog coding conventions.
---

# RTL Development Guide

## Project Overview

This is a **multi-cycle non-pipelined RISC-V RV32IMACF CPU** implementation in SystemVerilog with Rust-based verification.

**Key Components:**
- **Architecture:** Multi-cycle non-pipelined design with 12-state FSM (including S_ATOMIC_RMW for atomic operations) and variable-latency memory support
- **Memory Interface:** Ready/valid handshaking for instruction and data memory operations
- **Instruction Set:** RV32IMACF_Zicsr (118 instructions: 40 base + 8 multiply/divide + 11 atomic + 27 compressed + 26 floating-point + 6 CSR)

## Module Hierarchy

```
top (CPU)
├── fetch_buffer (RV32C fetch buffer - manages compressed instruction alignment)
├── decompress (RV32C instruction decompressor - combinational)
├── decoder (Instruction decoder)
├── alu (ALU operations - RV32I + M extension)
│   └── div_unit (Hardware division unit)
├── regfile (Register file)
├── csr_file (Control and Status Registers)
├── branch_unit (Branch comparison)
├── mem_interface (Memory interface logic)
└── writeback_mux (Result selection)
```

## Multi-cycle Architecture

### FSM States

The CPU uses a 12-state finite state machine:

1. **S_IDLE (0x0):** After reset, before first fetch
2. **S_FETCH (0x1):** Request instruction from memory, wait for `imem_ready`
3. **S_DECODE (0x2):** Decode instruction, read registers
4. **S_EXECUTE (0x3):** Execute ALU operation
5. **S_MEM_ADDR (0x4):** Calculate memory address for load/store
6. **S_MEM_READ (0x5):** Request data from memory, wait for `dmem_ready`
7. **S_MEM_WRITE (0x6):** Write data to memory, wait for `dmem_ready`
8. **S_WRITEBACK (0x7):** Write result to destination register
9. **S_BRANCH (0x8):** Evaluate branch condition and update PC
10. **S_CSR (0x9):** Execute CSR operation
11. **S_ATOMIC_RMW (0xB):** Atomic read-modify-write operations
12. **S_HALT (0xA):** ECALL/EBREAK halt state

### Instruction Cycle Counts

Different instruction types require different numbers of cycles:

| Instruction Class | Base Cycles | States |
|-------------------|-------------|--------|
| R-type (ADD, SUB, etc.) | 4 | FETCH → DECODE → EXECUTE → WRITEBACK |
| I-type Arithmetic | 4 | FETCH → DECODE → EXECUTE → WRITEBACK |
| Load (LW, LH, LB) | 5 | FETCH → DECODE → MEM_ADDR → MEM_READ → WRITEBACK |
| Store (SW, SH, SB) | 4 | FETCH → DECODE → MEM_ADDR → MEM_WRITE |
| Branch | 3 | FETCH → DECODE → BRANCH |
| Jump (JAL/JALR) | 4 | FETCH → DECODE → EXECUTE → WRITEBACK |
| Upper Immediate | 4 | FETCH → DECODE → EXECUTE → WRITEBACK |
| M-Extension (MUL/DIV) | 4 | FETCH → DECODE → EXECUTE → WRITEBACK |
| System (FENCE) | 2 | FETCH → DECODE |
| System (ECALL/EBREAK) | 2 | FETCH → DECODE → HALT |
| CSR Operations | 4 | FETCH → DECODE → CSR → WRITEBACK |

**Note:** Memory latency adds additional cycles. For example, with 3-cycle memory latency, a load instruction takes 5 base cycles + 3 cycles in FETCH + 3 cycles in MEM_READ = 11 total cycles.

### Memory Interface Signals

The multi-cycle design adds handshaking signals:

**Instruction Memory:**
- `imem_req` (output): CPU requests instruction fetch
- `imem_ready` (input): Memory has valid instruction data
- `imem_addr` (output): Instruction address
- `imem_data` (input): Instruction data

**Data Memory:**
- `dmem_req` (output): CPU requests memory operation
- `dmem_ready` (input): Memory operation complete
- `dmem_addr` (output): Data address
- `dmem_wdata` (output): Write data
- `dmem_rdata` (input): Read data
- `dmem_we` (output): Write enable
- `dmem_re` (output): Read enable
- `dmem_size` (output): Operation size (byte/halfword/word)

### Instruction Completion Signal

- `instr_complete` (output): High for 1 cycle when instruction finishes execution

## Supported Instructions

### RV32I Base (40 instructions):
- **Arithmetic:** ADD, ADDI, SUB
- **Logic:** AND, ANDI, OR, ORI, XOR, XORI
- **Shifts:** SLL, SLLI, SRL, SRLI, SRA, SRAI
- **Comparison:** SLT, SLTI, SLTU, SLTIU
- **Branches:** BEQ, BNE, BLT, BGE, BLTU, BGEU
- **Memory:** LW, LH, LB, LHU, LBU, SW, SH, SB
- **Upper Immediate:** LUI, AUIPC
- **Jumps:** JAL, JALR
- **Memory Ordering:** FENCE
- **System:** ECALL, EBREAK

### M Extension - Integer Multiplication and Division (8 instructions):
- **Multiplication:** MUL, MULH, MULHSU, MULHU
- **Division:** DIV, DIVU
- **Remainder:** REM, REMU

### A Extension - Atomic Instructions (11 instructions):
- **Load-Reserved/Store-Conditional:** LR.W, SC.W
- **Atomic Memory Operations:** AMOSWAP.W, AMOADD.W, AMOXOR.W, AMOAND.W, AMOOR.W
- **Atomic MIN/MAX:** AMOMIN.W, AMOMAX.W, AMOMINU.W, AMOMAXU.W

### C Extension - Compressed Instructions (27 instructions):
- **Quadrant 0:** C.ADDI4SPN, C.LW, C.SW
- **Quadrant 1:** C.NOP, C.ADDI, C.JAL, C.LI, C.ADDI16SP, C.LUI, C.SRLI, C.SRAI, C.ANDI, C.SUB, C.XOR, C.OR, C.AND, C.J, C.BEQZ, C.BNEZ
- **Quadrant 2:** C.SLLI, C.LWSP, C.JR, C.MV, C.EBREAK, C.JALR, C.ADD, C.SWSP
- **Benefits:** 16-bit encoding (vs 32-bit standard), 25-30% code size reduction, seamless mixing with standard instructions

### F Extension - Single-Precision Floating-Point (26 instructions):
- **Arithmetic:** FADD.S, FSUB.S, FMUL.S, FDIV.S, FSQRT.S
- **Fused Multiply-Add:** FMADD.S, FMSUB.S, FNMSUB.S, FNMADD.S
- **MIN/MAX:** FMIN.S, FMAX.S
- **Sign Injection:** FSGNJ.S, FSGNJN.S, FSGNJX.S
- **Comparisons:** FEQ.S, FLT.S, FLE.S
- **Conversions:** FCVT.W.S, FCVT.WU.S, FCVT.S.W, FCVT.S.WU
- **Load/Store:** FLW, FSW
- **Move/Classify:** FMV.X.W, FMV.W.X, FCLASS.S
- **Features:** 32-register FP file (f0-f31), IEEE 754-2008 compliant, FCSR for rounding modes and exception flags

### Zicsr Extension (6 instructions):
- **CSR Access:** CSRRW, CSRRS, CSRRC, CSRRWI, CSRRSI, CSRRCI

## Key Design Decisions

1. **Multi-cycle execution:** Instructions take 3-5+ base cycles plus variable memory latency
2. **FSM-based control:** 12-state finite state machine
3. **Variable-latency memory:** Ready/valid handshaking on instruction and data memory interfaces
4. **Exposed memory ports:** Instruction and data memory are external (managed by testbench)
5. **Register x0 hardwired to zero:** Hardware enforcement (not just software convention)
6. **Separate branch unit:** Dedicated branch comparison logic (not ALU-based)
7. **CSR support:** Full Control and Status Register implementation (Zicsr extension)
8. **FIFO-based debug:** MMIO FIFO at 0x40000000 for host communication with packet protocol
9. **Staging registers:** Flip-flop based intermediate storage for multi-cycle operation (FPGA-safe, no latches)

## Coding Conventions

### Signal Naming
- Use `snake_case` for signal names
- Prefix with purpose: `imem_`, `dmem_`, `alu_`, etc.
- Keep ports consistent with RISC-V naming: `rs1`, `rs2`, `rd`, `funct3`, etc.

### Linting
```bash
# Lint SystemVerilog files before committing
verilator --lint-only rtl/*.sv
```

All SystemVerilog code should pass Verilator linting before being committed.

## Debugging Hardware

**CRITICAL RULE:** When debugging hardware, **NEVER rely heavily on abstract reasoning** about what signals "should" be doing.

### Correct Debugging Approach

1. **Add `$display()` statements** to observe actual signal values
2. **Print state transitions** to see FSM behavior
3. **Observe timing** with cycle-by-cycle output
4. **Base hypotheses on concrete data** from simulation
5. **Verify assumptions** with additional instrumentation

### Example Debug Instrumentation

```systemverilog
always_ff @(posedge clk) begin
    if (state == S_FETCH) begin
        $display("FETCH: pc=%h instr=%h imem_ready=%b", pc, imem_data, imem_ready);
    end
    if (state == S_EXECUTE) begin
        $display("EXECUTE: alu_op=%h rs1_data=%h rs2_data=%h result=%h", 
                 alu_op, rs1_data, rs2_data, alu_result);
    end
end
```

### What NOT to Do

- ❌ Assuming signal values without checking them
- ❌ Predicting FSM state transitions without observation
- ❌ Guessing timing relationships
- ❌ Reasoning through complex logic without concrete data

**Key Principle:** Treat hardware debugging like experimental science - observe first, then reason based on evidence.
