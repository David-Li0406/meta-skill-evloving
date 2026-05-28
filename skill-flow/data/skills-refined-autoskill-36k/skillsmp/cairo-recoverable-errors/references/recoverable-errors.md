# Cairo Recoverable Errors Reference

Source: https://book.cairo-lang.org/ch09-02-recoverable-errors.html

## Result type
- `Result<T, E>` has variants `Ok(T)` and `Err(E)`.
- Use `match` to handle success and error cases explicitly.

## ResultTrait methods
- `unwrap` / `expect` return the `Ok` value or panic.
- `unwrap_err` / `expect_err` return the `Err` value or panic.
- `is_ok` / `is_err` check the variant.

## Error propagation
- The `?` operator returns early with `Err` or unwraps `Ok`.
- Use `?` to keep fallible flows concise.
