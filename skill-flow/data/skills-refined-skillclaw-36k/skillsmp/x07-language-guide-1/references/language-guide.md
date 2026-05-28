# Language Guide (x07AST JSON)

IMPORTANT:
- Output ONLY one JSON object (no preamble).
- Do NOT wrap the JSON in Markdown code fences.
- Do NOT output extra prose.
- Must satisfy x07AST schema_version `x07.x07ast@0.1.0`.

Program encoding: UTF-8 JSON text.

Entry program object fields:
- `schema_version`: `x07.x07ast@0.1.0`
- `kind`: `entry`
- `module_id`: `main`
- `imports`: array of module IDs (e.g. `std.bytes`)
- `decls`: array of decl objects
- `solve`: expression (must evaluate to bytes)

## Expression Encoding (json-sexpr)

- i32: JSON numbers in range -2147483648..2147483647
- atom: JSON strings with no whitespace
- list: JSON arrays: `["head", arg1, arg2, ...]` (head is an atom string; list must be non-empty)

## Types

- `i32` for integers and conditions (0=false, non-zero=true)
- `bytes` for owned byte arrays (move-only; outputs and owned buffers)
- `bytes_view` for borrowed byte views (zero-copy scanning/slicing)
- `vec_u8` for mutable byte vectors (move-only; capacity-planned builders)
- `option_i32`, `option_bytes` for typed optional values
- `result_i32`, `result_bytes` for typed results with deterministic error codes
- `iface` for interface records (used for streaming readers)
- Raw pointer types (standalone-only; require unsafe capability): `ptr_const_u8`, `ptr_mut_u8`, `ptr_const_void`, `ptr_mut_void`, `ptr_const_i32`, `ptr_mut_i32`

Move rules (critical):
- Passing `bytes` / `vec_u8` to a function that expects `bytes` / `vec_u8` **moves** (consumes) the value.
- `result_i32` / `result_bytes` values are also move-only; consume them once (use `*_err_code`, `*_unwrap_or`, or `try`).
- Mutating APIs return the updated value; always bind it with `let`/`set` (example: `["set","b",["bytes.set_u8","b",0,65]]`).

## Builtins

- `input` is the input byte view (bytes_view); refer to it as the atom string `input` in expressions.
- `iface.make_v1(data: i32, vtable: i32) -> iface` constructs an interface record value.

## Core Forms

- `begin`: `["begin", e1, e2, ...]` evaluates sequentially and returns the last expression
- `unsafe`: `["unsafe", e1, e2, ...]` evaluates sequentially and returns the last expression; inside it, unsafe-only operations are allowed (standalone-only)
- `let`: `["let", name, expr]` binds `name` in the current scope
- `set`: `["set", name, expr]` assigns an existing binding
- `if`: `["if", cond, then, else]` branches on non-zero `cond`
- `for`: `["for", i, start, end, body]` declares `i` (i32) and runs it from `start` to `end-1`
  - `body` is a single expression; use `begin` for multiple steps.
- `return`: `["return", expr]` returns early from the current function
  - In `solve`, the return value must be `bytes`.

## Examples

Echo (returns input):
```json
{"schema_version":"x07.x07ast@0.1.0","kind":"entry","module_id":"main","imports":[],"decls":[],"solve":["view.to_bytes","input"]}
```

Arity reminder:
- `if` is `["if", cond, then, else]`
- `for` is `["for", i, start, end, body]`
- `begin` is `["begin", e1, e2, ...]`

## Modules

Top-level fields:

- `imports`: array of module IDs
- `decls`: array of declarations (objects)
- `solve`: expression (entry programs only)

Declaration objects:

- `{"kind":"defn","name":"main.f","params":[{"name":"x","ty":"bytes"}],"result":"bytes","body":<expr>}`
- `{"kind":"defasync",...}` (returns awaited type; calling returns a task handle i32)
- `{"kind":"extern","abi":"C","name":"main.c_fn","link_name":"c_fn","params":[{"name":"x","ty":"i32"}],"result":"i32"}` (standalone-only; `result` may also be `"void"`)
- `{"kind":"export","names":["std.foo.bar", ...]}` (module files only)

Module IDs are dot-separated identifiers like `app.rle` or `std.bytes`.

Module resolution is deterministic:

