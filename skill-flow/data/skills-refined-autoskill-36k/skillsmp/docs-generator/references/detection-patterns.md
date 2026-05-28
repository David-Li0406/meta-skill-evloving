# Detection Patterns

Patterns for analyzing repositories to detect languages, frameworks, architecture, and conventions.

## Config File → Language/Framework Mapping

### JavaScript/TypeScript Ecosystem

| File | Indicates |
|------|-----------|
| `package.json` | Node.js project |
| `tsconfig.json` | TypeScript |
| `next.config.js`, `next.config.mjs` | Next.js |
| `nuxt.config.ts`, `nuxt.config.js` | Nuxt.js |
| `vite.config.ts`, `vite.config.js` | Vite |
| `astro.config.mjs` | Astro |
| `remix.config.js` | Remix |
| `svelte.config.js` | SvelteKit |
| `angular.json` | Angular |
| `vue.config.js` | Vue CLI |
| `gatsby-config.js` | Gatsby |
| `electron-builder.json` | Electron |
| `tauri.conf.json` | Tauri |
| `.babelrc`, `babel.config.js` | Babel |
| `webpack.config.js` | Webpack |
| `rollup.config.js` | Rollup |
| `esbuild.config.js` | esbuild |
| `jest.config.js` | Jest |
| `vitest.config.ts` | Vitest |
| `playwright.config.ts` | Playwright |
| `cypress.config.ts` | Cypress |

### Package Manager Detection

| File | Package Manager |
|------|-----------------|
| `pnpm-lock.yaml` | pnpm |
| `yarn.lock` | Yarn |
| `package-lock.json` | npm |
| `bun.lockb` | Bun |

Also check `package.json` → `packageManager` field.

### Python Ecosystem

| File | Indicates |
|------|-----------|
| `pyproject.toml` | Modern Python (check for tool) |
| `setup.py`, `setup.cfg` | Traditional Python package |
| `requirements.txt` | pip dependencies |
| `Pipfile` | pipenv |
| `poetry.lock` | Poetry |
| `pdm.lock` | PDM |
| `uv.lock` | uv |
| `manage.py` | Django |
| `app.py` + Flask imports | Flask |
| `main.py` + FastAPI imports | FastAPI |
| `pytest.ini`, `conftest.py` | pytest |

### Rust Ecosystem

| File | Indicates |
|------|-----------|
| `Cargo.toml` | Rust/Cargo |
| `Cargo.lock` | Committed dependencies |
| `rust-toolchain.toml` | Specific Rust version |

### Go Ecosystem

| File | Indicates |
|------|-----------|
| `go.mod` | Go modules |
| `go.sum` | Dependency checksums |
| `main.go` in root | CLI/executable |
| `cmd/` directory | Multi-binary project |

### Java/JVM Ecosystem

| File | Indicates |
|------|-----------|
| `pom.xml` | Maven |
| `build.gradle`, `build.gradle.kts` | Gradle |
| `settings.gradle` | Multi-module Gradle |
| `.mvn/` | Maven wrapper |
| `gradlew` | Gradle wrapper |

### Ruby Ecosystem

| File | Indicates |
|------|-----------|
| `Gemfile` | Bundler |
| `Gemfile.lock` | Locked dependencies |
| `Rakefile` | Rake tasks |
| `config/application.rb` | Rails |

### PHP Ecosystem

| File | Indicates |
|------|-----------|
| `composer.json` | Composer |
| `artisan` | Laravel |
| `symfony.lock` | Symfony |

### .NET Ecosystem

| File | Indicates |
|------|-----------|
| `*.csproj` | C# project |
| `*.fsproj` | F# project |
| `*.sln` | Visual Studio solution |
| `global.json` | .NET SDK version |

### Other

| File | Indicates |
|------|-----------|
| `Dockerfile` | Docker |
| `docker-compose.yml` | Docker Compose |
| `kubernetes/`, `k8s/` | Kubernetes |
| `terraform/`, `*.tf` | Terraform |
| `pulumi/`, `Pulumi.yaml` | Pulumi |
| `serverless.yml` | Serverless Framework |
| `.github/workflows/` | GitHub Actions |
| `.gitlab-ci.yml` | GitLab CI |
| `Jenkinsfile` | Jenkins |
| `.circleci/config.yml` | CircleCI |

---

## Directory Pattern → Architecture Style Mapping

### Monorepo Indicators

```
packages/
apps/
libs/
modules/
workspaces/
```

Also check:
- `package.json` → `workspaces`
- `pnpm-workspace.yaml`
- `lerna.json`
- `turbo.json` (Turborepo)
- `nx.json` (Nx)

### Layered Architecture Indicators

```
src/
├── controllers/    # or handlers/
├── services/       # or usecases/
├── repositories/   # or data/
├── models/         # or entities/
└── utils/          # or helpers/
```

### Domain-Driven Design Indicators

```
src/
├── domain/
│   ├── entities/
│   ├── value-objects/
│   └── aggregates/
├── application/
│   ├── commands/
│   ├── queries/
│   └── services/
├── infrastructure/
│   ├── persistence/
│   └── external/
└── interfaces/
    ├── api/
    └── web/
```

