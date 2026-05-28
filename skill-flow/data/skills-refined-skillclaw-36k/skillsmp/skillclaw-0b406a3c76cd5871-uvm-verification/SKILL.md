---
name: uvm-verification
description: Use this skill when creating UVM testbench components, such as tests, agents, drivers, monitors, sequences, or scoreboards in SystemVerilog.
---

# UVM Verification Methodology

This skill provides UVM testbench design patterns and best practices for the AXIUART_RV32I verification environment.

## When to Use This Skill

- Creating UVM testbench components (tests, environments, agents)
- Implementing drivers, monitors, sequences, or scoreboards
- Debugging UVM configuration or communication issues
- Resolving UVM naming convention questions
- Setting up factory patterns or objection management

## UVM Component Naming

### Component Hierarchy

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
| **Testbench** | `tb_<module>.sv` | `tb_axiuart_top.sv` |
| **UVM Test** | `<test_name>.sv` | `axiuart_basic_test.sv` |
| **UVM Package** | `<module>_pkg.sv` | `axiuart_uvm_pkg.sv` |

## UVM Component Templates

### Driver Template

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
            `uvm_fatal(get_type_name(), "Virtual interface not found in config DB")
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
        // Implementation goes here
    endtask
endclass
```