- Built-in modules: `std.vec`, `std.slice`, `std.bytes`, `std.codec`, `std.parse`, `std.fmt`, `std.prng`, `std.bit`, `std.text.ascii`, `std.text.utf8`, `std.test`, `std.regex-lite`, `std.json`, `std.csv`, `std.map`, `std.set`, `std.u32`, `std.small_map`, `std.small_set`, `std.hash`, `std.hash_map`, `std.hash_set`, `std.btree_map`, `std.btree_set`, `std.deque_u32`, `std.heap_u32`, `std.bitset`, `std.slab`, `std.lru_cache`, `std.result`, `std.option`, `std.io`, `std.io.bufread`, `std.fs`, `std.world.fs`, `std.rr`, `std.kv`, `std.path`
- Filesystem modules (standalone): `x07c compile --module-root <dir>` resolves `a.b` to `<dir>/a/b.x07.json`

Standalone binding override:

- In standalone-only worlds (`run-os`, `run-os-sandboxed`), `std.world.*` modules are resolved from `--module-root` only (no built-in fallback).
- This keeps program source stable (`import std.fs`) while the target world selects the adapter implementation.

Standalone OS builtins:

- These heads are only available when compiling with `--world run-os` or `--world run-os-sandboxed`:
  - `os.fs.read_file(path: bytes) -> bytes`
  - `os.fs.write_file(path: bytes, data: bytes) -> i32`
  - `os.fs.read_all_v1(path: bytes, caps: bytes) -> result_bytes`
  - `os.fs.write_all_v1(path: bytes, data: bytes, caps: bytes) -> result_i32`
  - `os.fs.mkdirs_v1(path: bytes, caps: bytes) -> result_i32`
  - `os.fs.remove_file_v1(path: bytes, caps: bytes) -> result_i32`
  - `os.fs.remove_dir_all_v1(path: bytes, caps: bytes) -> result_i32`
  - `os.fs.rename_v1(src: bytes, dst: bytes, caps: bytes) -> result_i32`
  - `os.fs.list_dir_sorted_text_v1(path: bytes, caps: bytes) -> result_bytes`
  - `os.fs.walk_glob_sorted_text_v1(root: bytes, glob: bytes, caps: bytes) -> result_bytes`
  - `os.fs.stat_v1(path: bytes, caps: bytes) -> result_bytes`
  - `os.env.get(key: bytes) -> bytes`
  - `os.time.now_unix_ms() -> i32`
  - `os.time.now_instant_v1() -> bytes`
  - `os.time.sleep_ms_v1(ms: i32) -> i32`
  - `os.time.local_tzid_v1() -> bytes`
  - `os.process.exit(code: i32) -> never`
  - `os.process.spawn_capture_v1(req: bytes, caps: bytes) -> i32`
  - `os.process.spawn_piped_v1(req: bytes, caps: bytes) -> i32`
  - `os.process.try_join_capture_v1(handle: i32) -> option_bytes`
  - `os.process.join_capture_v1(handle: i32) -> bytes` (yield boundary)
  - `os.process.stdout_read_v1(handle: i32, max: i32) -> bytes`
  - `os.process.stderr_read_v1(handle: i32, max: i32) -> bytes`
  - `os.process.stdin_write_v1(handle: i32, chunk: bytes) -> i32`
  - `os.process.stdin_close_v1(handle: i32) -> i32`
  - `os.process.try_wait_v1(handle: i32) -> i32`
  - `os.process.join_exit_v1(handle: i32) -> i32` (yield boundary)
  - `os.process.take_exit_v1(handle: i32) -> i32`
  - `os.process.kill_v1(handle: i32, sig: i32) -> i32`
  - `os.process.drop_v1(handle: i32) -> i32`
  - `os.process.run_capture_v1(req: bytes, caps: bytes) -> bytes`
    - Note: `req`/`caps` are `bytes` (move-only). To reuse, copy via `std.bytes.copy(req)` / `std.bytes.copy(caps)`.
  - `os.net.http_request(req: bytes) -> bytes` (currently traps; reserved for later)

Standalone unsafe + FFI:

- Only available in `run-os` / `run-os-sandboxed`.
- Unsafe block: `["unsafe", ...]`.
- Pointer creation/casts: `bytes.as_ptr`, `bytes.as_mut_ptr`, `view.as_ptr`, `vec_u8.as_ptr`, `vec_u8.as_mut_ptr`, `ptr.null`, `ptr.as_const`, `ptr.cast`, `addr_of`, `addr_of_mut`.
- Unsafe-only ops (require `unsafe` block): `ptr.add`, `ptr.sub`, `ptr.offset`, `ptr.read_u8`, `ptr.write_u8`, `ptr.read_i32`, `ptr.write_i32`, `memcpy`, `memmove`, `memset`.
- `extern` function calls require `unsafe` blocks.

