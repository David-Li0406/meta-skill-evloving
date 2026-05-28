# Debug server protocol (`agent-skills debug`)

This repo ships a local log capture server:

```bash
agent-skills debug
```

By default it:
- Listens on `127.0.0.1:7070`
- Requires an auth token (auto-generated at startup)
- Serves a tiny UI at `/` (SSE stream)
- Appends NDJSON to `.agent-skills/debug.ndjson` (disable with `--out=`)

## Endpoints

- `POST /v1/logs` — ingest an event
- `GET /v1/events` — snapshot of recent events (JSON array)
- `GET /v1/events/stream` — Server-Sent Events stream

## Auth

Either:
- `Authorization: Bearer <token>`
- `?token=<token>` (useful for the UI / SSE; less safe than headers)

Auth can be disabled with `agent-skills debug --no-auth`.

## Ingest examples

### JSON event (recommended)

```bash
curl -sS -X POST http://127.0.0.1:7070/v1/logs \
  -H 'Authorization: Bearer TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"level":"info","message":"hello","fields":{"requestId":"abc","userId":123}}'
```

### Plaintext

```bash
echo "hello" | curl -sS -X POST http://127.0.0.1:7070/v1/logs \
  -H 'Authorization: Bearer TOKEN' \
  --data-binary @-
```

### From the CLI

```bash
agent-skills debug send --token TOKEN --message "hello" --field requestId=abc --field userId=123
```

### Pipe any command’s stdout/stderr

Not built-in (yet). If you need this, add a small wrapper that reads stdin line-by-line and POSTs JSON events to `/v1/logs`, or add a first-class CLI command (suggested: `agent-skills debug pipe`).
