---
name: flight-prime
description: Prime context for a task - research, scan codebase, gather domain constraints. Use when starting implementation of a task file, PRD, or clear task description.
---

## ⚠️ EXECUTION RULES (MANDATORY)

1. **EXECUTE EACH STEP** - Do not skip steps based on "prior context"
2. **USE TOOLS** - You MUST call Read/Bash tools, not recall from memory
3. **SHOW WORK** - Each step must produce visible tool output
4. **NO SHORTCUTS** - "I already read this" is NOT acceptable

### Anti-Patterns (DO NOT DO THESE)
- ❌ "I already read the domain files earlier"
- ❌ "From earlier analysis..."
- ❌ Summarizing steps without executing them
- ❌ Claiming knowledge from "this conversation"

---

# /flight-prime

Prime the context for a task. Research, scan, and gather all facts needed before compiling a prompt.

## Usage

```
/flight-prime <task description>
/flight-prime PRD.md
/flight-prime tasks/001-project-setup.md
```

## Arguments

- `$ARGUMENTS` - Task description, PRD file, or task file to implement

---

## Process

### 1. READ ALL DOMAIN FILES FIRST (Critical)

**Before doing anything else**, read every domain file:

```bash
ls -la .flight/domains/
```

Then read each `.md` file. After reading, list what you found:

```markdown
## Available Domains
- code-hygiene.md: [Universal naming/quality - ALWAYS LOAD]
- javascript.md: [what it covers]
- react.md: [what it covers]
- [etc.]
```

**Identify which domains are RELEVANT to the task.**

### 2. Load Project Context

```bash
# Check for existing patterns
find . -name "*.js" -o -name "*.ts" -o -name "*.tsx" | head -20

# Check configs
ls -la package.json tsconfig.json .eslintrc* next.config.* 2>/dev/null

# Check existing structure
ls -la src/ app/ components/ lib/ 2>/dev/null
```

### 3. Research with Available Tools

Use all available research tools to ground implementation in current reality:

#### Domain Files (Always)
- Read `.flight/domains/*.md` for project constraints
- These override external documentation

#### Web Search
Use for:
- Current API documentation
- Recent breaking changes
- Framework version-specific patterns
- **Queries**: `"{library} {version} documentation"`, `"{framework} {feature} example"`, `"{error message}"`

#### MCP Tools (if available)

Check your tool list for these:

| Tool | What It Does | When to Use |
|------|--------------|-------------|
| `context7_*` | Library/framework docs (curated, versioned) | Getting current API docs for Next.js, React, Supabase, etc. |
| `firecrawl_*` | Deep web scraping, crawl entire sites | Extracting patterns from documentation sites |

**If MCP tools are available, prefer them over raw web search for documentation.**

**If tools would help but aren't available:**
```
NOTE: Better research results available with MCP tools:
- Context7: https://github.com/upstash/context7
- Firecrawl: https://github.com/mendableai/firecrawl

Proceeding with web search. Install MCP tools for improved documentation access.
```

### 4. Identify Constraints

From domain files and codebase, determine:
- What patterns MUST be followed
- What's FORBIDDEN (NEVER rules)
- What files need to be created/modified
- What existing patterns to match

### 5. Check for External Dependencies

If the task involves external APIs or libraries:
- Get exact endpoints, auth methods, response shapes
- Check for version-specific requirements
- Note any rate limits or quotas

---

## Output: PRIME.md

Generate this structure:

```markdown
# Prime: [Task Name]

## Task Summary
[One paragraph describing what needs to be built]

## Task Type
[API Endpoint | Migration | Component | Service | CLI Tool | etc.]

## Domains Loaded
- `code-hygiene.md` - Always loaded
- `[domain].md` - [why relevant]

## Key Constraints

### NEVER (will fail validation)
- [From domain files - hard failures]

### MUST (will fail validation)
- [From domain files - required patterns]

### SHOULD (warnings)
- [From domain files - best practices]

## Relevant Files

### Existing Patterns to Follow
- `path/to/file.js` - [why relevant, what pattern to match]

### Files to Create/Modify
- `path/to/new-file.js` - [what it will contain]

## External Dependencies

### APIs (if any)
- **Service:** [name]
- **Endpoint:** [URL]
- **Auth:** [method]
- **Docs:** [URL checked]

### Libraries (if any)
- `[library@version]` - [purpose]
- **Docs checked:** [URL or Context7]

## Research Sources
- [URL or tool]: [Key finding]

## Open Questions
- [Anything unclear that needs human input]
```

---

## Critical Rules

1. **READ DOMAIN FILES FIRST** - Before any external research
2. **ALWAYS LOAD code-hygiene.md** - It applies to everything
3. **USE MCP TOOLS** when available for documentation
4. **CITE SOURCES** - Note where information came from
5. **PULL ACTUAL CONSTRAINTS** from domain files into PRIME.md
6. **DO NOT IMPLEMENT** - This is research only
7. **DO NOT GENERATE CODE** - Output feeds into `/flight-compile`

---

## When to Use

| Starting Point | Use This? |
|----------------|-----------|
| Vague idea ("build SMS thing") | No → Use `/flight-prd` first |
| Clear task description | Yes |
| PRD.md from /flight-prd | Yes |
| Task file (tasks/001-*.md) | Yes |
| Have code, need to check | No → Use `/flight-validate` |

---

## Next Step

After generating PRIME.md, compile it into an executable prompt:

```
/flight-compile
```

**Workflow**: `/flight-prime` → `/flight-compile` → [implement] → `/flight-validate`

| Response | Action |
|----------|--------|
| `continue` or `c` | Proceed to `/flight-compile` |
| `review` | Display PRIME.md contents for review |
| `edit` | Modify PRIME.md before compiling |