## Functions

- Define with a `decls[]` entry of kind `defn`.
  - `body` is a single expression; wrap multi-step bodies in `begin`.
  - `ty` and `ret_ty` are `i32`, `bytes`, `bytes_view`, `vec_u8`, `option_i32`, `option_bytes`, `result_i32`, `result_bytes`, `iface`, `ptr_const_u8`, `ptr_mut_u8`, `ptr_const_void`, `ptr_mut_void`, `ptr_const_i32`, or `ptr_mut_i32`.
  - Function names must be namespaced and start with the current module ID.
    - In the entry file, use module `main` (example: `main.helper`).
  - `input` (bytes_view) is available in all function bodies.
- Call: `["name", arg1, arg2, ...]`

## Concurrency

Async functions are defined with `defasync`.
Calling an async function returns an opaque `i32` task handle.
To get concurrency, create multiple tasks before waiting on them (and avoid blocking operations outside tasks).

- Define with a `decls[]` entry of kind `defasync`.
  - `body` is a single expression; wrap multi-step bodies in `begin`.
  - `bytes` is the awaited return type (currently only `bytes` is supported).
- Call: `["name", arg1, arg2, ...]` -> `i32` (task handle)
- `["await", task_handle]` -> `bytes` (alias of `task.join.bytes`)
- `["task.spawn", task_handle]` -> `i32`
- `["task.is_finished", task_handle]` -> `i32` (0/1)
- `["task.try_join.bytes", task_handle]` -> `result_bytes` (err=1 not finished; err=2 canceled)
- `["task.join.bytes", task_handle]` -> `bytes`
- `["task.yield"]` -> `i32`
- `["task.sleep", ticks_i32]` -> `i32` (virtual time ticks)
- `["task.cancel", task_handle]` -> `i32`

Channels (bytes payloads):

- `["chan.bytes.new", cap_i32]` -> `i32`
- `["chan.bytes.try_send", chan_handle, bytes_view]` -> `i32` (0 full; 1 sent; 2 closed)
- `["chan.bytes.send", chan_handle, bytes]` -> `i32`
- `["chan.bytes.try_recv", chan_handle]` -> `result_bytes` (err=1 empty; err=2 closed)
- `["chan.bytes.recv", chan_handle]` -> `bytes`
- `["chan.bytes.close", chan_handle]` -> `i32`

## Built-in Modules (stdlib)

Call module functions using fully-qualified names (e.g. `["std.bytes.reverse","b"]`).

- `std.bytes`
  - `["std.bytes.len","b"]` -> i32
  - `["std.bytes.get_u8","b","i"]` -> i32 (0..255)
  - `["std.bytes.set_u8","b","i","v"]` -> bytes (returns `b`)
  - `["std.bytes.alloc","n"]` -> bytes (length `n`)
  - `["std.bytes.eq","a","b"]` -> i32 (1 if equal else 0)
  - `["std.bytes.find_u8","b","target"]` -> i32 (index, or -1)
  - `["std.bytes.cmp_range","a","a_off","a_len","b","b_off","b_len"]` -> i32 (-1/0/1)
  - `["std.bytes.max_u8","v"]` -> i32 (`v` is bytes_view; returns 0 if empty)
  - `["std.bytes.sum_u8","v"]` -> i32 (`v` is bytes_view; wraps mod 2^32)
  - `["std.bytes.count_u8","v","target"]` -> i32 (`v` is bytes_view)
  - `["std.bytes.starts_with","a","prefix"]` -> i32 (both bytes_view)
  - `["std.bytes.ends_with","a","suffix"]` -> i32 (both bytes_view)
  - `["std.bytes.reverse","b"]` -> bytes
  - `["std.bytes.concat","a","b"]` -> bytes
  - `["std.bytes.take","b","n"]` -> bytes
  - `["std.bytes.drop","b","n"]` -> bytes
  - `["std.bytes.copy","b"]` -> bytes
  - `["std.bytes.slice","b","start","len"]` -> bytes (copy; clamps within bounds)
- `std.codec`
  - `["std.codec.read_u32_le","b","off"]` -> i32 (`b` is bytes_view)
  - `["std.codec.write_u32_le","x"]` -> bytes
- `std.vec`
  - `["std.vec.with_capacity","cap"]` -> vec_u8
  - `["std.vec.len","v"]` -> i32
  - `["std.vec.get","v","i"]` -> i32 (0..255)
  - `["std.vec.push","v","x"]` -> vec_u8
  - `["std.vec.reserve_exact","v","additional"]` -> vec_u8
  - `["std.vec.extend_bytes","v","b"]` -> vec_u8
  - `["std.vec.as_bytes","v"]` -> bytes
