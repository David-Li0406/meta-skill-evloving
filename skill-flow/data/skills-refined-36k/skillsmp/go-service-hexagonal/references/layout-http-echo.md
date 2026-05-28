# HTTP REST/JSON Service Layout (Echo)

Use this when you want Echo (`github.com/labstack/echo/v4`) as the HTTP server/router.

## Directory tree (relative to base layout)

```text
cmd/
  <service>-api/
    main.go                 # Starts echo, graceful shutdown
internal/
  interface/http/
    server.go               # Echo routes + DTO mapping; depends on internal/interface
  interface/debughttp/      # Optional: pprof/trace handler mux (served on separate debug server)
  bootstrap/
    http.go                 # NewEcho(): wires ports and adapters
api/openapi/
  <service>.yaml            # Optional but recommended
```

## Hexagonal boundaries (Echo-specific reminders)

- Keep Echo handlers thin: parse/validate request, call `internal/interface`, map response.
- Do not let Echo types leak into `app`/`domain`/`internal/interface` or `internal/adapter`.
- Put middleware under `internal/interface/http/middleware` if it grows.
- Expose `GET /health/live` and `GET /health/ready` for liveness/readiness.
- Add profiling endpoints only when needed (opt-in) and serve them from a separate debug server (set `PPROF_PORT`, optional `PPROF_ADDR`).

## Scaffolding

Use the scaffolder with:

`python3 scripts/scaffold_hex_service.py --root <repo> --service <name> --kinds http` (Echo is the default; module defaults to folder name for new projects)

Add settings loading (env + optional config via Koanf) with `--settings config`.

If `go.mod` is created (new project), the scaffolder runs `go mod tidy` to fetch dependencies (Echo + Logrus). Use `--skip-deps` to skip.

Optional debug endpoints:

- Add pprof: append `--http-pprof`
- Add trace: append `--http-trace`
- Enable the debug server: set `PPROF_PORT` (and optional `PPROF_ADDR`, default `127.0.0.1`)
