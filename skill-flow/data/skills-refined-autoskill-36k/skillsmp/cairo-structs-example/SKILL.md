---
name: cairo-structs-example
description: Explain the Cairo example program that refactors rectangle area calculations into a struct, including `Into`/`TryInto` conversions; use when a request references the Chapter 5.2 struct example or asks for struct-based refactors.
---

# Cairo Structs Example

## Overview
Guide refactoring patterns from separate variables to tuples to structs, and show conversions between related structs.

## Quick Use
- Read `references/structs-example.md` before answering.
- Use the Rectangle example to illustrate why structs improve clarity.
- Include conversion trait usage (`Into`, `TryInto`) when discussing type transformations.

## Response Checklist
- Show how struct fields make code self-documenting.
- If converting types, mention that `.into()` needs a target type context.
- For fallible conversions, show `TryInto` returning `Option` or `Result`.

## Example Requests
- "Can you refactor these width/height variables into a struct?"
- "How do I convert between two struct types in Cairo?"

## Cairo by Example
- [Structures](https://cairo-by-example.xyz/custom_types/structs)
- [From and Into](https://cairo-by-example.xyz/conversion/into)
- [TryFrom and TryInto](https://cairo-by-example.xyz/conversion/try_into)
