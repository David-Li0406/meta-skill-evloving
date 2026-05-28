---
name: cairo-structs
description: Explain how to define and instantiate Cairo structs, field access, mutability, field init shorthand, and update syntax; use when a request involves struct definitions or field-related compile errors in Cairo.
---

# Cairo Structs

## Overview
Guide struct definitions, instantiation patterns, and safe field updates.

## Quick Use
- Read `references/structs.md` before answering.
- Use clear examples showing `struct` definition and `Type { field: value }` initialization.
- Highlight ownership effects of struct update syntax.

## Response Checklist
- Note that the whole instance must be `mut` to change any field.
- Use field init shorthand when variable names match field names.
- If using update syntax, mention that it moves fields from the source instance.

## Example Requests
- "How do I define a struct with multiple fields in Cairo?"
- "Why can't I mutate just one struct field without `mut`?"
- "How does struct update syntax affect ownership?"

## Cairo by Example
- [Custom Types](https://cairo-by-example.xyz/custom_types)
- [Structures](https://cairo-by-example.xyz/custom_types/structs)
- [Struct visibility](https://cairo-by-example.xyz/mod/struct_visibility)
