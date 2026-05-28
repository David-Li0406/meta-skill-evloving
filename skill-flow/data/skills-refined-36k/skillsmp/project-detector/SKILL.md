---
name: project-detector
description: >
  This skill should be used when the user asks to "detect project type",
  "analyze this project", "create project profile", "what tech stack is this",
  "scan project structure", "what database does this use", or when autonomous development starts in a new codebase.
  Detects package.json, pyproject.toml, go.mod, Cargo.toml to identify the technology stack.
  Also detects database providers (Supabase, Firebase, Prisma, etc.) and MCP availability.
---

# Project Detection Skill

Analyze the current directory and create `.claude/project-profile.yaml` to enable autonomous development workflows.

## Protocol

### Step 1: Check Existing Profile

Check if `.claude/project-profile.yaml` exists:
- If exists and is less than 1 day old → read and summarize it
- Otherwise → create or update it

### Step 2: Detect Package Manager and Language

Scan for project files:
```bash
ls package.json pyproject.toml go.mod Cargo.toml pom.xml 2>/dev/null
```

Identify the primary language based on which file exists.

### Step 3: Detect Framework

Look for framework-specific config files:

| Config File | Framework |
|-------------|-----------|
| `next.config.*` | Next.js |
| `vite.config.*` | Vite |
| `nuxt.config.*` | Nuxt |
| `astro.config.*` | Astro |
| `settings.py` + `manage.py` | Django |
| `Cargo.toml` with actix/axum | Rust web |

### Step 4: Extract Commands

Parse package.json scripts or detect standard commands:
- `test` - Testing command
- `lint` - Linting command
- `typecheck` - Type checking command
- `build` - Build command
- `dev` - Development server

### Step 5: Detect Database Provider (NEW)

Check for database dependencies in package.json, pyproject.toml, or config files:

| Dependency/Config | Provider |
|-------------------|----------|
| `@supabase/supabase-js` | Supabase |
| `firebase` or `firebase-admin` | Firebase |
| `prisma/` folder or `@prisma/client` | Prisma |
| `drizzle.config.ts` | Drizzle |
| `@planetscale/database` | PlanetScale |
| `@neondatabase/serverless` | Neon |
| `mongodb` or `mongoose` | MongoDB |
| `pg` or `postgres` | PostgreSQL |
| `mysql2` | MySQL |
| `better-sqlite3` | SQLite |

Also check for MCP availability:
- If Supabase detected → check if `mcp__supabase__*` tools are available
- MCP enables real-time schema validation

### Step 6: Identify Directory Patterns

Scan directory structure to find:
- Component locations
- API route locations
- Test file locations
- Source code organization

### Step 7: Write Profile

Write detected information to `.claude/project-profile.yaml` with structure:
```yaml
project:
  name: ""
  type: ""  # frontend, backend, fullstack
stack:
  language: ""
  framework: ""
database:
  provider: ""  # supabase, firebase, prisma, drizzle, planetscale, neon, mongodb, postgres, mysql, sqlite, none
  orm: ""       # prisma, drizzle, typeorm, mongoose, kysely, none
  mcp_available: false  # true if MCP tools detected for this provider
  schema_source: ""     # mcp, prisma/schema.prisma, drizzle/schema.ts, manual
commands:
  test: ""
  lint: ""
  typecheck: ""
  build: ""
verification:
  required: []
  optional: []
```

### Step 8: Summarize

Present detected configuration to the user for confirmation.

If database with MCP is detected, inform the user:
- Schema validation will use real-time MCP queries
- Type mismatches will be caught automatically
- RLS policies will be verified (Supabase)

## Additional Resources

### Reference Files

For detailed detection patterns:
- **`references/supported-frameworks.md`** - Complete list of supported frameworks with detection patterns
- **`references/database-providers.md`** - Database provider detection patterns and MCP integration

### Example Files

Working examples in `examples/`:
- **`project-profile-nextjs.yaml`** - Example profile for a Next.js project

### Script Reference

Run the detection script directly:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/detect-project.sh
```

## When NOT to Use This Skill

Do NOT use this skill when:

1. **Profile already exists and is recent** - Skip if less than 1 day old
2. **Empty directory** - No project to detect
3. **Non-project directories** - Home folders, system directories, etc.
4. **User explicitly provides tech stack** - Trust user input over detection
5. **Monorepo sub-packages** - Detect from root, not from individual packages

## Quality Standards

1. **ALWAYS** check for existing profile before regenerating
2. **NEVER** overwrite user-customized profile fields without confirmation
3. **ALWAYS** detect database provider if dependencies exist
4. **ALWAYS** check for MCP availability when database detected
5. **PRIORITIZE** parsing package.json/pyproject.toml over guessing
