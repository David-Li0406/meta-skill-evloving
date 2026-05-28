# Supported Frameworks Reference

Detailed detection patterns for each supported framework.

## JavaScript/TypeScript Frameworks

### Next.js
**Detection files:**
- `next.config.js`
- `next.config.mjs`
- `next.config.ts`

**Project type:** fullstack

**Typical structure:**
```
├── app/              # App Router (Next.js 13+)
├── pages/            # Pages Router (legacy)
├── components/
├── lib/
├── public/
└── package.json
```

**Default commands:**
```yaml
test: "npm test" or "jest"
lint: "npm run lint" or "next lint"
build: "npm run build" or "next build"
dev: "npm run dev" or "next dev"
typecheck: "tsc --noEmit"
```

### Vite
**Detection files:**
- `vite.config.js`
- `vite.config.ts`

**Project type:** frontend

**Typical structure:**
```
├── src/
│   ├── components/
│   ├── pages/
│   └── main.tsx
├── public/
└── package.json
```

### Nuxt
**Detection files:**
- `nuxt.config.ts`
- `nuxt.config.js`

**Project type:** fullstack

### Astro
**Detection files:**
- `astro.config.mjs`
- `astro.config.ts`

**Project type:** frontend

### SvelteKit
**Detection files:**
- `svelte.config.js`

**Project type:** fullstack

## Python Frameworks

### Django
**Detection files:**
- `manage.py` + `settings.py`
- `django` in pyproject.toml dependencies

**Project type:** backend

**Default commands:**
```yaml
test: "python manage.py test"
lint: "ruff check ." or "flake8"
dev: "python manage.py runserver"
typecheck: "mypy ."
```

### FastAPI
**Detection files:**
- `fastapi` in pyproject.toml dependencies

**Project type:** backend

**Default commands:**
```yaml
test: "pytest"
lint: "ruff check ."
dev: "uvicorn main:app --reload"
typecheck: "mypy ."
```

### Flask
**Detection files:**
- `flask` in pyproject.toml dependencies

**Project type:** backend

## Go Projects

**Detection files:**
- `go.mod`

**Project type:** backend

**Default commands:**
```yaml
test: "go test ./..."
lint: "golangci-lint run"
build: "go build ./..."
```

## Rust Projects

**Detection files:**
- `Cargo.toml`

**Project type:** varies (check for web frameworks)

**Web framework detection:**
- `actix-web` in Cargo.toml → backend
- `axum` in Cargo.toml → backend
- `rocket` in Cargo.toml → backend

**Default commands:**
```yaml
test: "cargo test"
lint: "cargo clippy"
build: "cargo build"
```

## Package Manager Detection

| Lock File | Package Manager |
|-----------|-----------------|
| `pnpm-lock.yaml` | pnpm |
| `yarn.lock` | yarn |
| `bun.lockb` | bun |
| `package-lock.json` | npm |
| (no lock file) | npm (default) |

## Adding New Framework Support

To add detection for a new framework:

1. Identify unique config files
2. Determine project type (frontend/backend/fullstack)
3. Map standard commands
4. Update `scripts/detect-project.sh`
5. Add to this reference document
