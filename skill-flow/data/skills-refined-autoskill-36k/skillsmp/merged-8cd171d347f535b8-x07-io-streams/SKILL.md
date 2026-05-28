---
name: x07-io-streams
description: Use this skill when implementing canonical streaming I/O patterns in X07 with std.io and std.io.bufread.
---

# x07-io-streams

Prefer streaming parsing and zero-copy views over full-buffer copies.

## Canonical patterns

- Prefer `bytes_view` + `view.*` builtins for scan/trim/split without copying.
- Use `std.io` / `std.io.bufread` for streaming reads:
  - `io.read`
  - `bufread.fill` + `bufread.consume`
- Utilize world adapters that return reader `iface`s:
  - `std.fs.open_read`
  - `std.rr.send`
  - `std.kv.get_stream`

For the built-in reference guide, use `x07 guide` and search for `std.io` / `std.io.bufread`.