---
name: assertion-design
description: Use this skill when defining timing requirements, protocol specifications, or formal properties for RTL verification using SystemVerilog Assertions (SVA) as executable specifications.
---

# Assertion-Based Specification Design

SVA methodology treating assertions as executable specifications, not testbench utilities.

## Core Principle (MANDATORY)

**Specifications SHALL be written as SystemVerilog Assertions**

- Natural language explanations are secondary and optional.
- RTL implementation details MUST NOT be referenced unless unavoidable.
- Written assertions MUST be sufficient to understand intended behavior without reading RTL.
- Assertions define **what** the design must do, not **how** it does it.

## When to Use This Skill

- Defining timing specifications for RTL modules.
- Specifying protocol requirements (AXI4, UART, custom interfaces).
- Creating formal properties for transaction sequences.
- Reviewing assertion coverage completeness.
- Debugging temporal property failures.

## Directory and File Policy (MANDATORY)

### Assertion File Locations

```
sim/assertions/
├── spec/              # Timing-related specifications (REQUIRED location)
│   ├── uart_timing_spec.sva
│   ├── axi4_protocol_spec.sva
│   └── frame_parser_timing_spec.sva
├── functional/        # Functional correctness assertions
│   ├── Frame_Parser_Assertions.sv
│   └── Uart_Tx_Assertions.sv
└── bind/              # Bind statements
    ├── bind_Frame_Parser.sv
    └── bind_Uart_Tx.sv
```

**Critical Rules:**
- All timing-related specifications → [sim/assertions/spec/](../../sim/assertions/spec/)
- Functional module assertions → [sim/assertions/functional/](../../sim/assertions/functional/)
- Bind statements → [sim/assertions/bind/](../../sim/assertions/bind/)
- **NEVER** embed assertions inside DUT modules.

## Assertion Separation (MANDATORY)

### ❌ Wrong: Assertions in DUT

```systemverilog
module Frame_Parser (/*...*/);
    // ❌ Never embed assertions in DUT
    assert property (@(posedge clk) frame_valid |-> byte_count >= 4);
endmodule
```

### ✅ Correct: Separate Assertion Module

```systemverilog
// File: sim/assertions/functional/Frame_Parser_Assertions.sv
module Frame_Parser_Assertions (
    input logic clk, 
    input logic rst, 
    input logic frame_valid,
    input logic [7:0] byte_count
);
    // Property definition
    property p_frame_minimum_length;
        @(posedge clk) disable iff (rst)
        frame_valid |-> byte_count >= 4;
    endproperty
```