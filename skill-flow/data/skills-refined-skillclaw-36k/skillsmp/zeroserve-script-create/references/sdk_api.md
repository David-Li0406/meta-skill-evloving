# Zeroserve SDK API (summary)

## Entry point and macros
- Include the SDK: `#include <zeroserve.h>`.
- Mark the entry function with `ZS_ENTRY` (section `zeroserve.request`).
- `ZS_STR("literal")` expands to `(ptr, len)` for NUL-terminated literals.

## Request inspection
- `zs_req_method(out, out_len)`
- `zs_req_path(out, out_len)`
- `zs_req_uri(out, out_len)`
- `zs_req_query(out, out_len)`
- `zs_req_scheme(out, out_len)`
- `zs_req_peer(out, out_len)`
- `zs_req_header(name, name_len, out, out_len)`
- `zs_req_query_param(name, name_len, out, out_len)`
- `zs_req_body_json()` parses the request body as JSON and returns a handle (-1 on failure,
  empty body, body > 256KB, or invalid JSON). The body is read lazily on first call and cached.

## Request mutation
- `zs_req_set_uri(uri, uri_len)`
- `zs_req_set_header(name, name_len, value, value_len)`
  - Pass `value_len = 0` to remove a header.

## Metadata (per-request string map)
- `zs_meta_get(key, key_len, out, out_len)`
- `zs_meta_set(key, key_len, value, value_len)`
  - Keys prefixed with `zs.response.header.` become response headers.

## Response / proxy
- `zs_respond(status, body, body_len)`
- `zs_reverse_proxy(backend_url, backend_url_len)`

## Logging, time, and environment
- `zs_log(msg, len)`
- `zs_now_ms()`
- `zs_env_get(name, name_len, out, out_len)` reads an environment variable.

## Crypto and encoding
- `zs_getrandom(out, out_len)`
- `zs_sha256(data, data_len, out, out_len)` writes a 32-byte SHA-256 digest (requires `out_len == 32`).
- `zs_hmac_sha256(key, key_len, msg, msg_len, out)`
- `zs_base64_encode(data, data_len, out, out_len, encoding)`
- `zs_base64_decode_in_place(buf, buf_len, encoding)`

## JSON parsing (handle table)
- `zs_json_parse(data, data_len)` parses JSON and returns a handle (-1 on failure).
- `zs_load_static_json(path, path_len)` reads the static file at `path` in the tarball and
  parses JSON, returning a handle (-1 if missing or invalid JSON). The path is used verbatim
  (no normalization, index fallback, or `.html` try).
- `zs_load_file_metadata(path, path_len)` returns a JSON handle for a tarball entry with
  `{"size":...,"etag":...,"mtime":...}` (-1 if missing). The path is used verbatim.
- `zs_json_reset(handle)` resets a handle back to the document root.
- `zs_json_get(handle, key, key_len)` reads an object key and returns a handle
  (-1 if missing, non-object, or invalid UTF-8 key).
- `zs_json_array_get(handle, array_index)` takes an array index and returns a handle
  (-1 if missing, non-array).
- `zs_json_read_string(handle, out, out_len)` writes a JSON string into `out`
  (use `out_len = 0` to query required length; -1 if not a string).
- `zs_json_read_i64(handle, out, out_len)` writes a native-endian `i64` into `out`
  (requires `out_len == sizeof(i64)`; -1 if not a number or out of range).
- `zs_json_read_bool(handle, out, out_len)` writes `0` or `1` into `out`
  (requires `out_len == 1`; -1 if not a boolean).
- `zs_object_free(handle)` releases a JSON handle when you're done with it.
- The handle table is limited (32 entries); free handles to avoid exhaustion.

## JSON creation and modification
- `zs_json_new_object()` creates an empty JSON object `{}`; returns a handle (-1 on failure).
- `zs_json_new_array()` creates an empty JSON array `[]`; returns a handle (-1 on failure).
- `zs_json_clone(handle)` deep-clones a JSON value into a new independent tree; returns a handle.
- `zs_json_len(handle)` returns the length of an array, object, or string (-1 for other types).
- `zs_json_type(handle)` returns the type code: `ZS_JSON_NULL` (0), `ZS_JSON_BOOL` (1),
  `ZS_JSON_NUMBER` (2), `ZS_JSON_STRING` (3), `ZS_JSON_ARRAY` (4), `ZS_JSON_OBJECT` (5).
- `zs_json_set(handle, key, key_len, value_handle)` sets a field on an object; the value is
  cloned from `value_handle`. Returns 0 on success, -1 if not an object.
- `zs_json_remove(handle, key, key_len)` removes a field from an object. Returns 0 on success,
  -1 if not an object or key not found.
- `zs_json_array_push(handle, value_handle)` appends a cloned value to an array; returns new
  length on success, -1 if not an array.
- `zs_json_array_set(handle, index, value_handle)` sets an element at an array index; returns
  0 on success, -1 if out of bounds or not an array.
- `zs_json_set_string(handle, value, value_len)` replaces the node with a string value.
- `zs_json_set_i64(handle, value)` replaces the node with an i64 value.
- `zs_json_set_bool(handle, value)` replaces the node with a boolean (0 = false, non-zero = true).
- `zs_json_set_null(handle)` replaces the node with null.

## JSON response
- `zs_json_respond(status, handle)` serializes the JSON handle to a response body, sets
  `Content-Type: application/json`, and sends the response. Returns 0 on success.

## Helper notes
- String helpers write C strings into the output buffer.
- Passing `out_len = 0` returns the required length.
- Binary helpers return the number of bytes written and do not NUL-terminate.
- `zs_sha256` requires `out_len` to be exactly 32 bytes.
- `zs_hmac_sha256` writes 32 bytes to the output buffer.
- `zs_base64_encode` requires the output buffer to fit the encoded length.
- Base64 `encoding` values: `ZS_BASE64_STANDARD`, `ZS_BASE64_STANDARD_NO_PAD`,
  `ZS_BASE64_URL`, `ZS_BASE64_URL_NO_PAD`.
- Header names are matched case-insensitively.
- The SDK also provides small string/memory helpers like `zs_strlen`, `zs_strcmp`,
  `zs_memcpy`, `zs_memset`, and `zs_utoa10`.
- `zs_req_body_json` reads the body lazily (only when called) and caches the result.
  Subsequent calls return the cached handle. The body is limited to 256KB.
