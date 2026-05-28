# Cairo Printing Reference

Source: https://www.starknet.io/cairo-book/ch12-08-printing.html

## Basics
- `println!` prints with newline; `print!` prints inline.
- Format placeholders: `{}` or `{var}`.
- Uses `Display` by default; use `{:?}` for `Debug`.

## format!
- `format!` returns a `ByteArray` instead of printing.
- Uses snapshots so input strings are not consumed.

## Custom types
- Implement `Display` to print with `{}`.
- Use `Debug` (derive `#[derive(Debug)]`) for convenient debugging.
- Use `Formatter` with `write!`/`writeln!` for custom formatting.
- `{:x}` prints hexadecimal for types implementing `LowerHex`.
