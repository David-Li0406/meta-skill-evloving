# CLAUDE.md Template

Template for generating the root `CLAUDE.md` file.

## Preservation Note

**Before generating**: Check if a CLAUDE.md already exists. If it does:
- Preserve any project-specific sections that are accurate and valuable
- Update outdated commands or descriptions
- Merge new content rather than replacing wholesale
- Keep custom sections the team has added

Only replace entirely if the existing file is significantly wrong or poorly organized.

## Structure

```markdown
# {Project Name}

## CRITICAL: Before You Start

**ALWAYS consult the `docs/` folder before making changes or answering questions about this project.**

Documentation is the source of truth for:
- Architectural decisions → `docs/architecture/`
- Coding standards → `docs/standards/`
- Getting started → `docs/onboarding/`

Use **progressive disclosure**: read high-level overviews first, then drill into specific docs as needed. Never assume patterns or conventions—verify in docs first.

## Project Summary

{2-3 line description of what the project does, its primary purpose, and key technologies.}

## Quick Start

{Commands discovered from project config files}

### Development

```bash
{install command}
{dev server command}
```

### Testing

```bash
{test command}
{lint command}
```

### Building

```bash
{build command}
```

## Documentation

### Architecture
- [`docs/architecture/01-overview.md`](docs/architecture/01-overview.md) — System overview and high-level design
- [`docs/architecture/02-directory-structure.md`](docs/architecture/02-directory-structure.md) — Repository layout
- [`docs/architecture/03-core-components.md`](docs/architecture/03-core-components.md) — Main modules and responsibilities
- [`docs/architecture/04-data-flow.md`](docs/architecture/04-data-flow.md) — Data flow and integration points

### Standards
- [`docs/standards/naming-conventions.md`](docs/standards/naming-conventions.md) — Naming patterns
- [`docs/standards/error-handling.md`](docs/standards/error-handling.md) — Error handling patterns
- [`docs/standards/testing.md`](docs/standards/testing.md) — Testing conventions
{Additional standards as detected}

### Onboarding
- [`docs/onboarding/01-setup.md`](docs/onboarding/01-setup.md) — Environment setup
- [`docs/onboarding/02-first-contribution.md`](docs/onboarding/02-first-contribution.md) — Making your first change

## Before Marking Work Complete

- Run tests: `{test command}`
- Run linter: `{lint command}`
- Ensure all checks pass before committing
```

## Command Discovery Patterns

### Priority Order

1. **justfile** (highest priority)
   ```bash
   # Check for justfile
   if [ -f "justfile" ] || [ -f "Justfile" ]; then
     # Use just commands
     just --list  # Discover available commands
   fi
   ```

2. **package.json with packageManager**
   ```json
   {
     "packageManager": "pnpm@8.0.0"  // Use pnpm
     "packageManager": "yarn@4.0.0"  // Use yarn
     "packageManager": "bun@1.0.0"   // Use bun
   }
   ```

3. **Makefile**
   ```bash
   if [ -f "Makefile" ]; then
     # Extract targets
     make help  # or grep for targets
   fi
   ```

4. **Default by ecosystem**
   - Node.js: Check for lock files (pnpm-lock.yaml → pnpm, yarn.lock → yarn, package-lock.json → npm)
   - Python: Check for pyproject.toml (poetry), requirements.txt (pip)
   - Rust: cargo
   - Go: go

### Common Commands to Discover

| Purpose | Check For |
|---------|-----------|
| Install | `install`, `setup`, `bootstrap` |
| Dev | `dev`, `start`, `serve`, `watch` |
| Build | `build`, `compile`, `dist` |
| Test | `test`, `spec`, `check` |
| Lint | `lint`, `format`, `check` |

### Example Discoveries

**Node.js with pnpm:**
```markdown
### Development
```bash
pnpm install
pnpm dev
```

### Testing
```bash
pnpm test
pnpm lint
```
```

**Rust with cargo:**
```markdown
### Development
```bash
cargo build
cargo run
```

### Testing
```bash
cargo test
cargo clippy
```
```

**Python with poetry:**
```markdown
### Development
```bash
poetry install
poetry run python main.py
```

### Testing
```bash
poetry run pytest
poetry run ruff check .
```
```

## CRITICAL Section Guidelines

The CRITICAL section must:

1. Be near the top of the file (right after title)
2. Explicitly instruct to consult docs before acting
3. List what each docs subfolder contains
4. Mention progressive disclosure pattern
5. Emphasize verification over assumption

**Bad examples (avoid):**
```markdown
# CRITICAL
Read the docs.
```

```markdown
## Important
Check docs/standards for conventions.
```

**Good example:**
```markdown
## CRITICAL: Before You Start

**ALWAYS consult the `docs/` folder before making changes or answering questions about this project.**

Documentation is the source of truth for:
- Architectural decisions → `docs/architecture/`
- Coding standards → `docs/standards/`
- Getting started → `docs/onboarding/`

Use **progressive disclosure**: read high-level overviews first, then drill into specific docs as needed. Never assume patterns or conventions—verify in docs first.
```

## Table of Contents Guidelines

- Group by category (Architecture, Standards, Onboarding)
- Use relative links: `[title](docs/path/file.md)`
- Include brief description after each link
- Keep descriptions to one line
- Order matches logical reading order
