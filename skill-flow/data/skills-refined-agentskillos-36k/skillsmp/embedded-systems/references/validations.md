# Embedded Systems - Validations

## Shared Variable Without Volatile

### **Id**
missing-volatile
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(bool|uint\d+_t|int\d+_t)\s+\w+\s*=.*//.*ISR|interrupt|IRQ
  - static\s+(bool|uint\d+_t|int\d+_t)\s+(?!volatile)\w+.*flag
### **Message**
Variable shared with ISR should be declared volatile.
### **Fix Action**
Add 'volatile' qualifier to variables accessed from interrupts
### **Applies To**
  - **/*.c
  - **/*.cpp
  - **/*.h

## Printf or Malloc in Interrupt Handler

### **Id**
printf-in-interrupt
### **Severity**
error
### **Type**
regex
### **Pattern**
  - void\s+\w+_IRQHandler.*\{[^}]*printf
  - void\s+\w+_IRQHandler.*\{[^}]*malloc
  - void\s+\w+_IRQHandler.*\{[^}]*free\(
  - void\s+\w+_IRQHandler.*\{[^}]*sprintf
### **Message**
Never use printf, sprintf, malloc, or free in interrupt handlers - they are not reentrant.
### **Fix Action**
Use buffer and process in main loop, or use SEGGER RTT for debug output
### **Applies To**
  - **/*.c
  - **/*.cpp

## Blocking Delay in Interrupt Handler

### **Id**
delay-in-interrupt
### **Severity**
error
### **Type**
regex
### **Pattern**
  - void\s+\w+_IRQHandler.*\{[^}]*delay
  - void\s+\w+_IRQHandler.*\{[^}]*(HAL_Delay|vTaskDelay)
  - void\s+\w+_IRQHandler.*\{[^}]*while\s*\([^)]+\)\s*;
### **Message**
Avoid blocking delays in ISRs. They block all lower-priority interrupts.
### **Fix Action**
Set flag in ISR, handle timing in main loop or use hardware timer
### **Applies To**
  - **/*.c
  - **/*.cpp

## Large Stack-Allocated Array

### **Id**
large-stack-array
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \w+\s+\w+\[\s*(512|1024|2048|4096|[5-9]\d{3}|\d{5,})\s*\]\s*[;=]
  - uint8_t\s+\w+\[\s*([2-9]\d{2}|\d{4,})\s*\]
### **Message**
Large arrays on stack may cause overflow. Embedded stacks are typically 1-4KB.
### **Fix Action**
Use 'static' keyword to place in .bss section, or allocate from heap with bounds checking
### **Applies To**
  - **/*.c
  - **/*.cpp

## Multi-Word Access Without Critical Section

### **Id**
unprotected-critical-section
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - volatile\s+(uint64_t|int64_t|double)\s+\w+(?![^;]*__disable_irq)
  - volatile\s+struct\s+\{[^}]+\}\s+\w+
### **Message**
Multi-word volatile variables need critical section protection for atomic access.
### **Fix Action**
Wrap reads/writes in __disable_irq()/__enable_irq() or use mutex
### **Applies To**
  - **/*.c
  - **/*.cpp
  - **/*.h

## Peripheral Access Pattern Without Clock Enable

### **Id**
no-clock-enable
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (USART|SPI|I2C|TIM|ADC|DAC)\d*->\w+\s*=[^;]+(?<!(RCC|CLK))
### **Message**
Ensure peripheral clock is enabled before accessing registers.
### **Fix Action**
Add RCC clock enable call before peripheral initialization
### **Applies To**
  - **/*.c
  - **/*.cpp

## Magic Number in Register Configuration

### **Id**
magic-register-value
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ->\w+\s*=\s*0x[0-9A-Fa-f]{3,}\s*;
  - ->\w+\s*\|=\s*0x[0-9A-Fa-f]{2,}\s*;
### **Message**
Use named constants or bitfield macros instead of magic numbers in register configuration.
### **Fix Action**
Replace with manufacturer-provided defines (e.g., USART_CR1_TE instead of 0x08)
### **Applies To**
  - **/*.c
  - **/*.cpp

## Recursive Function in Embedded Code

### **Id**
recursive-function
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (\w+)\s*\([^)]*\)\s*\{[^}]*\1\s*\(
### **Message**
Recursion can cause stack overflow in embedded systems with limited stack.
### **Fix Action**
Convert to iterative implementation using explicit stack or state machine
### **Applies To**
  - **/*.c
  - **/*.cpp

## Potentially Unaligned Pointer Cast

### **Id**
pointer-cast-alignment
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \(uint32_t\s*\*\)\s*\w+(?!.*aligned)
  - \(uint16_t\s*\*\)\s*\(\s*&?\s*\w+\[\d+\]\s*\)
### **Message**
Casting to wider type pointer may cause alignment fault on ARM.
### **Fix Action**
Use memcpy() for safe unaligned access, or ensure buffer alignment with __attribute__((aligned(4)))
### **Applies To**
  - **/*.c
  - **/*.cpp

## Long Function Without Watchdog Feed

### **Id**
no-watchdog-feed
### **Severity**
info
### **Type**
regex
### **Pattern**
  - for\s*\([^;]+;[^;]+<\s*(100|[2-9]\d{2}|\d{4,})[^)]+\)[^}]{500,}(?!watchdog|wdt|iwdg)
### **Message**
Long loop may exceed watchdog timeout. Consider feeding watchdog periodically.
### **Fix Action**
Add watchdog_feed() call inside long-running loops
### **Applies To**
  - **/*.c
  - **/*.cpp

## Floating Point in Interrupt Handler

### **Id**
float-in-isr
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - void\s+\w+_IRQHandler.*\{[^}]*(float|double)\s+\w+
  - void\s+\w+_IRQHandler.*\{[^}]*\d+\.\d+
### **Message**
Floating point in ISR requires FPU context save/restore. Consider fixed-point math.
### **Fix Action**
Use fixed-point arithmetic or ensure FPU lazy stacking is configured
### **Applies To**
  - **/*.c
  - **/*.cpp

## Assert Without Proper Handler

### **Id**
assert-in-production
### **Severity**
info
### **Type**
regex
### **Pattern**
  - assert\s*\([^)]+\)(?!.*NDEBUG)
### **Message**
Standard assert() may not be suitable for embedded. Use custom assert with safe failure mode.
### **Fix Action**
Implement custom assert that logs error and enters safe state, or define NDEBUG for production
### **Applies To**
  - **/*.c
  - **/*.cpp