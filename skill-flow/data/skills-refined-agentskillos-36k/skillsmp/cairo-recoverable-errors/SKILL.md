---
name: cairo-recoverable-errors
description: Explain Cairo recoverable errors using `Result`, `ResultTrait`, and the `?` operator; use when a request involves returning, matching, or unwrapping `Result` values in Cairo.
---

# Cairo Recoverable Errors

## Overview
Show how to model recoverable failures with `Result<T, E>` and handle them safely.

## Quick Use
- Read `references/recoverable-errors.md` before answering.
- Prefer `match` or `?` over `unwrap` in non-test code.
- Mention `expect` when a custom panic message is desired.

## Response Checklist
- Return `Result<T, E>` from fallible functions.
- Use `Ok(...)` and `Err(...)` explicitly.
- Apply `?` to propagate errors from called functions.

## Example Requests
- "How do I use `Result` in Cairo?"
- "What is the difference between `unwrap` and `expect`?"
- "How does the `?` operator work?"

## Cairo by Example
- [Option & unwrap](https://cairo-by-example.xyz/error/option_unwrap)
- [Unpacking options with ?](https://cairo-by-example.xyz/error/option_unwrap/question_mark)
- [Combinators: map](https://cairo-by-example.xyz/error/option_unwrap/map)
- [Combinators: and_then](https://cairo-by-example.xyz/error/option_unwrap/and_then)
- [Result](https://cairo-by-example.xyz/error/result)
- [Introducing ?](https://cairo-by-example.xyz/error/result/enter_question_mark)
- [Multiple error types](https://cairo-by-example.xyz/error/multiple_error_types)
- [Core Result](https://cairo-by-example.xyz/core/result)
