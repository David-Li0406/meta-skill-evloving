# Example patterns

## Log request method and path
- Read with `zs_req_method` and `zs_req_path` into fixed buffers.
- Clamp lengths before logging with `zs_log`.

## Reverse proxy for a path prefix
- Read path and compare prefix, then call `zs_reverse_proxy("http://127.0.0.1:9000", ...)`.
- After calling, return 0; later scripts will be skipped automatically.

## Health endpoint response
- Match a path like `/health`.
- Build a small JSON body and respond with `zs_respond(200, body, len)`.
- Set content type via `zs_meta_set(ZS_STR("zs.response.header.content-type"),
  ZS_STR("application/json"))`.

## Parse JSON from a header
- Read a header or query param into a buffer, then parse with `zs_json_parse`.
- Traverse with `zs_json_get`, `zs_json_array_get` and `zs_json_read_*` and check for `-1` handles.
- Free every handle with `zs_object_free` to avoid hitting the handle limit.

## Parse JSON from request body
- Call `zs_req_body_json()` to parse the request body as JSON and get a handle.
- Check for `-1` which indicates empty body, body > 256KB, or invalid JSON.
- Traverse with `zs_json_get`, `zs_json_array_get` and read values with `zs_json_read_*`.
- The body is read lazily on first call and cached for subsequent calls.
- Free the handle with `zs_object_free` when done.

Example:
```c
zs_s64 body = zs_req_body_json();
if (body < 0) {
  zs_respond(400, ZS_STR("Invalid JSON body"));
  return 0;
}

zs_s64 name = zs_json_get(body, ZS_STR("name"));
if (name < 0) {
  zs_object_free(body);
  zs_respond(400, ZS_STR("Missing name field"));
  return 0;
}

char name_buf[256];
zs_s64 len = zs_json_read_string(name, name_buf, sizeof(name_buf));
zs_object_free(body);

// Use name_buf...
```

## JWT verification and payload extraction
- Read the `authorization` header, require a `Bearer ` prefix, then split the token
  on `.` to get header, payload, and signature segments.
- Compute `zs_hmac_sha256` over the `header.payload` bytes and Base64URL encode it
  with `zs_base64_encode(..., ZS_BASE64_URL_NO_PAD)` to compare with the signature.
- Base64URL decode the payload in place with `zs_base64_decode_in_place`.

## Template metadata
- Use `zs_meta_set` to populate keys used by `<zs-meta>key</zs-meta>` placeholders
  in HTML/XML static responses.
- Metadata is shared across scripts in the request chain.

## Build and respond with JSON
- Create a JSON object with `zs_json_new_object()`.
- Add fields using `zs_json_set(obj, key, key_len, value_handle)` where `value_handle`
  can be created via `zs_json_parse`, `zs_json_new_object`, `zs_json_new_array`, or
  modified in place with `zs_json_set_string`, `zs_json_set_i64`, etc.
- Build arrays with `zs_json_new_array()` and `zs_json_array_push(arr, value_handle)`.
- Send the response with `zs_json_respond(200, obj)` which auto-sets Content-Type.
- Free handles with `zs_object_free` when done.

Example:
```c
zs_s64 resp = zs_json_new_object();
zs_s64 status = zs_json_parse(ZS_STR("\"ok\""));
zs_json_set(resp, ZS_STR("status"), status);
zs_object_free(status);

zs_s64 count = zs_json_parse(ZS_STR("0"));
zs_json_set_i64(count, 42);
zs_json_set(resp, ZS_STR("count"), count);
zs_object_free(count);

zs_json_respond(200, resp);
zs_object_free(resp);
```

## Modify existing JSON
- Load JSON with `zs_json_parse` or `zs_load_static_json`.
- Navigate to a node with `zs_json_get` or `zs_json_array_get`.
- Modify in place: `zs_json_set_string`, `zs_json_set_i64`, `zs_json_set_bool`, `zs_json_set_null`.
- Add/remove object fields with `zs_json_set` and `zs_json_remove`.
- Check type with `zs_json_type` and length with `zs_json_len`.
- Clone a subtree with `zs_json_clone` to create an independent copy.
