---
name: systemverilog-coding-standards
description: Use this skill when generating SystemVerilog RTL modules, interfaces, testbenches, UVM components, or assertions, ensuring adherence to coding standards for FPGA/ASIC design.
---

# SystemVerilog Coding Standards

This skill provides comprehensive SystemVerilog coding standards for FPGA/RTL design and UVM verification.

## When to Use This Skill

Use this skill when:
- Generating new RTL modules, interfaces, or packages
- Creating UVM testbench components (tests, agents, drivers, monitors, sequences)
- Writing SystemVerilog assertions
- Reviewing or modifying existing SystemVerilog code
- Resolving naming convention questions
- Implementing state machines or design patterns

## Critical Rules (Never Violate)

### 1. Timescale Directive (MANDATORY)
Every RTL, interface, and testbench file MUST begin with:
```systemverilog
`timescale 1ns / 1ps
```

### 2. Assertion Separation (MANDATORY)
Assertions MUST NEVER be written inside DUT modules. Always:
- Create a separate assertion module (e.g., `Frame_Parser_Assertions.sv`)
- Use `bind` statement to connect assertion module to DUT
- Store in `sim/assertions/functional/` or `sim/assertions/spec/`

### 3. Variable Declaration Placement (MANDATORY)
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

### 4. Reset Convention (MANDATORY)
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

### 5. Production Quality (MANDATORY)
Never generate:
- Placeholder code or comments like `// TODO` or `// Implement later`
- Stopgap solutions
- Temporary modules
- Unverifiable logic

## Naming Conventions

### RTL Elements

| Element | Convention | Example |
|---------|-----------|---------|
| **Modules** | Capitalized_With_Underscores | `Frame_Parser`, `Uart_Tx` |
| **Signals** | lowercase_with_underscores | `rx_fifo_data`, `frame_valid` |
| **Parameters** | ALL_CAPS_WITH_UNDERSCORES | `FIFO_DEPTH`, `CLK_FREQ_HZ` |
| **Localparams** | ALL_CAPS_WITH_UNDERSCORES | `SOF_BYTE`, `STATE_WIDTH` |
| **Enums** | lowercase_t suffix | `parser_state_t`, `axi_state_t` |
| **Enum Values** | ALL_CAPS | `IDLE`, `PROCESSING`, `ERROR` |
| **Interfaces** | lowercase_if suffix | `axi4_lite_if`, `uart_if` |
| **Functions** | lowercase_with_underscores | `calculate_crc()`, `state_to_string()` |
| **Tasks** | lowercase_with_underscores | `send_byte()`, `wait_for_ack()` |

### UVM Components

| Component | Naming Pattern | Example |
|-----------|---------------|---------|
| **Test** | `<module>_<type>_test` | `axiuart_basic_test` |
| **Environment** | `<module>_env` | `axiuart_env` |
| **Agent** | `<protocol>_agent` | `uart_agent` |
| **Driver** | `<protocol>_driver` | `uart_driver` |
| **Monitor** | `<protocol>_monitor` | `uart_monitor` |
| **Sequencer** | `<protocol>_sequencer` | `uart_sequencer` |
| **Sequence** | `<protocol>_<action>_sequence` | `uart_write_sequence` |
| **Transaction** | `<protocol>_transaction` | `uart_transaction` |
| **Scoreboard** | `<module>_scoreboard` | `axiuart_scoreboard` |

### File Naming

| File Type | Pattern | Example |
|-----------|---------|---------|
| **RTL Module** | `Module_Name.sv` | `Frame_Parser.sv` |
| **Interface** | `interface_name_if.sv` | `axi4_lite_if.sv` |
| **Package** | `package_name_pkg.sv` | `axiuart_reg_pkg.sv` |
| **Testbench** | `tb_<module>.sv` | `tb_axiuart_top.sv` |
| **UVM Test** | `<test_name>.sv` | `axiuart_basic_test.sv` |
| **Assertion Module** | `<Module>_Assertions.sv` | `Frame_Parser_Assertions.sv` |
| **Bind File** | `bind_<Module>.sv` | `bind_Frame_Parser.sv` |

**Critical**: Module name MUST match file name exactly (case-sensitive).

## Design Patterns

### State Machine Template

Use three-process state machine with typed enums:

