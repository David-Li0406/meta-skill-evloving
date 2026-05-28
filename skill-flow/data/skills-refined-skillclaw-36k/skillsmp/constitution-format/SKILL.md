---
name: Constitution Format
description: >-
  Knowledge about writing effective project constitution files for LLM/coding agents.
  Use this skill when creating, editing, or reviewing constitution.md files.
version: 0.1.0
---

# Constitution Format Knowledge

## Purpose

A constitution file defines rules, best practices, patterns, and guardrails for LLM and coding agents working in a project. Unlike human documentation, constitutions are optimized for token efficiency and machine parsing.

## File Location

Standard locations (checked in order):
1. `constitution.md` (project root)
2. `doc/constitution.md`

## Token Budget

**Hard limit: 25,000 tokens**

Approximate conversion: 1 token ≈ 4 characters

Monitor size when adding rules. A well-written constitution for a medium project typically uses 5,000-15,000 tokens.

## Structure

```markdown
# Project Constitution

Brief one-line project description.

## <Category 1>

- Rule 1
- Rule 2 (rationale)

## <Category 2>

- Rule 3
- Prefer X over Y
- Avoid Z
```

## Common Categories

| Category | Contents |
|----------|----------|
| **Stack** | Languages, frameworks, versions |
| **Patterns** | Required architectural patterns |
| **Anti-patterns** | What to avoid |
| **Conventions** | Naming, structure, organization |
| **Testing** | Testing requirements and approaches |
| **Security** | Security requirements |
| **Performance** | Performance constraints |
| **Dependencies** | Dependency rules |

## Writing Effective Rules

### DO

- **Imperative voice:** "Use X" not "You should use X"
- **Be specific:** "Use `const` by default" not "Prefer immutability"
- **Include brief rationale:** "Avoid any (breaks type safety)"
- **Quantify when possible:** "Max 300 lines per file"
- **State the positive:** "Use async/await" not "Don't use callbacks"

### DON'T

- Write explanatory prose
- Include code examples (unless critical)
- Duplicate information
- Use filler words (very, really, always try to)
- Over-qualify (usually, in most cases, generally)

## Rule Formats

**Simple rule:**
```markdown
- Use TypeScript strict mode
```

**Rule with rationale:**
```markdown
- Use TypeScript strict mode (catches null errors early)
```

**Preference:**
```markdown
- Prefer composition over inheritance
```

**Prohibition:**
```markdown
- Avoid `any` type
```

**Conditional:**
```markdown
- Use server components by default; client components only for interactivity
```

**Exception:**
```markdown
- Use strict mode (except legacy/ directory)
```

**Quantified:**
```markdown
- Max 300 lines per file
- Min 80% test coverage for business logic
```

## Example Constitution

```markdown
# Project Constitution

TypeScript monorepo for e-commerce platform.

## Stack

- TypeScript 5.3+ strict mode
- React 18 with Server Components
- Next.js 14 App Router
- PostgreSQL with Drizzle ORM
- Vitest for testing

## Patterns

- Feature-based directory structure
- Repository pattern for data access
- Use server components by default
- Client components only for interactivity
- Collocate tests with source files

## Anti-patterns

- Avoid `any` type (use `unknown` if needed)
- No barrel exports in feature modules
- No circular dependencies
- Avoid prop drilling beyond 2 levels

## Conventions

- camelCase for functions/variables
- PascalCase for components/types
- kebab-case for files and directories
- Prefix interfaces with I (IUser, IProduct)
- Suffix types with Type only if needed for clarity

## Testing

- Unit tests for business logic (min 80% coverage)
- Integration tests for API routes
- E2E tests for critical user flows
- Use Testing Library, avoid implementation details

## Security

- Validate all user input at API boundary
- Use parameterized queries only
- No secrets in code or logs
- HTTPS only, secure cookies
```

## Maintenance

- Review constitution when adding major features
- Remove rules for deprecated technologies
- Consolidate overlapping rules periodically
- Keep total under 25,000 tokens
