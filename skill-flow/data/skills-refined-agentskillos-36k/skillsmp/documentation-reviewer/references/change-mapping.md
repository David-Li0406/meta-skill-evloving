# Code-to-Documentation Mapping

Rules for mapping code changes to documentation updates across multiple languages.

## Python/Django

| File Pattern | Documentation Target |
|-------------|---------------------|
| `views.py`, `urls.py` | `docs/api/endpoints.md` |
| `models.py`, `serializers.py` | `docs/api/`, `docs/architecture/` |
| `management/commands/` | `docs/development/` |
| `settings.py` | `docs/getting-started/`, `docs/architecture/` |
| `pyproject.toml`, `requirements.txt` | `docs/getting-started/installation.md` |

## TypeScript/JavaScript

| File Pattern | Documentation Target |
|-------------|---------------------|
| `features/`, `components/` | `docs/architecture/frontend.md` |
| `routes/`, `api/` | `docs/api/` |
| `package.json` | `docs/getting-started/installation.md` |
| `tsconfig.json` | `docs/development/` |

## Go

| File Pattern | Documentation Target |
|-------------|---------------------|
| `go.mod`, `go.sum` | `docs/getting-started/installation.md` |
| `cmd/` | `docs/development/commands.md` |
| `pkg/` | `docs/api/`, `docs/architecture/` |
| `internal/` | `docs/architecture/` |
| `handlers/`, `routes/` | `docs/api/endpoints.md` |

## Rust

| File Pattern | Documentation Target |
|-------------|---------------------|
| `Cargo.toml` | `docs/getting-started/installation.md` |
| `src/lib.rs` | `docs/api/` |
| `src/main.rs` | `docs/getting-started/` |
| `src/bin/` | `docs/development/commands.md` |

## Java/Kotlin

| File Pattern | Documentation Target |
|-------------|---------------------|
| `build.gradle`, `pom.xml` | `docs/getting-started/installation.md` |
| `src/main/java/`, `src/main/kotlin/` | `docs/api/`, `docs/architecture/` |

## Ruby/Rails

| File Pattern | Documentation Target |
|-------------|---------------------|
| `Gemfile` | `docs/getting-started/installation.md` |
| `config/routes.rb` | `docs/api/endpoints.md` |
| `app/controllers/` | `docs/api/endpoints.md` |
| `app/models/` | `docs/architecture/` |

## Task Runners

| File Pattern | Documentation Target |
|-------------|---------------------|
| `justfile`, `Justfile`, `just/` | `docs/development/commands.md` |
| `Makefile` | `docs/development/commands.md` |
| `tasks/` (invoke) | `docs/development/invoke-tasks.md` |
| `scripts/` | `docs/development/` |

## Infrastructure

| File Pattern | Documentation Target |
|-------------|---------------------|
| `docker/`, `Dockerfile` | `docs/architecture/docker.md` |
| `kubernetes/`, `k8s/`, `helm/` | `docs/architecture/deployment.md` |
| `.github/workflows/`, `.gitlab-ci` | `docs/development/ci-cd.md` |
| `terraform/`, `ansible/` | `docs/architecture/infrastructure.md` |
| `nginx/` | `docs/architecture/docker.md` |

## High-Priority Patterns by Language

### Python
- `@api_view` → New API endpoint
- `@task` → New invoke task
- `models.Model` → New Django model
- `@router.` → New FastAPI route

### TypeScript/JavaScript
- `export default function` → New component
- `export {` → New module export
- `createRoute` → New route definition

### Go
- `func New*` → New constructor
- `func Handle*` → New handler
- `type ` → New type definition
- `require ` in go.mod → New dependency

### Rust
- `pub fn` → New public function
- `pub struct` → New public struct
- `pub trait` → New public trait

### Just/Make
- Lines with `:` → New task/target
- Lines with `@` → Recipe steps

## Documentation Templates

### New Task (justfile)

```markdown
### `just task-name`

Brief description.

**Usage:**
```bash
just task-name [options]
```
```

### New Go Handler

```markdown
### `GET /api/resource`

Description.

**Response:**
```json
{"field": "value"}
```
```
