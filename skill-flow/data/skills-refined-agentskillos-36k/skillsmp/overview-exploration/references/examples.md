# Overview Exploration Examples

## Example 1: Next.js Project

**Goal**: "Add authentication with OAuth"

**Exploration Commands**:
```python
# Step 1: Detect framework
Glob(pattern="package.json")
# → Found: package.json

Read(file_path="package.json")
# → Dependencies: next@14.0.0, react@18.2.0, typescript@5.0.0

# Step 2: Structure
Glob(pattern="*")
# → [".next", "app", "components", "lib", "public", "node_modules", "package.json"]

Glob(pattern="app/**/*.tsx")
# → ["app/page.tsx", "app/layout.tsx", "app/api/users/route.ts"]

# Step 3: Check existing auth
Grep(pattern="auth|login|session", output_mode="files_with_matches")
# → No matches

# Step 4: Read docs
Read(file_path="README.md")
# → Simple Next.js starter, no auth mentioned
```

**Output**:
```markdown
## Overview Exploration Results

**Project Type**: Next.js 14 App Router

**Tech Stack**:
- Language: TypeScript 5.0
- Framework: Next.js 14 (App Router)
- Database: Not found
- Test: Not found

**Directory Structure**:
```
project/
├── app/              # Next.js App Router pages
│   ├── page.tsx      # Homepage
│   ├── layout.tsx    # Root layout
│   └── api/          # API routes
├── components/       # React components
└── lib/              # Utilities
```

**Key Entry Points**:
- app/layout.tsx (root layout)
- app/api/* (API routes)

**Existing Patterns**:
- Auth: not found
- Database: not found
- API: REST via route handlers

**Relevant Files** (based on Goal):
- app/layout.tsx: Need to wrap with SessionProvider
- app/api/: Where auth routes will go
```

---

## Example 2: Go CLI Tool

**Goal**: "Add config file support"

**Exploration Commands**:
```python
# Step 1: Detect Go project
Glob(pattern="go.mod")
# → Found: go.mod

Read(file_path="go.mod")
# → module: github.com/user/tool, go 1.21

# Step 2: Structure
Glob(pattern="*")
# → ["cmd", "internal", "pkg", "go.mod", "go.sum", "README.md"]

Glob(pattern="cmd/**/*.go")
# → ["cmd/tool/main.go"]

Glob(pattern="internal/**/*.go")
# → ["internal/cli/cli.go", "internal/runner/runner.go"]

# Step 3: Check existing config
Grep(pattern="config|\.yaml|\.toml", output_mode="content", -n=true)
# → internal/cli/cli.go:15: // TODO: Add config file support

Read(file_path="internal/cli/cli.go")
# → CLI uses cobra, flags only, no config file
```

**Output**:
```markdown
## Overview Exploration Results

**Project Type**: Go CLI Tool

**Tech Stack**:
- Language: Go 1.21
- Framework: cobra (CLI framework)
- Database: N/A
- Test: go test (standard)

**Directory Structure**:
```
tool/
├── cmd/tool/         # Main entry point
├── internal/cli/     # CLI logic (cobra)
├── internal/runner/  # Business logic
└── pkg/              # Public packages
```

**Key Entry Points**:
- cmd/tool/main.go (entry point)
- internal/cli/cli.go (CLI setup)

**Existing Patterns**:
- Config: TODO comment found, not implemented
- CLI: cobra with flags
- Test: Standard go test

**Relevant Files** (based on Goal):
- internal/cli/cli.go: Add config loading here
- go.mod: May need viper or similar for config parsing
```

---

## Example 3: Python Django Project

**Goal**: "Add REST API endpoints"

**Exploration Commands**:
```python
# Step 1: Detect Python/Django
Glob(pattern="manage.py")
# → Found: manage.py

Glob(pattern="requirements.txt")
# → Found: requirements.txt

Read(file_path="requirements.txt")
# → Django==4.2, djangorestframework==3.14

# Step 2: Structure
Glob(pattern="*")
# → ["manage.py", "myproject", "apps", "requirements.txt"]

Glob(pattern="apps/**/views.py")
# → ["apps/users/views.py", "apps/posts/views.py"]

# Step 3: Check existing API
Grep(pattern="api|rest_framework|APIView", output_mode="files_with_matches")
# → apps/users/views.py (has basic ViewSets)
```

**Output**:
```markdown
## Overview Exploration Results

**Project Type**: Django Web Application

**Tech Stack**:
- Language: Python 3.11
- Framework: Django 4.2 + DRF 3.14
- Database: PostgreSQL (from settings)
- Test: pytest-django

**Directory Structure**:
```
project/
├── myproject/        # Project settings
│   ├── settings.py
│   └── urls.py
├── apps/             # Django apps
│   ├── users/
│   └── posts/
└── manage.py
```

**Key Entry Points**:
- myproject/urls.py (URL routing)
- apps/*/views.py (view logic)

**Existing Patterns**:
- API: DRF ViewSets in apps/users/
- Auth: Django built-in
- Database: Django ORM

**Relevant Files** (based on Goal):
- myproject/urls.py: Add API router
- apps/*/serializers.py: Need to create
```
