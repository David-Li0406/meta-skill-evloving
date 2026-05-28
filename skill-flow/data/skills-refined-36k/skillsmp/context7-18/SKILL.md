---
name: context7
description: Fetch up-to-date documentation and code examples for any library or framework using the Context7 MCP service. Use when the user asks for API references, code examples, library documentation, framework guides, or best practices for specific libraries such as React, Next.js, MongoDB, Supabase, Prisma, or any other npm ecosystem package.
# Optional, but recommended if you want Claude to freely run the CLI
allowed-tools: "Bash,Read,Grep,Glob"
---

# Context7

Use **Context7** to pull current, source-backed documentation and code examples for libraries and frameworks directly into the conversation.[web:8][web:12][web:16]

## Environment & Location

- This skill assumes the project has a `context7` skill directory with a `scripts/context7.ts` runner.
- The script should be executable via `bun` from the project root:
  - Preferred: `bun .claude/skills/context7/scripts/context7.ts <command> [options]`
- If the skill is installed elsewhere, adjust paths accordingly in Bash commands.

When unsure about the exact path, first use `Glob` and `Read` to locate `scripts/context7.ts`, then construct commands using the discovered path.

## When to Use This Skill

Use this skill when:

- The user requests:
  - API references or parameter details for a function, class, or component.
  - Up-to-date code examples for a library or framework.
  - Official or canonical documentation links or explanations.
  - Migration guidance across versions where current docs matter.
- The task involves libraries or frameworks such as:
  - React, Next.js, MongoDB, Supabase, Prisma, Tailwind, Express, etc.
- Local knowledge or static training data might be outdated and fresh docs would help.

If the user explicitly mentions “Context7” or “use context7”, always consider invoking this skill.

## Core Tools & Commands

All commands are executed via `bun` in Bash.[web:8][web:12]

### 1. resolve-library-id

**Purpose:** Map a human library name (e.g., `react`, `next.js`, `mongodb`) to a Context7-compatible library ID (e.g., `/facebook/react`).[web:12][web:16]

**Command pattern:**

```
bun .claude/skills/context7/scripts/context7.ts resolve-library-id --library-name "<library-name>"
```

**Usage guidelines:**

1. When the user gives a library by name (e.g., “React hooks”), first resolve the library ID.
2. If multiple libraries could match (e.g., `react`, `react-dom`), use the name that best matches the user’s question.
3. Parse the CLI output:
   - Extract the most relevant `Context7-compatible library ID`.
   - Prefer libraries whose description and ecosystem align with the user’s tech stack.

**Example calls:**

```
bun .claude/skills/context7/scripts/context7.ts resolve-library-id --library-name "react"
bun .claude/skills/context7/scripts/context7.ts resolve-library-id --library-name "next.js"
bun .claude/skills/context7/scripts/context7.ts resolve-library-id --library-name "mongodb"
```

Only skip this step if the user already provides a valid Context7 library ID like `/vercel/next.js` or `/mongodb/docs`.

### 2. get-library-docs

**Purpose:** Fetch up-to-date documentation and code examples for a specific library.[web:8][web:12][web:16]

**Command pattern:**

```
bun .claude/skills/context7/scripts/context7.ts get-library-docs \
  --context7-compatible-library-i-d "<library-id>" \
  [--mode "code" | "info"] \
  [--topic "<topic>"] \
  [--page <page-number>] \
  [--timeout <ms>] \
  [--output "text" | "markdown" | "json" | "raw"]
```

**Key parameters:**

- `--context7-compatible-library-i-d` (required):
  - The Context7 library ID, such as `/facebook/react`, `/vercel/next.js`, `/mongodb/docs`, `/supabase/supabase`, `/prisma/prisma`.
- `--mode`:
  - `"code"` (default) for API references, method signatures, and code snippets.
  - `"info"` for conceptual guides, explanations, and higher-level docs.
- `--topic`:
  - Narrow results to a specific area, e.g.:
    - React: `hooks`, `context`, `suspense`.
    - Next.js: `routing`, `app-router`, `middleware`.
    - Auth stacks: `authentication`, `oauth`, `session`, `jwt`.
