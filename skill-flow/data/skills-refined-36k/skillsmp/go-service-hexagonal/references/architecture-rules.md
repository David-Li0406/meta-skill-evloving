# Hexagonal Dependency Rules (Go)

Use this as a checklist when reviewing or proposing a directory structure.

## Allowed dependencies (high level)

- `domain` depends on nothing in the service (only standard library or small pure helpers).
- `app` depends on `domain` and outbound ports in `internal/adapter`.
- Inbound ports in `internal/interface` and outbound ports in `internal/adapter` depend on `domain` types as needed.
- Inbound adapters under `internal/interface/*` depend on inbound ports in `internal/interface` and `domain` (DTO mapping).
- Outbound adapters under `internal/adapter/*` depend on outbound ports in `internal/adapter` and `domain` (persistence/message mapping).
- When present, `internal/interface/options` depends on standard library and config libs only (no `app`/`adapter` imports). Prefer Koanf for config files; env overrides config, and TOML is the default when no extension is provided.
- `bootstrap` depends on everything to wire it together.
- `cmd/*` depends on `bootstrap` (and minimal infra like `os`, `signal`, settings loading when present).

## Single composition root

- Centralize DI in `internal/bootstrap.Compose(...)` (one place to construct and inject dependencies).

## Keep interfaces at the boundary

- Define inbound interfaces where adapters need them (`internal/interface`).
- Define outbound interfaces where the app needs them (`internal/adapter`).
- Avoid “interface soup”: keep ports small and focused on a single use case or capability.

## Common structure smells

- `domain` importing `adapter/*` or transport packages.
- `cmd/*` importing `adapter/*` directly (skip bootstrap).
- A `common` or `utils` package that accumulates unrelated helpers.
- Repository packages that return transport DTOs instead of domain/application types.
