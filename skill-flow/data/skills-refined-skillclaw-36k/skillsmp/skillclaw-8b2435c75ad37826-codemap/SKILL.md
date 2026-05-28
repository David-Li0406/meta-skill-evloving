---
name: codemap
description: Use this skill when you need to navigate codebases efficiently by finding symbol definitions, exploring file structures, or locating code by name, while significantly reducing token consumption.
---

# CodeMap - Codebase Structural Index

Navigate codebases efficiently using pre-built structural indexes stored in `.codemap/` directories.

## When to Use This Skill

**USE CodeMap when:**
- Finding where a class, function, method, or type is defined
- Understanding a file's structure before reading it
- Searching for symbols by name
- Reducing token usage during codebase exploration

**READ full files when:**
- Understanding implementation details
- Making edits to code
- The symbol isn't in the index (new/untracked file)

## Quick Reference

```bash
# Find a symbol by name (case-insensitive)
codemap find "SymbolName"

# Filter by type
codemap find "handle" --type method
codemap find "User" --type class
codemap find "Config" --type interface

# Show file structure with all symbols
codemap show path/to/file.ts

# Check if index is up-to-date
codemap validate

# View index statistics
codemap stats
```

## Workflow: Finding Code

### Step 1: Find Symbol Location
```bash
codemap find "UserService"
```
Output:
```
src/services/user.ts:15-189 [class] UserService
  (config: Config)
```

### Step 2: Read Only Relevant Lines
Instead of reading the entire file, read just lines 15-189:
```
Read src/services/user.ts lines 15-189
```

### Step 3: Explore Nested Symbols
```bash
codemap show src/services/user.ts
```
Output:
```
File: src/services/user.ts (hash: a3f2b8c1)
Lines: 542
Language: typescript

Symbols:
- UserService [class] L15-189
  - constructor [method] L20-35
  - getUser [method] L37-98
    (userId: string) : Promise<User>
  - createUser [async_method] L100-145
    (data: CreateUserDto) : Promise<User>
```

## Symbol Types

| Type | Description |
|------|-------------|
| `class` | Class declaration |
| `function` | Function declaration |
| `method` | Class method |
| `async_function` | Async function |
| `async_method` | Async class method |
| `interface` | TypeScript interface |
| `type` | TypeScript type alias |
| `enum` | Enum declaration |

## Index Structure

The `.codemap/` directory mirrors the project structure:
```
.codemap/
├── .codemap.json              # Root manifest
├── _root.codemap              # Root index file
```