### Microservices Indicators

```
services/
├── user-service/
├── order-service/
└── payment-service/
```

Or separate repos with:
- API gateway config
- Service discovery config
- Message queue config

### Feature-Based / Modular Indicators

```
src/
├── features/
│   ├── auth/
│   ├── users/
│   └── orders/
```

Or:

```
src/
├── auth/
│   ├── components/
│   ├── hooks/
│   └── api/
├── users/
└── orders/
```

### Frontend Architecture Indicators

```
# Component-based (React/Vue/Svelte)
src/
├── components/
├── pages/          # or views/
├── hooks/          # or composables/
├── stores/         # or state/
└── utils/

# Atomic Design
src/
├── atoms/
├── molecules/
├── organisms/
├── templates/
└── pages/
```

---

## Code Pattern Detection (Grep Patterns)

### Naming Conventions

```bash
# File naming - list source files
find src -type f -name "*.{ts,js,tsx,jsx,py,rs,go}" | head -20

# Variable naming - look for declarations
grep -rE "(const|let|var|def|fn|func)\s+\w+" src/ | head -20

# Class/Component naming
grep -rE "(class|interface|type|struct|enum)\s+\w+" src/ | head -20
```

### Error Handling Patterns

```bash
# Try/catch blocks
grep -rE "try\s*\{" src/ | wc -l

# Result/Either types
grep -rE "(Result|Either|Option|Maybe)<" src/ | head -10

# Error classes
grep -rE "class\s+\w*Error" src/ | head -10

# Error codes
grep -rE "error_code|ERROR_CODE|errorCode" src/ | head -10
```

### Testing Patterns

```bash
# Test frameworks
grep -rE "(describe|it|test|expect|assert)" tests/ | head -10

# Test file patterns
find . -name "*test*" -o -name "*spec*" | head -20

# Mock patterns
grep -rE "(mock|jest\.fn|vi\.fn|Mock|stub)" tests/ | head -10
```

### Logging Patterns

```bash
# Logger usage
grep -rE "(logger|console|log)\.(info|warn|error|debug)" src/ | head -20

# Structured logging
grep -rE "logger\.\w+\(['\"][^'\"]+['\"],\s*\{" src/ | head -10
```

### API Design Patterns

```bash
# REST endpoints
grep -rE "(GET|POST|PUT|DELETE|PATCH)\s+['\"/]" src/ | head -20

# Express/Fastify routes
grep -rE "\.(get|post|put|delete|patch)\s*\(['\"]/" src/ | head -20

# GraphQL
grep -rE "(Query|Mutation|Subscription|@Resolver)" src/ | head -10
```

---

## Build/Task Runner Detection

### Priority Order

1. **justfile / Justfile**
   ```bash
   if [ -f "justfile" ] || [ -f "Justfile" ]; then
     just --list
   fi
   ```

2. **package.json scripts**
   ```bash
   jq '.scripts | keys[]' package.json
   ```

3. **Makefile**
   ```bash
   grep -E "^[a-zA-Z_-]+:" Makefile | cut -d: -f1
   ```

4. **Taskfile.yml** (Task)
   ```bash
   task --list
   ```

5. **Language-specific**
   - Python: `pyproject.toml` → `[tool.poetry.scripts]` or `[project.scripts]`
   - Rust: `cargo run`, `cargo build`, `cargo test`
   - Go: `go run .`, `go build`, `go test ./...`

---

## Dependency Analysis

### Extract Key Dependencies

```bash
# Node.js
jq '.dependencies, .devDependencies | keys[]' package.json | sort -u

# Python (pyproject.toml)
grep -A100 '\[tool.poetry.dependencies\]' pyproject.toml | grep -E "^\w+ ="

# Rust
grep -E "^\w+\s*=" Cargo.toml | grep -v "^\[" | head -20

# Go
cat go.mod | grep -E "^\t" | awk '{print $1}'
```

### Framework Detection from Dependencies

| Dependency | Framework |
|------------|-----------|
| `react`, `react-dom` | React |
| `vue` | Vue |
| `svelte` | Svelte |
| `@angular/core` | Angular |
| `next` | Next.js |
| `nuxt` | Nuxt |
| `express` | Express |
| `fastify` | Fastify |
| `nestjs` | NestJS |
| `django` | Django |
| `flask` | Flask |
| `fastapi` | FastAPI |
| `actix-web`, `axum`, `rocket` | Rust web frameworks |
| `gin`, `echo`, `fiber` | Go web frameworks |

---

## Linting/Formatting Config Detection

| File | Tool |
|------|------|
| `.eslintrc*`, `eslint.config.*` | ESLint |
| `.prettierrc*`, `prettier.config.*` | Prettier |
| `biome.json` | Biome |
| `deno.json` | Deno |
| `.editorconfig` | EditorConfig |
| `rustfmt.toml` | rustfmt |
| `clippy.toml` | Clippy |
| `pyproject.toml` → `[tool.ruff]` | Ruff |
| `pyproject.toml` → `[tool.black]` | Black |
| `.golangci.yml` | golangci-lint |
| `rubocop.yml` | RuboCop |
