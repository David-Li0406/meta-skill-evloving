# Cairo Arithmetic Circuits Reference

Source: https://www.starknet.io/cairo-book/ch12-10-arithmetic-circuits.html

## Overview
- Arithmetic circuits model polynomial computations over a field.
- Cairo supports emulated circuits with modulo up to 384 bits.

## Core constructs
- Module: `core::circuit`.
- Builtins: `AddMod` and `MulMod`.
- Gates: `AddModGate`, `SubModGate`, `MulModGate`, `InvModGate`.

## Building circuits
- Use `CircuitElement<T>` with `CircuitInput<N>` for inputs.
- Combine with `circuit_add`, `circuit_sub`, `circuit_mul`, `circuit_inverse`.
- Outputs are tuples of circuit elements; include all degree-0 gates.

## Evaluating
- Provide inputs via `CircuitInputs` and call `eval` with a `CircuitModulus`.
- Outputs are `u384` values.
