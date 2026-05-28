# Path Finder Cheat Sheet

## Symbols Service - Complete Path Reference

### Core Business Logic

| What | Path |
|------|------|
| Symbol business model | `services/symbols/internal/biz/models.go` |
| Symbol interfaces (UseCase, Repo) | `services/symbols/internal/biz/interfaces.go` |
| Symbol use case implementation | `services/symbols/internal/biz/symbols.go` |
| Symbol use case tests | `services/symbols/internal/biz/symbols_test.go` |
| Business validation | `services/symbols/internal/biz/validator.go` |
| Business errors | `services/symbols/internal/biz/errors.go` |
| Biz Wire providers | `services/symbols/internal/biz/biz.go` |

### Data Access

| What | Path |
|------|------|
| GORM Symbol entity | `services/symbols/internal/data/model/symbol.go` |
| Symbol repository impl | `services/symbols/internal/data/repo/symbol.go` |
| Database setup | `services/symbols/internal/data/data.go` |
| Transaction utilities | `services/symbols/internal/data/common/transaction.go` |

### Service Layer (Handlers)

| What | Path |
|------|------|
| Symbol gRPC/HTTP handlers | `services/symbols/internal/service/symbols.go` |
| DTO ↔ Model mappers | `services/symbols/internal/service/mapper.go` |
| Service struct | `services/symbols/internal/service/service.go` |

### Server & Config

| What | Path |
|------|------|
| gRPC server setup | `services/symbols/internal/server/grpc.go` |
| HTTP server setup | `services/symbols/internal/server/http.go` |
| Server Wire providers | `services/symbols/internal/server/server.go` |
| Config proto schema | `services/symbols/internal/conf/conf.proto` |
| Runtime config YAML | `services/symbols/configs/config.yaml` |

### Entry Point & Build

| What | Path |
|------|------|
| Main entry point | `services/symbols/cmd/symbols/main.go` |
| Wire definitions | `services/symbols/cmd/symbols/wire.go` |
| Generated Wire code | `services/symbols/cmd/symbols/wire_gen.go` |
| Built binary | `services/symbols/bin/symbols` |
| Service Makefile | `services/symbols/Makefile` |
| Go module | `services/symbols/go.mod` |

### API & Contracts

| What | Path |
|------|------|
| Proto definition | `api/symbols/v1/symbols.proto` |
| Generated gRPC | `contracts/symbols/v1/symbols_grpc.pb.go` |
| Generated protobuf | `contracts/symbols/v1/symbols.pb.go` |
| Generated HTTP | `contracts/symbols/v1/symbols_http.pb.go` |
| OpenAPI spec | `contracts/symbols/v1/symbols.swagger.json` |

### Platform Shared Code

| What | Path |
|------|------|
| Request ID middleware | `platform/middleware/requestid/requestid.go` |
| Context helpers | `platform/middleware/requestid/context.go` |
| Pagination utilities | `platform/pagination/pagination.go` |
| Pagination metadata | `platform/pagination/meta.go` |

### Root Level

| What | Path |
|------|------|
| Workspace definition | `go.work` |
| Root Makefile | `Makefile` |
| Buf config | `buf.yaml` |
| Buf generation | `buf.gen.yaml` |
| Docker Compose | `docker-compose.yml` |
| Project instructions | `CLAUDE.md` |

## Path Construction Patterns

### Adding New Entity to Symbols Service

If adding a new entity called `Template`:

```
1. Proto definition:
   api/symbols/v1/symbols.proto (add Template messages & RPC)

2. Business model:
   services/symbols/internal/biz/models.go (add Template struct)

3. Business interface:
   services/symbols/internal/biz/interfaces.go (add TemplateUseCase, TemplateRepo)

4. Use case implementation:
   services/symbols/internal/biz/templates.go (new file)
   services/symbols/internal/biz/templates_test.go (new file)

5. GORM entity:
   services/symbols/internal/data/model/template.go (new file)

6. Repository implementation:
   services/symbols/internal/data/repo/template.go (new file)

7. Service handlers:
   services/symbols/internal/service/templates.go (new file)
   services/symbols/internal/service/mapper.go (add Template mappers)

8. Wire setup:
   services/symbols/cmd/symbols/wire.go (add providers)
```

### Adding New Service

If adding a new service called `projects`:

```
Root structure:
├── api/projects/v1/projects.proto
├── contracts/projects/v1/ (generated)
└── services/projects/
    ├── cmd/projects/
    │   ├── main.go
    │   ├── wire.go
    │   └── wire_gen.go
    ├── internal/
    │   ├── biz/
    │   ├── data/
    │   ├── service/
    │   ├── server/
    │   └── conf/
    ├── configs/config.yaml
    ├── go.mod
    └── Makefile

Update go.work:
use (
    ./contracts
    ./platform
    ./services/symbols
    ./services/projects  # Add this
)
```

## Command Contexts

### From Root Directory

```bash
# You are here: /Users/alex/GolandProjects/brizy-go-services/

# Contract operations
make contracts-generate
make contracts-lint
make contracts-all

# Access files
cat api/symbols/v1/symbols.proto
cat contracts/symbols/v1/symbols.pb.go
cat platform/pagination/pagination.go
```

### From Service Directory

```bash
# You are here: /Users/alex/GolandProjects/brizy-go-services/services/symbols/

# Service operations
make generate
make test
make build

# Access files (relative)
cat internal/biz/symbols.go
cat internal/data/repo/symbol.go
cat cmd/symbols/main.go
```

## Import Path Reference

### In Service Code

```go
// Import contracts
import pb "brizy-go-services/contracts/symbols/v1"

// Import platform
import "brizy-go-platform/pagination"
import "brizy-go-platform/middleware/requestid"

// Internal imports (within same service)
import "brizy-go-services/services/symbols/internal/biz"
import "brizy-go-services/services/symbols/internal/data/model"
```

### Module Boundaries

```
✅ Allowed:
- Service → Contracts (generated proto)
- Service → Platform (shared utilities)
- Service internal layers (service → biz → data)

❌ Not Allowed:
- Service A → Service B internal
- External → Service internal
- Data layer → Service layer (reverse dependency)
```
