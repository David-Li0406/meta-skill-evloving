# Prompt Design for Fanout Analysis

Effective prompt construction for parallel analysis sessions.

## Core Structure

Every fanout prompt follows this structure:

```xml
<role>Senior analyst specializing in {DOMAIN}.</role>

<context>
You are analyzing: $TARGET
Project type: $PROJECT_TYPE
Analysis focus: {SPECIFIC_FOCUS}
</context>

<task>
{NUMBERED_STEPS}
</task>

<constraints>
- READ-ONLY: Do NOT modify any files
- Do NOT create commits
- Do NOT execute side effects
- ONLY analyze and report
</constraints>

<output_contract>
Respond with ONLY this JSON:
{SCHEMA}
</output_contract>
```

## Design Principles

### 1. Role Clarity

The role sets the analytical lens:

| Analysis Type | Role Framing |
|---------------|--------------|
| gap | "capability gap and improvement opportunity specialist" |
| pattern | "pattern recognition and codification specialist" |
| friction | "developer experience and pain point specialist" |
| synergy | "connection and integration opportunity specialist" |
| platform | "platform utilization and capability assessment specialist" |
| meta | "reflective analysis and continuous improvement specialist" |

### 2. Context Precision

Provide exactly what the agent needs:

```xml
<context>
You are analyzing: ~/Developer/arbor/arbor-xyz
Project type: convex-turborepo
Analysis focus: identifying capability gaps between current state and mature project patterns
Reference projects: koto, kumori (for pattern comparison)
</context>
```

**Key context fields:**
- `$TARGET` - absolute path to analysis target
- `$PROJECT_TYPE` - detected or specified project type
- Analysis focus - specific lens for this analysis type
- Reference projects - when comparison is useful

### 3. Task Decomposition

Break analysis into 3-5 numbered steps:

```xml
<task>
1. **Understand current state**
   - Use `layer .` for architecture
   - Use `outline --stats` for code metrics

2. **Identify patterns**
   - Look for repeated structures
   - Note naming conventions

3. **Compare to reference**
   - Cross-check against known good patterns

4. **Synthesize findings**
   - Prioritize by impact
   - Note confidence levels
</task>
```

**Guidelines:**
- First step: exploration/discovery
- Middle steps: analysis/comparison
- Last step: synthesis/prioritization

### 4. Constraints Block

The constraints block is CRITICAL. Fanout is read-only by design.

```xml
<constraints>
- READ-ONLY: Do NOT modify any files
- Do NOT create commits
- Do NOT execute side effects
- ONLY analyze and report
</constraints>
```

**Why this matters:**
- Agents default to helpful action (including commits)
- Prior experiments showed agents committing during "analysis"
- Explicit constraints prevent unintended modifications

### 5. Output Contract

The output contract ensures parseable, aggregatable results:

```xml
<output_contract>
Respond with ONLY this JSON:
{
  "mode": "fanout",
  "analysis_type": "gap",
  "status": "success | partial | blocked | failed",
  "summary": "50-200 word summary of key findings",
  "confidence": 1-10,
  "artifacts": [
    {
      "type": "analysis",
      "content": "markdown content with structured findings"
    }
  ],
  "sources": {
    "files_read": ["list of files examined"],
    "tools_used": ["layer", "outline", etc.]
  },
  "assumptions": ["assumptions made during analysis"],
  "next_steps": ["recommended actions"],
  "blockers": []
}
</output_contract>
```

**Contract requirements:**
- ONLY JSON (no preamble, no explanation)
- All fields present (empty arrays acceptable)
- Confidence score reflects certainty
- Summary is standalone (readable without artifacts)

## Variable Substitution

Templates use shell-style variables:

| Variable | Source | Example |
|----------|--------|---------|
| `$TARGET` | --target flag or cwd | `~/Developer/arbor/arbor-xyz` |
| `$PROJECT_TYPE` | detected or --type flag | `convex-turborepo` |
| `$REFERENCE_PROJECTS` | optional --reference flag | `koto, kumori` |

**Substitution pattern:**
```bash
PROMPT=$(cat templates/gap-analysis.md | \
  sed "s|\$TARGET|$TARGET|g" | \
  sed "s|\$PROJECT_TYPE|$PROJECT_TYPE|g")
```

## Tool Guidance

Guide agents to use appropriate tools:

### For Architecture Understanding
```
Use `layer .` to understand package structure
Use `layer . --check-cycles` to find circular dependencies
```

### For Code Structure
```
Use `outline --stats` for codebase metrics
Use `outline --callers=X` to trace dependencies
Use `fd -e ts . src | outline -c` for full mapping
```

### For Pattern Discovery
```
Use `git log --oneline -20` for recent trajectory
Use `grep -r "pattern" --include="*.ts"` for specific patterns
```

### For Context Gathering
```
Read README.md, CLAUDE.md, AGENTS.md for project context
Check package.json for dependencies and scripts
```

## Prompt Length Guidelines

| Component | Target Length | Notes |
|-----------|---------------|-------|
| Role | 1 sentence | Clear, specific |
| Context | 3-5 lines | Essential facts only |
| Task | 10-20 lines | Numbered, actionable |
| Constraints | 4 lines | Always include |
| Output contract | 20-30 lines | Full JSON schema |

**Total prompt:** 50-80 lines optimal

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Vague role | Agent lacks focus | "Senior X specialist" |
| Missing constraints | Agent may modify files | Always include constraints block |
| Prose output | Can't aggregate | Use output_contract with JSON only |
| Too many steps | Agent gets lost | 3-5 steps maximum |
| No tool guidance | Agent explores blindly | Suggest specific tools |
| Ambiguous success | Hard to evaluate | Include confidence + status |

## Template Validation

Before using a template, verify:

1. [ ] Role is specific to analysis type
2. [ ] Context includes $TARGET and $PROJECT_TYPE
3. [ ] Task has 3-5 numbered steps
4. [ ] Constraints block is present and explicit
5. [ ] Output contract specifies exact JSON schema
6. [ ] No action verbs that imply modification (write, create, commit)
