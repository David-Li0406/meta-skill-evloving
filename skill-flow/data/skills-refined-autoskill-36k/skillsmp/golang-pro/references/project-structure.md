# Go Project Structure

## Standard Layout

```
project/
├── cmd/              # Main applications
│   ├── server/
│   └── cli/
├── internal/         # Private application code
│   ├── api/
│   ├── domain/
│   └── repository/
├── pkg/              # Public library code
├── api/              # OpenAPI specs, protobufs
├── configs/          # Configuration files
├── deployments/      # Docker, K8s configs
└── docs/             # Documentation
```

## Module Management

```go
// go.mod
module github.com/user/project

go 1.21

require (
    github.com/lib/pq v1.10.0
)
```

**Commands:**
- `go mod tidy` - Sync dependencies
- `go mod download` - Fetch packages
- `go get pkg@version` - Add/update package

## Internal Package Protection

`internal/` directories enforce encapsulation - only importable within parent tree.

## Workspaces (Go 1.18+)

```go
// go.work
go 1.21

use (
    ./service-a
    ./service-b
    ./shared
)
```
