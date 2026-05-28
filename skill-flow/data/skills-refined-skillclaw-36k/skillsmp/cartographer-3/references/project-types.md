# Project Type Detection Heuristics

This reference defines how to detect the primary project type from codebase signals.

## Project Types

| Type | Description |
|------|-------------|
| `frontend_spa` | Single-page application (React, Vue, Angular, Svelte) |
| `backend_api` | Server-side API application (Express, FastAPI, Django, etc.) |
| `fullstack` | Combined frontend and backend in single codebase |
| `monorepo` | Multiple packages/apps in single repository |
| `cli` | Command-line interface tool |
| `library` | Reusable package/library for other projects |
| `mobile` | Native or hybrid mobile application |
| `static_site` | Static site generator (Next.js SSG, Gatsby, Hugo) |

---

## Detection Signals

### Frontend SPA

**Primary Signals (HIGH confidence):**
- `package.json` contains `react`, `vue`, `@angular/core`, or `svelte`
- Presence of `vite.config.*`, `next.config.*`, `webpack.config.*`
- `src/App.tsx`, `src/App.vue`, `src/app/app.component.ts`
- `public/index.html` with SPA mounting point

**Secondary Signals (MEDIUM confidence):**
- `src/components/` directory
- `src/pages/` or `app/` directories
- State management deps: `redux`, `vuex`, `@ngrx/store`, `zustand`
- Routing deps: `react-router`, `vue-router`, `@angular/router`

**Disqualifying Signals:**
- `routes/`, `controllers/`, `services/` directories (suggests backend)
- Database deps: `prisma`, `typeorm`, `sequelize`, `mongoose`

---

### Backend API

**Primary Signals (HIGH confidence):**
- `package.json` contains `express`, `fastify`, `@nestjs/core`, `koa`, `hapi`
- `requirements.txt` or `pyproject.toml` with `flask`, `django`, `fastapi`
- `go.mod` with HTTP server packages (`gin`, `echo`, `fiber`)
- `Cargo.toml` with web framework (`actix-web`, `axum`, `rocket`)

**Secondary Signals (MEDIUM confidence):**
- `src/routes/`, `src/controllers/`, `src/services/` directories
- Database deps or ORM presence
- `prisma/schema.prisma`, `migrations/` directory
- API documentation: `openapi.yaml`, `swagger.json`

**Disqualifying Signals:**
- UI framework deps (React, Vue, etc.)
- `src/components/` directory

---

### Fullstack

**Primary Signals (HIGH confidence):**
- Both frontend and backend signals present at top level
- `client/` and `server/` directories
- `frontend/` and `backend/` directories
- Next.js with `api/` routes + pages

**Detection Logic:**
```
IF (frontend_signals >= 2) AND (backend_signals >= 2)
  AND NOT (monorepo_structure)
  THEN type = fullstack
```

---

### Monorepo

**Primary Signals (HIGH confidence):**
- Multiple `package.json` files at different levels
- `packages/`, `apps/`, `libs/` directories
- Build orchestration: `turbo.json`, `nx.json`, `lerna.json`, `pnpm-workspace.yaml`
- Workspace config in root `package.json`

**Secondary Signals (MEDIUM confidence):**
- `workspaces` field in `package.json`
- Cross-package references in dependencies
- Shared config files at root

**Sub-type Detection:**
After identifying monorepo, classify each package:
- Scan each package directory independently
- Record per-package type (frontend, backend, library, etc.)

---

### CLI

**Primary Signals (HIGH confidence):**
- `bin/` directory with executable entries
- `package.json` with `bin` field
- CLI deps: `commander`, `yargs`, `chalk`, `inquirer`, `clap`, `structopt`
- Single entry point pattern (`cli.ts`, `main.ts`, `index.ts`)

**Secondary Signals (MEDIUM confidence):**
- No UI framework deps
- Minimal directory structure
- Heavy use of process/stdin/stdout utilities

---

### Library

**Primary Signals (HIGH confidence):**
- `package.json` with `main`, `module`, `exports` fields
- `tsconfig.json` with `declaration: true`
- `src/index.ts` as primary export
- No `start` script or minimal scripts
- Published to npm (check `private: false`)

**Secondary Signals (MEDIUM confidence):**
- Comprehensive `exports` field
- Build output to `dist/`, `lib/`, `build/`
- Types generation (`*.d.ts` files)
- Multiple entry points

---

### Mobile

**Primary Signals (HIGH confidence):**
- `ios/` and `android/` directories (React Native, Flutter)
- `capacitor.config.*`, `ionic.config.json` (Ionic/Capacitor)
- `app.json` with expo config (Expo)
- `pubspec.yaml` with Flutter deps

**Secondary Signals (MEDIUM confidence):**
- Mobile-specific deps: `react-native`, `expo`, `@capacitor/core`
- Platform-specific code: `*.ios.ts`, `*.android.ts`

---

### Static Site

**Primary Signals (HIGH confidence):**
- `gatsby-config.js` (Gatsby)
- `hugo.toml`, `config.toml` with Hugo markers
- `_config.yml` with Jekyll markers
- `astro.config.mjs` (Astro)
- Next.js with `output: 'export'` or primarily static content

**Secondary Signals (MEDIUM confidence):**
- `content/`, `posts/`, `articles/` directories
- Markdown-heavy structure
- Static output directory: `_site/`, `public/`, `dist/`

---

## Detection Algorithm

```
function detectProjectType(codebase):
    signals = collectSignals(codebase)

    # Check for monorepo first (takes precedence)
    if signals.monorepo >= HIGH_THRESHOLD:
        return "monorepo"

    # Score each type
    scores = {
        "frontend_spa": scoreType(signals, FRONTEND_WEIGHTS),
        "backend_api": scoreType(signals, BACKEND_WEIGHTS),
        "fullstack": scoreType(signals, FULLSTACK_WEIGHTS),
        "cli": scoreType(signals, CLI_WEIGHTS),
        "library": scoreType(signals, LIBRARY_WEIGHTS),
        "mobile": scoreType(signals, MOBILE_WEIGHTS),
        "static_site": scoreType(signals, STATIC_WEIGHTS)
    }

    # Apply disqualifying signals
    for type, disqualifiers in DISQUALIFIERS:
        if any(d in signals for d in disqualifiers):
            scores[type] *= 0.5

    return maxScore(scores)
```

---

## Confidence Thresholds

| Confidence | Score Range | Action |
|------------|-------------|--------|
| HIGH | >= 0.8 | Auto-classify, no confirmation needed |
| MEDIUM | 0.5 - 0.8 | Auto-classify, note in observations |
| LOW | < 0.5 | Prompt user for confirmation |

---

## Edge Cases

### Hybrid Projects
Some projects don't fit cleanly:
- **Electron apps**: Classify as `frontend_spa` with note about Electron
- **SSR frameworks**: Classify based on primary use (static vs dynamic)
- **BFF patterns**: Classify as `fullstack` or note in observations

### Ambiguous Signals
When signals conflict:
1. Prioritize explicit config over inferred patterns
2. Check README/docs for project description
3. Fall back to user confirmation if LOW confidence
