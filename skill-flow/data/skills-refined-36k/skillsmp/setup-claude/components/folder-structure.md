# Folder Structure Component

This component provides standard folder templates for different project types.

## Base Structure (All Projects)

Every project should have these folders:

```
project-root/
├── src/              # Source code
├── docs/             # Documentation
├── scripts/          # Utility scripts
├── .claude/          # Claude configuration
│   ├── skills/       # Project-specific skills
│   ├── commands/     # Quick commands
│   └── settings.json # Hooks and settings
├── .gitignore        # Git ignore rules
├── CLAUDE.md         # Claude project context
└── README.md         # Project readme
```

**Commands to create:**
```bash
mkdir -p src docs scripts .claude/skills .claude/commands
touch .claude/settings.json CLAUDE.md README.md .gitignore
```

---

## Project Type Templates

### Frontend (React/Vue/Svelte)

```
project-root/
├── src/
│   ├── components/     # Reusable UI components
│   │   └── ui/         # Base UI components (buttons, inputs)
│   ├── pages/          # Page components (if not using file routing)
│   ├── hooks/          # Custom React hooks
│   ├── lib/            # Utility functions
│   ├── styles/         # Global styles, themes
│   ├── types/          # TypeScript type definitions
│   └── assets/         # Static assets (images, fonts)
├── public/             # Public static files
├── tests/              # Test files
│   ├── unit/           # Unit tests
│   └── e2e/            # End-to-end tests
├── docs/
├── scripts/
└── .claude/
```

**Commands:**
```bash
mkdir -p src/{components/ui,pages,hooks,lib,styles,types,assets}
mkdir -p public tests/{unit,e2e}
```

### Next.js App Router

```
project-root/
├── src/
│   ├── app/            # App Router pages and layouts
│   │   ├── (auth)/     # Auth route group
│   │   ├── api/        # API routes
│   │   ├── layout.tsx  # Root layout
│   │   └── page.tsx    # Home page
│   ├── components/
│   │   ├── ui/         # UI primitives
│   │   └── features/   # Feature-specific components
│   ├── lib/            # Server utilities
│   ├── hooks/          # Client hooks
│   └── types/
├── public/
├── tests/
├── docs/
├── scripts/
└── .claude/
```

**Commands:**
```bash
mkdir -p src/app/{api,"(auth)"}
mkdir -p src/{components/{ui,features},lib,hooks,types}
mkdir -p public tests
```

### Backend (Node.js/Express/Fastify)

```
project-root/
├── src/
│   ├── routes/         # API route handlers
│   ├── controllers/    # Business logic controllers
│   ├── services/       # Service layer
│   ├── models/         # Data models
│   ├── middleware/     # Express/Fastify middleware
│   ├── utils/          # Utility functions
│   ├── types/          # TypeScript types
│   └── config/         # Configuration files
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── scripts/
└── .claude/
```

**Commands:**
```bash
mkdir -p src/{routes,controllers,services,models,middleware,utils,types,config}
mkdir -p tests/{unit,integration}
```

### Python Backend (FastAPI/Flask/Django)

```
project-root/
├── src/
│   ├── app/            # Application package
│   │   ├── api/        # API routes
│   │   ├── models/     # Data models
│   │   ├── services/   # Business logic
│   │   ├── schemas/    # Pydantic schemas
│   │   └── core/       # Core config, deps
│   └── tests/          # Test files
├── docs/
├── scripts/
└── .claude/
```

**Commands:**
```bash
mkdir -p src/app/{api,models,services,schemas,core}
mkdir -p src/tests docs scripts .claude/skills
```

### Fullstack (Frontend + Backend)

```
project-root/
├── apps/
│   ├── web/            # Frontend application
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   └── lib/
│   │   └── package.json
│   └── api/            # Backend application
│       ├── src/
│       │   ├── routes/
│       │   ├── services/
│       │   └── models/
│       └── package.json
├── packages/           # Shared packages
│   └── shared/         # Shared types/utils
│       └── src/
├── docs/
├── scripts/
├── .claude/
└── package.json        # Workspace root
```

**Commands:**
```bash
mkdir -p apps/web/src/{components,pages,lib}
mkdir -p apps/api/src/{routes,services,models}
mkdir -p packages/shared/src
```

### CLI Tool

```
project-root/
├── src/
│   ├── commands/       # CLI command handlers
│   ├── lib/            # Core functionality
│   ├── utils/          # Utility functions
│   ├── types/          # TypeScript types
│   └── index.ts        # Entry point
├── bin/                # Executable scripts
├── tests/
├── docs/
├── scripts/
└── .claude/
```

**Commands:**
```bash
mkdir -p src/{commands,lib,utils,types}
mkdir -p bin tests
```

### Library/Package

```
project-root/
├── src/
│   ├── lib/            # Core library code
│   ├── types/          # TypeScript types
│   └── index.ts        # Public API exports
├── examples/           # Usage examples
├── tests/
├── docs/
├── scripts/
└── .claude/
```

**Commands:**
```bash
mkdir -p src/{lib,types}
mkdir -p examples tests
```

---

## Common Patterns

### Test File Co-location

Some projects prefer tests next to source:

```
src/
├── components/
│   ├── Button.tsx
│   ├── Button.test.tsx    # Test next to source
│   ├── Input.tsx
│   └── Input.test.tsx
```

### Feature-Based Structure

For larger apps, organize by feature:

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api.ts
│   │   └── types.ts
│   ├── dashboard/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── types.ts
│   └── settings/
├── shared/              # Shared across features
│   ├── components/
│   ├── hooks/
│   └── lib/
```

---

## .gitignore Templates

### Node.js / TypeScript

```gitignore
# Dependencies
node_modules/

# Build
dist/
.next/
out/

# Environment
.env
.env.local
.env*.local

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*

# Testing
coverage/

# Cache
.cache/
.turbo/
```

### Python

```gitignore
# Byte-compiled
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
venv/
.venv/
env/

# Environment
.env

# IDE
.idea/
.vscode/

# Distribution
dist/
build/
*.egg-info/

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
```

---

## Initialization Commands

### Quick Create All Folders

```bash
# Function to create structure based on type
create_project_structure() {
  local type=$1

  # Base structure (always)
  mkdir -p src docs scripts .claude/skills .claude/commands

  case $type in
    "frontend")
      mkdir -p src/{components/ui,pages,hooks,lib,styles,types,assets}
      mkdir -p public tests/{unit,e2e}
      ;;
    "backend")
      mkdir -p src/{routes,controllers,services,models,middleware,utils,types,config}
      mkdir -p tests/{unit,integration}
      ;;
    "fullstack")
      mkdir -p apps/web/src/{components,pages,lib}
      mkdir -p apps/api/src/{routes,services,models}
      mkdir -p packages/shared/src
      ;;
    "cli")
      mkdir -p src/{commands,lib,utils,types}
      mkdir -p bin tests
      ;;
    "library")
      mkdir -p src/{lib,types}
      mkdir -p examples tests
      ;;
  esac
}
```

### Initialize Git

```bash
# Only if not already a git repo
if [ ! -d .git ]; then
  git init
  echo "# $(basename $(pwd))" > README.md
  git add .
  git commit -m "Initial commit"
fi
```

---

## Validation

After creating structure, verify:

```bash
# List all directories
find . -type d -not -path '*/\.*' | head -20

# Verify .claude exists
ls -la .claude/

# Verify key files
ls CLAUDE.md README.md .gitignore .claude/settings.json 2>/dev/null
```
