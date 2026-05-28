---
model: sonnet
allowed-tools: Task, Glob, Grep, Read, Write, Bash(test:*), Bash(find:*), AskUserQuestion
argument-hint: <domain or path>
description: Deep domain analysis to enrich atlas references
---

## Context

Arguments: `/cartographer:explore <TARGET>`
- **<domain>** - Domain name from atlas (e.g., "components", "redux_slices")
- **<path>** - Direct path to explore (e.g., "src/features/auth")

Current directory: !`pwd`

## Workflow

### 1. Pre-flight Checks

**Verify atlas exists:**
```bash
test -f ".claude/skills/atlas/references/schema.yaml" && echo "EXISTS" || echo "NOT_FOUND"
```

If not found → Error: "No atlas found. Run `/cartographer:chart` first."

**Load current schema:**
- Read `.claude/skills/atlas/references/schema.yaml`
- Extract domain information

### 2. Resolve Target

**If argument matches domain name:**
- Look up domain in schema
- Get domain path and current documentation

**If argument is a path:**
- Verify path exists
- Check if path is covered by existing domain
- If not covered, note as potential new domain

**If no argument provided:**
- Use AskUserQuestion to select from domain list
- Or ask for path to explore

### 3. Deep Analysis

**Perform detailed exploration of target:**

```
Analyze the following area in depth:

Path: {target_path}
Current documentation: {existing_reference_path or "None"}

Goals:
1. Document ALL files with purposes (not just key files)
2. Identify internal structure and sub-areas
3. Extract common patterns specific to this domain
4. Find related domains and dependencies
5. Identify common tasks and how to perform them
6. Note any anti-patterns or technical debt

Return detailed analysis for enriched documentation.
```

**Use Read/Glob/Grep to:**
- List all files in domain
- Sample file contents for pattern detection
- Trace imports to find dependencies
- Identify entry points and key abstractions

### 4. Generate Enriched Reference

**Create detailed reference file with:**

#### File Inventory

```markdown
## File Inventory

| File | Lines | Purpose | Key Exports |
|------|-------|---------|-------------|
{for each file}
| `{path}` | {lines} | {purpose} | {exports} |
{/for}
```

#### Internal Structure

```markdown
## Internal Structure

### Sub-areas

{for each sub-area}
#### {sub_area_name}
- Location: `{path}`
- Purpose: {purpose}
- Files: {count}
{/for}
```

#### Dependencies

```markdown
## Dependencies

### Imports From
| Domain | Files | Type |
|--------|-------|------|
{domains this area imports from}

### Imported By
| Domain | Files | Type |
|--------|-------|------|
{domains that import from this area}
```

#### Common Tasks

```markdown
## Common Tasks

### {Task Name}

**When:** {when to do this task}

**Steps:**
1. {step 1}
2. {step 2}
3. {step 3}

**Files involved:**
- `{file1}` - {role}
- `{file2}` - {role}

**Example from codebase:**
```{language}
{code example}
```
```

#### Patterns and Conventions

```markdown
## Domain-Specific Patterns

### {Pattern Name}

**Convention:** {description}
**Example:** `{example}`
**Rationale:** {why this pattern}

### Anti-Patterns to Avoid

❌ **Don't:** {what not to do}
✅ **Do:** {correct approach}
```

### 5. Update Atlas

**Update domain reference:**
- Replace or enhance existing reference file
- Preserve user customizations if marked

**Update schema.yaml:**
- Update file count if changed
- Update key files if better ones identified
- Add observations

**Update SKILL.md:**
- Add new keywords to domain router if discovered
- Update task quick reference if applicable

### 6. Report Results

```markdown
## Domain Exploration Complete

**Target:** {domain_name} (`{path}`)

**Analysis Summary:**
- Files documented: {count}
- Sub-areas identified: {count}
- Dependencies mapped: {count} imports, {count} importers
- Tasks documented: {count}
- Patterns documented: {count}

**Files updated:**
- `.claude/skills/atlas/references/{domain_path}`
- `.claude/skills/atlas/references/schema.yaml`

**Key findings:**
{list notable discoveries}

**Next steps:**
- Run `/cartographer:explore {related_domain}` to explore connected areas
- Run `/cartographer:health` to verify overall atlas health
```

---

## Exploration Depth

| Aspect | Standard Chart | Deep Explore |
|--------|----------------|--------------|
| File listing | Key files only | All files |
| File purposes | Inferred | Examined |
| Dependencies | Not tracked | Mapped |
| Common tasks | Generic | Specific with examples |
| Patterns | Naming conventions | Implementation details |
| Sub-areas | Not detailed | Documented |

---

## Error Handling

| Error | Action | Recovery |
|-------|--------|----------|
| No atlas found | Error message | Run /cartographer:chart |
| Domain not found | Suggest similar or list available | User selects |
| Path not found | Error with suggestion | User provides valid path |
| Path not in atlas | Offer to add as new domain | User confirms |

## Responsibilities

**YOU (handler):**
- Resolve target domain/path
- Perform deep file analysis
- Generate enriched documentation
- Update atlas files
- Report findings

**You do the detailed exploration directly, reading files and tracing patterns.**