```systemverilog
// 1. State type with encoding hint
(* fsm_encoding = "one_hot" *)
typedef enum logic [3:0] {
    IDLE        = 4'b0001,
    PROCESSING  = 4'b0010,
    WAITING     = 4'b0100,
    ERROR       = 4'b1000
} state_t;

state_t state, state_next;

// 2. Helper function for debug (recommended)
function automatic string state_to_string(state_t st);
    case (st)
        IDLE:       return "IDLE";
        PROCESSING: return "PROCESSING";
        WAITING:    return "WAITING";
        ERROR:      return "ERROR";
        default:    return "UNKNOWN";
    endcase
endfunction

// 3. Combinational next-state logic
always_comb begin
    state_next = state;  // Default: hold state
    
    case (state)
        IDLE: begin
            if (start) state_next = PROCESSING;
        end
        PROCESSING: begin
            if (done) state_next = IDLE;
            else if (error) state_next = ERROR;
        end
        // ... other states
    endcase
end

// 4. Sequential state register
always_ff @(posedge clk) begin
    if (rst) begin
        state <= IDLE;
    end else begin
        state <= state_next;
    end
end

// 5. Output logic
always_comb begin
    busy = (state == PROCESSING);
    error_flag = (state == ERROR);
end
```

### Always Block Separation

Use `always_ff` for sequential logic, `always_comb` for combinational:

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

Never use `always @*` in new code (use `always_comb` instead).

### Parameter Width Calculations

Use `$clog2()` for width calculations:

```systemverilog
module Fifo #(
    parameter int DEPTH = 64,
    parameter int DATA_WIDTH = 8
)(/*...*/);
    // Address width: log2(DEPTH)
    localparam int ADDR_WIDTH = $clog2(DEPTH);  // 6 bits for 64 entries
    
    // Count width: log2(DEPTH) + 1 for full detection
    localparam int COUNT_WIDTH = $clog2(DEPTH) + 1;  // 7 bits
    
    logic [ADDR_WIDTH-1:0]  wr_ptr, rd_ptr;
    logic [COUNT_WIDTH-1:0] count;  // 0 to DEPTH (inclusive)
endmodule
```

**Critical**: 64-entry FIFO requires 6-bit addresses (0-63) and 7-bit counter (0-64).

### Module Header Format

```systemverilog
`timescale 1ns / 1ps

// Brief module description (1-2 lines)
// Key features or notes
module Module_Name #(
    // Parameters grouped by category
    parameter int WIDTH = 32,
    parameter int DEPTH = 64
)(
    // Clock and reset first
    input  logic                clk,
    input  logic                rst,
    
    // Input signals grouped logically
    input  logic [WIDTH-1:0]    data_in,
    input  logic                valid_in,
    
    // Output signals grouped logically
    output logic [WIDTH-1:0]    data_out,
    output logic                valid_out,
    
    // Debug signals last (if any)
    output logic [7:0]          debug_state
);
    // Module body
endmodule
```

### Interface Definition with Modports

```systemverilog
`timescale 1ns / 1ps

interface axi4_lite_if #(
    parameter int ADDR_WIDTH = 32,
    parameter int DATA_WIDTH = 32
)(
    input logic clk,
    input logic rst
);
    // Signal declarations
    logic [ADDR_WIDTH-1:0] awaddr;
    logic                  awvalid;
    logic                  awready;
    // ... other signals
    
    // Modport for master
    modport master (
        output awaddr, awvalid,
        input  awready
        // ... other directions
    );
    
    // Modport for slave
    modport slave (
        input  awaddr, awvalid,
        output awready
        // ... other directions
    );
endinterface
```

## UVM Verification Patterns

### UVM Component Template

