# Cairo Inlining Reference

Source: https://www.starknet.io/cairo-book/ch12-06-inlining-in-cairo.html

## Inline attributes
- `#[inline]` suggests inlining.
- `#[inline(always)]` strongly suggests inlining.
- `#[inline(never)]` suggests no inlining.
- All are hints; the compiler may ignore them.

## Tradeoffs
- Inlining reduces call overhead and steps.
- It can increase code size and compile time.
- Best for small, frequently used functions.

## Compiler behavior
- Uses heuristics (function weight/statement count) when no attribute is set.
- Avoids inlining complex control flow or panic-heavy functions.
