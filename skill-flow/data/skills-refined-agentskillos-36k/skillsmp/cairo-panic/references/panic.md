# Cairo Panic Reference

Source: https://book.cairo-lang.org/ch09-01-unrecoverable-errors-with-panic.html

## Basics
- Panics terminate execution and unwind by dropping variables and squashing dictionaries.
- Panics can be triggered implicitly (e.g., out-of-bounds array access) or explicitly.

## Panic APIs
- `panic(data_array)` accepts an array payload.
- `panic_with_felt252(code)` is a concise one-liner for a single felt error.
- `panic!("message")` accepts a string and supports messages longer than 31 bytes.

## `nopanic`
- `nopanic` marks functions that must not panic.
- Only `nopanic` functions can be called within a `nopanic` function.

## `#[panic_with]`
- `#[panic_with('reason', wrapper_name)]` generates a wrapper that panics on `None` or `Err`.
