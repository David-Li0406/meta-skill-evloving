# Code Project Analysis

Detailed patterns for analyzing code projects by language and framework.

## Node.js Projects

### Package.json Analysis

Extract and document:
- `name`, `version`, `description`
- `main` or `module` entry point
- `scripts` - especially `start`, `build`, `test`, `dev`
- `dependencies` - core runtime dependencies
- `devDependencies` - build/test tools
- `engines` - Node version requirements

### Framework Detection

| Dependency | Framework |
|------------|-----------|
| `next` | Next.js |
| `react` | React (check for CRA, Vite) |
| `express` | Express.js |
| `fastify` | Fastify |
| `nest` | NestJS |
| `nuxt` | Nuxt.js |
| `vue` | Vue.js |

### Configuration Files

- `tsconfig.json` - TypeScript configuration
- `.eslintrc.*` - Linting rules
- `jest.config.*` - Test configuration
- `vite.config.*` / `webpack.config.*` - Build configuration

## Python Projects

### pyproject.toml Analysis

```toml
[project]
name = "project-name"
version = "0.1.0"
dependencies = [...]

[project.scripts]
cli-name = "module:main"

[tool.pytest.ini_options]
# Test configuration
```

### Framework Detection

| Dependency | Framework |
|------------|-----------|
| `django` | Django |
| `flask` | Flask |
| `fastapi` | FastAPI |
| `airflow` | Apache Airflow |
| `celery` | Celery (task queue) |

### Directory Patterns

- `src/` or package name directory - Source code
- `tests/` - Test files
- `scripts/` - Utility scripts
- `docs/` - Documentation

## Go Projects

### go.mod Analysis

```go
module github.com/user/project

go 1.21

require (
    // Dependencies
)
```

### Project Structure

- `cmd/` - Main applications
- `pkg/` - Library code
- `internal/` - Private packages
- `api/` - API definitions (OpenAPI, proto)

### Common Patterns

| Import Path | Type |
|-------------|------|
| `net/http` | HTTP server |
| `github.com/gin-gonic/gin` | Gin framework |
| `github.com/gorilla/mux` | Gorilla router |
| `gorm.io/gorm` | GORM ORM |

## Java Projects

### Maven (pom.xml)

```xml
<project>
  <groupId>com.example</groupId>
  <artifactId>project</artifactId>
  <version>1.0.0</version>
  <dependencies>...</dependencies>
</project>
```

### Gradle (build.gradle)

```groovy
plugins {
    id 'java'
    id 'org.springframework.boot'
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
}
```

### Framework Detection

| Dependency | Framework |
|------------|-----------|
| `spring-boot` | Spring Boot |
| `quarkus` | Quarkus |
| `micronaut` | Micronaut |

## Monorepo Analysis

### Package Discovery

For each workspace package, extract:
- Package name and version
- Dependencies (internal and external)
- Scripts available
- Build outputs

### Dependency Graph

Document relationships between packages:
- Which packages depend on which
- Shared dependencies
- Build order requirements

### Common Commands

| Tool | List Packages | Run All |
|------|---------------|---------|
| npm workspaces | `npm ls -ws` | `npm run build -ws` |
| pnpm | `pnpm ls -r` | `pnpm -r run build` |
| yarn workspaces | `yarn workspaces list` | `yarn workspaces run build` |
| nx | `nx show projects` | `nx run-many -t build` |
| turbo | N/A | `turbo run build` |

## CI/CD Detection

| File | CI System |
|------|-----------|
| `.github/workflows/` | GitHub Actions |
| `.gitlab-ci.yml` | GitLab CI |
| `Jenkinsfile` | Jenkins |
| `.drone.yml` | Drone CI |
| `.circleci/config.yml` | CircleCI |
| `azure-pipelines.yml` | Azure DevOps |

## Container Detection

| File | Technology |
|------|------------|
| `Dockerfile` | Docker |
| `docker-compose.yml` | Docker Compose |
| `Containerfile` | Podman |
| `.dockerignore` | Docker (ignore patterns) |
