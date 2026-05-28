# Example CLAUDE.md with Codebase Context Integration

This shows how to integrate the codebase-context skill into your project's CLAUDE.md.

---

## CRITICAL: Read Codebase Context First

**BEFORE using Glob, Grep, or exploring the codebase, you MUST:**

1. Read `.claude/codebase-context.md` - human-readable project context
2. Read `.claude/code-index.json` - fast lookups for concepts, exports, types
3. Read `.claude/deps.mermaid` - dependency graph for tracing imports
4. Run `.claude/check-context-freshness.sh` - verify context is current

**Use the code index for fast lookups:**
- Need to find where authentication is handled? Check `concepts.authentication`
- Need to know what a file exports? Check `exports["path/to/file.ts"]`
- Need to find a type definition? Check `types.TypeName`
- Need to trace dependencies? Read deps.mermaid

**DO NOT** use file search tools (Glob, Grep, Task with Explore agent) until you have checked these files. They contain:
- Complete directory structure with file purposes
- Key files organized by feature
- Patterns, conventions, and code style
- Database schema and domain concepts
- Quick commands and common gotchas
- Concept → file location mappings
- Export lists for all modules
- Type definition locations
- Dependency relationships

If the freshness check returns "STALE", regenerate context before proceeding:
```
/skill codebase-context
```

This saves tokens and ensures accurate understanding of the codebase.

---

## Project Guidelines

[Your normal CLAUDE.md content goes here...]

### Code Style
- Use TypeScript strict mode
- Prefer functional components
- etc.

### Commands
```bash
pnpm dev      # Start dev server
pnpm test     # Run tests
pnpm build    # Production build
```