- `std.slice`
  - `["std.slice.clamp","b","start","len"]` -> bytes
  - `["std.slice.cmp_bytes","a","b"]` -> i32 (-1/0/1)
- `std.parse`
  - `["std.parse.u32_dec","b"]` -> i32
  - `["std.parse.u32_dec_at","b","off"]` -> i32
  - `["std.parse.i32_status_le","b"]` -> bytes (tag byte 1 + i32_le, or tag byte 0)
  - `["std.parse.i32_status_le_at","b","off"]` -> bytes (tag byte 1 + i32_le + next_off_u32_le, or tag byte 0)
- `std.fmt`
  - `["std.fmt.u32_to_dec","x"]` -> bytes
  - `["std.fmt.s32_to_dec","x"]` -> bytes
- `std.prng`
  - `["std.prng.lcg_next_u32","state"]` -> i32
  - `["std.prng.x07rand32_v1_stream","b"]` -> bytes
- `std.bit`
  - `["std.bit.popcount_u32","x"]` -> i32
- `std.text.ascii`
  - `["std.text.ascii.normalize_lines","b"]` -> bytes
  - `["std.text.ascii.tokenize_words_lower","b"]` -> bytes
  - `["std.text.ascii.split_u8","b","sep_u8"]` -> bytes (X7SL v1 slice list)
  - `["std.text.ascii.split_lines_view","b"]` -> bytes (X7SL v1 slice list; splits on `\n`, strips trailing `\r`, omits trailing empty line after final `\n`)
- `std.text.slices`
  - `["std.text.slices.builder_new_v1","cap_hint"]` -> vec_u8
  - `["std.text.slices.builder_push_v1","out","start","len"]` -> vec_u8
  - `["std.text.slices.builder_finish_v1","out","count"]` -> bytes (X7SL v1)
  - `["std.text.slices.validate_v1","x7sl"]` -> result_i32 (OK(count) or ERR(code); see `docs/text/x7sl-v1.md`)
  - `["std.text.slices.count_v1","x7sl"]` -> i32 (count or -1)
  - `["std.text.slices.start_v1","x7sl","idx"]` -> i32
  - `["std.text.slices.len_v1","x7sl","idx"]` -> i32
  - `["std.text.slices.view_at_v1","base_view","x7sl","idx"]` -> bytes_view
  - `["std.text.slices.copy_at_v1","base_view","x7sl","idx"]` -> bytes
- `std.text.utf8`
  - `["std.text.utf8.validate_or_empty","b"]` -> bytes
- `std.regex-lite`
  - `["std.regex-lite.find_literal","hay","needle"]` -> i32 (index, or -1)
  - `["std.regex-lite.is_match_literal","hay","needle"]` -> i32 (0/1)
  - `["std.regex-lite.count_matches_u32le","b"]` -> bytes
- `std.json`
  - `["std.json.canonicalize_small","json_bytes"]` -> bytes (or `ERR`)
  - `["std.json.extract_path_canon_or_err","b"]` -> bytes
- `std.csv`
  - `["std.csv.sum_second_col_i32_status_le","csv_bytes"]` -> bytes (tag byte 1 + i32_le, or tag byte 0)
  - `["std.csv.sum_second_col_i32le_or_err","csv_bytes"]` -> bytes (i32_le, or `ERR`)
- `std.map`
  - `["std.map.word_freq_sorted_ascii","b"]` -> bytes
- `std.set`
  - `["std.set.unique_lines_sorted","b"]` -> bytes
- `std.u32`
  - `["std.u32.read_le_at","b","off"]` -> i32
  - `["std.u32.write_le_at","b","off","x"]` -> bytes
  - `["std.u32.push_le","v","x"]` -> vec_u8
  - `["std.u32.pow2_ceil","x"]` -> i32
- `std.small_map`
  - `["std.small_map.empty_bytes_u32"]` -> bytes
  - `["std.small_map.len_bytes_u32","m"]` -> i32
  - `["std.small_map.get_bytes_u32","m","key"]` -> i32 (0 if missing)
  - `["std.small_map.put_bytes_u32","m","key","val"]` -> bytes
  - `["std.small_map.remove_bytes_u32","m","key"]` -> bytes
- `std.small_set`
  - `["std.small_set.empty_bytes"]` -> bytes
  - `["std.small_set.len_bytes","s"]` -> i32
  - `["std.small_set.contains_bytes","s","key"]` -> i32
  - `["std.small_set.insert_bytes","s","key"]` -> bytes
