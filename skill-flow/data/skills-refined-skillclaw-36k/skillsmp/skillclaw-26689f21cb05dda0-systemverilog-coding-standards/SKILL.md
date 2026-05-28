---
name: systemverilog-coding-standards
description: Use this skill when generating RTL modules, interfaces, state machines, or reviewing SystemVerilog code structure for FPGA/ASIC design.
---

# SystemVerilog Coding Standards

This skill provides comprehensive SystemVerilog coding standards for production RTL design, including guidelines for generating RTL modules, interfaces, and UVM components.

## When to Use This Skill

- Generating new RTL modules, interfaces, or packages
- Creating state machines or combinational/sequential logic
- Reviewing or refactoring existing SystemVerilog code
- Resolving naming convention or structural questions
- Implementing design patterns (FSMs, FIFOs, counters)
- Writing UVM testbench components and assertions

## Critical Rules (Never Violate)

### 1. Timescale Directive (MANDATORY)
Every RTL, interface, and testbench file MUST begin with:
```systemverilog
`timescale 1ns / 1ps
```

### 2. Variable Declaration Placement (MANDATORY)
All variable declarations MUST be at the beginning of module/block:

✅ **Correct:**
```systemverilog
module Example (/*...*/);
    // All declarations first
    typedef enum logic [1:0] {IDLE, RUN, DONE} state_t;
    state_t state, state_next;
    logic [7:0] counter;
    logic valid;
    
    // Logic follows declarations
    always_comb begin
        // ...
    end
endmodule
```

❌ **Wrong:**
```systemverilog
module Example (/*...*/);
    logic [7:0] counter;
    
    always_comb begin
        logic temp;  // ❌ Declaration inside block
        temp = counter + 1;
    end
endmodule
```

### 3. Reset Convention (MANDATORY)
Default: Synchronous, active-high reset

✅ **Standard:**
```systemverilog
always_ff @(posedge clk) begin
    if (rst) begin
        counter <= '0;
    end else begin
        counter <= counter + 1;
    end
end
```

For active-low reset, invert explicitly:
```systemverilog
module My_Module (input logic clk, input logic rst_n);
    logic rst;
    assign rst = ~rst_n;  // Explicit inversion
    
    always_ff @(posedge clk) begin
        if (rst) begin  // Use internal active-high
            // ...
        end
    end
endmodule
```

### 4. Always Block Types (MANDATORY)
- Use `always_ff` for sequential logic
- Use `always_comb` for combinational logic
- Never use `always @*` in new code

```systemverilog
// Combinational logic
always_comb begin
    data_next = data;
    if (increment) data_next = data + 1;
end

// Sequential logic
always_ff @(posedge clk) begin
    if (rst) begin
        data <= '0;
    end else begin
        data <= data_next;
    end
end
```

### 5. Assertion Separation (MANDATORY)
Assertions MUST NEVER be written inside DUT modules. Always:
- Create separate assertion module (e.g., `Frame_Parser_Assertions.sv`)
- Use `bind` statement to connect assertion module to DUT
- Store in `sim/assertions/functional/` or `sim/assertions/spec/`

❌ **Wrong:**
```systemverilog
module Frame_Parser (/*...*/);
    // ❌ Never embed assertions in DUT
    assert property (@(posedge clk) frame_valid |-> byte_count >= 4);
endmodule
```

✅ **Correct:**
```systemverilog
// File: sim/assertions/functional/Frame_Parser_Assertions.sv
module Frame_Parser_Assertions (
    input logic clk, rst, frame_valid,
    input logic [7:0] byte_count
);
    assert property (@(posedge clk) disable iff (rst)
        frame_valid |-> byte_count >= 4);
endmodule

// File: sim/assertions/bind/bind_Frame_Parser.sv
`ifdef ENABLE_ASSERTIONS
bind Frame_Parser Frame_Parser_Assertions u_assertions (.*);
`endif
```

### 6. Production Quality (MANDATORY)
Never generate placeholder code or incomplete implementations.