---
model: haiku
allowed-tools: Read, Glob, Grep
argument-hint: <query>
description: Quick keyword to path lookup using atlas
---

## Context

Arguments: `/cartographer:where <QUERY>`
- **<query>** - Keyword, file name, concept, or question (e.g., "auth", "UserProfile", "where is routing")

Current directory: !`pwd`

## Workflow

### 1. Load Atlas

**Read atlas files:**
- `.claude/skills/atlas/SKILL.md` - For domain router
- `.claude/skills/atlas/references/schema.yaml` - For paths and patterns

**If atlas not found:**
- Fall back to basic grep/glob search
- Note: "Atlas not found. Using basic search. Run `/cartographer:chart` for better results."

### 2. Parse Query

**Extract search intent:**
- File name: `UserProfile.tsx` → direct file search
- Keyword: `auth`, `routing`, `state` → domain lookup
- Question: "where is X", "how to Y" → keyword extraction
- Pattern: `*.service.ts` → pattern lookup

### 3. Search Strategy

**Priority order:**

1. **Exact file match:** Search for exact filename
2. **Domain router match:** Check atlas domain router keywords
3. **Schema domain match:** Check domain names and purposes
4. **Pattern match:** Check file patterns in schema
5. **Grep fallback:** Search file contents

### 4. Return Results

**For domain match:**

```markdown
## Found: {domain_name}

**Location:** `{path}`
**Purpose:** {purpose}

**Key files:**
{list key files}

**Reference:** [Read more]({reference_path})
```

**For file match:**

```markdown
## Found: {count} file(s)

{for each file}
- `{path}` - {inferred purpose or domain}
{/for}

**Related domain:** [{domain_name}]({reference_path})
```

**For pattern match:**

```markdown
## Pattern: {pattern_name}

**Location pattern:** `{glob}`
**Count:** {count} files
**Purpose:** {purpose}

**Examples:**
{list example files}

**Pattern guide:** [Implementation details]({pattern_reference})
```

**For multiple matches:**

```markdown
## Search: "{query}"

### Domains
{list matching domains with paths}

### Files
{list matching files}

### Patterns
{list matching patterns}

**Tip:** Be more specific or use domain name directly.
```

**For no match:**

```markdown
## No results for "{query}"

**Suggestions:**
- Try related terms: {suggestions}
- Browse domains: {list top domains}
- Search file contents: `grep -r "{query}" src/`
```

---

## Query Examples

| Query | Type | Expected Result |
|-------|------|-----------------|
| `auth` | keyword | Auth domain or auth-related files |
| `UserProfile.tsx` | filename | Direct file path |
| `*.api.ts` | pattern | API file pattern info |
| `where is state` | question | State management domain |
| `hooks` | keyword | Hooks domain |
| `redux slice` | multi-word | Redux slices domain |

---

## Response Format

Keep responses concise and actionable:

✅ **Good:**
```
## Found: hooks

**Location:** `src/hooks/`
**Reference:** [references/grow/hooks.md](references/grow/hooks.md)
```

❌ **Avoid:**
```
I searched the atlas and found that hooks are located in the src/hooks directory.
Based on the schema, this domain contains custom React hooks...
[lengthy explanation]
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| No atlas | Use basic search, suggest chart |
| No results | Suggestions and alternatives |
| Ambiguous query | Show all matches, ask for specificity |
| Multiple exact matches | List all with context |

## Responsibilities

**YOU (handler):**
- Parse query intent
- Search atlas efficiently
- Return concise, actionable results
- Provide navigation to full references

**This is a quick lookup command. Keep it fast and focused.**
