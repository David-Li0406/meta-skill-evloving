---
name: skills-architect
description: "Project-scoped skills router for .claude/skills/ with progressive disclosure. Use when creating, auditing, or refining skills in current project. Routes to skills-knowledge for implementation details. Do not use for standalone plugin development."
disable-model-invocation: true
---

# Skills Architect

Domain router for skills development with progressive disclosure and autonomy-first design.

## MANDATORY: Read Before Creating Skills

- **MUST READ**: [Official Skills Guide](https://code.claude.com/docs/en/skills)
  - Tool: `mcp__simplewebfetch__simpleWebFetch`
  - Cache: 15 minutes minimum
  - Blocking: DO NOT proceed without understanding skill structure

- **MUST READ**: [Agent Skills Specification](https://agentskills.io/specification)
  - Tool: `mcp__simplewebfetch__simpleWebFetch`
  - Cache: 15 minutes minimum
  - Blocking: DO NOT proceed without understanding progressive disclosure format

## Actions

### create
**Creates new skills** in `.claude/skills/<name>/`

**Target Directory**: `${CLAUDE_PROJECT_DIR}/.claude/skills/`

**Router Logic**:
1. Determine tier structure:
   - Tier 1: Metadata (~100 tokens)
   - Tier 2: SKILL.md (<500 lines for self-contained, or use references/)
   - Tier 3: references/ (on-demand)
2. Generate skill with:
   - YAML frontmatter (name, description, disable-model-invocation)
   - Progressive disclosure structure
   - Auto-discovery optimization
   - **MANDATORY URL fetching sections**
3. Create directory: `.claude/skills/<skill-name>/`
4. Write SKILL.md and references/ (if needed)
5. Validate: URL fetching sections, triggers

**Output Contract**:
```
## Skill Created: {skill_name}

### Location
- Path: .claude/skills/{skill_name}/
- SKILL.md: ✅
- references/: {count} files

### Tier Structure
- Tier 1: Metadata loaded
- Tier 2: SKILL.md ({size} chars)
- Tier 3: references/ ({count} files)

### Autonomy Score: {score}/10
Target: 80-95% completion without questions

### Progressive Disclosure
- Tier 1: ✅
- Tier 2: ✅
- Tier 3: ✅
```

### audit
**Audits skills** for quality and autonomy

**Router Logic**:
1. Check:
   - YAML frontmatter completeness
   - Progressive disclosure implementation
   - Autonomy score (80-95% completion)
   - Auto-discovery optimization
   - URL fetching sections
2. Generate audit with scoring

**Output Contract**:
```
## Skill Audit: {skill_name}

### Autonomy Assessment
- Completion without questions: {score}%
- Target: 80-95%

### Progressive Disclosure
- Tier 1 (Metadata): ✅/❌
- Tier 2 (SKILL.md): ✅/❌
- Tier 3 (references): ✅/❌

### Quality Issues
- {issue_1}
- {issue_2}

### Recommendations
- {recommendation_1}
- {recommendation_2}
```

### refine
**Improves skills** based on audit findings

**Router Logic**:
1. Review progressive disclosure
2. Enhance:
   - Metadata clarity
   - SKILL.md structure
   - references/ organization
   - Autonomy optimization
3. Validate improvements

**Output Contract**:
```
## Skill Refined: {skill_name}

### Improvements Applied
- {improvement_1}
- {improvement_2}

### Autonomy Improvement: {old_score}% → {new_score}%

### Progressive Disclosure Enhanced
- {enhancement_1}
- {enhancement_2}
```

## Core Principles

**Self-Sufficient Building Blocks**:
- Standalone invocation
- Command orchestration
- Subagent integration
- Skill chaining

**Progressive Disclosure**:
- Tier 1: Always loaded (metadata)
- Tier 2: Loaded on activation (SKILL.md)
- Tier 3: On-demand (references/)

**Autonomy-First**:
- 80-95% completion without questions
- Clear triggers and preconditions
- Deterministic execution

## Routing Criteria

**Direct action** when:
- Simple skill instantiation
- Clear pattern application
- Standard structure generation

**Route to skills-knowledge** when:
- Creating new skills
- Auditing existing skills
- Refining skill architecture
- Progressive disclosure questions
- URL fetching requirements