- `--page`:
  - Use `1` initially; increase (`2–10`) if more or different context is needed.
- Global options:
  - `-t, --timeout <ms>`: default `30000`, increase for large docs.
  - `-o, --output <format>`:
    - Prefer `markdown` for direct quoting and summarization.
    - Use `json` if you need to parse or reorganize results programmatically.

**Example calls:**

```
# Basic usage for Next.js API docs
bun .claude/skills/context7/scripts/context7.ts get-library-docs \
  --context7-compatible-library-i-d "/vercel/next.js"

# Focus on routing guides for Next.js
bun .claude/skills/context7/scripts/context7.ts get-library-docs \
  --context7-compatible-library-i-d "/vercel/next.js" \
  --mode "info" \
  --topic "routing" \
  --output "markdown"

# MongoDB conceptual docs about aggregation pipelines
bun .claude/skills/context7/scripts/context7.ts get-library-docs \
  --context7-compatible-library-i-d "/mongodb/docs" \
  --mode "info" \
  --topic "aggregation" \
  --page 1

# Supabase authentication code examples
bun .claude/skills/context7/scripts/context7.ts get-library-docs \
  --context7-compatible-library-i-d "/supabase/supabase" \
  --mode "code" \
  --topic "authentication" \
  --output "markdown"
```

## Decision Flow

When responding to a user query that might benefit from Context7:

1. **Check the question**
   - If the user wants current library behavior, exact API signatures, or framework-specific patterns, prefer Context7 over guessing from memory.
2. **Determine library identifier**
   - If a valid Context7 ID is provided, use it directly.
   - Otherwise, call `resolve-library-id` with the library or product name.
3. **Choose mode and topic**
   - Use `mode="code"` when the user is asking “how do I implement X?” or wants snippets.
   - Use `mode="info"` for conceptual explanations or migration guides.
   - Set `topic` based on the exact feature/area the user asks about.
4. **Fetch docs**
   - Call `get-library-docs` with the chosen parameters.
5. **Integrate results**
   - Summarize key points in your own words.
   - Show the most relevant snippets, trimming noise.
   - Explicitly relate the documentation back to the user’s codebase, stack, and constraints.

## Common Library IDs

Use these as shortcuts when relevant:[web:8][web:12][web:16]

| Library  | Context7 Library ID   |
|----------|-----------------------|
| React    | `/facebook/react`     |
| Next.js  | `/vercel/next.js`     |
| MongoDB  | `/mongodb/docs`       |
| Supabase | `/supabase/supabase`  |
| Prisma   | `/prisma/prisma`      |

If a requested library is not in this table, always attempt `resolve-library-id` with the exact name the user supplied.

## Requirements

- Installed **Bun** runtime to execute the `context7.ts` script.[web:8]
- The `context7` script must include or be configured with the `mcporter`/Context7 client dependencies according to the Context7 MCP documentation.[web:8][web:16]
- Network access from the execution environment so Context7 can reach upstream documentation sources.

## Examples

### Example 1: React useEffect dependency behavior

1. Run:

   ```
   bun .claude/skills/context7/scripts/context7.ts resolve-library-id --library-name "react"
   ```

2. Then:

   ```
   bun .claude/skills/context7/scripts/context7.ts get-library-docs \
     --context7-compatible-library-i-d "/facebook/react" \
     --mode "code" \
     --topic "useEffect dependencies" \
     --output "markdown"
   ```

3. Use the returned docs and snippets to:
   - Confirm current `useEffect` dependency array semantics.
   - Provide accurate examples aligned with the latest React release.

### Example 2: Next.js app router routing

1. Resolve:

   ```
   bun .claude/skills/context7/scripts/context7.ts resolve-library-id --library-name "next.js"
   ```

2. Fetch routing docs:

   ```
   bun .claude/skills/context7/scripts/context7.ts get-library-docs \
     --context7-compatible-library-i-d "/vercel/next.js" \
     --mode "info" \
     --topic "app router routing" \
     --output "markdown"
   ```

3. Use results to explain file structure, segment conventions, and route groups, plus provide concrete route examples.

