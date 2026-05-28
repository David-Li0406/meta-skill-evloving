# Directory Structure Analysis

Analyze directory structure to identify architecture patterns and key components.

## Overview

Map the directory structure to understand the application's organization and identify:
- Architecture patterns (MVC, microservices, monolith, etc.)
- Key components (backend, frontend, database, API, infrastructure)
- Configuration files
- Source code organization

---

## Directory Mapping Commands

### Basic Structure

```bash
# Show directory tree (limited depth to avoid noise)
find . -type d -maxdepth 3 | grep -v -E "node_modules|vendor|\.git|build|dist|target|__pycache__|\.next|\.nuxt" | sort | head -50
```

### Configuration Files

```bash
# Find all configuration files
find . -maxdepth 3 \( \
  -name "*.json" -o \
  -name "*.yaml" -o \
  -name "*.yml" -o \
  -name "*.toml" -o \
  -name "*.xml" -o \
  -name "*.conf" -o \
  -name "*.config" -o \
  -name ".env*" \
\) | grep -v -E "node_modules|vendor|\.git|dist|build" | sort | head -40
```

---

## Architecture Pattern Recognition

### Frontend Patterns

**Next.js / React (App Router)**
```
app/               # Next.js 13+ app directory
  components/
  api/
  (routes)/
public/
```

**Next.js (Pages Router)**
```
pages/             # Next.js pages
  api/             # API routes
components/
public/
```

**Standard React**
```
src/
  components/
  hooks/
  pages/
  utils/
public/
```

**Vue.js**
```
src/
  components/
  views/
  router/
  store/
public/
```

**Angular**
```
src/
  app/
    components/
    services/
    modules/
  assets/
```

### Backend Patterns

**Node.js/Express**
```
src/
  routes/
  controllers/
  models/
  middleware/
  services/
```

**NestJS**
```
src/
  modules/
  controllers/
  services/
  entities/
  dto/
```

**Django**
```
project_name/
  app_name/
    models/
    views/
    templates/
    migrations/
  settings/
manage.py
```

**Ruby on Rails**
```
app/
  models/
  controllers/
  views/
  helpers/
db/
  migrate/
config/
```

### Microservices Pattern

```
services/
  service-a/
  service-b/
  service-c/
shared/
docker-compose.yml
```

### Monorepo Pattern

```
packages/
  package-a/
  package-b/
apps/
  app-1/
  app-2/
turbo.json (or lerna.json, nx.json)
```

---

## Component Detection

### Backend Detection

Indicators of backend code:

```bash
# API/Backend directories
find . -type d -name "api" -o -name "server" -o -name "backend" -o -name "routes" -o -name "controllers" 2>/dev/null

# Server files
find . -name "server.js" -o -name "server.ts" -o -name "app.js" -o -name "app.ts" -o -name "main.py" 2>/dev/null
```

### Frontend Detection

Indicators of frontend code:

```bash
# Frontend directories
find . -type d -name "components" -o -name "pages" -o -name "views" -o -name "public" -o -name "assets" 2>/dev/null

# Frontend config files
find . -name "next.config.*" -o -name "vite.config.*" -o -name "vue.config.*" -o -name "angular.json" 2>/dev/null
```

### Database Detection

Indicators of database usage:

```bash
# ORM/Database directories
find . -type d -name "prisma" -o -name "migrations" -o -name "models" -o -name "entities" 2>/dev/null

# Database schema files
find . -name "schema.prisma" -o -name "*.sql" -o -name "database.yml" 2>/dev/null
```

### Infrastructure Detection

Indicators of infrastructure-as-code:

```bash
# IaC directories
find . -type d -name "terraform" -o -name "infrastructure" -o -name "infra" -o -name ".aws" 2>/dev/null

# IaC files
find . -name "*.tf" -o -name "cloudformation.yml" -o -name "serverless.yml" -o -name "cdk.json" 2>/dev/null
```

---

## Source File Counting

Count source files by type to understand project size:

### JavaScript/TypeScript

```bash
# TypeScript/JavaScript files (excluding tests, node_modules, build)
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) \
  | grep -v -E "node_modules|dist|build|\.next|coverage|test|spec" \
  | wc -l
```

### Python

```bash
# Python files
find . -type f -name "*.py" \
  | grep -v -E "__pycache__|venv|\.venv|dist|build|test_" \
  | wc -l
```

### Java

```bash
# Java files
find . -type f -name "*.java" \
  | grep -v -E "build|target|test" \
  | wc -l
```

### Ruby

```bash
# Ruby files
find . -type f -name "*.rb" \
  | grep -v -E "vendor|spec|test" \
  | wc -l
```

### Other Languages

Adapt the pattern based on detected language:
- PHP: `*.php`
- Go: `*.go`
- Rust: `*.rs`
- C#: `*.cs`
- Swift: `*.swift`
- Kotlin: `*.kt`

---

## Key Components Summary

After analysis, summarize key components:

```markdown
### Key Components Identified

- **Backend:** Yes - Express.js API server
  - Location: `src/api/` (12 routes, 8 controllers)
  - Database: PostgreSQL via Prisma ORM
  - Authentication: JWT-based

- **Frontend:** Yes - Next.js 14 with App Router
  - Location: `app/` (15 pages, 23 components)
  - Styling: Tailwind CSS
  - State: React Context + Server Components

- **Database:** PostgreSQL
  - ORM: Prisma
  - Schema: `prisma/schema.prisma` (8 models)
  - Migrations: 12 migration files

- **API:** RESTful + tRPC
  - REST endpoints: `app/api/` (5 routes)
  - tRPC router: `src/server/api/` (4 routers)
  - OpenAPI: Not found

- **Infrastructure:** AWS Serverless
  - IaC: Terraform (`infrastructure/terraform/`)
  - Services: Lambda, API Gateway, RDS, S3
  - CI/CD: GitHub Actions (`.github/workflows/`)
```

---

## Architecture Pattern Summary

Based on directory structure, identify the overall pattern:

**Examples:**

- **Monolithic Full-Stack** - Single repo with frontend + backend + database
- **Microservices** - Multiple independent services
- **JAMstack** - Static frontend + serverless functions + headless CMS
- **Serverless** - No traditional servers, all functions/managed services
- **Monorepo** - Multiple packages/apps in one repository
- **Client-Server** - Clear separation between client and server code

---

## Common Directory Structures by Framework

### Next.js 13+ (App Router)
```
app/
  (auth)/
    login/
    register/
  dashboard/
  api/
components/
  ui/
lib/
public/
prisma/
```

### Next.js (Pages Router)
```
pages/
  api/
  _app.tsx
  index.tsx
components/
public/
styles/
```

### Express.js Backend
```
src/
  routes/
  controllers/
  models/
  middleware/
  services/
  utils/
  config/
tests/
```

### Django
```
project/
  app/
    models.py
    views.py
    urls.py
    serializers.py
  settings/
  wsgi.py
manage.py
requirements.txt
```

### Rails
```
app/
  models/
  controllers/
  views/
  jobs/
  mailers/
db/
  migrate/
config/
  routes.rb
Gemfile
```

---

## Notes

- Exclude common noise directories: node_modules, vendor, .git, dist, build, target, __pycache__, .next, .nuxt, coverage
- Limit depth to 3 levels to avoid overwhelming output
- Use `head` to limit file counts for large codebases
- Look for naming conventions that indicate purpose (e.g., `controllers/`, `services/`, `utils/`)
