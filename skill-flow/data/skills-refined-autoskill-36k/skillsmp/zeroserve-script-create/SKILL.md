---
name: zeroserve-script-create
description: Create Zeroserve eBPF request-processing scripts in C for `.zeroserve/scripts` using the Zeroserve SDK (`zeroserve.h`). Use when you need to implement request inspection, header/query parsing, metadata templating, custom responses, or reverse-proxy behavior in a script.
---

# Zeroserve Script Create

## Overview

Zeroserve is a high-performance, scriptable HTTP server that uses `io_uring` and eBPF. It
serves a static website from a tarball, and optionally runs eBPF request scripts.
It supports HTTP, HTTPS, hot reload, a small templating pass for text responses, and
an opt-in reverse proxy from scripts.

This skill creates a Zeroserve request script in C from requirements, using the SDK helpers
and eBPF constraints. Output is a single `.c` file ready to place under `.zeroserve/scripts/`.
It includes JSON helper usage for parsing structured inputs from headers or params.

## Basic zeroserve usage

Serve a prebuilt tarball:

```bash
zeroserve --addr 0.0.0.0:8080 site.tar
```

Package a directory into a tarball and serve it:

```bash
# Create a tarball from the current directory
zeroserve --pack . > site.tar

# Serve it
zeroserve --addr 0.0.0.0:8080 site.tar
```

Packaging a site: Zeroserve expects a tarball whose root corresponds to the site root.
Use `--pack` to build one from a directory:

```bash
zeroserve --pack ./public > site.tar
```

Packaging notes:
- All regular files under the directory are added to the tarball.
- Request scripts live under `.zeroserve/scripts/`.
- Any `.c` file in `.zeroserve/scripts/` is compiled to an `.o` eBPF object.
  The resulting `.o` is included in the tarball and the `.c` is omitted.
- If a `.c` and `.o` share the same name, the `.o` is skipped in favor of recompiling.
- Script compilation requires `clang` and `llc` on your `PATH`.

If you want the SDK header without packing:

```bash
zeroserve --dump-sdk > zeroserve.h
```

## Workflow

1. Gather requirements
   - Trigger: path, method, header, query param, peer, or scheme.
   - Action: log, mutate URI/headers, set metadata, respond, or reverse proxy.
   - Short-circuit: confirm if the script should terminate the chain with `zs_respond` or `zs_reverse_proxy`.
2. Choose a base
   - Start from `assets/script_template.c` for a new script.
   - Keep the entry signature and `ZS_ENTRY` section if editing an existing script.
3. Implement logic
   - Read request data with `zs_req_*` helpers into fixed buffers; clamp lengths before use.
   - Use `ZS_STR("literal")` for helper calls needing `(ptr, len)` for string literals.
   - For JSON parsing, use `zs_json_parse`/`zs_json_get`/`zs_json_array_get` and
     `zs_json_read_*`, then free handles with `zs_object_free` (handle table is limited).
   - To parse the request body as JSON, use `zs_req_body_json()` which returns a handle
     (-1 on empty body, body > 256KB, or invalid JSON). The body is read lazily and cached.
   - To build JSON dynamically, use `zs_json_new_object`/`zs_json_new_array` and modify
     with `zs_json_set`, `zs_json_array_push`, `zs_json_set_string`, `zs_json_set_i64`, etc.
   - To send a JSON response, use `zs_json_respond(status, handle)` which auto-sets Content-Type.
   - To parse a static JSON file from the tarball, call `zs_load_static_json(path, path_len)`
     and treat the returned handle like any other JSON handle.
   - To read tarball entry metadata as JSON, call `zs_load_file_metadata(path, path_len)`
     and access `size`, `etag`, and `mtime`.
   - For response headers, set metadata keys `zs.response.header.<name>`.
   - Call `zs_respond`, `zs_json_respond`, or `zs_reverse_proxy` to stop later scripts.
4. Validate eBPF constraints
   - Avoid unbounded loops and recursion.
   - Keep stack usage small (BPF stack is limited).
5. Deliver result
   - Provide the `.c` file and note it should live under `.zeroserve/scripts/`.
   - Remind that `zeroserve --pack` compiles `.c` to `.o` automatically.
   - If needed, dump the SDK header with `zeroserve --dump-sdk` to inspect the full API.

## References

- `references/sdk_api.md` for the SDK helper list and notes.
- `references/scripting_behavior.md` for execution order, short-circuit rules, and packaging.
- `references/examples.md` for common patterns (logging, health response, reverse proxy, templating).
- `assets/script_template.c` for a starter skeleton.
