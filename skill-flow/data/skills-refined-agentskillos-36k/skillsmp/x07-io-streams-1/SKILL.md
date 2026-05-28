---
name: x07-io-streams
description: Canonical streaming I/O patterns in X07 using std.io / std.io.bufread and world adapters.
metadata:
  short-description: Streaming I/O patterns
  version: 0.1.0
  kind: docs
---

# x07-io-streams

Prefer streaming parsing and zero-copy views over full-buffer copies.

## Canonical patterns

- Prefer `bytes_view` + `view.*` builtins for scan/trim/split without copying.
- Prefer `std.io` / `std.io.bufread` for streaming reads:
  - `io.read`
  - `bufread.fill` + `bufread.consume`
- Prefer world adapters that return reader `iface`s:
  - `std.fs.open_read`
  - `std.rr.send`
  - `std.kv.get_stream`

For the built-in reference guide, use `x07c guide` and search for `std.io` / `std.io.bufread`.
