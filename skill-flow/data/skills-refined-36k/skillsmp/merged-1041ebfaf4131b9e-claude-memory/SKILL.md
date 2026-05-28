---
name: claude-memory
description: Create and optimize CLAUDE.md memory files or .claude/rules/ modular rules for Claude Code projects. Use this skill when setting up new projects or improving Claude Code's context awareness.
---

# Objective
Master the creation of effective Claude Code memory systems using either CLAUDE.md files or the modular `.claude/rules/` directory. This skill covers file hierarchy, content structure, path-scoped rules, formatting, emphasis techniques, and common anti-patterns to avoid.

Memory files are automatically loaded at session startup, consuming tokens from your 200k context window. Every instruction competes with Claude Code's ~50 built-in instructions, leaving ~100-150 effective instruction slots for your customizations.

**Two approaches available:**

- **CLAUDE.md** - Single file, simpler, best for small projects
- **.claude/rules/** - Modular files with optional path-scoping, best for large projects

# Quick Start

## Bootstrap New Project
Run `/init` in Claude Code to auto-generate a CLAUDE.md with project structure.

Or create manually at project root:

```markdown
# Project Name

## Tech Stack

- [Primary language/framework]
- [Key libraries]

## Commands

- `npm run dev` - Start development
- `npm test` - Run tests
- `npm run build` - Build for production

## Code Conventions

- [2-3 critical conventions]

## Important Context

- [1-2 architectural decisions worth knowing]
```

## Quick Add Memory
Press `#` during a Claude Code session to quickly add new memory items without editing the file directly.

## Edit Memory
Use `/memory` command to open CLAUDE.md in your system editor.

# File Hierarchy
Claude Code loads CLAUDE.md files in a specific order. Higher priority files are loaded first and take precedence.

## Loading Order
| Priority | Location | Purpose | Scope |
|----------|----------|---------|-------|
| 1 (Highest) | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | Enterprise policy (managed by IT) | All org users |
| 2 | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Project memory (git-tracked) | Team via git |
| 2 | `./.claude/rules/*.md` | Modular rules (git-tracked) | Team via git |
| 3 | `~/.claude/CLAUDE.md` | User preferences (global) | All your projects |
| 3 | `~/.claude/rules/*.md` | Personal modular rules (global) | All your projects |
| 4 (Lowest) | `./CLAUDE.local.md` | Personal project prefs (auto-gitignored) | Just you |

## Recursive Loading
Claude recurses UP from current directory to root, loading all CLAUDE.md files found.

Running Claude in `foo/bar/` loads:

1. `foo/bar/CLAUDE.md`
2. `foo/CLAUDE.md`
3. Root-level files

Claude also discovers CLAUDE.md in SUBTREES when reading files in those directories.

## Monorepo Strategy
For monorepos, use layered approach:

```
root/
├── CLAUDE.md              # Universal: tech stack, git workflow
├── apps/
│   ├── web/CLAUDE.md      # Frontend-specific patterns
│   └── api/CLAUDE.md      # Backend-specific patterns
└── packages/
    └── shared/CLAUDE.md   # Shared library conventions
```

Root file defines WHEN to use patterns; subtree files define HOW.

# Rules Directory
The `.claude/rules/` directory provides a **modular alternative** to monolithic CLAUDE.md files. Instead of one large file, you organize instructions into multiple focused markdown files.

## When to Use Rules
**Use `.claude/rules/` when:**

- Project has many distinct concerns (testing, security, API, frontend)
- Different rules apply to different file types
- Team members maintain different areas
- You want to update one concern without touching others

**Use CLAUDE.md when:**

- Project is small/simple
- All rules are universal
- You prefer a single source of truth

## Rules Structure
```
.claude/rules/
├── code-style.md      # Formatting and conventions
├── testing.md         # Test requirements
├── security.md        # Security checklist
├── frontend/
│   ├── react.md       # React-specific patterns
│   └── styles.md      # CSS conventions
└── backend/
    ├── api.md         # API development rules
    └── database.md    # Database conventions
```

**Key points:**

- All `.md` files are discovered recursively
- No imports or configuration needed
- Same priority as CLAUDE.md
- Supports symlinks for sharing rules across projects

## Path Scoped Rules
Rules can be scoped to specific files using YAML frontmatter:

```yaml
---
paths: src/api/**/*.ts
---
# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
```

**Path patterns supported:**

| Pattern                | Matches                                    |
| ---------------------- | ------------------------------------------ |
| `**/*.ts`              | All TypeScript files in any directory      |
| `src/**/*`             | All files under `src/` directory           |
| `src/components/*.tsx` | React components in specific directory     |
| `src/**/*.{ts,tsx}`    | TypeScript and TSX files (brace expansion) |
| `{src,lib}/**/*.ts`    | Files in multiple directories              |

**Rules without `paths` frontmatter** load unconditionally for all files.

## User Level Rules
Create personal rules that apply to all your projects:

```
~/.claude/rules/
├── preferences.md    # Your coding preferences
├── workflows.md      # Your preferred workflows
└── git.md            # Your git conventions
```

User-level rules load before project rules, giving project rules higher priority for overrides.

## Symlinks Support
Share common rules across multiple projects using symlinks:

```bash
# Symlink a shared rules directory
ln -s ~/shared-claude-rules .claude/rules/shared

