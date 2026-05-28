# Phase 7: Code Scaffolding

## Objective

Create the project structure, empty modules, and configuration files without implementation logic.

## Step 1: Directory Structure Design

Present structure options based on product type:

```markdown
### Decision: Project Structure

**Option A: Feature-Based (Recommended for most projects)**
```
project/
├── src/
│   ├── features/
│   │   ├── auth/
│   │   │   ├── handlers/
│   │   │   ├── services/
│   │   │   ├── models/
│   │   │   └── tests/
│   │   └── users/
│   │       ├── handlers/
│   │       ├── services/
│   │       ├── models/
│   │       └── tests/
│   ├── shared/
│   │   ├── utils/
│   │   ├── middleware/
│   │   └── types/
│   └── main.{ext}
├── config/
├── scripts/
└── tests/
    └── integration/
```

**Option B: Layer-Based**
```
project/
├── src/
│   ├── handlers/     # or controllers
│   ├── services/
│   ├── repositories/
│   ├── models/
│   └── utils/
├── config/
└── tests/
```

**Option C: Domain-Driven**
```
project/
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   └── value-objects/
│   ├── application/
│   │   ├── commands/
│   │   └── queries/
│   ├── infrastructure/
│   │   ├── persistence/
│   │   └── external/
│   └── presentation/
└── tests/
```

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **Feature-Based** | Easy navigation, scalable | Potential duplication | Medium-large projects |
| Layer-Based | Simple, familiar | Hard to scale, cross-cutting | Small projects |
| Domain-Driven | Clean separation | Steep learning curve | Complex domains |

**Recommendation**: [Option] because [reasoning]
```

## Step 2: Module/Package Scaffolding

Create empty modules with signatures:

```markdown
### Module Scaffold: [Module Name]

**Path**: `src/features/[feature]/[module].{ext}`

**Exports**:
```typescript
// Public interface - what this module exposes
export interface ModuleInterface {
  method1(param: Type): ReturnType;
  method2(param: Type): Promise<ReturnType>;
}

// Types used by this module
export interface ModuleConfig {
  setting1: string;
  setting2: number;
}

// Factory function
export function createModule(config: ModuleConfig): ModuleInterface;
```

**Internal Structure**:
```
module/
├── index.{ext}        # Public exports only
├── types.{ext}        # Type definitions
├── service.{ext}      # Main logic (empty)
├── repository.{ext}   # Data access (empty)
└── utils.{ext}        # Module-specific utilities
```

**Dependencies**:
- Internal: [Other modules from this project]
- External: [Third-party packages]
```

## Step 3: Configuration File Setup

```markdown
### Configuration Files

**Package/Project Definition**:
```json
// package.json / pyproject.toml / Cargo.toml / go.mod
{
  "name": "project-name",
  "version": "0.1.0",
  "description": "Project description",
  "scripts": {
    "build": "...",
    "test": "...",
    "lint": "...",
    "dev": "..."
  },
  "dependencies": {
    // Production dependencies
  },
  "devDependencies": {
    // Development dependencies
  }
}
```

**Environment Configuration**:
```yaml
# config/default.yaml
server:
  host: localhost
  port: 8080

database:
  host: localhost
  port: 5432
  name: appdb

logging:
  level: info
  format: json
```

**TypeScript/Compiler Config** (if applicable):
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "strict": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**Linting/Formatting**:
```json
// .eslintrc.json / .pylintrc / etc.
{
  "extends": ["recommended"],
  "rules": {
    // Project-specific rules
  }
}
```
```

## Step 4: Entry Point Setup

```markdown
### Entry Point: [main file]

**Path**: `src/main.{ext}`

**Structure**:
```typescript
// Imports
import { createServer } from './server';
import { loadConfig } from './config';
import { setupLogging } from './logging';

// Bootstrap function (empty implementation)
async function bootstrap(): Promise<void> {
  // TODO: Load configuration
  // TODO: Setup logging
  // TODO: Initialize dependencies
  // TODO: Start server
}

// Entry point
if (require.main === module) {
  bootstrap().catch(console.error);
}

export { bootstrap };
```
```

## Step 5: Build & CI Setup

```markdown
### Build Configuration

**Dockerfile** (if containerized):
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/main.js"]
```

**CI Pipeline** (.github/workflows/ci.yml):
```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run lint
      - run: npm run test
      - run: npm run build
```

**Makefile** (optional):
```makefile
.PHONY: build test lint dev clean

build:
	npm run build

test:
	npm run test

lint:
	npm run lint

dev:
	npm run dev

clean:
	rm -rf dist node_modules
```
```

## Step 6: Documentation Structure

```markdown
### Documentation Scaffolding

```
docs/
├── README.md           # Project overview
├── CONTRIBUTING.md     # How to contribute
├── api/               # API documentation
│   └── README.md
├── architecture/      # Architecture decisions
│   └── decisions/
│       └── 001-initial-architecture.md
└── guides/            # User guides
    └── getting-started.md
```

**README.md Template**:
```markdown
# Project Name

Brief description.

## Quick Start

\`\`\`bash
# Installation
npm install

# Development
npm run dev

# Testing
npm run test
\`\`\`

## Documentation

- [API Reference](./docs/api/)
- [Architecture](./docs/architecture/)
- [Contributing](./CONTRIBUTING.md)
```
```

## Step 7: Scaffolding Checklist

Verify all scaffolding is complete:

```
Scaffolding Checklist:
- [ ] Directory structure created
- [ ] All modules have empty files with exports
- [ ] Type definitions in place
- [ ] Configuration files created
- [ ] Entry point defined
- [ ] Build scripts configured
- [ ] CI pipeline setup
- [ ] Documentation structure created
- [ ] .gitignore configured
- [ ] README.md created
```

## Phase 7 Approval Gate

```markdown
## Phase 7 Summary: Code Scaffolding

### Project Structure
```
[Show final directory tree]
```

### Modules Created
| Module | Path | Dependencies |
|--------|------|--------------|
| [Module A] | src/... | [Deps] |
| [Module B] | src/... | [Deps] |

### Configuration Files
| File | Purpose |
|------|---------|
| package.json | Dependencies |
| tsconfig.json | TypeScript |
| Dockerfile | Container |
| .github/workflows/ci.yml | CI |

### Build Commands
| Command | Purpose |
|---------|---------|
| npm run build | Production build |
| npm run test | Run tests |
| npm run dev | Development mode |

### Verified
- [ ] Project compiles (empty)
- [ ] Linting passes
- [ ] CI pipeline runs
- [ ] Documentation accessible

---

**Do you approve Phase 7? Ready to proceed to Test Development?**
```