- `std.hash`
  - `["std.hash.fnv1a32_bytes","b"]` -> i32
  - `["std.hash.fnv1a32_range","b","start","len"]` -> i32
  - `["std.hash.fnv1a32_view","v"]` -> i32
  - `["std.hash.mix32","x"]` -> i32
- `std.hash_map` (u32 keys/values)
  - `["std.hash_map.with_capacity_u32","expected_len"]` -> i32
  - `["std.hash_map.len_u32","m"]` -> i32
  - `["std.hash_map.contains_u32","m","key"]` -> i32
  - `["std.hash_map.get_u32_or","m","key","default"]` -> i32
  - `["std.hash_map.set_u32","m","key","val"]` -> i32
- `std.hash_set`
  - u32 set: `["std.hash_set.new_u32","cap_pow2"]` -> i32, `["std.hash_set.add_u32","s","key"]` -> i32
  - view-key set: `["std.hash_set.view_new","expected_len"]` -> vec_u8, `["std.hash_set.view_insert","set","base","start","len"]` -> vec_u8
- `std.btree_map` (ordered u32->u32)
  - `["std.btree_map.empty_u32_u32"]` -> bytes
  - `["std.btree_map.len_u32_u32","m"]` -> i32
  - `["std.btree_map.get_u32_u32_or","m","key","default"]` -> i32
  - `["std.btree_map.put_u32_u32","m","key","val"]` -> bytes
- `std.btree_set` (ordered u32)
  - `["std.btree_set.empty_u32"]` -> bytes
  - `["std.btree_set.len_u32","s"]` -> i32
  - `["std.btree_set.contains_u32","s","key"]` -> i32
  - `["std.btree_set.insert_u32","s","key"]` -> bytes
- `std.deque_u32`
  - `["std.deque_u32.with_capacity","cap"]` -> bytes
  - `["std.deque_u32.len","dq"]` -> i32
  - `["std.deque_u32.push_back","dq","x"]` -> bytes
  - `["std.deque_u32.front_or","dq","default"]` -> i32
  - `["std.deque_u32.pop_front","dq"]` -> bytes
  - `["std.deque_u32.emit_u32le","dq"]` -> bytes
- `std.heap_u32`
  - `["std.heap_u32.with_capacity","cap"]` -> bytes
  - `["std.heap_u32.len","h"]` -> i32
  - `["std.heap_u32.push","h","x"]` -> bytes
  - `["std.heap_u32.min_or","h","default"]` -> i32
  - `["std.heap_u32.pop_min","h"]` -> bytes
  - `["std.heap_u32.emit_u32le","h"]` -> bytes
- `std.bitset`
  - `["std.bitset.new","bit_len"]` -> bytes
  - `["std.bitset.set","bs","bit"]` -> bytes
  - `["std.bitset.test","bs","bit"]` -> i32
  - `["std.bitset.intersection_count","a","b"]` -> i32
- `std.slab` (u32 values)
  - `["std.slab.new_u32","cap"]` -> bytes
  - `["std.slab.free_head_u32","slab"]` -> i32 (-1 if none)
  - `["std.slab.alloc_u32","slab"]` -> bytes
  - `["std.slab.free_u32","slab","handle"]` -> bytes
  - `["std.slab.get_u32","slab","handle","default"]` -> i32
  - `["std.slab.set_u32","slab","handle","val"]` -> bytes
- `std.lru_cache` (u32 keys/values)
  - `["std.lru_cache.new_u32","cap"]` -> bytes
  - `["std.lru_cache.len_u32","cache"]` -> i32
  - `["std.lru_cache.peek_u32_opt","cache","key"]` -> option_i32
  - `["std.lru_cache.peek_u32_or","cache","key","default"]` -> i32
  - `["std.lru_cache.touch_u32","cache","key"]` -> bytes
  - `["std.lru_cache.put_u32","cache","key","val"]` -> bytes
- `std.test`
  - `["std.test.pass"]` -> result_i32
  - `["std.test.fail","code"]` -> result_i32
  - `["std.test.assert_true","cond","code"]` -> result_i32
  - `["std.test.assert_i32_eq","a","b","code"]` -> result_i32
  - `["std.test.assert_bytes_eq","a","b","code"]` -> result_i32
  - `["std.test.code_assert_true"]` -> i32
  - `["std.test.code_assert_i32_eq"]` -> i32
  - `["std.test.code_assert_bytes_eq"]` -> i32
  - `["std.test.status_from_result_i32","r"]` -> bytes (5-byte X7TEST_STATUS_V1)