# Symlink individual rule files
ln -s ~/company-standards/security.md .claude/rules/security.md
```

Circular symlinks are detected and handled gracefully.

# Content Framework
Structure your CLAUDE.md using the WHAT-WHY-HOW framework:

**WHAT** - Project Context: Tech stack, directory structure, architecture  
**WHY** - Purpose: Architectural decisions, why patterns exist  
**HOW** - Workflow: Commands, testing, git workflow, verification steps  

```markdown
## Tech Stack

- Next.js 15 with App Router
- PostgreSQL via Prisma ORM

## Architecture Decisions

- Server Components for data fetching
- All forms use TanStack Form

## Commands

- `pnpm dev` - Start dev server
- `pnpm test:ci` - Run tests
- `pnpm build` - Production build

## Git Workflow

- Branch: `feature/name` or `fix/name`
- Run tests before committing
```

# Emphasis Techniques
Claude follows emphasized instructions more reliably. Use these techniques strategically for critical rules.

## Keyword Hierarchy
Use emphasis keywords in order of severity:

| Keyword       | Use For               | Example                                      |
| ------------- | --------------------- | -------------------------------------------- |
| **CRITICAL**  | Non-negotiable rules  | `**CRITICAL**: Never commit secrets`         |
| **NEVER**     | Absolute prohibitions | `NEVER: Push directly to main`               |
| **ALWAYS**    | Mandatory behaviors   | `ALWAYS: Run tests before pushing`           |
| **IMPORTANT** | Significant guidance  | `IMPORTANT: Keep components under 300 lines` |
| **YOU MUST**  | Explicit requirements | `YOU MUST: Use TanStack Form for forms`      |

## Formatting Patterns
**Bold + CRITICAL keyword:**

```markdown
**CRITICAL**: Always run tests before pushing code
```

**Capitalized emphasis:**

```markdown
IMPORTANT: Do not commit environment variables
YOU MUST: Follow the git workflow outlined below
NEVER: Include API keys in code
ALWAYS: Use TypeScript strict mode
```

**Strikethrough for forbidden options:**

```markdown
- `pnpm test:ci` - Run tests (use this)
- ~~`pnpm test`~~ - NEVER use (interactive mode)
```

**Visual markers (use sparingly):**

```markdown
⚠️ WARNING: This affects production data
🔒 SECURITY: Never commit secrets to git
```

# Placement Strategy
Order matters. Claude pays more attention to:

1. **First items** in each section (put critical rules first)
2. **Repeated items** across sections (repeat critical rules in context)
3. **Emphasized items** with CRITICAL/NEVER/ALWAYS keywords

Structure your file with critical rules first:

```markdown
## Code Conventions

### Critical Rules

- **NEVER** commit .env files
- **ALWAYS** run tests before pushing
- **CRITICAL**: Use TanStack Form for ALL forms

### General Guidelines

- Prefer Server Components
- Keep components under 300 lines
```

# Writing Effective Instructions
## Golden Rule
Show your CLAUDE.md to someone with minimal project context. If they're confused, Claude will be too.

## Be Specific
Vague instructions cause inconsistent behavior:

```markdown
❌ VAGUE:

- Format code properly
- Write good tests
- Follow best practices

✅ SPECIFIC:

- Run `pnpm lint` before committing (Prettier configured)
- Write tests in `__tests__/` using Vitest
- Use TanStack Form for all forms (see `src/features/form/`)
```

## Show Don't Tell
When format matters, show examples:

```markdown
❌ TELLING:
Use conventional commits with type and description.

✅ SHOWING:

## Commit Format
```

feat(auth): implement JWT authentication

Add login endpoint and token validation

```
Types: feat, fix, refactor, docs, test, chore
```

## Eliminate Ambiguity
Replace vague phrases with clear directives:

| Ambiguous            | Clear Alternative                   |
| -------------------- | ----------------------------------- |
| "Try to..."          | "Always..." or "Never..."           |
| "Should probably..." | "Must..." or "May optionally..."    |
| "Generally..."       | "Always... except when [condition]" |
| "Consider..."        | "If [condition], then [action]"     |

## Define Edge Cases
Anticipate questions and answer them:

```markdown
❌ INCOMPLETE:
Run tests before pushing.

