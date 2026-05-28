---
name: cairo-data-types
description: Explain Cairo scalar and compound data types, literals, conversions, and string forms; use when a request asks about Cairo types (felt252, integers, bool, strings, tuples, arrays, unit), type annotations, or conversion errors.
---

# Cairo Data Types

## Overview
Explain Cairo's core data types, literals, and conversions so answers stay type-correct and safe.

## Quick Use
- Read `references/data-types.md` before answering.
- State the target type explicitly and show the correct literal or conversion.
- Prefer integer types over `felt252` when safety (overflow/underflow checks) matters.

## Response Checklist
- Identify whether the value should be `felt252`, a specific integer type, `bool`, a string type, or a compound type.
- When literals are ambiguous, use a type suffix or explicit annotation.
- For conversions, show `try_into`/`into` patterns and mention potential failure where relevant.

## Example Requests
- "What is the difference between `felt252` and `u64` in Cairo?"
- "How do I write a short string vs a long string?"
- "Why does this integer literal need a type annotation?"

## Cairo by Example
- [Primitives](https://cairo-by-example.xyz/primitives)
- [Literals and operators](https://cairo-by-example.xyz/primitives/literals)
- [Tuples](https://cairo-by-example.xyz/primitives/tuples)
- [Types](https://cairo-by-example.xyz/types)
- [Type Inference](https://cairo-by-example.xyz/types/inference)
- [Aliasing](https://cairo-by-example.xyz/types/alias)
- [Conversion](https://cairo-by-example.xyz/conversion)
- [From and Into](https://cairo-by-example.xyz/conversion/into)
- [TryFrom and TryInto](https://cairo-by-example.xyz/conversion/try_into)
- [ByteArrays](https://cairo-by-example.xyz/core/bytearrays)