- `std.result`
  - `["std.result.ok_i32_le","x"]` -> bytes
  - `["std.result.err0"]` -> bytes
  - `["std.result.chain_sum_csv_i32","b"]` -> bytes
- `std.option`
  - `["std.option.some_i32_le","x"]` -> bytes
  - `["std.option.none"]` -> bytes
- `std.io`
  - `["std.io.read","reader","max"]` -> bytes (`reader` is `iface`)
- `std.io.bufread`
  - `["std.io.bufread.new","reader","cap"]` -> i32 (`reader` is `iface`)
  - `["std.io.bufread.fill","br"]` -> bytes_view
  - `["std.io.bufread.consume","br","n"]` -> i32
- `std.fs` (world-bound via `std.world.fs`)
  - `["std.fs.read","path_bytes"]` -> bytes
  - `["std.fs.read_async","path_bytes"]` -> bytes
  - `["std.fs.open_read","path_bytes"]` -> iface
  - `["std.fs.list_dir","path_bytes"]` -> bytes
  - `["std.fs.list_dir_sorted","path_bytes"]` -> bytes

- `std.world.fs` (adapter module; world-selected)
  - `["std.world.fs.read_file","path_bytes"]` -> bytes
  - `["std.world.fs.read_file_async","path_bytes"]` -> bytes

- `std.rr` (solve-rr only)
  - `["std.rr.send_request","req_bytes"]` -> bytes
  - `["std.rr.fetch","key_bytes"]` -> bytes
  - `["std.rr.send","key_bytes"]` -> iface

- `std.kv` (solve-kv only)
  - `["std.kv.get","key_bytes"]` -> bytes
  - `["std.kv.get_async","key_bytes"]` -> bytes
  - `["std.kv.set","key_bytes","val_bytes"]` -> i32
  - `["std.kv.get_stream","key_bytes"]` -> iface

- `std.path`
  - `["std.path.join","a","b"]` -> bytes
  - `["std.path.basename","p"]` -> bytes
  - `["std.path.extname","p"]` -> bytes

## Operators (i32)

- `["+","a","b"]` `["-","a","b"]` `["*","a","b"]` `["/","a","b"]` `["%","a","b"]`
- `["=","a","b"]` `["!=","a","b"]`
- Signed comparisons (two’s complement): `["<","a","b"]` `["<=","a","b"]` `[">","a","b"]` `[">=","a","b"]`
- Unsigned comparisons: `["<u","a","b"]` `[">=u","a","b"]`
- Shifts: `["<<u","a","b"]` `[">>u","a","b"]` (shift amount masked by 31)
- Bitwise: `["&","a","b"]` `["|","a","b"]` `["^","a","b"]`

## Integer Semantics

- Integers are 32-bit and arithmetic wraps modulo 2^32.
- Beware underflow/overflow: `["-",0,1]` becomes `-1` (wrap-around).
- `/` and `%` are unsigned u32 ops: `/` by 0 yields 0, and `%` by 0 yields the numerator.
- `["<u","x",0]` is always false and `[">=u","x",0]` is always true.
- For negative checks, use signed comparisons like `["<","x",0]`.
- For "can’t go below zero" counters, guard before decrementing.

## Bytes Ops

Use `std.bytes.*` functions (import `std.bytes`):

- `["std.bytes.len","b"]` -> i32
- `["std.bytes.get_u8","b","i"]` -> i32 (0..255)
- `["std.bytes.set_u8","b","i","v"]` -> bytes (returns `b`)
- `["std.bytes.alloc","n"]` -> bytes (length `n`)

Additional bytes ops:

- `["std.bytes.eq","a","b"]` -> i32 (1 if equal else 0)
- `["std.bytes.find_u8","b","target"]` -> i32 (index, or -1)
- `["std.bytes.cmp_range","a","a_off","a_len","b","b_off","b_len"]` -> i32 (-1/0/1)

- `["std.bytes.max_u8","v"]` -> i32 (`v` is bytes_view; returns 0 if empty)
- `["std.bytes.sum_u8","v"]` -> i32 (`v` is bytes_view; wraps mod 2^32)
- `["std.bytes.count_u8","v","target"]` -> i32 (`v` is bytes_view)
- `["std.bytes.starts_with","a","prefix"]` -> i32 (both bytes_view)
- `["std.bytes.ends_with","a","suffix"]` -> i32 (both bytes_view)

For copy/slice/concat/reverse/take/drop helpers, use `std.bytes.*` module functions (see Modules).