```systemverilog
class uart_driver extends uvm_driver #(uart_transaction);
    `uvm_component_utils(uart_driver)
    
    virtual uart_if vif;
    
    function new(string name = "uart_driver", uvm_component parent = null);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (!uvm_config_db#(virtual uart_if)::get(this, "", "vif", vif)) begin
            `uvm_fatal(get_type_name(), "Virtual interface not found")
        endif
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        forever begin
            seq_item_port.get_next_item(req);
            drive_transaction(req);
            seq_item_port.item_done();
        end
    endtask
    
    virtual task drive_transaction(uart_transaction trans);
        // Implementation
    endtask
endclass
```

### UVM Test with Objections

```systemverilog
class axiuart_basic_test extends uvm_test;
    `uvm_component_utils(axiuart_basic_test)
    
    axiuart_env env;
    
    function new(string name = "axiuart_basic_test", uvm_component parent = null);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        env = axiuart_env::type_id::create("env", this);
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        uart_write_sequence seq;
        
        phase.raise_objection(this, "Test starting");
        `uvm_info(get_type_name(), "========== Test Started ==========", UVM_LOW)
        
        // Test body
        seq = uart_write_sequence::type_id::create("seq");
        seq.start(env.uart_agt.sequencer);
        
        #1000ns;  // Wait for processing
        
        `uvm_info(get_type_name(), "========== Test Completed ==========", UVM_LOW)
        phase.drop_objection(this, "Test completed");
    endtask
endclass
```

### UVM Logging Standards

```systemverilog
// Informational (UVM_MEDIUM or UVM_HIGH)
`uvm_info(get_type_name(), 
    $sformatf("Transaction: addr=0x%08h, data=0x%08h", trans.addr, trans.data), 
    UVM_MEDIUM)

// Error (always displayed)
`uvm_error(get_type_name(), 
    $sformatf("CRC mismatch: expected=0x%04h, got=0x%04h", exp_crc, act_crc))

// Fatal error (stops simulation)
`uvm_fatal(get_type_name(), "Watchdog timeout - DUT not responding")
```

**Verbosity guidelines:**
- `UVM_LOW`: Test start/end, major phase transitions
- `UVM_MEDIUM`: Transaction-level events (default for regression)
- `UVM_HIGH`: Detailed signal-level activity (debug only)

## Assertion Patterns

### Property Naming Convention

Use `p_` prefix for properties:

```systemverilog
// Timing assertion
property p_setup_time_met;
    @(posedge clk) $rose(data_valid) |-> $past(data_stable, 2);
endproperty

// Protocol assertion
property p_handshake_valid_before_ready;
    @(posedge clk) disable iff (rst)
    ready |-> valid;
endproperty

// State machine assertion
property p_no_illegal_state_transitions;
    @(posedge clk) disable iff (rst)
    (state == ERROR) |=> (state == IDLE);
endproperty
```

### Assertion Compilation Control

```systemverilog
// In assertion module file
`ifdef ENABLE_ASSERTIONS
module Frame_Parser_Assertions (/*...*/);
    // Assertions here
endmodule
`endif

// In bind file
`ifdef ENABLE_ASSERTIONS
bind Frame_Parser Frame_Parser_Assertions u_assertions (/*...*/);
`endif
```

Enable with: `dsim +define+ENABLE_ASSERTIONS ...`

## Project-Specific Rules

### Register Management (JSON SSOT)

Register definitions come from `register_map/axiuart_registers.json`. Never hardcode addresses.

```systemverilog
import axiuart_reg_pkg::*;

module Register_Block #(
    parameter logic [31:0] BASE_ADDR = 32'h4000_0000
)(/*...*/);
    // Compute relative offsets
    localparam logic [11:0] REG_CONTROL_OFFSET = 
        (axiuart_reg_pkg::REG_CONTROL - BASE_ADDR);
    
    always_comb begin
        case (addr_offset)
            REG_CONTROL_OFFSET: rdata = control_reg;
            REG_STATUS_OFFSET:  rdata = status_reg;
            default:            rdata = '0;
        endcase
    end
endmodule
```

### Debug Signal Instrumentation

Prefix debug signals with `debug_`:

```systemverilog
module Frame_Parser (
    // Functional ports
    input  logic clk, rst,
    output logic frame_valid,
    
    // Debug ports (at end)
    output logic [7:0] debug_rx_data,
    output logic [3:0] debug_state,
    output logic       debug_crc_error
);
    // Implementation
endmodule
```

## Pre-Commit Checklist

Before committing SystemVerilog code:

- [ ] `` `timescale 1ns / 1ps`` present in every file
- [ ] All variable declarations at beginning of module/block
- [ ] Naming conventions followed (modules, signals, parameters)
- [ ] No assertions embedded in DUT modules
- [ ] Reset type is synchronous active-high (or explicitly inverted)
- [ ] FIFO/counter widths correct (use `$clog2()`)
- [ ] Comments in English, limited to non-obvious logic
- [ ] No placeholder code
- [ ] Interface modports defined (if using interfaces)
- [ ] State machines use typed enums
- [ ] `always_ff` for sequential, `