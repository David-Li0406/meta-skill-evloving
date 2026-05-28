# Project: [Name]

## Overview
[2-3 sentence description]

## Tech Stack
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS + Shadcn UI (@ui, @magicui)
- [Database: Supabase | None]
- [Other key tech]

## Development Workflow

### Skills
- `nextjs-project-setup` - Project setup
- `design-system` - Design management
- `test-driven-development` - TDD workflow

### MCP Tools
- Vercel: Deployment
- Shadcn: Components (Search→View→Example→Install)
- Supabase: DB/Auth (MCP only)

### Conventions
- Mobile-first responsive
- WCAG 2.1 AA accessibility
- Server actions for mutations
- Global Tailwind CSS (CSS variables only)
- TDD approach

### Anti-Patterns
❌ Supabase CLI (use MCP)
   **Why**: MCP provides better error handling and integration

❌ Skip Shadcn Example step
   **Why**: Examples reveal usage patterns and prevent integration issues

❌ Hardcoded colors
   **Why**: Breaks theme switching and design system consistency

❌ Code before tests
   **Why**: Tests-first ensures meeting requirements, not just confirming behavior

## References
@docs/architecture.md | @docs/design-system.md
