# Tech Stack Detection Guide

Reference for: Codebase Audit

How to detect project type, tech stack, and build configuration from filesystem.

## Package Manager Detection

Check for lock files to determine package manager:

| File | Package Manager | Audit Command |
|------|----------------|---------------|
| `package-lock.json` | npm | `npm audit --json` |
| `pnpm-lock.yaml` | pnpm | `pnpm audit --json` |
| `yarn.lock` | yarn | `yarn audit --json` |
| `requirements.txt` / `poetry.lock` | pip/poetry | `pip-audit --format json` or `safety check --json` |
| `Cargo.toml` | cargo | `cargo audit --json` |
| `go.mod` | go | `go list -json -m all \| nancy sleuth` |
| `Gemfile.lock` | bundler | `bundle audit` |
| `composer.lock` | composer | `composer audit` |

## Language and Framework Detection

Detect from configuration files:

### JavaScript/TypeScript
- `package.json` → Node.js project, check `dependencies` for frameworks
- `tsconfig.json` → TypeScript project
- `nuxt.config.ts` / `nuxt.config.js` → Nuxt (Vue framework)
- `next.config.js` / `next.config.ts` → Next.js (React framework)
- `vite.config.ts` / `vite.config.js` → Vite
- `vue.config.js` → Vue CLI
- `angular.json` → Angular

### Python
- `requirements.txt` / `pyproject.toml` → Python
- `manage.py` → Django
- Look for `flask` / `fastapi` in requirements → Flask/FastAPI

### Other Languages
- `Cargo.toml` → Rust
- `go.mod` → Go
- `*.csproj` / `*.sln` → .NET (C#/F#)
- `global.json` → .NET SDK version
- `build.gradle` / `pom.xml` → Java (Gradle/Maven)
- `Gemfile` → Ruby (Rails if `rails` in Gemfile)

## Cloud Platform Detection

| File/Pattern | Platform |
|-------------|----------|
| `azure-pipelines.yml` | Azure DevOps |
| `*.bicep` / `bicep/` | Azure Bicep (IaC) |
| `arm-template.json` / `azuredeploy.json` | Azure ARM templates |
| `*.tf` / `terraform/` | Terraform |
| `cloudformation.yml` / `*.template` | AWS CloudFormation |
| `.github/workflows/` | GitHub Actions |
| `.gitlab-ci.yml` | GitLab CI |
| `Jenkinsfile` | Jenkins |
| `.circleci/config.yml` | CircleCI |
| `serverless.yml` | Serverless Framework |

## Infrastructure and Tools

| File/Pattern | Tool/Purpose |
|-------------|-------------|
| `Dockerfile` / `docker-compose.yml` | Docker |
| `k8s/` / `kubernetes/` / `*.yaml` (with `kind: Deployment`) | Kubernetes |
| `.env` / `.env.example` | Environment configuration |
| `jest.config.js` / `jest.config.ts` | Jest (testing) |
| `vitest.config.ts` | Vitest (testing) |
| `playwright.config.ts` | Playwright (E2E testing) |
| `cypress.json` / `cypress.config.ts` | Cypress (E2E testing) |
| `*.test.js` / `*.spec.js` | xUnit pattern (testing) |
| `.eslintrc*` | ESLint (linting) |
| `.prettierrc` | Prettier (formatting) |
| `sonar-project.properties` | SonarQube |

## Build Tool Detection

| File | Build Tool |
|------|-----------|
| `webpack.config.js` | Webpack |
| `rollup.config.js` | Rollup |
| `esbuild.config.js` | esbuild |
| `turbo.json` | Turborepo |
| `nx.json` | Nx |
| `lerna.json` | Lerna |

## Database Detection

Look for:
- `prisma/schema.prisma` → Prisma ORM
- `drizzle.config.ts` → Drizzle ORM
- `typeorm.config.js` → TypeORM
- `knexfile.js` → Knex.js
- `sequelize.config.js` → Sequelize
- Check environment variables for `DATABASE_URL`, `POSTGRES_`, `MONGODB_`, etc.

## How to Build Tech Stack Summary

1. **Primary Language(s):** From lock files and config files
2. **Framework:** Nuxt, Next.js, Django, etc.
3. **Build/Bundler:** Vite, Webpack, Rollup, etc.
4. **Testing:** Jest, Vitest, Playwright, Cypress, pytest, etc.
5. **Cloud Platform:** Azure, AWS, GCP (from IaC and pipeline configs)
6. **IaC Tools:** Bicep, Terraform, ARM, CloudFormation
7. **CI/CD:** GitHub Actions, Azure DevOps, GitLab CI, etc.
8. **Database/ORM:** Prisma, TypeORM, etc.
9. **Linting/Formatting:** ESLint, Prettier, etc.

## Example Output

```markdown
## Tech Stack

**Language:** TypeScript 5.2, Node.js 20.x
**Framework:** Next.js 14 (App Router), React 18
**Database:** PostgreSQL 15 with Prisma
**Cloud:** Azure (App Service, SQL Database)
**IaC:** Bicep
**CI/CD:** Azure DevOps Pipelines
**Testing:** Jest, Playwright
**Build:** Turbo, Webpack
**Linting:** ESLint, Prettier
```
