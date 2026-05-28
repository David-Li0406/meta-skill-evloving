---
name: cairo-enums
description: Explain Cairo enums, defining variants with data, constructing values, and using Option; use when a request involves enum design, variant syntax, or pattern-matching enum values in Cairo.
---

# Cairo Enums

## Overview
Guide enum definitions, variant data, and common Option-based patterns in Cairo.

## Quick Use
- Read `references/enums.md` before answering.
- Show minimal examples with fully qualified variants like `EnumName::Variant`.
- Call out when pattern matching is required to access variant data.

## Response Checklist
- Define the enum with clear variant payload types.
- Construct values using `EnumName::Variant(...)` or `EnumName::Variant` for unit variants.
- Use `match` or `if let` to extract data from variants.

## Example Requests
- "How do I define an enum with data in Cairo?"
- "What is `Option` and how do I use `Some`/`None`?"
- "Why can't I access enum fields directly?"

## Cairo by Example
- [Enums](https://cairo-by-example.xyz/custom_types/enum)
- [use](https://cairo-by-example.xyz/custom_types/enum/enum_use)
- [Testcase: linked-list](https://cairo-by-example.xyz/custom_types/enum/testcase_linked_list)
- [Option](https://cairo-by-example.xyz/core/option)
