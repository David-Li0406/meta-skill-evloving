# Reference index
- Slot types: `:http-api`, `:llm-provider`, `:database`, `:blob-storage`, `:kv-store`, `:secret`
- Auth types: `:api-key`, `:bearer`, `:basic`, `:hmac-sha256`, `:signature`, `:ip-allowlist`, `:none` (note: webhook triggers require auth; `:none` is not allowed)
- Trigger types: `:manual`, `:schedule`, `:event`
- Step types: `:http`, `:llm`, `:db`, `:wait`, `:function`
- Flow helpers: `flow/poll`, `flow/now-ms`, `flow/elapsed?`, `flow/backoff`
- Form field types: `:string`, `:text`, `:number`, `:boolean`, `:select`, `:date`, `:email`, `:textarea`, `:password`, `:secret`
- Installations: subscribe, activation inputs, and upload triggers (see `./installations.md`)
