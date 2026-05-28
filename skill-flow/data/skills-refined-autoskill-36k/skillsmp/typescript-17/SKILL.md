---
name: typescript
description: Read when working with *.ts files
---

# TypeScript Rules


## Tech Stack
- Backend: Node.js with TypeScript, GraphQL, Apollo Server
- Database: PostgreSQL running on RDS

## Do's
- Be ruthless with typos, don't let them slip
- Prefer native functions over custom or Lodash's
- Use Lodash helpers instead of custom solutions
- Maintain consistency in naming and problem-solving
- Write simple, and clean code that is indistinguishable from the existing one
- Use modern (ES6) solutions, e.g. Object destructuring
- Use `async`/`await` instead of callbacks or `then()` Promises
- Prioritize readability over performance unless necessary
- Keep functions focused on a single task and simple
- Maximize type inference where possible
- Keep class properties private when possible
- When writing console.log's for testing, always use this form: `console.log('>>>', { value1, value2, ... })`
- Keep function parameters on one line when reasonable
- Prefer `if (arr[i])` over `if (i >= 0 && i < arr.length)`
- Prefer `if (arr.length)` over `if (arr.length > 0)`
- Use proper enum types instead of string literals for type safety (e.g., `Type.Fee` instead of `'Fee'`)
- All imported symbols from a file go in the same line, no newlines

## Don'ts
- Avoid strings for properties in Lodash functions (e.g. `_.get(obj, 'path.to.value')`), use a lambda
- Avoid `any` type unless absolutely needed
- Avoid relative imports, always use `src/...`
- No semicolons
- Never update src/types/graphql.ts or src/types/resolvers/graphql.ts. Those are auto-generated with `npm run gql:codegen`
- Avoid unnecessary empty lines in implementation code

## Naming

- Use simple, consistent names. When in doubt, name by type (e.g., `user`, `task`)
- Keep local variable names concise when context is clear (e.g., `col` instead of `assignedColumn`)
- Most local variables should be one, at most two words
- Always camelCase, never snake_case
- Within lambda one-liners (like inside map()) name parameters with a single letter (e.g., `(u) => u.name`)
- Shorten type names when they become very long (e.g., `LineItemWithApplications` instead of `LineItemWithApplications`)
- We prefix unused parameters with `_`
- We ONLY prefix exported functions with `_` for the case of unit testing them, to signal they should not be called directly

### By type
- Boolean: Start with `is`, `can`, `are` (e.g., `isActive`)
- Date: End with `At` (e.g., `createdAt`)
- Array: Use plural form (e.g., `users`)
- Object: Use plural or `Map` suffix (e.g., `userMap`)
- Enums: Use TitleCase (e.g., `OrganizationKind`)
- Queries: Noun for one, plural for many (e.g., `user`, `tasks`)
- Mutations: Verb+Noun (e.g., `updateOrganization`)
- Error: Call them `err`
- Events: Call them `e`

### Files & Modules
- Always use camelCase starting with a lower case, no hyphens or underscores
- Don't repeat the directory name in the file name
- If a directory needs +1 files but we usually import 1, use index.ts it
- Many modules are meant to be imported as `import * as X from './X'`, like integrations and utils

## Environment Variables
- Never use process.env, import from `src/domain/envs/index.ts` instead
- Base URLs should come from environment variables

## Module structure
- Generally, put exported things at the top of the file
- Internal types and helper functions should be at the bottom. You can use `function` form so they can be used before definition
- Keep implementation details private, expose only the minimal that's needed. This applies to types, functions, classes, etc.
- If something is exported, it shouldn't have a very short name. If it isn't exported, the context should be omitted from the name

## Comments
- Good code doesn't need many comments, don't do bad code
- Do not include JSDoc comments in your code
- We can include a single `/** ... */` above a function if it needs explaining
- We use `//` comments for inline explanations, always above the line of code it explains
- Keep documentation to the minimum and focused on usage, not implementation
- Never have an empty line above a `//` comment

## Other
- Before providing a block of code, reason about what is requested and the context provided first
- Never read/write files in sync mode, this is a server
- The linter removes unused imports on save, so if you are adding an import make sure it is used before you add it
