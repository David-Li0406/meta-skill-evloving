---
name: repo-name-generator
description: Generate creative, memorable repository names optimized for virality. Analyzes project content to suggest names that are catchy, searchable, and shareable. Use when asked to "name this repo", "suggest repo names", "what should I call this project", or "generate project name".
license: MIT
compatibility: Any environment
metadata:
  author: tsilva
  version: "1.0.0"
argument-hint: "[project-path]"
---

# Repo Name Generator

Generate 6 creative, memorable repository names optimized for virality.

## Quick Start

```
/repo-name-generator           # Analyze current directory
/repo-name-generator ./path    # Analyze specific path
```

## Workflow

### 1. Project Analysis

Examine available files to understand the project:

| File | What to Extract |
|------|-----------------|
| README.md | Project description, purpose |
| package.json / pyproject.toml / Cargo.toml / go.mod | Name, description, keywords |
| Main source files | Core functionality |
| Current repo name | Context for renaming |

### 2. Apply Virality Criteria

| Factor | Description | Examples |
|--------|-------------|----------|
| **Memorable** | Short, easy to spell/say | `vite`, `bun`, `deno` |
| **Searchable** | Unique, SEO-friendly | `fastapi`, `prisma` |
| **Shareable** | Fun to mention | `husky`, `panda` |
| **Descriptive** | Hints at purpose | `typescript`, `autoprefixer` |
| **Clever** | Wordplay, metaphors | `yarn`, `brew`, `nest` |

### 3. Generate Names Across Styles

Generate at least one name per style:

| Style | Characteristics |
|-------|-----------------|
| **Creative** | Metaphors, abstract concepts (phoenix, aurora) |
| **Professional** | Clean, corporate-friendly (dataforge, apikit) |
| **Playful** | Fun animals/objects (otter, rocket) |
| **Technical** | Describes function directly (quicksort, logstream) |
| **Punny** | Wordplay, tech jokes (gitgud, ctrl-z) |

## Output Format

Present exactly 6 name suggestions in this format:

```markdown
## Suggested Repository Names

### 1. **name-here**
> Tagline that captures the essence

**Style:** Creative | **Why it works:** Brief explanation of virality factors

---

### 2. **another-name**
> Another compelling tagline

**Style:** Professional | **Why it works:** Explanation

---

(continue for all 6 suggestions)
```

## Guidelines

- Names should be lowercase, hyphenated if multi-word
- Prefer 1-2 words (max 3)
- Avoid names already taken by popular projects
- Include mix of safe and bold options
- Consider domain availability patterns (.io, .dev, .sh)

## Example Output

For a CLI tool that formats code:

```markdown
## Suggested Repository Names

### 1. **prettify**
> Make your code beautiful

**Style:** Creative | **Why it works:** Evocative verb, easy to remember, hints at purpose

---

### 2. **codeshine**
> Polish your codebase to perfection

**Style:** Professional | **Why it works:** Compound word, professional feel, clear purpose

---

### 3. **tidy**
> Clean code, happy developers

**Style:** Playful | **Why it works:** Short, friendly, universal appeal

---

### 4. **fmt**
> Fast, minimal formatter

**Style:** Technical | **Why it works:** Unix-style brevity, instantly recognized by devs

---

### 5. **brushstroke**
> Paint your code with style

**Style:** Creative | **Why it works:** Artistic metaphor, memorable imagery

---

### 6. **lint-roller**
> Roll away the code lint

**Style:** Punny | **Why it works:** Visual pun on lint removal, memorable and shareable
```
