<!--
Embedded Cartographer Command: where
Standalone version for plugin-free operation
-->
---
allowed-tools: Read, Glob, Grep
argument-hint: <query>
description: Quick keyword to path lookup using atlas
---

## Context

Arguments: `/where <QUERY>`
- **<query>** - Keyword, file name, concept, or question

Current directory: !`pwd`

## Workflow

### 1. Load Atlas

Read:
- `.claude/skills/atlas/SKILL.md`
- `.claude/skills/atlas/references/schema.yaml`

If not found: Fall back to basic grep/glob.

### 2. Parse Query

Determine intent:
- File name: `UserProfile.tsx` → file search
- Keyword: `auth`, `routing` → domain lookup
- Question: "where is X" → keyword extraction
- Pattern: `*.service.ts` → pattern lookup

### 3. Search

**Priority order:**
1. Exact file match
2. Domain router match
3. Schema domain/purpose match
4. Pattern match
5. Grep fallback

### 4. Return Results

**Domain match:**
```markdown
## Found: {domain_name}

**Location:** `{path}`
**Purpose:** {purpose}

**Key files:**
{list}

**Reference:** [{path}]({reference})
```

**File match:**
```markdown
## Found: {count} file(s)

{list with paths and purposes}

**Related domain:** [{name}]({reference})
```

**Pattern match:**
```markdown
## Pattern: {name}

**Location:** `{glob}`
**Count:** {count} files

**Examples:**
{list}
```

**No match:**
```markdown
## No results for "{query}"

**Suggestions:**
- Try: {alternatives}
- Browse: {top domains}
```

Keep responses concise and actionable.
