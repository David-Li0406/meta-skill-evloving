# Tech Stack Skills Reference

This reference maps technologies to recommended skills.

## How to Use

1. Detect project tech stack (from config files or interview)
2. Look up recommended skills for each technology
3. Present recommendations to user
4. Install selected skills

---

## Frontend Skills

### React / Next.js

| Skill | Source | Description |
|-------|--------|-------------|
| react-best-practices | cc-guide/skills | React and Next.js performance patterns |
| tailwind-shadcn | cc-guide/skills | Tailwind CSS and shadcn/ui patterns |

**Detection:**
- `next.config.js` or `next.config.mjs` → Next.js
- `package.json` has `react` → React

### Vue.js

| Skill | Source | Description |
|-------|--------|-------------|
| vue-patterns | skills.sh | Vue 3 composition API patterns |

**Detection:**
- `package.json` has `vue`

### Svelte / SvelteKit

| Skill | Source | Description |
|-------|--------|-------------|
| svelte-patterns | skills.sh | Svelte and SvelteKit patterns |

**Detection:**
- `svelte.config.js` exists
- `package.json` has `svelte`

### Angular

| Skill | Source | Description |
|-------|--------|-------------|
| angular-patterns | skills.sh | Angular best practices |

**Detection:**
- `angular.json` exists
- `package.json` has `@angular/core`

---

## Backend Skills

### Node.js / Express / Fastify

| Skill | Source | Description |
|-------|--------|-------------|
| node-backend | skills.sh | Node.js backend patterns |

**Detection:**
- `package.json` has `express` or `fastify`

### Python / FastAPI

| Skill | Source | Description |
|-------|--------|-------------|
| python-api | skills.sh | FastAPI/Flask patterns |

**Detection:**
- `pyproject.toml` or `requirements.txt` has `fastapi` or `flask`

### Go

| Skill | Source | Description |
|-------|--------|-------------|
| go-patterns | skills.sh | Go idioms and patterns |

**Detection:**
- `go.mod` exists

### Rust

| Skill | Source | Description |
|-------|--------|-------------|
| rust-patterns | skills.sh | Rust best practices |

**Detection:**
- `Cargo.toml` exists

---

## Database Skills

### Convex

| Skill | Source | Description |
|-------|--------|-------------|
| convex-patterns | cc-guide/skills | Convex queries, mutations, real-time |

**Detection:**
- `convex/` directory exists
- `package.json` has `convex`

### Prisma

| Skill | Source | Description |
|-------|--------|-------------|
| prisma-patterns | skills.sh | Prisma ORM patterns |

**Detection:**
- `prisma/schema.prisma` exists
- `package.json` has `prisma`

### Drizzle

| Skill | Source | Description |
|-------|--------|-------------|
| drizzle-patterns | skills.sh | Drizzle ORM patterns |

**Detection:**
- `drizzle.config.ts` exists
- `package.json` has `drizzle-orm`

### SQL

| Skill | Source | Description |
|-------|--------|-------------|
| sql-patterns | skills.sh | SQL query optimization |

**Detection:**
- Generic, suggest for any DB project

---

## DevOps Skills

### Git

| Skill | Source | Description |
|-------|--------|-------------|
| git-workflow | cc-guide/skills | Git conventions for this project |

**Detection:**
- `.git/` exists (always recommend)

### Docker

| Skill | Source | Description |
|-------|--------|-------------|
| docker-patterns | skills.sh | Docker and container patterns |

**Detection:**
- `Dockerfile` exists
- `docker-compose.yml` exists

### GitHub Actions

| Skill | Source | Description |
|-------|--------|-------------|
| github-actions | skills.sh | CI/CD workflow patterns |

**Detection:**
- `.github/workflows/` exists

### Vercel

| Skill | Source | Description |
|-------|--------|-------------|
| vercel-patterns | skills.sh | Vercel deployment patterns |

**Detection:**
- `vercel.json` exists
- Project appears to be Next.js

---

## Testing Skills

### Jest

| Skill | Source | Description |
|-------|--------|-------------|
| jest-patterns | skills.sh | Jest testing patterns |

**Detection:**
- `jest.config.js` exists
- `package.json` has `jest`

### Vitest

| Skill | Source | Description |
|-------|--------|-------------|
| vitest-patterns | skills.sh | Vitest testing patterns |

**Detection:**
- `vitest.config.ts` exists
- `package.json` has `vitest`

### Playwright

| Skill | Source | Description |
|-------|--------|-------------|
| playwright-patterns | skills.sh | E2E testing with Playwright |

**Detection:**
- `playwright.config.ts` exists
- `package.json` has `@playwright/test`

### pytest

| Skill | Source | Description |
|-------|--------|-------------|
| pytest-patterns | skills.sh | Python testing patterns |

**Detection:**
- `pytest.ini` or `pyproject.toml` has pytest config
- `requirements.txt` has `pytest`

---

## Quick Lookup Table

| If you detect... | Recommend... |
|------------------|--------------|
| Next.js | react-best-practices, tailwind-shadcn, git-workflow |
| React (Vite) | react-best-practices, git-workflow |
| Vue | vue-patterns, git-workflow |
| Svelte | svelte-patterns, git-workflow |
| Express | node-backend, git-workflow |
| FastAPI | python-api, git-workflow |
| Go | go-patterns, git-workflow |
| Rust | rust-patterns, git-workflow |
| Convex | convex-patterns |
| Prisma | prisma-patterns |
| Docker | docker-patterns |
| Playwright | playwright-patterns |

---

## Detection Code

```bash
# Quick detection script
detect_stack() {
  local skills=()

  # Always recommend
  skills+=("git-workflow")

  # Frontend
  [ -f "next.config.js" ] || [ -f "next.config.mjs" ] && skills+=("react-best-practices" "tailwind-shadcn")
  grep -q '"vue"' package.json 2>/dev/null && skills+=("vue-patterns")
  [ -f "svelte.config.js" ] && skills+=("svelte-patterns")
  [ -f "angular.json" ] && skills+=("angular-patterns")

  # Backend
  grep -q '"express"\|"fastify"' package.json 2>/dev/null && skills+=("node-backend")
  grep -q "fastapi\|flask" requirements.txt pyproject.toml 2>/dev/null && skills+=("python-api")
  [ -f "go.mod" ] && skills+=("go-patterns")
  [ -f "Cargo.toml" ] && skills+=("rust-patterns")

  # Database
  [ -d "convex" ] && skills+=("convex-patterns")
  [ -f "prisma/schema.prisma" ] && skills+=("prisma-patterns")
  [ -f "drizzle.config.ts" ] && skills+=("drizzle-patterns")

  # DevOps
  [ -f "Dockerfile" ] && skills+=("docker-patterns")
  [ -d ".github/workflows" ] && skills+=("github-actions")

  # Testing
  [ -f "playwright.config.ts" ] && skills+=("playwright-patterns")

  echo "${skills[@]}"
}
```

---

## Presentation Template

```
Based on your project's tech stack, I recommend these skills:

Detected: Next.js + TypeScript + Tailwind CSS + Convex

Recommended Skills:
1. react-best-practices
   React and Next.js performance optimization patterns

2. tailwind-shadcn
   Tailwind CSS and shadcn/ui component patterns

3. convex-patterns
   Convex database queries, mutations, and real-time subscriptions

4. git-workflow
   Git conventions for consistent commits and PRs

Would you like to install all recommended skills?
```