Bytes literals:

- `["bytes.lit","token"]` -> bytes (UTF-8 of the atom string; no whitespace)
  - Example: `["bytes.lit","config.bin"]` produces `b"config.bin"`.
  - The token characters are literal (underscores stay underscores); there are no escape sequences.
  - For whitespace/newlines/arbitrary bytes, build a `vec_u8` and convert with `std.vec.as_bytes`.

## Views

Views are explicit, borrowed slices used for scan/trim/split without copying.

- `["bytes.view","b"]` -> bytes_view
- `["bytes.subview","b","start","len"]` -> bytes_view
- `["view.len","v"]` -> i32
- `["view.get_u8","v","i"]` -> i32
- `["view.slice","v","start","len"]` -> bytes_view
- `["view.to_bytes","v"]` -> bytes (copy)
- `["view.eq","a","b"]` -> i32 (1 if equal else 0)
- `["view.cmp_range","a","a_off","a_len","b","b_off","b_len"]` -> i32 (-1/0/1)

Note: `bytes.view`, `bytes.subview`, and `vec_u8.as_view` require an identifier owner (they cannot borrow from a temporary expression).

## Filesystem (solve-fs only)

- `["fs.read","path_bytes"]` -> bytes
- `["fs.read_async","path_bytes"]` -> bytes
- `["fs.open_read","path_bytes"]` -> iface
  - Returns an `iface` reader for streaming reads.
- `["fs.list_dir","path_bytes"]` -> bytes (newline-separated names, sorted, trailing `\n`)
  - `path_bytes` must be a safe relative path (no absolute paths, no `..`, no empty segments).
  - The fixture directory is the current working directory (`.`).

## Request/Response (solve-rr only)

- `["rr.send_request","req_bytes"]` -> bytes
  - Fixture-backed request/response (no real network).
  - `req_bytes` are hashed as `sha256(req_bytes)` and mapped to a response blob under `./.x07_rr/`.
- `["rr.fetch","key_bytes"]` -> bytes
  - Fixture-backed request/response with deterministic latency modeling.
- `["rr.send","key_bytes"]` -> iface
  - Returns an `iface` reader for streaming reads.

## Key/Value (solve-kv only)

- `["kv.get","key_bytes"]` -> bytes
  - Returns empty bytes if missing.
- `["kv.get_async","key_bytes"]` -> bytes
  - Same as `kv.get` but explicitly uses the async/latency-aware path.
- `["kv.get_stream","key_bytes"]` -> iface
  - Returns an `iface` reader for streaming reads.
- `["kv.set","key_bytes","val_bytes"]` -> i32
  - Returns 1 if inserted, 0 if updated.
  - Store is seeded per case from `./.x07_kv/seed.evkv` and reset per case.

## Streaming I/O

Readers are `iface` values returned by world adapters.

- `["io.open_read_bytes","b"]` -> iface (`b` is bytes/bytes_view/vec_u8)
- `["io.read","reader_iface","max_i32"]` -> bytes
- `["bufread.new","reader_iface","cap_i32"]` -> i32
- `["bufread.fill","br"]` -> bytes_view
- `["bufread.consume","br","n_i32"]` -> i32

## Vectors

`vec_u8` is a mutable byte vector value used for building outputs efficiently.

Use `std.vec.*` to create and manipulate `vec_u8` values:

- `["std.vec.with_capacity","cap"]` -> vec_u8
- `["std.vec.push","v","x"]` -> vec_u8
- `["std.vec.reserve_exact","v","additional"]` -> vec_u8
- `["std.vec.extend_bytes","v","b"]` -> vec_u8
- `["std.vec.as_bytes","v"]` -> bytes

Additional vec_u8 builtins:

- `["vec_u8.extend_bytes_range","v","b","start","len"]` -> vec_u8 (append subrange of `b`)
- `["vec_u8.as_view","v"]` -> bytes_view (borrowed view of current vec contents)

## Option / Result

Typed options:

- `["option_i32.none"]` -> option_i32
- `["option_i32.some","x"]` -> option_i32
- `["option_i32.is_some","o"]` -> i32
- `["option_i32.unwrap_or","o","default"]` -> i32

- `["option_bytes.none"]` -> option_bytes
- `["option_bytes.some","b"]` -> option_bytes
- `["option_bytes.is_some","o"]` -> i32
- `["option_bytes.unwrap_or","o","default"]` -> bytes

Typed results:

- `["result_i32.ok","x"]` -> result_i32
- `["result_i32.err","code"]` -> result_i32
- `["result_i32.is_ok","r"]` -> i32
- `["result_i32.err_code","r"]` -> i32
- `["result_i32.unwrap_or","r","default"]` -> i32

- `["result_bytes.ok","b"]` -> result_bytes
- `["result_bytes.err","code"]` -> result_bytes
- `["result_bytes.is_ok","r"]` -> i32
- `["result_bytes.err_code","r"]` -> i32
- `["result_bytes.unwrap_or","r","default"]` -> bytes

Propagation sugar:

- `["try","r"]` -> `i32` or `bytes` (requires the current `defn` return type is `result_i32` or `result_bytes`)

## Memory / Performance Tips

- Deterministic suite gates may enforce `mem_stats`: reduce `realloc_calls`, `memcpy_bytes`, and `peak_live_bytes`.
- Prefer building output with `std.vec` instead of repeated concatenation in a loop.
- If you can estimate the final size, start with `["std.vec.with_capacity","n"]` to avoid reallocations.
- When appending many bytes, prefer `["std.vec.extend_bytes","v","chunk"]` over per-byte `["std.vec.push",...]`.
- Convert once at the end: `["std.vec.as_bytes","v"]` returns bytes without copying.
- Use `bytes_view` + `view.*` builtins for scanning/slicing without copying.

- For streaming parsing, use `["bufread.fill","br"]` to get a `bytes_view` window, scan it, then `["bufread.consume","br","n"]`.

## Maps / Sets

Open-addressing hash tables with fixed capacity.
- capacity must be a non-zero power of two
- key `-1` is reserved and will trap

- `["map_u32.new","cap_pow2"]` -> i32
- `["map_u32.len","m"]` -> i32
- `["map_u32.contains","m","key"]` -> i32 (0/1)
- `["map_u32.get","m","key","default"]` -> i32
- `["map_u32.set","m","key","value"]` -> i32 (1 if inserted, 0 if updated)
- `["map_u32.remove","m","key"]` -> i32 (1 if removed, 0 if missing)
- `["set_u32.new","cap_pow2"]` -> i32
- `["set_u32.contains","s","key"]` -> i32 (0/1)
- `["set_u32.add","s","key"]` -> i32 (1 if inserted, 0 if already present)
- `["set_u32.remove","s","key"]` -> i32 (1 if removed, 0 if missing)

## Collection emitters

Use `emit_*` stdlib functions to produce canonical deterministic encodings:

- `std.hash_set.emit_u32le(set_u32_handle)` -> bytes (sorted ascending u32le)
- `std.hash_map.emit_kv_u32le_u32le(map_u32_handle)` -> bytes ((k u32le)(v u32le)... sorted by key)
- `std.btree_set.emit_u32le(btree_set_bytes)` -> bytes (already sorted)
- `std.btree_map.emit_kv_u32le_u32le(btree_map_bytes)` -> bytes (already sorted)
- `std.deque_u32.emit_u32le(dq_bytes)` -> bytes (front-to-back)
- `std.heap_u32.emit_u32le(heap_bytes)` -> bytes (non-decreasing pop-min order; consumes heap_bytes)

## Stdlib (pure)

Prefer calling stdlib helpers through their module namespaces (and include the module in `imports`):

- `std.codec`: `["std.codec.read_u32_le","b","off"]` (`b` is bytes_view), `["std.codec.write_u32_le","x"]`
- `std.parse`: `["std.parse.u32_dec","b"]`, `["std.parse.u32_dec_at","b","off"]`, `["std.parse.i32_status_le","b"]`
- `std.fmt`: `["std.fmt.u32_to_dec","x"]`, `["std.fmt.s32_to_dec","x"]`
- `std.prng`: `["std.prng.lcg_next_u32","state"]`

- `std.bit`: `["std.bit.popcount_u32","x"]`

## Common Templates

- 1-byte output: `["begin",["let","out",["bytes.alloc",1]],["set","out",["bytes.set_u8","out",0,"x"]],"out"]`
- Empty output: `["bytes.alloc",0]`
- Looping: use `bytes.len` once, then `["for","i",0,"n",body]`.

### Header + tail pattern

Many tasks use `input[0..k]` as parameters and the remaining bytes as data.

Example (k=1):

- `["begin",["let","x",["std.bytes.get_u8","input",0]],["let","n",["std.bytes.len","input"]],["let","v",["std.vec.with_capacity",["-","n",1]]],["for","i",1,"n",["std.vec.push","v",["std.bytes.get_u8","input","i"]]],["std.vec.as_bytes","v"]]`


