---
name: cairo-printing
description: Explain Cairo printing and formatting with print!/println!/format!, Display/Debug traits, and Formatter helpers; use when a request involves output formatting or printing custom types in Cairo.
---

# Cairo Printing

## Overview
Guide printing for standard and custom types, including Display and Debug formatting.

## Quick Use
- Read `references/printing.md` before answering.
- Use `println!` for newline output and `format!` for ByteArray formatting.
- Recommend `Debug` for complex types when no Display impl exists.

## Response Checklist
- `println!` and `print!` use Display (`{}`) and Debug (`{:?}`).
- `format!` returns a ByteArray and does not consume inputs.
- For custom types, implement `Display` or derive `Debug`.
- Use `write!`/`writeln!` with `Formatter` for custom formatting.

## Example Requests
- "How do I print a struct in Cairo?"
- "What is the difference between Display and Debug?"
- "How do I format a string without printing?"

## Cairo by Example
- [Hello World](https://cairo-by-example.xyz/hello)
- [Formatted print](https://cairo-by-example.xyz/hello/print)
- [Debug](https://cairo-by-example.xyz/hello/print/print_debug)
- [Display](https://cairo-by-example.xyz/hello/print/print_display)
- [Formatting](https://cairo-by-example.xyz/hello/print/fmt)