✅ COMPLETE:

## Testing

- Run `pnpm test:ci` before pushing
- If tests fail, fix before committing
- New features require tests in `__tests__/`
- Minimum 80% coverage for new code
```

## Provide Decision Criteria
When Claude must make choices, give criteria:

```markdown
## Component Choice

**Use Server Component when:**

- Data fetching only
- No user interaction needed

**Use Client Component when:**

- User interaction required
- Browser APIs needed (localStorage, window)
```

## Separate Obligation Levels
Clearly distinguish requirements from suggestions:

```markdown
## API Development

### Must Have

- Input validation with Zod
- Error handling for all endpoints

### Nice to Have

- Pagination for list endpoints
- Caching headers

### Must Not

- Expose internal errors to clients
- Log sensitive data
```

# Size Constraints
## Limits

- **Ideal**: 100-200 lines maximum
- **Practical max**: 300 lines before splitting
- **Universal items**: Under 60 lines

**Why these limits matter:**

- Claude reliably follows ~150-200 total instructions
- Claude Code's system prompt uses ~50 instructions
- Leaves ~100-150 slots for YOUR instructions
- Irrelevant content degrades instruction-following

## Scaling Strategy
When exceeding limits:

1. Move task-specific details to separate files
2. Link from CLAUDE.md with descriptions
3. Use progressive disclosure pattern

```markdown
## Detailed Guides

- **API Routes**: See [docs/api-patterns.md](docs/api-patterns.md)
- **Testing**: See [docs/testing-guide.md](docs/testing-guide.md)
- **Deployment**: See [docs/deployment.md](docs/deployment.md)
```

# Imports Feature
CLAUDE.md supports importing other markdown files:

```markdown
## External References

@docs/coding-standards.md
@~/.claude/my-global-preferences.md
@./team-conventions.md
```

## Import Rules

- Supports relative and absolute paths
- Home directory expansion with `~`
- Recursive imports up to 5 levels deep
- NOT evaluated inside code blocks or backticks

# Anti-Patterns
## Never Include
**Code Style Rules** - Use linters instead (LLMs are expensive, linters are free)

**Secrets** - NEVER include API keys, database URLs, tokens, credentials

**Too Much Content** - Link to docs instead of embedding 500+ lines

**Extensive Code** - Reference files instead (code examples become outdated)

**Vague Instructions** - Be specific.

## Examples What to Avoid
```markdown
❌ BAD:

- Use 2-space indentation (use Prettier instead)
- DATABASE_URL=postgresql://... (never include secrets)
- [500 lines of API docs] (link to external file)
- Format code properly (too vague)

✅ GOOD:

- ESLint/Prettier configured (see .eslintrc)
- Credentials in `.env` (never committed)
- API guide: See [docs/api.md](docs/api.md)
- Run `pnpm lint` before committing
```

# Workflow
## Decision Point
**ALWAYS ASK FIRST: Storage Strategy**

Before creating or updating memory files, ask the user:

> Do you want to use a single CLAUDE.md file or split into separate `.claude/rules/` files?
>
> **Option 1: Single CLAUDE.md** - All instructions in one file (simpler, best for small projects)
> **Option 2: Modular .claude/rules/** - Split by concern with optional path-scoping (better for large projects)

Use AskUserQuestion to present these options before proceeding.

**Decision guide:**

- **Choose CLAUDE.md** if: < 100 lines of instructions, simple project, universal rules
- **Choose .claude/rules/** if: 100+ lines, multiple file types with different rules, team maintains different areas

## Creating New Memory (CLAUDE.md approach)
1. Start with `/init` or minimal template
2. Add tech stack and commands first
3. Add conventions as you encounter friction
4. Test with real tasks
5. Iterate based on Claude's behavior

## Creating New Memory (.claude/rules/ approach)
1. Create `.claude/rules/` directory
2. Start with one file per major concern:
   - `general.md` - Universal project rules
   - `testing.md` - Testing conventions
   - `code-style.md` - Code conventions
3. Add path-scoped rules as needed:
   ```yaml
   ---
   paths: 
     - 'src/api/**/*.ts'
   ---
   # API rules here
   ```
4. Test with real tasks in different file contexts
5. Split or merge files based on usage patterns

## Maintaining Memory Files
1. Review quarterly (or when project changes significantly)
2. Remove outdated instructions
3. Add patterns that required repeated explanation
4. Keep CLAUDE.md under 200 lines (or split to .claude/rules/)
5. Use `#` for quick additions during work

## Migrating from CLAUDE.md to .claude/rules/
When CLAUDE.md exceeds 200 lines:

1. Identify distinct sections (testing, API, frontend, etc.)
2. Create `.claude/rules/` directory
3. Move each section to its own file
4. Add `paths` frontmatter where rules are file-type specific
5. Keep only universal