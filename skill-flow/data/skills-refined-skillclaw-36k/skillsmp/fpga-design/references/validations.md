# Fpga Design - Validations

## Case Statement Without Default

### **Id**
missing-default-case
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - case\s*\([^)]+\)[^}]*endcase(?!.*default)
  - case\s*\([^)]+\)(?![\s\S]{0,500}default)
### **Message**
Case statement without default may infer latch.
### **Fix Action**
Add 'default:' clause with explicit assignment
### **Applies To**
  - **/*.v
  - **/*.sv

## Blocking Assignment in Sequential Logic

### **Id**
blocking-in-sequential
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - always\s*@\s*\(\s*posedge[^)]+\)[^;]*\b\w+\s*=\s*(?!.*<=)
### **Message**
Use non-blocking (<=) for sequential logic to avoid race conditions.
### **Fix Action**
Replace = with <= in always @(posedge clk) blocks
### **Applies To**
  - **/*.v
  - **/*.sv

## Direct Clock Domain Crossing

### **Id**
direct-cdc-connection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - always\s*@\s*\(\s*posedge\s+clk_b[^}]*\b(\w+_a)\b(?!.*sync)
### **Message**
Signal appears to cross clock domains without synchronizer.
### **Fix Action**
Add 2-FF synchronizer or async FIFO for CDC
### **Applies To**
  - **/*.v
  - **/*.sv

## Initial Block in Synthesizable Code

### **Id**
initial-block
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^\s*initial\s+begin(?![\s\S]*\.tb\.)
### **Message**
Initial blocks don't synthesize. Use reset instead.
### **Fix Action**
Replace with synchronous reset: always @(posedge clk) if (!rst_n)
### **Applies To**
  - **/*.v
  - **/*.sv

## Incomplete Sensitivity List

### **Id**
incomplete-sensitivity
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - always\s*@\s*\([^*][^)]*\)\s*begin[^}]*\b(\w+)\b(?![^}]*@.*\1)
### **Message**
Consider using @(*) for combinational logic to auto-include all signals.
### **Fix Action**
Replace explicit sensitivity list with always @(*)
### **Applies To**
  - **/*.v

## Synchronizer Without ASYNC_REG Attribute

### **Id**
missing-async-reg
### **Severity**
info
### **Type**
regex
### **Pattern**
  - reg\s+\[\d+:0\]\s+\w*sync\w*(?!.*ASYNC_REG)
### **Message**
Synchronizer registers should have ASYNC_REG attribute for proper placement.
### **Fix Action**
Add (* ASYNC_REG = "TRUE" *) before register declaration
### **Applies To**
  - **/*.v
  - **/*.sv

## Asynchronous Reset Without Synchronizer

### **Id**
async-reset-no-sync
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - negedge\s+rst_n(?!.*sync)
### **Message**
Asynchronous reset should be synchronized for clean release.
### **Fix Action**
Use reset synchronizer: async assert, sync release pattern
### **Applies To**
  - **/*.v
  - **/*.sv

## Signal Driving Many Modules

### **Id**
high-fanout-signal
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \.(\w+)\(enable\)[^;]*\.(\w+)\(enable\)[^;]*\.(\w+)\(enable\)
### **Message**
High fanout signal may cause timing issues.
### **Fix Action**
Consider registering signal at each destination or using synthesis directives
### **Applies To**
  - **/*.v
  - **/*.sv

## Missing Clock Definition

### **Id**
missing-clock-constraint
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - get_ports.*clk(?!.*create_clock)
### **Message**
Clock port should have create_clock constraint.
### **Fix Action**
Add: create_clock -period <ns> [get_ports clk]
### **Applies To**
  - **/*.xdc
  - **/*.sdc

## IO Without Delay Constraint

### **Id**
unconstrained-io
### **Severity**
info
### **Type**
regex
### **Pattern**
  - get_ports.*data(?!.*set_input_delay|set_output_delay)
### **Message**
Data ports should have input/output delay constraints.
### **Fix Action**
Add set_input_delay/set_output_delay for all data ports
### **Applies To**
  - **/*.xdc
  - **/*.sdc

## Non-Blocking in Combinational Logic

### **Id**
non-blocking-combinational
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - always\s*@\s*\(\s*\*\s*\)[^}]*<=
### **Message**
Use blocking (=) for combinational logic.
### **Fix Action**
Replace <= with = in always @(*) blocks
### **Applies To**
  - **/*.v
  - **/*.sv