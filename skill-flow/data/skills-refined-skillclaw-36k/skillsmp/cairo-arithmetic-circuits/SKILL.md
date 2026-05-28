---
name: cairo-arithmetic-circuits
description: Explain Cairo arithmetic circuits using core::circuit, gates, CircuitElement, and evaluation; use when a request involves building or evaluating arithmetic circuits in Cairo.
---

# Cairo Arithmetic Circuits

## Overview
Guide building and evaluating arithmetic circuits using Cairo's core circuit module.

## Quick Use
- Read `references/arithmetic-circuits.md` before answering.
- Use a small example like `a * (a + b)` with `circuit_add` and `circuit_mul`.
- Mention the `u384` limb type and modulus selection.

## Response Checklist
- Use `CircuitElement<T>` and `CircuitInput<N>` for inputs.
- Combine gates with `circuit_add`, `circuit_sub`, `circuit_mul`, `circuit_inverse`.
- Build outputs as a tuple of circuit elements.
- Provide witnesses via `CircuitInputs` and evaluate with a `CircuitModulus`.

## Example Requests
- "How do I build a simple arithmetic circuit in Cairo?"
- "What are AddMod/MulMod gates used for?"
- "How do I evaluate a circuit with a modulus?"
