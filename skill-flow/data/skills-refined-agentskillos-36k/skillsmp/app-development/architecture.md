# Architecture Skill

This skill provides comprehensive knowledge of the AI Coaching Platform's architecture, design patterns, and organizational principles.

## Purpose

Use this skill when:
- Planning new features or major refactoring
- Understanding overall system architecture
- Learning import patterns and file organization
- Making architectural decisions
- Reviewing code structure and conventions

## Core Documentation

### Primary Reference

@exemplar-stack.md - The complete architectural reference for AI assistants

### Architecture Documentation

@architecture/core-principles.md
@architecture/design-patterns.md
@architecture/import-patterns.md
@architecture/project-structure.md
@architecture-overview.md

## Key Concepts

### Path Aliases
All imports use path aliases (defined in tsconfig.json):
- `@/*` - Root src
- `@actions/*` - Server actions
- `@zod-schema/*` - Zod schemas
- `@mongoose-schema/*` - Mongoose models
- `@components/*` - All components
- `@core-components/*` - Core atomic components
- `@server/*` - Server utilities
- `@error/*` - Error handling
- `@ui/*` - UI components
- `@hooks/*` - React hooks
- `@utils/*` - Utilities
- `@types/*` - Type definitions

### Schema-Driven Design
Zod schemas are the canonical source of truth for all data structures. Mongoose schemas define database structure but Zod schemas drive TypeScript types.

### Component Hierarchy
Components follow a strict hierarchy:
1. **Core** - Atomic, reusable building blocks
2. **Composed** - Combinations of core components
3. **Domain** - Business logic components
4. **Features** - Complete feature implementations

### CRUD Factory Pattern
Standardized patterns for Create, Read, Update, Delete operations with:
- Zod schema validation
- Server action implementation
- React Query hooks
- Consistent error handling

## File Organization

```
src/
├── app/
│   ├── actions/          # Server actions (grouped by feature number)
│   └── [routes]/         # Next.js app router pages
├── components/
│   ├── core/             # Atomic components
│   ├── composed/         # Composed components
│   ├── domain/           # Domain-specific components
│   └── ui/               # UI library components
├── lib/
│   ├── schema/
│   │   ├── zod-schema/       # Validation schemas
│   │   └── mongoose-schema/  # Database models
│   ├── server/           # Server utilities
│   ├── error/            # Error handling
│   └── utils/            # Utility functions
├── hooks/                # React hooks
├── query/                # React Query setup
└── types/                # TypeScript types
```

## Naming Conventions

- **Feature Numbering**: Features are organized by number (e.g., 313 for Roadmaps Skills)
- **Schema Files**: `{entity}-zod-schema.ts` and `{entity}-mongoose-schema.ts`
- **Server Actions**: `{operation}-{entity}.ts` (e.g., `fetch-roadmaps-skills.ts`)
- **Components**: PascalCase (e.g., `StudentCard.tsx`)
- **Hooks**: camelCase with `use` prefix (e.g., `useStudentData.ts`)

## Standards

- **TypeScript**: Avoid `any` types, use proper typing or `unknown` with type guards
- **Validation**: All external data validated with Zod schemas
- **Error Handling**: Use standardized error handling patterns from `@error/*`
- **Database**: Always use `withDbConnection` wrapper for MongoDB operations
- **Serialization**: Use `.toJSON()` when returning Mongoose documents

## Integration with Other Skills

- For backend/API patterns → Use `data-flow` skill
- For UI component development → Use `component-system` skill
- For implementation workflows → Use `workflows` skill
