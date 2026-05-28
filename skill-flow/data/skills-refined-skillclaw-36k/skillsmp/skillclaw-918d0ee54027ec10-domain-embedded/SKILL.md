---
name: domain-embedded
description: Use this skill when developing embedded or no_std Rust applications for microcontrollers, ensuring compliance with hardware constraints and real-time requirements.
---

# Embedded Domain

> **Layer 3: Domain Constraints**

## Domain Constraints → Design Implications

| Domain Rule      | Design Constraint      | Rust Implication          |
|------------------|-----------------------|---------------------------|
| No heap          | Stack allocation       | heapless, no Box/Vec      |
| No std           | Core only             | #![no_std]                |
| Real-time        | Predictable timing     | No dynamic allocation      |
| Resource limited  | Minimal memory        | Static buffers             |
| Hardware safety   | Safe peripheral access | HAL + ownership            |
| Interrupt safe    | No blocking in ISR    | Atomic, critical sections  |

---

## Critical Constraints

### No Dynamic Allocation

```
RULE: Cannot use heap (no allocator)
WHY: Deterministic memory, no OOM
RUST: heapless::Vec<T, N>, arrays
```

### Interrupt Safety

```
RULE: Shared state must be interrupt-safe
WHY: ISR can preempt at any time
RUST: Mutex<RefCell<T>> + critical section
```

### Hardware Ownership

```
RULE: Peripherals must have clear ownership
WHY: Prevent conflicting access
RUST: HAL takes ownership, singletons
```

---

## Trace Down ↓

From constraints to design (Layer 2):

```
"Need no_std compatible data structures"
    ↓ m02-resource: heapless collections
    ↓ Static sizing: heapless::Vec<T, N>

"Need interrupt-safe state"
    ↓ m03-mutability: Mutex<RefCell<Option<T>>>
    ↓ m07-concurrency: Critical sections

"Need peripheral ownership"
    ↓ m01-ownership: Singleton pattern
    ↓ m12-lifecycle: RAII for hardware
```

---

## Layer Stack

| Layer    | Examples        | Purpose               |
|----------|-----------------|-----------------------|
| PAC      | stm32f4, esp32c3| Register access       |
| HAL      | stm32f4xx-hal   | Hardware abstraction   |
| Framework| RTIC, Embassy   | Concurrency           |
| Traits   | embedded-hal    | Portable drivers      |

## Framework Comparison

| Framework | Style          | Best For                     |
|-----------|----------------|------------------------------|
| RTIC      | Priority-based  | Interrupt-driven apps        |
| Embassy   | Async          | Complex state machines       |
| Bare metal| Manual         | Simple apps                  |

## Key Crates

| Purpose                | Crate                  |
|-----------------------|-----------------------|
| Runtime (ARM)         | cortex-m-rt           |
| Panic handler          | panic-halt, panic-probe|
| Collections            | heapless              |
| HAL traits            | embedded-hal          |
| Logging               | defmt                 |
| Flash/debug           | pro                   |